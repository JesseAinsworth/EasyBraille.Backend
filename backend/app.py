from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)

# ✅ CORS para tu dominio personalizado
CORS(app, resources={r"/api/*": {"origins": "https://www.easy-braille.com"}}, supports_credentials=True)

# ✅ Encabezados CORS para todas las respuestas
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "https://www.easy-braille.com"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return response

# ✅ Ruta raíz para verificar que el backend está activo
@app.route("/")
def index():
    return jsonify({"message": "EasyBraille backend activo"})

# ✅ Registro de usuario
@app.route("/api/auth/register", methods=["POST", "OPTIONS"])
def register():
    if request.method == "OPTIONS":
        return '', 200  # Preflight OK

    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Faltan campos"}), 400

        print(f"📥 Registro recibido: {email}")
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

# ✅ Inicio de sesión
@app.route("/api/auth/login", methods=["POST", "OPTIONS"])
def login():
    if request.method == "OPTIONS":
        return '', 200  # Preflight OK

    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Faltan campos"}), 400

        # Simulación de autenticación
        if email == "test@example.com" and password == "123456":
            return jsonify({
                "message": "Inicio de sesión exitoso",
                "user": {
                    "name": email.split("@")[0],
                    "email": email
                }
            }), 200
        else:
            return jsonify({"error": "Credenciales inválidas"}), 401

    except Exception as e:
        print(f"❌ Error en login: {e}")
        return jsonify({"error": "Error interno"}), 500

# ✅ Puedes agregar más rutas aquí (traducción Braille, historial, logout, etc.)

# ✅ Configuración para Railway y Gun
