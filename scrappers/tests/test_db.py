import pytest
from db.db import Database
import datetime

# Fixture to initialize the Database object
@pytest.fixture(scope="module")
def database():
    return Database()
    

@pytest.mark.parametrize("table", ["Events", "Odds", "Urls", "Sports", "Bookmakers"])

# Test cases for Database class
@pytest.mark.database
def test_execute_query(database , table):
    sql = f"SELECT * FROM {table}"
    result = database.execute_query(sql, None)
    assert isinstance(result, list)

@pytest.mark.database
def test_execute_insert(database):
    sql = "INSERT INTO Events (sport_id, team_name1, team_name2, league_name, event_date, found_in) VALUES (%s, %s, %s, %s, %s, %s)"
    data = (1, "team1", "team2", "league", datetime.datetime.now(), 1)
    result = database.execute_insert(sql, data)
    assert isinstance(result, int)  


# Add more test cases for other methods as needed

# If you have tests that require setup and teardown
# you can use fixtures for that purpose
