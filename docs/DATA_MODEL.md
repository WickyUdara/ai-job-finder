# 📊 Data Model (MongoDB)

## Conventions
- `_id`: `ObjectId`
- `created_at`, `updated_at`: `ISODate`
- `embeddings`: `float[]` (`VECTOR_DIM`)

---

## 🧑 Users


{
  "_id": ObjectId,
  "email": string,          // unique
  "password_hash": string,
  "role": "user" | "hr" | "admin",
  "created_at": ISODate
}

## 🧑 CVs
{
  "_id": ObjectId,
  "user_id": ObjectId,
  "filename": string,
  "raw_text": string,
  "ocr_used": boolean,

  "extracted_fields": {
    "name": string?,
    "contact": { "email": string?, "phone": string?, "location": string? },
    "summary": string?,
    "experience": [
      { "company": string?, "role": string?, "start": string?, "end": string?, "bullets": string[]? }
    ],
    "education": [
      { "school": string?, "degree": string?, "start": string?, "end": string? }
    ],
    "skills": {
      "programming": string[]?,
      "ml": string[]?,
      "data": string[]?,
      "cloud": string[]?,
      "other": string[]?
    },
    "certifications": string[]?,
    "years_experience": number?
  },

  "embedding": float[]?,   // VECTOR_DIM

  "quality_report": {
    "score": number,
    "rubric": {
      "ats_readiness": number,
      "clarity": number,
      "quantification": number,
      "keyword_coverage": number,
      "structure_formatting": number,
      "consistency": number
    },
    "strengths": string[],
    "improvements": [
      { "area": string, "issue": string, "fix_example": string }
    ],
    "rewritten_examples": {
      "summary": string?,
      "bullets": string[]?
    }?
  },

  "created_at": ISODate,
  "updated_at": ISODate
}

## 🧑 Chats
{
  "_id": ObjectId,
  "cv_id": ObjectId,
  "messages": [
    { "role": "system" | "user" | "assistant", "content": string, "timestamp": ISODate }
  ],
  "created_at": ISODate,
  "updated_at": ISODate
}

## 🧑 Jobs
{
  "_id": ObjectId,
  "title": string,
  "company": string,
  "location": string,
  "description": string,
  "tags": string[],
  "url": string?,
  "embedding": float[],     // VECTOR_DIM
  "salary": string?,
  "source": "generated" | "manual",
  "created_at": ISODate,
  "updated_at": ISODate
}

## 🧑 Job Matches

{
  "_id": ObjectId,
  "cv_id": ObjectId,
  "job_id": ObjectId,
  "score": number,           // 0-100
  "similarity": number,      // 0-1
  "matched_skills": string[],
  "explanation": string?,
  "created_at": ISODate
}

##📑 Indexes

- users: email (unique)

- cvs: user_id, created_at

- jobs: created_at, tags, embedding (vector index in Atlas)

- chats: cv_id, created_at

- admin_actions: timestamp

##🔍 Vector Index (MongoDB Atlas)

- jobs.embedding: VECTOR_DIM with HNSW/IVF (Atlas config)

- cvs.embedding: optional (for comparing CVs or personalized retrieval)