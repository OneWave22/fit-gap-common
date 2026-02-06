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
    # Test a protected endpoint
    response = client.post("/api/v1/resumes")
    assert response.status_code == 401 

def test_auth_invalid_key(mock_api_key):
    response = client.post("/api/v1/resumes", headers={"Authorization": "Bearer invalid-key"})
    assert response.status_code == 401

def test_auth_valid_key(mock_api_key):
    # This might return 422 if body is missing, but should NOT be 401/403
    response = client.post("/api/v1/resumes", headers={"Authorization": f"Bearer {mock_api_key}"})
    assert response.status_code != 401
    assert response.status_code != 403

def test_auth_no_server_config(monkeypatch):
    monkeypatch.delenv("API_KEY", raising=False)
    # Using auth to trigger the check
    response = client.post("/api/v1/resumes", headers={"Authorization": "Bearer some-key"})
    assert response.status_code == 500