import pandas as pd
import time
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import IsolationForest
from dbConnect import read_all_from_table


def cargar_y_preprocesar_logs(conexion):
    cursor = conexion.cursor()
    df = read_all_from_table(conexion, cursor, 'Logs')
    cursor.close()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hora'] = df['timestamp'].dt.hour
    df['dia_semana'] = df['timestamp'].dt.weekday  

    le_ip = LabelEncoder()
    df['ip_origen_encoded'] = le_ip.fit_transform(df['ip_origen'])

    scaler = StandardScaler()
    df[['puerto_destino', 'hora', 'dia_semana']] = scaler.fit_transform(df[['puerto_destino', 'hora', 'dia_semana']])

    X = df[['ip_origen_encoded', 'puerto_destino', 'hora', 'dia_semana']]

    return df, X

def entrenar_isolation_forest(X):
    model_if = IsolationForest(contamination=0.05, random_state=42)
    model_if.fit(X)
    return model_if


def predecir_eventos(df, X, model_if):
    df['anomaly'] = model_if.predict(X)

    df['sospechoso'] = df['anomaly'].apply(lambda x: 1 if x == -1 else 0)

    eventos_sospechosos = df[df['sospechoso'] == 1]

    if not eventos_sospechosos.empty:
        print(f"Se encontraron {len(eventos_sospechosos)} eventos sospechosos:")
        print(eventos_sospechosos[['timestamp', 'ip_origen', 'puerto_destino', 'sospechoso']])
        # Modificar
    else:
        print("No se encontraron eventos sospechosos.")
    
    return eventos_sospechosos

def ejecutar_modelo(model_if):
    while True:
        file_path = ''
        df, X = cargar_y_preprocesar_logs(file_path)

        predecir_eventos(df, X, model_if)

        #  60 segundos antes de procesar nuevos logs
        time.sleep(60)  

if __name__ == "__main__":

    file_path_inicial = ''
    df_inicial, X_inicial = cargar_y_preprocesar_logs(file_path_inicial)
    model_if = entrenar_isolation_forest(X_inicial)

    ejecutar_modelo(model_if)

