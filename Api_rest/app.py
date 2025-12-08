from flask import Flask, jsonify

from routes.auth_routes import auth_bp
from routes.productos_routes import productos_bp
from routes.ordenes_routes import ordenes_bp


def create_app():
    app = Flask(__name__)

    @app.route("/ping", methods=["GET"])
    def ping():
        """Endpoint de prueba para verificar que la API está en línea."""
        return jsonify({"message": "API en línea"}), 200

    app.register_blueprint(auth_bp)
    app.register_blueprint(productos_bp)
    app.register_blueprint(ordenes_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
