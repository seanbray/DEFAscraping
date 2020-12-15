from bs4 import BeautifulSoup
import requests
import pandas as pd


def merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res

# creating a blank list for the URLs to populate to
url_list = []
DEFA_dict = {}
# then create a list of film roles to scrape from the site
csv_columns = ['Title', 'Year', 'Runtime', 'Format', 'Director', 'Script', 'Dramaturg', 'Editor', 'Camera', 'Set Design',
           'Costume Design', 'Music (Score)', 'Cast', 'Producer']
csv_file = "Data.csv"

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
    roledict = {}
    for i in range(len(captions)): # make this a try/except
        try:
            role = soup.select('caption')[i].text
            name = soup.select("tbody span")[i].text
            roledict.update({role: name})
        except:
            break
    info = {'Title': title, 'Year': year, 'Runtime': runtime, 'Format': format}
    film_dict = merge(info, roledict)
    DEFA_dict[n] = film_dict
    n = n + 1
    complete = (n / 1099) * 100
    print(str(round(complete, 2)) + "%") # reports the % completion, helps track progress

df = pd.DataFrame.from_dict(DEFA_dict, orient='index')
df.to_excel(r'D:\Dropbox\2020 Fall\DHUM\Portfolio\Git\DEFAscraping\testexport.xlsx', startrow=0, index = False,header= True)
