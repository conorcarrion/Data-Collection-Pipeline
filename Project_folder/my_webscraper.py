from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument('--headless')
# add options=options to webdriver.Chrome to run in headless mode
# use to quit driver in headless mode: driver.quit()

driver = webdriver.Chrome(options=options)
URL = 'https://www.thewhiskyexchange.com/d/872/top-10-whiskies'
driver.get(URL)
time.sleep(1)

accept_cookies = driver.find_element(By.XPATH, '//button[@data-tid="banner-accept"]').click()

# structure of data: {'whiskeys':{'example_whiskey_name':{'example_attribute': 'example_value'}}, 'number_of_whiskeys': <number of whiskeys added>}

whiskey_data = {'whiskeys':{}, 'number_of_whiskeys': 0}
top10_list = driver.find_element(By.XPATH, '//ul[@class="top10-list"]')
whiskey_list = top10_list.find_elements(By.XPATH, './li/div/header/h2[@class="top10-product__name"]')


for whiskey in whiskey_list:
    whiskey_name = whiskey.text
    whiskey_data['whiskeys'].update({whiskey_name: {}})
    whiskey_data['number_of_whiskeys'] += 1

print(whiskey_data)
driver.quit()

