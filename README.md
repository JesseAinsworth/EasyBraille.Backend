# EasyBraille - Backend

Backend API de EasyBraille construido con **Flask**, **Python 3**, **YOLOv8** y **OpenCV**.

## 🚀 Inicio Rápido

### Requisitos
- Python 3.8+
- pip

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/JesseAinsworth/EasyBraille-Backend.git
cd EasyBraille-Backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Ejecutar la Aplicación

```bash
# Desarrollo
python app.py

# O con Flask
flask run
```

El servidor estará disponible en `http://localhost:5000`

### Producción

```bash
./gunicorn_start.sh
```

## 📁 Estructura del Proyecto

```
backend/
├── app.py                 # Punto de entrada principal
├── config.py             # Configuración
├── braille_detector.py    # Detector de Braille
├── requirements.txt       # Dependencias
├── dataset/              # Datos de entrenamiento/validación
│   ├── train/
│   ├── valid/
│   └── test/
├── models/               # Modelos entrenados
│   └── best.pt           # Mejor modelo YOLOv8
├── services/             # Servicios de negocio
│   ├── translate_service.py
│   └── stats_service.py
├── utils/                # Utilidades
│   ├── braille_translator.py
│   └── image_utils.py
├── yolov8_model/         # Modelo YOLO
│   └── detect.py
└── Dockerfile            # Configuración Docker
```

## 🔌 Endpoints API

### Detección de Braille
- `POST /api/detect` - Detectar caracteres Braille en una imagen
- `POST /api/translate` - Traducir Braille a texto

### Estadísticas
- `GET /api/stats` - Obtener estadísticas

### Health Check
- `GET /health` - Verificar estado del servidor

## 📚 Tecnologías Principales

- **Framework**: Flask con Flask-CORS
- **Lenguaje**: Python 3
- **IA/ML**: YOLOv8 (Ultralytics)
- **Procesamiento de Imagen**: OpenCV, Pillow
- **Configuración**: PyYAML
- **Arrays Numéricos**: NumPy

## 🧠 Modelos IA

El proyecto utiliza **YOLOv8** para la detección de caracteres Braille.

### Entrenar Modelo

```bash
python train.py
```

### Evaluar Modelo

```bash
python eval_translation.py
```

## 🐳 Docker

```bash
# Construir imagen
docker build -f Dockerfile -t easybraille-backend .

# Ejecutar contenedor
docker run -p 5000:5000 easybraille-backend
```

## 🔐 Variables de Entorno

Crea un archivo `.env`:

```env
FLASK_ENV=development
FLASK_DEBUG=True
CORS_ORIGINS=http://localhost:3000
MODEL_PATH=./models/best.pt
```

## 📖 Documentación Adicional

- [Flask Docs](https://flask.palletsprojects.com)
- [YOLOv8 Docs](https://docs.ultralytics.com/)
- [OpenCV Docs](https://docs.opencv.org/)

## 📝 Licencia

Este proyecto es parte de EasyBraille.

## 👥 Contribuir

Las contribuciones son bienvenidas. Por favor, crea un fork, realiza tus cambios y envía un pull request.
