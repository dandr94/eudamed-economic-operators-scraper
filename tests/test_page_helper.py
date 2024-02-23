import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from pages.utils.page_helper import PageHelper


class TestPageHelper(unittest.TestCase):
    WEBDRIVER_OPTIONS = ['--headless=new', '--disable-extensions', '--disable-infobars', '--disable-gpu',
                         '--disable-notifications']

    def setUp(self) -> None:
        options = webdriver.ChromeOptions()

        for option in self.WEBDRIVER_OPTIONS:
            options.add_argument(option)

        self.driver = webdriver.Chrome(options=options)

        self.page_helper = PageHelper(self.driver, 3)

    # def tearDown(self):
    #     self.driver.quit()

    def test_load_manufacturers(self):
        self.page_helper.load_manufacturers()

        role_location = (By.XPATH,
                         '/html/body/app-root/eui-block-content/div/ecl-app/div/div/div/app-search-eo/search-tags/div/span/span/span')

        role = self.page_helper.wait_for_presence(role_location)

        expected_url = 'https://ec.europa.eu/tools/eudamed/#/screen/search-eo?actorTypeCode=refdata.actor-type.manufacturer&submitted=true'
        expected_role = 'Manufacturer'

        self.assertEqual(self.driver.current_url, expected_url)

        self.assertEqual(role.text, expected_role)

    def test_load_importers(self):
        self.page_helper.load_importers()

        role_location = (By.XPATH,
                         '/html/body/app-root/eui-block-content/div/ecl-app/div/div/div/app-search-eo/search-tags/div/span/span/span')

        role = self.page_helper.wait_for_presence(role_location)

        expected_url = 'https://ec.europa.eu/tools/eudamed/#/screen/search-eo?actorTypeCode=refdata.actor-type.importer' \
                       '&submitted=true'
        expected_role = 'Importer'

        self.assertEqual(expected_url, self.driver.current_url)

        self.assertEqual(expected_role, role.text)

    def test_wait_for_presence(self):
        self.page_helper.load_importers()

        role_location = (By.XPATH,
                         '/html/body/app-root/eui-block-content/div/ecl-app/div/div/div/app-search-eo/search-tags/div/span/span/span')

        role = self.page_helper.wait_for_presence(role_location)

        self.assertIsNotNone(role)

    def test_wait_for_presence_timeout(self):
        role_location = (By.ID, 'element_id')

        role = self.page_helper.wait_for_presence(role_location)

        expected_result = 'Timeout for presence Exception error!'

        self.assertIn(expected_result, role)

    def test_scroll_to_element(self):
        self.page_helper.load_importers()

        role_location = (By.XPATH,
                         '/html/body/app-root/eui-block-content/div/ecl-app/div/div/div/app-search-eo/search-tags/div/span/span/span')

        role = self.page_helper.wait_for_presence(role_location)

        self.page_helper.scroll_to_element(role)

        is_in_view = role.is_displayed()

        self.assertTrue(is_in_view)

    def test_accept_cookies(self):
        self.page_helper.load_importers()

        cookies_location = (By.XPATH, "//a[@href='#accept']")

        cookies_banner = self.page_helper.wait_for_presence(cookies_location)

        self.assertIsInstance(cookies_banner, WebElement)

        self.page_helper.accept_cookies()

        cookies_banner_after = self.page_helper.wait_for_presence(cookies_location)

        self.assertNotIsInstance(cookies_banner_after, WebElement)

    def test_close_cookies_prompt_after_accept(self):
        self.page_helper.load_importers()

        self.page_helper.accept_cookies()

        prompt_close_button_location = (By.CLASS_NAME, 'wt-ecl-message__close')

        prompt_close_button = self.page_helper.wait_for_presence(prompt_close_button_location)

        self.assertIsInstance(prompt_close_button, WebElement)

        self.page_helper.close_cookies_prompt_after_accept()

        prompt_close_button_after = self.page_helper.wait_for_presence(prompt_close_button_location)

        self.assertNotIsInstance(prompt_close_button_after, WebElement)
