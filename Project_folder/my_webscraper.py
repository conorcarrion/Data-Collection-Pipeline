### Start of my code for Webscraper by Conor Quinn ###

# Import

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
from dataclasses import dataclass


# dataclass for whisky
@dataclass(repr=True)
class Whisky:
    """Class for detailing attributes of a whisky."""
    name: str = None
    subname: str = None
    product_id: str = None
    contents_liquid_volume: str = '0cl'
    alcohol_by_volume: str = '0%'
    price: str = '£0'
    description: str = 'tasteless'
    facts: dict = None
    flavour_style: dict = None
    flavour_character: list = None
    

# Scraper Object with methods to control it
class Scraper():
    
    def __init__(self) -> None:
        # selenium webdriver setup
        options = Options()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)
        URL = 'https://www.thewhiskyexchange.com/brands/scotchwhisky/40/single-malt-scotch-whisky'
        self.driver.get(URL)
        time.sleep(2)
        

    # Start up selenium webdriver with options. Open main page and accept cookies. 
    def load_and_accept_cookies(self):
        
        try: 
            accept_cookies = self.driver.find_element(By.XPATH, '//button[@data-tid="banner-accept"]')
            accept_cookies.click()
            
        except:
            pass
        time.sleep(2)


# Scraping methods #

     # Method to fetch all the brands of whisky from main page into a url list
    def get_whisky_url_list(self):
        az_item_links = self.driver.find_elements(By.XPATH, '//*[@class="az-item-link"]')
        
        whisky_brand_href_list = []
        for az_item_link in az_item_links:
            whisky_href = az_item_link.get_attribute('href')
            whisky_brand_href_list.append(whisky_href)

        return whisky_brand_href_list


    # Method to fetch the urls for individual products from the urls obtained by get_whisky_url_list
    def get_full_whisky_url_list(self, url_list):
        with open('full_whisky_url_list.text', 'w') as l:
            pass
        for whisky_url in url_list:
            self.driver.get(whisky_url)
            time.sleep(0.5)
            product_cards = self.driver.find_elements(By.XPATH, '//*[@class="product-card"]')
            full_whisky_url_list = []

            for product_card in product_cards:
                whisky_href = product_card.get_attribute('href')
                               
                with open('full_whisky_url_list.text', 'a') as l:    
                    l.write(f'{whisky_href}')
                    l.write('\n')
                full_whisky_url_list.append(whisky_href)

        return full_whisky_url_list

    # Method to iterate through every whisky url in the list of whisky urls provided 
    def get_all_whisky_profiles(self, list_of_whisky_urls):
        # Iterate through every whisky url in the list_of_whisky_urls
        main_whisky_list = []
        with open('testing.text', 'w') as l:
            pass
        for whisky_url in list_of_whisky_urls:
            whisky = Whisky()
            whisky = self.get_a_whisky_profile(whisky_url, whisky)

            whiskydict = whisky.__dict__
            with open('testing.text', 'a') as t:
                t.write(str(whiskydict))
                t.write('\n')
            main_whisky_list.append(whiskydict)
               
        return main_whisky_list            
            

    # Method to get the profile of a whisky product from the URL provided
    def get_a_whisky_profile(self, url, whisky):

        self.driver.get(url)
        time.sleep(0.5)

        # fetch details of the whisky
        # basics

        whisky.name = self.driver.find_element(By.XPATH, '//*[@class="product-main__name"]').text
        try:
            whisky.subname = self.driver.find_element(By.XPATH, '//*[@class="product-main__sub-name"]').text
        except NoSuchElementException:
            pass
        
        whisky.product_id = url.split('/')[-2]
        main_data = self.driver.find_element(By.XPATH, '//*[@class="product-main__data"]').text
        main_data_tuple = main_data.split(' / ')
        whisky.contents_liquid_volume = main_data_tuple[0]
        whisky.alcohol_by_volume = main_data_tuple[1]

        whisky.price = self.driver.find_element(By.XPATH, '//*[@class="product-action__price"]').text

        whisky.description = self.driver.find_element(By.XPATH, '//*[@class="product-main__description"]').text
        # whisky.description = description_tag.find_element(By.CLASS_NAME, 'p').text

        # facts section
        facts = self.driver.find_elements(By.XPATH, '//*[@class="product-facts__item"]')
        whisky.facts= {}
        for fact in facts:
            fact_key = fact.find_element(By.XPATH, './h4[@class="product-facts__type"]').text
            print(fact_key)
            fact_value = fact.find_element(By.XPATH, './p[@class="product-facts__data"]').text
            print(fact_value)
            whisky.facts[fact_key] = fact_value

        # flavour profile section
        flavour_profile_style = self.driver.find_elements(By.XPATH, '//li[@class="flavour-profile__item flavour-profile__item--style"]')
        whisky.flavour_style = {}
        for flavour in flavour_profile_style:
            
            flavour_style_value = flavour.find_element(By.XPATH, './/span[@class="circle-text-content"]').text
            flavour_style_key = flavour.find_element(By.XPATH, './/span[@class="flavour-profile__label"]').text
            whisky.flavour_style[flavour_style_key] = flavour_style_value

        flavour_profile_character = self.driver.find_elements(By.XPATH, '//li[@class="flavour-profile__item flavour-profile__item--character"]')
        whisky.flavour_character = []
        for flavour in flavour_profile_character:
            
            flavour_character = flavour.find_element(By.XPATH, './span[@class="flavour-profile__label"]').text
            whisky.flavour_character.append(flavour_character)

        whisky.facts['test'] = 'test'
        return (whisky)

    # Method to pull individual url strings from the mass url file
    def read_whisky_list_from_text(text):
        with open('full_whisky_url_list.text', 'r') as l:
            full_whisky_list = l.read().split('\n')
        return full_whisky_list


    # Method to scroll to the bottom of the page
    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        pass

    # Method to do basic shutdown
    def scraper_quit(self):
        self.driver.close()
        self.driver.quit()

    # main execution method
    def run(self):
        self.load_and_accept_cookies()
        sample_list = ['https://www.thewhiskyexchange.com/p/19204/talisker-storm', 'https://www.thewhiskyexchange.com/p/43962/port-charlotte-10-year-old']
        self.get_all_whisky_profiles(sample_list)
        self.scraper_quit()


# Boilerplate code to stop funny things happening when you import or something
if __name__ == '__main__':
    scraperinstance = Scraper()
    scraperinstance.run()
    
    



    

    



# methods to retrieve data

    # def get_name():
    #     whisky_name = whisky_item_list.find_elements(By.XPATH, './div/header/h2[@class="top10-product__name"]')

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




    



