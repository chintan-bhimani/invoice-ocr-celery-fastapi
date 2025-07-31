import pytesseract
from PIL import Image
import os
from pdf2image import convert_from_path


def extract_text(file_path: str) -> str:
    if file_path.lower().endswith(".pdf"):
        try:
            images = convert_from_path(file_path)
            text = ""
            for img in images:
                text += pytesseract.image_to_string(img)
            return text
        except Exception as e:
            return f"OCR failed for PDF: {e}"
    else:
        try:
            return pytesseract.image_to_string(Image.open(file_path))
        except Exception as e:
            return f"OCR failed for image: {e}"
