from urllib.request import urlopen


url_list = []

with open("output.txt", "r") as f:
    for item in f:
        url_list.append(str.rstrip(item))

for url in url_list:
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")