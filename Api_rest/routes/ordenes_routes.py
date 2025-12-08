from flask import Blueprint
from services.ordenes_service import crear_orden

ordenes_bp = Blueprint("ordenes", __name__)

@ordenes_bp.route("/api/orden", methods=["POST"])
def crear_orden_endpoint():
    """Ruta para crear una nueva orden."""
    return crear_orden()
