from fastapi import FastAPI, UploadFile, File
import shutil
import os
from pypdf import PdfReader

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

import nltk
nltk.download('punkt')

app = FastAPI()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# -------- PDF TEXT EXTRACTION --------
def extract_text_from_pdf(file_path):

    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + " "

    return text


# -------- TEXT SUMMARIZATION --------
def summarize_text(text, sentences_count=5):

    if not text or len(text.strip()) < 50:
        return "Not enough readable text found in the PDF."

    try:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LsaSummarizer()

        summary_sentences = summarizer(parser.document, sentences_count)

        summary = " ".join(str(sentence) for sentence in summary_sentences)

        if not summary.strip():
            summary = text[:300]

        return summary

    except Exception as e:
        return f"Summary generation failed: {str(e)}"


# -------- API 1 : UPLOAD FILE --------
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "File uploaded successfully",
        "filename": file.filename
    }


# -------- API 2 : SUMMARY --------
@app.post("/summary")
async def get_summary(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text_from_pdf(file_path)

    if not text:
        return {"error": "Could not extract text from this PDF"}

    summary = summarize_text(text, 5)

    return {
        "file_name": file.filename,
        "summary": summary
    }


# -------- API 3 : ANALYZE PDF --------
@app.post("/analyze")
async def analyze_file(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text_from_pdf(file_path)

    if not text:
        return {"error": "Could not extract text from this PDF"}

    summary = summarize_text(text, 7)

    word_count = len(text.split())

    return {
        "file_name": file.filename,
        "word_count": word_count,
        "summary": summary,
        "preview_text": text[:500]
    }