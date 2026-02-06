import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_analyze_endpoint_success():
    payload = {
        "resume_data": {
            "skills": ["Python", "FastAPI"],
            "experience": [{"role": "Dev", "years": 3}]
        },
        "job_data": {
            "required_skills": ["Python", "SQL", "Docker"],
            "min_experience": 2
        }
    }
    response = client.post("/api/v1/analyze", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["overall_score"] > 0
    assert "Python" in data["matched_skills"]
    assert "SQL" in data["missing_skills"]
    assert data["experience_alignment"] == "Matches"
    assert len(data["recommendations"]) > 0

def test_analyze_endpoint_invalid_input():
    response = client.post("/api/v1/analyses", json={"invalid": "data"})
    assert response.status_code == 422
