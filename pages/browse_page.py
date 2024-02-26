from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from pages.utils.page_helper import PageHelper


class BrowsePage(PageHelper):
    """
        Represents a page helper for browsing and interacting with search results.

        This class extends PageHelper and provides methods specifically designed
        for interacting with the search results page.

    """

    def __init__(self, driver: WebDriver, wait_time: int):
        """
            Initializes a BrowsePage object.

            Args:
               - driver: WebDriver instance for browser automation.
               - wait_time: The maximum time to wait for elements to appear on the page, in seconds.
        """
        super().__init__(driver, wait_time)

    def wait_for_table_to_load(self) -> None:
        """
            Waits for the search results table to be loaded on the page.
        """
        table_location = (
            By.XPATH,
            '/html/body/app-root/eui-block-content/div/ecl-app/div/div/div/app-search-eo/eui-block-content/div')

        self.wait_for_presence(table_location)

    def find_table_rows(self) -> List[WebElement]:
        """
            Finds and returns the rows of the search results table.

            Returns:
                - A list of WebElements representing the rows of the table.
        """
        table_rows_location = (By.TAG_NAME, 'tr')

        self.wait_for_presence(table_rows_location)

        rows = self.find_elements(self.driver, table_rows_location)

        return rows

    def find_action_button(self, row_num: int) -> WebElement:
        """
            Finds and returns the action button for a specific row of the search results table.

            Args:
                - row_num: The row number for which to find the action button.

            Returns:
                - The WebElement representing the action button for the specified row.
        """
        action_button_location = (By.XPATH,
                                  f'/html/body/app-root/eui-block-content/div/ecl-app/div/div/div/app-search-eo/eui'
                                  f'-block-content/div/div/p-table/div/div/table/tbody/tr[{row_num + 1}]/td[8]/button')

        action_button = self.wait_for_presence(action_button_location)

        return action_button

    def find_next_page_button(self) -> WebElement:
        """
            Finds and returns the next page button on the search results page.

            Returns:
                    - The WebElement representing the next page button.
        """
        next_page_button_location = (By.XPATH,
                                     "/html/body/app-root/eui-block-content/div/ecl-app/div/div/div/app"
                                     "-search-eo/eui-block-content/div/div/p-table/div/p-paginator/div/button[3]")

        next_page_button = self.wait_for_presence(next_page_button_location)

        return next_page_button

    def find_previous_page_button(self) -> WebElement:
        """
            Finds and returns the previous page button on the search results page.

            Returns:
                - The WebElement representing the previous page button.
        """
        previous_page_button_location = (By.XPATH,
                                         '/html/body/app-root/eui-block-content/div/ecl-app/div/div/div/app-search-eo'
                                         '/eui-block-content/div/div/p-table/div/p-paginator/div/button[2]')

        previous_page_button = self.wait_for_presence(previous_page_button_location)

        return previous_page_button

    def find_last_page_button(self):
        # TODO: Function that is not implemented in the main code. It exists for the sole purpose to start scraping
        #  from last page to first. Why? Right now there is memory problem where the longer it scraps to more RAM it
        #  takes. So this function can be used to start scraping from different spot to lower RAM consumption.
        #  Example: you start scraping from first page to last -> you get to half of the pages and the RAM gets out
        #  of control -> you start scraping from last page to first instead until you meet the point where you
        #  stopped. It is bad solution and I need to find where the memory problem is. Somewhere selenium is not
        #  closing properly instances or the cache is getting out of control, needs further investigation. You need
        #  to implement it manually in the main.py. To do it you need to make it when you get the first page to click
        #  on the last page and then start scraping then change the next button instead to be for the previous
        #  button so it click on the previous button instead, all functions are implemented and it is easy to do so
        #  if needed.

        """
            Finds and returns the last page button on the search results page.

            Returns:
                - The WebElement representing the last page button.
        """
        last_page_button_location = (By.XPATH,
                                     '/html/body/app-root/eui-block-content/div/ecl-app/div/div/div/app-search-eo/eui'
                                     '-block-content/div/div/p-table/div/p-paginator/div/button[4]')

        last_page_button = self.wait_for_presence(last_page_button_location)

        return last_page_button

    def find_table_dropdown_trigger(self) -> WebElement:
        """
            Finds and returns the dropdown trigger element for selecting rows per page.

            Returns:
                - The WebElement representing the dropdown trigger.
        """
        table_dropdown_trigger_location = (By.CLASS_NAME, 'p-dropdown-trigger')

        table_dropdown_trigger = self.wait_for_presence(table_dropdown_trigger_location)

        return table_dropdown_trigger

    def find_option_for_table_rows(self) -> List[WebElement]:
        """
            Finds and returns the options available for selecting rows per page.

            Returns:
                - A list of WebElements representing the available options.
        """
        options_location = (By.TAG_NAME, 'p-dropdownitem')

        self.wait_for_presence(options_location)

        options = self.find_elements(self.driver, options_location)

        return options

    def choose_table_rows_per_page(self, num: int) -> None:
        """
            Chooses the number of rows to display per page in the search results table.

            Args:
                - num: The number of rows to display per page.
        """
        table_dropdown = self.find_table_dropdown_trigger()

        table_dropdown.click()

        options = self.find_option_for_table_rows()

        for option in options:
            if option.text == num:
                option.click()
                break

    def find_actor_id(self, row_num: int) -> str:
        """
            Finds and returns the actor ID for a specific row of the search results table.

            Args:
                - row_num: The row number for which to find the actor ID.

            Returns:
                - The actor ID as a string.
        """
        actor_id_location = (By.XPATH,
                             f'/html/body/app-root/eui-block-content/div/ecl-app/div/div/div/app-search-eo/eui-block'
                             f'-content/div/div/p-table/div/div/table/tbody/tr[{row_num}]/td[1]')

        actor_id = self.wait_for_presence(actor_id_location)

        return self.extract_text(actor_id)

    @staticmethod
    def is_button_disabled(button: WebElement) -> bool:
        """
            Checks if a button element is disabled.

            Args:
                - button: The button element to check.

            Returns:
                - True if the button is disabled, False otherwise.
        """
        return "p-disabled" in button.get_attribute("class")
