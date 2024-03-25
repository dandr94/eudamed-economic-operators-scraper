import logging
import time
from typing import Tuple


class TextFormatter:
    """
        A utility class for formatting text messages with ANSI color codes and symbols, making it easier to convey
        the meaning and status of messages in a visually distinguishable manner.
    """

    def __init__(self):
        self.symbols = {
            'success': '\u2713',  # Checkmark symbol for success
            'fail': '\u2717',  # Cross symbol for failure
            'work_in_progress': '\u21AC'  # Arrow symbol for work in progress
        }

        self.ANSI = {
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'reset': '\033[0m'
        }

    def format_message(self,
                       message: str,
                       color: str,
                       symbol: str) -> str:
        """
            Formats a message with specified color and symbol.

            Args:
                - message: The message to be formatted.
                - color: The color to be applied to the message.
                - symbol: The symbol to be prefixed to the message.

            Returns:
                - Formatted message string.
        """
        return f'{self.ANSI[color]}{self.symbols[symbol]} {message}{self.ANSI["reset"]}'

    def format_message_success(self, message: str) -> str:
        """
            Formats a success message with green color and a checkmark symbol.

            Args:
                - message: The success message to be formatted.

            Returns:
                - Formatted success message string.
        """
        return self.format_message(message, 'green', 'success')

    def format_message_fail(self, message: str) -> str:
        """
            Formats a failure message with red color and a cross-symbol.

            Args:
                - message: The failure message to be formatted.

            Returns:
                - Formatted failure message string.
        """
        return self.format_message(message, 'red', 'fail')

    def format_message_work_in_progress(self, message: str) -> str:
        """
            Formats a work in a progress message with yellow color and an arrow symbol.

            Args:
                - message: The work in progress message to be formatted.

            Returns:
                - Formatted work in progress message string.
        """
        return self.format_message(message, 'yellow', 'work_in_progress')

    def format_custom_message(self, message: str, color: str) -> str:
        """
            Formats a custom message with the specified color.

            Args:
                - message: The custom message to be formatted.
                - color: The color to be applied to the message.

            Returns:
                - Formatted custom message string.
        """
        return f'{self.ANSI[color]} {message}{self.ANSI["reset"]}'


class Logger:
    """
        A class for logging messages to a file.
    """
    LOG_FILE_NAME = 'app.log'
    LOG_FORMATTER = '%(asctime)s - %(levelname)s - %(message)s'

    def __init__(self):
        """
            Initialize the Logger class.
        """
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter(self.LOG_FORMATTER)
        file_handler = logging.FileHandler(self.LOG_FILE_NAME)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def log_info(self, message: str) -> None:
        self.logger.info(message)

    def log_error(self, message: str) -> None:
        self.logger.error(message)

    def log_warning(self, message: str) -> None:
        self.logger.warning(message)


class AppMessages:
    APP_STARTING_MESSAGE = 'The scraping has now started...'
    WORKING_ON_URL_MESSAGE = 'Working on record with URL: {url}...'
    COMPLETED_RECORD_MESSAGE = 'Successfully scraped the record with URL: {url}!'
    SAVED_CURRENT_SCRAPED_DATA = 'Saving collected data. Continuing to the next page...'
    TIME_ELAPSED_MESSAGE = 'Time elapsed: {elapsed_time_formatted}'
    AVERAGE_TIME_UNTIL_COMPLETION_MESSAGE = 'Estimated time until completion: {days} day(s), {hours} hour(s), ' \
                                            '{minutes} minute(s), {seconds} second(s)'
    REMAINING_RECORDS_MESSAGE = 'Remaining records: {remaining_records}...'
    KEYBOARD_INTERRUPTION_MESSAGE = 'Scraping interrupted by user!'
    UNEXPECTED_ERROR_MESSAGE = 'Unexpected error has occurred: {exception}'
    SCRAPING_COMPLETED_MESSAGE = 'Scraping has successfully finished! Data has been saved to {filename}.'
    RECORD_ALREADY_SCRAPED_MESSAGE = 'Record with actor ID {actor_id} already scraped. Continuing to the next one...'


class MessageProvider:
    """
        MessageProvider class for generating and displaying messages during scraping.

        This class provides methods to format and print various messages related to the
        scraping process such as start messages, progress messages, completion messages,
        and error messages.

        Attributes:
            - text_formatter: TextFormatter instance for formatting text messages.
        """

    def __init__(self, text_formatter: TextFormatter, app_messages: AppMessages):
        self.text_formatter = text_formatter
        self.app_messages = app_messages

    def timed_custom_message(self, msg: str, color: str) -> str:
        """
            Formats a custom message with timestamp and specified color.

            Args:
                - msg: The message to be formatted.
                - color: The color to be applied to the message.

            Returns:
                - Formatted message string.
         """
        return self.text_formatter.format_custom_message(f'[{get_current_time()}] - {msg}', color)

    def app_starting(self) -> None:
        """
            Displays a message indicating the start of scraping.
        """

        msg = self.app_messages.APP_STARTING_MESSAGE

        print(self.timed_custom_message(msg, 'green'))

    def working_on(self, url: str) -> None:
        """
            Displays a message indicating work on a specific record URL.

            Args:
                - url: The URL of the record being worked on.
        """
        msg = self.app_messages.WORKING_ON_URL_MESSAGE.format(url=url)

        print(self.timed_custom_message(msg, 'yellow'))

    def completed_record(self, url: str) -> None:
        """
            Displays a message indicating successful completion of scraping for a record.

            Args:
                - url: The URL of the completed record.
        """

        msg = self.app_messages.COMPLETED_RECORD_MESSAGE.format(url=url)

        print(self.timed_custom_message(msg, 'green'))

    def saved_current_scraped_data(self) -> None:
        """
            Displays a message indicating the saving of scraped data and proceeding to the next page.
        """
        msg = self.app_messages.SAVED_CURRENT_SCRAPED_DATA

        print(self.timed_custom_message(msg, 'green'))

    def time_of_current_session(self, start_time: float) -> None:
        """
            Displays the elapsed time since the start of the scraping session.

            Args:
                - start_time: The start time of the scraping session.
        """
        elapsed_time_seconds = int(time.time() - start_time)

        elapsed_time_formatted = format_elapsed_time(elapsed_time_seconds)

        msg = self.app_messages.TIME_ELAPSED_MESSAGE.format(elapsed_time_formatted=elapsed_time_formatted)

        print(self.timed_custom_message(msg, 'yellow'))

    def average_time_until_completion(self, records_remaining: int, records_per_page: int,
                                      time_per_page: float) -> None:
        """
            Displays the estimated time until completion based on the remaining records and time per page.

            Args:
                - records_remaining: The number of remaining records to scrape.
                - records_per_page: The number of records per page.
                - time_per_page: The average time taken to scrape a page.
        """
        days, hours, minutes, seconds = calculate_average_time_until_completion(records_remaining, records_per_page,
                                                                                time_per_page)
        msg = self.app_messages.AVERAGE_TIME_UNTIL_COMPLETION_MESSAGE.format(days=days, hours=hours, minutes=minutes,
                                                                             seconds=seconds)

        print(self.timed_custom_message(msg, 'yellow'))

    def remaining_records(self, remaining_records: int) -> None:
        """
            Displays the number of remaining records to be scraped.

            Args:
                - remaining_records: The number of remaining records.
        """
        msg = self.app_messages.REMAINING_RECORDS_MESSAGE.format(remaining_records=remaining_records)

        print(self.timed_custom_message(msg, 'yellow'))

    def keyboard_interruption_msg(self) -> None:
        """
            Displays a message indicating scraping interruption by the user.
        """
        msg = self.app_messages.KEYBOARD_INTERRUPTION_MESSAGE

        print(self.timed_custom_message(msg, 'red'))

    def unexpected_error_msg(self, exception: Exception) -> None:
        """
            Displays a message indicating an unexpected error during scraping.

            Args:
                - exception: The exception object representing the error.
        """
        msg = self.app_messages.UNEXPECTED_ERROR_MESSAGE.format(exception=str(exception))

        print(self.timed_custom_message(msg, 'red'))

    def scraping_completed_msg(self, filename: str) -> None:
        """
            Displays a message indicating the completion of scraping and the saved file.

            Args:
                - filename: The name of the file where the data is saved.
        """
        msg = self.app_messages.SCRAPING_COMPLETED_MESSAGE.format(filename=filename)

        print(self.timed_custom_message(msg, 'green'))

    def record_already_scraped(self, actor_id: str) -> None:
        """
            Displays a message indicating a record with a specific actor ID has already been scraped.

            Args:
                - actor_id: The ID of the actor whose record has already been scraped.
        """
        msg = self.app_messages.RECORD_ALREADY_SCRAPED_MESSAGE.format(actor_id=actor_id)

        print(self.timed_custom_message(msg, 'yellow'))


def format_elapsed_time(elapsed_time_seconds: int) -> str:
    """
        Formats elapsed time in seconds to HH:MM:SS format.

        Args:
            - elapsed_time_seconds: Elapsed time in seconds.

        Returns:
            - Formatted elapsed time string in HH:MM:SS format.
    """
    hours = elapsed_time_seconds // 3600
    minutes = (elapsed_time_seconds % 3600) // 60
    seconds = (elapsed_time_seconds % 3600) % 60

    elapsed_time_formatted = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    return elapsed_time_formatted


def calculate_average_time_until_completion(records_remaining: int,
                                            records_per_page: int,
                                            time_per_page: float) -> Tuple[int, ...]:
    """
        Calculates the estimated time until completion based on the remaining records, records per page,
        and time per page.

        Args:
            - records_remaining: Number of remaining records to scrape.
            - records_per_page: Number of records displayed per page.
            - time_per_page: Average time taken to scrape a page.

        Returns:
            - Tuple containing the estimated time until completion in days, hours, minutes, and seconds.
    """
    pages_remaining = records_remaining / records_per_page

    estimated_time_until_completion = pages_remaining * time_per_page

    days = int(estimated_time_until_completion // (24 * 3600))
    hours = int((estimated_time_until_completion % (24 * 3600)) // 3600)
    minutes = int((estimated_time_until_completion % 3600) // 60)
    seconds = int(estimated_time_until_completion % 60)

    return days, hours, minutes, seconds


def get_current_time() -> str:
    """
        Gets the current time in HH:MM:SS format.

        Returns:
            - Current time string in HH:MM:SS format.
    """
    return time.strftime("%H:%M:%S", time.localtime())
