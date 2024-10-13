import os
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content
import PyPDF2
import docx
import re
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

def extractor(prompt,validate= False):
    print("i am in executor")
    
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

    # Create the model
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_schema": content.Schema(
        type = content.Type.OBJECT,
        properties = {
        "personal_info": content.Schema(
            type = content.Type.OBJECT,
            properties = {
            "name": content.Schema(
                type = content.Type.STRING,
            ),
            "phone_no": content.Schema(
                type = content.Type.NUMBER,
            ),
            "email": content.Schema(
                type = content.Type.STRING,
            ),
            },
        ),
        "education": content.Schema(
            type = content.Type.OBJECT,
            properties = {
            "degree": content.Schema(
                type = content.Type.STRING,
            ),
            "university": content.Schema(
                type = content.Type.STRING,
            ),
            },
        ),
        "work_experience ": content.Schema(
            type = content.Type.OBJECT,
            properties = {
            "company": content.Schema(
                type = content.Type.STRING,
            ),
            "role": content.Schema(
                type = content.Type.STRING,
            ),
            "description": content.Schema(
                type = content.Type.STRING,
            ),
            "start_date": content.Schema(
                type = content.Type.STRING,
            ),
            "end_date": content.Schema(
                type = content.Type.STRING,
            ),
            },
        ),
        "skills": content.Schema(
            type = content.Type.STRING,
        ),
        },
    ),
    "response_mime_type": "application/json",
    }

    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
    )

    chat_session = model.start_chat(
    history=[
    ]
    )

    if isinstance(validate, int):
        response = chat_session.send_message(f"{prompt}")
    elif validate == False:
        response = chat_session.send_message(f"Extract information required from the given resume data is to {prompt}")
    
    else:
        response = chat_session.send_message(f"validate information required from the given resume data is to {prompt}")
    

    return response.text
        


def reader(file_path):
    print('i am in reador')
    # Check if the file exists
    if not os.path.isfile(file_path):
        return "File not found."

    # Check if the file is empty
    if os.path.getsize(file_path) == 0:
        return "File is empty."

    # Get the file extension
    _, file_extension = os.path.splitext(file_path)

    # Initialize an empty string for the text content
    text = ""

    try:
        if file_extension.lower() == '.pdf':
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    page_text = page.extract_text() or ''
                    text += page_text
            if text:
                return text.strip()
            else:
                return "No text found"

        elif file_extension.lower() == '.docx':
            doc = docx.Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + '\n'
            if text:
                return text.strip()
            else:
                return "No text found"

        else:
            return "Unsupported file format. Please provide a PDF or DOCX file."

    except Exception as e:
        return f"An error occurred: {str(e)}"

# Example usage:


# def validator(resume):
#     errors = []

#     def validate_email(email):
#         """Validate email format"""
#         email_pattern = r"[^@]+@[^@]+\.[^@]+"
#         if not re.match(email_pattern, email):
#             errors.append(f"Invalid email format: {email}")

#     def validate_phone(phone):
#         """Validate phone number format"""
#         phone_pattern = r"^\+?[1-9]\d{1,14}$"
#         if not re.match(phone_pattern, phone):
#             errors.append(f"Invalid phone number format: {phone}")

#     def validate_date(date_text):
#         """Validate date format YYYY-MM-DD"""
#         try:
#             datetime.strptime(date_text, '%Y-%m-%d')
#         except ValueError:
#             errors.append(f"Invalid date format: {date_text}")

#     def validate_url(url):
#         """Validate URL format"""
#         url_pattern = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
#         if not re.match(url_pattern, url):
#             errors.append(f"Invalid URL format: {url}")

#     def validate_name(name):
#         """Check if the name is not empty"""
#         if not name or not isinstance(name, str):
#             errors.append("Name is missing or invalid.")

#     def validate_personal_info(personal_info):
#         """Validate personal information"""
#         validate_name(personal_info.get("name", ""))
#         validate_email(personal_info.get("email", ""))
#         validate_phone(personal_info.get("phone", ""))
#         validate_url(personal_info.get("linkedin", ""))

#     # Start validation
#     validate_personal_info(resume.get("personal_info", {}))

    

#     return errors

def validator(resume):
    
    return extractor("Find errors and put invalid wherever you find error on given " + str(resume)  , validate = True)
        

op = {
  "personal_info": {
    "name": "Jane Smith",
    "phone_no": 1234567890,
    "email": "janecom"
  },
  "education": {
    "degree": "Master of Science in Computer Science",
    "university": "Tech University"
  },
  "work_experience": {
    "company": "Innovatech Solutions",
    "role": "Data Scientist",
    "description": "Analyzed data sets to improve business processes and customer satisfaction.",
    "start_date": "2022-01-15",
    "end_date": "2023-06-30"
  },
  "skills": 
  """
    "Data Analysis",
    "Machine Learning",
    "Python",
    "SQL",
    "Data Visualization"
  """
  
}


# print(validator(op))
