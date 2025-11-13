# Imagen base ligera con Python 3.10
FROM python:3.10-slim

# Información del mantenedor
LABEL maintainer="maintainer@example.com"
LABEL description="Backend de EasyBraille - Flask con YOLOv8 y MongoDB"

# Variables de entorno para producción
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV FLASK_ENV=production
ENV GUNICORN_WORKERS=3
ENV GUNICORN_TIMEOUT=120

# Render clona el repo en esta ruta
WORKDIR /opt/render/project/src

# Instalar dependencias del sistema necesarias para OpenCV, Pillow, etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copiar el archivo de dependencias
COPY requirements.txt ./

# Instalar dependencias de Python (incluyendo PyTorch CPU)
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -f https://download.pytorch.org/whl/cpu/torch_stable.html torch torchvision \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn

# Copiar todos los archivos del backend al contenedor
COPY . .

# Crear usuario no root por seguridad
RUN useradd --create-home --shell /bin/bash appuser \
    && chown -R appuser:appuser /opt/render/project/src
USER appuser

# Exponer el puerto Flask/Gunicorn
EXPOSE 5000

# Comando de ejecución (Gunicorn para producción)
CMD ["sh", "-c", "exec gunicorn app:app -b 0.0.0.0:5000 --workers ${GUNICORN_WORKERS} --timeout ${GUNICORN_TIMEOUT} --log-level info"]
