#!/bin/bash
set -e
PORT=${PORT:-8080}
echo "Starting EasyBraille backend on port $PORT"
exec gunicorn --bind 0.0.0.0:${PORT} --workers 2 --worker-class sync backend.app:app
