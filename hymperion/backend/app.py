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
        cursor = mysql.connection.cursor()
        query = "SELECT id, descripcion, ubicacion, fecha, status FROM OpenAI WHERE status = 'pendiente'"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        formatted_results = []
        for row in result:
            try:
                # Parseamos la descripción que contiene los datos JSON
                risk_data = json.loads(row[1])  
                formatted_result = {
                    "id": row[0],  
                    "risk_score": risk_data.get("risk_score"),
                    "risk_description": risk_data.get("risk_description"),
                    "risk_mitigation": risk_data.get("risk_mitigation"),
                    "risk_impact": risk_data.get("risk_impact"),
                    "ubicacion": row[2],
                    "fecha": row[3],
                    "status": row[4]
                }
                formatted_results.append(formatted_result)
            except json.JSONDecodeError as e:
                print(f"Error al decodificar JSON: {e} en la fila: {row[1]}")
        
        return jsonify(formatted_results)
    
    except Exception as e:
        print(f"Error en la consulta de la base de datos: {e}")
        return jsonify({"error": "Error al obtener los datos de la base de datos"}), 500


@app.route('/tickets/resueltos', methods=['GET'])
def obtener_tickets_resueltos():
    try:
        cursor = mysql.connection.cursor()
        query = "SELECT id, descripcion, ubicacion, fecha, status FROM OpenAI WHERE status = 'resuelto'"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        formatted_results = []
        for row in result:
            try:
                risk_data = json.loads(row[1])  
                formatted_result = {
                    "id": row[0],  
                    "risk_score": risk_data.get("risk_score"),
                    "risk_description": risk_data.get("risk_description"),
                    "risk_mitigation": risk_data.get("risk_mitigation"),
                    "risk_impact": risk_data.get("risk_impact"),
                    "ubicacion": row[2],
                    "fecha": row[3],
                    "status": row[4]
                }
                formatted_results.append(formatted_result)
            except json.JSONDecodeError as e:
                print(f"Error al decodificar JSON: {e} en la fila: {row[0]}")
        
        return jsonify(formatted_results)
    
    except Exception as e:
        print(f"Error en la consulta de la base de datos: {e}")
        return jsonify({"error": "Error al obtener los datos de la base de datos"}), 500

# tickets dinamicos por sede pendientes
@app.route('/tickets/pendientes/<string:sede>', methods=['GET'])
def obtener_tickets_pendientes_por_sede(sede):
    try:
        cursor = mysql.connection.cursor()
        # Filtrar por ubicación (sede) y estado resuelto
        query = "SELECT id, descripcion, ubicacion, fecha, status FROM OpenAI WHERE ubicacion = %s AND status = 'pendiente'"
        cursor.execute(query, (sede,))
        result = cursor.fetchall()
        cursor.close()

        formatted_results = []
        for row in result:
            try:
                risk_data = json.loads(row[1])  
                formatted_result = {
                    "id": row[0],  
                    "risk_score": risk_data.get("risk_score"),
                    "risk_description": risk_data.get("risk_description"),
                    "risk_mitigation": risk_data.get("risk_mitigation"),
                    "risk_impact": risk_data.get("risk_impact"),
                    "ubicacion": row[2],
                    "fecha": row[3],
                    "status": row[4]
                }
                formatted_results.append(formatted_result)
            except json.JSONDecodeError as e:
                print(f"Error al decodificar JSON: {e} en la fila: {row[0]}")
        
        return jsonify(formatted_results)
    
    except Exception as e:
        print(f"Error en la consulta de la base de datos: {e}")
        return jsonify({"error": "Error al obtener los datos de la base de datos"}), 500

    
# tickets dinamicos por sede resueltos
@app.route('/tickets/resueltos/<string:sede>', methods=['GET'])
def obtener_tickets_resueltos_por_sede(sede):
    try:
        cursor = mysql.connection.cursor()
        # Filtrar por ubicación (sede) y estado resuelto
        query = "SELECT id, descripcion, ubicacion, fecha, status FROM OpenAI WHERE ubicacion = %s AND status = 'resuelto'"
        cursor.execute(query, (sede,))
        result = cursor.fetchall()
        cursor.close()

        formatted_results = []
        for row in result:
            try:
                risk_data = json.loads(row[1])  
                formatted_result = {
                    "id": row[0],  
                    "risk_score": risk_data.get("risk_score"),
                    "risk_description": risk_data.get("risk_description"),
                    "risk_mitigation": risk_data.get("risk_mitigation"),
                    "risk_impact": risk_data.get("risk_impact"),
                    "ubicacion": row[2],
                    "fecha": row[3],
                    "status": row[4]
                }
                formatted_results.append(formatted_result)
            except json.JSONDecodeError as e:
                print(f"Error al decodificar JSON: {e} en la fila: {row[0]}")
        
        return jsonify(formatted_results)
    
    except Exception as e:
        print(f"Error en la consulta de la base de datos: {e}")
        return jsonify({"error": "Error al obtener los datos de la base de datos"}), 500

# Eliminar un ticket
@app.route('/tickets/<int:id>', methods=['DELETE'])
def eliminar_ticket(id):
    try:
        cursor = mysql.connection.cursor()
        query = "DELETE FROM OpenAI WHERE id = %s"
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
        query = "UPDATE OpenAI SET status = 'Resuelto' WHERE id = %s"
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
        query = "UPDATE OpenAI SET status = 'pendiente' WHERE id = %s"
        cursor.execute(query, (id,))
        mysql.connection.commit()
        cursor.close()

        return jsonify({"message": f"Ticket con id {id} marcado como pendiente"}), 200
    
    except Exception as e:
        print(f"Error al marcar el ticket como resuelto: {e}")
        return jsonify({"error": "Error al marcar el ticket como pendiente"}), 500



if __name__ == '__main__':
    app.run(port=5000, debug=True)
