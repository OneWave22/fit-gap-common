from fastapi import FastAPI, Depends, Security, HTTPException, UploadFile, File, Form, status, Request
from fastapi.responses import JSONResponse
from core.auth import verify_api_key
from models.analysis import AnalysisInput, AnalysisOutput
from models.resume import ResumeParsedData
from logic.skills import compare_skills
from logic.experience import check_experience_fit
from logic.recommendations import generate_recommendations
from core.pdf import extract_text_from_pdf
from core.llm import parse_resume_with_llm
from core.database import get_supabase_client
import os
import shutil
import tempfile
from typing import Optional

app = FastAPI()

# Custom exception for our standardized error format
class FitGapException(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code

@app.exception_handler(FitGapException)
async def fitgap_exception_handler(request: Request, exc: FitGapException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.code,
                "message": exc.message
            }
        }
    )

# Standard success response wrapper
def success_response(data: dict, status_code: int = 200):
    return {"success": True, "data": data}

@app.get("/")
def read_root():
    return {"Hello": "Fit-Gap API"}

@app.post("/api/v1/analyze", response_model=None, dependencies=[Depends(verify_api_key)])
def analyze_fit_gap(input_data: AnalysisInput):
    try:
        resume_skills = input_data.resume_data.get("skills", [])
        job_skills = input_data.job_data.get("required_skills", [])
        matched_skills, missing_skills = compare_skills(resume_skills, job_skills)
        resume_exp = input_data.resume_data.get("experience", [])
        job_min_years = input_data.job_data.get("min_experience", 0)
        experience_alignment = check_experience_fit(resume_exp, job_min_years)
        recommendations = generate_recommendations(missing_skills)
        skill_score = len(matched_skills) / len(job_skills) if job_skills else 1.0
        exp_weight = {"Exceeds": 1.0, "Matches": 1.0, "Partial": 0.5, "Below": 0.0}.get(experience_alignment, 0.0)
        overall_score = (skill_score * 0.7) + (exp_weight * 0.3)
        
        return success_response({
            "overall_score": overall_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "recommendations": recommendations,
            "experience_alignment": experience_alignment
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/resumes", status_code=201, dependencies=[Depends(verify_api_key)])
async def upload_resume(
    file: UploadFile = File(...),
    store_original: bool = Form(False)
):
    if not file.filename.lower().endswith(".pdf"):
        raise FitGapException("UNSUPPORTED_FILE_TYPE", "Only PDF files are supported", 400)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name
        
    try:
        raw_text = extract_text_from_pdf(tmp_path)
        parsed_data = await parse_resume_with_llm(raw_text)
        
        supabase = get_supabase_client()
        db_data = {
            "raw_text": raw_text,
            "parsed_data": parsed_data.dict(),
            "is_stored": store_original
        }
        res = supabase.table("resumes").insert(db_data).execute()
        
        if not res.data:
            raise FitGapException("INTERNAL_ERROR", "Failed to save to database", 500)
            
        resume_id = res.data[0]["id"]
        
        if store_original:
            with open(tmp_path, "rb") as f:
                supabase.storage.from_("resumes").upload(f"{resume_id}.pdf", f)
                
        return success_response({
            "resume_id": resume_id,
            "parsed_data": parsed_data.dict(),
            "created_at": res.data[0].get("created_at")
        }, status_code=201)
        
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

@app.post("/api/v1/postings", dependencies=[Depends(verify_api_key)])
def create_posting():
    return success_response({"message": "Success"})