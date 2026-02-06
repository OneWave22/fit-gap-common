from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from uuid import UUID

class PostingSkill(BaseModel):
    name: str
    detail: str
    source: str

class PostingParsedData(BaseModel):
    required_skills: List[PostingSkill]
    preferred_skills: List[PostingSkill]
    responsibilities: List[str]
    required_experience: List[str] = []
    culture_keywords: List[str]

class JobPosting(BaseModel):
    id: UUID
    company_name: Optional[str] = None
    parsed_data: PostingParsedData
    created_at: datetime
    updated_at: Optional[datetime] = None
