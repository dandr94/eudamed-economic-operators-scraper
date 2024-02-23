import logging
import time
import psutil

class TextFormatter:
    """
        A utility class for formatting text messages with ANSI color codes and symbols, making it easier to convey
        the meaning and status of messages in a visually distinguishable manner.
    """

    def __init__(self):
        self.symbols = {
            'success': '\u2713',
            'fail': '\u2717',
            'work_in_progress': '\u21AC'
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
        return f'{self.ANSI[color]}{self.symbols[symbol]} {message}{self.ANSI["reset"]}'

    def format_message_success(self, message: str) -> str:
        return self.format_message(message, 'green', 'success')

    def format_message_fail(self, message: str) -> str:
        return self.format_message(message, 'red', 'fail')

    def format_message_work_in_progress(self, message: str) -> str:
        return self.format_message(message, 'yellow', 'work_in_progress')

    def format_custom_message(self, message: str, color: str) -> str:
        return f'{self.ANSI[color]} {message}{self.ANSI["reset"]}'


# Logger class for handling logging
class Logger:
    """
    A class for logging messages to a file.
    """
    LOG_FILE_NAME = 'app.log'
    LOG_FORMATTER = '%(asctime)s - %(levelname)s - %(message)s'

    def __init__(self):
        """
        Initialize the Logger class.

        This constructor sets up the logger with a specified format and file handler.
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


class MemoryUsageExceededError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class MessageProvider:
    def __init__(self):
        self.text_formatter = TextFormatter()

    def timed_custom_message(self, msg, color):
        return self.text_formatter.format_custom_message(f'[{get_current_time()}] - {msg}', color)

    def app_starting(self):
        msg = 'The scrapping has now started...'

        print(self.timed_custom_message(msg, 'green'))

    def working_on(self, url):
        msg = f'Working on record with URL: {url}...'

        print(self.timed_custom_message(msg, 'yellow'))

    def completed_record(self, url):
        msg = f'Successfully scrapped the record with URL: {url}!'

        print(self.timed_custom_message(msg, 'green'))

    def saved_current_scrapped_data(self):
        msg = 'Saving collected data. Continuing to the next page...'

        print(self.timed_custom_message(msg, 'green'))

    def time_of_current_session(self, start_time):
        elapsed_time_seconds = int(time.time() - start_time)

        hours = elapsed_time_seconds // 3600
        minutes = (elapsed_time_seconds % 3600) // 60
        seconds = (elapsed_time_seconds % 3600) % 60

        elapsed_time_formatted = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        msg = f'Time elapsed: {elapsed_time_formatted}'

        print(self.timed_custom_message(msg, 'yellow'))

    def average_time_until_completion(self, records_remaining, records_per_page, time_per_page):
        pages_remaining = records_remaining / records_per_page
        estimated_time_until_completion = pages_remaining * time_per_page

        days = int(estimated_time_until_completion // (24 * 3600))
        hours = int((estimated_time_until_completion % (24 * 3600)) // 3600)
        minutes = int((estimated_time_until_completion % 3600) // 60)
        seconds = int(estimated_time_until_completion % 60)

        msg = f'Estimated time until completion: {days} day(s), {hours} hour(s), {minutes} minute(s), {seconds} second(s)'

        print(self.timed_custom_message(msg, 'yellow'))

    def remaining_records(self, remaining_records):
        msg = f'Remaining records: {remaining_records}...'

        print(self.timed_custom_message(msg, 'yellow'))

    def keyboard_interruption_msg(self):
        msg = 'Scrapping interrupted by user!'

        print(self.timed_custom_message(msg, 'red'))

    def unexpected_error_msg(self, exception):
        msg = f'Unexpected error has occurred: {str(exception)}'

        print(self.timed_custom_message(msg, 'red'))

    def scrapping_completed_msg(self, filename):
        msg = f'Scrapping has successfully finished! Data has been saved to {filename}.'

        print(self.timed_custom_message(msg, 'green'))

    def record_already_scrapped(self, actor_id):
        msg = f'Record with actor ID {actor_id} already scrapped. Continuing to the next one...'

        print(self.timed_custom_message(msg, 'yellow'))

    def memory_usage_exceeded_msg(self, max_memory_usage_in_gb):
        msg = f'Memory usage exceeded {max_memory_usage_in_gb} GB. Stopping the application.'

        print(self.timed_custom_message(msg, 'red'))

    def current_memory_usage_msg(self, current_memory_usage_in_gb):
        msg = f'Current memory usage: {current_memory_usage_in_gb:.2f} GB'

        print(self.timed_custom_message(msg, 'yellow'))


def get_current_time() -> str:
    return time.strftime("%H:%M:%S", time.localtime())


def get_current_memory_usage_in_gb():
    current_memory_usage_bytes = psutil.Process().memory_info().rss
    memory_usage_gb = current_memory_usage_bytes / (1024 ** 3)

    return memory_usage_gb
