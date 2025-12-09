from flask import Blueprint
from services.procesamiento_service import procesar_productos_csv

csv_bp = Blueprint("csv", __name__)


@csv_bp.route("/procesar-productos-csv", methods=["POST"])
def procesar_csv():
    """Endpoint para procesar un archivo CSV y cargar productos a la BD."""
    return procesar_productos_csv()
