from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re 
import csv
import requests
import pandas as pd
import numpy as np
import pickle
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
	country = []
	country_lst=['USD','EUR','GPB', 'CHF']

	headings = soup.find_all('div', {'class': 'search-result__caption'})

	""" Assign correct date  """
	auction = soup.title.text
	auction = auction.split(' ')
	print(auction)
	if auction[0] == 'Hilton' :
		date.append('11/05/' + str(auction[2]))
	elif auction[0] == 'Hershey' :
		date.append('10/06/' + str(auction[1]))
	elif auction[1] == 'Moritz' :
		date.append('09/17/' + str(auction[2]))
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
	elif auction[0] == 'Arizona' :
		date.append('01/29/' + str(auction[1]))
	elif auction[3] == 'Museum' :
		date.append('12/08/' + str(auction[5]))
	elif auction[2] == '70th' :
		date.append('10/27/' + str(auction[5]))
	elif auction[1] == 'Dingman' :
		date.append('06/23/' + str(auction[3]))
	elif auction[5] == 'Holidays' :
		date.append('12/11/' + str(auction[6]))
	elif auction[1] == 'Dhabi' :
		date.append('11/30/' + str(auction[2]))
	elif auction[3] == 'Garaj' :
		date.append('09/28/' + str(auction[5]))
	elif auction[1] == 'Saragga' :
		date.append('09/21/' + str(auction[3]))
	elif auction[1] == 'Erba' :
		date.append('05/25/' + str(auction[2]))
	elif auction[1] == 'Guyton' :
		date.append('05/04/' + str(auction[3]))
	elif auction[0] == 'Essen' :
		date.append('04/11/' + str(auction[1]))
	elif auction[1] == 'Elkhart' :
		date.append('10/23/' + str(auction[3]))
	elif auction[1] == 'Mitosinka' :
		date.append('09/25/' + str(auction[3]))
	elif auction[0] == 'Shift/monterey' :
		date.append('08/14/' + str(auction[1]))
	elif auction[4] == 'Petitjean' :
		date.append('06/03/2020')



	""" Find all text from soup """
	for item in headings:
		Price_Lots.append(item.find('span', {'class':'heading-subtitle--bold ng-binding'}).text)

	for item in headings:
		Model_and_Make.append(item.find('p', {'class':'heading-subtitle--bold ellipsis ng-binding'}).text)

	for item in headings:
		sold_soup.append(item.find('p', {'class':'clearfix'}).text)

	""" Assign correct sold marker """
	sold_lst = [item.split() for item in sold_soup]
	sold_lst = list(chain.from_iterable(sold_lst))

	for index, elem in enumerate(sold_lst) :
		if (index+1 < len(sold_lst) and index - 1 >= 0) :

			prev_el = str(sold_lst[index-1])
			curr_el = str(elem)
			next_el = str(sold_lst[index+1])

			# print(curr_el)
			if prev_el in country_lst and curr_el == 'Sold' :
				sold.append('Sold')
			elif prev_el[0] == 'C' and curr_el == 'Sold' :
				sold.append('Sold')
			if prev_el in country_lst and curr_el == 'Not' and next_el == 'Sold':
				sold.append('Not Sold')
			elif prev_el[0] == 'C' and curr_el == 'Not' and next_el == 'Sold':
				sold.append('Not Sold')
			else : continue

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


	""" Split up nested lists into separate ones """
	Lot, Price = zip(*Price_Lots)
	Year, Car = zip(*Model_and_Make)

	""" Split car make and model """
	Car = [item.split(' ',1) for item in Car]
	Make, Model = zip(*Car)

	""" Assign country origin of vehicle """
	pkl_file = open('car_list.pkl', 'rb')
	car_dict = pickle.load(pkl_file)

	pkl_file = open('master_lst.pkl', 'rb')
	master_lst = pickle.load(pkl_file)


	for item in Make :
		if item not in master_lst : 
			country.append('Missing')
		for k in car_dict['USA'] :
			if k == item :
				country.append('USA')
		for k in car_dict['UK'] :
			if k == item :
				country.append('UK')
		for k in car_dict['Italy'] :
			if k == item :
				country.append('Italy')
		for k in car_dict['Germany'] :
			if k == item :
				country.append('Germany')
		for k in car_dict['France'] :
			if k == item :
				country.append('France')
		for k in car_dict['Japan'] :
			if k == item :
				country.append('Japan')
		for k in car_dict['Sweden'] :
			if k == item :
				country.append('Sweden')
		for k in car_dict['Spain'] :
			if k == item :
				country.append('Spain')
		for k in car_dict['Austria'] :
			if k == item :
				country.append('Austria')
		for k in car_dict['UK_Italy'] :
			if k == item :
				country.append('UK_Italy')

	print(country)

	pkl_file.close()
	pkl_file.close()

	""" Identifies currency, cleans string and converts to integer """
	indicator = ''

	for string in Price :
		if '$' in string:
			Price = [item.replace('$','') for item in Price if item in Price] 
			Price = [item.replace(',','') for item in Price if item in Price]
			Price = [(re.sub(r"-.*",r"",string)) for string in Price]
			Price = [(re.sub(r".*Avail.*",r"0",string)) for string in Price]
		elif 'CHF' in string:
			indicator = 'swiss'
			Price = [item.replace('CHF','') for item in Price if item in Price] 
			Price = [item.replace(',','') for item in Price if item in Price]
			Price = [(re.sub(r"-.*",r"",string)) for string in Price]
			Price = [(re.sub(r".*Avail.*",r"0",string)) for string in Price]
		elif 'GBP' in string:
			indicator = 'pound'
			Price = [item.replace('GBP','') for item in Price if item in Price] 
			Price = [item.replace(',','') for item in Price if item in Price]
			Price = [(re.sub(r"-.*",r"",string)) for string in Price]
			Price = [(re.sub(r".*Avail.*",r"0",string)) for string in Price]
		elif '€' in string:
			indicator = 'euro'
			Price = [item.replace('€','') for item in Price if item in Price] 
			Price = [item.replace(',','') for item in Price if item in Price]
			Price = [(re.sub(r"-.*",r"",string)) for string in Price]
			Price = [(re.sub(r".*Avail.*",r"0",string)) for string in Price]
		elif '£' in string:
			indicator = 'pound'
			Price = [item.replace('£','') for item in Price if item in Price] 
			Price = [item.replace(',','') for item in Price if item in Price]
			Price = [(re.sub(r"-.*",r"",string)) for string in Price]
			Price = [(re.sub(r".*Avail.*",r"0",string)) for string in Price]


	""" converts currency to USD (conversion rate taken Oct 15 via google) """
	Price = list(map(int, Price))
	Price = list(map(float, Price))
	if indicator == 'euro' :
		Price = [num * 1.16 for num in Price]
	elif indicator == 'pound' :
		Price = [num * 1.38 for num in Price]
	elif indicator == 'swiss' :
		Price = [num * 1.08 for num in Price]
	Price = list(map(round,Price))

	""" Date array match length of others """
	date = date * len(Year)

	""" Put data in data frame """
	data = {'Lot': Lot, 'Price_USD': Price, 'Year': Year, 'Make': Make, 'Model': Model, 'Sold': sold,'Date': date, "Country": country}
	df = pd.DataFrame.from_dict(data,orient='index')
	df = df.transpose()

	""" Assign random variable to save .csv """
	rnum = np.random.randint(1,1000,size=2)

	df.to_csv(str(np.random.randint(1,1000,size=1)) + '.csv')

make_soup('https://rmsothebys.com/en/home/auction-results/es20')


# data = {'Lot': Price_Lots, 'Sold': sold, 'Make_and_model': Model_and_Make}
# df = pd.DataFrame(data=data)

""" Merges csvs """

# merge = pd.concat(
# 	map(pd.read_csv,['[543].csv','[577].csv','[719].csv','[825].csv']), ignore_index=True)

# merge.to_csv('Arizona16.csv',index=False)












