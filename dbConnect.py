import mysql.connector
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_connection():
    """Creates and returns a MySQL database connection."""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        return conn
    except mysql.connector.Error as err:
        logging.error(f"Error: {err}")
        return None

def check_new_rows(cursor, last_id, table_name):
    """Checks for new rows in the Logs table."""
    query = f"SELECT * FROM {table_name} WHERE id > %s ORDER BY id ASC"
    cursor.execute(query, (last_id,))
    return cursor.fetchall()

def post_output(conn, response, table_name):
    """Posts the analysis result to the database."""
    try:
        cursor = conn.cursor()
        query = f"""
        INSERT INTO {table_name} (description)
        VALUES (%s)
        """
        data = (str(response),)
        cursor.execute(query, data)
        conn.commit()
        cursor.close()
        logging.info("Output successfully posted to the database.")
    except mysql.connector.Error as err:
        logging.error(f"Error posting output to the database: {err}")

def read_last_id_from_db(cursor, column):
    """Reads the last processed ID from the database."""
    query = f"SELECT {column} FROM LastId ORDER BY id DESC LIMIT 1"
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
        return result[0]
    return 0 

def write_last_id_to_db(cursor, conn, last_id):
    """Writes the last processed ID to the database."""
    query = "INSERT INTO LastId (last_processed_id) VALUES (%s)"
    cursor.execute(query, (last_id,))
    conn.commit()
