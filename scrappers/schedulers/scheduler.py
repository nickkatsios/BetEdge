from scrappers.scrapper_manager import Scrapper_manager
from urls.url_scrapper_manager import Url_scrapper_manager
from scrappers.configs.general_scrapper_configs import asci_art
import schedule
import time

class ScraperScheduler:
    """ A Scheduler is a component that schedules the scrappers to run in a given interval

    Attributes:
        args: An object containing the cli arguments"""
    def __init__(self, args):
        self.args = args

    def run_odds_scrappers(self):
        """ Runs the scrappers from central Scrapper Manager Class"""
        print(asci_art)
        manager = Scrapper_manager(self.args.headless, self.args.parallel, self.args.logging,
                                   self.args.browser, self.args.notify)
        manager.run_scrappers()
        
    def run_url_scrappers(self):
        """ Runs the scrappers from central Scrapper Manager Class"""
        manager = Url_scrapper_manager(self.args.headless, self.args.parallel, self.args.logging,
                                   self.args.browser, self.args.notify)
        manager.run_url_scrappers()

    def odds_scrapping_job(self):
        """ Specify the event and odds scrapping job to be run by the scheduler"""
        self.run_odds_scrappers()
        
    def url_scrapping_job(self):
        """Specify the league and event url scrapping job to be run by the scheduler"""
        self.run_url_scrappers()

    def start_scheduler(self):
        # Schedule the job to run every x minutes
        # Minutes provided by cli argument
        schedule.every(self.args.schedule_odds).minutes.do(self.odds_scrapping_job)
        
        schedule.every(self.args.schedule_urls).minutes.do(self.url_scrapping_job)

        # Run the job continuously
        while True:
            schedule.run_pending()
            time.sleep(1)
            