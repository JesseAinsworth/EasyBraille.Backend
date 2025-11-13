# Usa una imagen base ligera
FROM python:3.10-slim

# Define el directorio de trabajo
WORKDIR /app

# Instala dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 libglib2.0-0 && rm -rf /var/lib/apt/lists/*

# Copia los archivos necesarios
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el backend
COPY backend ./backend

# Copia el script de inicio
COPY start.sh .

# Da permisos de ejecución
RUN chmod +x start.sh

# Usa el script de inicio
CMD ["./start.sh"]
