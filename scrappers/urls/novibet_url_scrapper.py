import time
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.common.by import By

"""
-------Url Strategy------
NOVIBET: 1. Go to the leagues url and for each league click the link , extract it and go back --> slow but necessary
2. For each league url, go to the url and extract all the <a> tags that contain the urls of the matches.
"""

class Novibet_url_scrapper:
    
    def __init__(self, driver,  db, logger, notifier, bookmaker_id,  base_urls) -> None:
        self.driver = driver
        self.db = db
        self.logger = logger
        self.notifier = notifier
        self.bookmaker_id = bookmaker_id
        self.base_urls = base_urls

     # *----- NOVIBET LEAGUE URL SCRAPPING -----*
     
    def close_popups_and_cookies(self):
        try:
            # locate close button of popup ad and close
            close_popup_btn = self.driver.find_element(By.CLASS_NAME , "registerOrLogin_closeButton")
            close_popup_btn.click()
            self.driver.implicitly_wait(1)
            # Accept cookies
            accept_cookes_btn = self.driver.find_element(By.CLASS_NAME , "acceptCookies_button")
            accept_cookes_btn.click()
            self.driver.implicitly_wait(1)
        except:
            self.logger.info(__class__.__name__ + " : " + "Error closing popup")
            pass

    def get_league_elements(self):
            cards = self.driver.find_elements(By.TAG_NAME , "cm-card")
            time.sleep(1.5)
            return cards

    def check_element_exists(self):
        try:
            self.driver.find_element(By.CLASS_NAME , "")
        except:
            return False
        return True
    
    def get_league_name(self , league_element):
        league_info = league_element.find_element(By.CLASS_NAME , "couponContent_cardTitle").text
        league_name, country_name = league_info.split("\n")
        return league_name
    
    def run_league_url_extractor(self):
        self.driver.get(self.base_urls)
        time.sleep(2)
        self.close_popups_and_cookies()
        leagues = self.get_league_elements()
        league_urls = []
        wait_sec = 1
        for i in range(10):
            try:
                leagues = self.get_league_elements()
                league = leagues[i]
                league.click()
                time.sleep(wait_sec)
                url = self.driver.current_url
                league_urls.append(url)
                self.driver.back()
                time.sleep(wait_sec)
            except:
                self.logger.info(__class__.__name__ + " : " + "Error getting league urls")
                continue
        return league_urls
    
    # *----- NOVIBET EVENT URL SCRAPPING -----*
    
    def run_event_url_extractor(self, league_urls):
        event_urls = []
        for url in league_urls:
            self.driver.get(url)
            self.driver.implicitly_wait(1)
            self.close_popups_and_cookies()
            events_a_tags = self.driver.find_elements(By.CSS_SELECTOR , "a.event_general")
            for event in events_a_tags:
                event_urls.append(event.get_attribute("href"))
            # filter out live events
            event_urls = list(filter(lambda x: "live" not in x, event_urls))
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