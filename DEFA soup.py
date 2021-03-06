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

# create a dataframe here, then fill it in the following for loop, then print to excel there's almost certainly a
# better way, but this works well enough for my purposes, and I've only just started learning pandas
defa_df = pd.DataFrame(columns= ['Title', 'Year', 'Runtime', 'Format', 'Director', 'Script', 'Dramaturg', 'Editor', 'Camera', 'Set Design',
           'Costume Design', 'Music (Score)', 'Cast', 'Producer'], index=['Film'])
print(defa_df)
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
    info = {'Title': [title], 'Year': [year], 'Runtime': [runtime], 'Format': [format]}
    film_df = pd.DataFrame(info, columns= ['Title', 'Year', 'Runtime', 'Format'])
    # because the roles for a given film can vary, the above doesn't work well to get them. hence the following:
    for role in credits: # this method is somewhat flawed in that it can only grab the first person for each role,
        # no good solution yet
        try:
            dfs = pd.read_html(html, match=role, skiprows=0)
            df = dfs[0]
            df.columns = [role]
            film_df.insert(1, role, df, allow_duplicates=True)
        except:
            film_df.insert(1, role, 'NaN')
        defa_df = pd.concat([defa_df, film_df], sort=True) # and here we expand the master defa dataframe
    n = n+1
    print(str((n/1099)*100) + "%") # reports the % completion, helps track progress

defa_df.to_excel(r'D:\Dropbox\2020 Fall\DHUM\Portfolio\Git\DEFAscraping\export.xlsx', startrow=0, index = False,header= True)
