from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC

from scrappers.scrapper_interface import Scrapper_interface

from standardizers.date_standardizer import Date_standardizer
from standardizers.option_title_standardizer import Option_title_standardizer
from handlers.scrapper_event_handler import Scrapper_event_handler

import time as time_module
import traceback

"""
Betsson strategy differs from the other bookmakers.
The odds for each match are loaded from AWS cloudfront and contained in an iframe.
To access the odds, we need to switch to the iframe first.
The odds are loaded only once and we iterate through matches in the league by clicking on them.
When clicked, a markets container is loaded with the odds of the match.
This is where we do the scraping.
That means that the url list is a list of **LEAGUES** urls and not **MATCHES**.
"""


class Betsson_scrapper(Scrapper_interface):
    def __init__(self , driver , sport_id, urls, allowed_markets, db, logger, notifier) -> None:
        self.driver = driver
        self.sport_id = sport_id
        self.urls = urls
        self.allowed_markets = allowed_markets
        self.db = db
        self.bookmaker_id = 4
        self.logger = logger
        self.scrapper_event_handler = Scrapper_event_handler(self.db, self.bookmaker_id, self.logger)
        self.notifier = notifier

    def close_popups_and_cookies(self):
        """ Closes all the popups and cookies warnings that appear when the page loads
        """
        try:
            # Close cookies popup
            cookies_button = self.driver.find_element(By.ID , "onetrust-accept-btn-handler")
            cookies_button.click()
        except Exception as e:
            self.logger.error("No cookies popup found")

    def get_all_event_elments(self):
        """ Returns all the event elements in the page

        Returns:
            events: A list of selenium webelements containing the events
        """
        events = self.driver.find_elements(By.TAG_NAME , "obg-event-info")
        return events

    def wait_for_page_to_load(self):
        """ Waits for the page to load
        
        Since betsson has the particular feature with the iframe, the page is
        loaded only once and we iterate through matches in the league by clicking
        on them.
        This is why time.sleep is used here.
        """
        time_module.sleep(5)

    def wait_for_markets_to_load(self):
        """ Waits for the odds in the markets container to load"""
        time_module.sleep(0.5)

    def switch_to_iframe(self):
        """ Switches to the iframe that contains the odds

        This is unique to this bookmaker. The odds are loaded from AWS cloudfront and 
        contained in an iframe. 
        Selenium cant locate elements in an iframe from root dom, so we need to switch to it first
        """
        iframe = self.driver.find_elements(By.TAG_NAME , "iframe")[0]
        self.driver.switch_to.frame(iframe)
        # print("Switched to iframe")

    def get_event_markets_container(self):
        """ Returns the container of the markets of the event

        Returns:
            markets_container: A selenium webelement containing the markets
        """
        markets_container = WebDriverWait(self.driver, timeout=2).until(
                EC.element_to_be_clickable((By.CLASS_NAME , "content-container")))
        return markets_container
            
    def get_event_details(self, event_markets_container):
        """ Returns the league, teams and time of the event
        These are the attributes needed to store an event in the db and match it
        """
        league = self.get_event_league(event_markets_container)
        team1, team2 = self.get_event_teams(event_markets_container)
        time = self.get_event_datetime(event_markets_container)
        return league, team1 , team2, time

    def get_event_league(self, event_markets_container):
        """ Returns the league name of the event
        
        Returns: 
            league: A string containing the league name of the event
            test-id="sportsbook-competition-breadcrumb"
        """
        league = event_markets_container.find_element(By.CLASS_NAME , "obg-event-info-category-label").text
        # Sanitization
        # league = league.lower()
        return league

    def get_event_teams(self, event_markets_container):
        """ Returns the 2 teams of the event"""
        teams = event_markets_container.find_elements(By.CLASS_NAME , "obg-event-info-participant-label")
        team1 = teams[0].text
        team2 = teams[1].text
        return team1, team2

    def get_event_datetime(self, event_markets_container):
        """ Returns the datetime of the event
        
        Returns:
            time: A datetime object containing the time of the event
        """
        time_str = event_markets_container.find_element(By.TAG_NAME , "time").text
        # Sanitization
        ds = Date_standardizer()
        datetime_obj = ds.standardize_date(time_str, "betsson")
        return datetime_obj

    def get_market_odds(self, market, market_name):
        """ Returns the odds and option titiles of a specified market
        market: A market selenium webelement present in the page

        Returns:
            option_titles: A list of strings containing the titles of the options
            odds: A list of strings containing the odds of the options

            test-id="event.market-selection"
            test-id="odds"
        """
        options = market.find_elements(By.CLASS_NAME , 'obg-selection-content')
        option_titles = []
        odds = []
        for option in options:
            option_title = option.find_element(By.CLASS_NAME , "obg-selection-content-label").text
            option_titles.append(option_title)
            option_odds = option.find_element(By.CLASS_NAME , 'obg-numeric-change').text
            # Sanitization
            option_odds = float(option_odds.replace("," , "."))
            odds.append(option_odds)
        # Sanitization
        # If the market is event winner, then the option titles are 1, X, 2 or 1,2
        if self.allowed_markets[market_name] == 1:
            ots = Option_title_standardizer()
            option_titles = ots.standardize_event_winner_titles(self.sport_id)
        return option_titles, odds
        
    def get_markets(self, event_markets_container):
        """ Returns the available betting markets for the event

        Returns:
            markets: A list of selenium webelements containing the markets
            market_names: A list of strings containing the names of the markets
        """
        markets = event_markets_container.find_elements(By.TAG_NAME , "obg-m-event-market-group")
        market_names = []
        for market in markets:
            name = market.find_element(By.CLASS_NAME , "obg-m-event-market-group-header-name").text
            market_names.append(name)
        return markets , market_names
    
    
    def run_scrapper(self):
        """ Runs the scrapper for the specified urls

        It closes popups and accepts cookies for the first url
        and waits for the page to load for the rest of the urls
        since the cookies appear only at the start

        The scrapper switches to the iframe that contains the odds
        and gets the event elements
        For each event, it clicks on the event
        A component with the markets of the event appears
        And scrappes the details from this componentS
        
        The scrapper first gets the event details,
        calls the event handler which
        checks to see if this event is already in the db
        If it is, it adds the bookmaker id in the "found in" column of the event 
        and retrieves the existing event id,
        It then adds the odds to the Odds table in the db
        If it is not, it creates a new event in the db and adds the odds to the Odds table
        """
        self.logger.info(f"Running Betsson scrapper in {self.driver.name.upper()} browser")
        for index, url in enumerate(self.urls):
            try:
                # Log url
                self.logger.info(f"Navigating to URL: {url}: {index} out of {len(self.urls)} ")
                # Navigate to url
                self.driver.get(url)
                # Wait for page to load
                self.wait_for_page_to_load()
                # Close popups and accept cookies on the external iframe
                self.close_popups_and_cookies()
                # Switch to iframe
                self.switch_to_iframe()
                # Get event elements
                event_elements = self.get_all_event_elments()
                # For each event
                for event in event_elements:
                    # Click on event
                    event.click()
                    # Get event markets container
                    event_markets_container = self.get_event_markets_container()
                    # Get event details
                    league, team1, team2, time = self.get_event_details(event_markets_container)
                    self.logger.info(f"Extracted Event Details - League: {league}, Teams: {team1}, {team2}, Time: {time}")
                    # Check if event exists in db and get event id
                    event_id = self.scrapper_event_handler.handle_event(self.sport_id, league, team1, team2, time)
                    # Ensure odds in the event_markets_container are loaded
                    try:
                        event_markets_container.find_element(By.CLASS_NAME , "obg-selection-content")
                    except:
                        self.wait_for_markets_to_load()
                    # Get markets and market names
                    markets , market_names = self.get_markets(event_markets_container)
                    # Get allowed markets and corresponding odds
                    for market, market_name in zip(markets , market_names):
                        # Check if market is allowed
                        if self.allowed_markets.get(market_name) is not None:
                            # Get option titles and odds
                            option_titles, market_odds = self.get_market_odds(market , market_name)
                            market_id = self.allowed_markets[market_name]
                            # Log odds and market name
                            self.logger.info(f"Processing Market: {market_name}")
                            # write odds to db
                            self.scrapper_event_handler.write_odds_to_db(self.bookmaker_id, event_id, market_id,
                                                                          option_titles, market_odds, market_name)
                    event.click()
                    time_module.sleep(1)
            except Exception as e:
                # Logs detailed traceback information
                self.logger.error(f"Error while scraping url: {url}")
                # Logs only exceptions 3 function layers deep
                self.logger.error(traceback.format_exc(limit=3))
                if self.notifier is not None:
                    self.notifier.notify_error("Error while scraping url" + str(traceback.format_exc(limit=4)))
                continue
