import pytest
from uuid import uuid4
from datetime import datetime
from models.resume import Resume, ResumeParsedData
from models.posting import JobPosting, PostingParsedData

def test_resume_model_validation():
    data = {
        "id": uuid4(),
        "parsed_data": {
            "skills": [{"name": "Python", "level": "Expert", "source": "5 years"}],
            "experiences": [{"title": "Dev", "duration": "2020-2023", "description": "coding", "achievements": ["done"]}],
            "metrics": [{"value": "100%", "context": "uptime"}],
            "soft_skills": ["comm"],
            "keywords": ["fast"]
        },
        "created_at": datetime.utcnow()
    }
    resume = Resume(**data)
    assert resume.parsed_data.skills[0].name == "Python"

def test_posting_model_validation():
    data = {
        "id": uuid4(),
        "company_name": "Tech Co",
        "parsed_data": {
            "required_skills": [{"name": "Python", "detail": "2 years", "source": "JD"}],
            "preferred_skills": [],
            "responsibilities": ["coding"],
            "culture_keywords": ["fast"]
        },
        "created_at": datetime.utcnow()
    }
    posting = JobPosting(**data)
    assert posting.company_name == "Tech Co"
