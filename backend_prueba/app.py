from flask import Flask, jsonify
from inicio_sesion import login
from productos import llamar_productos
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "API en línea"}), 200

@app.route("/api/login", methods=["POST"])
def iniciar_sesion():
    return login()

@app.route("/api/productos", methods=["GET"])
def traer_productos():
    return llamar_productos()

if __name__ == "__main__":
    app.run(debug=True)
