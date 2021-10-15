from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re 
import csv
import requests
import pandas as pd
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


	sold_str = [item.split() for item in sold_soup]

	for lst in sold_str :
		for index, elem in enumerate(lst) :
			if (index+1 < len(lst) and index - 1 >= 0) :

				prev_el = str(lst[index-1])
				curr_el = str(elem)
				next_el = str(lst[index+1])

				if (prev_el == 'USD' or 'EUR' or 'GPB') and curr_el == 'Not' and next_el == 'Sold':
					sold.append(curr_el + ' ' + next_el)
				if (prev_el == 'USD' or 'EUR' or 'GPB') and curr_el == 'Sold' and next_el == 'Current:':
					sold.append(curr_el)
				if curr_el == 'Bid:' and next_el == 'Sold' :
					continue
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


	# """ Make date list match length with others """
	for i in range(len(Year)-1) :
		date += date

	""" Put data in data frame """
	data = {'Lot': Lot, 'Price': Price, 'Year': Year, 'Car': Car, 'Sold': sold, 'Date': date}
	df = pd.DataFrame.from_dict(data,orient='index')
	df = df.transpose()
	print(df.head(2))

make_soup('https://rmsothebys.com/en/home/auction-results/hf16')


# data = {'Lot': Price_Lots, 'Sold': sold, 'Make_and_model': Model_and_Make}
# df = pd.DataFrame(data=data)














