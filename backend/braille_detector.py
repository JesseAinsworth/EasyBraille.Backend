# backend/braille_detector.py

from ultralytics import YOLO
from utils.braille_translator import braille_to_text
import os

# Ruta del modelo entrenado
MODEL_PATH = "yolov8_model/best.pt"  # relativa a backend/
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"No se encontró el modelo en {MODEL_PATH}")

model = YOLO(MODEL_PATH)

def detectar_braille(imagen_path):
    """
    Detecta símbolos Braille en una imagen y devuelve el texto traducido.
    """
    results = model(imagen_path)

    # Extraer etiquetas detectadas
    labels = []
    for r in results:
        for box in r.boxes:
            label_idx = int(box.cls[0])
            label_name = r.names[label_idx]  # Nombre del símbolo detectado
            labels.append(label_name)
    
    texto = braille_to_text(labels)
    return texto
