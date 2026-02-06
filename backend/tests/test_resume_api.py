import pytest
from fastapi.testclient import TestClient
from main import app
import os
from uuid import uuid4
import fitz

client = TestClient(app)

@pytest.fixture
def mock_auth():
    os.environ["API_KEY"] = "test-key"
    return {"Authorization": "Bearer test-key"}

@pytest.fixture
def valid_pdf_content():
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Resume Content")
    content = doc.tobytes()
    doc.close()
    return content

def test_post_resume_success(mocker, mock_auth, valid_pdf_content):
    # Mock PDF extraction
    mocker.patch("main.extract_text_from_pdf", return_value="Mock Resume Text")
    
    # Mock LLM parsing (async)
    mock_parsed_data = mocker.MagicMock()
    mock_parsed_data.dict.return_value = {"skills": []}
    mocker.patch("main.parse_resume_with_llm", return_value=mock_parsed_data)
    
    # Mock Supabase
    mock_db_instance = mocker.MagicMock()
    mocker.patch("main.get_supabase_client", return_value=mock_db_instance)
    mock_db_instance.table().insert().execute.return_value = mocker.MagicMock(data=[{"id": str(uuid4()), "created_at": "now"}])
    
    files = {"file": ("resume.pdf", valid_pdf_content, "application/pdf")}
    
    response = client.post("/api/v1/resumes", files=files, headers=mock_auth)
    
    assert response.status_code == 201
    assert response.json()["success"] == True
    assert "resume_id" in response.json()["data"]

def test_post_resume_invalid_file_type(mock_auth):
    files = {"file": ("test.txt", b"plain text", "text/plain")}
    response = client.post("/api/v1/resumes", files=files, headers=mock_auth)
    assert response.status_code == 400
    assert response.json()["success"] == False
    assert response.json()["error"]["code"] == "UNSUPPORTED_FILE_TYPE"