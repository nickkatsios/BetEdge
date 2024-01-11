class Scrapper_interface:
    """Interface for scrappers
    
    Provides a framework for adding new scrappers to the project
    All scrappers should inherit from this class
    See: https://realpython.com/python-interface/ for more info
    To add a new scrapper, create a new file in the scrappers folder named <company_name>_scrapper.py
    The file should contain a class named <company_name>_scrapper that inherits from Scrapper_interface
    eg: bet365_scrapper.py --> class Bet365_scrapper(Informal_scrapper_interface)

    Sanitization:
    All scrappers should sanitize the data they return
    eg: remove spaces, convert to lowercase, remove special characters , convert odds to float etc
    This is to ensure that the data is consistent across all scrappers
    The sanitization should be done inside the respective methods that return a text result
    
    Testing:
    All scrappers should be tested individually to ensure that they return the correct data
    before being added to the scrapper manager

    The class should implement the methods below 
    """
    def __init__(self , driver , sport, urls, allowed_markets, db) -> None:
        pass

    def close_popups_and_cookies(self):
        """ Closes popups and accepts cookies if they exist"""

    def wait_for_page_to_load(self):
        """ Waits for the page to load by checking if an odd element is clickable"""
        pass

    def get_event_details(self):
        """Returns the details of an event from the bookmaker's website"""
        pass
    
    def get_event_league(self):
        """Returns the league of an event from the bookmaker's website"""
        pass

    def get_event_teams(self):
        """Returns the teams of an event from the bookmaker's website"""
        pass

    def get_event_datetime(self):
        """Returns the datetime of an event from the bookmaker's website"""
        pass

    def get_markets(self):
        """ Returns the available betting markets for the event

        Returns:
            markets: A list of selenium webelements containing the markets
            market_names: A list of strings containing the names of the markets
        """
        
    def get_market_odds(self, market):
        """ Returns the odds and option titiles of a specified market
        market: A market selenium webelement present in the page

        Returns:
            option_titles: A list of strings containing the titles of the options
            odds: A list of strings containing the odds of the options
        """

    def run_scrapper(self):
        """Runs the scrapper"""
        pass