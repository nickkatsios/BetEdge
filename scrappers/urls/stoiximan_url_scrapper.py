from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.common.by import By

"""
STOIXIMAN: 1.Go to the leagues url and extract all the countries elements,
grab for each country its <a> tag and get the link
2. for each league url, go to the url and extract all 
the <a> tags that contain the urls of the matches
"""

class Stoiximan_url_scrapper:
    
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
                close_popup_btn = self.driver.find_element(By.CLASS_NAME , "sb-modal__close__btn")
                close_popup_btn.click()
                self.driver.implicitly_wait(1)
                # Accept cookies
                accept_cookes_btn = self.driver.find_element(By.ID , "onetrust-reject-all-handler")
                accept_cookes_btn.click()
                self.driver.implicitly_wait(1)
        except:
            print("error closing popup")
            pass
        
    # *----- LEAGUE URL SCRAPPING -----*
    def get_all_league_urls(self):
        urls = []
        league_elements = self.driver.find_elements(By.CSS_SELECTOR, "div.tw-flex.tw-flex-col.tw-mt-m")
        for league_element in league_elements:
            a_tag = league_element.find_element(By.TAG_NAME , "a")
            url = a_tag.get_attribute("href")
            league_name = a_tag.text
            urls.append(url)
        return urls
    
    def run_league_url_extractor(self):
        self.driver.get(self.base_urls)
        self.close_popups_and_cookies()
        # extract the urls from the categories page
        league_urls = self.get_all_league_urls()
        return league_urls

    # *----- EVENT URL SCRAPPING -----*
    def run_event_url_extractor(self, league_urls):
        event_urls = []
        for url in league_urls:
            self.driver.get(url)
            self.driver.implicitly_wait(1)
            self.close_popups_and_cookies()
            events_a_tags = self.driver.find_elements(By.CSS_SELECTOR , "a.GTM-event-link")
            for event in events_a_tags:
                event_urls.append(event.get_attribute("href"))
            # filter out live events
            event_urls = list(filter(lambda x: "live" not in x, event_urls))
        return event_urls
    
    def run_url_extractor(self):
        league_urls = self.run_league_url_extractor()
        event_urls = self.run_event_url_extractor(league_urls)
        self.write_urls_to_db(event_urls)
    
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