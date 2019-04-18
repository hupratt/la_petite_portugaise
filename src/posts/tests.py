
from django.test import TestCase
from bs4 import BeautifulSoup
import requests

class MyTests(TestCase):
    def grab_sitemap(self, url):
        r = requests.get(url, verify=False)
        sitemapTags = BeautifulSoup(r.text, features="html.parser").find_all("url")
        print("The number of sitemaps are {0}".format(len(sitemapTags)))
        liste, liste2= list(), list()
        for sitemap in sitemapTags:
            liste.append(sitemap.find_all('loc')[0])
        for i in liste:
            liste2.append(requests.post(i.text, verify=False).status_code)
        return liste2
    def setup(self):
        url = "https://www.lapetiteportugaise.eu/sitemap.xml"
        # url = "http://127.0.0.1:8000/sitemap.xml"
        liste = grab_sitemap(url)
        return liste
    def test_answer(self):
        for i in setup():
            assert i == 200
