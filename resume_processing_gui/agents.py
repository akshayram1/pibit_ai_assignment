import os
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content
import PyPDF2
import docx
import re
from datetime import datetime
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

def extractor(prompt, validate=False):
    st.write("Extracting information...")
    
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_schema": content.Schema(
            type=content.Type.OBJECT,
            properties={
                "personal_info": content.Schema(
                    type=content.Type.OBJECT,
                    properties={
                        "name": content.Schema(type=content.Type.STRING),
                        "phone_no": content.Schema(type=content.Type.NUMBER),
                        "email": content.Schema(type=content.Type.STRING),
                    },
                ),
                "education": content.Schema(
                    type=content.Type.OBJECT,
                    properties={
                        "degree": content.Schema(type=content.Type.STRING),
                        "university": content.Schema(type=content.Type.STRING),
                    },
                ),
                "work_experience": content.Schema(
                    type=content.Type.OBJECT,
                    properties={
                        "company": content.Schema(type=content.Type.STRING),
                        "role": content.Schema(type=content.Type.STRING),
                        "description": content.Schema(type=content.Type.STRING),
                        "start_date": content.Schema(type=content.Type.STRING),
                        "end_date": content.Schema(type=content.Type.STRING),
                    },
                ),
                "skills": content.Schema(type=content.Type.STRING),
            },
        ),
        "response_mime_type": "application/json",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(history=[])

    if isinstance(validate, int):
        response = chat_session.send_message(f"{prompt}")
    elif validate == False:
        response = chat_session.send_message(f"Extract information required from the given resume data is to {prompt}")
    else:
        response = chat_session.send_message(f"validate information required from the given resume data is to {prompt}")

    return response.text

def reader(file):
    st.write("Reading file...")
    
    if file is None:
        return "No file uploaded."

    file_extension = os.path.splitext(file.name)[1].lower()
    text = ""

    try:
        if file_extension == '.pdf':
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() or ''
        elif file_extension == '.docx':
            doc = docx.Document(file)
            for paragraph in doc.paragraphs:
                text += paragraph.text + '\n'
        else:
            return "Unsupported file format. Please provide a PDF or DOCX file."

        if text:
            return text.strip()
        else:
            return "No text found"

    except Exception as e:
        return f"An error occurred: {str(e)}"

def validator(resume):
    st.write("Validating resume...")
    return extractor("Find errors and put invalid wherever you find error on given " + str(resume), validate=True)