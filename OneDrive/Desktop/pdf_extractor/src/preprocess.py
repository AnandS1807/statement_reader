# src/preprocess.py
import pdfplumber
from PIL import Image
import pytesseract

def extract_text_from_pdf(pdf_path):
    """Extract text from a digital PDF."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def extract_text_from_image(image_path):
    """Extract text from an image using OCR."""
    return pytesseract.image_to_string(Image.open(image_path))

def preprocess_pdf(pdf_path):
    """Preprocess a PDF (digital or scanned)."""
    try:
        return extract_text_from_pdf(pdf_path)
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None