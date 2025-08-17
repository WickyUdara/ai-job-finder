from pydantic import BaseModel

class CVUploadResponse(BaseModel):
    cv_id: str
    filename: str
    ocr_used: bool

class CVBasicInfo(BaseModel):
    cv_id: str
    filename: str
    ocr_used: bool
    raw_text_preview: str
