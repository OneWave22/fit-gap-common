from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from uuid import UUID

class ResumeSkill(BaseModel):
    name: str
    level: str
    source: str

class ResumeExperience(BaseModel):
    title: str
    duration: str
    description: str
    achievements: List[str]

class ResumeMetric(BaseModel):
    value: str
    context: str

class ResumeParsedData(BaseModel):
    skills: List[ResumeSkill]
    experiences: List[ResumeExperience]
    metrics: List[ResumeMetric]
    soft_skills: List[str]
    keywords: List[str]

class Resume(BaseModel):
    id: UUID
    user_id: Optional[UUID] = None
    parsed_data: ResumeParsedData
    created_at: datetime
    updated_at: Optional[datetime] = None
