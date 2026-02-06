import pytest
from pydantic import ValidationError
from models.analysis import AnalysisInput, AnalysisOutput

def test_analysis_input_validation():
    # Valid input
    valid_input = {
        "resume_data": {
            "skills": ["Python", "FastAPI"],
            "experience": [{"role": "Backend Dev", "years": 3}]
        },
        "job_data": {
            "required_skills": ["Python", "SQL"],
            "min_experience": 2
        }
    }
    input_model = AnalysisInput(**valid_input)
    assert input_model.resume_data["skills"] == ["Python", "FastAPI"]

    # Invalid input
    with pytest.raises(ValidationError):
        AnalysisInput(resume_data="invalid")

def test_analysis_output_validation():
    valid_output = {
        "overall_score": 0.85,
        "matched_skills": ["Python"],
        "missing_skills": ["SQL"],
        "recommendations": ["Learn SQL"],
        "experience_alignment": "Matches"
    }
    output_model = AnalysisOutput(**valid_output)
    assert output_model.overall_score == 0.85
