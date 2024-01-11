![CI](https://github.com/nickkatsios/BetEdge-Scrappers/actions/workflows/build_and_test.yml/badge.svg)

# Betedge-Scrappers
A repo containing the scrapping scripts for all bookmakers for the Betedge project.

## Getting Started
1. Install MySQL server on your local machine. This project is meant to be run and tested on Ubuntu. You can find the instructions [here](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04).
2. Replicate the db schema to your local MySQL server by running the scripts located in ```/db/sql```.
```bash
mysql -u <your_db_username> -p < ./db/sql/create_schema.sql
```
3. Add the categories, bookmakers and markets to the db by running the scripts located in ```/db/sql```.
```bash 
mysql -u <your_db_username> -p < ./db/sql/add_test_data.sql
```
Replace ```<your_db_username>``` with your local mysql username, usually root.</br></br>

4. Add you local mysql password in an `.env` file in the ```/db``` folder as shown in the .env.example file.

## Running
The project uses poetry for dependency management. To install poetry for your system follow the instructions [here](https://python-poetry.org/docs/#installing-with-pipx).
or
```bash
pip install poetry
```

Clone the project and cd into it:
```bash
git clone https://github.com/nickkatsios/BetEdge-Scrappers.git
cd BetEdge-Scrappers
```

After installing poetry, run the following command in the root directory of the project to install the dependencies:
```bash
poetry install
```
To extract the urls for scrapping ,run the following command in the root directory of the project:
```bash
poetry run python url_scrape.py
```
Or just add some sample urls in the db to test the scrappers.
```bash
python3 ./db_helper_scripts/db_load_sample_urls.py
```
To run the scrappers, run the following command in the root directory of the project:
```bash
poetry run python main_scrape.py
```
## Arguments
The following arguments can be passed to the script:
- ```-h``` or ```--help``` to get the help message.
- ```--headless``` to run the scrappers in headless mode (No browser GUI).
- ```--parallel``` or ```-p``` to run the scrappers in parallel with multiprocessing.
- ```--logging``` or ```-l``` Enables logging. At the top level, it means that the logs are visible in the console as the scrappers are running. In the scrapper level it means that logs are written continously in the /logs folder.
- ```--browser``` or ```-b``` to specify the browser to use. The default is ```chrome```. The supported browsers are ```chrome``` and ```firefox```.
-  ```--notify``` or ```-n``` to enable email notifications for errors. The email credentials must be added in a ```.env``` file in the notifers folder.
- ```--schedule_odds <interval>``` or ```-s``` to run the odds scrappers in scheduler mode. The scrappers will run every ***interval*** minutes. The scheduler can be stopped by pressing ```ctrl + c```.
- ```--schedule_urls <interval>``` to run the url scrappers in scheduler mode. The scrappers will run every ***interval*** minutes.

## Docker
To run the project in a docker container, do the following:
1. Create a .env file in the root directory of the project with the variables defined in the ```.env.example``` file.
2. Build the docker image by running:
```bash
docker compose up --build
```
If the app container fails the first time with a connection error to the db , it means that the db is still initializing. If you want to run the scrappers manually, wait a few seconds and try again.
1. Find the ***container id*** of the app container by running:
```bash
docker ps -a
```
2. Rerun the app container by running:
```bash
docker start <container_id>
```
If you want to run the scrappers in specified interval, add the ```--schedule``` argument to the CMD in the Dockerfile:
* CMD ["poetry", "run", "python3", "main_scrape.py" , "--logging" , "--headless" , "--browser", "firefox" , "--schedule" , "your_desired_interval"] this will eliminate the need to rerun the container manually.
## Adding a scrapper
1. Create a new class in the ```scrappers``` folder that inherits from the ```Scrapper_interface``` class and implements the methods defined. The class should be named `bookmakername_scrapper.py`.
(See the ```scrappers/novibet_scrapper.py``` for an example)
2. Define date standardization methods by adding them to ```date_standardizer``` and ```option_title_standardizer``` in ```standardizers```
3. Import and add the scrapper to the scrapper manager `run_scrappers()` method in ```scrappers/scrapper_manager.py```
## Practical steps
1. Copy/paste novibet scrapper
2. Iterate id on self.bookmaker id for the new scrapper in the __init__
3. Add scrapper config file --> map market titles to market ids
4.  Change class names and/or scrapping procedure in the methods included in get `get_event_details` and `get_markets`, `get_market_odds` according to the html of the new bookmaker site
5. Identify all date formats the bookmaker uses for an event and add a format function in `date_standardizer` for each date format (see novibet for example)
6.  Add test url entries to the db
7.  Test the scrapper and debug
8.  Add aditional functions as needed depending on the bookmaker site (eg: if you need to change language, or close popups etc)
9. When this is done , add the new scrapper to `scrapper_manager`
10. You are done

## Sanitization:
All scrappers should sanitize the data they return
eg: remove spaces, convert to lowercase, remove special characters , convert odds to float etc
This is to ensure that the data is consistent across all scrappers
The sanitization should be done inside the respective methods that return a text result

## Testing:
All scrappers should be tested individually to ensure that they return the correct data
before being added to the scrapper manager

# Standards
## Date standardization
All dates should be standardized to the following format: ```YYYY-MM-DD HH:MM:SS``` where seconds are usually 0
All dates are standardized by calling the ```date_standardizer.standardize_date()``` method.
## Odds standardization
All odds should be standardized to the following format: ```0.00``` where the odds are rounded to 2 decimal places
## Odds title standardization
For each market there exists a specified format for the option title.
All option titles are automatically formatted by calling the ```option_title_standardizer.standardize_option_title()``` method.
### Event winner markets
For event winner markets the title should be in the following format: ```1X2``` for 3-way markets and ```12``` for 2-way markets
### Over/Under markets
For over/under markets the title should be in the following format: ```Over/Under X.X``` where X.X is the value of the over/under eg ```Over 2.5``` , ```Under 2.5```

## Market standardization
All markets should be standardized to the following format: ```market_id``` where the market_id is the id of the market in the db.
To do that, the scrapper should have a dictionary called allowed_markets_bookmakername in the relative config file that maps the market titles to the market ids as they are being scrapped.
## Event standardization
All event teams are stored in the db as found in the bookmaker site. The scrapper should not change the team names in any way.
## Bookmaker standardization
The bookmaker id for each new scrapper should be added in the dictionary in the ```scrappers/configs/general_scrapper_configs.py``` file. The id is also initialized in the ```__init__``` method of each scrapper class.






