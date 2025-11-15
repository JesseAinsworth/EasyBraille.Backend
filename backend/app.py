from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# CORS explícito para tu dominio
CORS(app, resources={r"/api/*": {"origins": "https://www.easy-braille.com"}}, supports_credentials=True)

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "https://www.easy-braille.com"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return response

# ✅ Nuevo endpoint de registro
@app.route("/api/auth/register", methods=["POST", "OPTIONS"])
def register():
    if request.method == "OPTIONS":
        return '', 200  # Respuesta para preflight CORS

    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Faltan campos"}), 400

        # Aquí iría la lógica real de registro (guardar en DB, etc.)
        print(f"📥 Registro recibido: {email}")

        return jsonify({"message": "Usuario registrado correctamente"}), 200

    except Exception as e:
        print(f"❌ Error en registro: {e}")
        return jsonify({"error": "Error interno"}), 500

if __name__ == "__main__":
    app.run(debug=False, port=8000)
