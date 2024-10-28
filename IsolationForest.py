import pandas as pd
import mysql.connector
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import IsolationForest

def obtener_conexion():
    conexion = mysql.connector.connect(
        host="193.203.166.161",         
        user="u836958475_Laboratorios",      
        password="AegisHyperion123",  
        database="u836958475_CyberSecurity"  
    )
    return conexion

def log_repetido(conexion, log_id):
    query = f"SELECT COUNT(1) FROM IsolationForest WHERE id = {log_id}"
    cursor = conexion.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    return result[0] > 0

def obtener_logs(conexion, last_log_id):
    query = f"""
    SELECT *
    FROM Logs
    WHERE id > {last_log_id}
    """
    df = pd.read_sql(query, conexion)
    return df

def guardar_eventos_sospechosos(conexion, df):
    cursor = conexion.cursor()
    for _, row in df.iterrows():
        if log_repetido(conexion, row['id']):
            continue
        fecha_mysql = row['fecha'].strftime('%Y-%m-%d %H:%M:%S')
        
        insert_query = """
        INSERT INTO IsolationForest (id, descripcion, fecha, ip_origen, ip_destino, puerto, ubicacion, data_size)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (row['id'], row['descripcion'], fecha_mysql, row['ip_origen'], row['ip_destino'], row['puerto'], row['ubicacion'], row['data_size']))
    conexion.commit()

def cargar_y_preprocesar_logs(conexion, last_log_id):
    df = obtener_logs(conexion, last_log_id)
    
    if df.empty:
        return None, None, last_log_id
    
    df['fecha'] = pd.to_datetime(df['fecha'])
    df['hora'] = df['fecha'].dt.hour
    df['dia_semana'] = df['fecha'].dt.weekday  

    le_ip_privada = LabelEncoder()
    df['ip_privada_encoded'] = le_ip_privada.fit_transform(df['ip_privada'])

    le_ip_origen = LabelEncoder()
    df['ip_origen_encoded'] = le_ip_origen.fit_transform(df['ip_origen'])

    le_ip_destino = LabelEncoder()
    df['ip_destino_encoded'] = le_ip_destino.fit_transform(df['ip_destino'])

    le_ubicacion = LabelEncoder()
    df['ubicacion_encoded'] = le_ubicacion.fit_transform(df['ubicacion'])

    scaler = StandardScaler()
    df[['puerto', 'data_size', 'hora', 'dia_semana']] = scaler.fit_transform(df[['puerto', 'data_size', 'hora', 'dia_semana']])

    X = df[['ip_privada_encoded', 'ip_origen_encoded', 'ip_destino_encoded', 'ubicacion_encoded', 'puerto', 'data_size', 'hora', 'dia_semana']]

    return df, X, df['id'].max()

def entrenar_isolation_forest(X):
    model_if = IsolationForest(contamination=0.05, random_state=42)
    model_if.fit(X)
    return model_if

def predecir_eventos(df, X, model_if):
    df['anomaly'] = model_if.predict(X)
    df['sospechoso'] = df['anomaly'].apply(lambda x: 1 if x == -1 else 0)
    eventos_sospechosos = df[df['sospechoso'] == 1]
    return eventos_sospechosos

def ejecutar_modelo(model_if, conexion):
    last_log_id = 0

    df, X, last_log_id = cargar_y_preprocesar_logs(conexion, last_log_id)

    if df is not None:
        eventos_sospechosos = predecir_eventos(df, X, model_if)
        if not eventos_sospechosos.empty:
            guardar_eventos_sospechosos(conexion, eventos_sospechosos)

if __name__ == "__main__":
    conexion = obtener_conexion()
    df_inicial, X_inicial, last_log_id = cargar_y_preprocesar_logs(conexion, last_log_id=0)
    model_if = entrenar_isolation_forest(X_inicial)
    ejecutar_modelo(model_if, conexion)
    conexion.close()

