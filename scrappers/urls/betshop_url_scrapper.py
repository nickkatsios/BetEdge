import time
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.common.by import By
import traceback

"""
-------Url Strategy------
BETSHOP: 1.Go to the leagues url and extract all the <a> tags for each section and filter them 
2.Go to the leagues url and go back and forth between the leagues and extract the urls of the matches
"""

class Betshop_url_scrapper:
    
    def __init__(self, driver,  db, logger, notifier, bookmaker_id,  base_urls) -> None:
        self.driver = driver
        self.db = db
        self.logger = logger
        self.notifier = notifier
        self.bookmaker_id = bookmaker_id
        self.base_urls = base_urls
        
    def close_popups_and_cookies(self):
        try:
            # locate close button of popup ad and close
            accept_cookies_btn = self.driver.find_element(By.CSS_SELECTOR , "button.rounded-md.text-white")
            accept_cookies_btn.click()
            self.driver.implicitly_wait(1)
        except:
            self.logger.info(__class__.__name__ + " : " + "Error closing popup")
            pass
        
    # *----- BETSHOP LEAGUE URL SCRAPPING -----*

    # just get all <a> elements and filter them by their class proprerties to get league urls
    def get_all_league_urls(self):
        all_a_tags = self.driver.find_elements(By.TAG_NAME , "a")
        urls = []
        for a_tag in all_a_tags:
            url = a_tag.get_attribute("href")
            if url is not None and url.startswith("https://www.betshop.gr/sports/game/stoixima-podosfairo/"):
                urls.append(url)
        return urls
    
    def run_league_url_extractor(self):
        self.driver.get(self.base_urls)
        self.close_popups_and_cookies()
        time.sleep(3)
        # extract the urls from the categories page
        urls = self.get_all_league_urls()
        return urls
    
    # *----- BETSHOP EVENT URL SCRAPPING -----*

    def get_event_elements(self):
        panel = self.driver.find_elements(By.CLASS_NAME , "min-h-screen")[1]
        event_elements = panel.find_elements(By.CSS_SELECTOR , "div.truncate")
        time.sleep(1.5)
        return event_elements
    
    def run_event_url_extractor(self, urls):
        for url in urls:
            # go to league main page
            self.driver.get(url)
            time.sleep(2)
            self.close_popups_and_cookies()
            # get event elements
            matches = self.get_event_elements()
            event_urls = []
            wait_sec = 1
            # for each event element, click and get url
            for i in range(len(matches)): 
                try:
                    matches = self.get_event_elements()
                    match = matches[i]
                    match.click()
                    time.sleep(wait_sec)
                    url = self.driver.current_url
                    event_urls.append(url)
                    self.driver.back()
                    time.sleep(wait_sec)
                except:
                    self.logger.info(__class__.__name__ + " : " + "Error getting event urls")
                    self.logger.info(__class__.__name__ + " : " + traceback.format_exc())
                    continue
            # save to db for each league
            self.write_urls_to_db(event_urls)
            
            
    def run_url_extractor(self):
        league_urls = self.run_league_url_extractor()
        self.run_event_url_extractor(league_urls)
    
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
    