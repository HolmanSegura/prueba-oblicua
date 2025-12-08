from flask import Flask, jsonify
from dotenv import load_dotenv

from productos import llamar_productos
from procesamiento import procesar_productos_csv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Crear la aplicación Flask
app = Flask(__name__)


@app.route("/ping", methods=["GET"])
def ping():
    """Endpoint de prueba para verificar que el microservicio está en línea."""
    return jsonify({"message": "Microservicio CSV en línea"}), 200


@app.route("/productos", methods=["GET"])
def traer_productos():
    """Endpoint para obtener la lista de productos desde la base de datos."""
    return llamar_productos()


@app.route("/procesar-productos-csv", methods=["POST"])
def productos_csv():
    """Endpoint para procesar un archivo CSV con productos."""
    return procesar_productos_csv()


if __name__ == "__main__":
    app.run(port=5100, debug=True)
