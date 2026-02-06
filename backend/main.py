from fastapi import FastAPI, Depends, Security, HTTPException, UploadFile, File, Form, status, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from core.auth import verify_api_key
from models.analysis import AnalysisInput, AnalysisOutput
from models.resume import ResumeParsedData
from models.posting import PostingParsedData
from logic.skills import compare_skills
from logic.experience import check_experience_fit
from logic.recommendations import generate_recommendations
from core.pdf import extract_text_from_pdf
from core.llm import parse_resume_with_llm, parse_posting_with_llm
from core.database import get_supabase_client
import os
import shutil
import tempfile
from typing import Optional, Dict, Any
from uuid import UUID

app = FastAPI()

# --- Schemas for Requests ---
class PostingCreate(BaseModel):
    company_name: Optional[str] = None
    raw_text: str

class ResumeUpdate(BaseModel):
    parsed_data: Dict[str, Any]

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
    return JSONResponse(
        status_code=status_code,
        content={"success": True, "data": data}
    )

@app.get("/")
def read_root():
    return {"Hello": "Fit-Gap API"}

@app.post("/api/v1/analyze", dependencies=[Depends(verify_api_key)])
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

# --- Resume API ---

@app.post("/api/v1/resumes", dependencies=[Depends(verify_api_key)])
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

@app.get("/api/v1/resumes/{resume_id}", dependencies=[Depends(verify_api_key)])
def get_resume(resume_id: UUID):
    supabase = get_supabase_client()
    res = supabase.table("resumes").select("*").eq("id", str(resume_id)).single().execute()
    
    if not res.data:
        raise FitGapException("NOT_FOUND", "Resume not found", 404)
        
    return success_response({
        "resume_id": res.data["id"],
        "parsed_data": res.data["parsed_data"],
        "created_at": res.data.get("created_at")
    })

@app.patch("/api/v1/resumes/{resume_id}", dependencies=[Depends(verify_api_key)])
def update_resume(resume_id: UUID, update: ResumeUpdate):
    supabase = get_supabase_client()
    
    # 1. Fetch current
    current = supabase.table("resumes").select("parsed_data").eq("id", str(resume_id)).single().execute()
    if not current.data:
        raise FitGapException("NOT_FOUND", "Resume not found", 404)
        
    # 2. Merge parsed_data (top-level fields)
    new_parsed_data = current.data["parsed_data"].copy()
    new_parsed_data.update(update.parsed_data)
    
    # 3. Update
    res = supabase.table("resumes").update({"parsed_data": new_parsed_data}).eq("id", str(resume_id)).execute()
    
    if not res.data:
        raise FitGapException("INTERNAL_ERROR", "Failed to update resume", 500)
        
    return success_response({
        "resume_id": res.data[0]["id"],
        "parsed_data": res.data[0]["parsed_data"],
        "updated_at": res.data[0].get("updated_at")
    })

@app.delete("/api/v1/resumes/{resume_id}", dependencies=[Depends(verify_api_key)])
def delete_resume(resume_id: UUID):
    supabase = get_supabase_client()
    res = supabase.table("resumes").delete().eq("id", str(resume_id)).execute()
    
    if not res.data:
        raise FitGapException("NOT_FOUND", "Resume not found or already deleted", 404)
        
    # Optional: Delete from storage if existed (omitting complex storage check for MVP)
    
    return success_response({"message": "서류가 삭제되었습니다."})

# --- Job Posting API ---

@app.post("/api/v1/postings", status_code=201, dependencies=[Depends(verify_api_key)])
async def create_posting(posting: PostingCreate):
    if len(posting.raw_text) < 100:
        raise FitGapException("TEXT_TOO_SHORT", "Job posting text must be at least 100 characters", 400)
        
    try:
        parsed_data = await parse_posting_with_llm(posting.raw_text)
        supabase = get_supabase_client()
        db_data = {
            "company_name": posting.company_name,
            "raw_text": posting.raw_text,
            "parsed_data": parsed_data.dict()
        }
        res = supabase.table("job_postings").insert(db_data).execute()
        
        if not res.data:
            raise FitGapException("INTERNAL_ERROR", "Failed to save posting to database", 500)
            
        return success_response({
            "posting_id": res.data[0]["id"],
            "company_name": res.data[0].get("company_name"),
            "parsed_data": parsed_data.dict(),
            "created_at": res.data[0].get("created_at")
        }, status_code=201)
        
    except Exception as e:
        if isinstance(e, FitGapException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))