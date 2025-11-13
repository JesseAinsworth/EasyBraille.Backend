# Usar imagen oficial con las herramientas necesarias
FROM python:3.10-slim

WORKDIR /app

# Instalar solo dependencias de sistema críticas
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primero (para cache de Docker)
COPY requirements.txt .

# Instalar pip upgrade y luego dependencias
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar aplicación
COPY . .

EXPOSE 8000

# Comando de inicio
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "120", "backend.app:app"]
