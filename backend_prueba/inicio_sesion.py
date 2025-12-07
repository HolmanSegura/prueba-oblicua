from flask import request, jsonify
from base_datos import conexion_bd
from jwt_token import crear_token

def login():
    datos = request.get_json()

    correo = datos.get("email")
    contrasena = datos.get("password")

    if not correo or not contrasena:
        return jsonify({
            "exito": False,
            "token": None,
            "mensaje": "email y password son requeridos"
        }), 400

    conn = conexion_bd()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT * FROM usuario WHERE email = %s and password = %s;
    """

    cursor.execute(query, (correo, contrasena))
    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    if usuario is None:
        return jsonify({
            "exito": False,
            "token": None,
            "mensaje": "Credenciales inválidas"
        }), 401

    token = crear_token(usuario)

    usuario_datos = {
        "usuario_id": usuario["usuario_id"],
        "nombre": usuario["nombre"],
        "apellido": usuario["apellido"],
        "email": usuario["email"],
    }

    return jsonify({
        "exito": True,
        "token": token,
        "usuario": usuario_datos
    }), 200
