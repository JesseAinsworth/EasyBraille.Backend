import json
import os

STATS_FILE = "backend/stats.json"

def load_stats():
    if not os.path.exists(STATS_FILE):
        return {"total_translations": 0}
    with open(STATS_FILE, "r") as f:
        return json.load(f)

def save_stats(stats):
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f)

def increment_translations():
    stats = load_stats()
    stats["total_translations"] = stats.get("total_translations", 0) + 1
    save_stats(stats)
