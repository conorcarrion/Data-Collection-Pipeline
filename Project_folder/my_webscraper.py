from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from dataclasses import dataclass
from typing import List

options = Options()
options.add_argument('--headless')


@dataclass
class Whiskey:
    """Class for detailing attributes of a whiskey."""
    name: str
    type: str
    link: str
    alcohol_by_volume: float
    bottle_price: float
    Description: str
    Style: dict
    Character: list


class Scraper():
    
    def __init__(self) -> None:
        pass

    def load_and_accept_cookies(self):
        self.driver = webdriver.Chrome(options=options)
        URL = 'https://www.thewhiskyexchange.com/brands/scotchwhisky/40/single-malt-scotch-whisky'
        self.driver.get(URL)
        time.sleep(2)
        try: 
            accept_cookies = self.driver.find_element(By.XPATH, '//button[@data-tid="banner-accept"]')
            accept_cookies.click()
            
        except:
            pass
        time.sleep(3)

     # Methods to crawl through website
    def get_whiskey_href_list(self):
        az_item_links = self.driver.find_elements(By.XPATH, '//*[@class="az-item-link"]')
        
        whiskey_brand_href_list = []
        for az_item_link in az_item_links:
            whiskey_href = az_item_link.get_attribute('href')
            whiskey_brand_href_list.append(whiskey_href)

        return whiskey_brand_href_list

    def go_to_letter(letter):
        URL = URL + f'#goto-{letter}'

    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        pass

    def scraper_quit(self):
        self.driver.close()
        self.driver.quit()

    def run(self):
        self.load_and_accept_cookies()
        self.get_whiskey_href_list()
        self.scraper_quit()

if __name__ == '__main__':
    scraperinstance = Scraper()
    scraperinstance.run()
    print(scraperinstance.get_whiskey_href_list())
    print(len(scraperinstance.get_whiskey_href_list()))
    



    

    



# methods to retrieve data

    # def get_name():
    #     whiskey_name = whiskey_item_list.find_elements(By.XPATH, './div/header/h2[@class="top10-product__name"]')

    # def get_type():
    #     pass

    # def get_link():
    #     pass

    # def get_alcohol_by_volume():
    #     pass

    # def get_bottle_price():
    #     pass

    # def get_description():
    #     pass

    # def get_style():
    #     pass    
    
    # def get_character():
    #     pass




    



