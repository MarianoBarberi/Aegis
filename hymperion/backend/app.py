import json
from flask import Flask, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = '193.203.166.161'
app.config['MYSQL_USER'] = 'u836958475_Laboratorios'
app.config['MYSQL_PASSWORD'] = 'AegisHyperion123'
app.config['MYSQL_DB'] = 'u836958475_CyberSecurity'

CORS(app)
mysql = MySQL(app)

@app.route('/')
def index():
    return jsonify({"message": "API is working!"})  # Respuesta JSON

@app.route('/tickets/pendientes', methods=['GET'])
def obtener_tickets_pendientes():
    try:
        # Use a context manager for cursor, which ensures immediate cleanup
        with mysql.connection.cursor() as cursor:
            cursor.execute("CALL GetPendingEvents()")
            # Retrieve results in a single call for efficiency
            result = cursor.fetchall()

        # Process rows directly into a list of dictionaries
        formatted_results = [
            {
                "id": row[0],  
                "risk_score": row[1],
                "risk_description": row[2],
                "risk_mitigation": row[3],
                "risk_impact": row[4],
                "status": row[5],
                "evento": row[6],
                "fecha": row[7],
                "ubicacion": row[8],
                "puerto": row[9]
            } for row in result
        ]

        return jsonify(formatted_results)
    
    except Exception as e:
        print(f"Error en la consulta de la base de datos: {e}")
        return jsonify({"error": "Error al obtener los datos de la base de datos"}), 500

@app.route('/tickets/resueltos', methods=['GET'])
def obtener_tickets_resueltos():
    try:
        # Using a context manager for the cursor to ensure it closes immediately after use
        with mysql.connection.cursor() as cursor:
            cursor.execute("CALL GetResolvedEvents()")
            result = cursor.fetchall()

        # Process each row into a dictionary using list comprehension
        formatted_results = [
            {
                "id": row[0],                # id
                "risk_score": row[1],         # risk_score
                "risk_description": row[2],   # risk_description
                "risk_mitigation": row[3],    # risk_mitigation
                "risk_impact": row[4],        # risk_impact
                "status": row[5],             # status
                "evento": row[6],             # evento
                "fecha": row[7],              # fecha
                "ubicacion": row[8],          # ubicacion
                "puerto": row[9]              # puerto
            } for row in result
        ]

        return jsonify(formatted_results)

    except Exception as e:
        print(f"Error en la consulta de la base de datos: {e}")
        return jsonify({"error": "Error al obtener los datos de la base de datos"}), 500

@app.route('/tickets/pendientes/<string:sede>', methods=['GET'])
def obtener_tickets_pendientes_por_sede(sede):
    try:
        # Use a context manager to ensure the cursor closes immediately after use
        with mysql.connection.cursor() as cursor:
            # Call the stored procedure with the location (sede) parameter
            query = "CALL GetPendingEventsByUbi(%s)"
            cursor.execute(query, (sede,))
            result = cursor.fetchall()

        # Convert each row into a dictionary using list comprehension
        formatted_results = [
            {
                "id": row[0],                # id
                "risk_score": row[1],         # risk_score
                "risk_description": row[2],   # risk_description
                "risk_mitigation": row[3],    # risk_mitigation
                "risk_impact": row[4],        # risk_impact
                "status": row[5],             # status
                "evento": row[6],             # evento
                "fecha": row[7],              # fecha
                "ubicacion": row[8],          # ubicacion
                "puerto": row[9]              # puerto
            } for row in result
        ]

        return jsonify(formatted_results)

    except Exception as e:
        print(f"Error en la consulta de la base de datos: {e}")
        return jsonify({"error": "Error al obtener los datos de la base de datos"}), 500

    
# tickets dinamicos por sede resueltos
@app.route('/tickets/resueltos/<string:sede>', methods=['GET'])
def obtener_tickets_resueltos_por_sede(sede):
    try:
        # Use a context manager to ensure the cursor closes immediately after use
        with mysql.connection.cursor() as cursor:
            # Call the stored procedure with the location (sede) parameter
            query = "CALL GetResolvedEventsByUbi(%s)"
            cursor.execute(query, (sede,))
            result = cursor.fetchall()

        # Convert each row into a dictionary using list comprehension
        formatted_results = [
            {
                "id": row[0],                # id
                "risk_score": row[1],         # risk_score
                "risk_description": row[2],   # risk_description
                "risk_mitigation": row[3],    # risk_mitigation
                "risk_impact": row[4],        # risk_impact
                "status": row[5],             # status
                "evento": row[6],             # evento
                "fecha": row[7],              # fecha
                "ubicacion": row[8],          # ubicacion
                "puerto": row[9]              # puerto
            } for row in result
        ]
        
        return jsonify(formatted_results)
    
    except Exception as e:
        print(f"Error en la consulta de la base de datos: {e}")
        return jsonify({"error": "Error al obtener los datos de la base de datos"}), 500

# Eliminar un ticket
@app.route('/tickets/<int:id>', methods=['DELETE'])
def eliminar_ticket(id):
    try:
        cursor = mysql.connection.cursor()
        query = "CALL DeleteFromOpenAI(%s)"
        cursor.execute(query, (id,))
        mysql.connection.commit()
        cursor.close()

        return jsonify({"message": f"Ticket con id {id} eliminado exitosamente"}), 200
    
    except Exception as e:
        print(f"Error al eliminar el ticket: {e}")
        return jsonify({"error": "Error al eliminar el ticket"}), 500

# Marcar un ticket como resuelto
@app.route('/tickets/<int:id>/resuelto', methods=['PUT'])
def marcar_ticket_resuelto(id):
    try:
        cursor = mysql.connection.cursor()
        query = "CALL SetStatusResuelto(%s)"
        cursor.execute(query, (id,))
        mysql.connection.commit()
        cursor.close()

        return jsonify({"message": f"Ticket con id {id} marcado como resuelto"}), 200
    
    except Exception as e:
        print(f"Error al marcar el ticket como resuelto: {e}")
        return jsonify({"error": "Error al marcar el ticket como resuelto"}), 500

# Marcar un ticket como pendiente
@app.route('/tickets/<int:id>/pendiente', methods=['PUT'])
def marcar_ticket_pendiente(id):
    try:
        cursor = mysql.connection.cursor()
        query = "CALL SetStatusPendiente(%s)"
        cursor.execute(query, (id,))
        mysql.connection.commit()
        cursor.close()

        return jsonify({"message": f"Ticket con id {id} marcado como pendiente"}), 200
    
    except Exception as e:
        print(f"Error al marcar el ticket como resuelto: {e}")
        return jsonify({"error": "Error al marcar el ticket como pendiente"}), 500



if __name__ == '__main__':
    app.run(port=5000, debug=True)
