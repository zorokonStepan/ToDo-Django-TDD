from django.test import TestCase

from ...models import Item, List


class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get('/todo/')
        self.assertTemplateUsed(response, 'todo/home.html')


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        response = self.client.get('/todo/one-of-a-kind-list-in-the-world/')
        self.assertTemplateUsed(response, 'todo/list.html')

    def test_displays_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)


class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        self.client.post('/todo/new/', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/todo/new/', data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/todo/one-of-a-kind-list-in-the-world/')
