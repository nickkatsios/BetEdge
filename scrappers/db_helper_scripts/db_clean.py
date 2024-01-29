import sys
import os

# Append the project root directory to the sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from db.db import Database

""" Helper script to clean the database from non consistent data"""

if __name__ == '__main__':
    db = Database()
    # Delete all data from tables
    sql = "DELETE FROM Urls"
    db.execute_update(sql, data=None)
    print("----------URLs deleted----------")
    sql = "DELETE FROM Odds"
    db.execute_update(sql, data=None)
    print("----------Odds deleted----------")
    sql = "DELETE FROM Arbitrage"
    db.execute_update(sql, data=None)
    print("----------Arbitrage deleted----------")
    sql = "DELETE FROM Arbitrage_Outcomes"
    db.execute_update(sql, data=None)
    print("----------Arbitrage_Outcomes deleted----------")
    sql = "DELETE FROM Events"
    db.execute_update(sql, data=None)
    print("----------Events deleted----------")

