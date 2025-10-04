from flask import Flask, jsonify, request
from icalendar import Calendar, Event
from pypdf import PdfReader
from docx import Document
import fitz
import io
import os

app = Flask(__name__)

def intake_file(filename: str) -> str:
    '''
    Intakes a file and returns it as a string.
    '''
    with open(filename, "r") as file:
        content = file.read()
    return content

def validate_file_format(filename: str) -> bool:
    '''
    Validates the file format to be either .pdf, .docx, or .txt.
    '''
    ALLOWED_EXTENSIONS = [".docx", ".pdf", ".txt"]
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXTENSIONS
    
def parse_file(filename: str) -> str:
    '''
    Parses a file to a string.
    '''
    if filename.lower().endswith(".docx"):
        doc = Document(filename)
        return "\n".join(p.text.strip() for p in doc.paragraphs if p.text.strip())
    
    elif filename.lower().endswith(".pdf"):
        # --- Try PyMuPDF first ---
        if fitz is not None:
            with fitz.open(filename) as doc:
                # If encrypted, try blank password first
                if getattr(doc, "needs_pass", False) and not doc.authenticate(""):
                    raise ValueError("PDF is encrypted; password required.")
                parts = []
                for page in doc:
                    text = (page.get_text() or "").strip()
                    if text:
                        parts.append(text)
                return "\n".join(parts)

        # --- Fallback to pypdf ---
        if PdfReader is not None:
            reader = PdfReader(filename)
            if getattr(reader, "is_encrypted", False):
                try:
                    ok = reader.decrypt("")  # try blank password
                    if ok == 0:
                        raise ValueError("PDF is encrypted; password required.")
                except Exception:
                    raise ValueError("PDF is encrypted; password required.")
            parts = []
            for page in reader.pages:
                text = (page.extract_text() or "").strip()
                if text:
                    parts.append(text)
            return "\n".join(parts)

        # Neither backend available
        raise ImportError("Install either 'pymupdf' or 'pypdf' to parse PDFs.")

    elif filename.lower().endswith(".txt"):
        with open(filename, "r", encoding="utf-8", errors="replace") as f:
            return f.read()

    else:
        raise ValueError("Unsupported file type. Use .docx, .pdf, or .txt.")

@app.post("/test")
def intake_user_input():
    '''
    Takes the user input into the parameters.
    '''
    print("This function is being called")
    project_name = request.form.get("projectName", "")
    start_date = request.form.get("startDate", "")
    end_date = request.form.get("endDate", "")
    description = request.form.get("description", "")
    try:
        text_file = request.files['file']
    except:
        text_file = ""
    if not project_name or not start_date or not end_date:
        return jsonify({"error": "Request is missing a field."}), 400
    if text_file:
        parse_file(text_file)
    elif not text_file and not description:
        return jsonify({"error": "There is no file, or it is missing a description."}), 400
    return jsonify({"message": "Success."})

@app.get("/output")
def output(data: dict) -> str:
    '''
    Returns a string back to the front end.
    '''
    return jsonify(data)

def andrews_function() -> None:
    pass

if __name__ == "__main__":
    app.run(port = 8000)