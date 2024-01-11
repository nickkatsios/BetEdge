import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.common.by import By
from scrappers.configs.general_scrapper_configs import Bookmaker, Sport

"""
This class is responsible for extracting the urls of the individual matches from the bookmakers
it uses the league urls extracted from the League_Url_extractor and extracts the urls of the matches in each league
-------Strategies------
NOVIBET: for each league url, go to the url and extract all the <a> tags that contain the urls of the matches
BETSHOP: Go to the leagues url and go back and forth between the leagues and extract the urls of the matches
STOIXIMAN: for each league url, go to the url and extract all the <a> tags that contain the urls of the matches
BETSSON: No need to get match urls, the scrapper will get the data from the league url
"""
class Event_Url_extractor:

    def __init__(self , is_headless, league_urls) -> None:
        # headless config
        self.is_headless = is_headless
        options = None
        if self.is_headless:
            options = ChromeOptions()
            options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=options)
        self.driver.set_window_size(2000 , 1500)
        # league_urls form: [[novibet_urls], [betshop_urls], [stoiximan_urls], [betsson_urls]]
        self.league_urls_novibet = league_urls[0]
        self.league_urls_betshop = league_urls[1]
        self.league_urls_stoiximan = league_urls[2]

# *----- REUSABLE -----*
    def close_popups_and_cookies(self , company_name):
        
        try:
            if company_name == Bookmaker.NOVIBET.value:
                # locate close button of popup ad and close
                close_popup_btn = self.driver.find_element(By.CLASS_NAME , "registerOrLogin_closeButton")
                close_popup_btn.click()
                self.driver.implicitly_wait(1)
                # Accept cookies
                accept_cookes_btn = self.driver.find_element(By.CLASS_NAME , "acceptCookies_button")
                accept_cookes_btn.click()
                self.driver.implicitly_wait(1)
            elif company_name == Bookmaker.BETSHOP.value:
                # locate close button of popup ad and close
                accept_cookies_btn = self.driver.find_element(By.CSS_SELECTOR , "button.rounded-md.text-white")
                accept_cookies_btn.click()
                self.driver.implicitly_wait(1)
            elif company_name == Bookmaker.STOIXIMAN.value:
                # locate close button of popup ad and close
                close_popup_btn = self.driver.find_element(By.CLASS_NAME , "sb-modal__close__btn")
                close_popup_btn.click()
                self.driver.implicitly_wait(1)
                # Accept cookies
                accept_cookes_btn = self.driver.find_element(By.ID , "onetrust-reject-all-handler")
                accept_cookes_btn.click()
                self.driver.implicitly_wait(1)
        except:
            print("error closing popups and cookies")
            return

# *----- NOVIBET -----*

    def run_url_extractor_novibet(self, urls):
        event_urls = []
        for url in urls:
            self.driver.get(url)
            self.driver.implicitly_wait(1)
            self.close_popups_and_cookies(Bookmaker.NOVIBET.value)
            events_a_tags = self.driver.find_elements(By.CSS_SELECTOR , "a.event_general")
            for event in events_a_tags:
                event_urls.append(event.get_attribute("href"))
            # filter out live events
            event_urls = list(filter(lambda x: "live" not in x, event_urls))
        return event_urls

# *----- BETSHOP -----*

    def get_event_elements_betshop(self):
        panel = self.driver.find_element(By.CLASS_NAME , "groupedByDate")
        event_elements = panel.find_elements(By.CSS_SELECTOR , "div.truncate")
        time.sleep(1.5)
        return event_elements
    
    def run_url_extractor_betshop(self, urls):
        for url in urls:
            # go to league main page
            self.driver.get(url)
            time.sleep(2)
            self.close_popups_and_cookies(Bookmaker.BETSHOP.value)
            # get event elements
            matches = self.get_event_elements_betshop()
            event_urls = []
            wait_sec = 1
            # for each event element, click and get url
            for i in range(len(matches)): 
                try:
                    matches = self.get_event_elements_betshop()
                    match = matches[i]
                    match.click()
                    time.sleep(wait_sec)
                    url = self.driver.current_url
                    event_urls.append(url)
                    self.driver.back()
                    time.sleep(wait_sec)
                except:
                    print("error finding element, reloading...")
                    self.driver.get(url)
                    continue
        return event_urls
    
# *----- STOIXIMAN -----*

    def run_url_extractor_stoiximan(self, urls):
        event_urls = []
        for url in urls:
            self.driver.get(url)
            self.driver.implicitly_wait(1)
            self.close_popups_and_cookies(Bookmaker.STOIXIMAN.value)
            events_a_tags = self.driver.find_elements(By.CSS_SELECTOR , "a.GTM-event-link")
            for event in events_a_tags:
                event_urls.append(event.get_attribute("href"))
            # filter out live events
            event_urls = list(filter(lambda x: "live" not in x, event_urls))
        return event_urls


# *----- MAIN -----*
    def run_url_extractor(self):
        event_urls = []

        # run the url extractors for each bookmaker
        event_urls_novibet = self.run_url_extractor_novibet(self.league_urls_novibet)
        event_urls.append(event_urls_novibet)

        event_league_urls_stoiximan = self.run_url_extractor_stoiximan(self.league_urls_stoiximan)
        event_urls.append(event_league_urls_stoiximan)

        event_league_urls_betshop = self.run_url_extractor_betshop(self.league_urls_betshop)
        event_urls.append(event_league_urls_betshop)

        self.end_url_extracting() 
        return event_urls
 
    def end_url_extracting(self):
        self.driver.quit()