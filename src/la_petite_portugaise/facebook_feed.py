from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu') 
options.add_argument('--no-sandbox')

header = {
    'Host':'www.procato.com',
    'Connection':'keep-alive',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
}

driver = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=options)

url = 'https://fr-fr.facebook.com/lapetiteportugaisebxl/posts'
url2 = 'https://fr-fr.facebook.com/pg/lapetiteportugaisebxl/posts/?ref=page_internal'

# class to look for: _'4-u2 _4-u8'

driver.get(url)
# and a browser pops up if the headless option above is disabled

soup = BeautifulSoup(driver.page_source, features="html.parser")


print('congratulations, found {} matches'.format(len(soup.find_all(class_=re.compile("4-u2")))))

import numpy as np
liste, liste2 = list(), list()
for tag in soup.find_all(class_=re.compile("4-u2")):
    for subject in (tag.find_all('p')):
        liste.append(subject.text)
    for subject in (tag.find_all('abbr')):
        liste2.append(subject.text)

print(len(np.array(liste)))
print(len(np.array(liste2)))
arr = np.array(liste, liste2)
print(arr)

from datetime import datetime

clean_dates = list()
for i in liste2:
    if (len(i)>8):
        clean_dates.append(i)

len(clean_dates)