from django.http import HttpRequest
from django.test import SimpleTestCase, TestCase
from django.urls import reverse
import requests
from bs4 import BeautifulSoup
from .models import Post
from django.contrib.auth.models import User
from datetime import datetime
import pytz


class ConsultSitemapTest(SimpleTestCase):
    allow_database_queries = True

    @classmethod
    def setUpClass(cls):
        # Do pre test initialization here.
        super(ConsultSitemapTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # Do post test clean uphere.
        super(ConsultSitemapTest, cls).tearDownClass()

    def setUp(self):

        session = self.client.session
        session['is_mobile'] = False
        session.save()

    def test_home_page_status_code(self):
        response = self.client.get('/en/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_home_page_contains_correct_html(self):
        response = self.client.get('/en/')
        self.assertContains(response, 'lapetiteportugaise.bxl@gmail.com')

    def test_home_page_does_not_contain_incorrect_html(self):
        response = self.client.get('/en/')
        self.assertNotContains(
            response, 'Hi there! I should not be on the page.')

    def test_sitemap_urls(self):
        def parse_url(liste):
            """
            ['http://example.com/en/about-us/', 'http://example.com/en/contact/', 'http://example.com/en/']
            into
            ['/en/about-us/', '/en/contact/', '/en/']
            """
            return_list = list()
            for url in liste:
                pairs = [index for index,
                         char in enumerate(url) if char == '/']
                crop = url[pairs[2]:]
                return_list.append(crop)
            return return_list

        def verify_return_code(input):
            """
            Consult: ['/en/about-us/', '/en/contact/', '/en/']
            Return: ['200','200','200']
            """
            liste = list()
            # headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
            for i in input:
                liste.append(self.client.get(i).status_code)
            return liste

        def grab_urls_from_sitemap(url):
            # self.client.get('/en/')
            r = self.client.get(url)
            sitemapTags = BeautifulSoup(
                r.content, features="html.parser").find_all("url")
            assert(len(sitemapTags) > 0)
            liste = list()
            for sitemap in sitemapTags:
                for i in (sitemap.find_all('loc')):
                    liste.append(i.get_text())
            return liste
        # url = "https://www.lapetiteportugaise.eu/sitemap.xml"
        url = "http://127.0.0.1:8000/sitemap.xml"
        url_list = grab_urls_from_sitemap(url)
        url_list = parse_url(url_list)
        status_list = verify_return_code(url_list)
        # self.assertEqual(status_list,['200','200','200'])
        for i in status_list:
            assert i == 200


class PostTests(TestCase):

    def setUp(self):
        User.objects.create_superuser(
            'myuser', 'myemail@test.com', 'password')
        session = self.client.session
        session['is_mobile'] = False
        session.save()
        Post.objects.create(content='just a test',
                            timestamp=datetime.now().replace(tzinfo=pytz.UTC))

    def test_text_content(self):
        post = Post.objects.get(id=1)
        expected_object_name = f'{post.content}'
        self.assertEquals(expected_object_name, 'just a test')

    # def test_post_list_view(self):
    #     response = self.client.get(reverse('posts'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, 'just a test')
    #     self.assertTemplateUsed(response, 'posts.html')
