import streamlit as st
import json
from agents import reader, extractor, validator

st.title("Resume Parser and Validator")

uploaded_file = st.file_uploader("Choose a PDF or DOCX file", type=["pdf", "docx"])

if uploaded_file is not None:
    # Read the file
    file_content = reader(uploaded_file)
    
    if "Unsupported file format" in file_content or "No text found" in file_content:
        st.error(file_content)
    else:
        # Extract information
        extracted_info = extractor(file_content)
        
        # Display extracted information
        st.subheader("Extracted Information")
        try:
            json_data = json.loads(extracted_info)
            st.json(json_data)
        except json.JSONDecodeError:
            st.text(extracted_info)
        
        # Validate information
        validation_result = validator(extracted_info)
        
        st.subheader("Validation Result")
        try:
            json_data = json.loads(validation_result)
            st.json(json_data)
        except json.JSONDecodeError:
            st.text(validation_result)
        
        # User feedback
        st.subheader("Provide Feedback")
        user_feedback = st.text_area("Enter your feedback or corrections:")
        
        if st.button("Submit Feedback"):
            if user_feedback:
                # Process feedback
                updated_info = extractor(f"Update the following information based on this feedback: {user_feedback}\n\nOriginal information: {extracted_info}")
                
                st.subheader("Updated Information")
                try:
                    json_data = json.loads(updated_info)
                    st.json(json_data)
                except json.JSONDecodeError:
                    st.text(updated_info)
            else:
                st.warning("Please provide feedback before submitting.")

st.sidebar.info("Upload a resume (PDF or DOCX) to start the parsing and validation process.")