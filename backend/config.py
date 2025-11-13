"""
backend/config.py - Configuración para producción en Render
"""

import os
from datetime import timedelta

# Entorno
ENVIRONMENT = os.getenv('FLASK_ENV', 'development')
IS_PRODUCTION = ENVIRONMENT == 'production'

# Puerto
PORT = int(os.getenv('PORT', 8000))

# CORS Configuration
CORS_ORIGINS = [
    'http://localhost:3000',  # Frontend local
    'http://localhost:5000',  # Backend local
    'https://easybraille-frontend.onrender.com',  # Frontend en Render
    'https://easybraille-backend.onrender.com',   # Backend en Render
]

# Si está en producción, ser más restrictivo
if IS_PRODUCTION:
    CORS_ORIGINS = [
        'https://easybraille-frontend.onrender.com',
        'https://easybraille-backend.onrender.com',
    ]

# Timeout para uploads (10 minutos)
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB

# Logging
LOG_LEVEL = 'INFO' if IS_PRODUCTION else 'DEBUG'

# Modelo YOLO
MODEL_PATH = 'backend/models/best.pt'

# Directorio temporal
TEMP_DIR = os.getenv('TEMP_DIR', 'temp')

print(f'[CONFIG] Environment: {ENVIRONMENT}')
print(f'[CONFIG] Port: {PORT}')
print(f'[CONFIG] CORS Origins: {CORS_ORIGINS}')
