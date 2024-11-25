import time
import logging
from OpenAI import initialize_llm, analyze_row, create_rag_chain
from dbConnect import create_connection, check_new_rows, post_output, read_last_id_from_db, write_last_id_to_db
from IsolationForest import cargar_y_preprocesar_logs, entrenar_isolation_forest, ejecutar_modelo
import warnings
import re

# Configure logging
logging.basicConfig(level=print, format='%(asctime)s - %(levelname)s - %(message)s')
warnings.filterwarnings("ignore", message="pandas only supports SQLAlchemy connectable")

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
            new_rows = check_new_rows(cursor, last_IsolationForest_id, "Logs")

            if new_rows:
                print(f"Found {len(new_rows)} new rows:")
                df_inicial, X_inicial, last_IsolationForest_id = cargar_y_preprocesar_logs(conn, last_log_id=0)
                print('cargado y preprocesado')
                model_if = entrenar_isolation_forest(X_inicial)
                print('entrenado')
                ejecutar_modelo(model_if, conn)
                print('predecido')
            else:
                print("No new rows found.")

            new_rows2 = check_new_rows(cursor, last_Open_id, "IsolationForest")
            if new_rows2:
                print(f"Found new rows:")
                rag_chain = create_rag_chain(llm)
                for row in new_rows2:
                    print(row)

                    # Analyze the row using the LLM
                    analysis_result_openai, risk_score, risk_description, risk_mitigation, risk_impact = analyze_row(llm, row, rag_chain)
                    
                    print(analysis_result_openai["answer"])

                    match = re.search(r'\{(.*?)\}', analysis_result_openai['answer'], re.DOTALL)
                    if match:
                        analysis_result_openai['answer'] = match.group(0)
                    else:
                        analysis_result_openai['answer'] = "Error: No match found."

                    if not conn.is_connected():
                        conn.reconnect()

                    # Post the analysis result to the database
                    post_output(conn, analysis_result_openai["answer"], risk_score, risk_description, risk_mitigation, risk_impact, row[6], row[2] ,"OpenAI", idIsoFo=row[0])

                # Update last_id to the ID of the most recent row
                last_Open_id = new_rows2[-1][0]
                write_last_id_to_db(cursor, conn, last_Open_id, last_IsolationForest_id)
            else:
                print("No new rows found.")

            time.sleep(10)  # Poll the database every 10 seconds

    except KeyboardInterrupt:
        print("Script terminated by user.")
    finally:
        cursor.close()
        conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    main()

