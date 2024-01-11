from datetime import datetime
from matchers.event_matcher import Event_matcher

class Scrapper_event_handler:

    def __init__(self, db , bookmaker_id, logger) -> None:
        self.db = db
        self.bookmaker_id = bookmaker_id
        self.logger = logger
        self.event_matcher = Event_matcher(self.logger)
        self.logger.info(f"Scrapper event handler initialized for bookmaker {bookmaker_id}")

    def load_db_events(self):
        """ Loads the events from the db

        Returns:
            db_events: A list of tuples containing the events from the db
        """
        sql = "SELECT * FROM Events"
        db_events = self.db.execute_query(sql, data=None)
        return db_events
    
    def validate_replace_none(self, *args):
        """ Validates and replaces None values with empty strings in the given arguments.
        Args:
            *args: Variable number of arguments to validate and replace None values.
        Returns:
            Tuple: Tuple containing the validated and replaced values.
        """
        validated_args = tuple('' if arg is None else arg for arg in args)
        self.logger.info(f"None values replaced with empty strings in args: {validated_args}")
        return validated_args


    def event_exists_in_db(self, sport_id, league, team1, team2, time):
        """ Checks if the event exists in the db
        Args:
            league: A string containing the league name of the event
            team1: A string containing the name of the first team
            team2: A string containing the name of the second team
            time: A string containing the datetime of the event

        Note: the handler will load the events from the db only once at the creation of the scrapper
        If scrappers are running in parallel and an event is added to the db,
        the handler will not know about it

        Returns:
            event_id: An integer containing the id of the event if it exists in the db
            or 0 if it doesn't exist
        """
        db_events = self.load_db_events()
        for db_event in db_events:
            event_id = self.event_matcher.event_matches(sport_id , league, team1, team2, time, db_event)
            if event_id != 0:
                return event_id 
        return 0
                
    def write_event_to_db(self, sport_id, league, team1, team2, time):
        """ Writes a new event to the db

        Args:
            league: A string containing the league name of the event
            team1: A string containing the name of the first team
            team2: A string containing the name of the second team
            time: A string containing the datetime of the event
        """
        # replace all none parameters with empty strings
        sport_id, league, team1, team2, time = self.validate_replace_none(sport_id, league, team1, team2, time)

        # if time is empty string, set it to 1970-01-01 00:00:00 (unix epoch) , to be replaced later
        time = datetime(1970, 1, 1, 00, 00) if time == '' else time
        
        sql = "INSERT INTO Events (sport_id, team_name1, team_name2, league_name, event_date, found_in) VALUES (%s, %s, %s, %s, %s, %s)"
        found_in = str(self.bookmaker_id)
        values = (sport_id, team1, team2, league, time, found_in)
        new_event_id = self.db.execute_insert(sql, values)
        self.logger.info(f"New event written to db with ID: {new_event_id}")
        return new_event_id

    def update_event_in_db(self, event_id):
        """ Updates the event in the db by adding the bookmaker id in the "found in" column

        Args:
            event_id: An integer containing the id of the event
        """

        # Get the old found_in string
        sql = "SELECT found_in FROM Events WHERE event_id = %s"
        values = (event_id,)
        self.db.execute_query(sql, values)
        old_found_in_string = self.db.execute_query(sql, values)
        old_found_in_string = old_found_in_string[0][0]
        # Add the new bookmaker id to the string and update the db
        sql = "UPDATE Events SET found_in = %s WHERE event_id = %s"
        new_found_in_string = old_found_in_string + "," + str(self.bookmaker_id)
        values = (new_found_in_string, event_id)
        self.db.execute_update(sql, values)
        self.logger.info(f"Event updated in db")

    def write_odds_to_db(self, bookmaker_id, event_id, market_id, option_titles, market_odds, market_name):
        """ Writes the odds to the db

        Args:
            event_id: An integer containing the id of the event
            market_name: A string containing the name of the market
            option_titles: A list of strings containing the titles of the options
            odds: A list of strings containing the odds of the options
        """
        # Write options to db
        db_timestamp = datetime.now()
        for i in range(len(option_titles)):
            sql = "INSERT INTO Odds (bookmaker_id, event_id, market_id, option_title, odds_value, timestamp) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (bookmaker_id, event_id, market_id, option_titles[i], market_odds[i], db_timestamp)
            self.db.execute_insert(sql, values)
        self.logger.info(f"New options written to db for: {market_name}")

    def handle_event(self, sport_id, league, team1, team2, time):
        """ Handles the scrapped event

        it checks if the event exists in the db and if it doesn't it writes it to the db
        if it does exist it updates the "found in" column in the db to add the bookmaker id

        Args:
            league: A string containing the league name of the event
            team1: A string containing the name of the first team
            team2: A string containing the name of the second team
            time: A string containing the datetime of the event
        
        Returns:
            event_id: An integer containing the id of the event

        """
        event_id = self.event_exists_in_db(sport_id , league, team1, team2, time)
        if event_id == 0:
            # Write event to db
            event_id = self.write_event_to_db(sport_id, league, team1, team2, time)
        else:
            # Update existing event in db
            self.update_event_in_db(event_id)
        return event_id