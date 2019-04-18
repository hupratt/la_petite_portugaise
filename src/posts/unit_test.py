from django.test import TestCase
from bs4 import BeautifulSoup
import requests
import warnings
warnings.filterwarnings("ignore")

def verify_return_code(input):
    """
    Return a list of status codes from the sitemap
    >>> grab_sitemap('http://127.0.0.1:8000/sitemap.xml')
    ['200','200','200']
    """
    liste = list()
    for i in input:
        liste.append(requests.post(i.text, verify=False).status_code)
    return liste

def grab_urls_from_sitemap(url):
    r = requests.get(url, verify=False)
    sitemapTags = BeautifulSoup(r.text, features="html.parser").find_all("url")
    print("The number of sitemaps are {0}".format(len(sitemapTags)))
    liste = list()
    for sitemap in sitemapTags:
        liste.append(sitemap.find_all('loc')[0])
    return liste

class MyTests(unittest.TestCase):
    def test_url(self):
        url = "https://www.lapetiteportugaise.eu/sitemap.xml"
        # url = "http://127.0.0.1:8000/sitemap.xml"
        url_list = grab_urls_from_sitemap(url)
        status_list =verify_return_code(url_list)
        # self.assertEqual(status_list,['200','200','200'])
        for i in status_list:
            assert i == 200
