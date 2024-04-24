import psycopg2
from sqlalchemy import create_engine
import os
import pandas as pd

def get_db_engine():
    database_url = os.getenv('DATABASE_URL')
    engine = create_engine(database_url)
    return engine

class Database:
    def __init__(self, url):
        self.conn = psycopg2.connect(url)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def create_table(self):
        with self.conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS fairy_tales (
                    id SERIAL PRIMARY KEY,
                    prompt TEXT,
                    fairy_tale TEXT
                );
            ''')
            self.conn.commit()

    def insert_fairy_tale(self, prompt, fairy_tale):
        with self.conn.cursor() as cur:
            cur.execute('''
                INSERT INTO fairy_tales (prompt, fairy_tale)
                VALUES (%s, %s)
            ''', (prompt, fairy_tale))
            self.conn.commit()

    def fetch_fairy_tales(self):
        with self.conn.cursor() as cur:
            cur.execute('SELECT id, prompt, fairy_tale FROM fairy_tales')
            rows = cur.fetchall()
            df = pd.DataFrame(rows, columns=['id', 'prompt', 'fairy_tale'])
            return df

def format_fairy_tale_dataframe(df):
    # This function can be enhanced to format fairy tale data as needed
    return df
