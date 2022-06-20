from pyrsistent import b
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
    description: str
    style: dict
    character: list


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
    def get_whiskey_url_list(self):
        az_item_links = self.driver.find_elements(By.XPATH, '//*[@class="az-item-link"]')
        
        whiskey_brand_href_list = []
        for az_item_link in az_item_links:
            whiskey_href = az_item_link.get_attribute('href')
            whiskey_brand_href_list.append(whiskey_href)

        return whiskey_brand_href_list

    def get_full_whiskey_url_list(self, url_list):
        with open('full_whiskey_url_list.text', 'w') as l:
            pass
        for whiskey_url in url_list:
            self.driver.get(whiskey_url)
            time.sleep(1)
            product_cards = self.driver.find_elements(By.XPATH, '//*[@class="product-card"]')
            full_whiskey_url_list = []

            for product_card in product_cards:
                whiskey_href = product_card.get_attribute('href')
                domain = 'https://thewhiskeyexchange.com'
                
                with open('full_whiskey_url_list.text', 'a') as l:    
                    l.write(f'{whiskey_href}')
                    l.write('\n')
                full_whiskey_url_list.append(whiskey_href)

        return full_whiskey_url_list

    def get_whiskey_profile(self, list_of_whiskey_urls):
        for whiskey_url in list_of_whiskey_urls:
            self.driver.get(whiskey_url)
            time.sleep(1)
            name = self.driver.find_element(By.XPATH, '//h1[@class="product-main__name"').text
            subname = self.driver.find_element(By.XPATH, '//h1[@class="product-main__sub-name"').text
            main_data = self.driver.find_element(By.XPATH, '//p[@class="product-main-data"').text
            main_data_tuple = main_data.split(' / ')
            contents_liquid_volume = main_data_tuple[0]
            alcohol_by_volume = main_data_tuple[1]
            facts = self.driver.find_elements(By.XPATH, '//li[@class="product-facts__item"')
            facts_dict = {}
            for fact in facts:
                fact_type = fact.find_element(By.XPATH, './p[@class="product-facts__type"').text
                fact_

            flavour_profile = fact.



            type = self.driver.find_element(By.XPATH, '//h1[@class="product-main__name"').text
            link = self.driver.find_element(By.XPATH, '//h1[@class="product-main__name"').text
            
            price = self.driver.find_element(By.XPATH, '//h1[@class="product-main__name"').text
            description = self.driver.find_element(By.XPATH, '//h1[@class="product-main__name"').text
            
            Character: list


            whiskey = Whiskey()



    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        pass

    def scraper_quit(self):
        self.driver.close()
        self.driver.quit()

    def run(self):
        self.load_and_accept_cookies()
        whiskey_url_list = self.get_whiskey_url_list()
        full_whiskey_url_list = self.get_full_whiskey_url_list(whiskey_url_list)
        
        print(len(full_whiskey_url_list))
        self.scraper_quit()

if __name__ == '__main__':
    scraperinstance = Scraper()
    scraperinstance.run()
    
    



    

    



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




    



