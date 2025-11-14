from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# CORS explícito para permitir solicitudes desde tu dominio web
CORS(app, resources={r"/api/*": {"origins": "https://www.easy-braille.com"}}, supports_credentials=True)

# También puedes usar "*" si estás en desarrollo:
# CORS(app, resources={r"/api/*": {"origins": "*"}})

# Agregar encabezados manuales para OPTIONS si es necesario
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "https://www.easy-braille.com"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return response
