from flask import Flask, jsonify, request
from icalendar import Calendar, Event
from File_Parser import parse_file
from groq_call import groq_call

app = Flask(__name__)


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

    file_contents = ""

    if text_file:
        file_contents = parse_file(text_file)

    elif not text_file and description:
        file_contents = description

    elif not text_file and not description:
        return jsonify({"error": "There is no file, or it is missing a description."}), 400

    llm_prompt = f"""
    {
          "project_name": {project_name},
          "start_date": {start_date},
          "end_date": {end_date},
          "project_description": {file_contents}
    }
    """

    llm_response = groq_call(llm_prompt)
    return jsonify(llm_response)

if __name__ == "__main__":
    app.run(port = 8000)