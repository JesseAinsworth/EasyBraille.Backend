from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import os
import bcrypt
import bson

# 1️⃣ Inicializar Flask
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

    print(f"🔗 Conectando a MongoDB Atlas...")
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.server_info()  # fuerza verificación
    db = client["easybraille"]
    usuarios = db["users"]
except Exception as e:
    print(f"❌ Error conectando a MongoDB: {e}")
    usuarios = None

# 4️⃣ Ruta raíz
@app.route("/")
def index():
    return jsonify({"message": "EasyBraille backend activo"})

# 5️⃣ Registro de usuario
@app.route("/api/auth/register", methods=["POST", "OPTIONS"])
def register():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    if usuarios is None:
        return jsonify({"error": "Base de datos no disponible"}), 500

    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Formato inválido"}), 400

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Faltan campos"}), 400

        if usuarios.find_one({"email": email}):
            return jsonify({"error": "El usuario ya existe"}), 409

        hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        usuarios.insert_one({
            "email": email,
            "password": hashed_pw.decode(),  # guardar como string
            "name": email.split("@")[0],
            "role": "user",
            "isActive": True,
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        })

        print(f"✅ Usuario registrado: {email}")
        return jsonify({
            "message": "Usuario registrado correctamente",
            "user": {
                "name": email.split("@")[0],
                "email": email
            }
        }), 200

    except Exception as e:
        print(f"❌ Error en registro: {e}")
        return jsonify({"error": "Error interno"}), 500

# 6️⃣ Inicio de sesión
@app.route("/api/auth/login", methods=["POST", "OPTIONS"])
def login():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    if usuarios is None:
        return jsonify({"error": "Base de datos no disponible"}), 500

    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Formato inválido"}), 400

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Faltan campos"}), 400

        user = usuarios.find_one({"email": email})
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404

        stored_pw = user["password"]

        # Manejo flexible: string o Binary
        if isinstance(stored_pw, bson.binary.Binary):
            stored_pw = stored_pw.decode()
        elif isinstance(stored_pw, bytes):
            stored_pw = stored_pw.decode()

        if bcrypt.checkpw(password.encode("utf-8"), stored_pw.encode("utf-8")):
            print(f"✅ Usuario autenticado: {email}")
            return jsonify({
                "message": "Inicio de sesión exitoso",
                "user": {
                    "name": user["name"],
                    "email": user["email"],
                    "role": user.get("role", "user"),
                    "isActive": user.get("isActive", True)
                }
            }), 200
        else:
            return jsonify({"error": "Credenciales inválidas"}), 401

    except Exception as e:
        print(f"❌ Error en login: {e}")
        return jsonify({"error": "Error interno"}), 500

# 7️⃣ Configuración Railway/Gunicorn
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
