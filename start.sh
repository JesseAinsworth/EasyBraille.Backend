#!/bin/bash
PORT=${PORT:-8000}
exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --worker-class sync backend.app:app
