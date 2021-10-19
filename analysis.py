from matplotlib import pyplot as plt
import matplotlib
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
from datetime import datetime
import pandas as pd
import numpy as np
import csv
import re
import seaborn as sns
from scipy.stats import norm

df = pd.read_csv('RM_MASTER_LIST.csv', index_col=0, parse_dates=True)

mini = df[((df['Model'].str.contains('Mini')) | (df['Make'].str.contains('Mini'))) & (df['Make'].str.contains('Alfa') ==False) & 
	(df['Make'].str.contains('Honda') ==False) & (df['Make'].str.contains('Marcos') ==False) & (df['Make'].str.contains('ACOMA') ==False) & 
	(df['Make'].str.contains('Moretti') ==False) & (df['Make'].str.contains('Mickey') ==False) & (df['Make'].str.contains('Fiat') ==False)]

MG = df[((df['Model'].str.contains('MG')) | (df['Make'].str.contains('MG'))) & (df['Model'].str.contains('TD') ==True) & (df['Make'].str.contains('Mercedes-Benz') ==False) & 
	(df['Make'].str.contains('Tojeiro-MG') ==False) & (df['Make'].str.contains('Mercedes-AMG') ==False)]
p911 = df[df['Model'].str.contains('911') == True]
print(len(p911))
p911_sold = p911[p911['Sold'] == 'Sold']
p911_not_sold = p911[p911['Sold'] != 'Sold']
print(len(p911_not_sold))
mini_sold = mini[mini['Sold'] == 'Sold']
MG_sold = MG[MG['Sold'] == 'Sold']


small_cars = df[((df['Make'].str.contains('Ferves')) & (df['Model'].str.contains('Ranger'))) | ((df['Make'].str.contains('Fiat') & ((df['Model'].str.contains('500') | (df['Model'].str.contains('600'))))) | 
	(df['Make'].str.contains('Peel')) | (df['Model'].str.contains('Isetta')) | (df['Model'].str.contains('Kabinenroller')) | (df['Make'].str.contains('Goggomobil')) | 
	(df['Model'].str.contains('Bianchina')) | ((df['Make'].str.contains('Heinkel')) & (df['Model'].str.contains('Kabine'))))]
# print(small_cars)

# small_cars.to_csv('small_cars_check.csv')




""" Country Average """
# country_avg = df.groupby('Country', as_index=False)['Price_USD'].mean()

# germany_grouped = df[df["Country"] == "Germany"]
# g_avg = germany_grouped.groupby('Year', as_index=False)['Price_USD'].mean()

# USA_grouped = df[df["Country"] == "USA"]
# usa_avg = germany_grouped.groupby('Year', as_index=False)['Price_USD'].mean()

# Italy_grouped = df[df["Country"] == "Italy"]
# italy_avg = Italy_grouped.groupby('Year', as_index=False)['Price_USD'].mean()

# UK_grouped = df[df["Country"] == "UK"]
# uk_avg = UK_grouped.groupby('Year', as_index=False)['Price_USD'].mean()

# plt.plot(uk_avg.Year, uk_avg.Price_USD)
# plt.plot(usa_avg.Year, usa_avg.Price_USD)
# plt.plot(italy_avg.Year, italy_avg.Price_USD)
# plt.plot(g_avg.Year, g_avg.Price_USD)
# plt.show()
""" END """

""" 911 95' boxplot """
p911_sold = p911[p911['Sold'] == 'Sold']
# p911_95 = p911_sold[p911_sold['Year'] == 1995]
p911_73 = p911_sold[p911_sold['Year'] == 1973]
# p911_73.boxplot(column=['Price_USD'], return_type='axes');
# plt.ylabel('Price')
# plt.title('1973 Porsche 911')
# # plt.xlabel('Year Produced')
# plt.ylim(1,160000)
# plt.xticks([1], [''])
# plt.yticks([0,200000,400000,600000,800000,1000000,1200000,1400000,1600000], ['$0','$200K','$400K','$600K','$800K','$1M','$1,2M','$1.4M','$1.6M'])
# plt.show()



# p911_73_tour = p911_sold[(p911_sold['Year'] == 1973) & (p911_sold['Model'].str.contains('Touring'))]
# p911_73_tour.boxplot(column=['Price_USD'], return_type='axes');
# plt.ylabel('Price')
# plt.title('1973 Porsche 911 Carrera RS 2.7 Touring')
# # plt.xlabel('Year Produced')
# plt.ylim(1,160000)
# plt.xticks([1], [''])
# plt.yticks([0,200000,400000,600000,800000,1000000,1200000,1400000,1600000], ['$0','$200K','$400K','$600K','$800K','$1M','$1,2M','$1.4M','$1.6M'])
# plt.show()




# print(p911_73_tour['Price_USD'].describe())
# # p911_sold.sort_values(by=['Year'])
# p911_73.to_csv('yearcheck.csv')





""" All Average by year """
# avg_1 = df[(df['Year'] > 1900) & (df['Sold'] == 'Sold')]
# avg_2 = avg_1.groupby('Year', as_index=False)['Price_USD'].mean()
# df.groupby('Year', as_index=False)['Price_USD'].mean()
# avg_2.set_index('Year')['Price_USD'].plot.line(figsize=(12, 10), linewidth=2.5, color='#008000')
# plt.title('Average Price of Car by Year', y=1.02, fontsize=22)
# plt.xlabel("Year Produced", labelpad=15)
# plt.ylabel('Price')
# plt.ylim(0,1500000)
# plt.yticks([0,250000,500000,750000,1000000,1250000,1500000], ['$0','$250,000','$500,000','$750,000','$1,000,000','$1,250,000','$1,500,000'])
# plt.show()
""" END """

""" Water Cooled Vs. Air Cooled """
# aircooled = p911[p911['Year'] < 1998]
# aircooled_mean = aircooled['Price_USD'].mean()
# watercooled = p911[p911['Year'] > 1997]
# watercooled_mean = watercooled['Price_USD'].mean()

# wc_vs_ac = pd.DataFrame({
# 	'Air-cooled' : [aircooled_mean],
# 	'Water-cooled' : [watercooled_mean],
# 	}, index=[1])

# wc_vs_ac.plot.bar()
# plt.ylim(0,300000)
# plt.title('Porsche 911: Mean Price Sold')
# plt.ylabel('Price')
# plt.yticks([0,50000,100000,150000,200000,250000,300000], ['$0','$50,000','$100,000','$150,000','$200,000','$250,000','$300,000'])
# plt.show()
""" END """


""" BAR PLOT 911 AVERAGE BY YEAR PRODUCED """
# p91_yr_avg = p911.groupby('Year', as_index=False)['Price_USD'].mean()
# p91_yr_sold = p911.groupby('Date', as_index=False)['Price_USD'].mean()
# # p91_yr_avg.set_index('Year')
# p91_yr_avg.set_index('Year')['Price_USD'].plot.bar(figsize=(12, 10), linewidth=2.5, color='#800020')
# plt.title('Mean Price of Porsche 911 by Year', y=1.02, fontsize=22)
# plt.xlabel("Year", labelpad=15)
# plt.ylabel('Price')
# plt.legend()
# plt.ylim(0,800000)
# # plt.xticks(pYearValues)
# # plt.xticks([1960,1965,1970,1975,1980,1985,1990,1995,2000,2005,2010,2015,2020], ['1960','1965','1970','1975','1980','1985','1990','1995','2000','2005','2010','2015',
# # 	'2020'])
# plt.yticks([0,50000,100000,200000,300000,400000,500000,600000,700000,800000], ['$0','$50,000','$100,000','$200,000','$300,000','$400,000','$500,000','$600,000','$700,000','$800,000'])
# plt.show()
""" END """

""" Porsche 911 BOX PLOT """
# p911.boxplot(by='Year', column=['Price_USD'], grid = False)
# print(p911[p911['Price_USD'] > 750000])
# p911_sold.boxplot(column=['Price_USD'], return_type='axes');
# plt.ylabel('Price')
# plt.title('Porsche 911 Sales')
# plt.legend()
# plt.ylim(0,2750000)
# plt.xticks([1], [''])
# plt.yticks([0,250000,500000,750000,1000000,1250000,1500000,1750000,2000000,2250000,2500000,2750000], ['$0','$250K','$500K','$750K','$1M','$1.25M','$1.5M','$1.75M','$2M','$2.25M','$2.5M','$2.75M'])
# plt.show()
""" END """

""" Ferrari Box Plot """
# f40_sold = df[(df['Model'].str.contains('F40') == True) & (df['Sold'] == 'Sold')]
# f40_sold.boxplot(column=['Price_USD'], return_type='axes');
# plt.ylabel('Price')
# plt.title('Ferrari F40 Sales')
# plt.legend()
# plt.ylim(0,2750000)
# plt.xticks([1], [''])
# plt.yticks([0,250000,500000,750000,1000000,1250000,1500000,1750000,2000000,2250000,2500000,2750000], ['$0','$250K','$500K','$750K','$1M','$1.25M','$1.5M','$1.75M','$2M','$2.25M','$2.5M','$2.75M'])
# plt.show()
# f40.to_csv('checkcheck.csv')


# car_count = {'Country':['US','UK','Italy','Germany','France','Japan','Sweden','Spain','Austria','Belgium','Netherlands','Australia','Switzerland'],
# 			'Count': [98,45,39,22,22,11,6,2,1,1,1,1,1]}


# ccount_df = pd.DataFrame(car_count)

# plt.title('Car Companies Per Country')
# plt.bar(x=ccount_df['Country'],height=ccount_df['Count'])
# plt.gca().invert_xaxis()
# plt.show()
# USA,98
# UK 45
# Italy 39
# Germany 22
# France 22
# Japan 11
# Sweden 6
# Spain 2
# Austria 1
# Belgium 1
# Netherlands 1 
# Australia 1
# Switzerland 1






""" MINI BOX PLOT """
# mini_sold.boxplot(column=['Price_USD'], return_type='axes');
# MG_sold.boxplot(column=['Price_USD'], return_type='axes');
# plt.yticks([0,10000,20000,30000,40000], ['$0','$10K','$20K','$30K','$40K'])
# plt.ylabel('Price')
# plt.title('MG TD Sales')
# plt.xticks([1], [''])
# plt.show()
""" END """

""" Porsche 911 Strip Plot """
# sns.set_theme(style="whitegrid")
# ax = sns.stripplot(x='Sold',y="Price_USD",data=p911_sold)
# plt.show()
""" END """

""" Porsche 911 Scatter """
# p911_sold['Date']= pd.to_datetime(p911_sold['Date'])
# p911_not_sold['Date']= pd.to_datetime(p911_not_sold['Date'])
# sns.set_style('darkgrid')
# hey = sns.scatterplot(x='Date',y='Price_USD',data=p911_sold,s=50,alpha=1,color="black")
# hi= sns.scatterplot(x='Date', y='Price_USD',data=p911_not_sold, s=50, alpha=0.5,color='grey')
# plt.title('Porsche 911 Sales: 2016 - 2021', y=1.02, fontsize=14)
# plt.ylabel('Price')
# plt.xlabel('Year Sold')
# plt.legend(labels=["Sold","Not Sold"])

# # print(p911_sold.info())
# # # start, end = ax.get_xlim()
# # # plt.xlim('2021-01-01')
# # # plt.xticks([2016,2017,2018,2019,2020,2021],['2016','2017','2018','2019','2020','2021'])
# # # plt.xticks(np.arange(min(p911_sold['Year'], max(p911_sold['Year']))))
# hey.get_figure().autofmt_xdate()
# hi.get_figure().autofmt_xdate()
# plt.ylim(3500000)
# plt.yticks([0,250000,500000,750000,1000000,1250000,1500000,1750000,2000000,2250000,2500000,2750000,3000000,3250000,3500000], ['$0','$250K','$500K','$750K','$1M','$1.25M','$1.5M','$1.75M','$2M','$2.25M','$2.5M','$2.75M','$3M','$3.25M','$3.5M'])
# plt.show()
""" END """

""" mini scatter """
print(mini_sold['Price_USD'].describe())
mini_sold = mini[mini['Sold'] == 'Sold']
mini_not_sold = mini[mini['Sold'] != 'Sold']
mini_sold['Date']= pd.to_datetime(mini_sold['Date'])
mini_not_sold['Date']= pd.to_datetime(mini_not_sold['Date'])
sns.set_style('darkgrid')
sold_ = sns.scatterplot(x='Date',y='Price_USD',data=mini_sold,s=50,alpha=1,color="green")
not_sold = sns.scatterplot(x='Date', y='Price_USD',data=mini_not_sold, s=50, alpha=0.5,color='grey')
plt.title('Mini Sales: 2016 - 2021', y=1.02, fontsize=14)
sold_.get_figure().autofmt_xdate()
not_sold.get_figure().autofmt_xdate()
 plt.ylim(3500000)
plt.yticks([0,250000,500000,750000,1000000,1250000,1500000,1750000,2000000,2250000,2500000,2750000,3000000,3250000,3500000], ['$0','$250K','$500K','$750K','$1M','$1.25M','$1.5M','$1.75M','$2M','$2.25M','$2.5M','$2.75M','$3M','$3.25M','$3.5M'])
plt.show()
plt.ylabel('Price')
plt.xlabel('Year Sold')
plt.legend(labels=["Sold","Not Sold"])
plt.show()
""" END """

# micro_sold = small_cars[small_cars['Sold'] == 'Sold']
# micro_not_sold = small_cars[small_cars['Sold'] != 'Sold']
# micro_sold['Date']= pd.to_datetime(micro_sold['Date'])
# micro_not_sold['Date']= pd.to_datetime(micro_not_sold['Date'])
# sns.set_style('darkgrid')
# sold_ = sns.scatterplot(x='Date',y='Price_USD',data=micro_sold,s=50,alpha=1,color="blue")
# not_sold = sns.scatterplot(x='Date', y='Price_USD',data=micro_not_sold, s=50, alpha=0.5,color='grey')
# plt.title('Microcar Sales: 2016 - 2021', y=1.02, fontsize=14)
# sold_.get_figure().autofmt_xdate()
# not_sold.get_figure().autofmt_xdate()
# plt.ylabel('Price')
# plt.xlabel('Year Sold')
# plt.legend(labels=["Sold","Not Sold"])
# plt.show()


# """ ALL CARS SCATTER """
american = small_cars[small_cars['Sold'] == 'Sold']
# american_2 = df[(df['Country'] == 'USA') & (df['Sold'] == 'Sold')]
# p911 = df[(df['Country'].str.contains('Germany') == True) & (df['Sold'] == 'Sold')]
# ital = df[(df['Country'].str.contains('Italy') == True) & (df['Sold'] == 'Sold')]

# uk_16 = american[american['Date'].str.contains('2016')]
# uk_16_avg = uk_16["Price_USD"].mean()
# uk_17 = american[american['Date'].str.contains('2017')]
# uk_17_avg = uk_17["Price_USD"].mean()
# uk_18 = american[american['Date'].str.contains('2018')]
# uk_18_avg = uk_18["Price_USD"].mean()
# uk_19 = american[american['Date'].str.contains('2019')]
# uk_19_avg = uk_19["Price_USD"].mean()
# uk_20 = american[american['Date'].str.contains('2020')]
# uk_20_avg = uk_20["Price_USD"].mean()
# uk_21 = american[american['Date'].str.contains('2021')]
# uk_21_avg = uk_21["Price_USD"].mean()

# us_16 = american_2[american_2['Date'].str.contains('2016')]
# us_16_avg = us_16["Price_USD"].mean()
# us_17 = american_2[american_2['Date'].str.contains('2017')]
# us_17_avg = us_17["Price_USD"].mean()
# us_18 = american_2[american_2['Date'].str.contains('2018')]
# us_18_avg = us_18["Price_USD"].mean()
# us_19 = american_2[american_2['Date'].str.contains('2019')]
# us_19_avg = us_19["Price_USD"].mean()
# us_20 = american_2[american_2['Date'].str.contains('2020')]
# us_20_avg = us_20["Price_USD"].mean()
# us_21 = american_2[american_2['Date'].str.contains('2021')]
# us_21_avg = us_21["Price_USD"].mean()

# p911_16 = p911[p911['Date'].str.contains('2016') == True]
# p911_16_avg_price = p911_16["Price_USD"].mean()

# p911_17 = p911[p911['Date'].str.contains('2017') == True]
# p911_17_avg_price = p911_17["Price_USD"].mean()

# p911_18 = p911[p911['Date'].str.contains('2018') == True]
# p911_18_avg_price = p911_18["Price_USD"].mean()

# p911_19 = p911[p911['Date'].str.contains('2019') == True]
# p911_19_avg_price = p911_19["Price_USD"].mean()

# p911_20 = p911[p911['Date'].str.contains('2020') == True]
# p911_20_avg_price = p911_20["Price_USD"].mean()

# p911_21 = p911[p911['Date'].str.contains('2021') == True]
# p911_21_avg_price = p911_21["Price_USD"].mean()

# ital_16 = ital[ital['Date'].str.contains('2016') == True]
# ital_16_avg_price = ital_16["Price_USD"].mean()

# ital_17 = ital[ital['Date'].str.contains('2017') == True]
# ital_17_avg_price = ital_17["Price_USD"].mean()

# ital_18 = ital[ital['Date'].str.contains('2018') == True]
# ital_18_avg_price = ital_18["Price_USD"].mean()

# ital_19 = ital[ital['Date'].str.contains('2019') == True]
# ital_19_avg_price = ital_19["Price_USD"].mean()

# ital_20 = ital[ital['Date'].str.contains('2020') == True]
# ital_20_avg_price = ital_20["Price_USD"].mean()

# ital_21 = ital[ital['Date'].str.contains('2021') == True]
# ital_21_avg_price = ital_21["Price_USD"].mean()


avg_cars_price = pd.DataFrame({
	'UK' : [uk_16_avg,uk_17_avg,uk_18_avg,uk_19_avg,uk_20_avg,uk_21_avg]
# 	'USA' : [us_16_avg,us_17_avg,us_18_avg,us_19_avg,us_20_avg,us_21_avg],
# 	# 'Germany' : [p911_16_avg_price,p911_17_avg_price,p911_18_avg_price,p911_19_avg_price,p911_20_avg_price,p911_21_avg_price],
# 	# 'Italy' : [ital_16_avg_price,ital_17_avg_price,ital_18_avg_price,ital_19_avg_price,ital_20_avg_price,ital_21_avg_price]
	}, index=[2016,2017,2018,2019,2020,2021])


# plt.plot(avg_cars_price,marker='.',)
# # plt.legend()
# plt.ylim(75000)
# plt.title('Microcars Average Price')
# plt.xlabel('Year Sold')
# # plt.legend(['USA','Germany']);
# plt.ylabel('Price')
# plt.gca().invert_yaxis()
# plt.yticks([0,25000,50000,75000], ['$0','$25K','$50K','$75K'])
# plt.show()




# usa_sold['Date']= pd.to_datetime(p911_sold['Date'])
# p911_not_sold['Date']= pd.to_datetime(p911_not_sold['Date'])
# sns.set_style('darkgrid')
# hey = sns.scatterplot(x='Date',y='Price_USD',data=p911_sold,s=50,alpha=1,color="black")
# hi= sns.scatterplot(x='Date', y='Price_USD',data=p911_not_sold, s=50, alpha=0.5,color='grey')
# plt.title('Porsche 911 Sales: 2016 - 2021', y=1.02, fontsize=14)
# plt.ylabel('Price')
# plt.xlabel('Year Sold')
# plt.legend(labels=["Sold","Not Sold"])

# print(p911_sold.info())
# # start, end = ax.get_xlim()
# # plt.xlim('2021-01-01')
# # plt.xticks([2016,2017,2018,2019,2020,2021],['2016','2017','2018','2019','2020','2021'])
# # plt.xticks(np.arange(min(p911_sold['Year'], max(p911_sold['Year']))))
# hey.get_figure().autofmt_xdate()
# hi.get_figure().autofmt_xdate()
# plt.ylim(3500000)
# plt.yticks([0,250000,500000,750000,1000000,1250000,1500000,1750000,2000000,2250000,2500000,2750000,3000000,3250000,3500000], ['$0','$250K','$500K','$750K','$1M','$1.25M','$1.5M','$1.75M','$2M','$2.25M','$2.5M','$2.75M','$3M','$3.25M','$3.5M'])
# plt.show()


""" stats for 911 sold """
# quantiles = p911_sold['Price_USD'].quantile([0.01, 0.25, 0.5, 0.75, 0.99])
# print(quantiles)
# print('The mean is: ',p911_sold['Price_USD'].mean())
# print('The media is:', p911_sold['Price_USD'].median())
# print('The standard deviation is: ',np.std(p911_sold['Price_USD']))
# print(p911['Price_USD'].std())
# mean = 263225
# SD = 381339
# one_sd = norm.cdf(SD, mean, SD) - norm.cdf(-SD, mean, SD)
# two_sd = norm.cdf(2 * SD, mean, SD) - norm.cdf(-2 * SD, mean, SD)
# three_sd = norm.cdf(3 * SD, mean, SD) - norm.cdf(-3 * SD, mean, SD)
# print("Fraction of values within one SD =", one_sd)
# print("Fraction of values within two SD =", two_sd)
# print("Fraction of values within three SD =", three_sd)




# p91_yr_sold.set_index('Date')['Price_USD'].plot(figsize=(12, 10), linewidth=2.5, color='#800020')
# plt.title('Mean Price Sold by Auction Date', y=1.02, fontsize=22)
# plt.xlabel("Year", labelpad=15)
# plt.ylabel('Price')
# plt.legend()
# plt.ylim(0,1000000)
# plt.show()


dusenberg = df[df['Make'].str.contains('Ferrari') == True]
# f40 = df[df['Location'].str.contains('Scottsdale,AZ') == True]
# ital = df[df['Location'].str.contains('Amelia Island,FL') == True]






# sns.set_style('dark')
# sns.scatterplot(x='Year',y='Price_USD',data=p911,s=50,alpha=0.6,color="#800020")
# plt.title('Porsche 911: 2016 - 2021', y=1.02, fontsize=14)
# plt.ylabel('Price')
# plt.xlabel('Year Produced')
# plt.ylim(1,120000)
# plt.yticks([0,100000,200000,300000,400000,500000,600000,700000,800000,900000,1000000,1100000,1200000], ['$0','$100,000','$200,000','$300,000','$400,000','$500,000','$600,000','$700,000','$800,000','$900,000','$1,000,000','$1,100,000','$1,200,000'])
# plt.show()
































# print(f40)

# p911.sort_values(by=['Year'])

# p911_by_date = p911.groupby('Date', as_index=False)['Price_USD'].mean()
# # print(testdf)
# p911_by_date.set_index('Date')['Price_USD'].plot.bar(figsize=(12, 10), linewidth=2.5, color='#800020')
# # plt.plot.bar(p911_by_date.Date, p911_by_date.Price_USD, label="Price")

# plt.title('Average Price of Porsche 911')
# plt.ylabel('Price in USD')
# plt.legend()
# # plt.xlim('2016-01-01','2021-12-12')

# plt.show()


# f40_16 = f40[f40['Date'].str.contains('2016') == True]
# f40_16_avg_price = f40_16["Price_USD"].mean()

# f40_17 = f40[f40['Date'].str.contains('2017') == True]
# f40_17_avg_price = f40_17["Price_USD"].mean()

# f40_18 = f40[f40['Date'].str.contains('2018') == True]
# f40_18_avg_price = f40_18["Price_USD"].mean()

# f40_19 = f40[f40['Date'].str.contains('2019') == True]
# f40_19_avg_price = f40_19["Price_USD"].mean()

# f40_20 = f40[f40['Date'].str.contains('2020') == True]
# f40_20_avg_price = f40_20["Price_USD"].mean()

# f40_21 = f40[f40['Date'].str.contains('2021') == True]
# f40_21_avg_price = f40_21["Price_USD"].mean()






# ital_16 = ital[ital['Date'].str.contains('2016') == True]
# ital_16_avg_price = ital_16["Price_USD"].mean()

# ital_17 = ital[ital['Date'].str.contains('2017') == True]
# ital_17_avg_price = ital_17["Price_USD"].mean()

# ital_18 = ital[ital['Date'].str.contains('2018') == True]
# ital_18_avg_price = ital_18["Price_USD"].mean()

# ital_19 = ital[ital['Date'].str.contains('2019') == True]
# ital_19_avg_price = ital_19["Price_USD"].mean()

# ital_20 = ital[ital['Date'].str.contains('2020') == True]
# ital_20_avg_price = ital_20["Price_USD"].mean()

# ital_21 = ital[ital['Date'].str.contains('2021') == True]
# ital_21_avg_price = ital_21["Price_USD"].mean()

# p911_16 = p911[p911['Date'].str.contains('2016') == True]
# p911_16_avg_price = p911_16["Price_USD"].mean()

# p911_17 = p911[p911['Date'].str.contains('2017') == True]
# p911_17_avg_price = p911_17["Price_USD"].mean()

# p911_18 = p911[p911['Date'].str.contains('2018') == True]
# p911_18_avg_price = p911_18["Price_USD"].mean()

# p911_19 = p911[p911['Date'].str.contains('2019') == True]
# p911_19_avg_price = p911_19["Price_USD"].mean()

# p911_20 = p911[p911['Date'].str.contains('2020') == True]
# p911_20_avg_price = p911_20["Price_USD"].mean()

# p911_21 = p911[p911['Date'].str.contains('2021') == True]
# p911_21_avg_price = p911_21["Price_USD"].mean()

# porsche_mean_price_per_year.plot.line(color={'Mean Price':'#742802'})
# f40_mean_price_per_year.plot.line(color={'Mean Price':'#FF0000'})

# avg_cars_price = pd.DataFrame({
# 	'Scottsdale, AZ' : [f40_16_avg_price,f40_17_avg_price,f40_18_avg_price,f40_19_avg_price,f40_20_avg_price,f40_21_avg_price],
# 	# 'Monterey, CA' : [p911_16_avg_price,p911_17_avg_price,p911_18_avg_price,p911_19_avg_price,p911_20_avg_price,p911_21_avg_price],
# 	'Amelia Island, FL' : [ital_16_avg_price,ital_17_avg_price,ital_18_avg_price,ital_19_avg_price,ital_20_avg_price,ital_21_avg_price]
# 	}, index=[2016,2017,2018,2019,2020,2021])

# avg_cars_price.plot.line(style='.-')

# plt.title('Mean Price Per Year')
# plt.ylabel('Price in Millions')
# plt.legend()
# plt.ylim(0,800000)
# plt.yticks([0,200000,400000,600000,800000], ['$0','$200,000','$400,000','$600,000','$800,000'])


# plt.show()




# porsche_mean_price_per_year = pd.DataFrame({
# 	'Mean Price': [p911_16_avg_price,p911_17_avg_price,p911_18_avg_price,p911_19_avg_price,p911_20_avg_price,p911_21_avg_price],
# 	}, index=[2016,2017,2018,2019,2020,2021])

# porsche_mean_price_per_year.plot.line(color={'Mean Price':'#742802'})
# plt.show()







# p911_16.to_csv('p_16.csv')
# print(p911_year.index.year)



# p911_16 = p911[p911['Year'].str.contains()]











# df.plot.scatter(x='Year',y='Price_USD')
# plt.show()

# lk = df.groupby("Location")

# pebble = lk.get_group('Monterey,CA')


# date_peb =  pebble.groupby("Date")

# # date_peb.plot.scatter(x="Date", y="Price_USD", alpha=0.5)
# # plt.show()

# pebble16 = date_peb.get_group('2016-08-20')
# p16_avg = int(pebble16["Price_USD"].mean())
# pebble17 = date_peb.get_group('2017-08-20')
# p17_avg = int(pebble17["Price_USD"].mean())
# pebble18 = date_peb.get_group('2018-08-20')
# p18_avg = int(pebble18["Price_USD"].mean())
# pebble19 = date_peb.get_group('2019-08-20')
# p19_avg = int(pebble19["Price_USD"].mean())
# # pebble20 = date_peb.get_group('2016-08-20')
# pebble21 = date_peb.get_group('2021-08-20')
# p21_avg = int(pebble21["Price_USD"].mean())

# date_peb.plot.scatter(x="2016-08-20", y="Price_USD", alpha=0.5)
# plt.show()


# pebble.groupby('Date')['Price_USD'].sum().plot.bar(figsize=(8, 8), fontsize=8, yticks = range(0,100000000,50000000))


# # pebble19.plot.bar(x='Country', y='Price_USD')
# plt.show()

# print(p16_avg,p17_avg,p18_avg)


# print(pebble.get_group('2016-08-20').sum())

# x = np.arrange('2016-08-20', '2021-08-20')
# y = np.arrange(0,100000000)
 
# # plotting
# plt.title("Line graph")
# plt.xlabel("Date")
# plt.ylabel("Price")
# plt.plot(x, y, color ="red")
# plt.show()

# mont.to_csv('UPDATED.csv')