from django.http import HttpRequest
from django.test import SimpleTestCase
from django.urls import reverse
import os
from . import views


class HomePageTests(SimpleTestCase):
    def setUpClass(self):
        os.environ['DJANGO_SETTINGS_MODULE'] = 'la_petite_portugaise.settings'

        BASE_DIR = os.path.dirname(os.path.dirname(
            os.path.abspath(__file__)))

        sys.path.append(BASE_DIR)
        os.environ['DJANGO_SETTINGS_MODULE'] = 'la_petite_portugaise.settings'
        django.setup()

    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_contains_correct_html(self):
        response = self.client.get('/')
        self.assertContains(response, '<h1>Homepage</h1>')

    def test_home_page_does_not_contain_incorrect_html(self):
        response = self.client.get('/')
        self.assertNotContains(
            response, 'Hi there! I should not be on the page.')
