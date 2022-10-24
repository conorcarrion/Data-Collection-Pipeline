# Import
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import math
import os
import re
import requests
import uuid


# Scraper Object with methods to control it

class Scraper:

    '''
    This is the main Scraper class which runs the selenium webdriver,
    scrapes the urls for each product on a page, opens those pages and finally
    scrapes the profile of the spirit.
    '''

    # Start up selenium webdriver with options. Open main page.
    def __init__(self, mainpage_url, headless: bool):

        '''Initialises the loading of the page with Selenium settings.'''

        # selenium webdriver setup
        if headless:
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument('--headless')
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--start-maximized")
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        else:
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


        self.mainpage_url = mainpage_url
        self.driver.get(self.mainpage_url)
        self.driver.implicitly_wait(2)

        # Setting up the directory filepath for this scrape session ie The Whisky Exchange/Scotch Whisky/Single Malt Scotch Whisky/
        
        mainpage_breadcrumb_item_elements = self.driver.find_elements(By.XPATH, '//*[@class="breadcrumb__link"]')
        self.mainpage_filepath = ''

        for n in range(len(mainpage_breadcrumb_item_elements)):
            e = mainpage_breadcrumb_item_elements[n]
            directory = e.get_attribute('title')
            
            if e == mainpage_breadcrumb_item_elements[-1]:
                directory = e.get_attribute('innerText')

            self.mainpage_filepath = os.path.join(self.mainpage_filepath, directory)
             
    
        # preventing HTTP 403 error
        session = requests.Session()
        session.headers.update({'User-Agent': 'Custom user agent'})
        session.get('https://httpbin.org/headers')
        
        
    # accept cookies button
    def accept_cookies(self):

        '''Presses the accept cookies popup from the webpage.'''

        try: 
            accept_cookies = self.driver.find_element(By.XPATH, '//button[@data-tid="banner-accept"]')
            accept_cookies.click()
            print('cookie accept completed')
        except:
            print('cookie accept failed')
            self.scraper_quit()
            pass
            
        self.driver.implicitly_wait(2)

    def pagenumber_adjuster(self, url, x):

        '''
        Method to modify the provided url to move through to the desired page
        -
        Arguments:
            url (string): the url to be modified
            x (integer): the page to load
            
        Returns:
            new_page (string): the modified url showing page x
        '''

        new_page = re.sub('pg=[0-9]+', f'pg={x}', url)
        return new_page

    def pagesize_adjuster(self, url, x): # not currently used

        '''
        Method to modify the provided url to adjust the number of items shown on the desired page
        -
        Arguments:
            url (string): the url to be modified
            x (integer): the number of items to load per page
            
        Returns:
            new_page (string): the modified url with page size x 
        '''

        new_page = re.sub('psize=[0-9]+', f'psize={x}', url)
        return new_page

# Scraping methods #

     # Method to fetch all the urls from the main page and put in python list
    def get_url_list(self, url) -> list:

        '''
        Method to scrape all the spirit urls from the main page and further pages and append the product urls to a python list.
        -
        Returns:
            list: strings list of URLs
        '''
        print('fetching url list from driver')
        self.driver.get(url)
        self.driver.implicitly_wait(2)

        # Total number of spirits on all pages
        total_product_cards = self.driver.find_element(By.XPATH, '//*[@class="paging-count__value js-paging-count__value--total"]')
        total_product_cards_number = int(total_product_cards.get_attribute('innerText'))
        self.total_product_cards_number = total_product_cards_number

        # Number of spirits per page (dictated by 'psize=n' in the url, hardcoded by author into url)
        pagesize = self.driver.find_element(By.XPATH, '//*[@class="paging-count__value js-paging-count__value--end"]')
        pagesize_number = int(pagesize.get_attribute('innerText'))

        number_of_pages = total_product_cards_number / pagesize_number
        number_of_pages = math.ceil(number_of_pages)
        print(f'the total number of spirits at this url is {total_product_cards_number} over {number_of_pages} pages.')
        
        
        spirit_url_list = []
        for x in range(1, number_of_pages+1):

            newpage = self.pagenumber_adjuster(url, x)
            self.driver.get(newpage)
            self.driver.implicitly_wait(2)
            product_cards = self.driver.find_elements(By.XPATH, '//*[@class="product-card"]')

            for product in product_cards:
            
                spirit_url = product.get_attribute('href')
                spirit_url_list.append(spirit_url)
            
        return spirit_url_list
    
    # Method to get the profile of a spirit product from the URL provided
    def get_a_spirit_profile(self, url, spirit):

        '''
        Method to scrape the spirit profile from a given url and apply those attributes to a spirit object.
        -
        Arguments:
            url (string): the url of the spirit profile to be scraped
            spirit (instance of the spirit dataclass): spirit dataclass instance
        
        Returns:
            spirit (instance of the spirit dataclass): spirit dataclass instance with scraped information assigned
        '''

        self.driver.get(url)
        self.driver.implicitly_wait(2)

        ## Scraping the profile of the Spirit
        # names and identifiers
        
        spirit_name_element = self.driver.find_element(By.XPATH, '//*[@class="product-main__name"]')
        spirit.name = spirit_name_element.get_attribute('innerText').split('\n')[0]
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
        spirit.price = float(price[1:].replace(',', '')) # cut off the £ sign and remove comma

        spirit.description = self.driver.find_element(By.XPATH, '//*[@class="product-main__description"]').text
        
        # facts section
        facts = self.driver.find_elements(By.XPATH, '//*[@class="product-facts__item"]')
        spirit.facts= {}

        for fact in facts:

            fact_key_element = fact.find_element(By.XPATH, './*[@class="product-facts__type"]')
            fact_key = fact_key_element.get_attribute('innerText')
            fact_value_element = fact.find_element(By.XPATH, './p[@class="product-facts__data"]')
            fact_value = fact_value_element.get_attribute('innerText')
            spirit.facts[fact_key] = fact_value

        # flavour profile section
        # style is a dictionary with values of 1-5 for keys: Body Richness Smoke Sweetness
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

        try: 
            spirit_image_element = self.driver.find_element(By.XPATH, '//*[@class="product-main__image"]')
            spirit.image_url = spirit_image_element.get_attribute('src')
        except NoSuchElementException: # some profile pages have a 'slider' of multiple images. The below code tries to capture just the main one of the bottle which is saved on the site itself.
                spirit_image_elements = self.driver.find_elements(By.XPATH, '//*[@class="product-slider__image"]')
                for n in range(len(spirit_image_elements)):
                    
                    if 'https' in spirit_image_elements[n].get_attribute('src'):
                        spirit.image_url = spirit_image_elements[n].get_attribute('src')
                        break
                pass
                 
        # Mirroring the directory structure of the site's database         
        breadcrumb_item_elements = self.driver.find_elements(By.XPATH, '//*[@class="breadcrumb__link"]')
        
        spirit.filepath = ''
        for element in breadcrumb_item_elements:
            # rstrip() to remove spaces at the end of names on the site
            directory = element.get_attribute('title').rstrip().lstrip()
            if element == breadcrumb_item_elements[-1]: 
                directory = element.get_attribute('innerText').rstrip().lstrip()
            spirit.filepath = os.path.join(spirit.filepath, directory)
            if element == breadcrumb_item_elements[-2]: # best way to scrape the brand name is from this element
                spirit.brand_name = directory.rstrip().lstrip()      
        
        print(f'creating {spirit.filepath}')
       
        return (spirit)

    # Method to do basic shutdown
    def scraper_quit(self):

        '''Closes the current chrome window and shuts down the driver.'''
        print('shutting down driver')
        self.driver.close()
        self.driver.quit()

    
