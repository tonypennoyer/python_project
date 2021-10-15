import tabula
import pandas as pd


def pdf_to_csv(url,file_name) :
	return tabula.convert_into(url, file_name, pages='all', area=[[71,33,540,660]], stream=True, guess=False)
	return file_name

def clean_data(file, date) :
	df = pd.read_csv(file,  error_bad_lines=False)

	df.rename(columns = {'Unnamed: 1': 'Cars'}, inplace=True)

	df[['Year','Make_and_Model']] = df['Cars'].str.split(' ', n = 1, expand = True)

	df.drop('Cars', axis=1, inplace = True)

	df['Date'] = date

	return df.to_csv(file)




