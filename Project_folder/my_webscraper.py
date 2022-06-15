from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from dataclasses import dataclass

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
    Style: dict = {'Body': int, 'Richness': int, 'Smoke': int, 'Sweetness': int}
    Character: list = []


# structure of data: {'whiskeys':{'example_whiskey_name':{'example_attribute': 'example_value'}}, 'number_of_whiskeys': <number of whiskeys added>}

class Scraper():
    
    driver = webdriver.Chrome(options=options)
    URL = 'https://www.thewhiskyexchange.com/d/872/top-10-whiskies'
    driver.get(URL)
    time.sleep(1)
    accept_cookies = driver.find_element(By.XPATH, '//button[@data-tid="banner-accept"]').click()

    def __init__():
        pass

    def get_name():
        whiskey_name = whiskey_item_list.find_elements(By.XPATH, './div/header/h2[@class="top10-product__name"]')

    def get_type():
        pass

    def get_link():
        pass

    def get_alcohol_by_volume():
        pass

    def get_bottle_price():
        pass

    def get_description():
        pass

    def get_style():
        pass    
    
    def get_character():
        pass


whiskey_data = {'whiskeys':{}, 'number_of_whiskeys': 0}
top10_container = driver.find_element(By.XPATH, '//ul[@class="top10-list"]')

whiskey_item_list = top10_container.find_elements(By.XPATH, './li[@class="top10-list__item"]')
num_whiskey = len(whiskey_item_list)

for i in range(num_whiskey):
    
    
    whiskey_name = whiskey.text
    whiskey_data['whiskeys'].update({whiskey_name: {}})
    whiskey_data['number_of_whiskeys'] += 1
    

whiskey_type_list = top10_container.find_elements(By.XPATH, './li/div/header/h2[@class="top10-product__name"]')



driver.quit()


    



