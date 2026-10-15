import json
import faiss
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

EMBEDDINGS_FILE = os.path.join(BASE_DIR, "embeddings", "embeddings.json")
VECTOR_DIR = os.path.join(BASE_DIR, "vectorstore")
INDEX_FILE = os.path.join(VECTOR_DIR, "faiss_index.bin")

# Create folder automatically
os.makedirs(VECTOR_DIR, exist_ok=True)

with open(EMBEDDINGS_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

embeddings = np.array(
    [item["embedding"] for item in data],
    dtype="float32"
)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

faiss.write_index(index, INDEX_FILE)

print("FAISS index created successfully.")
print("Saved to:", INDEX_FILE)