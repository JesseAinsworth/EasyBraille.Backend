import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS

# Asegurarse de que el módulo backend sea accesible
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from braille_detector import detectar_braille
except ImportError as e:
    print(f"Error importando braille_detector: {e}")

    def detectar_braille(path):
        return "Error: Modelo no disponible"

# Configuración Flask
app = Flask(__name__)
CORS(app)

TEMP_DIR = os.path.join(os.path.dirname(__file__), "temp")
os.makedirs(TEMP_DIR, exist_ok=True)

# Health checks
@app.route("/", methods=["GET"])
def root():
    return jsonify({
        "status": "ok",
        "service": "EasyBraille Backend",
        "environment": os.getenv("FLASK_ENV", "production")
    }), 200

@app.route("/api/health", methods=["GET"])
def api_health():
    return jsonify({"status": "healthy"}), 200

# Endpoint principal
@app.route("/api/braille-image", methods=["POST"])
def translate_braille():
    if "image" not in request.files:
        return jsonify({"error": "No se subió ninguna imagen"}), 400

    file = request.files["image"]
    file_path = os.path.join(TEMP_DIR, file.filename)
    file.save(file_path)

    try:
        texto = detectar_braille(file_path)
        return jsonify({"texto": texto, "status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)
