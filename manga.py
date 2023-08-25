import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
# import time to sleep so that the website doesn't block us
import time
import random
import os
# setting the url to be scraped
home_url = "https://manganato.com/"


# getting the html page
respense = requests.get(home_url)

# parsing the html page
soup = BeautifulSoup(respense.text, "html.parser")

# getting the list of mangas
list = soup.find_all("a")
manga_list = soup.find_all("div", class_="content-homepage-item")

# getting the manga name and url
dict = {}
for manga in manga_list:
    name = manga.find("a")["title"]
    url = manga.find("a")["href"]
    dict[name] = url

# iterating through the list of mangas
counter = 0
errors = 0
for name, url in dict.items():
    respense = requests.get(url + f'/chapter-{counter}')
    # check if the response is valid
    if respense.status_code == 200:
        # parsing the html page
        soup = BeautifulSoup(respense.text, "html.parser")
        # getting the list of images
        list = soup.find_all("img", class_="container-chapter-reader")
        # iterating through the list of images
        for image in list:
            # getting the image url
            image_url = image["src"]
            # getting the image name
            image_name = image_url.split("/")[-1]
            # getting the image
            image = requests.get(image_url)
            # to not get blocked
            # sleep a number of random miliseconds
            random_time = random.randint(1, 3)*0.1
            time.sleep(random_time)
            if not os.path.exists(name):
                os.makedirs(name)
            # saving the image
            with open(f"{name}/{image_name}", "wb") as file:
                file.write(image.content)
        # incrementing the counter
        break
        counter += 1
    else:
        if errors > 10:
            errors = 0
            break
        else:
            errors += 1
            
    

    


