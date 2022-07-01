### Start of my code for Webscraper by Conor Quinn ###

# Import
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from dataclasses import dataclass
import json
import uuid
import os


@dataclass(repr=True)
class Spirit:

    # """dataclass for detailing attributes of a Spirit."""

    name: str = None
    brand_name = str = None
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
    

# Scraper Object with methods to control it

class Scraper:

    # Start up selenium webdriver with options. Open main page.
    def __init__(self, mainpage_url):
        # selenium webdriver setup
        options = Options()
        # options.add_argument('--headless')
        options.binary_location = '/usr/bin/google-chrome-beta'
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager(version='104.0.5112.20').install()), options=options)
        self.driver.get(mainpage_url)
        self.mainpage = mainpage_url.split('.com/')[-1]
        time.sleep(1.5)
        
        
    # accept cookies button
    def accept_cookies(self):
        try: 
            accept_cookies = self.driver.find_element(By.XPATH, '//button[@data-tid="banner-accept"]')
            accept_cookies.click()
            print('cookies accepted')
        except:
            pass
            print('cookie accept failed')
        time.sleep(1.5)


# Scraping methods #

     # Method to fetch all the urls from the main page and put in python list
    def get_url_list(self):
        product_cards = self.driver.find_elements(By.XPATH, '//*[@class="product-card"]')
               
        spirit_url_list = []
        
        for product in product_cards:
            
            spirit_url = product.get_attribute('href')
            spirit_url_list.append(spirit_url)
            
        return spirit_url_list
    
    # Method to get the profile of a spirit product from the URL provided
    def get_a_spirit_profile(self, url, spirit):

        self.driver.get(url)
        time.sleep(0.5)

        # fetch details of the spirit
        # basics
        
        spirit_name_element = self.driver.find_element(By.XPATH, '//*[@class="product-main__name"]')
        spirit.name = spirit_name_element.get_attribute('innerText').split('\n')[0]
        try:
            spirit.subname = self.driver.find_element(By.XPATH, '//*[@class="product-main__sub-name"]').text
        except NoSuchElementException:
            pass

        spirit.brand_name = spirit.name.split(' ')[0]
        
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

    # Method to do basic shutdown
    def scraper_quit(self):
        self.driver.close()
        self.driver.quit()

    # checks if urls on mainpage have already been collected and either 
    # imports the text file or creates the list by scraping
    def url_list_scrape_check(self):
        page_scrape_file = os.path.join('raw_data', self.mainpage, f'{self.mainpage}.text')
        if os.path.exists(page_scrape_file):
            url_list = FileManager.unpack_text_to_python_list(page_scrape_file)
            print(page_scrape_file)
            return url_list
        else:
            url_list = self.get_url_list
            FileManager.output_list_to_text_file(url_list, self.mainpage)
            return url_list

    # Method to check if url has already been scraped
    def url_scrape_check(self, spirit_instance): #TODO
        spirit_json = os.path.join(
            'raw_data', 
            self.mainpage, 
            spirit_instance.brandname, 
            f'{spirit_instance.product_uuid}.json'
            )
        if os.path.exists(spirit_json):
            pass
        else:
            pass


    # Method to iterate through every spirit url in the list of spirit urls provided 
    def get_x_spirit_profiles(self, list_of_spirit_urls, x=100):
        for n in range(x):
            spirit_url = list_of_spirit_urls[n]
            spirit_profile = self.get_a_spirit_profile(spirit_url, Spirit())
            FileManager.output_spirit_to_data_file(spirit_profile, self.mainpage)
        
    def activate_cloudstorage():
        pass

    def activate_analyzer():
        pass

    def run(self, x):
        self.accept_cookies()
        url_list = self.url_list_scrape_check()
        self.get_x_spirit_profiles(url_list, x)
        self.scraper_quit()

class FileManager:

    # Take a list variable and a name for the file and create/overwrite the file then add contents as a list with line breaks
    def output_list_to_text_file(url_list, mainpage):
        mainpage_underscore= mainpage.replace('/', '_')
        Path(
            f'/home/conor/Documents/Scratch/Data Collection/Project_folder/raw_data/{mainpage_underscore}'
            ).mkdir(parents=True, exist_ok=True)
        filepath = os.path.join('raw_data', mainpage_underscore, mainpage_underscore)
        with open(f'{filepath}.text', 'w') as l:
            pass

        with open(f'{filepath}.text', 'a') as l:
            for url in url_list:
                l.write(url)
                l.write('\n')

    # make file called 'input' and put in the contents of 'input' as json file
    def output_spirit_to_data_file(input, mainpage):
        mainpage_underscore= mainpage.replace('/', '_')
        Path(
            f'/home/conor/Documents/Scratch/Data Collection/Project_folder/raw_data/{mainpage_underscore}/{input.brand_name}'
            ).mkdir(parents=True, exist_ok=True)
        filepath = os.path.join('raw_data', mainpage_underscore, input.brand_name, input.product_uuid)
        with open(f'{filepath}.json', 'w') as outfile:
            pass
        inputdict = input.__dict__
        with open(f'{filepath}.json', 'a') as outfile:
            json.dump(inputdict, outfile, indent=4)
           
    # convert the contents of a line break separated text file at 'file path' to a Python List       
    def unpack_text_to_python_list(file_path):
        with open(file_path, 'r') as file:
            url_list_content = file.read()
            url_list = url_list_content.split('\n')
            
        return url_list

    # unpack a json dictionary file and return it to 
    def unpack_json_file(json_file_path):
        with open(json_file_path, 'r') as data:
            content = data.read()
            unpacked_dict = json.loads(content)
        return unpacked_dict


# Boilerplate code to stop funny things happening when you import or something
if __name__ == '__main__':
    mainpage_url = 'https://www.thewhiskyexchange.com/c/40/single-malt-scotch-whisky?psize=2500&sort=nasc'
    execute = Scraper(mainpage_url)
    execute.run(10)
    
 