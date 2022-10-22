# Data Collection Pipeline Readme

## Milestone 1 & 2
### Set up environment and Decide which website to collect data from
My major interests are magic the gathering, video games, brazilian jiu-jitsu, whisky, biology. From this selection I looked at possibilities to collect valuable data that may be of interest to an industry. Some options were:

1. Cardmarket.com - buying and selling of collectible trading cards. I was interested in the Magic: The Gathering market. This would be mostly looking at prices across card variants and condition.
2. tracker.gg - video game stats tracker. Looking at different player's skills and 
3. beltchecker.com - check BJJ players and their achieved belts
4. rcsb.org/ - Protein Data bank
5. thewhiskyexchange.com - spirits database with flavour profile

I went with whiskeyexchange as the website seemed well set up, would use a webscraper not an API and would be within my level of ability to analyze and create insights with. 

## Milestone 3
### Prototype finding the individual page for entry

Selenium is an open-source tool that automates web browsers. The selenium webdriver drives a browser natively, as a user would.
Using Selenium for Chrome, I wrote methods to build a webscraper in Python. I created a Scraper class and wrote init and an 'accept cookies' method to click the accept cookies popup banner. I set 'headless' mode in the options which means it runs without the typical browser interface.

Selenium has multiple ways to find elements on a page. One of the most reliable ways is through the XPATH. Xpaths can be absolute or relative. An absolute xpath would be:
/html/body/div[2]/div[1]/div/h4[1]/b/html[1]/body[1]/div[2]/div[1]/div[1]/h4[1]/b[1]

while a relative xpath would be : 
//div[@class='featured-box cloumnsize1']//h4[1]//b[1]

Absolute paths are precise however any changes made to the site will invalidate them, so they are not much use for a longer term project unless the website html is static. Even in relative xpaths, the tag such as 'div' or 'h1' (heading 1) could change. I stuck to using //* as a wild card and finding specific elements as, assuming the website creator used the good practice of using unique names for elements, I would not have any issues.

```
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
```
While I wanted to specifically look at Scotch single malt whisky, I wanted to ensure the webscraper was written in a way that I could use it for wine, gin, rum,  or any other spirit on thewhiskyexchange.com without changing the code. 

Looking at a single product

Next I wrote a method to collect the urls for each brand/distillery out of the page.
For example the url for the Aberfeldy distillery is:

https://www.thewhiskyexchange.com/b/40/aberfeldy-single-malt-scotch-whisky

This url has a page with all the Aberfeldy whiskies and can be clicked on to access the url for each individual product. For example the first product is:

https://www.thewhiskyexchange.com/p/5850/aberfeldy-12-year-old


I started with this page: https://www.thewhiskyexchange.com/brands/scotchwhisky/40/single-malt-scotch-whisky.

This page has an A-Z of various brands/distilleries, which when opened, have a page of the products by that brand/distillery. I felt this was a useful layout as it had the products nested within the brands, which I could implement as folders/products/data later.

```
    def get_whisky_url_list(self):
        az_item_links = self.driver.find_elements(By.XPATH, '//*[@class="az-item-link"]')

        whisky_brand_href_list = []
        for az_item_link in az_item_links:
            whisky_href = az_item_link.get_attribute('href')
            whisky_brand_href_list.append(whisky_href)

        return whisky_brand_href_list
```

## Milestone 4
### Retrieve data from details page

As part of this milestone I created a method called get_spirit_profile() which took the arguments of: an instance of a spirit dataclass and the url to be scraped for the attributes.

I then used webdriver.find_element(By.XPATH, <tag name>) to find all the elements from the spirit profile page that I wanted to collect. This included:

name (string): the full name name of the spirit product, including the brand/distillery name.            
brand_name (string): the brand/distillery name, taken as the first word from the name. 
subname (string): some spirits had a subtitle name, eg. Aberlour 12 year old, the golden dram.
product_id (string): taken from the url, believed to be the site's product id eg. from /p/40978/aberfeldy-12-year-old-the-golden-dram, 40978
product_uuid (string): each spirit product has a universally unique ID generated by the UUID python package. 
contents_liquid_volume (string): volume of the bottle
alcohol_by_volume (string): alcohol percentage of the spirit
price (float): price of the bottle(s) captured by removing the '£' from a price string and converting to float
description (string): text description of the product
facts (dict): a fact sheet of the spirit product in dictionary format as different products have different facts
flavour_style (dict): Takes the body, richness, smoke and sweetness ratings as scores out of 5 in dictionary format
flavour_character (list): A list of the flavours of the spirit, eg. nutmeg, apple, melon, honey 

I stored these attributes to the instance of the spirit dataclass passed in. This method allowed me to keep the spirit dataclass separated from the Scraper methods.

I learned many micro coding techniques. I learned: 
1. how to use Path to create a folder (mkdir) in python
2. how to adjust the chrome driver options to use a beta version due to the 103 update breaking selenium. 
3. how to use json.dump and json.loads to convert files to json and back. 
4. how to use the UUID package to create universal unique id numbers.
5. how to better structure my code using the OOP paradigm. I learned how to correctly put comments and docstring information into my code. 
6. how to use try & except for exception handling
7. how to use os.path.exists and os.path.join

## Milestone 5
### Documentation and testing

As part of this milestone I refactored and optimised any code which was unduly long or had nested loops where they were not necessary. I added docstrings to all my functions. This helped to make sure my functions were doing what they were supposed to as simply as possible and amalgamate or separate functions as appropriate. 

The next part of this milestone was creating test methods and restructuring the project. The restructuring of the project helped me moved methods to the right locations and change the run/execute information to it's own .py file. 

The test methods were put into test_webscraper.py. I struggled for a long time with testing as I wasn't sure how to make the methods with the right resolution. Making methods that seemed to be testing something important seemed difficult to me as I would end up using the method itself to create the data I wanted, then compare the output of the method to that data, which seemed very circular. But manually typing out the data I was expecting from a profile also seemed a daft approach. 

I restructured my files to be a library with AwsManager, FileManager, Scraper and Spirit python files. Then I moved some of the run methods to main.py. I also separated the test methods into tests for FileManager and tests for Scraper. 

For FileManager, I simply made a test list: ['x', 'y', 'z'] and a test Spirit instance and then used the output methods to send them to a text or json file respectively. I then used the unpack methods to read those files and return the information back to python list or dict respectively. Finally I assert whether the original list/dict matches the output/unpacked list/dict. 

For Scraper methods, I used a known profile to compare the basic information for Lagavulin 16 year old to scraped information for the get_a_spirit_profile method. For the get_url_list method I used a custom mainpage with the page size set to 10 and 33 spirit urls to be scraped. This tests the pagination and completion of the method but saves time by not scraping through 2500+ urls. 

## Milestone 6
### Scalably store the data

I set up an AWS S3 server and created boto3 methods to upload a dictionary of the data in json form and the main product image as jpg. I also set up and connected an RDS server and used psycopg2, sqlalchemy and pandas to upload my data as rows into a table. 