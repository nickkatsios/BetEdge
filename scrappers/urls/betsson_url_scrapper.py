import time
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.common.by import By

"""
-------Url Strategy------
BETSSON: Go to the leagues url and switch to the iframe that contains the sidebar,
click on the football icon and extract all the <a> tags
Since the betsson scrapping strategy for odds is to click through all events in a league and extract the odds,
We don t need to extract the urls of the events here. We just need to extract the urls of the leagues
"""

class Betsson_url_scrapper:
    
    def __init__(self, driver,  db, logger,  notifier, bookmaker_id,  base_urls) -> None:
        self.driver = driver
        self.db = db
        self.logger = logger    
        self.notifier = notifier
        self.bookmaker_id = bookmaker_id
        self.base_urls = base_urls
        
    def close_popups_and_cookies(self):
        pass
        
    # *----- BETSSON ALL URL SCRAPPING -----*
    def get_all_league_urls(self):
        self.switch_to_iframe()
        time.sleep(2)
        urls = []
        # click on sidebar icon
        sidebar_icons = self.driver.find_elements(By.CLASS_NAME, "obg-sport-catalog-component-header-label-wrapper")
        # get the icon with the text "Football"
        football_icon = [icon for icon in sidebar_icons if icon.text == "Football"][0]
        football_icon.click()
        league_container = self.driver.find_element(By.TAG_NAME, "obg-accordion-content")
        a_tags = league_container.find_elements(By.TAG_NAME , "a")
        for a_tag in a_tags:
            url = a_tag.get_attribute("href")
            league_name = a_tag.text
            urls.append(url)
        return urls
    
    def switch_to_iframe(self):
        """ Switches to the iframe that contains the odds

        This is unique to this bookmaker. The odds are loaded from AWS cloudfront and 
        contained in an iframe. 
        Selenium cant locate elements in an iframe from root dom, so we need to switch to it first
        """
        iframe = self.driver.find_elements(By.TAG_NAME , "iframe")[0]
        self.driver.switch_to.frame(iframe)
        print("Switched to iframe")
    
    def run_league_url_extractor(self):
        self.driver.get(self.base_urls)
        # extract the urls from the categories page
        urls = self.get_all_league_urls()
        return urls
    
    def run_url_extractor(self):
        league_urls = self.run_league_url_extractor()
        self.write_urls_to_db(league_urls)
    
    def write_urls_to_db(self, urls):
        """Writes the urls to the database
        Args:
            urls (list): A list of urls
            bookmaker_id (int): The id of the bookmaker
        """
        for url in urls:
            sql = "INSERT INTO Urls (bookmaker_id, url, timestamp) VALUES (%s, %s, NOW())"
            values = (self.bookmaker_id, url)
            self.db.execute_insert(sql, values)
        self.logger.info(__class__.__name__ + " : " + "Inserted: " + str(len(urls)) + " urls to db")