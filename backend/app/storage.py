import json
import os
import faiss

def load_chunks(filename="processed.json", folder="data"):
    path = os.path.join(folder, filename)
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        raise FileNotFoundError("Processed chunks not found or file is empty.")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_chunks(chunks, filename="processed.json", folder="data"):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)

def save_index(index, path="data/index.faiss"):
    faiss.write_index(index, path)

def load_index(path="data/index.faiss"):
    return faiss.read_index(path)
