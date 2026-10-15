import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEXT_FOLDER = os.path.join(BASE_DIR, "output_text")
CHUNK_FOLDER = os.path.join(BASE_DIR, "chunks")

os.makedirs(CHUNK_FOLDER, exist_ok=True)


def chunk_text(text, chunk_size=500):

    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


def process_files():

    for file in os.listdir(TEXT_FOLDER):

        if file.endswith(".txt"):

            path = os.path.join(TEXT_FOLDER, file)

            with open(path, "r", encoding="utf-8") as f:
                text = f.read()

            chunks = chunk_text(text)

            for i, chunk in enumerate(chunks):

                chunk_file = f"{file[:-4]}_chunk{i}.txt"

                with open(os.path.join(CHUNK_FOLDER, chunk_file), "w", encoding="utf-8") as cf:
                    cf.write(chunk)

            print(f"Chunks created for {file}")


if __name__ == "__main__":
    process_files()