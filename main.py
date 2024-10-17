import time
import logging
import mysql.connector
from OpenAI import initialize_llm, analyze_row
from dbConnect import create_connection, check_new_rows, post_output, read_last_id_from_db, write_last_id_to_db

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    llm = initialize_llm()
    conn = create_connection()

    if conn is None:
        return  # Exit if connection could not be established

    cursor = conn.cursor()

    try:
        last_id = read_last_id_from_db(cursor)

        while True:
            new_rows = check_new_rows(cursor, last_id, "IsolationForest")

            if new_rows:
                logging.info(f"Found {len(new_rows)} new rows:")
                for row in new_rows:
                    """ROW: [ID, 'description', 'ubicacion', datetime.date[2024, 10, 17]]"""
                    logging.info(row)

                    # analysis_result_forest = 
                    # logging.info(f"Analysis Result: {analysis_result_forest}")
                    # post_output(conn, analysis_result_forest, "IsolationForest")

                    # Analyze the row using the LLM
                    analysis_result_openai = analyze_row(llm, row)
                    # analysis_result_openai = analyze_row(llm, analysis_result_forest)
                    logging.info(f"Analysis Result: {analysis_result_openai}")

                    # Post the analysis result to the database
                    post_output(conn, analysis_result_openai, "OpenAI")

                # Update last_id to the ID of the most recent row
                last_id = new_rows[-1][0]
                write_last_id_to_db(cursor, conn, last_id)
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
