import streamlit as st
import requests

st.title("Job Finder: Chat with Your CV")

# Store CV ID after upload, or enter manually for testing
if "cv_id" not in st.session_state:
    st.session_state.cv_id = None

st.write("Upload your CV in PDF or DOCX format:")
uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'docx'])

if uploaded_file is not None:
    files = {'file': (uploaded_file.name, uploaded_file, uploaded_file.type)}
    response = requests.post("http://localhost:8000/upload-cv/", files=files)
    if response.ok:
        data = response.json()
        st.success(f"CV '{uploaded_file.name}' uploaded successfully!")
        st.header("Extracted CV Content:")
        st.text_area("Content", data['content'], height=400)
        st.session_state.cv_id = data.get('cv_id')
    else:
        st.error("Error uploading file: " + response.text)

# Initialize chat history if not present
if "messages" not in st.session_state:
    # Each message: dict with keys 'role' ('user' or 'assistant') and 'content'
    st.session_state.messages = []

st.markdown("---")
st.header("Chatbot")

if not st.session_state.cv_id:
    st.info("Please upload a CV to start chatting.")
else:
    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User input
    user_input = st.chat_input("Ask a question about your CV")

    if user_input:
        # Display user message immediately
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Call backend chat API
        payload = {"cv_id": st.session_state.cv_id, "question": user_input}
        chat_response = requests.post("http://localhost:8000/chat/", json=payload)

        if chat_response.ok:
            answer = chat_response.json().get("answer", "")
            # Display assistant response
            st.session_state.messages.append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"):
                st.markdown(answer)
        else:
            error_msg = f"Error: {chat_response.text}"
            st.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
