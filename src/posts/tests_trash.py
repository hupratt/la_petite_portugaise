
from django.test import TestCase
from bs4 import BeautifulSoup
import requests


def verify_return_code(input):
    """
    Return a list of status codes from the sitemap
    >>> grab_sitemap('http://127.0.0.1:8000/sitemap.xml')
    ['200','200','200']
    """
    liste = list()
    # headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    for i in input:
        liste.append(requests.get(i, verify=False).status_code)
    return liste

def grab_urls_from_sitemap(url):
    r = requests.get(url, verify=False)
    sitemapTags = BeautifulSoup(r.text, features="html.parser").find_all("url")
    print("The number of sitemaps are {0}".format(len(sitemapTags)))
    liste = list()
    for sitemap in sitemapTags:
        for i in (sitemap.find_all('loc')):
            liste.append(i.get_text())
    return liste

def test_answer():
    url = "https://www.lapetiteportugaise.eu/sitemap.xml"
    # url = "http://127.0.0.1:8000/sitemap.xml"
    url_list = grab_urls_from_sitemap(url)
    print(url_list)
    status_list =verify_return_code(url_list)
    # self.assertEqual(status_list,['200','200','200'])
    for i in status_list:
        assert i == 200