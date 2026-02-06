import os
import fitz  # PyMuPDF

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts text from a PDF file.
    """
    if not file_path.lower().endswith(".pdf"):
        raise ValueError("Unsupported file type. Only PDF is supported.")
        
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
        
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
            
    return text.strip()
