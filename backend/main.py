from fastapi import FastAPI, HTTPException
from models.analysis import AnalysisInput, AnalysisOutput
from logic.skills import compare_skills
from logic.experience import check_experience_fit
from logic.recommendations import generate_recommendations

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "Fit-Gap API"}

@app.post("/api/v1/analyses", response_model=AnalysisOutput)
def analyze_fit_gap(input_data: AnalysisInput):
    """
    Analyzes the fit-gap between a resume and a job posting.
    """
    try:
        resume_skills = input_data.resume_data.get("skills", [])
        job_skills = input_data.job_data.get("required_skills", [])
        
        # 1. Skill Matching
        matched_skills, missing_skills = compare_skills(resume_skills, job_skills)
        
        # 2. Experience Alignment
        resume_exp = input_data.resume_data.get("experience", [])
        job_min_years = input_data.job_data.get("min_experience", 0)
        experience_alignment = check_experience_fit(resume_exp, job_min_years)
        
        # 3. Recommendations
        recommendations = generate_recommendations(missing_skills)
        
        # 4. Scoring (Basic weighted average for MVP)
        skill_score = len(matched_skills) / len(job_skills) if job_skills else 1.0
        # Experience weight (Matches=1.0, Exceeds=1.0, Partial=0.5, Below=0.0)
        exp_weight = {"Exceeds": 1.0, "Matches": 1.0, "Partial": 0.5, "Below": 0.0}.get(experience_alignment, 0.0)
        
        overall_score = (skill_score * 0.7) + (exp_weight * 0.3)
        
        return AnalysisOutput(
            overall_score=overall_score,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            recommendations=recommendations,
            experience_alignment=experience_alignment
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))