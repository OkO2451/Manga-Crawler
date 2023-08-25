import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import time
import random
import os
# setting the url to be scraped
home_url = "https://asura.nacm.xyz/"

# getting the html page
respense = requests.get(home_url)

# parsing the html page
soup = BeautifulSoup(respense.text, "html.parser")

# getting the list of mangas
manga_list = soup.find_all("a", class_="series")

# getting the manga name and url
dict = {}
for manga in manga_list:
    name = manga.find("h4").text
    if name is not None:
        name = name.strip()
        url = manga["href"]
        dict[name] = url
# alt
for i in range(0,len(manga_list)//2):
    name = manga_list[2*i].find("h4")
    # strip name from <h4> tags
    name = name.text
    url = manga_list[2*i]["href"]
    dict[name] = url