from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait


class PageHelper:
    def __init__(self, driver, wait_time):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, wait_time)

    def get_url(self, url):
        self.driver.get(url)

    def load_manufacturers(self):
        url = 'https://ec.europa.eu/tools/eudamed/#/screen/search-eo?actorTypeCode=refdata.actor-type.manufacturer' \
              '&submitted=true'

        self.get_url(url)

    def load_importers(self):
        url = 'https://ec.europa.eu/tools/eudamed/#/screen/search-eo?actorTypeCode=refdata.actor-type.importer' \
              '&submitted=true'

        self.get_url(url)

    def wait_for_presence(self, location):
        try:
            return self.wait.until(EC.presence_of_element_located(location))
        except TimeoutException as e:
            return f'Timeout for presence Exception error! \nMessage: {e}'

    def scroll_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def accept_cookies(self):
        cookies_location = (By.XPATH, "//a[@href='#accept']")

        cookies = self.wait_for_presence(cookies_location)

        cookies.click()

    def close_cookies_prompt_after_accept(self):
        prompt_close_button_location = (By.CLASS_NAME, 'wt-ecl-message__close')

        prompt_close_button = self.wait_for_presence(prompt_close_button_location)

        prompt_close_button.click()

    @staticmethod
    def find_element(element, location):
        return element.find_element(*location)

    @staticmethod
    def find_elements(element, location):
        return element.find_elements(*location)

    @staticmethod
    def extract_text(element):
        return element.text

