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

def test_get_posting_success(mocker, mock_auth):
    posting_id = str(uuid4())
    mock_db_instance = mocker.MagicMock()
    mocker.patch("main.get_supabase_client", return_value=mock_db_instance)
    mock_db_instance.table().select().eq().single().execute.return_value = mocker.MagicMock(data={"id": posting_id, "company_name": "Test Co", "parsed_data": {}})
    
    response = client.get(f"/api/v1/postings/{posting_id}", headers=mock_auth)
    assert response.status_code == 200
    assert response.json()["data"]["posting_id"] == posting_id

def test_patch_posting_success(mocker, mock_auth):
    posting_id = str(uuid4())
    mock_db_instance = mocker.MagicMock()
    mocker.patch("main.get_supabase_client", return_value=mock_db_instance)
    
    # Mock LLM re-parsing
    mock_parsed_data = mocker.MagicMock()
    mock_parsed_data.dict.return_value = {"required_skills": ["New Skill"]}
    mocker.patch("main.parse_posting_with_llm", return_value=mock_parsed_data)
    
    # Mock update
    mock_db_instance.table().update().eq().execute.return_value = mocker.MagicMock(data=[{"id": posting_id, "parsed_data": {"required_skills": ["New Skill"]}}])
    
    payload = {"raw_text": "Updated long text..." * 10}
    response = client.patch(f"/api/v1/postings/{posting_id}", json=payload, headers=mock_auth)
    
    assert response.status_code == 200
    assert response.json()["data"]["parsed_data"]["required_skills"] == ["New Skill"]

def test_delete_posting_success(mocker, mock_auth):
    posting_id = str(uuid4())
    mock_db_instance = mocker.MagicMock()
    mocker.patch("main.get_supabase_client", return_value=mock_db_instance)
    mock_db_instance.table().delete().eq().execute.return_value = mocker.MagicMock(data=[{"id": posting_id}])
    
    response = client.delete(f"/api/v1/postings/{posting_id}", headers=mock_auth)
    assert response.status_code == 200
    assert "삭제되었습니다" in response.json()["data"]["message"]
