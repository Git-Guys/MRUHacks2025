from flask import Flask, jsonify, request
from icalendar import Calendar, Event
from docx import Document
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
    ALLOWED_EXTENSIONS = [".pdf", ".docx", ".txt"]
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXTENSIONS
    
def parse_docx(filename: str) -> str:
    '''
    Parses a .docx to a string.
    '''
    doc = Document(filename)
    return "\n".join(p.text.strip() for p in doc.paragraphs if p.text.strip())

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
    return jsonify({"message": "Success"})

@app.get("/output")
def output(data: dict) -> str:
    '''
    Returns a string back to the front end.
    '''
    return jsonify(data)

if __name__ == "__main__":
    app.run(port = 8000)