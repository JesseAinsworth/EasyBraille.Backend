
Despliegue del backend EasyBraille

Este documento resume pasos y recomendaciones para desplegar el backend en EC2 (con Docker) y en Elastic Beanstalk.

Requisitos previos
- Cuenta AWS con permisos para EC2 / Elastic Beanstalk
- (Recomendado) Un bucket S3 para almacenar pesos de modelo grandes (no incluir checkpoints en el repo)
- Docker instalado para despliegues basados en contenedores

Contenido incluido
- `Dockerfile` — imagen de producción (gunicorn, usuario no root, dependencias del sistema)
- `Procfile` — para Elastic Beanstalk (plataforma Python) si no se usa Docker
- `gunicorn_start.sh` — wrapper opcional para iniciar gunicorn
- `.gitignore` — patrones recomendados (excluye `dataset/`, `temp/`, imágenes, etc.)

Recomendaciones generales
- No incluya checkpoints pesados en el repo. Suba pesos a S3 y descárguelos en tiempo de arranque o use EFS.
- Use variables de entorno para configurar el número de workers, timeout y la URL del modelo.
- Para rendimiento con YOLO en producción considere instancias con GPU. Para despliegue en CPU, use las ruedas oficiales de PyTorch CPU (el Dockerfile ya instala la versión CPU por defecto).

Despliegue en EC2 (Docker)
1) Construir la imagen localmente:

```bash
docker build -t easybraille-backend:latest backend/
```

2) Ejecutar la imagen en la instancia EC2 (ejemplo):

```bash
docker run -d --name easybraille-backend -p 5000:5000 \
  -e GUNICORN_WORKERS=3 -e GUNICORN_TIMEOUT=120 \
  -e MODEL_S3_PATH="s3://my-bucket/path/to/model.pt" \
  easybraille-backend:latest
```

3) (Opcional) Crear un archivo systemd para gestionar el contenedor (ejemplo):

```ini
[Unit]
Description=EasyBraille backend (Docker)
After=docker.service

[Service]
Restart=always
ExecStart=/usr/bin/docker run --rm --name easybraille-backend -p 5000:5000 \
  -e GUNICORN_WORKERS=3 -e GUNICORN_TIMEOUT=120 easybraille-backend:latest
ExecStop=/usr/bin/docker stop easybraille-backend

[Install]
WantedBy=multi-user.target
```

Elastic Beanstalk
- Opción A (usando Docker): Elastic Beanstalk puede desplegar una sola aplicación Docker utilizando el `Dockerfile` en la raíz del paquete.
  - Empaqueta el contenido del backend (Dockerfile incluido) y desplegar en EB como aplicación Docker.
  - EB construirá la imagen usando el Dockerfile, por lo que es conveniente que el Dockerfile sea autosuficiente (como el incluido).

- Opción B (usando plataforma Python): use `Procfile` y `requirements.txt`. En este caso EB desplegará en una VM EC2 y ejecutará `gunicorn`.

Comandos EB (ejemplo usando la CLI):

```bash
# crear aplicación y ambiente (ejemplo: plataforma Docker)
eb init -p docker easybraille-backend
eb create easybraille-prod --single
eb deploy
```

Notas sobre dependencias y tamaño de la imagen
- Las dependencias de `ultralytics` y `torch` son grandes. Para builds reproducibles, considere fijar versiones en `requirements.txt`.
- Para despliegues en CPU, usamos el índice de PyTorch CPU en el Dockerfile. Para GPU en EC2, reconfigure la instalación de torch para la versión CUDA apropiada y utilice instancias con drivers NVIDIA y AMI compatibles.

Variables de entorno sugeridas
- MODEL_PATH: ruta local al fichero del modelo (si lo descarga desde S3, colóquelo aquí después de descargarlo)
- MODEL_S3_PATH: ruta S3 para descargar el fichero en el arranque
- GUNICORN_WORKERS, GUNICORN_TIMEOUT

Ejemplo de flujo seguro para modelos grandes
1. Subir `best.pt` a S3.
2. En arranque del contenedor, el entrypoint descarga el fichero desde S3 a `/app/models/best.pt`.
3. La app carga el modelo desde `/app/models/best.pt`.

Si quieres, puedo añadir un pequeño script `bootstrap_model.py` que descarga desde S3 si `MODEL_S3_PATH` está presente.
