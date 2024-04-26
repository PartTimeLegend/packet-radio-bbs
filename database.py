import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self, host, user, password, database_name):
        self.conn = self.connect_to_database(host, user, password, database_name)

    def connect_to_database(self, host, user, password, database_name):
        try:
            conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database_name
            )
            if conn.is_connected():
                print('Connected to MySQL database')
                return conn
        except Error as e:
            print(f'Error connecting to MySQL database: {e}')
            return None

    def execute_query(self, query, params=None):
        cursor = self.conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.conn.commit()
            return cursor
        except Error as e:
            print(f"Error executing query: {e}")
            return None
