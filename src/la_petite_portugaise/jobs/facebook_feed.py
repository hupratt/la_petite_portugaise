from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import locale, re, time, os
import pandas as pd
from .posts.models import Post
import sqlite3
from sqlite3 import Error


def grab_from_facebook(url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu') 
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=options)
    # class to look for: _'4-u2 _4-u8'
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, features="html.parser")

    print('congratulations, found {} matches'.format(len(soup.find_all(class_=re.compile("4-u2")))))

    liste, liste2 = list(), list()
    for tag in soup.find_all(class_=re.compile("4-u2")):
        for subject in (tag.find_all('p')):
            liste.append(subject.text)
        for date in (tag.find_all('abbr')):
            liste2.append(date.text)

    clean_dates = list()

    for i in liste2:
        if (len(i)>8):
            try:
                locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
                date_temp = (datetime.strptime(i, '%d. %B um %H:%S')).replace(year = datetime.today().year)
                clean_dates.append(date_temp)
            except ValueError:
                pass
            try:
                locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
                date_temp = (datetime.strptime(i, '%d %B %H:%S')).replace(year = datetime.today().year)
                clean_dates.append(date_temp)
            except ValueError:
                pass
            try:
                locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
                date_temp = (datetime.strptime(i, '%d %B, %H:%S')).replace(year = datetime.today().year)
                clean_dates.append(date_temp)
            except ValueError:
                pass

    json = dict()

    len_json = min(len(clean_dates),len(liste))

    for i in range(len_json):
        if i % 2 == 0:
            json[clean_dates[i]] = liste[i]

    return json, len_json


def search_import_file(a,b):
    liste=[]
    for i in os.listdir(os.path.curdir):
        liste.append(i)
    for file in liste: 
        if (file.startswith(a) and file.endswith(b)):
            curdir = os.path.abspath(os.path.curdir)
            path_to_file = os.path.join(curdir,file)
            print("found",path_to_file)
    return path_to_file

def create_excel(json, len_json):

    to_remove = search_import_file('Facebook_retrieve_','xlsx')

    try:
        os.remove(to_remove)
    except UnexpectedError as e:
        print("Error:",e)

    df = pd.DataFrame.from_dict(json, orient='index')
    timer=time.strftime("%Y%m%d_%H%M%S")
    filename='Facebook_retrieve_'+timer+'_'+str(len_json)+'.xlsx'
    writer = pd.ExcelWriter(filename)
    df.to_excel(writer,'Facebook', header=True, index=True)
    writer.save()

def add_to_postgres(json, database):
    conn = create_connection(database)
    with conn:
        for key, value in json.items():
            try:
                min_value = key - timedelta(seconds=5)
                max_value = key + timedelta(seconds=5)
                post = Post.objects.filter(timestamp__range=[min_value,max_value])
            except Error:
                Post.objects.create(content = "value", timestamp = "key")
        print('added to db: SUCCESS')

def main():
    os.chdir(str('/home/ubuntu/Dev/la_petite_portugaise/src/la_petite_portugaise/'))
    database = str("/home/hugo/Development/la_petite_portugaise/src/db.sqlite3")
    url = 'https://fr-fr.facebook.com/lapetiteportugaisebxl/posts'
    json, len_json = grab_from_facebook(url)
    # create_excel(json, len_json)
    add_to_postgres(json, database)


if __name__ == '__main__':
    main()