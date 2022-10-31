from lib.Scraper import Scraper
from lib.Spirit import Spirit
from lib.FileManager import FileManager
import unittest
import time
import random
import re


class ScraperTestCase(unittest.TestCase):

    def setUp(self):

        self.url = 'https://www.thewhiskyexchange.com/c/40/single-malt-scotch-whisky?pg=1&psize=24&sort=nasc'
        self.scraper = Scraper(self.url, True)
        self.scraper.accept_cookies
         
    def test_pagenumber_adjuster(self):

        expected_number = random.randint(1,5)
        expected_number_string = f'pg={expected_number}'
        new_page = self.scraper.pagenumber_adjuster(self.url, expected_number)
        
        page = re.compile('pg=[0-9]+')
        actual_number_string = page.findall(new_page)[0]

        self.assertEqual(actual_number_string, expected_number_string)   

    def test_get_url_list(self):

        laga_url = 'https://www.thewhiskyexchange.com/b/40/lagavulin-single-malt-scotch-whisky?pg=1&psize=10'
        expected_url_list = self.scraper.get_url_list(laga_url)
        
        FileManager.output_list_to_text_file(expected_url_list, 'tests')
        assert type(expected_url_list) is list
        self.assertEqual(len(expected_url_list), self.scraper.total_product_cards_number)

        for url in expected_url_list:
            assert 'www.thewhiskyexchange.com/' in url, 'a url in the list does not contain expected domain'

    def test_get_a_spirit_profile(self):
        
        test_url = 'https://www.thewhiskyexchange.com/p/3121/lagavulin-16-year-old'
        self.scraper.driver.get(test_url)
        self.scraper.driver.implicitly_wait(2)

        actual_spirit_profile = self.scraper.get_a_spirit_profile(test_url, Spirit())
        assert actual_spirit_profile.name == 'Lagavulin 16 Year Old'
        assert actual_spirit_profile.alcohol_by_volume == '43%'
        assert actual_spirit_profile.contents_liquid_volume == '70cl'

    def tearDown(self):
        self.scraper.scraper_quit
        del self.scraper
        time.sleep(1)
     
unittest.main(argv=[''], verbosity=3, exit=False, warnings='ignore')