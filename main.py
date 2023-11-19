import requests
import string
from bs4 import BeautifulSoup
import pandas as pd

years = [year for year in range(2013, 2024)]
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
          'December']

dates = []
names = []
states = []

for year in years:
	for month in months:

		if year == 2023 and month == 'December':
			break

		current_link = f'https://en.wikipedia.org/wiki/List_of_killings_by_law_enforcement_officers_in_the_United_States,_{month}_{year}'
		response = requests.get(current_link)
		data = response.text
		soup = BeautifulSoup(data, 'html.parser')

		row_raw = soup.select('.wikitable > tbody > tr > td')
		row = [row.text.strip() for row in row_raw]

		dates.append(row[0])
		names.append(row[1])
		states.append(row[2])


data = {
	'Date': dates,
	'Name': names,
	'State': states
}
df = pd.DataFrame(data)

print(df)



