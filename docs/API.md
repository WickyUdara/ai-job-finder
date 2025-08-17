# 📡 API Specification (v1)

## 🌍 Base URL
- **Local**: `http://localhost:8000`

---

## 🔐 Authentication

- JWT Bearer tokens in the `Authorization` header:


- **Roles**:
- `user`
- `hr`
- `admin` (has access to admin console endpoints)

- **Error Format**:
```json
{
  "detail": "message",
  "code"?: "string",
  "context"?: { ... }
}

👤 Auth Endpoints
POST /auth/register

Registers a new user.
Body:

{ "email": "string", "password": "string", "role?": "user|hr|admin" }


Returns:

{ "user_id": "string" }

POST /auth/login

Login with email and password.
Body:

{ "email": "string", "password": "string" }


Returns:

{
  "access_token": "string",
  "refresh_token": "string",
  "token_type": "bearer",
  "expires_in": number
}

POST /auth/refresh

Refresh access token.
Body:

{ "refresh_token": "string" }


Returns:

{ "access_token": "string", "token_type": "bearer", "expires_in": number }

POST /auth/logout

Logout user.
Body: {}
Returns:

{ "success": true }

📄 CV Intake & Extraction
POST /cv/upload

Upload a CV.

Content-Type: multipart/form-data

Form fields: file (pdf|docx)

Returns:

{ "cv_id": "string", "filename": "string", "ocr_used": boolean }

GET /cv/{cv_id}

Retrieve CV metadata.
Returns:

{
  "cv_id": "string",
  "user_id": "string",
  "created_at": "ISODate",
  "filename": "string",
  "raw_text_preview": "string",
  "ocr_used": boolean
}

POST /cv/{cv_id}/extract

Force re-extraction with OCR fallback.
Returns:

{ "cv_id": "string", "raw_text": "string", "ocr_used": boolean }

POST /cv/{cv_id}/structure

Normalize CV into structured schema (Gemini).
Returns:

{
  "cv_id": "string",
  "extracted_fields": { ... }
}

GET /cv/{cv_id}/structured

Retrieve structured CV fields.
Returns:

{ "cv_id": "string", "extracted_fields": { ... } }

💬 Chat with CV
POST /cv/{cv_id}/chat

Chat with extracted CV data.
Body:

{ "message": "string" }


Returns:

{
  "reply": "string",
  "messages": [{ "role": "system|user|assistant", "content": "string", "timestamp": "ISODate" }]
}

GET /cv/{cv_id}/chat/history

Retrieve chat history.
Query: limit?: number (default 50)
Returns:

[{ "role": "system|user|assistant", "content": "string", "timestamp": "ISODate" }]

📝 CV Quality Evaluation
POST /cv/{cv_id}/quality/evaluate

Evaluate CV quality.
Returns:

{
  "score": number,
  "rubric": { ... },
  "strengths": ["string"],
  "improvements": [{ "area": "string", "issue": "string", "fix_example": "string" }],
  "rewritten_examples": { "summary": "string?", "bullets": ["string"]? }
}

GET /cv/{cv_id}/quality

Retrieve last saved evaluation.

💼 Jobs (Admin)
POST /admin/jobs/generate

Generate sample jobs.

Role: admin
Body:

{ "count?": number }


Returns:

{ "inserted": number }

POST /admin/jobs

Create a new job.

Role: admin
Body:

{ "title": "string", "company": "string", "location": "string", "description": "string", "tags?": ["string"] }


Returns:

{ "job_id": "string" }

PUT /admin/jobs/{job_id}

Update a job.

Role: admin
Body: Partial job fields
Returns:

{ "updated": true }

DELETE /admin/jobs/{job_id}

Delete a job.

Role: admin
Returns:

{ "deleted": true }

GET /admin/jobs

List jobs with optional filters.

Role: admin
Query: search?, page=1, limit=20
Returns:

{ "jobs": [...], "total": number }

💼 Jobs (User/HR)
POST /match/cv/{cv_id}

Find best job matches for CV.
Body:

{
  "top_k?": number,
  "filters?": { "location?": "string", "remote?": boolean, "min_score?": number },
  "strategy?": { "weights?": { "similarity?": number, "exact_skill?": number, "seniority?": number } }
}


Returns:

{
  "matches": [
    { "job_id": "string", "title": "string", "company": "string", "location": "string", "url?": "string",
      "score": number, "similarity": number, "matched_skills": ["string"], "explanation?": "string" }
  ],
  "total": number
}

GET /jobs/{job_id}

Retrieve job details.

GET /jobs

List jobs with optional filters.
Query: search?, tags?, page?, limit?
Returns:

{ "jobs": [...], "total": number }

🛡️ Admin Console & Audit
GET /admin/cv

List CVs.

Role: admin
Returns:

[{ "cv_id": "string", "user_id": "string", "created_at": "ISODate", "file": "string", "quality_score?": number, "chat_count?": number, "summary?": "string" }]

GET /admin/cv/{cv_id}

Retrieve full CV record.

Role: admin

GET /admin/actions

List admin actions.

Role: admin
Returns:

{ "actions": [{ "id": "string", "admin_id": "string", "action_type": "string", "payload": {}, "timestamp": "ISODate" }], "total": number }


---

Would you like me to also **merge the API.md and DATA_MODEL.md into a single "Developer Docs" index** with cross-links, so contributors can navigate between API and Data Model easily?