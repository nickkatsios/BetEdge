from scrappers.scrapper_manager import Scrapper_manager
from schedulers.scheduler import ScraperScheduler
from scrappers.configs.general_scrapper_configs import asci_art
import argparse
import logging
import os

""" Main file that triggers the scrappers once
"""

def process_args() :
    """Processes the arguments from the command line

    See help for available arguments
    Returns:
        args: An object containing the arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--headless', help='Runs the scrappers from a headless browser (no GUI)' , action='store_true' , required=False)
    parser.add_argument('--parallel', '-p', help='Runs the scrappers in parallel processes using the concurrent.futures module' , action='store_true' , required=False)
    parser.add_argument('--logging', '-l', help='Enables logging. At the top level, it means that the logs are visible in the console as the scrappers are running. In the scrapper level it means that logs are written continously in the /logs folder' , action='store_true' , required=False)
    browser_choices = ['chrome', 'firefox']
    parser.add_argument('--browser', '-b', type=str, help=f'Name of the browser to be used in scrapping. Available options: {", ".join(browser_choices)}. Default: chrome', choices=browser_choices, default='chrome', required=False)
    parser.add_argument('--notify', '-n', help='Enables email notifications. Default: False' , action='store_true' , required=False)
    parser.add_argument('--schedule_odds', '-s' , help='Runs the odds scrappers in a schedule of x minutes' , type=int , required=False , default=0)
    parser.add_argument('--schedule_urls', '-u' , help='Runs the url scrappers in a schedule of x minutes' , type=int , required=False , default=0)
    args = parser.parse_args()
    return args

def config_logging(is_logging):
    """ Configures the top level logging module
        and creates the logs directory if it doesn't exist
    """
    if is_logging:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    if not os.path.exists('logs'):
        os.makedirs('logs')

def run_scrappers(is_headless , is_parallel, is_logging, browser , notify):
    """ Runs the scrappers from central Scrapper Manager Class
    """
    print(asci_art)
    manager = Scrapper_manager(is_headless , is_parallel, is_logging, browser , notify)
    manager.run_scrappers()
    
def run_scheduler(args):
    """ Runs the scheduler from central Scheduler Class"""
    scheduler = ScraperScheduler(args)
    scheduler.start_scheduler()

if __name__ == '__main__':
    args = process_args()
    config_logging(args.logging)
    
    if args.schedule_odds != 0 or args.schedule_urls != 0:
        run_scheduler(args)
    else:
        run_scrappers(args.headless , args.parallel,
                      args.logging , args.browser , args.notify)
