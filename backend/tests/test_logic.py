import pytest
from logic.skills import compare_skills

def test_compare_skills_exact_match():
    resume_skills = ["Python", "Java", "SQL"]
    job_skills = ["Python", "SQL", "Docker"]
    
    matched, missing = compare_skills(resume_skills, job_skills)
    
    assert set(matched) == {"Python", "SQL"}
    assert set(missing) == {"Docker"}

def test_compare_skills_case_insensitive():
    resume_skills = ["python", "JAVA"]
    job_skills = ["Python", "java", "Docker"]
    
    matched, missing = compare_skills(resume_skills, job_skills)
    
    assert set(matched) == {"python", "JAVA"}
    assert set(missing) == {"Docker"}
