from bs4 import BeautifulSoup
import requests
import pandas as pd
import openpyxl

# creating a blank list for the URLs to populate to
url_list = []
# then create a list of film roles to scrape from the site
credits = ['Director', 'Script', 'Dramaturg', 'Editor', 'Camera', 'Set Design',
           'Costume Design', 'Music (Score)', 'Cast', 'Producer']

# this populates the url list with the scraping output
with open("output.txt", "r") as f:
    for item in f:
        url_list.append(str.rstrip(item))

n = 0

# this for loop works through all of the URLs on my list, grabs the film title, then populates the production roles
for url in url_list:
    html = requests.get(url).text
    soup = BeautifulSoup(html, features="lxml")
    # title, year, runtime, format always occupy the same span per page, so they can be grabbed easily as follows
    title = soup.find('title').string
    title = title.replace(' | DEFA Film Library', '')
    year = soup.select('span')[2].text
    runtime = soup.select('span')[4].text
    format = soup.select('span')[6].text
    captions = soup.findAll('caption')
    for n in range(len(captions)):
        role = soup.select('caption')[n].text
        caption1 = soup.find_all('caption')[n]
        # caption2 = soup.find_all('caption')[n+1] # need to find a way to grab all spans between these captions
        foundRole = caption1.find_next_sibling.string
        print(foundRole)
    info = {'Title': [title], 'Year': [year], 'Runtime': [runtime], 'Format': [format]}
    print(info)
    n = n+1
    print(str((n/1099)*100) + "%") # reports the % completion, helps track progress

# defa_df.to_excel(r'D:\Dropbox\2020 Fall\DHUM\Portfolio\Git\DEFAscraping\export.xlsx', startrow=0, index = False,header= True)
