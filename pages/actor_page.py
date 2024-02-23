from selenium.webdriver.common.by import By

from pages.utils.page_helper import PageHelper


class ActorPage(PageHelper):
    def __init__(self, driver, wait_time):
        super().__init__(driver, wait_time)

    def wait_for_actor_information_to_load(self):
        actor_information_location = (By.ID, 'actor_information')

        # self.wait_for_presence(actor_information_location)

        return self.wait_for_presence(actor_information_location)

    def find_actor_information_last_updated(self):
        information_last_updated_location = (By.XPATH,
                                             '/html/body/app-root/eui-block-content/div/ecl-app/div/div/div/app-eo'
                                             '-detail/eui-block-content/div/div/div[2]/div[2]/div['
                                             '1]/div/mat-accordion/mat-expansion-panel/div/div/div['
                                             '1]/app-history-nav/ul/li[2]')

        # self.wait_for_presence(information_last_updated_location)

        information_last_updated = self.wait_for_presence(information_last_updated_location)

        information_last_updated_text_split = self.extract_text(information_last_updated).split(': ')

        key, value = information_last_updated_text_split[0], information_last_updated_text_split[1]

        return {key: value}

    def find_actor_dl_elements(self, actor_information_container):
        actor_dl_elements_location = (By.TAG_NAME, 'dl')

        self.wait_for_presence(actor_dl_elements_location)

        actor_dl_elements = self.find_elements(actor_information_container, actor_dl_elements_location)

        return actor_dl_elements

    def find_actor_information_container(self):
        actor_information_location = (By.XPATH,
                                      '/html/body/app-root/eui-block-content/div/ecl-app/div/div/div/app-eo-detail'
                                      '/eui-block-content/div/div/div[2]/div[2]/div['
                                      '1]/div/mat-accordion/mat-expansion-panel/div/div/div[2]')

        return self.wait_for_presence(actor_information_location)

    def extract_actor_information(self):
        actor_information = self.find_actor_information_container()

        actor_information_dl_elements = self.find_actor_dl_elements(actor_information)

        actor_information_text_parsed = self.parse_text(actor_information_dl_elements)

        actor_information_text_parsed.update(self.find_actor_information_last_updated())
        actor_information_text_parsed['Actor URL'] = self.driver.current_url

        return actor_information_text_parsed

    @staticmethod
    def parse_text(dl_elements):
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
