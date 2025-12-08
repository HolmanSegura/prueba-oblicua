from flask import jsonify
from db.base_datos import conexion_bd

def llamar_productos():
    """
    Obtiene la lista de productos ordenados por nombre.
    """
    conn = None
    cursor = None

    try:
        conn = conexion_bd()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM producto ORDER BY nombre"
        cursor.execute(query)
        productos = cursor.fetchall()

        return jsonify(productos), 200

    except Exception as e:
        return jsonify({"error": "Error al obtener productos"}), 500

    finally:
        if cursor is not None:
            try:
                cursor.close()
            except Exception:
                pass
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass
