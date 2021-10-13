import camelot

tables = camelot.read_pdf('21_rm_ariz.pdf')
tables.export('21.csv', f='csv', compress=True)
