release: pip install --upgrade pip
web: gunicorn --chdir backend --bind 0.0.0.0:$PORT --workers 2 --worker-class sync app:app
