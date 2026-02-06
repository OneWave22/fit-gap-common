from typing import List, Dict, Any

def check_experience_fit(resume_experience: List[Dict[str, Any]], job_min_years: int) -> str:
    """
    Calculates total years of experience and compares with job requirement.
    Returns "Exceeds", "Matches", "Partial", or "Below".
    """
    total_years = sum(exp.get("years", 0) for exp in resume_experience)
    
    if total_years >= job_min_years * 2.0:
        return "Exceeds"
    elif total_years >= job_min_years:
        return "Matches"
    elif total_years >= job_min_years * 0.8:
        return "Partial"
    else:
        return "Below"
