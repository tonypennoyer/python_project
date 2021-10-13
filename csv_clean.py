import pandas as pd


df = pd.read_csv('21_rmPebble.csv', error_bad_lines=False)

print(df.columns)

df.rename(columns = {'Unnamed: 1': 'Cars'}, inplace=True)

df[['Year','Make_and_Model']] = df['Cars'].str.split(' ', n = 1, expand = True)

df.drop('Cars', axis=1, inplace = True)
df.drop('Sold', axis=1, inplace = True)

df['Date'] = '01/01/2021'

 df.to_csv('new_pebble.csv')