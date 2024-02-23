import time

from selenium import webdriver

from data_handling import load_data, save_data
from pages.actor_page import ActorPage
from pages.browse_page import BrowsePage
from utils import MessageProvider
from data_handling import OUTPUT_FILENAME


class Scraper:
    WEBDRIVER_OPTIONS = ['--headless=new', '--disable-extensions', '--disable-infobars', '--disable-gpu',
                         '--disable-notifications']
    WEBDRIVER_WAIT_TIME = 10
    ROWS_PER_PAGE = 50
    TOTAL_RECORDS_FOUND = 23153  # 21.02.2024
    PAGE_LOAD_TIME = 2
    MAX_CONSECUTIVE_EXCEPTIONS = 5
    WAIT_TIME_BETWEEN_RUNS = 30
    MAX_MEMORY_USAGE_GB = 10

    def __init__(self):
        self.driver = None
        self.browse_page = None
        self.actor_page = None
        self.message_provider = MessageProvider()
        self.remaining_records = self.TOTAL_RECORDS_FOUND

    def initialize_driver(self):
        options = webdriver.ChromeOptions()

        for option in self.WEBDRIVER_OPTIONS:
            options.add_argument(option)

        self.driver = webdriver.Chrome(options=options)

        self.browse_page = BrowsePage(self.driver, self.WEBDRIVER_WAIT_TIME)

        self.actor_page = ActorPage(self.driver, self.WEBDRIVER_WAIT_TIME)

    def cleanup(self):
        if self.driver:
            self.driver.quit()

    def run(self):
        consecutive_exceptions = 0

        while consecutive_exceptions < self.MAX_CONSECUTIVE_EXCEPTIONS:
            self.message_provider.app_starting()

            try:
                self.initialize_driver()

                self.scrape_data()

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

    def scrape_data(self):
        self.browse_page.load_manufacturers()

        self.browse_page.accept_cookies()

        self.browse_page.close_cookies_prompt_after_accept()

        # Only works if the window size is maximize_window() with resolution of monitor 1920x1080
        self.browse_page.choose_table_rows_per_page(str(self.ROWS_PER_PAGE))

        time.sleep(2)

        last_page_button = self.browse_page.find_last_page_button()

        self.browse_page.scroll_to_element(last_page_button)

        last_page_button.click()

        start_session_time = time.time()

        existing_data = load_data(OUTPUT_FILENAME)

        while True:
            loop_start_time = time.time()

            new_data = {}

            self.driver.refresh()

            self.browse_page.wait_for_table_to_load()

            table_rows = self.browse_page.find_table_rows()

            self.remaining_records = self.TOTAL_RECORDS_FOUND - len(existing_data)

            for i in range(0, len(table_rows) - 1):
                actor_id = self.browse_page.find_actor_id(i + 1)

                # self.remaining_records -= 1

                if actor_id in existing_data:
                    self.message_provider.record_already_scrapped(actor_id)
                    continue

                current_row_button = self.browse_page.find_action_button(i)

                self.browse_page.scroll_to_element(current_row_button)

                current_row_button.click()

                self.actor_page.wait_for_actor_information_to_load()

                self.message_provider.working_on(self.driver.current_url)

                new_data[actor_id] = self.actor_page.extract_actor_information()

                self.message_provider.completed_record(self.driver.current_url)

                self.driver.back()

            self.message_provider.time_of_current_session(start_session_time)

            self.message_provider.remaining_records(self.remaining_records)

            if len(new_data) > 0:
                existing_data.update(new_data)

                save_data(existing_data, OUTPUT_FILENAME)

                self.message_provider.saved_current_scrapped_data()

                loop_end_time = time.time()

                time_per_page = loop_end_time - loop_start_time

                self.message_provider.average_time_until_completion(
                    self.remaining_records, self.ROWS_PER_PAGE, time_per_page + self.PAGE_LOAD_TIME)

            next_page_button = self.browse_page.find_next_page_button()

            # previous_page_button = self.browse_page.find_previous_page_button()

            if self.browse_page.is_button_disabled(next_page_button):
                break
            else:
                next_page_button.click()


if __name__ == "__main__":
    scraper = Scraper()
    scraper.run()
