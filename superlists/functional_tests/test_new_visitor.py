import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class NewVisitorTest(StaticLiveServerTestCase):
    MAX_WAIT = 10

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, "id_list_table")
                rows = table.find_elements(By.TAG_NAME, "tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException):
                if time.time() - start_time > self.MAX_WAIT:
                    raise
                time.sleep(0.5)

    def test_can_start_a_todo_list(self):
        self.browser.get(f'{self.live_server_url}/todo/')

        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header_text)

        input_box = self.browser.find_element(By.ID, "id_new_item")
        self.assertEqual(input_box.get_attribute("placeholder"), "Enter a to-do item")

        input_box.send_keys("Buy peacock feathers")

        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy peacock feathers")

        input_box = self.browser.find_element(By.ID, "id_new_item")
        input_box.send_keys("Use peacock feathers to make a fly")
        input_box.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table("1: Buy peacock feathers")
        self.wait_for_row_in_list_table("2: Use peacock feathers to make a fly")

    def test_multiple_users_can_start_lists_at_different_urls(self):
        self.browser.get(f'{self.live_server_url}/todo/')

        input_box = self.browser.find_element(By.ID, "id_new_item")
        input_box.send_keys("Buy peacock feathers")
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy peacock feathers")

        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, "/todo/.+")

        self.browser.delete_all_cookies()

        self.browser.get(f'{self.live_server_url}/todo/')
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertNotIn("make a fly", page_text)

        input_box = self.browser.find_element(By.ID, "id_new_item")
        input_box.send_keys("Buy milk")
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")

        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, "/todo/.+")
        self.assertNotEqual(francis_list_url, edith_list_url)

        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertIn("Buy milk", page_text)

    def test_layout_and_styling(self):
        self.browser.get(f'{self.live_server_url}/todo/')
        self.browser.set_window_size(1024, 768)

        input_box = self.browser.find_element(By.ID, 'id_new_item')
        self.assertAlmostEqual(input_box.location['x'] + input_box.size['width'] / 2, 512, delta=10)

        input_box.send_keys("testing")
        input_box.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table("1: testing")
        input_box = self.browser.find_element(By.ID, "id_new_item")
        self.assertAlmostEqual(input_box.location["x"] + input_box.size["width"] / 2, 512, delta=10)
