from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver import FirefoxOptions
import concurrent.futures
from db.db import Database
import logging
import os
from urls.scrapper_url_loader import Scrapper_url_loader

from notifiers.email_notifier import Email_notifier

# Scrappers
from scrappers.novibet_scrapper import Novibet_scrapper
from scrappers.stoixoiman_scrapper import Stoiximan_scrapper
from scrappers.betshop_scrapper import Betshop_scrapper
from scrappers.betsson_scrapper import Betsson_scrapper

# Configs
from scrappers.configs.general_scrapper_configs import *
from scrappers.configs.novibet_config import novibet_allowed_markets
from scrappers.configs.stoiximan_config import stoiximan_allowed_markets
from scrappers.configs.betshop_config import betshop_allowed_markets
from scrappers.configs.betsson_config import betsson_allowed_markets


class Scrapper_manager:
    """ A Scrapper_manager is a component that manages the scrappers and their drivers.

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
        result = scrapper.run_scrapper()
        return result

    def run_scrappers(self):
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
        url_loader = Scrapper_url_loader(db)

        notifier = self.create_notifier() if self.notify else None

        root_logger = logging.getLogger()

        # Init scrappers ordered by bookmaker id
        
        novibet_urls = url_loader.load_urls(bookmaker_ids["novibet"])
        novibet_scrapper = Novibet_scrapper(None, Sport.FOOTBALL.value, novibet_urls, novibet_allowed_markets , db, self.create_logger(Bookmaker.NOVIBET.value) , notifier)
        root_logger.info(f"Novibet scrapper created with {len(novibet_urls)} urls")
        scrappers.append(novibet_scrapper)

        betshop_urls = url_loader.load_urls(bookmaker_ids["betshop"])
        betshop_scrapper = Betshop_scrapper(None, Sport.FOOTBALL.value , betshop_urls, betshop_allowed_markets , db, self.create_logger(Bookmaker.BETSHOP.value), notifier )
        root_logger.info(f"Betshop scrapper created with {len(betshop_urls)} urls")
        scrappers.append(betshop_scrapper)

        stoiximan_urls = url_loader.load_urls(bookmaker_ids["stoiximan"])
        stoiximan_scrapper = Stoiximan_scrapper(None, Sport.FOOTBALL.value, stoiximan_urls, stoiximan_allowed_markets , db, self.create_logger(Bookmaker.STOIXIMAN.value),  notifier)
        root_logger.info(f"Stoiximan scrapper created with {len(stoiximan_urls)} urls")
        scrappers.append(stoiximan_scrapper)
        
        # betsson_urls = url_loader.load_urls(bookmaker_ids["betsson"])
        # betsson_scrapper = Betsson_scrapper(None, Sport.FOOTBALL.value, betsson_urls, betsson_allowed_markets , db, self.create_logger(Bookmaker.BETSSON.value), notifier)
        # root_logger.info(f"Betsson scrapper created with {len(betsson_urls)} urls")
        # scrappers.append(betsson_scrapper)
        
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
            root_logger.info(f"Running {len(scrappers)} scrappers in sequence...")
            # Create a global driver for all scrappers
            global_driver = self.create_driver()
            # Iterate the scrappers and run them
            for scrapper in scrappers:
                # Set the global driver for each scrapper
                scrapper.driver = global_driver
                # Run the scrapper directly
                scrapper.run_scrapper()

    def end_scrapping(self):
        """Closes the driver and window for each scrapper
        """
        self.driver.quit()