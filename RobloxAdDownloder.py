import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.request import urlretrieve

def unshorten_url(url):
    response = requests.head(url, allow_redirects=True)
    return response.url

def download_image(url, folder_path):
    image_name = url.split('/')[-2]
    image_path = os.path.join(folder_path, f"{image_name}.png")
    if not os.path.exists(image_path):
        urlretrieve(url, image_path)
    return image_path

def process_roblox_ad(ad_url):
    response = requests.get(ad_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    ad_link = soup.find('a', class_='ad')['href']
    ad_link = unshorten_url(ad_link)

    image_url = soup.find('img')['src']
    return ad_link, image_url

base_url = 'https://www.roblox.com/user-sponsorship/'
ads_folder = os.path.join(os.path.expanduser('~'), 'Documents', 'RobloxAds')

if not os.path.exists(ads_folder):
    os.makedirs(ads_folder)

while True:
    time.sleep(2)
    for user_id in range(1, 4):
        user_url = f"{base_url}{user_id}"

        ad_link, image_url = process_roblox_ad(user_url)
        hash_folder_name = ad_link.split('/')[-1].replace("-", " ") + " - " + image_url.split('/')[-5]

        folder_path = os.path.join(ads_folder, hash_folder_name)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        if not os.path.exists(os.path.join(folder_path, hash_folder_name)):
            image_path = download_image(image_url, folder_path)

            game_link_file = os.path.join(folder_path, 'Game.txt')
            with open(game_link_file, 'w') as file:
                file.write(ad_link)

            print(f"Ad Link: {ad_link}")
            print(f"Image saved at: {image_path}")
            print()
        else:
            print("Skipping image " + hash_folder_name + " as it is already downloaded.")
