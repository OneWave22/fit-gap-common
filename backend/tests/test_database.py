import pytest
import os
from unittest.mock import patch, MagicMock
from core.database import get_supabase_client, _reset_supabase_client

@pytest.fixture(autouse=True)
def reset_db_client():
    _reset_supabase_client()
    yield
    _reset_supabase_client()

@pytest.fixture
def mock_env_vars():
    with patch.dict(os.environ, {
        "SUPABASE_URL": "https://test.supabase.co",
        "SUPABASE_SERVICE_KEY": "test-key"
    }):
        yield

def test_get_supabase_client_success(mock_env_vars):
    with patch("core.database.create_client") as mock_create:
        mock_create.return_value = MagicMock()
        client = get_supabase_client()
        assert client is not None
        mock_create.assert_called_once_with("https://test.supabase.co", "test-key")
        
        # Second call should reuse the same client
        client2 = get_supabase_client()
        assert client2 is client
        assert mock_create.call_count == 1

def test_get_supabase_client_missing_config(monkeypatch):
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    with pytest.raises(RuntimeError, match="Supabase configuration missing"):
        get_supabase_client()