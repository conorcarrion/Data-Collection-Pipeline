### Start of my code for Webscraper by Conor Quinn ###

# Import
from pathlib import Path
from unicodedata import decimal
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
from dataclasses import dataclass
import json
from re import sub
import uuid


@dataclass(repr=True)
class Spirit:

    # """dataclass for detailing attributes of a Spirit."""

    name: str = None
    subname: str = None
    product_id: str = None
    product_uuid: str = None
    contents_liquid_volume: str = '0cl'
    alcohol_by_volume: str = '0%'
    price: float = 0
    description: str = 'tasteless'
    facts: dict = None
    flavour_style: dict = None
    flavour_character: list = None
    

class DataCollector:

    def __init__(self) -> None:
        pass

    def activate_scraper():
        pass

    def activate_filemanager():
        pass

    def activate_cloudstorage():
        pass

    def activate_analyzer():
        pass


# Scraper Object with methods to control it

class Scraper:
    
    def __init__(self, mainpage_url):
        # selenium webdriver setup
        options = Options()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(mainpage_url)
        time.sleep(1.5)
        

    # Start up selenium webdriver with options. Open main page and accept cookies. 
    def load_and_accept_cookies(self):
        try: 
            accept_cookies = self.driver.find_element(By.XPATH, '//button[@data-tid="banner-accept"]')
            accept_cookies.click()
        except:
            pass
        time.sleep(1.5)


# Scraping methods #

     # Method to fetch all the brandnames and their urls from the provided main page
    def get_brand_url_list(self):
        az_item_links = self.driver.find_elements(By.XPATH, '//*[@class="az-item-link"]')
               
        spirit_brand_url_list = []
        spirit_brand_name_list = []
        FileManager.make_output_text_file(spirit_brand_name_list)
        FileManager.make_output_text_file(spirit_brand_url_list)

        for az_item_link in az_item_links:
            
            spirit_brandname = az_item_link.find_element(By.XPATH, './span[@class="az-item-name"]').text
            spirit_brand_name_list.append(spirit_brandname)

            spirit_url = az_item_link.get_attribute('href')
            spirit_brand_url_list.append(spirit_url)
            FileManager.append_to_text_file(spirit_brandname, spirit_brand_name_list)
            FileManager.append_to_text_file(spirit_url, spirit_brand_url_list)

        return spirit_brandname, spirit_brand_url_list

    

    # Method to fetch the urls for individual products from the urls obtained by get_spirit_url_list
    def get_url_list_of_lists(self, spirit_brand_url_list):
        
        url_list_of_lists = [] # list of lists, with a list of each whisky product in a list of each whiskey brand
        FileManager.make_output_text_file(url_list_of_lists)

        for spirit_url in spirit_brand_url_list:
            self.driver.get(spirit_url)
            time.sleep(0.5)
            product_cards = self.driver.find_elements(By.XPATH, '//*[@class="product-card"]')

            spirit_product_list = []
            for product_card in product_cards:
                spirit_url = product_card.get_attribute('href')
                spirit_product_list.append(spirit_url)

            url_list_of_lists.append(spirit_product_list)
            FileManager.append_to_text_file(spirit_product_list, url_list_of_lists)

        return url_list_of_lists

    
    # Method to get the profile of a spirit product from the URL provided
    def get_a_spirit_profile(self, url, spirit):

        self.driver.get(url)
        time.sleep(0.5)

        # fetch details of the spirit
        # basics

        spirit.name = self.driver.find_element(By.XPATH, '//*[@class="product-main__name"]').text
        try:
            spirit.subname = self.driver.find_element(By.XPATH, '//*[@class="product-main__sub-name"]').text
        except NoSuchElementException:
            pass
        
        spirit.product_id = url.split('/')[-2]
        spirit.product_uuid = str(uuid.uuid4())

        # The site gives volume and alcohol percentage in same entry so has to be split and formatted.
        main_data = self.driver.find_element(By.XPATH, '//*[@class="product-main__data"]').text
        main_data_tuple = main_data.split(' / ') # site entry example: '70cl / 40%' 
        spirit.contents_liquid_volume = main_data_tuple[0]
        spirit.alcohol_by_volume = main_data_tuple[1]

        price = self.driver.find_element(By.XPATH, '//*[@class="product-action__price"]').text
        spirit.price = float(price[1:]) # cut off the £ sign

        spirit.description = self.driver.find_element(By.XPATH, '//*[@class="product-main__description"]').text
        
        # facts section
        facts = self.driver.find_elements(By.XPATH, '//*[@class="product-facts__item"]')
        spirit.facts= {}
        for fact in facts:
            fact_key_element = fact.find_element(By.XPATH, './h4[@class="product-facts__type"]')
            fact_key = fact_key_element.get_attribute('innerText')
            fact_value_element = fact.find_element(By.XPATH, './p[@class="product-facts__data"]')
            fact_value = fact_value_element.get_attribute('innerText')
            spirit.facts[fact_key] = fact_value

        # flavour profile section
        # style is a dictionary with numbers 1-5 for keys: Body Richness Smoke Sweetness
        flavour_profile_style = self.driver.find_elements(By.XPATH, '//li[@class="flavour-profile__item flavour-profile__item--style"]')
        spirit.flavour_style = {}
        for flavour in flavour_profile_style:
            
            flavour_style_value = flavour.find_element(By.XPATH, './/span[@class="circle-text-content"]').text
            flavour_style_key = flavour.find_element(By.XPATH, './/span[@class="flavour-profile__label"]').text
            spirit.flavour_style[flavour_style_key] = flavour_style_value

        # character is a list with various flavour elements such as: salt, vanilla, toffee etc
        flavour_profile_character = self.driver.find_elements(By.XPATH, '//li[@class="flavour-profile__item flavour-profile__item--character"]')
        spirit.flavour_character = []
        for flavour in flavour_profile_character:
            
            flavour_character = flavour.find_element(By.XPATH, './span[@class="flavour-profile__label"]').text
            spirit.flavour_character.append(flavour_character)

        return (spirit)

  
 # Method to iterate through every spirit url in the list of spirit urls provided 
    def get_all_spirit_profiles(self, list_of_spirit_urls): # TODO
        
        
        FileManager.make_output_text_file('data.json')

        for spirit_url in list_of_spirit_urls:
            spirit = Spirit()
            spirit = self.get_a_spirit_profile(spirit_url, spirit)

            spiritdict = spirit.__dict__
            with open('test.json', 'a') as outfile:
                json.dump(spiritdict, outfile, indent=4)
                
            main_spirit_list.append(spiritdict)

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
        # self.get_brand_url_list() - 
        sample_list = ['https://www.thespiritexchange.com/p/19204/talisker-storm', 'https://www.thespiritexchange.com/p/43962/port-charlotte-10-year-old']
        self.get_all_spirit_profiles(sample_list)
        self.scraper_quit()


class FileManager:

    def make_output_text_file(outfile_name):
        with open(f'{outfile_name}.text', 'w') as l:
            pass

    def append_to_text_file(input, outfile_name):
        with open(f'{outfile_name}.text', 'a') as l:    
            l.write(f'{input}')
            l.write('\n')

    # Method to create the subfolders based on brand/distillery name
    def create_brandname_folder(self, brand):
        Path(
            f'/home/conor/Documents/Scratch/Data Collection/Project_folder/raw_data/{brand}'
            ).mkdir(parents=True, exist_ok=True)

      # Method to pull individual url strings from the mass url file
    def read_spirit_list_from_text(text):
        with open(text, 'r') as l:
            full_spirit_list = l.read().split('\n')
        return full_spirit_list


# Boilerplate code to stop funny things happening when you import or something
if __name__ == '__main__':
    mainpage_url = 'https://www.thespiritexchange.com/brands/scotchspirit/40/single-malt-scotch-spirit'
    scraperinstance = Scraper(mainpage_url)
    scraperinstance.run()
    
 