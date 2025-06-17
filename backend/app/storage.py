import json
import os

def save_chunks(chunks, filename="processed.json", folder="data"):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)

def load_chunks(filename="processed.json", folder="data"):
    path = os.path.join(folder, filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
