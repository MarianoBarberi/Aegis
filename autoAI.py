import mysql.connector
import time
import logging
import os
from langchain_openai import OpenAI
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

def initialize_llm(api_key=None, model="gpt-3.5-turbo-instruct", max_tokens=1000, temperature=0.0):
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY")

    llm = OpenAI(
        model=model,
        api_key=api_key,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return llm

def get_template():
    return """You are a cybersecurity risk analyst at a laboratory.
    You are tasked with analyzing the risks of the laboratory's infrastructure.
    The input is a log of the laboratory's network traffic.
    Analyze the risks of the laboratory's infrastructure and score the risks from 1 to 10, 
    where 1 is the lowest risk and 5 is the highest risk.
    The output should be only in this format and no other format is accepted:
    {{
        "risk_score": 3,
        "risk_description": "The laboratory's network traffic is not encrypted.",
        "risk_mitigation": "Encrypt the laboratory's network traffic.",
        "risk_impact": "If the laboratory's network traffic is not encrypted, sensitive data can be intercepted."
    }}
    """

def create_connection():
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

def check_new_rows(cursor, last_id):
    query = "SELECT * FROM IsolationForest WHERE id > %s ORDER BY id ASC"
    cursor.execute(query, (last_id,))
    return cursor.fetchall()

def analyze_row(llm, row):
    template = get_template()
    input_data = f"Network traffic log: {row[1]}"
    prompt = template.replace("The input is a log of the laboratory's network traffic.", input_data)
    
    response = llm(prompt)
    return response

def post_output(conn, response):
    try:
        cursor = conn.cursor()
        query = """
        INSERT INTO OpenAI (description)
        VALUES (%s)
        """
        data = (str(response),)
        cursor.execute(query, data)
        conn.commit()
        cursor.close()
        logging.info("Output successfully posted to the database.")
    except mysql.connector.Error as err:
        logging.error(f"Error posting output to the database: {err}")


def read_last_id(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return int(f.read().strip())
    return 0  # Default last_id if file does not exist

def write_last_id(file_path, last_id):
    with open(file_path, 'w') as f:
        f.write(str(last_id))

def main():
    last_id_file = "last_id.txt"  # File to store the last processed ID
    last_id = read_last_id(last_id_file)  # Read last processed ID from file
    llm = initialize_llm()
    conn = create_connection()

    if conn is None:
        return  # Exit if connection could not be established

    cursor = conn.cursor()

    try:
        while True:
            new_rows = check_new_rows(cursor, last_id)

            if new_rows:
                logging.info(f"Found {len(new_rows)} new rows:")
                for row in new_rows:
                    logging.info(row)

                    # Analyze the row using Langchain
                    analysis_result = analyze_row(llm, row)
                    logging.info(f"Analysis Result: {analysis_result}")

                    # Post the analysis result to the database
                    post_output(conn, analysis_result)

                # Update last_id to the ID of the most recent row and write to file
                last_id = new_rows[-1][0]
                write_last_id(last_id_file, last_id)
            else:
                logging.info("No new rows found.")

            time.sleep(10)  # Poll the database every 10 seconds

    except KeyboardInterrupt:
        logging.info("Script terminated by user.")
    except mysql.connector.Error as err:
        logging.error(f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()
        logging.info("Database connection closed.")

if __name__ == "__main__":
    main()
