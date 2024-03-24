import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from main import WebDriverOptions
from pages.utils.page_helper import PageHelper


class TestPageHelper(unittest.TestCase):
    TEST_ROLE = 'importer'

    def setUp(self) -> None:
        self.web_driver_options = WebDriverOptions(wait_time=3)

        self.driver = webdriver.Chrome(options=self.web_driver_options.get_driver_options())

        self.page_helper = PageHelper(self.driver, self.web_driver_options.get_web_driver_wait_time)

        self.page_helper.load_url(self.TEST_ROLE)

    # def tearDown(self):
    #     self.driver.quit()

    def test_load_role(self):
        role = 'manufacturer'

        self.page_helper.load_url(role)

        role_location = (By.XPATH,
                         '/html/body/app-root/eui-block-content/div/ecl-app/div/div/div/app-search-eo/search-tags/div'
                         '/span/span/span')

        filter_role = self.page_helper.wait_for_presence(role_location)

        expected_url = f'https://ec.europa.eu/tools/eudamed/#/screen/search-eo?actorTypeCode=refdata.actor-type.{role}&submitted=true'

        self.assertEqual(expected_url, self.driver.current_url)

        self.assertEqual(role.capitalize(), filter_role.text)

    def test_wait_for_presence(self):
        role_location = (By.XPATH,
                         '/html/body/app-root/eui-block-content/div/ecl-app/div/div/div/app-search-eo/search-tags/div'
                         '/span/span/span')

        role = self.page_helper.wait_for_presence(role_location)

        self.assertIsNotNone(role)

        self.assertIsInstance(role, WebElement)

    def test_wait_for_presence_timeout(self):
        role_location = (By.ID, 'element_id')

        role = self.page_helper.wait_for_presence(role_location)

        expected_result = 'Timeout for presence Exception error!'

        self.assertIn(expected_result, role)

    def test_scroll_to_element(self):
        role_location = (By.XPATH,
                         '/html/body/app-root/eui-block-content/div/ecl-app/div/div/div/app-search-eo/search-tags/div'
                         '/span/span/span')

        role = self.page_helper.wait_for_presence(role_location)

        self.page_helper.scroll_to_element(role)

        is_in_view = role.is_displayed()

        self.assertTrue(is_in_view)

    def test_accept_cookies(self):
        cookies_location = (By.XPATH, "//a[@href='#accept']")

        cookies_banner = self.page_helper.wait_for_presence(cookies_location)

        self.assertIsInstance(cookies_banner, WebElement)

        self.page_helper.accept_cookies()

        cookies_banner_after = self.page_helper.wait_for_presence(cookies_location)

        self.assertNotIsInstance(cookies_banner_after, WebElement)

    # Old test that is not needed anymore, but maybe the functionality can be introduced again, so it will stay.
    # def test_close_cookies_prompt_after_accept(self):
    #     self.page_helper.accept_cookies()
    #
    #     prompt_close_button_location = (By.CLASS_NAME, 'wt-ecl-message__close')
    #
    #     prompt_close_button = self.page_helper.wait_for_presence(prompt_close_button_location)
    #
    #     self.assertIsInstance(prompt_close_button, WebElement)
    #
    #     self.page_helper.close_cookies_prompt_after_accept()
    #
    #     prompt_close_button_after = self.page_helper.wait_for_presence(prompt_close_button_location)
    #
    #     self.assertNotIsInstance(prompt_close_button_after, WebElement)
