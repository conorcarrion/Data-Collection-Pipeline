### Start of my code for Webscraper by Conor Quinn ###

# Import
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from dataclasses import dataclass
from typing import List

# selenium webdriver setup
options = Options()
options.add_argument('--headless')

# dataclass for Whiskey
@dataclass
class Whiskey:
    """Class for detailing attributes of a whiskey."""
    name: str = None
    subname: str = None
    type: str = None
    whiskey_url: str = None
    contents_liquid_volume: str = '0cl'
    alcohol_by_volume: str = '0%'
    bottle_price: str = '£0'
    description: str = 'tasteless'
    facts: dict = None
    flavour_style: dict = None
    flavour_character: list = None
    character: list = None

# Scraper Object with methods to control it
class Scraper():
    
    def __init__(self) -> None:
        pass

    # Start up selenium webdriver with options. Open main page and accept cookies. 
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
        time.sleep(2)

     # Scraping methods

     # Method to fetch all the brands of whiskey from main page into a url list
    def get_whiskey_url_list(self):
        az_item_links = self.driver.find_elements(By.XPATH, '//*[@class="az-item-link"]')
        
        whiskey_brand_href_list = []
        for az_item_link in az_item_links:
            whiskey_href = az_item_link.get_attribute('href')
            whiskey_brand_href_list.append(whiskey_href)

        return whiskey_brand_href_list


    # Method to fetch the urls for individual products from the urls obtained by get_whiskey_url_list
    def get_full_whiskey_url_list(self, url_list):
        with open('full_whiskey_url_list.text', 'w') as l:
            pass
        for whiskey_url in url_list:
            self.driver.get(whiskey_url)
            time.sleep(0.5)
            product_cards = self.driver.find_elements(By.XPATH, '//*[@class="product-card"]')
            full_whiskey_url_list = []

            for product_card in product_cards:
                whiskey_href = product_card.get_attribute('href')
                               
                with open('full_whiskey_url_list.text', 'a') as l:    
                    l.write(f'{whiskey_href}')
                    l.write('\n')
                full_whiskey_url_list.append(whiskey_href)

        return full_whiskey_url_list


    # Method to get the profile of each whiskey product from the list of product urls obtained by get_full_whiskey_url_list
    def get_whiskey_profile(self, list_of_whiskey_urls):

        # Iterate through every whiskey url in the list_of_whiskey_urls
        for whiskey_url in list_of_whiskey_urls:
            self.driver.get(whiskey_url)
            time.sleep(0.5)

            # fetch details of the whiskey
            # basics

        

            name = self.driver.find_element(By.XPATH, '//h1[@class="product-main__name"')
            subname = self.driver.find_element(By.XPATH, '//h1[@class="product-main__sub-name"')
            product_id = self.driver.find_element(By.XPATH, '//input-id[@value="18089"')
            main_data = self.driver.find_element(By.XPATH, '//p[@class="product-main-data"')
            main_data_tuple = main_data.split(' / ')
            contents_liquid_volume = main_data_tuple[0]
            alcohol_by_volume = main_data_tuple[1]

            price = self.driver.find_element(By.XPATH, '//*[@class="product-action__price"')

            description_tag = self.driver.find_element(By.XPATH, '//*[@class="product-main__description"')
            description = description_tag.find_element(By.CLASS_NAME, 'p')

            # facts section
            facts = self.driver.find_elements(By.XPATH, '//*[@class="product-facts__item"')
            facts_dict = {}
            for fact in facts:
                fact_key = fact.find_element(By.TAG_NAME, 'h4')
                fact_value= fact.find_element(By.TAG_NAME, 'p')
                facts_dict[fact_key] = fact_value

            # flavour profile section
            flavour_profile_style = self.driver.find_elements(By.XPATH, '//li[@class="flavour-profile__item flavour-profile__item--style"')
            flavour_style_dict = {}
            for flavour in flavour_profile_style:
                flavour_style_value = flavour.find_element(By.XPATH, '//span[@class="circle-text-content"')
                flavour_style_key = flavour.find_element(By.XPATH, '//span[@class="flavour-profile__label"')
                flavour_style_dict[flavour_style_key] = flavour_style_value

            flavour_profile_character = self.driver.find_elements(By.XPATH, '//li[@class="flavour-profile__item flavour-profile__item--character"')
            flavour_character_list = []
            for flavour in flavour_profile_character:
                flavour_character = flavour.find_element(By.XPATH, '//span[@class="flavour-profile__label"')
                flavour_character_list.append(flavour_character)



            whiskey = Whiskey(
                name=name, 
                subname=subname, 
                contents_liquid_volume=contents_liquid_volume, 
                alcohol_by_volume=alcohol_by_volume, 
                facts=facts, 
                flavour_style_dict=flavour_style_dict, 
                flavour_character_list=flavour_character_list, 
                price=price, 
                description=description
                )


    # a function to scroll to the bottom of the page
    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        pass

    # basic shutdown function
    def scraper_quit(self):
        self.driver.close()
        self.driver.quit()

    # main method to run the scraper
    def run(self):
        self.load_and_accept_cookies()
        whiskey_url_list = self.get_whiskey_url_list()
        full_whiskey_url_list = self.get_full_whiskey_url_list(whiskey_url_list)

        sample_list = ['https://www.thewhiskyexchange.com/p/5258/aberfeldy-21-year-old', 'https://www.thewhiskyexchange.com/p/43962/port-charlotte-10-year-old']
        self.get_whiskey_profile(sample_list)
        self.scraper_quit()


# Boilerplate code to stop funny things happening when you import or something
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




    



