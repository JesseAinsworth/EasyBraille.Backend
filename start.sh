#!/bin/bash
# Usa el puerto proporcionado por Railway, o 8000 si no existe
PORT=${PORT:-8000}
echo "Starting app on port $PORT"
exec gunicorn --bind 0.0.0.0:${PORT} --workers 2 --worker-class sync backend.app:app
