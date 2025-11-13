# backend/app.py

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from braille_detector import detectar_braille

# --- Configuración ---
app = Flask(__name__)
CORS(app)  # permite peticiones desde otros puertos
TEMP_DIR = "temp"

# Crear carpeta temporal si no existe
os.makedirs(TEMP_DIR, exist_ok=True)

# --- Endpoint principal ---
@app.route("/api/braille-image", methods=["POST"])
def translate_braille():
    if "image" not in request.files:
        return jsonify({"error": "No se subió ninguna imagen"}), 400
    
    file = request.files["image"]
    file_path = os.path.join(TEMP_DIR, file.filename)
    file.save(file_path)

    try:
        texto = detectar_braille(file_path)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Borrar archivo temporal
        if os.path.exists(file_path):
            os.remove(file_path)

    return jsonify({"texto": texto})

# --- Ejecutar servidor ---
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
