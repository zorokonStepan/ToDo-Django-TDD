from django.test import TestCase

from ...models import Item


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/todo/')
        self.assertTemplateUsed(response, 'todo/home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/todo/', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/todo/')

    def test_only_saves_items_when_necessary(self):
        self.client.get('/todo/')
        self.assertEqual(Item.objects.count(), 0)
