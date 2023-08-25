import requests  # to retrive the HTML
from bs4 import BeautifulSoup  # to filter through the requests
# import time to sleep so that the website doesn't block us
import time
import random
import io
# Creating the folders
import os
# saving it as png and dealing with errors
from PIL import Image, UnidentifiedImageError 

# setting the url to be scraped
home_url = "https://suryascans.com/"

# getting the html page
respense = requests.get(home_url)

# parsing the html page
soup = BeautifulSoup(respense.text, "html.parser")

manga_list = soup.find_all("a", class_="series")

for manga in manga_list:
    name_tag = manga.find("h4")
    if name_tag is not None:
        name = name_tag.text
        if name not in dict.keys() and name != None:
            url = name.lower().replace(" ", "-")

            dict[name] = url


def suryaUrl(name, counter):
    return f"https://suryascans.com/{name}-chapter-{counter}/"

# iterating through the list of mangas
counter = 1
errors = 0
for name, url in dict.items():
    # checking if the manga folder exists
    if not os.path.exists(name):
        os.makedirs(name)
    # getting the html page
    url = suryaUrl(url,counter)
    respense = requests.get(url)
    # check if the response is valid
    while respense.status_code == 200 :
        random_time = random.randint(1, 3)*0.1
        time.sleep(random_time)
        # parsing the html page
        soup = BeautifulSoup(respense.text, "html.parser")
        # getting the list of images
        list = soup.find_all("img")
        print(f"{name} chapter : {counter}")
        # creating a chapter folder
        if not os.path.exists(f"{name}/{counter}"):
            os.makedirs(f"{name}/{counter}")
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
            time.sleep(1 + random_time)
            # saving the image
            try:
                # Download and save the image
                response = requests.get(image_url)
                image_data = response.content
                image = Image.open(io.BytesIO(image_data))

                # Convert the image to PNG format
                png_image = image.convert("RGBA").convert("RGB")

                # Save the image to a PNG file
                png_file_name = os.path.splitext(image_name)[0] + ".png"
                png_image.save(f"{name}/{counter}/{png_file_name}")

            except UnidentifiedImageError:
                print(f"Unable to identify image: {image_url}")


        # incrementing the counter
        counter += 1
    counter = 1
        
