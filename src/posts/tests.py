from django.test import TestCase
from bs4 import BeautifulSoup
import requests


def grab_sitemap(url):
    r = requests.get(url)
    sitemapTags = BeautifulSoup(r.text).find_all("url")
    print("The number of sitemaps are {0}".format(len(sitemapTags)))
    liste, liste2= list(), list()
    for sitemap in sitemapTags:
        liste.append(sitemap.find_all('loc')[0])
    for i in liste:
        liste2.append(requests.post(i.text).status_code)
    return liste2

def func():
    url = "https://www.lapetiteportugaise.eu/sitemap.xml"
    url = "http://127.0.0.1:8000/sitemap.xml"
    liste = grab_sitemap(url)
    return liste

def test_answer():
    for i in func():
        assert i == 200
