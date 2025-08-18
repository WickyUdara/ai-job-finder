from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional

class CVUploadResponse(BaseModel):
    cv_id: str
    filename: str
    ocr_used: bool

class CVBasicInfo(BaseModel):
    cv_id: str
    filename: str
    ocr_used: bool
    raw_text_preview: str

class QualityRubric(BaseModel):
    ats_readiness: Optional[int] = None
    clarity: Optional[int] = None
    quantification: Optional[int] = None
    keyword_coverage: Optional[int] = None
    structure_formatting: Optional[int] = None
    consistency: Optional[int] = None

class ImprovementItem(BaseModel):
    area: str
    issue: str
    fix_example: Optional[str] = None

class RewrittenExamples(BaseModel):
    summary: Optional[str] = None
    bullets: Optional[List[str]] = None

class QualityReport(BaseModel):
    score: int
    rubric: QualityRubric
    strengths: List[str]
    improvements: List[ImprovementItem]
    rewritten_examples: Optional[Any] = None  # Can be dict or list depending on LLM output
    evaluated_at: Optional[str] = None  # Or use datetime type for more control
    raw: Optional[str] = None  # For fallback/debug


class Job(BaseModel):
    job_id: Optional[str]
    title: str
    description: str
    requirements: List[str]
    skills: List[str]
    employer: Optional[str] = None
    location: Optional[str] = None
    embedding: Optional[List[float]] = None  # LLM job vector

class JobMatchResult(BaseModel):
    job_id: str
    title: str
    score: float
    why: Optional[str]

