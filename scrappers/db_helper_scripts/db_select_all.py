import sys
import os

# Append the project root directory to the sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from db.db import Database
import argparse

""" Helper script to retrieve all items from a MySQL table"""

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Retrieve all items from a MySQL table')
    parser.add_argument('table_name', type=str, help='Name of the table in the database')
    args = parser.parse_args()
    print("----------- "+ args.table_name + " -----------")
    mydb = Database()
    # Execute query
    query = f"SELECT * FROM {args.table_name}"
    result = mydb.execute_query(query, data=None)
    # Print results
    for row in result:
        print(row)