import mysql.connector.pooling
import os
from dotenv import load_dotenv
import logging

class Database:
    def __init__(self):
        """ Initializes the connection pool to the database

        The connection pool is created and managed separately from the instances of the database class.
        When you create a new instance of the database class,
        it will access the same connection pool (assuming you are using the same pool_name),
        which means the pool will handle connection reuse and management across
        all the instances of the database class.

        This behavior ensures that the database connections are shared and reused efficiently,
        even if you create multiple objects of the database class in
        different modules or parts of your application.
        """

        load_dotenv()
        DB_HOST = os.getenv('DB_HOST')
        DB_USER = os.getenv('DB_USER')
        DB_PASS = os.getenv('DB_PASS')
        DB_NAME = os.getenv('DB_NAME')
        DB_PORT = os.getenv('DB_PORT')
        db_config = {
            "host": DB_HOST,
            "port": DB_PORT,
            "user": DB_USER,
            "password": DB_PASS,
            "database": DB_NAME,
            "auth_plugin" : 'mysql_native_password'
        }

        self.pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="scrapper_pool",
                                                               pool_size=4,  # Set the pool size as needed
                                                               **db_config)
        root_logger = logging.getLogger()
        root_logger.info("----------- Successfully connected to the database on port: " + DB_PORT + " host: " + DB_HOST + "-----------")

    def execute_query(self, query, data):
        """ Executes a query to the database

        Args:
            query: A string containing the query to be executed
            data: A tuple containing the data to be inserted to the database

        Returns:
            result: A list containing the results of the query
        """
        connection = self.pool.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(query, data)
            result = cursor.fetchall()
            connection.commit()
            return result
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()
            connection.close()

    def execute_update(self, query, data):
        """ Executes an update query to the database

        Args:
            query: A string containing the query to be executed
            data: A tuple containing the data to be inserted to the database
        """
        connection = self.pool.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(query, data)
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()
            connection.close()
    
    def execute_insert(self, query, data):
        """ Executes an insert query to the database

        Args:
            query: A string containing the query to be executed
            data: A tuple containing the data to be inserted to the database

        Returns:
            lastrowid: An integer containing the id of the last inserted row
        """
        connection = self.pool.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(query, data)
            connection.commit()
            lastrowid = cursor.lastrowid
            return lastrowid
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()
            connection.close()