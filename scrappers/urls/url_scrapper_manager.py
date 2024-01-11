from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver import FirefoxOptions
import concurrent.futures
from db.db import Database
import logging
import os

from notifiers.email_notifier import Email_notifier

# Scrappers
from urls.novibet_url_scrapper import Novibet_url_scrapper
from urls.stoiximan_url_scrapper import Stoiximan_url_scrapper
from urls.betshop_url_scrapper import Betshop_url_scrapper
from urls.betsson_url_scrapper import Betsson_url_scrapper

# configs
from urls.url_scrapper_configs import base_urls
from scrappers.configs.general_scrapper_configs import Bookmaker, Sport, bookmaker_ids

class Url_scrapper_manager:
    """ A Scrapper_manager is a component that manages the url scrappers and their drivers.

    As more scrappers get added , the scrapper manager will be the central component for running and retrieving results
    Strategies can be used to run the scrappers in parallel (multiproccessing) or in sequence

    Attributes:
        is_headless: A boolean value that determines if the driver will be headless or not
        is_parallel: A boolean value that determines if the scrappers will be run in parallel or not
        is_logging: A boolean value that determines if the scrappers will log their actions
        browser: A string value that determines which browser will be used for scrapping
        notify: A boolean value that determines if the notifier will be used
    """

    def __init__(self , is_headless , is_parallel, is_logging, browser , notify) -> None:
        self.is_headless = is_headless
        self.is_parallel = is_parallel
        self.is_logging = is_logging
        self.browser = browser
        self.notify = notify

    def create_logger(self , scrapper_name):
        """Creates a logger for a scrapper"""
        scrapper_logger = logging.getLogger(__name__ + '.' + scrapper_name)
        # Creating a file handler for scraper-specific logging
        scrapper_file_handler = logging.FileHandler(os.path.join('logs', f'{scrapper_name}.log'))
        # Setting the desired logging level for scraper
        logging_level = logging.DEBUG if self.is_logging else logging.CRITICAL
        scrapper_logger.setLevel(logging_level)
        scrapper_file_handler.setLevel(logging_level)
        # Creating a formatter for scraper-specific logging
        scraper_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        scrapper_file_handler.setFormatter(scraper_formatter)
        # Adding the file handler to the scraper logger
        scrapper_logger.addHandler(scrapper_file_handler)
        return scrapper_logger
    
    def create_notifier(self):
        """Creates a notifier for a scrapper"""
        notifier = Email_notifier("whale.mail.alert@gmail.com" , "nickkatsios0@gmail.com")
        return notifier

    def create_driver(self):
        """Dynamicly creates a driver as needed by the scrappers

        Used for multiprocessing and parallel scrapping
        """
        root_logger = logging.getLogger()
        if self.browser == "chrome":
            return self.create_chrome_driver(root_logger)
        elif self.browser == "firefox":
            return self.create_firefox_driver(root_logger)
    
    def create_chrome_driver(self, root_logger):
        """
        Creates a chrome driver and sets the specified options
        """
        options = None
        if self.is_headless:
            options = ChromeOptions()
            options.add_argument("--headless")
            root_logger.info(f"Running {self.browser.upper()} in headless mode")
        driver = webdriver.Chrome(options=options)
        driver.set_window_size(2000, 1500)
        return driver
    
    def create_firefox_driver(self, root_logger):
        """
        Creates a firefox driver and sets the specified options
        Note: on linux, you may need to install geckodriver and add it as driver executable
        better to install firefox with sudo apt install firefox 
        """
        options = None
        if self.is_headless:
            options = FirefoxOptions()
            options.add_argument("--headless")
            root_logger.info(f"Running {self.browser.upper()} in headless mode")
        driver = webdriver.Firefox(options=options)
        driver.set_window_size(2000, 1500)
        return driver

    def run_scrapper(self , scrapper):
        """Runs a scrapper and returns the results as a list of Bet objects

        A driver is created for each scrapper dynamically since it can't be pickled
        
        Args:
            scrapper: A scrapper object that will be run
        """
        scrapper.driver = self.create_driver()
        result = scrapper.run_url_extractor()
        return result

    def run_url_scrappers(self):
        """Runs all the scrappers and manages their drivers and urls

        Scrappers are run in parallel using the concurrent.futures module
        Strategies can be used to run the scrappers in sequence or in parallel
        Notes:
            The handler is initialized inside the init method of each scrapper , not when it is being run
            Thus, we will need to create the logger that is passed into the handler from the scrapper at the scrapper creation
        """

        scrappers = []

        # Init global db object
        db = Database()

        # Init url loader
        notifier = self.create_notifier() if self.notify else None

        root_logger = logging.getLogger()

        # Init scrappers ordered by bookmaker id
        
        novibet_url_scrapper = Novibet_url_scrapper(None, db, self.create_logger(Bookmaker.NOVIBET.value), notifier, bookmaker_ids['novibet'], base_urls[Bookmaker.NOVIBET.value][Sport.FOOTBALL.value])
        root_logger.info(f"--------Novibet Url scrapper created--------")
        scrappers.append(novibet_url_scrapper)
        
        stoiximan_url_scrapper = Stoiximan_url_scrapper(None, db, self.create_logger(Bookmaker.STOIXIMAN.value), notifier, bookmaker_ids['stoiximan'], base_urls[Bookmaker.STOIXIMAN.value][Sport.FOOTBALL.value])
        root_logger.info(f"--------Stoiximan Url scrapper created--------")
        scrappers.append(stoiximan_url_scrapper)
        
        betshop_url_scrapper = Betshop_url_scrapper(None, db, self.create_logger(Bookmaker.BETSHOP.value), notifier, bookmaker_ids['betshop'], base_urls[Bookmaker.BETSHOP.value][Sport.FOOTBALL.value])
        root_logger.info(f"--------Betshop Url scrapper created--------")
        scrappers.append(betshop_url_scrapper)
        
        betsson_url_scrapper = Betsson_url_scrapper(None, db, self.create_logger(Bookmaker.BETSSON.value), notifier, bookmaker_ids['betsson'], base_urls[Bookmaker.BETSSON.value][Sport.FOOTBALL.value])
        root_logger.info(f"--------Betsson Url scrapper created--------")
        scrappers.append(betsson_url_scrapper)
        
        # Parallel scrapping
        if self.is_parallel:
            # Context manager runs every scrapper , creating a driver dynamically for each one.
            with concurrent.futures.ThreadPoolExecutor() as executor:
                root_logger.info(f"Running {len(scrappers)} scrappers in parallel...")
                # Submit scraping tasks for each scrapper
                futures = [executor.submit(self.run_scrapper, scrapper) for scrapper in scrappers]
                # Wait for all tasks to complete
                concurrent.futures.wait(futures)

        # Sequential scrapping
        else:
            root_logger.info(f"Running {len(scrappers)} url scrappers in sequence...")
            # Create a global driver for all scrappers
            global_driver = self.create_driver()
            # Iterate the scrappers and run them
            for scrapper in scrappers:
                # Set the global driver for each scrapper
                scrapper.driver = global_driver
                # Run the scrapper directly
                scrapper.run_url_extractor()

    def end_scrapping(self):
        """Closes the driver and window for each scrapper
        """
        self.driver.quit()