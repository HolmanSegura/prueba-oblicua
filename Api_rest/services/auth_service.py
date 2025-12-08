from flask import request, jsonify
from db.base_datos import conexion_bd
from utils.jwt_token import crear_token

def _respuesta_login(exito, mensaje, status, token=None, usuario=None):
    """
    Construye la respuesta estándar del endpoint de login.
    """
    cuerpo = {
        "exito": exito,
        "mensaje": mensaje,
        "token": token,
    }
    if usuario is not None:
        cuerpo["usuario"] = usuario
    return jsonify(cuerpo), status


def login():
    """
    Endpoint que autentica a un usuario por email y password
    y devuelve un token JWT en caso de éxito.
    """
    datos = request.get_json(silent=True) or {}

    correo = datos.get("email")
    contrasena = datos.get("password")

    # Validar que se proporcionen email y password
    if not correo or not contrasena:
        return _respuesta_login(
            exito=False,
            mensaje="email y password son requeridos",
            status=400,
            token=None,
        )

    conn = None
    cursor = None

    try:
        # Conexión a la base de datos y consulta de usuario
        conn = conexion_bd()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM usuario WHERE email = %s AND password = %s"
        cursor.execute(query, (correo, contrasena))
        usuario = cursor.fetchone()

        # Validar credenciales del usuario
        if usuario is None:
            return _respuesta_login(
                exito=False,
                mensaje="Credenciales inválidas",
                status=401,
                token=None,
            )

        # Generar token JWT y devolver respuesta exitosa
        token = crear_token(usuario)

        usuario_datos = {
            "nombre": usuario["nombre"],
            "apellido": usuario["apellido"],
            "usuario_id": usuario["usuario_id"]
        }

        return _respuesta_login(
            exito=True,
            mensaje="Login exitoso",
            status=200,
            token=token,
            usuario=usuario_datos,
        )

    except Exception:
        # Manejar errores inesperados en el proceso de login
        return _respuesta_login(
            exito=False,
            mensaje="Error interno en el servidor",
            status=500,
            token=None,
        )

    finally:
        # Cerrar recursos de base de datos
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()