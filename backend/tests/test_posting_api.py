import pytest
from fastapi.testclient import TestClient
from main import app
import os
from uuid import uuid4

client = TestClient(app)

@pytest.fixture
def mock_auth():
    os.environ["API_KEY"] = "test-key"
    return {"Authorization": "Bearer test-key"}

def test_post_posting_success(mocker, mock_auth):
    # Mock LLM parsing (async)
    mock_parsed_data = mocker.MagicMock()
    mock_parsed_data.dict.return_value = {"required_skills": []}
    mocker.patch("main.parse_posting_with_llm", return_value=mock_parsed_data)
    
    # Mock Supabase
    mock_db_instance = mocker.MagicMock()
    mocker.patch("main.get_supabase_client", return_value=mock_db_instance)
    mock_db_instance.table().insert().execute.return_value = mocker.MagicMock(data=[{"id": str(uuid4()), "created_at": "now"}])
    
    payload = {
        "company_name": "Tech Startup A",
        "raw_text": "We need a Python developer..." * 10 # To meet minimum length if needed
    }
    
    response = client.post("/api/v1/postings", json=payload, headers=mock_auth)
    
    assert response.status_code == 201
    assert response.json()["success"] == True
    assert "posting_id" in response.json()["data"]

def test_post_posting_missing_raw_text(mock_auth):
    response = client.post("/api/v1/postings", json={"company_name": "Test"}, headers=mock_auth)
    assert response.status_code == 422 # Pydantic validation error
