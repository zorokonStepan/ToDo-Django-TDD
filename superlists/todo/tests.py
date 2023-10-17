from django.test import TestCase


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/todo/')
        self.assertTemplateUsed(response, 'todo/home.html')
