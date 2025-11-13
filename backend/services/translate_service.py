from ultralytics import YOLO
import cv2
import numpy as np
from utils.braille_translator import braille_to_text

# Cargar modelo YOLOv8 entrenado
model = YOLO("backend/yolov8_model/best.pt")

def translate_image(image_file):
    # Leer imagen desde archivo en memoria
    img_array = np.frombuffer(image_file.read(), np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    # Ejecutar detección
    results = model(img)

    # Extraer las clases detectadas
    labels = []
    for r in results:
        for box in r.boxes:
            cls = int(box.cls)
            labels.append(model.names[cls])  # Obtener nombre de la clase

    # Traducir Braille a texto
    texto = braille_to_text(labels)
    return texto
