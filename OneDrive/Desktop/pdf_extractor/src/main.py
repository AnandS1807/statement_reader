# src/main.py
import sys
import os
import json

# Add the project root directory to sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
print("Current Working Directory:", os.getcwd())

# Update imports to use relative paths
from .preprocess import preprocess_pdf
from .classify import classify_document_with_ollama
from .extract import extract_data_with_ollama
from .normalize import normalize_dates, normalize_currency
from .confidence import calculate_confidence


pdf_path = "C:/Users/ANAND/OneDrive/Desktop/pdf_extractor/data/input_pdfs/sample.pdf"

def process_pdf(pdf_path):
    # Step 1: Preprocess
    text = preprocess_pdf(pdf_path)
    
    # Step 2: Classify with Ollama
    doc_type = classify_document_with_ollama(pdf_path)
    
    # Step 3: Extract with Ollama
    extracted_text = extract_data_with_ollama(pdf_path)
    
    # Convert the extracted text to a structured format
    if isinstance(extracted_text, dict):
        extracted_data = extracted_text
    else:
        try:
            extracted_data = json.loads(extracted_text)
        except json.JSONDecodeError:
            extracted_data = {
                "dates": [],
                "amounts": []
            }
    
    
    # Step 4: Normalize the extracted data
    try:
        dates = normalize_dates(extracted_data.get("dates", []))
    except (TypeError, AttributeError):
        dates = []
        
    try:
        amounts = normalize_currency(extracted_data.get("amounts", []))
    except (TypeError, AttributeError):
        amounts = []
    
    # Step 5: Confidence
    confidence = calculate_confidence(extracted_data, [])
    print(f"Extracted text: {extracted_text}")
    print(f"Document type: {doc_type}")
    print(f"Extracted data: {extracted_data}")

    return {
        "document_type": doc_type,
        "dates": dates,
        "amounts": amounts,
        "confidence": confidence,
        "raw_extracted_text": extracted_text
    }

if __name__ == "__main__":
    pdf_path = "C:/Users/ANAND/OneDrive/Desktop/pdf_extractor/data/input_pdfs/sample.pdf"
    result = process_pdf(pdf_path)
    print(result)