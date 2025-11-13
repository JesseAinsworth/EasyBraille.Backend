release: pip install --upgrade pip
web: gunicorn --bind 0.0.0.0:$PORT --workers 2 --worker-class sync backend.app:app
