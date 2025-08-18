# 🏗️ Architecture

## Overview
- **API-first**: stable endpoints to support both **Streamlit** and future **React** frontend.
- **Services layer**: isolates core business logic (extraction, structuring, quality, matching).
- **Gemini**: used for OCR, structured extraction, chat, and critique.
- **Vector search**: powered by **MongoDB Atlas Vector Search** (preferred), with **FAISS** fallback for local/dev.
- **Authentication**: JWT with role-based access; admin-only routes for console operations.
- **Frontend**:
  - **Streamlit** for rapid development and iteration.
  - **React** migration planned, consuming the same stable API.

## High-Level Flow

1. **User uploads CV** → API routes → `cv_extraction` & `cv_structuring` services.  
2. **Gemini** enhances extraction, OCR fallback, and structured data.  
3. **CV quality evaluation** → `cv_quality` service.  
4. **Job matching** → embeddings + cosine similarity via MongoDB Atlas Vector Search (or FAISS).  
5. **Admin console** → manages jobs, audits CV history, monitors system.  
6. **Frontend (Streamlit/React)** consumes only API endpoints (no direct DB calls).  

## Components

- **FastAPI Backend**
  - Routes (`/auth`, `/cv`, `/jobs`, `/admin`)
  - Services layer (business logic)
  - Core utilities (config, security, embeddings, Gemini wrappers)
- **Database**
  - MongoDB Atlas (or local)
  - Vector search index for jobs + CV embeddings
- **Frontend**
  - Streamlit (development/testing)
  - React (future migration)
- **AI Layer**
  - Gemini for OCR, extraction, structured CVs, chat, critique

