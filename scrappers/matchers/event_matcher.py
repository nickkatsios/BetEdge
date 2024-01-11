import re

class Event_matcher:

    def __init__(self, logger):
        self.logger = logger
    """
    This class is responsible for matching events from the db with events from the bookmakers.

    It associates them based on the names of the teams and the time of the events.
    Strategy for team names:
    1) Check for exact match --> if true obviously they are the same events --> return (no need for further validation)
    2) Check for regex match --> if true they are the same events --> return (no need for further validation)
    3) Check for one word match match --> if true at least one word from one team name exist in the other --> return (acceptable from testing) , will cross check with time
    4) Check for fuzzy match --> if true the names are similar --> return (acceptable from testing)
    5) If none of the above return False
    6) If the names match, check if the time of the events is the same --> if true return (no need for further validation)
    """
    
    def team_names_match(self, team1 , team2 , db_team1 , db_team2):
        """
        Implementation of the team name matching strategy
        
        Returns:
        bool: True if the team names match, False otherwise 
        """

        team1_bet1 = team1
        team2_bet1 = team2

        team1_bet2 = db_team1
        team2_bet2 = db_team2

        exact_match = self.is_exact_name_match(team1_bet1 , team1_bet2) and self.is_exact_name_match(team2_bet1 , team2_bet2)
        if(exact_match):
            return True
        
        regex_match = self.is_regex_match(team1_bet1 , team1_bet2) and self.is_regex_match(team2_bet1 , team2_bet2)
        if(regex_match):
            return True
        
        one_word_match = self.is_one_word_match(team1_bet1 , team1_bet2) and self.is_one_word_match(team2_bet1 , team2_bet2)
        if(one_word_match):
            return True
        
        fuzzy_match = self.is_fuzzy_match(team1_bet1 , team1_bet2 , 2) and self.is_fuzzy_match(team2_bet1 , team2_bet2 , 2)
        if(fuzzy_match):
            return True
                
        return False

    def is_exact_name_match(self, team_name1 , team_name_2):
        """Checks if 2 team names from a pair of events match exactly

        Args:
        team_name1 (str): The name of the first team
        team_name_2 (str): The name of the second team    
        
        Returns: 
        bool: True if the names match, False otherwise
        """
        return team_name1 == team_name_2
    
    def is_regex_match(self ,team_name1 , team_name_2):
        """Checks if 2 team names from a pair of events match using regular expressions

        Args:
        team_name1 (str): The name of the first team
        team_name_2 (str): The name of the second team    
        
        Returns: 
        bool: True if the names match, False otherwise
        """

        #remove non-alphanumeric characters and convert to lowercase
        team_name1 = re.sub(r'\W+', '', team_name1).lower()
        team_name_2 = re.sub(r'\W+', '', team_name_2).lower()

        # match the team names using regular expressions
        pattern = r'\b' + re.escape(team_name1) + r'\b'
        return bool(re.search(pattern, team_name_2, re.IGNORECASE))
    
    
    def is_one_word_match(self ,team_name1, team_name2):
        """Checks if a single word of one string exists in the other.

        !!!!!!!!!!
        Returns False Positives 
        eg "Manchester United" and "Manchester City" will match
        !!!!!!!!!!

        Args:
        team_name1 (str): The name of the first team
        team_name_2 (str): The name of the second team    
        
        Returns: 
        bool: True if the names match, False otherwise
        """
        words1 = team_name1.split()
        words2 = team_name2.split()

        for word in words1:
            if word in words2:
                return True

        for word in words2:
            if word in words1:
                return True

        return False
    
    def is_fuzzy_match(self ,team_name1 , team_name_2, max_dist):
        """Sellers algorithm for approximate string matching

        Complexity: O(n * m)
        Returns True if the two input strings match within the specified maximum
        edit distance, False otherwise.

        Args:
        team_name1 (str): The name of the first team
        team_name_2 (str): The name of the second team    
        
        Returns: 
        bool: True if the names match approximately, False otherwise
        """
        # Initialize the distance matrix with zeros
        n = len(team_name1)
        m = len(team_name_2)
        dist = [[0 for j in range(m+1)] for i in range(n+1)]

        # Initialize the first row and column of the distance matrix
        for i in range(n+1):
            dist[i][0] = i
        for j in range(m+1):
            dist[0][j] = j

        # Fill in the rest of the distance matrix
        for i in range(1, n+1):
            for j in range(1, m+1):
                cost = 0 if team_name1[i-1] == team_name_2[j-1] else 1
                dist[i][j] = min(dist[i-1][j]+1, dist[i][j-1]+1, dist[i-1][j-1]+cost)

        return dist[n][m] <= max_dist
    

    def times_match(self, time, db_time):
        """ Checks if the given times match

        Args:
            time: A datetime object containing the time of the event
            db_time: A datetime object containing the time of the db event
        """
        return (
        time.year == db_time.year
        and time.month == db_time.month
        and time.day == db_time.day
        and time.hour == db_time.hour
        # Can also check minutes and seconds if needed
    )
    
    def sports_match(self, sport, db_sport):
        """ Checks if the given sports match

        Args:
            sport: A string containing the sport of the event
            db_sport: A string containing the sport of the db event
        """
        return sport == db_sport
    
    def event_matches(self, sport_id, league, team1, team2, time, db_event):
        """ Checks if the given event info matches the db event

        Args:
            league: A string containing the league name of the event
            team1: A string containing the name of the first team
            team2: A string containing the name of the second team
            time: A datetime object containing the time of the event
            db_event: A tuple containing the event info from the db
        """
        # Deconstruct the db_event tuple
        # TODO and self.sports_match(sport_id, db_sport_id) when more sports are added
        db_event_id, db_sport_id, db_team1, db_team2,  db_league, db_time, found_in = db_event
        if self.team_names_match(team1, team2, db_team1, db_team2) and self.times_match(time, db_time):
            self.logger.info(f"Event matched with db event with id: {db_event_id}")
            return db_event_id
        return 0