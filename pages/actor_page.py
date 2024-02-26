from typing import Dict, List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from pages.utils.page_helper import PageHelper


class ActorPage(PageHelper):
    """
        Represents a page helper specifically designed for scraping actor-specific information.

        The ActorPage class extends the functionality of the PageHelper class to facilitate
        the extraction of detailed information about actors from web pages.
    """

    def __init__(self, driver: WebDriver, wait_time: int):
        """
            Initializes the ActorPage instance.

            Args:
               - driver: WebDriver instance for browser automation.
               - wait_time: The time to wait for elements to load.
        """
        super().__init__(driver, wait_time)

    def wait_for_actor_information_to_load(self):
        """
            Waits for actor information to load on the page.
        """
        actor_information_location = (By.ID, 'actor_information')

        # self.wait_for_presence(actor_information_location)

        return self.wait_for_presence(actor_information_location)

    def find_actor_information_last_updated(self) -> Dict[str, str]:
        """
            Finds when the last information was updated about the actor.

            Returns:
                - A dictionary containing the last updated information.
        """
        information_last_updated_location = (By.XPATH,
                                             '/html/body/app-root/eui-block-content/div/ecl-app/div/div/div/app-eo'
                                             '-detail/eui-block-content/div/div/div[2]/div[2]/div['
                                             '1]/div/mat-accordion/mat-expansion-panel/div/div/div['
                                             '1]/app-history-nav/ul/li[2]')

        information_last_updated = self.wait_for_presence(information_last_updated_location)

        information_last_updated_text_split = self.extract_text(information_last_updated).split(': ')

        key, value = information_last_updated_text_split[0], information_last_updated_text_split[1]

        return {key: value}

    def find_actor_dl_elements(self, actor_information_container: WebElement) -> List[WebElement]:
        """
            Finds the dl elements containing actor information.

            Args:
                - actor_information_container: The container containing actor information.
        """
        actor_dl_elements_location = (By.TAG_NAME, 'dl')

        self.wait_for_presence(actor_dl_elements_location)

        actor_dl_elements = self.find_elements(actor_information_container, actor_dl_elements_location)

        return actor_dl_elements

    def find_actor_information_container(self) -> WebElement:
        """
            Finds the container containing actor information on the page.
        """
        actor_information_location = (By.XPATH,
                                      '/html/body/app-root/eui-block-content/div/ecl-app/div/div/div/app-eo-detail'
                                      '/eui-block-content/div/div/div[2]/div[2]/div['
                                      '1]/div/mat-accordion/mat-expansion-panel/div/div/div[2]')

        return self.wait_for_presence(actor_information_location)

    def extract_actor_information(self) -> Dict[str, str]:
        """
            Extracts actor information from the page.

            Returns:
                - A dictionary containing actor information.
        """
        actor_information = self.find_actor_information_container()

        actor_information_dl_elements = self.find_actor_dl_elements(actor_information)

        actor_information_text_parsed = self.parse_text(actor_information_dl_elements)

        actor_information_text_parsed.update(self.find_actor_information_last_updated())

        actor_information_text_parsed['Actor URL'] = self.driver.current_url

        return actor_information_text_parsed

    @staticmethod
    def parse_text(dl_elements: List[WebElement]) -> Dict[str, str]:
        """
            Parses text from dl elements and constructs a dictionary.

            Args:
                - dl_elements: The dl elements containing text to parse.

            Returns:
                - A dictionary containing parsed text.
        """
        elements_to_skip = ['Actor identification', 'Actor address', 'Actor contact details']

        to_dict = {}

        for dl in dl_elements:
            dl_split = dl.text.split('\n')

            if len(dl_split) <= 1:
                dl_el = dl_split[0].strip()

                if dl_el not in elements_to_skip:
                    to_dict[dl_el] = '-'
            else:
                to_dict[dl_split[0].strip()] = dl_split[1].strip()

        return to_dict
