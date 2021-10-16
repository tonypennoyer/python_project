import pandas as pd
import numpy as np
import csv
import re

def final_clean(csv_file):
	df = pd.read_csv(csv_file)

	df = df[df['Make'] != 'No']

	df = df[df['Price_USD'] != 0]

	df = df[df['Date'] != '12/11/|']

	df = df[df['Price_USD'] > 3000]

	df = df[df["Year"].str.contains('½','310')==False]

	df = df[df["Lot"].str.contains('N')==False]

	df = df[df['Year'] != '5']
	df = df[df['Year'] != '24']
	df = df[df['Year'] != '312']
	df = df[df['Year'] != '270']
	df = df[df['Year'] != '330']

	df = df[df['Year'].str.isnumeric()]

	pd.to_numeric(df['Year'], downcast='integer')

	mcoun = "'Missing'"

	df['Country'].fillna(value='Missing', inplace=True)

	df['Sold'].fillna(value='Sold', inplace=True)

	df["Date"] = pd.to_datetime(df["Date"])

	df["Year"] = df['Year'].astype('int')

	print(df["Price_USD"].max())

	print(df.dtypes)

	print(df.isna().sum())

	df = df.sort_values(by=['Date'],ascending=False)

	df.to_csv('UPDATED.csv', index=False) 




