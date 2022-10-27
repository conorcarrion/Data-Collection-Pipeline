from lib.AwsManager import AwsManager
from lib.FileManager import FileManager
from lib.Scraper import Scraper
from lib.Spirit import Spirit

import os

mainpage_url = 'https://www.thewhiskyexchange.com/c/40/single-malt-scotch-whisky?pg=1&psize=120&sort=nasc'

s3_bucket = 'aicore-webscraper-cq'

class Main:
    
    def __init__(self, mainpage_url, save_locally=False, x=100):

        '''
        This method is the meta information of running the program. After initialisation it accepts the
        cookies, checks if the url list exists then either: 

            1. imports it from a text file and converts to a python list 
            2. scrapes the urls from the mainpage and appends them to a python list
            
        Once x (default x=100) number of profiles have been scraped, the scraper closes the chrome window and webdriver.
        save_locally will delete the files after upload to s3/rds server by default (=False)
        '''
        self.save_locally = save_locally
        webscraper = Scraper(mainpage_url, True)
        webscraper.accept_cookies()
        url_list = self.url_list_scrape_check(webscraper)
        self.get_x_spirit_profiles(webscraper, url_list, x)
        webscraper.scraper_quit()

    def url_list_scrape_check(self, webscraper):

        '''
        Checks if urls on mainpage have already been collected and either imports the text file or creates the list by scraping.
        -
        Returns:
            url_list (list): list of urls for specific products scraped from the mainpage
        '''

        print(f'checking whether to fetch urls or unpack file for {webscraper.mainpage_filepath}')
        page_scrape_file = f'{webscraper.mainpage_filepath}/url_list.text'
        if os.path.exists(page_scrape_file):
            print('url list exists, unpacking...')
            url_list = FileManager.unpack_text_to_python_list(page_scrape_file)
            AwsManager.upload_file(page_scrape_file, s3_bucket)
            if not self.save_locally:
                os.remove(page_scrape_file)
            return url_list
        else:
            print('url list not found, fetching through driver...')
            url_list = webscraper.get_url_list(mainpage_url)
            FileManager.output_list_to_text_file(url_list, webscraper.mainpage_filepath)
            AwsManager.upload_file(page_scrape_file, s3_bucket)
            if not self.save_locally:
                os.remove(page_scrape_file)
            return url_list


    # Method to iterate through every spirit url in the list of spirit urls provided 
    def get_x_spirit_profiles(self, webscraper, spirit_url_list, x=100):

        '''
        Method to begin iterating through a list of urls and scraping the profile from each page.
        -
        Arguments:
                spirit_url_list (list): A list of url strings to be scraped
                x (integer): defaults to 100, the number of profiles to scrape before stopping.
                            This exists purely to limit the running of the program after demonstrating it works.

        Outputs:
                The scraped information is saved in dictionary format as a json file called data.json.
                This file is saved to a folder named after the unique id (spirit.product_uuid), 
                itself in a folder named after the brand/distillery name (spirit.brand_name).        
        '''
        rds_server = AwsManager.rds_server()
        for n in range(x):
            spirit_url = spirit_url_list[n]
            spirit_product_id = spirit_url.split('/')[-2]
            exists = AwsManager.rds_exists_check(spirit_product_id, rds_server)
            if exists:
                print(f'Skipping {spirit_product_id}')
            if not exists:
                spirit_profile = webscraper.get_a_spirit_profile(spirit_url, Spirit())
                AwsManager.insert_row(spirit_profile, rds_server)
                json_path, image_path = FileManager.output_spirit_to_data_file(spirit_profile)
                AwsManager.upload_file(json_path, s3_bucket, json_path)
                AwsManager.upload_file(image_path, s3_bucket, image_path)
                if not self.save_locally:
                    os.remove(json_path)
                    os.remove(image_path)


if __name__ == '__main__':
    program = Main(mainpage_url, False)

