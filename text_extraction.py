import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from docx import Document
import pandas as pd

def extract_text(file_path):
    try:
        if file_path.endswith(".pdf"):
            with pdfplumber.open(file_path) as pdf:
                text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
                if not text.strip():
                    text = extract_text_with_ocr(file_path)
                return text if text.strip() else "No text extracted"
        elif file_path.endswith(".docx"):
            doc = Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs])
        elif file_path.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        elif file_path.endswith((".xls", ".xlsx")):
            df = pd.read_excel(file_path, sheet_name=None) 
            return "\n".join([sheet.astype(str).to_string() for sheet in df.values()])
    except Exception as e:
        print(f"⚠️ Error extracting from {file_path}: {e}")
        return ""

def extract_text_with_ocr(pdf_path):
    try:
        images = convert_from_path(pdf_path)
        return "\n".join([pytesseract.image_to_string(img) for img in images])
    except Exception as e:
        print(f"OCR extraction failed for {pdf_path}: {e}")
        return "OCR extraction failed"
