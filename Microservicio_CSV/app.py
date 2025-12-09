from flask import Flask, jsonify
from dotenv import load_dotenv

from routes.productos_routes import productos_bp
from routes.csv_routes import csv_bp

# Cargar variables de entorno
load_dotenv()

# Crear la aplicación Flask
app = Flask(__name__)


@app.route("/ping", methods=["GET"])
def ping():
    """Endpoint de prueba para verificar que el microservicio está en línea."""
    return jsonify({"message": "Microservicio CSV en línea"}), 200


# Registrar blueprints
app.register_blueprint(productos_bp)
app.register_blueprint(csv_bp)


if __name__ == "__main__":
    app.run(port=5100, debug=True)
