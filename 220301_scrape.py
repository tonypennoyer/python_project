from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException   
from selenium.common.exceptions import TimeoutException
import re 
import csv
import requests
import pandas as pd
from datetime import datetime
import numpy as np
import pickle
import time
import math
import os, glob
from time import sleep
from random import randint
from itertools import chain
from csv import writer
from bs4 import BeautifulSoup

def get_auction(soup) :
	auction = soup.title.text
	auction = auction.split(' ')
	auction_name = []
	for word in auction :
		if word == '|' :
			break
		else :
			auction_name.append(word)
	auction_name = '_'.join(auction_name)
	return auction_name

def get_yr_mdl_mk(headings) :
	Year_Model_and_Make = []
	for item in headings:
		Year_Model_and_Make.append(item.find('p', {'class':'heading-subtitle--bold ellipsis ng-binding'}).text)

	for c, string in enumerate(Year_Model_and_Make) :
		if string.split(' ')[0].isdigit() == False or len(string.split(' ')[0]) != 4:
			Year_Model_and_Make[c] = '0000 0000 0000'.split(' ',1)
		else : Year_Model_and_Make[c] = string.split(' ',1)

	print(Year_Model_and_Make)
	return Year_Model_and_Make

def get_sold(headings) :  

	sold = []
	
	keywords = ['Sold', 'Not Sold','Sold After Auction']
	pattern = re.compile('|'.join(keywords))

	for item in headings:
		item = item.text
		match = pattern.search(item)
		if match : 
			sold.append(match.group(0))
		if match is None :
			sold.append('Unknown')
	
	return sold

def get_price_and_lot(headings) :
	Price_and_Lot = []
	for item in headings:
			Price_and_Lot.append(item.find('span', {'class':'heading-subtitle--bold ng-binding'}).text)

	Price_and_Lot = [item.replace('GBP', r'').replace('EUR', r'').replace('USD',r'').replace('Lot',r'').replace(' ',r'').replace('\n',r'').strip().split('|') for item in Price_and_Lot]

	for string in Price_and_Lot :
		if len(string) == 1 :
			string.append('0000')
	
	if '$' in Price_and_Lot[0][0] and len(Price_and_Lot) == 1:
		single_price_lot = list(('1',Price_and_Lot[0][0]))
		Price_and_Lot = []
		Price_and_Lot.append(single_price_lot)
		
	return Price_and_Lot
def clean_price(Price) :
	Price = [item.replace(',','') for item in Price if item in Price]
	Price = [(re.sub(r"-.*",r"",string)) for string in Price]
	Price = [(re.sub(r".*Avail.*",r"0",string)) for string in Price]
	return Price

def get_price(Price) :  
	indicator = ''

	for string in Price :
		if '$' in string:
			Price = [item.replace('$','') for item in Price if item in Price] 
			Price = clean_price(Price)
		if 'CAD' in string:
			indicator = 'canadian'
			Price = [item.replace('CAD','') for item in Price if item in Price] 
			Price = clean_price(Price)
		elif 'CHF' in string:
			indicator = 'swiss'
			Price = [item.replace('CHF','') for item in Price if item in Price] 
			Price = clean_price(Price)
		elif 'GBP' in string:
			indicator = 'pound'
			Price = [item.replace('GBP','') for item in Price if item in Price] 
			Price = clean_price(Price)
		elif '€' in string:
			indicator = 'euro'
			Price = [item.replace('€','') for item in Price if item in Price] 
			Price = clean_price(Price)
		elif '£' in string:
			indicator = 'pound'
			Price = [item.replace('£','') for item in Price if item in Price] 
			Price = clean_price(Price)


	""" converts currency to USD (conversion rate taken Oct 15 via google) """
	Price = [item.replace('SoldAfterAuction','0') for item in Price]
	Price = [item.replace('PriceUponRequest','0') for item in Price]
	Price = list(map(float, Price))
	Price = list(map(float, Price))
	if indicator == 'euro' :
		Price = [num * 1.16 for num in Price]
	elif indicator == 'pound' :
		Price = [num * 1.38 for num in Price]
	elif indicator == 'swiss' :
		Price = [num * 1.08 for num in Price]
	elif indicator == 'canadian' :
		Price = [num * .79 for num in Price]

	price_list = list(map(round,Price))
	return price_list


# Take multiple date formats and making them standard datetime
def get_date(string) :
	string = string.strip()
	string = re.split(' |-',string)
	string = ' '.join(string).split()
	if len(string) == 4 :
		string = string[1:]
	elif len(string) == 5 :
		string = string[2:]
	string = '-'.join(string)
	dt = datetime.strptime(string, "%d-%B-%Y").date()
	return dt

def get_origin(make_list):
	pkl_file = open('car_list.pkl', 'rb')
	car_dict = pickle.load(pkl_file)

	country = []
	for item in make_list :
		car_origin = car_dict.get(item)
		if car_origin == None :
			country.append('Unknown')
		else : country.append(car_origin)

	pkl_file.close()
	pkl_file.close()
	return country

def make_soup_for_vin(url) :
	options = Options()
	options.headless = True

	DRIVER_PATH = '/Users/tonypennoyer/desktop/scraping/chromedriver'
	driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

	driver.get(url)

	soup = BeautifulSoup(driver.page_source, 'html.parser')
	driver.quit()
	return soup

def make_soup(url) :
	options = Options()
	options.headless = True

	DRIVER_PATH = '/Users/tonypennoyer/desktop/scraping/chromedriver'
	driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

	fetch_url = url

	driver.get(url)

	soup = BeautifulSoup(driver.page_source, 'html.parser')
	df = scrape_rm(soup)
	driver.quit()
	return df



def scrape_rm(soup) :
	Year_Model_and_Make = []
	sold_soup = []
	sold = []
	country_lst=['USD','EUR','GBP', 'CHF']
	no_error = 'no price'

	headings = soup.find_all('div', {'class': 'search-result__caption'})

	if not headings : ## Check if page is valid
		msg = 'done'
		return msg
	else :
		msg = 'still running'

	date_find = soup.find('div',{'class':'tile__subtitle mb-8px'}).text

	""" Assign correct date  """
	dt = get_date(date_find)

	""" Assign Auction name """
	auction_name = get_auction(soup)

	""" Assign correct sold marker """
	sold = get_sold(headings)

	""" separate year, model and make"""
	Year_Model_and_Make = get_yr_mdl_mk(headings)

	# Year, Model_and_Make = map(list,zip(*Year_Model_and_Make))
	Year = [i[0] for i in Year_Model_and_Make]
	Model_and_Make = [i[1] for i in Year_Model_and_Make]


	Model_and_Make = [item.split(' ',1) for item in Model_and_Make]
	Make = [i[0] for i in Model_and_Make]
	Model = [i[1] for i in Model_and_Make]

	# """ clean price and lot number"""
	Price_and_Lot = get_price_and_lot(headings)
	Lot = [i[0] for i in Price_and_Lot]
	Price = [i[1] for i in Price_and_Lot]

	""" Assign country origin of vehicle """
	country = get_origin(Make)

	""" Identifies currency, cleans string and converts to integer """
	prices = get_price(Price)

	""" Put auction and date in all columns """
	auc_name = []
	for x in range(len(Year)) :
		auc_name.append(auction_name)

	date = []
	for x in range(len(Year)) :
		date.append(dt)

	""" Put data in data frame """
	data = {'Lot': Lot, 'Price_USD': prices, 'Year': Year, 'Make': Make, 'Model': Model, 'Sold': sold,'Date': date, "Country": country, "Location": auc_name}
	df = pd.DataFrame.from_dict(data,orient='index')
	df = df.transpose()

	return df


def auction_iterator(year) :
	options = Options()
	options.headless = True

	DRIVER_PATH = '/Users/tonypennoyer/desktop/scraping/chromedriver'
	driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

	
	auction_year_url = 'https://rmsothebys.com/en/home/results/'+str(year)
	
	driver.get(auction_year_url)
	
	auction_links = []
	
	base = 'https://rmsothebys.com/'
	mid = '#?SortBy=Default&SearchTerm=&Category=All%20Categories&IncludeWithdrawnLots=false&Auction='
	end = '&OfferStatus=All%20Availability&AuctionYear=&Model=Model&Make=Make&FeaturedOnly=false&StillForSaleOnly=false&Collection=All%20Lots&WithoutReserveOnly=false&Day=All%20Days&TimedOnly=false&OneHubLinkOnly=false&InspectionReportOnly=false&AuctionedStatus=All%20Lots&page='
	
	elems = driver.find_elements_by_xpath("//a[@href]")
	for elem in elems:
		if elem.get_attribute("href").find('auction-results') != -1 :
			elem = elem.get_attribute("href")
			elem = elem + mid + elem[-4:].upper() + end
			auction_links.append(elem)
		else : continue
	
	return auction_links
	


def check_exists(xpath):
	try:
		driver.find_element_by_xpath(xpath)
	except NoSuchElementException:
		return False
	return True


def get_links(url) :
	options = Options()
	options.headless = True

	DRIVER_PATH = '/Users/tonypennoyer/desktop/scraping/chromedriver'
	driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

	driver.get(url)
	
	links = []
	
	elems = driver.find_elements_by_xpath("//a[@ng-href]")
	for elem in elems:
		links.append(elem.get_attribute("href"))
	
	links = list(set(links)) 
	driver.quit()
	return links

def get_vin(link_of_page) :

	options = Options()
	options.headless = True
	

	DRIVER_PATH = '/Users/tonypennoyer/desktop/scraping/chromedriver'
	driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)


	links = get_links(link_of_page)
	vin_lst = []
	lot_lst = []
	link_lst = []

	vin_check_lst = []

	for link in links :

		try :
			driver.get(link)
		except TimeoutException:
			print('time out')
			try:
				driver.get(link)
			except TimeoutException:
				print('time out 2')
				try:
					driver.get(link)
				except TimeoutException:
					print('timeout on get_vin')

		soup = BeautifulSoup(driver.page_source, 'html.parser')

		regex = '/+(....)+#'
		code= re.findall(regex, link)
		code = ''.join(code)

		try:
			driver.find_element_by_xpath('//*[@id="site-content"]/div[1]/div[4]/div/div/div[2]/section[2]/div/div[1]/div/div[1]/div[2]/div')
			exists = True
		except NoSuchElementException:
			try:
				driver.find_element_by_xpath('//*[@id="site-content"]/div[1]/div[4]/div/div/div[2]/section[2]/div/div[1]/div/div[1]/div[2]/div')
				exists = True
			except NoSuchElementException:
				try:
					driver.find_element_by_xpath('//*[@id="site-content"]/div/div[3]/div/div/div[2]/section[2]/div/div[1]/div/div[1]/div[2]/div')
					exists = True                 
				except NoSuchElementException:
					exists = False


		try :
			lot = soup.find('h3',{'class':'heading-details--bolder'}).text.strip().split(' ')
		except AttributeError :
			try :
				lot = soup.find('h3',{'class':'heading-details--bolder'}).text.strip().split(' ')
			except AttributeError :
				print('no lot text on this page')
		lot_check = any(lot in 'Lot' for lot in lot)
		vin_check_lst.append(exists)

		if exists == True and lot_check == True :
			vin = soup.find('div',{'class':'col-xs-8 col-sm-7 lot__specifications--right'}).text.strip()
			lot = [i for i in lot if i]
			lot = ' '.join(lot)
			lot = lot[lot.find('Lot')+4:]
			vin_lst.append(vin)
			lot_lst.append(lot)
			link_lst.append(link)
		 
		elif exists == True and lot_check == False :
			vin = soup.find('div',{'class':'col-xs-8 col-sm-7 lot__specifications--right'}).text.strip()
			lot = '1'
			lot_lst.append(lot)
			vin_lst.append(vin)
			link_lst.append(link)
	

		elif exists == False :
			lot_lst.append(None)
			vin_lst.append(None)
			link_lst.append(None)


	vin_df = pd.DataFrame(
		{'VIN': vin_lst,
		 'Lot': lot_lst,
		 'Link': link_lst,
		})

	driver.quit()
	return vin_df


def auction_pages(year) :

	main_links = auction_iterator(year)
	auction_count = len(main_links)
	current_count = 0

	end = '&pageSize=40'
	

	for auction in main_links:
		all_links_for_auction = []
		full_link = auction + str(1) + end
		soup = make_soup_for_vin(full_link)
		try :
			lot_count = soup.find('h3',{'class':'heading-content ng-binding'}).text.strip()
		except AttributeError :
			print('redo lot count')
			try :
				soup = make_soup_for_vin(full_link)
				lot_count = soup.find('h3',{'class':'heading-content ng-binding'}).text.strip()
			except AttributeError :
				print('redo lot count 2')
				try :
					soup = make_soup_for_vin(full_link)
					lot_count = soup.find('h3',{'class':'heading-content ng-binding'}).text.strip()
				except AttributeError :
					sleep(2)
					print('lot count failed')
					try :
						soup = make_soup_for_vin(full_link)
						lot_count = soup.find('h3',{'class':'heading-content ng-binding'}).text.strip()
					except AttributeError :
						sleep(2)
						print('redo lot count 2')
						try :
							soup = make_soup_for_vin(full_link)
							lot_count = soup.find('h3',{'class':'heading-content ng-binding'}).text.strip()
						except AttributeError :
							print('lot count failed')

		lot_count = str(lot_count)
		lot_count = int(lot_count.split(' ')[0])
		page_count = math.ceil(lot_count / 40)
		for n in range(1,page_count+1):
			all_links_for_auction.append(auction + str(n) + end)
		get_all(all_links_for_auction)
		current_count += 1
		print(str(current_count) + '/' + str(auction_count) + ' auctions done')


def get_all(all_auction_links) :
	for page, link in enumerate(all_auction_links) :
		page_num = page + 1
		full_link = link
		regex="/+(....)+#"
		code= re.findall(regex, full_link)
		code = ''.join(code)

		t0 = time.time()
		df = make_soup(full_link)   ######### GET ALL OTHER INFO
		t1 = time.time()
		total_make_soup = round(t1-t0)
		print(code + " make soup took " + str(total_make_soup) + " seconds long")

		try :
			if (df['Make'] == '0000').all() or (df['Price_USD'] < 8000).all() :
				print("these ain't cars - skipping page " + str(page_num))
				continue
		except TypeError:
			sleep(2)

		t2 = time.time()
		vin_df = get_vin(full_link) ######### GET VIN

		if vin_df.empty: ## IF PAGE IS ALL NULLS BREAK
			print('no vins on ' + code  +' page ' + str(page_num))
			continue

		t3 = time.time()
		total_get_vin= round(t3-t2)
		print("get vin took " + str(total_get_vin) + " seconds long")

		if isinstance(df, pd.DataFrame) == False : 
			print('Redoing make_soup..')
			t0 = time.time()
			try :
				df = make_soup(full_link)   ######### GET ALL OTHER INFO
			except IndexError :
				try :
					df = make_soup(full_link)
				except IndexError :
					print('model make index out of range investigate')

			t1 = time.time()
			total_make_soup = round(t1-t0)
			print("make soup redo took " + str(total_make_soup) + " seconds long")

		if isinstance(df, pd.DataFrame) == False : 
			print('Redoing page ' + str(page_num) + ' make_soup..')
			t0 = time.time()
			df = make_soup(full_link)   ######### GET ALL OTHER INFO
			t1 = time.time()
			total_make_soup = round(t1-t0)
			print("make soup redo took " + str(total_make_soup) + " seconds long")

		if isinstance(df, pd.DataFrame) == False : 
			print('Redoing page ' + str(page_num) + ' make_soup..')
			t0 = time.time()
			df = make_soup(full_link)   ######### GET ALL OTHER INFO
			t1 = time.time()
			total_make_soup = round(t1-t0)
			print("make soup redo took " + str(total_make_soup) + " seconds long")

		try:
			merged_df = pd.merge(df, vin_df, on='Lot')
		except TypeError :
			print('make_soup failed')
			

		try : 
			merged_df.to_csv('/Users/tonypennoyer/desktop/scraping/output/'+ code + '_' + str(page_num)+ '.csv')
		except AttributeError as ae:
			break
		print(code + ' page '+str(page_num) +' done')


def year_iterator(max_year) : # iterate through all rm auctions

	for i in range(2005,max_year) :
		auction_pages(i)


auction_pages(2012)
