import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "braille-yolov8.pt")

# Configuración de estadísticas (puedes guardar en DB en el futuro)
STATS_FILE = os.path.join(BASE_DIR, "stats.json")
