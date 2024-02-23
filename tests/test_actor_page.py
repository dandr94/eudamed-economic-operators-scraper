import unittest
from unittest.mock import Mock

from selenium import webdriver

from pages.actor_page import ActorPage


class TestActorPage(unittest.TestCase):
    WEBDRIVER_OPTIONS = ['--headless=new', '--disable-extensions', '--disable-infobars', '--disable-gpu',
                         '--disable-notifications']
    TEST_URL = 'https://ec.europa.eu/tools/eudamed/#/screen/search-eo/22938fc4-eadb-459b-9a6a-14defd0275c8'

    EXPECTED_DATA = {
        "Actor ID/SRN": "AD-MF-000001354",
        "Role": "Manufacturer",
        "Country": "Andorra",
        "Actor/Organisation name": "SOADCO, S.L. [ES]",
        "Abbreviated name": "SOADCO, S.L. [ES]",
        "VAT number": "-",
        "EORI": "BEAD923395B",
        "National trade register": "923395B",
        "Last confirmation date of actor data accuracy": "-",
        "Street name": "Av. del Pessebre",
        "Street number": "76-82",
        "Address line 2": "-",
        "PO box": "-",
        "City name": "Escaldes-Engordany",
        "Postal Code": "AD700",
        "Latitude": "42.513416",
        "Longitude": "1.535454",
        "Email": "maria.mitjaneta@soadco.com",
        "Telephone number": "+37 6 800 590",
        "Web site": "-",
        "Last update date": "2021-02-11",
        "Actor URL": "https://ec.europa.eu/tools/eudamed/#/screen/search-eo/22938fc4-eadb-459b-9a6a-14defd0275c8"
    }

    def setUp(self) -> None:
        options = webdriver.ChromeOptions()

        for option in self.WEBDRIVER_OPTIONS:
            options.add_argument(option)

        self.driver = webdriver.Chrome(options=options)

        self.driver.get(self.TEST_URL)

        self.actor_page = ActorPage(self.driver, 3)
    #
    # def tearDown(self):
    #     self.driver.quit()

    def test_wait_for_actor_information_to_load(self):
        actor_information_element = self.actor_page.wait_for_actor_information_to_load()

        self.assertTrue(actor_information_element.is_displayed())

    def test_find_actor_information_last_updated(self):
        last_updated_info = self.actor_page.find_actor_information_last_updated()

        key = 'Last update date'

        self.assertIsNotNone(last_updated_info)
        self.assertIn(key, last_updated_info)

        # This will fail if record gets updated
        self.assertEqual(self.EXPECTED_DATA[key], last_updated_info[key])

    def test_find_actor_information_container(self):
        actor_information_container = self.actor_page.find_actor_information_container()

        self.assertIsNotNone(actor_information_container)

    def test_find_actor_dl_elements(self):
        actor_information_container = self.actor_page.find_actor_information_container()

        self.assertIsNotNone(actor_information_container)

        actor_dl_elements = self.actor_page.find_actor_dl_elements(actor_information_container)

        self.assertTrue(actor_dl_elements)

        self.assertIsInstance(actor_dl_elements, list)

    def test_parse_text(self):
        mock_dl_element1 = Mock()
        mock_dl_element1.text = "Role\nManufacturer"

        mock_dl_element2 = Mock()
        mock_dl_element2.text = "Street number\n123 Street"

        mock_dl_element3 = Mock()
        mock_dl_element3.text = "Email\ncontact@example.com"

        mock_dl_element4 = Mock()
        mock_dl_element4.text = "Actor identification"

        mock_dl_element5 = Mock
        mock_dl_element5.text = "Phone number"

        dl_elements = [mock_dl_element1, mock_dl_element2, mock_dl_element3, mock_dl_element4, mock_dl_element5]
        parsed_data = self.actor_page.parse_text(dl_elements)

        self.assertTrue(isinstance(parsed_data, dict))
        self.assertEqual(parsed_data, {
            'Role': 'Manufacturer',
            'Street number': '123 Street',
            'Email': 'contact@example.com',
            'Phone number': '-'
        })
        self.assertNotIn(mock_dl_element4.text, parsed_data)

    # This test could fail if data is updated, right now expected data is hard coded
    def test_extract_actor_information(self):
        actor_information = self.actor_page.extract_actor_information()

        self.assertEqual(self.EXPECTED_DATA, actor_information)
