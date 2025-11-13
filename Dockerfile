# Imagen base
FROM python:3.10-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar la app
COPY . .

# Exponer puerto
EXPOSE 8000

# Comando de inicio
CMD ["gunicorn", "--chdir", "backend", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "120", "app:app"]
