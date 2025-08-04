import docx

def extract_text_from_docx(file_data):
    doc = docx.Document(file_data)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text.strip()