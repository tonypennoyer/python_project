import tabula

# df = tabula.read_pdf('21_rm_ariz.pdf', options="--columns 10.1,20.2,30.3", pages='all', stream=True,guess=False)

def pdf_to_csv(url,file_name) :
	tabula.convert_into(url, file_name, pages='all',  output_format="csv", stream=True, guess=False)

# tabula.convert_into('/Users/tonypennoyer/desktop/scraping/21_rm_ariz.pdf', 'test.csv', pages='all',  output_format="csv", stream=True,guess=False)

# pdf_to_csv('https://rmsothebys.com/media/229200/rm-sothebys-arizona-official-results-usd-by-result.pdf', 'rm_test.csv')

tabula.convert_into('21_rm_ariz.pdf', 'tony.csv', pages='all', area=[[71,33,540,660]], stream=True, guess=False)

