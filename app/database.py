import sqlite3
from contextlib import closing

# Database file path
DB_FILE = 'voip_database.db'

class Database:
    def __init__(self):
        self.connection = sqlite3.connect(DB_FILE)
        self.connection.row_factory = sqlite3.Row

    def create_table(self):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            self.connection.commit()

    def close(self):
        self.connection.close()

    def execute_query(self, query, parameters=()):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(query, parameters)
            return cursor.fetchall()

    def execute_write_query(self, query, parameters=()):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(query, parameters)
            self.connection.commit()