from flask import Blueprint
from services.auth_service import login

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/api/login", methods=["POST"])
def iniciar_sesion():
    """Ruta para iniciar sesión y obtener un token JWT."""
    return login()
