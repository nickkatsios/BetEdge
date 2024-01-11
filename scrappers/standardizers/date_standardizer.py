from datetime import datetime, timedelta

class Date_standardizer:
    """Class that standardizes the date format for the db""

    Usage:
        standardizer = DateStandardizer()
        standardized_date = standardizer.standardize_date(date_str, bookmaker)

    Dates in the DB are DATETIMES with format: YYYY:MM:DD HH:MM:SS
    Seconds should usually be set to 0
    """
    def __init__(self):
        self.format_mapping = {}
        self.add_format_conversion('novibet' , self.novibet_conversion)
        self.add_format_conversion('stoiximan' , self.stoiximan_conversion)
        self.add_format_conversion('betshop' , self.betshop_conversion)
        self.add_format_conversion('betsson' , self.betsson_conversion)

    def add_format_conversion(self, format_key, conversion_func):
        """Adds a new format conversion function to the format mapping
        
        Args:
            format_key: A string that represents the bookmaker
            conversion_func: A function that converts a date string to a datetime object for the db
        """
        self.format_mapping[format_key] = conversion_func

    def standardize_date(self, date_str, bookmaker):
        if bookmaker in self.format_mapping:
            try:
                conversion_func = self.format_mapping[bookmaker]
                standardized_date = conversion_func(date_str)
                return standardized_date
            except ValueError as e:
                raise ValueError(f"Unable to convert to datetime: {date_str}")
            
    def novibet_conversion(self, date_str):
        """Converts a date string to a datetime object for the db for novibet
        Args:
            date_str: A string that represents the scrapped date
        Returns:
            date_obj: A datetime object that represents the date for the db
        """

        def format_1(date_str):
            # For the case eg Apr 30 23:00
            # Parse the date string using the specified format
            date_obj = datetime.strptime(date_str, "%b %d %H:%M")
            # Assuming the date is for the current year, you may want to add the current year to the datetime object
            date_obj = date_obj.replace(year=datetime.now().year)
            return date_obj
            
    
        def format_2(date_str):
            # For the case eg Mon 23:00
            abreviated_weekdays_nums = {
                "Mon": 0,
                "Tue": 1,
                "Wed": 2,
                "Thu": 3,
                "Fri": 4,
                "Sat": 5,
                "Sun": 6
            }
    
            day_str, time_str = date_str.split(" ")
            hour, minute = map(int, time_str.split(":"))
    
            # Find the next occurrence of the specified day of the week relative to the current date
            current_datetime = datetime.now()
            current_weekday = current_datetime.weekday()
            target_weekday = abreviated_weekdays_nums[day_str]
    
            days_to_add = (target_weekday - current_weekday + 7) % 7
            if days_to_add == 0:
                days_to_add = 7
    
            next_occurrence = current_datetime + timedelta(days=days_to_add)
    
            # Create the datetime object with the year, day, hour, and minute
            date_obj = next_occurrence.replace(hour=hour, minute=minute, second=0, microsecond=0)
    
            return date_obj
        
        def format_3(date_str):
            """ For the case eg 23:00 """
            hour, minute = map(int, date_str.split(":"))
            current_date = datetime.now().date()
            date_obj = datetime(current_date.year, current_date.month, current_date.day, hour, minute)
            return date_obj
        
        # List of conversion functions to try
        conversion_functions = [format_1, format_2, format_3]
            
        # Try each conversion function until one works
        for conversion_function in conversion_functions:
            try:
                date_obj = conversion_function(date_str)
                return date_obj
            except ValueError:
                pass

    def stoiximan_conversion(self, date_str):
        """Converts a date string to a datetime object for the db for stoiximan
        Args:
            date_str: A string that represents the scrapped date
        Returns:
            date_obj: A datetime object that represents the date for the db
        """

        def format_1(date_str):
            # For the case eg Sunday, 20 August 2023 22:00
            # Parse the date string using the specified format
            date_obj = datetime.strptime(date_str, "%A, %d %B %Y %H:%M")
            return date_obj
        
        # List of conversion functions to try
        conversion_functions = [format_1]
            
        # Try each conversion function until one works
        for conversion_function in conversion_functions:
            try:
                date_obj = conversion_function(date_str)
                return date_obj
            except ValueError:
                pass

    def betshop_conversion(self, date_str):
        """Converts a date string to a datetime object for the db for stoiximan
        Args:
            date_str: A string that represents the scrapped date
        Returns:
            date_obj: A datetime object that represents the date for the db
        """

        def format_1(date_str):
            # For the case eg 30/04 23:00
            # Assuming the date is for the current year, you can add the current year to the date string
            date_str_with_year = f"{datetime.now().year}/{date_str}"
            date_obj = datetime.strptime(date_str_with_year, "%Y/%d/%m %H:%M")
            return date_obj
        
        # List of conversion functions to try
        conversion_functions = [format_1]
            
        # Try each conversion function until one works
        for conversion_function in conversion_functions:
            try:
                date_obj = conversion_function(date_str)
                return date_obj
            except ValueError:
                pass

    def betsson_conversion(self, date_str):
        """Converts a date string to a datetime object for the db for betsson
        Args:
            date_str: A string that represents the scrapped date
        Returns:
            date_obj: A datetime object that represents the date for the db
        """

        def format_1(date_str):
            # For the case eg 18 Aug, 21:00 
            # Assuming the date is for the current year, you can add the current year to the date string
            date_str_with_year = f"{datetime.now().year}, {date_str}"
            date_obj = datetime.strptime(date_str_with_year, "%Y, %d %b, %H:%M")
            return date_obj
        
        # List of conversion functions to try
        conversion_functions = [format_1]
            
        # Try each conversion function until one works
        for conversion_function in conversion_functions:
            try:
                date_obj = conversion_function(date_str)
                return date_obj
            except ValueError:
                pass


                    


