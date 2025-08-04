import PyPDF2

def extract_text_from_pdf(file_data):
    reader = PyPDF2.PdfReader(file_data)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""   
    return text.strip()