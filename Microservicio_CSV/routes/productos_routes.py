from flask import Blueprint
from services.productos_service import llamar_productos

productos_bp = Blueprint("productos", __name__)

@productos_bp.route("/productos", methods=["GET"])
def traer_productos():
    """Ruta para obtener la lista de productos."""
    return llamar_productos()
