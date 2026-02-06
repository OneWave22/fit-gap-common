from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class AnalysisInput(BaseModel):
    resume_data: Dict[str, Any]
    job_data: Dict[str, Any]

class AnalysisOutput(BaseModel):
    overall_score: float
    matched_skills: List[str]
    missing_skills: List[str]
    recommendations: List[str]
    experience_alignment: str
