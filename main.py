#!/usr/bin/env python3
from dotenv import load_dotenv, find_dotenv
import psycopg
# Could use an ORM (such as SQLAlchemy) if time resources were plenty.
import os
# Could use class based approach, but... time.
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


def get_db_connection():
    try:
        conn = psycopg.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f'Could not connect to Stylite database. Error: {e}')


def fetch_records():
    print("Connecting to database.")
    conn = get_db_connection()
    print(conn)
    cur = conn.cursor()
    print("Fetching shop records.")
    cur.execute("SELECT * FROM t_shops")
    shops = cur.fetchall()
    print("Fetching budget records.")
    cur.execute("SELECT * FROM t_budgets")
    budgets = cur.fetchall()
    print(shops)
    print(budgets)
    conn.close()
    pass


def handle_half_budget(shop_id):
    pass


def handle_full_budget(shop_id):
    pass


def process_records(records):
    pass


if __name__ == "__main__":
    fetch_records()
