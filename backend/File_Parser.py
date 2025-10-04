from pypdf import PdfReader
from docx import Document
import fitz
import io
import os

def parse_file(filename: str) -> str:
    '''
    Parses a file to a string.
    '''
    # READ WORD DOCUMENT
    if filename.lower().endswith(".docx"):
        doc = Document(filename)
        return "\n".join(p.text.strip() for p in doc.paragraphs if p.text.strip())

    # READ PDF
    elif filename.lower().endswith(".pdf"):
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

    elif filename.lower().endswith(".txt"):
        with open(filename, "r", encoding="utf-8", errors="replace") as f:
            return f.read()

    # TODO image

    else:
        raise ValueError("Unsupported file type. Use .docx, .pdf, or .txt.")
