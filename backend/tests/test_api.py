import pytest
from fastapi.testclient import TestClient
from main import app
import os

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_api_key():
    key = "test-api-key-123"
    os.environ["API_KEY"] = key
    return key

def test_analyze_endpoint_success(mock_api_key):
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
    response = client.post("/api/v1/analyze", json=payload, headers={"Authorization": f"Bearer {mock_api_key}"})
    
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["overall_score"] > 0
    assert "Python" in data["matched_skills"]
    assert "SQL" in data["missing_skills"]
    assert data["experience_alignment"] == "Matches"
    assert len(data["recommendations"]) > 0

def test_analyze_endpoint_invalid_input(mock_api_key):
    response = client.post("/api/v1/analyze", json={"invalid": "data"}, headers={"Authorization": f"Bearer {mock_api_key}"})
    assert response.status_code == 422
