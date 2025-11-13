"""
backend/app.py - Flask app para Braille Detection
Optimizado para despliegue en Render
"""

import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

# Importar configuración
from config import CORS_ORIGINS, PORT, TEMP_DIR, ENVIRONMENT

# Importar detector
from braille_detector import detectar_braille

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear app
app = Flask(__name__)

# Configurar CORS
CORS(app, resources={
    r"/api/*": {
        "origins": CORS_ORIGINS,
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Crear carpeta temporal si no existe
os.makedirs(TEMP_DIR, exist_ok=True)

# ─────────────────────────────────────────────────────────
# ENDPOINTS
# ─────────────────────────────────────────────────────────

@app.route("/", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "service": "EasyBraille Backend",
        "environment": ENVIRONMENT
    }), 200


@app.route("/api/health", methods=["GET"])
def api_health():
    """API health check"""
    return jsonify({"status": "healthy"}), 200


@app.route("/api/braille-image", methods=["POST"])
def translate_braille():
    """
    Endpoint principal para detectar Braille en imágenes
    
    Espera: multipart/form-data con 'image'
    Retorna: JSON con el texto detectado
    """
    try:
        # Validar que hay imagen
        if "image" not in request.files:
            return jsonify({
                "error": "No se subió ninguna imagen",
                "code": "NO_IMAGE"
            }), 400

        file = request.files["image"]
        
        # Validar que el archivo no está vacío
        if file.filename == "":
            return jsonify({
                "error": "Nombre de archivo vacío",
                "code": "EMPTY_FILENAME"
            }), 400

        # Guardar archivo temporalmente
        file_path = os.path.join(TEMP_DIR, file.filename)
        file.save(file_path)
        
        logger.info(f"Imagen recibida: {file.filename}")

        try:
            # Detectar Braille
            texto = detectar_braille(file_path)
            
            logger.info(f"Detección exitosa: {len(texto)} caracteres")
            
            return jsonify({
                "texto": texto,
                "imagen": file.filename,
                "status": "success"
            }), 200

        except Exception as e:
            logger.error(f"Error en detección: {str(e)}")
            return jsonify({
                "error": "Error al detectar Braille",
                "details": str(e),
                "code": "DETECTION_ERROR"
            }), 500

        finally:
            # Eliminar archivo temporal
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Archivo temporal eliminado: {file.filename}")

    except Exception as e:
        logger.error(f"Error no esperado: {str(e)}")
        return jsonify({
            "error": "Error interno del servidor",
            "details": str(e),
            "code": "SERVER_ERROR"
        }), 500


# ─────────────────────────────────────────────────────────
# ERROR HANDLERS
# ─────────────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint no encontrado",
        "code": "NOT_FOUND"
    }), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "error": "Error interno del servidor",
        "code": "SERVER_ERROR"
    }), 500


# ─────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    if ENVIRONMENT == "development":
        # Desarrollo: usar Flask debug server
        app.run(
            host="0.0.0.0",
            port=PORT,
            debug=True,
            use_reloader=True
        )
    else:
        # Producción: usar Gunicorn (no ejecutar aquí)
        app.run(
            host="0.0.0.0",
            port=PORT,
            debug=False
        )
