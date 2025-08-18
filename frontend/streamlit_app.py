import streamlit as st
import requests
import os

BACKEND = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="CV Intelligence - Phase 1", page_icon="📄", layout="wide")
st.title("CV Intelligence Platform — Phase 1 (Upload & Extraction)")

with st.expander("Backend settings", expanded=False):
    st.write(f"Backend URL: {BACKEND}")

st.subheader("Upload CV (PDF/DOCX)")
uploaded = st.file_uploader("Choose your CV file", type=["pdf", "docx"])

if "cv_id" not in st.session_state:
    st.session_state.cv_id = None

if uploaded is not None:
    if st.button("Upload and Extract"):
        files = {"file": (uploaded.name, uploaded, uploaded.type)}
        try:
            resp = requests.post(f"{BACKEND}/cv/upload", files=files, timeout=120)
            if resp.ok:
                data = resp.json()
                st.session_state.cv_id = data.get("cv_id")
                st.success(f"Uploaded: {uploaded.name} | OCR used: {data.get('ocr_used')}")
            else:
                st.error(f"Upload failed: {resp.status_code} {resp.text}")
        except Exception as e:
            st.error(f"Request error: {e}")

st.markdown("---")
st.subheader("Extracted Text Preview")

if st.session_state.cv_id:
    try:
        r = requests.get(f"{BACKEND}/cv/{st.session_state.cv_id}", timeout=60)
        if r.ok:
            info = r.json()
            st.write(f"Filename: {info['filename']}")
            st.write(f"OCR used: {info['ocr_used']}")
            st.text_area("Preview", info["raw_text_preview"], height=400)
        else:
            st.error(f"Fetch failed: {r.status_code} {r.text}")
    except Exception as e:
        st.error(f"Request error: {e}")
else:
    st.info("Upload a CV to see extracted text")


st.markdown("---")
st.subheader("Ask questions about your CV")

if st.session_state.cv_id:
    chat_history = st.session_state.get("chat_history", [])

    user_msg = st.text_input("Your question:")
    
    if st.button("Send Question") and user_msg:
        resp = requests.post(
            f"{BACKEND}/cv/{st.session_state.cv_id}/chat", json={"message": user_msg}, timeout=60
        )
        if resp.ok:
            data = resp.json()
            reply = data.get("reply", "")
            messages = data.get("messages", [])
            st.session_state["chat_history"] = messages

            st.markdown(f"**You:** {user_msg}")
            st.markdown(f"**Bot:** {reply}")
        else:
            st.error(f"Chat failed: {resp.text}")
    # Show previous chat
    for m in chat_history[-5:]:
        st.write(f"[{m['role'].capitalize()}]: {m['content']}")

else:
    st.info("Upload a CV to enable chat.")

st.markdown("---")
st.subheader("Extract structured CV info")

if st.session_state.cv_id:
    if st.button("Extract Key Features"):
        resp = requests.post(f"{BACKEND}/cv/{st.session_state.cv_id}/structure", timeout=60)
        if resp.ok:
            fields = resp.json()
            st.json(fields)
        else:
            st.error(f"Extraction failed: {resp.text}")


def display_quality_report(result):
    st.success(f"CV Quality Score: {result.get('score', 'N/A')}/100")
    rubric = result.get('rubric', {})
    st.write("## Rubric Breakdown")
    st.json(rubric)

    st.write("## Strengths")
    strengths = result.get("strengths", [])
    if strengths:
        for strength in strengths:
            st.write(f"- {strength}")
    else:
        st.write("No strengths identified.")

    st.write("## Improvements")
    improvements = result.get("improvements", [])
    if improvements:
        for imp in improvements:
            area = imp.get('area', '')
            issue = imp.get('issue', '')
            fix_example = imp.get('fix_example', '')
            st.write(f"- **{area}:** {issue} (Fix: {fix_example})")
            st.write("")  # Add extra spacing
    else:
        st.write("No improvements suggested.")

    if "rewritten_examples" in result:
        st.write("## Rewritten Examples")
        st.json(result["rewritten_examples"])


st.markdown("---")
st.subheader("CV Quality Evaluation and Recommendations")

if st.session_state.get("cv_id"):
    if st.button("Evaluate CV Quality"):
        with st.spinner("Evaluating CV quality..."):
            try:
                resp = requests.post(
                    f"{BACKEND}/cv/{st.session_state.cv_id}/quality/evaluate", timeout=120
                )
                if resp.ok:
                    result = resp.json()
                    display_quality_report(result)
                else:
                    st.error(f"Quality evaluation failed: {resp.status_code} {resp.text}")
            except Exception as e:
                st.error(f"Request failed: {e}")

    st.write("### Last Quality Report")
    try:
        resp2 = requests.get(
            f"{BACKEND}/cv/{st.session_state.cv_id}/quality", timeout=60
        )
        if resp2.ok:
            result = resp2.json()
            st.info(f"Previous CV Quality Score: {result.get('score', 'N/A')}/100")
            display_quality_report(result)
        else:
            st.write("No previous report found.")

        if resp.ok:
            result = resp.json()
            if "raw" in result:
                st.error("Received unparsable JSON from backend. Raw output:")
                st.text_area("Raw Gemini output", result["raw"], height=400)
            else:
                display_quality_report(result)
        else:
            st.error(f"Quality evaluation failed: {resp.status_code} {resp.text}")

    except Exception as e:
        st.write(f"Could not retrieve previous report: {e}")
else:
    st.info("Upload a CV first to evaluate its quality.")