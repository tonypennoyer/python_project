from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re 
import csv
import requests
import pandas as pd
import numpy as np
from itertools import chain
from csv import writer
from bs4 import BeautifulSoup


def make_soup(url) :
	options = Options()
	options.headless = True

	DRIVER_PATH = '/Users/tonypennoyer/desktop/scraping/chromedriver'
	driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

	fetch_url = url

	driver.get(url)

	soup = BeautifulSoup(driver.page_source, 'html.parser')
	print('done1')
	scrape_rm(soup)



def scrape_rm(soup) :
	Price_Lots = []
	Model_and_Make = []
	sold_soup = []
	sold = []
	date = []
	country_lst=['USD','EUR','GPB']

	headings = soup.find_all('div', {'class': 'search-result__caption'})

	""" This section is to assign the correct date to our date list.
	this is based on the auctions date and name """
	auction = soup.title.text
	auction = auction.split(' ')
	if auction[0] == 'Hilton' :
		date.append('11/05/' + str(auction[2]))
	elif auction[0] == 'Hershey' :
		date.append('10/06/' + str(auction[1]))
	elif auction[0] == 'London' :
		date.append('09/07/' + str(auction[1]))
	elif auction[1] == 'Fall' :
		date.append('09/01/' + str(auction[2]))
	elif auction[0] == 'Monterey' :
		date.append('08/20/' + str(auction[1]))
	elif auction[0] == 'Motor' :
		date.append('07/30/' + str(auction[2]))
	elif auction[0] == 'Santa' :
		date.append('06/25/' + str(auction[2]))
	elif auction[0] == 'Monaco' :
		date.append('05/14/' + str(auction[1]))
	elif auction[1] == 'Spring' :
		date.append('05/05/' + str(auction[2]))
	elif auction[0] == 'Fort' :
		date.append('04/03/' + str(auction[2]))


	for item in headings:
		Price_Lots.append(item.find('span', {'class':'heading-subtitle--bold ng-binding'}).text)


	for item in headings:
		Model_and_Make.append(item.find('p', {'class':'heading-subtitle--bold ellipsis ng-binding'}).text)

	for item in headings:
		sold_soup.append(item.find('p', {'class':'clearfix'}).text)


	sold_lst = [item.split() for item in sold_soup]

	sold_lst = list(chain.from_iterable(sold_lst))

	# sold_lst = [item.replace('High','') for item in sold_lst]
	# sold_lst = [item.replace('bidder','') for item in sold_lst]
	# sold_lst = [item.replace('Bid:','') for item in sold_lst]

	# print(sold_lst)

	for index, elem in enumerate(sold_lst) :
		if (index+1 < len(sold_lst) and index - 1 >= 0) :

			prev_el = str(sold_lst[index-1])
			curr_el = str(elem)
			next_el = str(sold_lst[index+1])

			# print(curr_el)
			if prev_el in country_lst and curr_el == 'Sold' :
				sold.append('Sold')
			if prev_el in country_lst and curr_el == 'Not' and next_el == 'Sold':
				sold.append('Not Sold')
			else : continue


	# print(len(sold))

	""" Cleaning data section """
	Model_and_Make = [item.split(' ', 1) for item in Model_and_Make]

	Price_Lots = [item.replace('\n','') for item in Price_Lots]
	Price_Lots = [item.replace('Lot','') for item in Price_Lots]
	Price_Lots = [item.strip() for item in Price_Lots]
	Price_Lots = [item.replace(' ','') for item in Price_Lots]
	Price_Lots = [item.replace('USD','') for item in Price_Lots]
	Price_Lots = [item.replace('EUR','') for item in Price_Lots]
	Price_Lots = [item.replace('GBP','') for item in Price_Lots]
	Price_Lots = [item.split('|') for item in Price_Lots]

	# print(sold_str)

	""" Split up nested lists into separate ones """
	Lot, Price = zip(*Price_Lots)
	Year, Car = zip(*Model_and_Make)


	""" Make date list match length with others """
	date = date * len(Year)

	""" Put data in data frame """
	data = {'Lot': Lot, 'Price': Price, 'Year': Year, 'Cars': Car, 'Sold': sold,'Date': date}
	df = pd.DataFrame.from_dict(data,orient='index')
	df = df.transpose()

	# rnum = np.random.randint(1,1000,size=2)

	df.to_csv(str(np.random.randint(1,1000,size=1)) + '.csv')

make_soup('https://rmsothebys.com/en/home/auction-results/mo16#/&page=%7B2%7D?SortBy=Default&SearchTerm=&Category=All%20Categories&IncludeWithdrawnLots=false&Auction=MO16&OfferStatus=All%20Availability&AuctionYear=&Model=Model&Make=Make&FeaturedOnly=false&StillForSaleOnly=false&Collection=All%20Lots&WithoutReserveOnly=false&Day=All%20Days&TimedOnly=false&OneHubLinkOnly=false&InspectionReportOnly=false&AuctionedStatus=All%20Lots&page=3&pageSize=40')


# data = {'Lot': Price_Lots, 'Sold': sold, 'Make_and_model': Model_and_Make}
# df = pd.DataFrame(data=data)

# merge = pd.concat(
# 	map(pd.read_csv,['Mont_16_page_1.csv','Mont_16_page_2.csv','Mont_16_page_3.csv']), ignore_index=True)

# merge.to_csv('Mont16.csv')












