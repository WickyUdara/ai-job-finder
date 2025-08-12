import streamlit as st
import requests

BACKEND = "http://localhost:8000"

st.title("Job Finder: Upload, Chat, and Live Job Matches (Arbeitnow API)")

# Existing CV upload + chat sections remain the same...
if "cv_id" not in st.session_state:
    st.session_state.cv_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []

st.subheader("Upload your CV (PDF/DOCX)")
uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx"])
if uploaded_file is not None:
    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
    try:
        resp = requests.post(f"{BACKEND}/upload-cv/", files=files, timeout=60)
        if resp.ok:
            data = resp.json()
            st.session_state.cv_id = data.get("cv_id")
            st.success(f"Uploaded: {uploaded_file.name}")
            st.text_area("Extracted Content", data.get("content", "")[:5000], height=300)
        else:
            st.error(f"Upload error: {resp.text}")
    except Exception as e:
        st.error(f"Upload request failed: {e}")

st.markdown("---")
st.subheader("Chat with Your CV")
if not st.session_state.cv_id:
    st.info("Upload a CV to enable chat and job matching.")
else:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask a question about your CV")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        payload = {"cv_id": st.session_state.cv_id, "question": user_input}
        try:
            chat_resp = requests.post(f"{BACKEND}/chat/", json=payload, timeout=60)
            if chat_resp.ok:
                answer = chat_resp.json().get("answer", "")
                st.session_state.messages.append({"role": "assistant", "content": answer})
                with st.chat_message("assistant"):
                    st.markdown(answer)
            else:
                err = f"Error: {chat_resp.text}"
                st.session_state.messages.append({"role": "assistant", "content": err})
                st.error(err)
        except Exception as e:
            err = f"Chat request failed: {e}"
            st.session_state.messages.append({"role": "assistant", "content": err})
            st.error(err)

st.markdown("---")
st.subheader("Job Suggestions Based on Your CV")

if st.session_state.cv_id:
    if st.button("Suggest Relevant Jobs"):
        with st.spinner("Finding jobs that match your CV..."):
            try:
                # Just send CV ID
                params = {"cv_id": st.session_state.cv_id}
                r = requests.get(f"{BACKEND}/jobs/arbeitnow", params=params, timeout=60)
            except Exception as e:
                st.error(f"Search failed: {e}")
                r = None

        if r and r.ok:
            data = r.json()
            matches = data.get("matches", [])
            st.write(f"Found {len(matches)} job matches")
            for job in matches[:100]:
                st.markdown(f"### [{job['title']}]({job['url']})")
                meta_parts = [p for p in [job.get("company", ""), job.get("location", "")] if p]
                if meta_parts:
                    st.write(" — ".join(meta_parts))
                st.write(f"Match score: {job.get('score', 0)} | Skills: {', '.join(job.get('matched_skills', []))}")
                tags = job.get("tags", [])
                if tags:
                    st.write("Tags: " + ", ".join(tags))
                st.write("---")
        elif r:
            st.error(f"Error: {r.status_code} {r.text}")
else:
    st.info("Upload a CV first to get job suggestions.")
