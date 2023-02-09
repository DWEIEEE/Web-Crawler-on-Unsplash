#!/usr/bin/env python
# coding: utf-8

# In[6]:


# Version_4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import requests
import time
import os

input_image = input("Please enter image category：")
limit = input("Please enter the number of images：")

browser = webdriver.Chrome(ChromeDriverManager().install())
 
browser.get(f"https://unsplash.com/s/photos/{input_image}")
browser.implicitly_wait(4)

page_next = browser.find_element(By.CLASS_NAME,"CwMIr.DQBsa.p1cWU.jpBZ0.AYOsT.Olora.I0aPD.dEcXu")
page_next.click()
time.sleep(2)

soup = BeautifulSoup(browser.page_source,"html.parser")
# Stock
results_t = soup.find_all("img",{"loading":"eager"})
image_links_t = [results_t.get("src") for results_t in results_t]
#
results = soup.find_all("img",{"itemprop":"thumbnailUrl"})
image_links = [result.get("src") for result in results]
image_links = list(set(image_links))
js = "window.scrollTo(0, document.body.scrollHeight-document.body.clientWidth-(document.body.clientWidth/4));"
while len(image_links) <= int(limit):
    print("found:",len(image_links),end='\r')
    browser.execute_script(js)
    time.sleep(2)
    soup = BeautifulSoup(browser.page_source,"html.parser")
    results = soup.find_all("img",{"itemprop":"thumbnailUrl"})
    image_links = [result.get("src") for result in results]
    image_links = list(set(image_links))
print("Finish Found")
image_links = image_links_t + image_links # Stock
image_links = image_links[:int(limit)]

path = f"images/{input_image}"
current_path = os.path.abspath(os.getcwd())
print("Downloading to",current_path + '\images\\' + str(input_image) )
print("Number of downloads:",len(image_links))
if not os.path.exists(path):
        os.makedirs(path)
for index, link in enumerate(image_links):
    print(index+1,':',link)
    img = requests.get(link)
    with open(path + "\\" + input_image + str(index+1) + ".jpg", "wb") as file:  
        file.write(img.content)  
    
print("Total found:",int(limit))
print("Total downloaded:",len(image_links))

