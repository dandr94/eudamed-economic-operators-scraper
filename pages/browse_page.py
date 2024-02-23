from selenium.webdriver.common.by import By

from pages.utils.page_helper import PageHelper


class BrowsePage(PageHelper):
    def __init__(self, driver, wait_time):
        super().__init__(driver, wait_time)

    def wait_for_table_to_load(self):
        table_location = (
            By.XPATH,
            '/html/body/app-root/eui-block-content/div/ecl-app/div/div/div/app-search-eo/eui-block-content/div')

        self.wait_for_presence(table_location)

    def find_table_rows(self):
        table_rows_location = (By.TAG_NAME, 'tr')

        self.wait_for_presence(table_rows_location)

        rows = self.find_elements(self.driver, table_rows_location)

        return rows

    def find_action_button(self, row_num):
        action_button_location = (By.XPATH,
                                  f'/html/body/app-root/eui-block-content/div/ecl-app/div/div/div/app-search-eo/eui'
                                  f'-block-content/div/div/p-table/div/div/table/tbody/tr[{row_num + 1}]/td[8]/button')

        action_button = self.wait_for_presence(action_button_location)

        return action_button

    def find_next_page_button(self):
        next_page_button_location = (By.XPATH,
                                     "/html/body/app-root/eui-block-content/div/ecl-app/div/div/div/app"
                                     "-search-eo/eui-block-content/div/div/p-table/div/p-paginator/div/button[3]")

        next_page_button = self.wait_for_presence(next_page_button_location)

        return next_page_button

    def find_previous_page_button(self):
        previous_page_button_location = (By.XPATH,
                                         '/html/body/app-root/eui-block-content/div/ecl-app/div/div/div/app-search-eo'
                                         '/eui-block-content/div/div/p-table/div/p-paginator/div/button[2]')

        previous_page_button = self.wait_for_presence(previous_page_button_location)

        return previous_page_button

    def find_last_page_button(self):
        last_page_button_location = (By.XPATH,
                                     '/html/body/app-root/eui-block-content/div/ecl-app/div/div/div/app-search-eo/eui'
                                     '-block-content/div/div/p-table/div/p-paginator/div/button[4]')

        last_page_button = self.wait_for_presence(last_page_button_location)

        return last_page_button

    def find_table_dropdown_trigger(self):
        table_dropdown_trigger_location = (By.CLASS_NAME, 'p-dropdown-trigger')

        table_dropdown_trigger = self.wait_for_presence(table_dropdown_trigger_location)

        return table_dropdown_trigger

    def find_option_for_table_rows(self):
        options_location = (By.TAG_NAME, 'p-dropdownitem')

        self.wait_for_presence(options_location)

        options = self.find_elements(self.driver, options_location)

        return options

    def choose_table_rows_per_page(self, num):
        table_dropdown = self.find_table_dropdown_trigger()

        table_dropdown.click()

        options = self.find_option_for_table_rows()

        for option in options:
            if option.text == num:
                option.click()
                break

    def find_actor_id(self, row_num):
        actor_id_location = (By.XPATH,
                             f'/html/body/app-root/eui-block-content/div/ecl-app/div/div/div/app-search-eo/eui-block'
                             f'-content/div/div/p-table/div/div/table/tbody/tr[{row_num}]/td[1]')

        actor_id = self.wait_for_presence(actor_id_location)

        return self.extract_text(actor_id)

    @staticmethod
    def is_button_disabled(button):
        return "p-disabled" in button.get_attribute("class")