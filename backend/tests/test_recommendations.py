import pytest
from logic.recommendations import generate_recommendations

def test_generate_recommendations_basic():
    missing_skills = ["Python", "Docker"]
    recommendations = generate_recommendations(missing_skills)
    
    assert "Consider gaining experience with Python to match this requirement." in recommendations
    assert "Consider gaining experience with Docker to match this requirement." in recommendations
    assert len(recommendations) == 2

def test_generate_recommendations_empty():
    assert generate_recommendations([]) == []
