import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from main import WebDriverOptions
from pages.browse_page import BrowsePage


class TestBrowsePage(unittest.TestCase):
    TEST_ROLE = 'importer'

    def setUp(self) -> None:
        self.web_driver_options = WebDriverOptions(wait_time=3)

        self.driver = webdriver.Chrome(options=self.web_driver_options.get_driver_options())

        self.browse_page = BrowsePage(self.driver, self.web_driver_options.get_web_driver_wait_time)

        self.browse_page.load_url(self.TEST_ROLE)

    #
    # def tearDown(self):
    #     self.driver.quit()

    def test_wait_for_table_to_load(self):
        self.browse_page.wait_for_table_to_load()

        table_location = (
            By.XPATH,
            '/html/body/app-root/eui-block-content/div/ecl-app/div/div/div/app-search-eo/eui-block-content/div')

        table = self.browse_page.find_element(self.driver, table_location)

        self.assertTrue(table)

        self.assertIsInstance(table, WebElement)

    def test_find_table_rows(self):
        rows = self.browse_page.find_table_rows()

        self.assertIsInstance(rows, list)

        self.assertTrue(len(rows) > 0)

    def test_find_action_button(self):
        row_num = 1

        action_button = self.browse_page.find_action_button(row_num)

        self.assertIsInstance(action_button, WebElement)

        aria_label = action_button.get_attribute("aria-label")

        expected_aria_label = 'View detail'

        self.assertEqual(expected_aria_label, aria_label)

    def test_find_next_page_button(self):
        next_page_button = self.browse_page.find_next_page_button()

        self.assertIsInstance(next_page_button, WebElement)

        # For some reason it does not load in time, so we need to wait for 1 sec
        time.sleep(1)

        aria_label = next_page_button.get_attribute("aria-label")

        expected_aria_label = 'Next page'

        self.assertEqual(expected_aria_label, aria_label)

    def test_find_previous_page_button(self):
        previous_page_button = self.browse_page.find_previous_page_button()

        self.assertIsInstance(previous_page_button, WebElement)

        # For some reason it does not load in time, so we need to wait for 1 sec
        time.sleep(1)

        aria_label = previous_page_button.get_attribute("aria-label")

        expected_aria_label = 'Previous page'

        self.assertEqual(expected_aria_label, aria_label)

    def test_find_last_page_button(self):
        last_page_button = self.browse_page.find_last_page_button()

        self.assertIsInstance(last_page_button, WebElement)

        # For some reason it does not load in time, so we need to wait for 1 sec
        time.sleep(1)

        aria_label = last_page_button.get_attribute("aria-label")

        expected_aria_label = 'Last page'

        self.assertEqual(expected_aria_label, aria_label)

    def test_find_table_dropdown_trigger(self):
        dropdown_trigger = self.browse_page.find_table_dropdown_trigger()

        self.assertIsInstance(dropdown_trigger, WebElement)

        aria_label = dropdown_trigger.get_attribute("aria-label")

        expected_aria_label = 'dropdown trigger'

        self.assertEqual(expected_aria_label, aria_label)

    def test_find_option_for_table_rows(self):
        # We need to accept and remove the cookies prompt otherwise it interferes with the dropdown
        self.browse_page.accept_cookies()
        self.browse_page.close_cookies_prompt_after_accept()

        table_dropdown_trigger = self.browse_page.find_table_dropdown_trigger()

        table_dropdown_trigger.click()

        options = self.browse_page.find_option_for_table_rows()

        self.assertIsInstance(options, list)

        expected_options_len = 3

        self.assertEqual(expected_options_len, len(options))

        self.assertEqual(options[0].text, '10')
        self.assertEqual(options[1].text, '25')
        self.assertEqual(options[2].text, '50')

    def test_choose_table_rows_per_page(self):
        # We need to accept and remove the cookies prompt otherwise it interferes with the dropdown
        self.browse_page.accept_cookies()
        self.browse_page.close_cookies_prompt_after_accept()

        num_rows_per_page = "10"

        self.browse_page.choose_table_rows_per_page(num_rows_per_page)

        selected_option_location = (By.ID, 'pr_id_2_label')

        selected_option = self.browse_page.find_element(self.driver, selected_option_location)

        self.assertEqual(selected_option.text, num_rows_per_page)

    def test_find_actor_id(self):
        row_num = 1

        actor_id = self.browse_page.find_actor_id(row_num)

        self.assertTrue(actor_id)

        self.assertIsInstance(actor_id, str)

    def test_is_button_disabled(self):
        next_page_button = self.browse_page.find_next_page_button()

        is_next_page_button_disabled = self.browse_page.is_button_disabled(next_page_button)

        self.assertFalse(is_next_page_button_disabled)

        previous_page_button = self.browse_page.find_previous_page_button()

        is_previous_page_button_disabled = self.browse_page.is_button_disabled(previous_page_button)

        self.assertTrue(is_previous_page_button_disabled)
