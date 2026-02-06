import pytest
from logic.experience import check_experience_fit

def test_check_experience_fit_matches():
    # Resume total: 3 years. Job required: 2 years.
    resume_exp = [{"role": "Dev", "years": 1}, {"role": "Senior", "years": 2}]
    job_min_years = 2
    
    alignment = check_experience_fit(resume_exp, job_min_years)
    assert alignment == "Matches"

def test_check_experience_fit_exceeds():
    # Resume total: 10 years. Job required: 3 years.
    resume_exp = [{"role": "Dev", "years": 10}]
    job_min_years = 3
    
    alignment = check_experience_fit(resume_exp, job_min_years)
    assert alignment == "Exceeds"

def test_check_experience_fit_below():
    # Resume total: 1 year. Job required: 5 years.
    resume_exp = [{"role": "Intern", "years": 1}]
    job_min_years = 5
    
    alignment = check_experience_fit(resume_exp, job_min_years)
    assert alignment == "Below"

def test_check_experience_fit_partial():
    # Resume total: 1.8 years. Job required: 2 years.
    # Let's say if it's within 20% of the requirement but below, it's "Partial".
    resume_exp = [{"role": "Dev", "years": 1.8}]
    job_min_years = 2
    
    alignment = check_experience_fit(resume_exp, job_min_years)
    assert alignment == "Partial"
