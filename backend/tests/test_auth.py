import pytest
from fastapi.testclient import TestClient
from main import app
import os

client = TestClient(app)

@pytest.fixture
def mock_api_key():
    key = "test-api-key-123"
    os.environ["API_KEY"] = key
    return key

def test_auth_missing_header():
    response = client.get("/")
    # Even the root might need auth based on "All endpoints defined below must be protected"
    # Wait, usually root is public, but let's see if we should protect it or a specific sub-path.
    # The spec says "All endpoints defined below must be protected". 
    # Let's test a protected endpoint like /api/v1/resumes
    response = client.post("/resumes")
    assert response.status_code == 401 # FastAPI HTTPBearer returns 401 if missing header by default

def test_auth_invalid_key(mock_api_key):
    response = client.post("/resumes", headers={"Authorization": "Bearer invalid-key"})
    assert response.status_code == 401

def test_auth_valid_key(mock_api_key):
    # This might fail with 404 if the endpoint is not implemented, but it should pass the auth check
    response = client.post("/resumes", headers={"Authorization": f"Bearer {mock_api_key}"})
    assert response.status_code != 401
    assert response.status_code != 403

def test_auth_no_server_config(monkeypatch):
    monkeypatch.delenv("API_KEY", raising=False)
    # Using auth to trigger the check
    response = client.post("/resumes", headers={"Authorization": "Bearer some-key"})
    assert response.status_code == 500
