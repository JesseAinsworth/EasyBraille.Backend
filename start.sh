#!/bin/bash
set -e  # Para que falle si algo va mal

# Mostrar valor real del puerto
echo "Valor de PORT: $PORT"

# Asegurarse de que sea un número
if ! [[ "$PORT" =~ ^[0-9]+$ ]]; then
  echo "PORT inválido: $PORT — usando 8000 por defecto"
  PORT=8000
fi

exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --worker-class sync backend.app:app
