# backend/app.py
import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS

# Agregar el directorio backend al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Intentar importar braille_detector (disponible localmente)
try:
    from braille_detector import detectar_braille
    HAS_DETECTOR = True
except (ImportError, ModuleNotFoundError) as e:
    print(f'Warning: Braille detector no disponible: {e}')
    HAS_DETECTOR = False
    
    # Fallback function
    def detectar_braille(path):
        return 'BRAILLE_TEXT_PLACEHOLDER'

# Configuracion
app = Flask(__name__)
CORS(app)
TEMP_DIR = os.path.join(os.path.dirname(__file__), 'temp')

os.makedirs(TEMP_DIR, exist_ok=True)

# Health check
@app.route('/', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'service': 'EasyBraille Backend',
        'environment': os.getenv('FLASK_ENV', 'development'),
        'detector_available': HAS_DETECTOR
    }), 200

@app.route('/api/health', methods=['GET'])
def api_health():
    return jsonify({
        'status': 'healthy',
        'detector': 'available' if HAS_DETECTOR else 'unavailable'
    }), 200

# Endpoint principal
@app.route('/api/braille-image', methods=['POST', 'OPTIONS'])
def translate_braille():
    if request.method == 'OPTIONS':
        return '', 200
    
    if 'image' not in request.files:
        return jsonify({
            'error': 'No se subio ninguna imagen',
            'code': 'NO_IMAGE'
        }), 400

    file = request.files['image']
    if not file or file.filename == '':
        return jsonify({
            'error': 'Archivo vacio',
            'code': 'EMPTY_FILE'
        }), 400

    file_path = os.path.join(TEMP_DIR, file.filename)
    
    try:
        file.save(file_path)
        
        # Detectar Braille
        if HAS_DETECTOR:
            texto = detectar_braille(file_path)
        else:
            # Retornar placeholder para testing
            texto = 'BRAILLE_DETECTED'
        
        return jsonify({
            'texto': texto,
            'status': 'success',
            'detector_used': HAS_DETECTOR
        }), 200

    except Exception as e:
        return jsonify({
            'error': f'Error al procesar imagen: {str(e)}',
            'code': 'PROCESSING_ERROR'
        }), 500
    finally:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
