import sys
import os
import datetime

# Append the project root directory to the sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from db.db import Database

""" Helper script to add sample urls to the database for each bookmaker"""

if __name__ == '__main__':
    db = Database()
    sql = "INSERT INTO Urls (bookmaker_id, url, timestamp) VALUES (%s, %s, %s)"
    data = [
        (1, 'https://www.novibet.gr/en/sports/matches/pas-giannina-lamia/e33692811', datetime.datetime.now()),
        (2, 'https://en.stoiximan.gr/match-odds/pas-giannina-lamia/44262838/', datetime.datetime.now()),
        (3, 'https://www.betshop.gr/sports/sportevent/stoixima-podosfairo/greece-super-league/pas-giannina-lamia/5854924', datetime.datetime.now()),
        (4, 'https://www.betsson.gr/en/sportsbook/football/greece/greece-super-league-1', datetime.datetime.now()),
    ]
    for row in data:
        db.execute_insert(sql, row)
    print("--------- Sample urls added to the database ---------")


