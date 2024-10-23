import time
import logging
import mysql.connector
from OpenAI import initialize_llm, analyze_row
from dbConnect import create_connection, check_new_rows, post_output, read_last_id_from_db, write_last_id_to_db
from IsolationForest import cargar_y_preprocesar_logs, entrenar_isolation_forest, predecir_eventos, guardar_eventos_sospechosos

# Configure logging
logging.basicConfig(level=print, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    llm = initialize_llm()
    conn = create_connection()

    if conn is None:
        return  # Exit if connection could not be established

    cursor = conn.cursor()

    try:
        last_Open_id = read_last_id_from_db(cursor, column="last_processed_id")
        last_IsolationForest_id = read_last_id_from_db(cursor, column="last_IsolationForest_id")

        while True:
            new_rows = check_new_rows(cursor, last_Open_id, "Logs")

            if new_rows:
                df, X = cargar_y_preprocesar_logs(conn, last_IsolationForest_id)
                print('cargado y preprocesado')
                model_if = entrenar_isolation_forest(X)
                print('entrenado')
                response = predecir_eventos(df, X, model_if)
                print('predecido')

                # Guardar eventos sospechosos
                if not response.empty:
                    guardar_eventos_sospechosos(conn, response)
                    print('Eventos sospechosos guardados')

                last_IsolationForest_id = df['id'].max()

                print(f"Found {len(new_rows)} new rows:")
                for row in new_rows:
                    print(row)

                    # Analyze the row using the LLM
                    analysis_result_openai = analyze_row(llm, row)
                    print(f"Analysis Result: {analysis_result_openai}")

                    # Post the analysis result to the database
                    post_output(conn, analysis_result_openai, "OpenAI")

                # Update last_id to the ID of the most recent row
                last_Open_id = new_rows[-1][0]
                write_last_id_to_db(cursor, conn, last_Open_id, last_IsolationForest_id)
            else:
                print("No new rows found.")

            time.sleep(10)  # Poll the database every 10 seconds

    except KeyboardInterrupt:
        print("Script terminated by user.")
    except mysql.connector.Error as err:
        logging.error(f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    main()

