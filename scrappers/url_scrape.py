from scrappers.configs.general_scrapper_configs import Bookmaker, Sport
import argparse
from urls.url_scrapper_manager import Url_scrapper_manager
import logging

""" Main file that runs the url scrappers once"""

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
    args = parser.parse_args()
    return args

def config_logging(is_logging):
    """ Configures the top level logging module
        and creates the logs directory if it doesn't exist
    """
    if is_logging:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    # Argument parsing
    args = process_args()
    config_logging(args.logging)
    url_scrapper_manager = Url_scrapper_manager(args.headless , args.parallel, args.logging, args.browser , args.notify)
    url_scrapper_manager.run_url_scrappers()
    
    