from typing import List, Tuple

def compare_skills(resume_skills: List[str], job_skills: List[str]) -> Tuple[List[str], List[str]]:
    """
    Compares resume skills against job skills (case-insensitive).
    Returns (matched_skills, missing_skills).
    """
    resume_skills_lower = {s.lower(): s for s in resume_skills}
    
    matched = []
    missing = []
    
    for js in job_skills:
        if js.lower() in resume_skills_lower:
            matched.append(resume_skills_lower[js.lower()])
        else:
            missing.append(js)
            
    return matched, missing
