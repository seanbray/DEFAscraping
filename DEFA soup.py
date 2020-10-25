from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

url_list = []
credits = ['Director', 'Script', 'Dramaturg', 'Editor', 'Camera', 'Set Design',
           'Costume Design', 'Music (Score)', 'Cast', 'Producer']

with open("output.txt", "r") as f:
    for item in f:
        url_list.append(str.rstrip(item))

# need to create a dataframe here, then fill it in the following for loop, then print to excel?
defa_df = pd.DataFrame(columns= ['Title', 'Director', 'Script', 'Dramaturg', 'Editor', 'Camera', 'Set Design',
           'Costume Design', 'Music (Score)', 'Cast', 'Producer'], index=['Film'])
print(defa_df)
n = 0

for url in url_list:
    html = requests.get(url).text
    soup = BeautifulSoup(html, features='lxml')
    title = soup.find('title').string
    title = [[title.replace(' | DEFA Film Library', '')]]
    runtime = soup.find('span', {"class": "views-field views-field-field-duration"})
    print(runtime)
    film_df = pd.DataFrame(title, columns= ['Title'])
    for role in credits:
        try:
            dfs = pd.read_html(html, match=role, skiprows=0)
            df = dfs[0]
            df.columns = [role]
            film_df.insert(1, role, df, allow_duplicates=True)
        except:
            film_df.insert(1, role, 'NaN')
        defa_df = pd.concat([defa_df, film_df])
    n = n+1
    print(str((n/1099)*100) + "%")

defa_df.to_excel(r'D:\Dropbox\Dropbox\2020 Fall\DHUM\Portfolio\export.xlsx', startrow=0, index = False,header= True)
