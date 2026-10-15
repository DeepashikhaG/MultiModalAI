import os
import json
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

CHUNK_FOLDER = os.path.join(BASE_DIR, "chunks")
EMBED_FOLDER = os.path.join(BASE_DIR, "embeddings")
OUTPUT_FILE = os.path.join(EMBED_FOLDER, "embeddings.json")

os.makedirs(EMBED_FOLDER, exist_ok=True)

model = SentenceTransformer("all-MiniLM-L6-v2")

documents = []

for file in os.listdir(CHUNK_FOLDER):

    if file.endswith(".txt"):

        path = os.path.join(CHUNK_FOLDER, file)

        with open(path, "r", encoding="utf-8") as f:
            text = f.read().strip()

        if text == "":
            continue

        embedding = model.encode(text).tolist()

        # extract original pdf name
        pdf_name = file.split("_chunk")[0] + ".pdf"

        documents.append({
            "file_name": file,
            "pdf_name": pdf_name,
            "text": text,
            "embedding": embedding
        })

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(documents, f, indent=4)

print("Embeddings stored successfully.")