from django.db import models
""" The models.py file is used to define the database schema.
    After defining the schema, django can manipulate the database easily.
    The schema is defined using classes, which are mapped to tables in the database.
    The fields of the classes are mapped to columns in the database.

    The meta class is used to tell django not to manage the tables and
    use the existing tables in local mysql instead.
"""

class Bookmakers(models.Model):
    bookmaker_id = models.AutoField(primary_key=True)
    bookmaker_name = models.CharField(max_length=255, null=False)

    class Meta:
        managed = False  # This tells Django not to manage this table
        db_table = 'Bookmakers'  # Use the existing table name

class Sports(models.Model):
    sport_id = models.AutoField(primary_key=True)
    sport_name = models.CharField(max_length=255, unique=True)

    class Meta:
        managed = False  # This tells Django not to manage this table
        db_table = 'Sports'  # Use the existing table name

class Events(models.Model):
    event_id = models.AutoField(primary_key=True)
    sport_id = models.ForeignKey(Sports, db_column='sport_id', on_delete=models.CASCADE)
    team_name1 = models.CharField(max_length=255, null=False)
    team_name2 = models.CharField(max_length=255, null=False)
    league_name = models.CharField(max_length=255, null=True)
    event_date = models.DateTimeField(null=False)
    found_in = models.CharField(max_length=255)

    def __str__(self):
        return self.team_name1 + ' vs ' + self.team_name2 + ' ' + self.league_name

    class Meta:
        managed = False  # This tells Django not to manage this table
        db_table = 'Events'  # Use the existing table name

class Markets(models.Model):
    market_id = models.AutoField(primary_key=True)
    market_type = models.CharField(max_length=255, null=False)

    class Meta:
        managed = False  # This tells Django not to manage this table
        db_table = 'Markets'  # Use the existing table name

class Odds(models.Model):
    odd_id = models.AutoField(primary_key=True)
    bookmaker_id = models.ForeignKey(Bookmakers, db_column='bookmaker_id', on_delete=models.CASCADE)
    event_id = models.ForeignKey(Events, db_column='event_id', on_delete=models.CASCADE)
    market_id = models.ForeignKey(Markets, db_column='market_id', on_delete=models.CASCADE)
    option_title = models.CharField(max_length=255, null=False)
    odds_value = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    timestamp = models.DateTimeField(null=False)

    def __str__(self):
        return 'Title: ' + self.option_title + ' Value: ' + str(self.odds_value) + ' Found in: ' + str(self.bookmaker_id.bookmaker_name)

    class Meta:
        managed = False  # This tells Django not to manage this table
        db_table = 'Odds'  # Use the existing table name

class Arbitrage(models.Model):
    arbitrage_id = models.AutoField(primary_key=True)
    event_id = models.ForeignKey(Events, db_column='event_id' ,on_delete=models.CASCADE)
    market_id = models.ForeignKey(Markets, db_column='market_id', on_delete=models.CASCADE)
    arbitrage_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    timestamp = models.DateTimeField()
    
    class Meta:
        managed = False  # This tells Django not to manage this table
        db_table = 'Arbitrage'  # Use the existing table name

class ArbitrageOutcomes(models.Model):
    outcome_id = models.AutoField(primary_key=True)
    arbitrage_id = models.ForeignKey(Arbitrage, db_column='arbitrage_id', on_delete=models.CASCADE)
    bookmaker_id = models.ForeignKey(Bookmakers, db_column='bookmaker_id', on_delete=models.CASCADE)
    outcome_title = models.CharField(max_length=255, null=False)
    outcome_odds = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        managed = False  # This tells Django not to manage this table
        db_table = 'Arbitrage_Outcomes'  # Use the existing table name

class Urls(models.Model):
    url_id = models.AutoField(primary_key=True)
    bookmaker_id = models.ForeignKey(Bookmakers, db_column='bookmaker_id', on_delete=models.CASCADE)
    url = models.CharField(max_length=255, null=False)
    timestamp = models.DateTimeField(null=False)

    class Meta:
        managed = False  # This tells Django not to manage this table
        db_table = 'Urls'  # Use the existing table name
