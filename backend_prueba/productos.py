from flask import jsonify
from base_datos import conexion_bd

def llamar_productos():
    conn = conexion_bd()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT * FROM producto ORDER BY nombre
    """
    cursor.execute(query)
    productos = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(productos), 200
