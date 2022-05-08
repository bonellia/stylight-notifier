#!/usr/bin/env python3
from dotenv import load_dotenv
import psycopg
# Could use an ORM (such as SQLAlchemy) if time resources were plenty.
import os

# Could use class based approach, but... time.
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


def get_db_connection():
    """
    Using the environment variables, connects to the Stylight database.

    :return: The connection instance to be used.
    """
    try:
        conn = psycopg.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f'Could not connect to Stylite database. Error: {e}')


def fetch_records():
    """
    Using notify_list view, fetches records of interest.
    :return: List of shops with their budget status.
    """
    print("Connecting to database...")
    conn = get_db_connection()
    print(conn)
    cur = conn.cursor()
    print("Fetching notify list records.")
    cur.execute("SELECT * FROM notify_list")
    qualifying_shops = cur.fetchall()
    print(qualifying_shops)
    print("Closing DB connection.")
    conn.close()
    return qualifying_shops


def handle_half_budget(shop):
    """
    Notifies the shop that has exceeded half of its budget.
    :param shop: Subject shop that needs to be notified.
    """
    print(f'{shop[4]} has used half their budget!')


def set_shop_offline(shop):
    """
    Given a shop, sets it offline.
    :param shop: Subject shop that exceeded their budget.
    """
    update_query = """ UPDATE t_shops
                    SET a_online = %s
                    WHERE a_id = %s"""
    conn = None
    try:
        print(f'Unlisting shop with the ID {shop[0]}.')
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(update_query, (False, shop[0]))
        conn.commit()
        cur.close()
    except (Exception, psycopg.DatabaseError) as error:
        print(f'Error: {error}')
    finally:
        if conn is not None:
            conn.close()


def handle_full_budget(shop):
    """
    Notifies the given shop and turns it offline.
    :param shop: Subject shop that will be handled.
    """
    print(f'{shop[4]} has used all their budget!')
    set_shop_offline(shop)


def process_records(records):
    """
    Using the records provided, triggers necessary actions.
    :param records: List of shop records to process.
    """
    print("Processing budget status of shops.")
    for shop in records:
        shop_id, budget_cycle, budget_max, budget_spent, shop_name, is_listed = shop
        if budget_spent < budget_max:
            if budget_spent >= budget_max / 2:
                handle_half_budget(shop)
        else:
            handle_full_budget(shop)


if __name__ == "__main__":
    operation_records = fetch_records()
    process_records(operation_records)
