from urllib.request import urlopen
import re


def store_url():  # this function writes the urls to a text file as I find them
    defa = open("output.txt", "a")
    defa.write(film_link)
    defa.write("\n")
    defa.close()


for n in range(0, 110):  # there are 110 film list pages on the website
    url = "https://ecommerce.umass.edu/defa/films?page=" + str(n)  # this iterates through the pages
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")  # makes the url treatable as text
    pattern = '/defa/film/.*?"'  # all of the individual film pages follow this pattern
    match_results = re.findall(pattern, html, re.IGNORECASE)
    link_list = ' '.join(match_results).replace('"','').split()
    link_list = list(dict.fromkeys(link_list))
    for link in link_list:
        film_link = "https://ecommerce.umass.edu" + link
        print(url + 'written')  # this is unnecessary but I like to see the progression
        store_url()  # writing to text as we go may? be slightly slower, but makes it easier if the program crashes
