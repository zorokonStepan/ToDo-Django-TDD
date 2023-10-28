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

    def test_can_start_a_list_and_retrieve_it_later(self):
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
