# Imagen base ligera con Python 3.10
FROM python:3.10-slim

# Información del mantenedor
LABEL maintainer="maintainer@example.com"
LABEL description="Backend de EasyBraille - Flask con YOLOv8"

# Variables de entorno para producción
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV FLASK_ENV=production
ENV GUNICORN_WORKERS=2
ENV GUNICORN_TIMEOUT=120

# Render clona el repo en esta ruta
WORKDIR /opt/render/project/src

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copiar el archivo de dependencias
COPY requirements.txt ./

# Instalar dependencias de Python
# Usar binarios precompilados de PyTorch para CPU
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir -r requirements.txt

# Copiar todos los archivos del backend al contenedor
COPY . .

# Crear usuario no root por seguridad
RUN useradd --create-home --shell /bin/bash appuser \
    && chown -R appuser:appuser /opt/render/project/src
USER appuser

# Exponer el puerto Flask/Gunicorn
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Comando de ejecución (Gunicorn para producción)
CMD ["sh", "-c", "exec gunicorn backend.app:app -b 0.0.0.0:8000 --workers \ --timeout \ --log-level info"]
