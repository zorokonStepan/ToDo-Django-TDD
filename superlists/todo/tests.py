from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from .views import home_page


class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/todo/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/todo/')
        html = response.content.decode('utf8')

        self.assertTrue(html.strip().startswith('<html>'))
        self.assertIn('<title>To-Do list</title>', html)
        self.assertTrue(html.strip().endswith('</html>'))

        self.assertTemplateUsed(response, 'todo/home.html')
