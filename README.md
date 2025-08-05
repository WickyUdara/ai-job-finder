# Job Finder App

A smart job finder that allows users to upload their CVs, chat with an AI about their resume, and recommends jobs from online sources.

## Features

- **Upload CV:** Accept CVs in PDF, DOCX formats.
- **Chatbot:** AI-driven conversation for CV-based questions and career advice.
- **Job Recommendations:** Fetch and suggest relevant jobs from online sources.

## Tech Stack

- **Frontend:** Streamlit (for quick prototyping)
- **Backend:** FastAPI (Python)
- **Database:** MongoDB
- **CV Parsing:** spaCy, PyPDF2, python-docx
- **AI/NLP:** OpenAI API or HuggingFace Transformers
- **Job Integration:** BeautifulSoup, Requests (for scraping job boards)
- **Deployment:** Docker

## Folder Structure
job_finder/
│
├── backend/
│ ├── app/
│ │ ├── api/ # FastAPI routes
│ │ ├── core/ # Business logic
│ │ ├── models/ # Pydantic models
│ │ ├── parsers/ # CV parsing utils
│ │ ├── db/ # DB connection, schemas
│ │ └── main.py # FastAPI entrypoint
│ └── requirements.txt # Backend dependencies
│
├── frontend/
│ ├── streamlit_app.py # Streamlit app
│ └── requirements.txt # Frontend dependencies
│
├── README.md
├── .gitignore
├── docker-compose.yml (optional, for local dev)

## Getting Started

1. **Clone the repository**
2. **Install dependencies** for both `frontend` and `backend`
    ```
    cd backend
    pip install -r requirements.txt

    cd ../frontend
    pip install -r requirements.txt
    ```
3. **Set up MongoDB** (local or cloud)
4. **Run the backend**
    ```
    uvicorn app.main:app --reload
    ```
5. **Run the frontend**
    ```
    streamlit run streamlit_app.py
    ```

---

## requirements.txt (Backend)

gemini 2.5 flash for OCR