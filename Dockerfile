FROM python:3.10-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Crear directorio de modelos si no existe
RUN mkdir -p backend/models

# Exponer puerto
EXPOSE 8000

# Variables de entorno
ENV FLASK_APP=backend.app:app
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Comando de inicio - optimizado para Render
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--worker-class", "sync", "--timeout", "120", "backend.app:app"]
