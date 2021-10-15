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

	headings = soup.find_all('div', {'class': 'search-result__caption'})

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
				elif (prev_el == 'USD' or 'EUR' or 'GPB') and curr_el == 'Sold' :
					sold.append(curr_el)
				else : continue

	print(sold)
	Price_Lots = [item.replace('\n','') for item in Price_Lots]
	Price_Lots = [item.replace('Lot','') for item in Price_Lots]
	Price_Lots = [item.strip() for item in Price_Lots]
	Price_Lots = [item.replace(' ','') for item in Price_Lots]
	Price_Lots = [item.replace('USD','') for item in Price_Lots]
	Price_Lots = [item.replace('EUR','') for item in Price_Lots]
	Price_Lots = [item.replace('GBP','') for item in Price_Lots]
	Price_Lots = [item.split('|') for item in Price_Lots]
	print(Price_Lots)

# make_soup('https://rmsothebys.com/en/home/auction-results/mo16')
make_soup('https://rmsothebys.com/en/home/auction-results/lf16')


# data = {'Lot': Price_Lots, 'Sold': sold, 'Make_and_model': Model_and_Make}
# df = pd.DataFrame(data=data)














