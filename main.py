import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

years = [year for year in range(2013, 2016)]
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
          'December']

dates = []
names = []
states = []
years_col = []


def search():
	for year in years:
		for month in months:

			if year == 2023 and month == 'December':
				break

			current_link = f'https://en.wikipedia.org/wiki/List_of_killings_by_law_enforcement_officers_in_the_United_States,_{month}_{year}'
			response = requests.get(current_link)
			data = response.text
			soup = BeautifulSoup(data, 'html.parser')

			table_raw = soup.select('.wikitable > tbody > tr > td')
			table = [row.text.strip() for row in table_raw]
			for index in range(len(table)):
				if index % 4 == 0:
					dates.append(table[index])
				elif index % 4 == 1:
					if table[index] == 'California (Fresno)':
						print(table[index - 1])
					names.append(table[index])
				elif index % 4 == 2:
					states.append(table[index])

			print(f'Progress: {month} | {year}')

	if len(dates) > len(names):
		for index in range(len(dates) - len(names)):
			names.append('')
	elif len(names) > len(dates):
		for index in range(len(names) - len(dates)):
			dates.append('')

	if len(dates) > len(states):
		for index in range(len(dates) - len(states)):
			states.append('')
	elif len(states) > len(dates):
		for index in range(len(states) - len(dates)):
			dates.append('')

	if len(names) > len(states):
		for index in range(len(names) - len(states)):
			states.append('')
	elif len(states) > len(names):
		for index in range(len(states) - len(names)):
			names.append('')

	print(f'Dates: {len(dates)}')
	print(f'Names: {len(names)}')
	print(f'States: {len(states)}')

	data = {
		'Date': dates,
		'Name': names,
		'State': states
	}
	df = pd.DataFrame(data)
	df.to_csv('lethal_force_policy_2013_2015')


def count_by_year(year):
	count = 0
	for date in range(len(df['Date'])):
		count += 1 and df['Date'][date][:4] == year
	return count


search()

df = pd.read_csv('lethal_force_policy_2013_2015')

df2013_count = count_by_year('2013')
df2015_count = count_by_year('2015')

percentage_increase = round((df2015_count * 100) / df2013_count)
print(f'Police murders have been increased {percentage_increase}% (2013 ~ 2015)')

