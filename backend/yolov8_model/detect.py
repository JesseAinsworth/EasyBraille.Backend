from ultralytics import YOLO
import cv2

# Cargar el modelo entrenado
model = YOLO("runs/train/braille_model/weights/best.pt")

# Ruta de imagen
image_path = "test_image.jpg"

# Ejecutar predicción
results = model(image_path, show=True, conf=0.5)

# Guardar resultados
for r in results:
    r.save(filename="output.jpg")

print("✅ Detección completada y guardada en output.jpg")
