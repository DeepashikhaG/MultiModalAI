'''import pypdf
def pdf_to_text(pdf_path="..\\data\\pdf\\MultiModal_synopsis.pdf"):
    with open(pdf_path, "rb") as file:
        pdf = pypdf.PdfReader(file)
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text
print(pdf_to_text())'''

import os
import pdfplumber

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

PDF_FOLDER = os.path.join(BASE_DIR, "data", "pdf")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "output_text")

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def extract_pdf_text():

    for file in os.listdir(PDF_FOLDER):

        if file.lower().endswith(".pdf"):

            pdf_path = os.path.join(PDF_FOLDER, file)

            print(f"Processing PDF: {file}")

            text = ""

            with pdfplumber.open(pdf_path) as pdf:

                for page in pdf.pages:
                    page_text = page.extract_text()

                    if page_text:
                        text += page_text + "\n"

            output_file = os.path.join(
                OUTPUT_FOLDER,
                file.split(".")[0] + ".txt"
            )

            with open(output_file, "w", encoding="utf-8") as f:
                f.write(text)

            print(f"Saved text to {output_file}")


if __name__ == "__main__":
    extract_pdf_text()