import os
import pytesseract
from PIL import Image
import cv2

# Path to tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

IMAGE_FOLDER = os.path.join(BASE_DIR, "data", "images")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "output_text")

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def preprocess_image(image_path):

    img = cv2.imread(image_path)

    # convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # apply threshold to improve text detection
    thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

    return thresh


def extract_images_text():

    for file in os.listdir(IMAGE_FOLDER):

        if file.lower().endswith((".png", ".jpg", ".jpeg")):

            image_path = os.path.join(IMAGE_FOLDER, file)

            print(f"Processing image: {file}")

            processed_image = preprocess_image(image_path)

            text = pytesseract.image_to_string(processed_image)

            print("Detected Text:", text)

            output_file = os.path.join(
                OUTPUT_FOLDER,
                file.split(".")[0] + ".txt"
            )

            with open(output_file, "w", encoding="utf-8") as f:
                f.write(text)

            print(f"Saved text to {output_file}")


if __name__ == "__main__":
    extract_images_text()