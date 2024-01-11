from scrappers.configs.general_scrapper_configs import Sport

class Option_title_standardizer:
    """ Standardizes the option titles of the events
    """
        
    def standardize_event_winner_titles(self,sport):
        """ Returns the standardized option titles for the event winner market
        """
        if sport == Sport.FOOTBALL.value:
            return ["1", "X", "2"]
        else:
            return ["1", "2"]