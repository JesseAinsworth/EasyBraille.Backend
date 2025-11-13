# Dockerfile para backend Flask/FastAPI con YOLO
FROM python:3.10-slim

# Production-ready backend image for EasyBraille
LABEL maintainer="maintainer@example.com"

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV FLASK_ENV=production
ENV GUNICORN_WORKERS=3
# Increase default Gunicorn timeout to allow longer image processing (seconds)
ENV GUNICORN_TIMEOUT=300

WORKDIR /app

# Install system deps needed for some Python wheels (opencv, pillow, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
	build-essential \
	ca-certificates \
	libgl1 \
	libglib2.0-0 \
	&& rm -rf /var/lib/apt/lists/*

# Copy the repo-root requirements file into the image
COPY requirements.txt ./

# Upgrade pip, install CPU PyTorch wheel first, then install other Python requirements
RUN pip install --no-cache-dir --upgrade pip \
	&& pip install --no-cache-dir -f https://download.pytorch.org/whl/cpu/torch_stable.html torch torchvision \
	&& pip install --no-cache-dir -r requirements.txt \
	&& pip install --no-cache-dir gunicorn

# Copy backend sources into image (Dockerfile is located in backend/)
COPY . .

# Create a non-root user to run the app
RUN useradd --create-home --shell /bin/bash appuser \
	&& chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

# Use gunicorn for production; env vars control workers/timeout
CMD ["sh", "-c", "exec gunicorn app:app -b 0.0.0.0:5000 --workers ${GUNICORN_WORKERS} --timeout ${GUNICORN_TIMEOUT} --log-level info"]
