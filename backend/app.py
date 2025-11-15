from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os
import bcrypt
from datetime import datetime

# 1️⃣ Crear la instancia de Flask primero
app = Flask(__name__)

# 2️⃣ Configurar CORS
ALLOWED_ORIGIN = "https://www.easy-braille.com"
CORS(app, resources={r"/api/*": {"origins": ALLOWED_ORIGIN}}, supports_credentials=True)

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return response

# 3️⃣ Conexión a MongoDB Atlas
try:
    MONGO_URI = os.environ.get("MONGO_URI")
    if not MONGO_URI:
        raise Exception("MONGO_URI no está definido")

    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.server_info()
    db = client["easybraille"]
    usuarios = db["users"]
except Exception as e:
    print(f"❌ Error conectando a MongoDB: {e}")
    usuarios = None

# 4️⃣ Definir rutas DESPUÉS de crear `app`
@app.route("/")
def index():
    return jsonify({"message": "EasyBraille backend activo"})

@app.route("/api/auth/register", methods=["POST", "OPTIONS"])
def register():
    ...
    # tu lógica de registro aquí

@app.route("/api/auth/login", methods=["POST", "OPTIONS"])
def login():
    ...
    # tu lógica de login aquí

# 5️⃣ Configuración Railway/Gunicorn
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
