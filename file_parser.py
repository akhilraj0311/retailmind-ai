from pypdf import PdfReader
import pandas as pd
from docx import Document

def parse_file(file_path):
    """
    Extract text from PDF, DOCX, CSV, or TXT files
    """

    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text

    elif file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
        return df.to_string()

    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text

    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    else:
        raise ValueError("Unsupported file type. Please upload PDF, DOCX, CSV, or TXT.")