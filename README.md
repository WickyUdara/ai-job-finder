# 📄 CV Intelligence Platform (Streamlit-first)

An **end-to-end CV Intelligence Platform** for extraction, analysis, and matching.  
Currently Streamlit-first for rapid iteration, with a stable API layer to support a future React migration.

---

## ✨ Features

- **Upload CV** → robust extraction with OCR fallback (Gemini).  
- **Chat with CV** → query key skills, experience, and attributes.  
- **Evaluate CV quality** → score and prioritized improvements (Gemini).  
- **Job matching** → cosine similarity search against an internal job dataset.  
- **Admin console** → audit CV history, generate/manage jobs.  

---

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)  
- **Database**: MongoDB (Atlas or local)  
- **AI**: Gemini (OCR, extraction, chat, critique)  
- **Vector Search**: MongoDB Atlas Vector Search (preferred) or FAISS fallback  
- **Frontend (dev)**: Streamlit  
- **Frontend (future)**: React  
- **Auth**: JWT (access + refresh tokens)  

---

## 📂 Folder Structure

backend/app/api       # FastAPI routes (auth, cv, quality, jobs, admin)
backend/app/services  # Business logic (extraction, quality, dataset, matching)
backend/app/core      # Config, security, embeddings, Gemini wrappers
docs/                 # API.md, DATA_MODEL.md, PROMPTS.md, ARCHITECTURE.md
frontend/             # Streamlit app for development/testing

---

Backend

# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # (Linux/Mac)
venv\Scripts\activate     # (Windows)

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create backend/.env from .env.example and set values

# 4. Run the server
uvicorn app.main:app --reload  

----

Frontend (Streamlit)
# 1. Create/activate a virtual environment
python -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run Streamlit app
streamlit run streamlit_app.py


## 📖 API Docs

Interactive docs available at:
👉 http://localhost:8000/docs

## 🧭 Development Phases

- CV upload + OCR extraction

- Chat with CV + structured extraction

- Quality evaluation + improvement suggestions

- Job dataset (1,000 roles) + embeddings + matching

- Admin console (history, job generation, CRUD)

- Migrate UI to React

## 🔐 Security & Privacy

- JWT-protected endpoints

- Role-based access (admin routes)

- Avoid logging raw CV content

- Optional: PII redaction + encryption-at-rest

🛣️ Roadmap

- Semantic matching enhancements

- Target-role aware critique

- Bookmarks, saved searches, exports

- Background workers for heavy tasks