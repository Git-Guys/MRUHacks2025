from pypdf import PdfReader
from docx import Document
import fitz
import io
import os
from image_conversion import convert_any_to_png
from Image_Processor import extract_text_from_image

def parse_file(file) -> str:
    """
    Parses an uploaded file (from Flask) into plain text.
    Supports .docx, .pdf, and .txt.
    """
    filename = file.filename.lower()

    # Read the file bytes once
    data = file.read()
    if not data:
        raise ValueError("Uploaded file appears to be empty.")

    # DOCX
    if filename.endswith(".docx"):
        # docx.Document can open a file-like object
        doc = Document(io.BytesIO(data))
        return "\n".join(p.text.strip() for p in doc.paragraphs if p.text.strip())

    # PDF
    elif filename.endswith(".pdf"):
        reader = PdfReader(io.BytesIO(data))
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

    # TXT
    elif filename.endswith(".txt"):
        try:
            return data.decode("utf-8")
        except UnicodeDecodeError:
            return data.decode("latin-1", errors="replace")

    # IMAGES
    elif filename.endswith(".png") or filename.endswith(".jpg") or \
        filename.endswith(".jpeg") or filename.endswith(".heic") or \
        filename.endswith(".heif") or filename.endswith(".bmp") or \
        filename.endswith(".tiff") or filename.endswith(".webp"):
            return extract_text_from_image(convert_any_to_png(file))["text"]

    else:
        raise ValueError("Unsupported file type. Use .docx, .pdf, or .txt.")
