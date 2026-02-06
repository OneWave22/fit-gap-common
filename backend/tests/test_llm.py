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
    # ... (existing java test)
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

def test_generate_posting_prompt():
    from core.llm import generate_posting_prompt
    raw_text = "Looking for a Python expert with 2 years of SQL."
    prompt = generate_posting_prompt(raw_text)
    assert "Python expert" in prompt
    assert "required_skills" in prompt

def test_parse_llm_posting_response():
    from core.llm import parse_llm_posting_response
    from models.posting import PostingParsedData
    mock_response = """
    {
        "required_skills": [{"name": "Python", "detail": "Expert", "source": "Text"}],
        "preferred_skills": [],
        "responsibilities": ["Coding"],
        "culture_keywords": ["Fast"]
    }
    """
    parsed = parse_llm_posting_response(mock_response)
    assert isinstance(parsed, PostingParsedData)
    assert parsed.required_skills[0].name == "Python"
