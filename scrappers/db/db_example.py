""" Exaple of how to use the Database class to connect to the database and execute queries.
"""
from db import Database

db = Database()

# Example of executing a query
query = "SELECT * FROM Events"
result = db.execute_query(query, data=None)
for event in result:
    print(event)
# Process the result or perform other database operations...

