from typing import Tuple, List, Union

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from selenium.common import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait


class PageHelper:
    """
        A utility class providing helper methods for interacting with web pages.
    """

    def __init__(self, driver: WebDriver, wait_time: int):
        """
            Initializes the PageHelper with a WebDriver instance and wait time.

            Args:
                - driver: WebDriver instance for browser automation.
                - wait_time: The maximum time to wait for an element to appear on the page, in seconds.
        """
        self.driver = driver
        self.wait = WebDriverWait(self.driver, wait_time)

    def get_url(self, url: str) -> None:
        """
            Navigates the browser to the specified URL.

            Args:
                - url: The URL to navigate to.
        """
        self.driver.get(url)

    def load_url(self, role):
        """
            Loads a specific URL based on the role of the actor.

            Args:
                - role: The role of the actor for which the URL is to be loaded.
        """
        url = f'https://ec.europa.eu/tools/eudamed/#/screen/search-eo?actorTypeCode=refdata.actor-type.{role}' \
              '&submitted=true'

        self.get_url(url)

    def wait_for_presence(self, location: Tuple[str, str]) -> Union[WebElement, str]:
        """
            Waits for the presence of an element identified by the given location on the page.

            Args:
                - location: A tuple representing the location strategy and value (e.g., (By.ID, 'element_id')).

            Returns:
                - The located WebElement upon successful presence.
                - A timeout error message if the element is not found within the specified time.
        """
        try:
            return self.wait.until(EC.presence_of_element_located(location))
        except TimeoutException as e:
            return f'Timeout for presence Exception error! \nMessage: {e}'

    def scroll_to_element(self, element: WebElement) -> None:
        """
            Scrolls the page to bring the specified element into view.

            Args:
                - element: The WebElement to which the page should be scrolled.
        """
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def accept_cookies(self) -> None:
        """
            Accepts cookies by clicking on the corresponding button.
        """
        cookies_location = (By.XPATH, "//a[@href='#accept']")

        cookies = self.wait_for_presence(cookies_location)

        cookies.click()

    def close_cookies_prompt_after_accept(self) -> None:
        """
            Closes the cookies prompt after accepting them.
        """
        prompt_close_button_location = (By.CLASS_NAME, 'wt-ecl-message__close')

        prompt_close_button = self.wait_for_presence(prompt_close_button_location)

        prompt_close_button.click()

    @staticmethod
    def find_element(element: Union[WebDriver, WebElement], location: Tuple[str, str]) -> WebElement:
        """
            Finds and returns a single WebElement within the specified element's scope.

            Args:
                - element: The parent WebElement within which to search.
                - location: A tuple representing the location strategy and value (e.g., (By.ID, 'element_id')).

        Returns:
                - The located WebElement.
        """
        return element.find_element(*location)

    @staticmethod
    def find_elements(element: Union[WebDriver, WebElement], location: Tuple[str, str]) -> List[WebElement]:
        """
            Finds and returns multiple WebElements within the specified element's scope.

            Args:
                - element: The parent WebElement within which to search.
                - location: A tuple representing the location strategy and value (e.g., (By.ID, 'element_id')).

            Returns:
                - A list of located WebElements.
        """
        return element.find_elements(*location)

    @staticmethod
    def extract_text(element: WebElement) -> str:
        """
            Extracts the text content of the specified WebElement.

            Args:
                - element: The WebElement from which to extract text.

            Returns:
                - The text content of the WebElement.
        """
        return element.text
