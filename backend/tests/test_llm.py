import pytest
from core.llm import generate_resume_prompt, parse_llm_resume_response
from models.resume import ResumeParsedData

def test_generate_resume_prompt():
    raw_text = "Experienced Python developer with 5 years in FastAPI."
    prompt = generate_resume_prompt(raw_text)
    assert "Experienced Python developer" in prompt
    assert "JSON" in prompt

def test_parse_llm_resume_response():
    mock_response = """
    {
        "skills": [{"name": "Python", "level": "Expert", "source": "5 years"}],
        "experiences": [{"title": "Dev", "duration": "2020-2023", "description": "coding", "achievements": ["done"]}],
        "metrics": [{"value": "100%", "context": "uptime"}],
        "soft_skills": ["comm"],
        "keywords": ["fast"]
    }
    """
    parsed = parse_llm_resume_response(mock_response)
    assert isinstance(parsed, ResumeParsedData)
    assert parsed.skills[0].name == "Python"

def test_parse_llm_resume_response_with_markdown():
    mock_response = """
    ```json
    {
        "skills": [{"name": "Java", "level": "Expert", "source": "5 years"}],
        "experiences": [],
        "metrics": [],
        "soft_skills": [],
        "keywords": []
    }
    ```
    """
    parsed = parse_llm_resume_response(mock_response)
    assert parsed.skills[0].name == "Java"
