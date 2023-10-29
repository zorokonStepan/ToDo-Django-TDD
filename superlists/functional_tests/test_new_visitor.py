import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from django.test import LiveServerTestCase


class NewVisitorTest(LiveServerTestCase):
    MAX_WAIT = 10

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, 'id_list_table')
                rows = table.find_elements(By.TAG_NAME, 'tr')
                self.assertIn(row_text, [row.text for row in rows])
                return None
            except (AssertionError, WebDriverException) as exception:
                if time.time() - start_time > self.MAX_WAIT:
                    raise exception
                time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):
        self.browser.get(f'{self.live_server_url}/todo/')

        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)

        input_box = self.browser.find_element(By.ID, 'id_new_item')
        input_box.send_keys('Buy peacock feathers')
        input_box.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        input_box = self.browser.find_element(By.ID, 'id_new_item')
        input_box.send_keys('Make a fly from peacock feathers')
        input_box.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table('2: Make a fly from peacock feathers')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        self.browser.get(f'{self.live_server_url}/todo/')

        input_box = self.browser.find_element(By.ID, 'id_new_item')
        input_box.send_keys('Buy peacock feathers')
        input_box.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        self.browser.quit()
        self.browser = webdriver.Firefox()

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text

        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('Make a fly', page_text)

        input_box = self.browser.find_element(By.ID, 'id_new_item')
        input_box.send_keys('Buy milk')
        input_box.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Buy milk')

        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)
