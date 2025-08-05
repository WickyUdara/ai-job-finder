import streamlit as st
import requests

st.title("Job Finder: CV Upload Demo")

st.write("Upload your CV in PDF or DOCX format:")

uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'docx'])

if uploaded_file is not None:
    files = {'file': (uploaded_file.name, uploaded_file, uploaded_file.type)}
    response = requests.post(
        "http://localhost:8000/upload-cv/", 
        files=files
    )
    if response.ok:
        data = response.json()
        st.success(f"CV '{uploaded_file.name}' uploaded successfully!")
        st.header("Extracted CV Content:")
        st.text_area("Content", data['content'], height=400)
    else:
        st.error("Error uploading file: " + response.text)
