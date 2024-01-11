import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.common.by import By
from scrappers.configs.general_scrapper_configs import Bookmaker, Sport

"""
This class is responsible for extracting the urls of the leagues from the bookmakers
-------Strategies------
NOVIBET: Go to the leagues url and for each league click the link , extract it and go back --> slow but necessary
BETSHOP: Go to the leagues url and extract all the <a> tags for each section and filter them 
STOIXIMAN: Go to the leagues url and extract all the countries elements, grab for each country its <a> tag and get the link
BETSSON: Go to the leagues url and switch to the iframe that contains the sidebar, click on the football icon and extract all the <a> tags
"""
class League_Url_extractor:

    def __init__(self , is_headless , novibet_url ,  betshop_url , stoiximan_url, betsson_url) -> None:
        # headless config
        self.is_headless = is_headless
        options = None
        if self.is_headless:
            options = ChromeOptions()
            options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=options)
        self.driver.set_window_size(2000 , 1500)
        # url init
        self.novibet_url = novibet_url
        self.betshop_url = betshop_url
        self.stoiximan_url = stoiximan_url
        self.betsson_url = betsson_url

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

    def get_league_elements_novibet(self):
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
    
    def run_league_url_extractor_novibet(self):
        self.driver.get(self.novibet_url)
        time.sleep(2)
        self.close_popups_and_cookies(Bookmaker.NOVIBET.value)
        leagues = self.get_league_elements_novibet()
        urls = []
        wait_sec = 1
        for i in range(5):
            try:
                leagues = self.get_league_elements_novibet()
                league = leagues[i]
                league.click()
                time.sleep(wait_sec)
                url = self.driver.current_url
                urls.append(url)
                self.driver.back()
                time.sleep(wait_sec)
            except:
                print("error finding element")
                continue
        return urls


# *----- BETSHOP -----*

    # just get all <a> elements and filter them by their class proprerties to get league urls
    def get_all_league_urls_betshop(self):
        all_a_tags = self.driver.find_elements(By.TAG_NAME , "a")
        urls = []
        for a_tag in all_a_tags:
            class_attr = a_tag.get_attribute("class")
            url = a_tag.get_attribute("href")
            if(class_attr == "block align-bottom text-light-500 hover:text-light-600"):
                league_name = self.driver.find_element(locate_with(By.TAG_NAME,  "label").to_left_of(a_tag)).text
                urls.append(url)
        return urls
    
    def run_league_url_extractor_betshop(self):
        self.driver.get(self.betshop_url)
        self.close_popups_and_cookies(Bookmaker.BETSHOP.value)
        time.sleep(3)
        # extract the urls from the categories page
        urls = self.get_all_league_urls_betshop()
        return urls

# *----- STOIXIMAN -----*
    def get_all_league_urls_stoiximan(self):
        urls = []
        league_elements = self.driver.find_elements(By.CSS_SELECTOR, "div.tw-flex.tw-flex-col.tw-mt-m")
        for league_element in league_elements:
            a_tag = league_element.find_element(By.TAG_NAME , "a")
            url = a_tag.get_attribute("href")
            league_name = a_tag.text
            urls.append(url)
        return urls
    
    def run_league_url_extractor_stoiximan(self):
        self.driver.get(self.stoiximan_url)
        self.close_popups_and_cookies(Bookmaker.STOIXIMAN.value)
        # extract the urls from the categories page
        urls = self.get_all_league_urls_stoiximan()
        return urls
    
# *----- BETSSON -----*
    def get_all_league_urls_betsson(self):
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
    
    def run_league_url_extractor_betsson(self):
        self.driver.get(self.betsson_url)
        # extract the urls from the categories page
        urls = self.get_all_league_urls_betsson()
        return urls
    
# *----- MAIN -----*
    def run_league_url_extractor(self):
        """
        Runs the url extractors for each bookmaker and returns a list of lists of urls
        In the form: [[novibet_urls], [betshop_urls], [stoiximan_urls], [betsson_urls]]
        """
        league_urls = []
        # run the url extractors for each bookmaker

        league_urls_novibet = self.run_league_url_extractor_novibet()
        league_urls.append(league_urls_novibet)

        league_urls_stoiximan = self.run_league_url_extractor_stoiximan()
        league_urls.append(league_urls_stoiximan)

        league_urls_betshop = self.run_league_url_extractor_betshop()
        league_urls.append(league_urls_betshop)

        league_urls_betsson = self.run_league_url_extractor_betsson()
        league_urls.append(league_urls_betsson)

        self.end_url_extracting() 
        return league_urls
 
    def end_url_extracting(self):
        self.driver.quit()





