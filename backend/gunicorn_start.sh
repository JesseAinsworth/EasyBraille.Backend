#!/bin/sh
# Simple entrypoint wrapper that runs gunicorn with env-configurable settings.
set -e

: ${GUNICORN_WORKERS:=3}
: ${GUNICORN_TIMEOUT:=120}

echo "Starting gunicorn with ${GUNICORN_WORKERS} workers and timeout ${GUNICORN_TIMEOUT}"
exec gunicorn app:app -b 0.0.0.0:5000 --workers ${GUNICORN_WORKERS} --timeout ${GUNICORN_TIMEOUT} --log-level info
