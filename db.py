import psycopg2
from sqlalchemy import create_engine
import os
import pandas as pd

def get_db_engine():
    database_url = os.getenv('DATABASE_URL')
    engine = create_engine(database_url)
    return engine



import psycopg2

class Database:
    def __init__(self, db_url):
        self.db_url = db_url
        self.conn = None
        self.ensure_connection()

    def __enter__(self):
        # Return self to allow usage like `with Database() as db:`
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Close the database connection when exiting the context
        if self.conn:
            self.conn.close()

    def connect_to_database(self):
        try:
            self.conn = psycopg2.connect(self.db_url)
            print("Database connection established.")
        except Exception as e:
            print(f"Failed to connect to the database: {e}")
            self.conn = None

    def ensure_connection(self):
        # Check if connection is open; if not, try to reconnect
        if self.conn is None or self.conn.closed == 1:
            self.connect_to_database()


    def create_table(self):
        self.ensure_connection()
        if self.conn is not None:
            try:
                with self.conn.cursor() as cur:
                    cur.execute('''
                        CREATE TABLE IF NOT EXISTS fairy_tales (
                            id SERIAL PRIMARY KEY,
                            prompt TEXT,
                            fairy_tale TEXT,
                            image_url TEXT
                        );
                    ''')
                    self.conn.commit()
            except Exception as e:
                print(f"Failed to create table: {e}")

    def insert_fairy_tale(self, prompt, story, image_url):
        self.ensure_connection()
        if self.conn is not None:
            with self.conn.cursor() as cur:
                # Using parameterized queries to ensure safety against SQL injection
                cur.execute('''
                    INSERT INTO fairy_tales (prompt, fairy_tale, image_url)
                    VALUES (%s, %s, %s)
                ''', (prompt, story, image_url))
                self.conn.commit()
        else:
            print("Failed to execute database command: No active connection.")
            
    def fetch_fairy_tales(self):
        if self.conn:
            try:
                with self.conn.cursor() as cur:
                    cur.execute('SELECT id, prompt, fairy_tale, image_url FROM fairy_tales')
                    return cur.fetchall()
            except Exception as e:
                print(f"An error occurred while fetching fairy tales: {e}")
                return []
        else:
            print("Connection not available.")
            return []

"""
class Database:
    def __init__(self, db_url):
        self.db_url = db_url
        self.conn = None

    def __enter__(self):
        self.conn = psycopg2.connect(self.db_url)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

    def insert_fairy_tale(self, prompt, story, image_url):
        self.ensure_connection()
        if self.conn is not None:
            with self.conn.cursor() as cur:
                # Using parameterized queries to ensure safety against SQL injection
                cur.execute('''
                    INSERT INTO fairy_tales (prompt, fairy_tale, image_url)
                    VALUES (%s, %s, %s)
                ''', (prompt, story, image_url))
                self.conn.commit()
        else:
            print("Failed to execute database command: No active connection.")


        
    def fetch_fairy_tales(self):
        if self.conn is not None:
            with self.conn.cursor() as cur:
                cur.execute('SELECT id, prompt, fairy_tale, image_url FROM fairy_tales')
                return cur.fetchall()
        else:
            print("Failed to fetch fairy tales: No active or valid connection.")
            return []



    def create_table(self):
        with self.conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS fairy_tales (
                    id SERIAL PRIMARY KEY,
                    prompt TEXT,
                    fairy_tale TEXT,
                    image_url TEXT
                );
            ''')
            self.conn.commit()

"""
