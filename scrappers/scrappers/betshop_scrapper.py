from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC

from scrappers.scrapper_interface import Scrapper_interface

from standardizers.date_standardizer import Date_standardizer
from standardizers.option_title_standardizer import Option_title_standardizer
from handlers.scrapper_event_handler import Scrapper_event_handler

import traceback    

class Betshop_scrapper(Scrapper_interface):
    def __init__(self , driver , sport_id, urls, allowed_markets, db, logger, notifier) -> None:
        self.driver = driver
        self.sport_id = sport_id
        self.urls = urls
        self.allowed_markets = allowed_markets
        self.db = db
        self.bookmaker_id = 3
        self.logger = logger
        self.scrapper_event_handler = Scrapper_event_handler(self.db, self.bookmaker_id, self.logger)
        self.notifier = notifier

    def change_language(self):
        """ Changes the language of the page to english

        This is needed because the page is in greek by default
        This method is unique to this scrapper
        """
        self.driver.find_element(By.CSS_SELECTOR , "span.uppercase.mt-1.inline-block").click()
        english = self.driver.find_element(By.CSS_SELECTOR , "div.block.cursor-pointer.truncate.px-4.py-2").click()

    def close_popups_and_cookies(self):
        try:
            # locate close button of popup ad and close
            accept_cookies_btn = self.driver.find_element(By.CSS_SELECTOR , "button.rounded-md.text-white")
            accept_cookies_btn.click()
            self.driver.implicitly_wait(1)
        except Exception as e:
            self.logger.error("No cookies popup found")

    def wait_for_page_to_load(self):
        """ Waits for the page to load by checking if an odd element is clickable

        If the first odd element is clickable, then the rest will be as well,
        so we can assume that the page has loaded
        """
        WebDriverWait(self.driver, timeout=3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR , "button.flex.w-full.items-center")))
            
    def get_event_details(self):
        """ Returns the league, teams and time of the event
        These are the attributes needed to store an event in the db and match it
        """
        league = self.get_event_league()
        team1, team2 = self.get_event_teams()
        time = self.get_event_datetime()
        return league, team1 , team2, time

    def get_event_league(self):
        """ Returns the league name of the event
        
        Returns: 
            league: A string containing the league name of the event
        """
        league = self.driver.find_element(By.XPATH, "//div[@leagueslug]")
        league = league.get_attribute("leagueslug")
        # Sanitization
        league = league.replace("-", " ")
        return league

    def get_event_teams(self):
        """ Returns the 2 teams of the event"""
        teams = self.driver.find_element(By.CSS_SELECTOR, 'h3.text-xl').text
        teams = teams.split(" - ")
        team1 = teams[0]
        team2 = teams[1]
        return team1, team2
        
    def get_event_datetime(self):
        """ Returns the datetime of the event
        
        Returns:
            time: A datetime object containing the time of the event

        """
        time_str = self.driver.find_element(By.CSS_SELECTOR , "span.mr-1").text
        # Sanitization
        ds = Date_standardizer()
        datetime_obj = ds.standardize_date(time_str, "betshop")
        return datetime_obj

    def get_market_odds(self, market, market_name):
        """ Returns the odds and option titiles of a specified market
        market: A market selenium webelement present in the page

        Returns:
            option_titles: A list of strings containing the titles of the options
            odds: A list of strings containing the odds of the options

        """
        options = market.find_elements(By.CSS_SELECTOR , "button.flex.w-full.items-center")
        option_titles = []
        odds = []
        for option in options:
            spans = option.find_elements(By.TAG_NAME , "span")
            option_title = spans[0].text
            option_titles.append(option_title)
            option_odds = spans[1].text
            # Sanitization
            option_odds = float(option_odds.replace("," , "."))
            odds.append(option_odds)
        # Sanitization
        # if market is event winner, standardize the option titles to 1x2 or 12
        if self.allowed_markets[market_name] == 1:
            ots = Option_title_standardizer()
            option_titles = ots.standardize_event_winner_titles(self.sport_id)
        return option_titles, odds
        
    def get_markets(self):
        """ Returns the available betting markets for the event

        Returns:
            markets: A list of selenium webelements containing the markets
            market_names: A list of strings containing the names of the markets
        """
        markets = self.driver.find_elements(By.CSS_SELECTOR , "div.mb-1.select-none.rounded-sm")
        market_names = []
        for market in markets:
            name = market.find_element(By.CSS_SELECTOR , "div.flex-auto.cursor-pointer").text
            market_names.append(name)
        return markets , market_names
    
    def run_scrapper(self):
        """ Runs the scrapper for the specified urls

        It closes popups and accepts cookies for the first url
        and waits for the page to load for the rest of the urls
        since the cookies appear only at the start

        The scrapper first gets the event details,
        calls the event handler which
        checks to see if this event is already in the db
        If it is, it adds the bookmaker id in the "found in" column of the event 
        and retrieves the existing event id,
        It then adds the odds to the Odds table in the db
        If it is not, it creates a new event in the db and adds the odds to the Odds table
        """
        self.logger.info(f"Running Betshop Scrapper in {self.driver.name.upper()} browser")
        for index,url in enumerate(self.urls):
            try:
                # Log url
                self.logger.info(f"Navigating to URL: {url}: {index} out of {len(self.urls)} ")
                # Navigate to url
                self.driver.get(url)
                # On first url, change language and wait for page to load
                if index == 0:
                    self.close_popups_and_cookies()
                    self.change_language() 
                    self.wait_for_page_to_load()
                else:
                    # On the rest of the urls, just wait for page to load
                    # the language is cached
                    self.wait_for_page_to_load()    
                # Get event details
                league, team1, team2, time = self.get_event_details()
                # Check if event exists in db and get event id
                event_id = self.scrapper_event_handler.handle_event(self.sport_id, league, team1, team2, time)
                self.logger.info(f"Extracted Event Details - League: {league}, Teams: {team1}, {team2}, Time: {time}")
                # Get market elements
                markets , market_names = self.get_markets()
                # Get allowed markets and corresponding odds
                for market, market_name in zip(markets , market_names):
                    # Check if market is allowed
                    if self.allowed_markets.get(market_name) is not None:
                        # Get option titles and odds
                        option_titles, market_odds = self.get_market_odds(market, market_name)
                        market_id = self.allowed_markets[market_name]
                        self.logger.info(f"Processing Market: {market_name}")
                        # write odds to db
                        self.scrapper_event_handler.write_odds_to_db(self.bookmaker_id, event_id, market_id,
                                                                      option_titles, market_odds, market_name)
            except Exception as e:
                # Logs detailed traceback information
                self.logger.error(f"Error while scraping url: {url}")
                # Logs only exceptions 3 function layers deep
                self.logger.error(traceback.format_exc(limit=3))
                if self.notifier is not None:
                    self.notifier.notify_error("Error while scraping url" + str(traceback.format_exc(limit=4)))
                continue
