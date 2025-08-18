import streamlit as st
import requests
import os
import io
import json

BACKEND = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="CV Intelligence - Phase 1", page_icon="📄", layout="wide")
st.title("CV Intelligence Platform — Phase 1 (Upload & Extraction)")

# with st.expander("Backend settings", expanded=False):
#     st.write(f"Backend URL: {BACKEND}")

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
    with st.expander("Strengths", expanded=True):
        for strength in result.get("strengths", []):
            st.write(f"- {strength}")

    st.write("## Improvements")
    improvements = result.get("improvements", [])
    with st.expander("Improvements", expanded=True):
        for imp in result.get("improvements", []):
            st.write(f"- {imp.get('area', '')}: {imp.get('issue', '')} (Fix: {imp.get('fix_example', '')})")


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


if st.session_state.get("cv_id"):
    # After fetching result (ensure it's a dict, not raw)
    result_for_export = None
    # Get latest report
    resp2 = requests.get(
        f"{BACKEND}/cv/{st.session_state.cv_id}/quality", timeout=60
    )
    if resp2.ok:
        result_for_export = resp2.json()
        # Download as JSON
        json_bytes = io.BytesIO(json.dumps(result_for_export, indent=2).encode("utf-8"))
        st.download_button(
            label="Download Quality Report (JSON)",
            data=json_bytes,
            file_name=f"cv_quality_report_{st.session_state.cv_id}.json",
            mime="application/json"
        )
        # Download as text summary
        # Create text format report
        def pretty_report_text(data):
            text = []
            text.append(f"CV Quality Score: {data.get('score', 'N/A')}/100")
            rubric = data.get("rubric", {})
            text.append("Rubric Breakdown:")
            for k, v in rubric.items():
                text.append(f"  - {k}: {v}")
            text.append("Strengths:")
            for s in data.get("strengths", []):
                text.append(f"  - {s}")
            text.append("Improvements:")
            for imp in data.get("improvements", []):
                area = imp.get("area", "")
                issue = imp.get("issue", "")
                fix = imp.get("fix_example", "")
                text.append(f"  - {area}: {issue} (Fix: {fix})")
            if "rewritten_examples" in data:
                text.append("Rewritten Examples:")
                re = data.get("rewritten_examples")
                if isinstance(re, list):
                    for ex in re:
                        text.append(f"  - {ex}")
                elif isinstance(re, dict):
                    for k, v in re.items():
                        text.append(f"  {k}: {v}")
            return "\n".join(text)

        txt_bytes = io.BytesIO(pretty_report_text(result_for_export).encode("utf-8"))
        st.download_button(
            label="Download Quality Report (Text)",
            data=txt_bytes,
            file_name=f"cv_quality_report_{st.session_state.cv_id}.txt",
            mime="text/plain"
        )



st.markdown("---")
st.subheader("Job Dataset Management")

with st.expander("Add a new job to dataset"):
    job_title = st.text_input("Job Title")
    job_desc = st.text_area("Job Description")
    job_reqs = st.text_area("Requirements (comma separated)")
    job_skills = st.text_area("Skills (comma separated)")
    job_employer = st.text_input("Employer")
    job_location = st.text_input("Location")
    if st.button("Upload Job"):
        job_data = {
            "title": job_title,
            "description": job_desc,
            "requirements": [r.strip() for r in job_reqs.split(",") if r.strip()],
            "skills": [s.strip() for s in job_skills.split(",") if s.strip()],
            "employer": job_employer,
            "location": job_location
        }
        r = requests.post(f"{BACKEND}/job/upload", json=job_data)
        if r.ok:
            st.success(f"Job uploaded: {r.json()['title']}")
        else:
            st.error(r.text)

st.subheader("All Jobs in Dataset")
r2 = requests.get(f"{BACKEND}/job/list")
if r2.ok:
    jobs_list = r2.json()
    for job in jobs_list:
        st.write(f"- {job['title']} ({job.get('location','')})")

st.markdown("---")
st.subheader("Job Matching for Your CV")
if st.session_state.get("cv_id"):
    if st.button("Find Best Jobs for My CV"):
        r3 = requests.get(f"{BACKEND}/job/match/{st.session_state.cv_id}")
        if r3.ok:
            st.write("Top Matches:")
            for match in r3.json():
                st.write(f"- {match['title']} (Score: {match['score']:.3f})")
        else:
            st.error(r3.text)
else:
    st.info("Upload and evaluate a CV, then match to jobs!")