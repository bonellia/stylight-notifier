#!/usr/bin/env python3
from dotenv import load_dotenv
from datetime import datetime
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
    Using a DB connection, retrieves shops and budgets.
    Returns them as a dictionary with keys "shops" and "budgets".
    """
    print("Connecting to database...")
    conn = get_db_connection()
    print(conn)
    cur = conn.cursor()
    print("Fetching shop records.")
    cur.execute("SELECT * FROM t_shops")
    shops = cur.fetchall()
    print("Fetching budget records.")
    cur.execute("SELECT * FROM t_budgets WHERE a_month >= date_trunc('month', CURRENT_DATE)")
    budgets = cur.fetchall()
    # print(shops)
    # print(budgets)
    print("Closing DB connection.")
    conn.close()
    return {"shops": shops, "budgets": budgets}


def find_shop(shop_id, shops):
    """
    Given a shop ID, tries to fetch matching shop record.

    :param shop_id: ID to query shop list.
    :param shops: Shop list to look for.
    :return: A shop tuple with the form (id, name, online).
    """
    try:
        # Filter shops that match the given ID.
        candidates = [shop for shop in shops if shop[0] == shop_id]
        return candidates[0]
    except (Exception, IndexError) as error:
        print(f'No shop found with the id {shop_id}')
        print(f'Error: {error}')


def handle_half_budget(shop_id, shops):
    """
    Given a shop ID, notifies the said shop that exceeds the half budget.

    :param shop_id: ID of the subhect shop.
    :param shops: Shop list to filter correct shop, so the name can be used in the "email".
    """
    shop_to_notify = find_shop(shop_id, shops)
    shop_name = shop_to_notify[1]
    is_shop_listed = shop_to_notify[2]
    if is_shop_listed:
        print(f'{shop_name} has used half their budget!')


def set_shop_offline(shop_id):
    """
    Given a shop ID, sets a shop as not listed.
    :param shop_id: ID of the shop with insufficient budget.
    :return: Number of rows affected.
    """
    update_query = """ UPDATE t_shops
                    SET a_online = %s
                    WHERE a_id = %s"""
    conn = None
    updated_rows = 0
    try:
        print(f'Unlisting shop with the ID {shop_id}.')
        conn = get_db_connection()
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        cur.execute(update_query, (False, shop_id))
        updated_rows = cur.rowcount
        conn.commit()
        cur.close()
    except (Exception, psycopg.DatabaseError) as error:
        print(f'Error: {error}')
    finally:
        if conn is not None:
            conn.close()
    return updated_rows


def handle_full_budget(shop_id, shops):
    """
    Given a shop with exceeding expenditure, notifies the shop and unlists it.

    :param shop_id: ID of the shop that exceeds its budget.
    :param shops: Shop list to filter correct shop, so the name can be used in the "email".
    """
    shop_to_notify = find_shop(shop_id, shops)
    shop_name = shop_to_notify[1]
    is_shop_listed = shop_to_notify[2]
    # Note that we could initially fetch only online shops, but I chose to do it here.
    if is_shop_listed:
        print(f'{shop_name} has used all their budget!')
        set_shop_offline(shop_id)


def process_records(records):
    """
    Using the records provided, triggers necessary actions.
    :param records: List of shop records to process.
    """
    # Since we are only interested in current month, lets get it first:
    current_rotation_date = datetime.today().date().replace(day=1)
    # print(current_rotation_date)
    print("Processing budget status of shops.")
    for budget in records["budgets"]:
        shop_id, budget_cycle, budget_max, budget_spent = budget
        if budget_cycle == current_rotation_date:
            if budget_spent < budget_max:
                if budget_spent >= budget_max / 2:
                    handle_half_budget(shop_id, records["shops"])
            else:
                handle_full_budget(shop_id, records["shops"])


if __name__ == "__main__":
    operation_records = fetch_records()
    process_records(operation_records)
