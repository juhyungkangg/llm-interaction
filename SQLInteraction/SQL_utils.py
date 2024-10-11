import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import json
import tempfile
import ast


load_dotenv()

# Database connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_DATABASE')
        )
        if connection.is_connected():
            print("Connected to MySQL database.")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Function to check if data exists in the table
def execute_query(connection, query, params=None):
    cursor = connection.cursor(dictionary=True)  # dictionary=True to return rows as dicts

    try:
        if params is None:
            cursor.execute(query)
        else:
            cursor.execute(query, params)
        results = cursor.fetchall()

        if results:
            return results
        else:
            print(f"No data found.")
    except Error as e:
        print(f"Error while checking data: {e}")


def fetch_query(query, params=None):
    connection = create_connection()
    if connection:
        if params is None:
            results = execute_query(connection, query)
        else:
            results = execute_query(connection, query, params)
        connection.close()

        return results
    else:
        print(f"Connection to MySQL failed.")
        return None


def update_has_processed(data):
    connection = create_connection()
    if data is None:
        return False

    cursor = connection.cursor(dictionary=True)

    for table_name, rows in data.items():
        for row in rows:
            update_query = f"""
            UPDATE {table_name}
            SET has_processed = TRUE
            WHERE id = %s AND source_id = %s;
            """
            if row['has_processed']:
                cursor.execute(update_query, (row['id'], row['source_id']))
                connection.commit()
    print("Updated has_processed.")
    connection.close()


def update_has_filtered(data):
    connection = create_connection()
    if data is None:
        return False

    cursor = connection.cursor(dictionary=True)

    for table_name, rows in data.items():
        for row in rows:
            update_query = f"""
            UPDATE {table_name}
            SET has_filtered = TRUE
            WHERE id = %s AND source_id = %s;
            """
            if row['filter']:
                cursor.execute(update_query, (row['id'], row['source_id']))
                connection.commit()
    print("Updated has_filtered.")
    connection.close()


def update_signal(data):
    signal_query = """
    INSERT INTO signal_db (id, datetime, source_id, sentiment, reliability, relevance)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE 
        sentiment = VALUES(sentiment), 
        reliability = VALUES(reliability), 
        relevance = VALUES(relevance), 
        datetime = VALUES(datetime);
    """

    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    for table_name, rows in data.items():
        for row in rows:
            if isinstance(row['relevance'], dict):
                # Proceed if signal_data is a dictionary
                relevance_json = json.dumps(row['relevance'])
            else:
                print(f"Error: Expected a dictionary but got {type(row['relevance'])}")
                relevance_json = {}

            cursor.execute(signal_query, (
                row['id'],
                row['datetime'],
                row['source_id'],
                row['sentiment'],
                row['reliability'],
                relevance_json
            ))
            connection.commit()

    print("Updated signal.")

    # Close the cursor and connection
    cursor.close()
    connection.close()


