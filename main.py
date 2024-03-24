import time

from selenium import webdriver
from data_handling import load_data, save_data
from pages.actor_page import ActorPage
from pages.browse_page import BrowsePage
from utils import MessageProvider, TextFormatter
from data_handling import OUTPUT_FILENAME


class ScraperOptions:
    # Available roles
    MANUFACTURER_ROLE = 'manufacturer'
    IMPORTER_ROLE = 'importer'

    # Change this to "importer" to extract importer data
    ROLE = 'importer'

    ROLE_VALUE_ERROR_MSG = "Invalid role specified."
    # Options: 10, 25, 50. Changes how many records are there in a table per page
    ROWS_PER_PAGE = 10

    # TODO: Fetch the total records found everytime the app is starting instead of hard-coding the value
    # Keeping this precise can improve estimated time
    TOTAL_RECORDS_FOUND = 7213   # Last update: 24.03.2024

    # The time it takes to load a page (in seconds), used for calculating total estimated time for completion. Change
    # as needed.
    PAGE_LOAD_TIME = 2

    # How much consecutive exceptions can be raised before the program stops for good.
    MAX_CONSECUTIVE_EXCEPTIONS = 5

    # The wait time between runs (in seconds). When the app raises an error, it will try to start the program again
    # after that time if MAX_CONSECUTIVE_EXCEPTIONS has not reached the maximum
    WAIT_TIME_BETWEEN_RUNS = 30


class WebDriverOptions:
    # Options you can pass to configurate your webdriver. '--headless=new'
    # More info: https://github.com/GoogleChrome/chrome-launcher/blob/main/docs/chrome-flags-for-tools.md

    WEBDRIVER_OPTIONS = ['--headless=new', '--disable-extensions', '--disable-infobars', '--disable-gpu',
                         '--disable-notifications']

    # Depends on the loading time of your page (in seconds). Adjust as needed or pass a value as argument when you initialize the
    # class.
    WEBDRIVER_WAIT_TIME = 10

    def __init__(self, wait_time: int = WEBDRIVER_WAIT_TIME):
        self.web_driver_wait_time = wait_time

    @property
    def get_web_driver_wait_time(self):
        return self.web_driver_wait_time

    def get_driver_options(self) -> webdriver.ChromeOptions:
        options = webdriver.ChromeOptions()

        for option in self.WEBDRIVER_OPTIONS:
            options.add_argument(option)

        return options


class Scraper(ScraperOptions):
    def __init__(self, driver, browse_page: BrowsePage, actor_page: ActorPage, message_provider: MessageProvider):
        self.driver = driver
        self.browse_page = browse_page
        self.actor_page = actor_page
        self.message_provider = message_provider
        self.remaining_records = self.TOTAL_RECORDS_FOUND
        self.existing_data = load_data(
            OUTPUT_FILENAME)  # TODO: Make filename to be dynamic (depending on the role chosen) instead of hard coding the name
        self.new_data = {}  # TODO: Maybe remove this and pass it to functions
        self.session_time = 0
        self.loop_start_time = 0
        self.loop_end_time = 0

    def run(self) -> None:
        """
            Runs the scraping process.

            This function orchestrates the scraping process by handling exceptions, initializing the driver,
            executing data scraping, and displaying messages. If unknown exception is raised it will try to restart
            the process again if MAX_CONSECUTIVE_EXCEPTIONS are not reached.

        """
        consecutive_exceptions = 0

        while consecutive_exceptions < self.MAX_CONSECUTIVE_EXCEPTIONS:
            self.message_provider.app_starting()

            try:
                self.start_scraping_data()

                self.message_provider.scrapping_completed_msg(OUTPUT_FILENAME)

            except KeyboardInterrupt:
                self.message_provider.keyboard_interruption_msg()
                break

            except Exception as e:
                consecutive_exceptions += 1
                self.message_provider.unexpected_error_msg(e)

            finally:
                self.cleanup()

            # If scraping failed, wait before attempting again
            if consecutive_exceptions > 0:
                time.sleep(self.WAIT_TIME_BETWEEN_RUNS)

    def cleanup(self) -> None:
        """
            Cleans up resources.

            Quits the WebDriver if it exists to free up system resources.

        """
        if self.driver:
            self.driver.quit()

    def go_to_next_page_if_possible(self) -> bool:
        """
        Go to the next page if available.
        """
        next_page_button = self.browse_page.find_next_page_button()

        if self.browse_page.is_button_disabled(next_page_button):
            return False
        else:
            next_page_button.click()
            return True

    def save_existing_data(self) -> None:
        """
        Save scraped data.
        """
        self.existing_data.update(self.new_data)

        save_data(self.existing_data, OUTPUT_FILENAME)

        self.message_provider.saved_current_scrapped_data()

    def display_completion_time(self) -> None:
        """
        Display average completion time.
        """
        self.loop_end_time = time.time()

        time_per_page = self.loop_end_time - self.loop_start_time

        self.message_provider.average_time_until_completion(
            self.remaining_records, self.ROWS_PER_PAGE, time_per_page + self.PAGE_LOAD_TIME)

    def display_session_info(self) -> None:
        """
        Display session information.
        """
        self.message_provider.time_of_current_session(self.session_time)
        self.message_provider.remaining_records(self.remaining_records)

    def process_table_rows(self, table_rows_count: int) -> None:
        """
            Processes each row in the table.

            Parameters:
            - table_rows_len: int. Number of table rows on the current page

            This method iterates through each row in the provided table,
            retrieves the actor ID for each row, checks if the actor ID exists in the existing data,
            and calls the scrape_actor_page method to scrape data if the actor ID is not in the existing data.
            If the actor ID is already present, it logs a message indicating that the record has already been scraped.
        """

        # We need to use this kind of loop because if we iter through the rows, as elements it will raise
        # StaleElementReferenceException
        for i in range(0, table_rows_count - 1):
            actor_id = self.browse_page.find_actor_id(i + 1)

            if actor_id in self.existing_data:
                self.message_provider.record_already_scrapped(actor_id)
                continue

            self.scrape_actor_page(i, actor_id)

    def scrape_actor_page(self, i: int, actor_id: str) -> None:
        """
            Scrapes information from the actor page based on the given index and actor ID.

            Parameters:
            - i: The index of the current row.
            - actor_id: The ID of the actor whose page is being scraped.

            This method locates and clicks the action button associated with the specified row,
            waits for the actor information to load, captures the actor's information,
            updates the new data with the scraped information, logs the completion of the record,
            and navigates back to the previous page.
        """
        current_row_button = self.browse_page.find_action_button(i)

        self.browse_page.scroll_to_element(current_row_button)

        current_row_button.click()

        self.actor_page.wait_for_actor_information_to_load()

        self.message_provider.working_on(self.driver.current_url)

        self.new_data[actor_id] = self.actor_page.extract_actor_information()

        self.message_provider.completed_record(self.driver.current_url)

        self.driver.back()

    def scrape_pages(self) -> None:
        """
            Scrapes data from each page of the table.

            This method starts a session timer, refreshes the browser page,
            waits for the table to load, finds the table rows,
            calculates the remaining records to be scraped,
            processes each table row, displays session information,
            saves the existing data if new data is found, and displays completion time.

            The scraping continues until there are no more pages to scrape.
        """
        self.session_time = time.time()

        while True:
            self.loop_start_time = time.time()

            self.driver.refresh()

            self.browse_page.wait_for_table_to_load()

            table_rows = self.browse_page.find_table_rows()

            self.remaining_records = self.TOTAL_RECORDS_FOUND - len(self.existing_data)

            self.process_table_rows(len(table_rows))

            self.display_session_info()

            if len(self.new_data) > 0:
                self.save_existing_data()
                self.display_completion_time()

            if not self.go_to_next_page_if_possible():
                break

    def load_role(self) -> None:
        """
        Loads the appropriate role data based on the specified role.
        """
        if self.ROLE == self.MANUFACTURER_ROLE:
            self.browse_page.load_url(self.MANUFACTURER_ROLE)
        elif self.ROLE == self.IMPORTER_ROLE:
            self.browse_page.load_url(self.IMPORTER_ROLE)
        else:
            raise ValueError(self.ROLE_VALUE_ERROR_MSG)

    def start_scraping_data(self) -> None:
        """
            Initiates the data scraping process based on the specified role.

            If the role is set to 'manufacturer', load the manufacturers' data.
            If the role is set to 'importer', load the importers' data.
            Raises a ValueError if an invalid role is specified.
        """

        self.load_role()

        self.browse_page.accept_cookies()

        # Right now the close prompt does not exist as 24.03.2024. When I was working on this project, a month ago
        # there was one. So if they decide to introduce it again, this is a fail-safe; hopefully they introduce it
        # with the same attribute...
        self.browse_page.close_cookies_prompt_after_accept()

        self.browse_page.choose_table_rows_per_page(self.ROWS_PER_PAGE)

        self.scrape_pages()


if __name__ == "__main__":
    # You can pass wait time if you need to adjust it, currently default is 10s wait time.
    web_driver_options = WebDriverOptions()

    driver = webdriver.Chrome(options=web_driver_options.get_driver_options())

    browse_page = BrowsePage(driver, web_driver_options.get_web_driver_wait_time)

    actor_page = ActorPage(driver, web_driver_options.get_web_driver_wait_time)

    test_formatter = TextFormatter()

    message_provider = MessageProvider(test_formatter)

    scraper = Scraper(driver, browse_page, actor_page, message_provider)

    scraper.run()
