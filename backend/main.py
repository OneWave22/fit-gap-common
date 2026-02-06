from fastapi import FastAPI, Depends, Security, HTTPException, UploadFile, File, Form, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel, Field
from core.auth import verify_api_key
from core.security import (
    create_access_token,
    create_refresh_token,
    create_signup_token,
    create_state_token,
    decode_token,
    get_cookie_settings,
    require_access_token,
    require_signup_token,
)
from core.google_oauth import build_google_auth_url, exchange_code_for_tokens, verify_google_id_token
from integrations.biz_verify import verify_biz_registration
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
from datetime import datetime, timezone
import shutil
import tempfile
from typing import Optional, Dict, Any, Literal
from uuid import UUID

app = FastAPI()

_allowed_origins = os.getenv("CORS_ALLOW_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in _allowed_origins if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def _get_int_env(name: str, default: int) -> int:
    val = os.getenv(name)
    if not val:
        return default
    try:
        return int(val)
    except ValueError:
        return default

# --- Schemas for Requests ---
class PostingCreate(BaseModel):
    company_name: Optional[str] = None
    raw_text: str

class PostingUpdate(BaseModel):
    company_name: Optional[str] = None
    raw_text: Optional[str] = None

class ResumeUpdate(BaseModel):
    parsed_data: Dict[str, Any]

class NicknameUpdate(BaseModel):
    nickname: str

class ResumeTextUpdate(BaseModel):
    raw_text: str

class AnalysisRequest(BaseModel):
    resume_id: UUID
    posting_id: UUID

class AnalysisRead(BaseModel):
    analysis_id: UUID

class IdTokenRequest(BaseModel):
    id_token: str

class OnboardingComplete(BaseModel):
    role: Literal["JOBSEEKER", "COMPANY"]
    jobseeker_type: Optional[str] = Field(None, alias="jobseekerType")
    nickname: Optional[str] = None
    company_name: Optional[str] = Field(None, alias="companyName")
    biz_reg_no: Optional[str] = Field(None, alias="bizRegNo")

    model_config = {"populate_by_name": True}

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

def _set_refresh_cookie(response, refresh_token: str):
    cookie_opts = get_cookie_settings()
    response.set_cookie("refresh_token", refresh_token, httponly=True, **cookie_opts)

def _clear_refresh_cookie(response):
    cookie_opts = get_cookie_settings()
    response.delete_cookie("refresh_token", **cookie_opts)

@app.get("/")
def read_root():
    return {"Hello": "Fit-Gap API"}

# --- Auth API ---

@app.get("/auth/google/start")
def google_auth_start():
    state = create_state_token(ttl_minutes=10)
    url = build_google_auth_url(state)
    return RedirectResponse(url=url)

@app.get("/api/auth/callback/google")
def google_auth_callback(code: str, state: str):
    payload = decode_token(state)
    if payload.get("typ") != "state":
        raise FitGapException("INVALID_STATE", "Invalid OAuth state", 400)

    try:
        token_res = exchange_code_for_tokens(code)
        id_token = token_res.get("id_token")
        if not id_token:
            raise FitGapException(
                "GOOGLE_TOKEN_EXCHANGE_FAILED",
                f"Missing id_token. keys={list(token_res.keys())}",
                400,
            )
        id_payload = verify_google_id_token(id_token)
    except FitGapException:
        raise
    except Exception as e:
        raise FitGapException("GOOGLE_TOKEN_EXCHANGE_FAILED", str(e), 400)

    provider_sub = id_payload.get("sub")
    email = id_payload.get("email")
    if not provider_sub:
        raise FitGapException("INVALID_ID_TOKEN", "Invalid id_token payload", 400)

    supabase = get_supabase_client()
    oauth = (
        supabase.table("oauth_accounts")
        .select("*")
        .eq("provider", "GOOGLE")
        .eq("provider_sub", provider_sub)
        .execute()
    )

    user = None
    oauth_row = oauth.data[0] if oauth.data else None
    if oauth_row:
        user = (
            supabase.table("users").select("*").eq("id", oauth_row["user_id"]).single().execute()
        ).data
    else:
        nickname = (email.split("@")[0] if email else "user")
        user_res = (
            supabase.table("users")
            .insert({"email": email, "nickname": nickname, "status": "PENDING_ONBOARDING"})
            .execute()
        )
        if not user_res.data:
            raise FitGapException("INTERNAL_ERROR", "Failed to create user", 500)
        user = user_res.data[0]
        supabase.table("oauth_accounts").insert(
            {
                "user_id": user["id"],
                "provider": "GOOGLE",
                "provider_sub": provider_sub,
                "email": email,
            }
        ).execute()

    frontend_base = os.getenv("FRONTEND_BASE_URL", "https://fit-gap.vercel.app")
    if user.get("status") == "ACTIVE":
        access = create_access_token(
            user_id=user["id"],
            role=user.get("role"),
            ttl_minutes=_get_int_env("ACCESS_TOKEN_TTL_MINUTES", 15),
        )
        refresh = create_refresh_token(
            user_id=user["id"], ttl_days=_get_int_env("REFRESH_TOKEN_TTL_DAYS", 14)
        )
        res = RedirectResponse(url=f"{frontend_base}/login/callback#idToken={id_token}")
        _set_refresh_cookie(res, refresh)
        return res

    signup_token = create_signup_token(
        provider="GOOGLE",
        provider_sub=provider_sub,
        email=email,
        ttl_minutes=_get_int_env("SIGNUP_TOKEN_TTL_MINUTES", 20),
    )
    res = RedirectResponse(url=f"{frontend_base}/onboarding?authToken={signup_token}")
    return res

@app.post("/onboarding/complete")
@app.post("/api/onboarding/complete")
def onboarding_complete(
    payload: OnboardingComplete,
    token_data: Dict[str, Any] = Depends(require_signup_token),
):
    provider_sub = token_data.get("sub")
    email = token_data.get("email")
    if not provider_sub:
        raise FitGapException("ONBOARDING_TOKEN_INVALID", "Invalid signup token", 401)

    supabase = get_supabase_client()
    oauth = (
        supabase.table("oauth_accounts")
        .select("*")
        .eq("provider", "GOOGLE")
        .eq("provider_sub", provider_sub)
        .execute()
    )

    oauth_row = oauth.data[0] if oauth.data else None
    preferred_nickname = payload.nickname or (email.split("@")[0] if email else "user")
    if not oauth_row:
        user_res = (
            supabase.table("users")
            .insert({"email": email, "nickname": preferred_nickname, "status": "PENDING_ONBOARDING"})
            .execute()
        )
        if not user_res.data:
            raise FitGapException("INTERNAL_ERROR", "Failed to create user", 500)
        user = user_res.data[0]
        supabase.table("oauth_accounts").insert(
            {
                "user_id": user["id"],
                "provider": "GOOGLE",
                "provider_sub": provider_sub,
                "email": email,
            }
        ).execute()
    else:
        user = (
            supabase.table("users")
            .select("*")
            .eq("id", oauth_row["user_id"])
            .single()
            .execute()
        ).data

    if user.get("status") == "ACTIVE":
        raise FitGapException("ALREADY_ONBOARDED", "User already onboarded", 400)

    if payload.role == "JOBSEEKER":
        if not payload.jobseeker_type:
            raise FitGapException("INVALID_REQUEST", "jobseeker_type is required", 400)
        if not payload.nickname:
            raise FitGapException("INVALID_REQUEST", "nickname is required", 400)
        supabase.table("jobseeker_profiles").upsert(
            {"user_id": user["id"], "type": payload.jobseeker_type},
            on_conflict="user_id",
        ).execute()
        supabase.table("users").update({"nickname": payload.nickname}).eq("id", user["id"]).execute()
    else:
        if not payload.company_name or not payload.biz_reg_no:
            raise FitGapException("INVALID_REQUEST", "company_name and biz_reg_no are required", 400)
        if not verify_biz_registration(payload.biz_reg_no):
            raise FitGapException("BIZ_VERIFY_FAILED", "사업자 등록번호 인증에 실패했습니다.", 422)
        supabase.table("company_profiles").upsert(
            {
                "user_id": user["id"],
                "company_name": payload.company_name,
                "biz_reg_no": payload.biz_reg_no,
                "biz_verified": True,
                "biz_verified_at": datetime.now(timezone.utc).isoformat(),
            },
            on_conflict="user_id",
        ).execute()

    supabase.table("users").update(
        {"role": payload.role, "status": "ACTIVE"}
    ).eq("id", user["id"]).execute()

    access = create_access_token(
        user_id=user["id"],
        role=payload.role,
        ttl_minutes=_get_int_env("ACCESS_TOKEN_TTL_MINUTES", 15),
    )
    refresh = create_refresh_token(
        user_id=user["id"], ttl_days=_get_int_env("REFRESH_TOKEN_TTL_DAYS", 14)
    )

    res = success_response(
        {
            "user_id": user["id"],
            "role": payload.role,
            "nickname": user.get("nickname"),
            "access_token": access,
            "refresh_token": refresh,
        }
    )
    _set_refresh_cookie(res, refresh)
    return res

@app.post("/api/auth/session")
def create_session(payload: IdTokenRequest):
    try:
        id_payload = verify_google_id_token(payload.id_token)
    except Exception as e:
        raise FitGapException("INVALID_ID_TOKEN", str(e), 401)

    provider_sub = id_payload.get("sub")
    email = id_payload.get("email")
    if not provider_sub:
        raise FitGapException("INVALID_ID_TOKEN", "Missing sub", 401)

    supabase = get_supabase_client()
    oauth = (
        supabase.table("oauth_accounts")
        .select("*")
        .eq("provider", "GOOGLE")
        .eq("provider_sub", provider_sub)
        .execute()
    )
    oauth_row = oauth.data[0] if oauth.data else None
    user = None
    if oauth_row:
        user = (
            supabase.table("users")
            .select("*")
            .eq("id", oauth_row["user_id"])
            .single()
            .execute()
        ).data

    if not user:
        signup_token = create_signup_token(
            provider="GOOGLE",
            provider_sub=provider_sub,
            email=email,
            ttl_minutes=_get_int_env("SIGNUP_TOKEN_TTL_MINUTES", 20),
        )
        return success_response(
            {
                "requires_onboarding": True,
                "auth_token": signup_token,
            }
        )

    if user.get("status") != "ACTIVE":
        signup_token = create_signup_token(
            provider="GOOGLE",
            provider_sub=provider_sub,
            email=email,
            ttl_minutes=_get_int_env("SIGNUP_TOKEN_TTL_MINUTES", 20),
        )
        return success_response(
            {
                "requires_onboarding": True,
                "auth_token": signup_token,
            }
        )

    access = create_access_token(
        user_id=user["id"],
        role=user.get("role"),
        ttl_minutes=_get_int_env("ACCESS_TOKEN_TTL_MINUTES", 15),
    )
    refresh = create_refresh_token(
        user_id=user["id"], ttl_days=_get_int_env("REFRESH_TOKEN_TTL_DAYS", 14)
    )
    res = success_response(
        {
            "access_token": access,
            "refresh_token": refresh,
            "role": user.get("role"),
            "user_id": user.get("id"),
            "nickname": user.get("nickname"),
            "requires_onboarding": False,
        }
    )
    _set_refresh_cookie(res, refresh)
    return res

@app.post("/api/auth/logout")
def logout():
    res = success_response({"message": "logged out"})
    _clear_refresh_cookie(res)
    return res

@app.get("/me")
def get_me(token_data: Dict[str, Any] = Depends(require_access_token)):
    user_id = token_data.get("sub")
    supabase = get_supabase_client()
    user = supabase.table("users").select("*").eq("id", user_id).single().execute().data
    if not user:
        raise FitGapException("NOT_FOUND", "User not found", 404)
    return success_response(
        {
            "id": user["id"],
            "email": user.get("email"),
            "nickname": user.get("nickname"),
            "role": user.get("role"),
            "status": user.get("status"),
        }
    )

@app.get("/api/mypage")
def get_mypage(token_data: Dict[str, Any] = Depends(require_access_token)):
    user_id = token_data.get("sub")
    supabase = get_supabase_client()
    user = supabase.table("users").select("*").eq("id", user_id).single().execute().data
    if not user:
        raise FitGapException("NOT_FOUND", "User not found", 404)

    role = user.get("role")
    profile = None
    resumes = []
    postings = []
    if role == "JOBSEEKER":
        profile_res = (
            supabase.table("jobseeker_profiles")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )
        profile = profile_res.data[0] if profile_res.data else None
        resumes = (
            supabase.table("resumes")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        ).data or []
    elif role == "COMPANY":
        profile_res = (
            supabase.table("company_profiles")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )
        profile = profile_res.data[0] if profile_res.data else None
        postings = (
            supabase.table("job_postings")
            .select("*")
            .eq("created_by", user_id)
            .execute()
        ).data or []

    return success_response(
        {
            "user": {
                "id": user["id"],
                "email": user.get("email"),
                "nickname": user.get("nickname"),
                "role": role,
                "status": user.get("status"),
            },
            "profile": profile,
            "resumes": resumes,
            "postings": postings,
        }
    )

@app.patch("/api/mypage/nickname")
def update_nickname(
    payload: NicknameUpdate, token_data: Dict[str, Any] = Depends(require_access_token)
):
    user_id = token_data.get("sub")
    if not payload.nickname.strip():
        raise FitGapException("INVALID_REQUEST", "nickname is required", 400)
    supabase = get_supabase_client()
    res = (
        supabase.table("users")
        .update({"nickname": payload.nickname.strip()})
        .eq("id", user_id)
        .execute()
    )
    if not res.data:
        raise FitGapException("NOT_FOUND", "User not found", 404)
    return success_response({"nickname": res.data[0].get("nickname")})

@app.put("/api/mypage/resume")
def upsert_resume_text(
    payload: ResumeTextUpdate, token_data: Dict[str, Any] = Depends(require_access_token)
):
    user_id = token_data.get("sub")
    role = token_data.get("role")
    if role != "JOBSEEKER":
        raise FitGapException("FORBIDDEN", "Only jobseeker accounts can edit resumes", 403)
    if not payload.raw_text.strip():
        raise FitGapException("INVALID_REQUEST", "raw_text is required", 400)

    supabase = get_supabase_client()
    existing = (
        supabase.table("resumes")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    ).data
    if existing:
        resume_id = existing[0]["id"]
        res = (
            supabase.table("resumes")
            .update({"raw_text": payload.raw_text, "parsed_data": {}})
            .eq("id", resume_id)
            .execute()
        )
        if not res.data:
            raise FitGapException("INTERNAL_ERROR", "Failed to update resume", 500)
        return success_response({"resume_id": resume_id})

    res = (
        supabase.table("resumes")
        .insert(
            {
                "user_id": user_id,
                "raw_text": payload.raw_text,
                "parsed_data": {},
                "is_stored": False,
            }
        )
        .execute()
    )
    if not res.data:
        raise FitGapException("INTERNAL_ERROR", "Failed to create resume", 500)
    return success_response({"resume_id": res.data[0]["id"]})

@app.delete("/api/mypage")
def delete_account(token_data: Dict[str, Any] = Depends(require_access_token)):
    user_id = token_data.get("sub")
    supabase = get_supabase_client()
    resume_rows = (
        supabase.table("resumes").select("id").eq("user_id", user_id).execute()
    ).data or []
    posting_rows = (
        supabase.table("job_postings")
        .select("id")
        .eq("created_by", user_id)
        .execute()
    ).data or []

    resume_ids = [row["id"] for row in resume_rows]
    posting_ids = [row["id"] for row in posting_rows]

    if resume_ids:
        supabase.table("analyses").delete().in_("resume_id", resume_ids).execute()
    if posting_ids:
        supabase.table("posting_insights").delete().in_("posting_id", posting_ids).execute()
        supabase.table("analyses").delete().in_("posting_id", posting_ids).execute()

    supabase.table("resumes").delete().eq("user_id", user_id).execute()
    supabase.table("job_postings").delete().eq("created_by", user_id).execute()
    supabase.table("jobseeker_profiles").delete().eq("user_id", user_id).execute()
    supabase.table("company_profiles").delete().eq("user_id", user_id).execute()
    supabase.table("oauth_accounts").delete().eq("user_id", user_id).execute()

    res = supabase.table("users").delete().eq("id", user_id).execute()
    if not res.data:
        raise FitGapException("NOT_FOUND", "User not found", 404)
    response = success_response({"message": "Account deleted"})
    _clear_refresh_cookie(response)
    return response

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

@app.post("/analyses")
def create_analysis(
    payload: AnalysisRequest, token_data: Dict[str, Any] = Depends(require_access_token)
):
    user_id = token_data.get("sub")
    supabase = get_supabase_client()

    resume = (
        supabase.table("resumes")
        .select("*")
        .eq("id", str(payload.resume_id))
        .eq("user_id", user_id)
        .single()
        .execute()
    ).data
    if not resume:
        raise FitGapException("NOT_FOUND", "Resume not found", 404)

    posting = (
        supabase.table("job_postings")
        .select("*")
        .eq("id", str(payload.posting_id))
        .single()
        .execute()
    ).data
    if not posting:
        raise FitGapException("NOT_FOUND", "Posting not found", 404)

    resume_parsed = resume.get("parsed_data") or {}
    posting_parsed = posting.get("parsed_data") or {}

    resume_skills = resume_parsed.get("skills", [])
    job_skills = posting_parsed.get("required_skills", [])
    matched_skills, missing_skills = compare_skills(resume_skills, job_skills)
    resume_exp = resume_parsed.get("experience", [])
    job_min_years = posting_parsed.get("min_experience", 0)
    experience_alignment = check_experience_fit(resume_exp, job_min_years)
    recommendations = generate_recommendations(missing_skills)

    skill_score = len(matched_skills) / len(job_skills) if job_skills else 1.0
    exp_weight = {"Exceeds": 1.0, "Matches": 1.0, "Partial": 0.5, "Below": 0.0}.get(
        experience_alignment, 0.0
    )
    overall_score = int(round((skill_score * 0.7 + exp_weight * 0.3) * 100))
    if overall_score >= 80:
        signal = "green"
    elif overall_score >= 40:
        signal = "yellow"
    else:
        signal = "red"

    insert_data = {
        "resume_id": str(payload.resume_id),
        "posting_id": str(payload.posting_id),
        "overall_score": overall_score,
        "fit_items": matched_skills,
        "gap_items": missing_skills,
        "explanation": "Auto-generated analysis",
        "confidence": "Medium",
    }
    res = supabase.table("analyses").insert(insert_data).execute()
    analysis_id = res.data[0]["id"] if res.data else None

    return success_response(
        {
            "analysis_id": analysis_id,
            "overall_score": overall_score,
            "signal": signal,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "recommendations": recommendations,
            "experience_alignment": experience_alignment,
        },
        status_code=201,
    )

@app.get("/analyses/{analysis_id}")
def get_analysis(
    analysis_id: UUID, token_data: Dict[str, Any] = Depends(require_access_token)
):
    supabase = get_supabase_client()
    analysis = (
        supabase.table("analyses")
        .select("*")
        .eq("id", str(analysis_id))
        .single()
        .execute()
    ).data
    if not analysis:
        raise FitGapException("NOT_FOUND", "Analysis not found", 404)

    overall_score = analysis.get("overall_score") or 0
    if overall_score >= 80:
        signal = "green"
    elif overall_score >= 40:
        signal = "yellow"
    else:
        signal = "red"

    return success_response(
        {
            "analysis_id": analysis.get("id"),
            "resume_id": analysis.get("resume_id"),
            "posting_id": analysis.get("posting_id"),
            "overall_score": overall_score,
            "signal": signal,
            "fit_items": analysis.get("fit_items") or [],
            "gap_items": analysis.get("gap_items") or [],
            "over_items": analysis.get("over_items") or [],
            "summary": analysis.get("explanation") or "",
            "confidence": analysis.get("confidence") or "Medium",
        }
    )

# --- Resume API ---

@app.post("/resumes")
@app.post("/api/v1/resumes")
async def upload_resume(
    file: UploadFile = File(...),
    store_original: bool = Form(False),
    token_data: Dict[str, Any] = Depends(require_access_token),
):
    user_id = token_data.get("sub")
    if not user_id:
        raise FitGapException("UNAUTHORIZED", "Missing user id", 401)
    if not file.filename.lower().endswith(".pdf"):
        raise FitGapException("UNSUPPORTED_FILE_TYPE", "Only PDF files are supported", 400)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name
        
    try:
        raw_text = extract_text_from_pdf(tmp_path)
        parsed_data = await parse_resume_with_llm(raw_text)
        
        supabase = get_supabase_client()
        existing = (
            supabase.table("resumes")
            .select("id")
            .eq("user_id", user_id)
            .execute()
        ).data
        if existing:
            raise FitGapException("LIMIT_EXCEEDED", "Only one resume is allowed per account", 400)
        db_data = {
            "user_id": user_id,
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

@app.get("/resumes/{resume_id}")
@app.get("/api/v1/resumes/{resume_id}")
def get_resume(resume_id: UUID, token_data: Dict[str, Any] = Depends(require_access_token)):
    user_id = token_data.get("sub")
    supabase = get_supabase_client()
    res = (
        supabase.table("resumes")
        .select("*")
        .eq("id", str(resume_id))
        .eq("user_id", user_id)
        .single()
        .execute()
    )
    
    if not res.data:
        raise FitGapException("NOT_FOUND", "Resume not found", 404)
        
    return success_response({
        "resume_id": res.data["id"],
        "parsed_data": res.data["parsed_data"],
        "created_at": res.data.get("created_at")
    })

@app.patch("/resumes/{resume_id}")
@app.patch("/api/v1/resumes/{resume_id}")
def update_resume(resume_id: UUID, update: ResumeUpdate, token_data: Dict[str, Any] = Depends(require_access_token)):
    user_id = token_data.get("sub")
    supabase = get_supabase_client()
    current = (
        supabase.table("resumes")
        .select("parsed_data")
        .eq("id", str(resume_id))
        .eq("user_id", user_id)
        .single()
        .execute()
    )
    if not current.data:
        raise FitGapException("NOT_FOUND", "Resume not found", 404)
        
    new_parsed_data = current.data["parsed_data"].copy()
    new_parsed_data.update(update.parsed_data)
    res = supabase.table("resumes").update({"parsed_data": new_parsed_data}).eq("id", str(resume_id)).execute()
    
    if not res.data:
        raise FitGapException("INTERNAL_ERROR", "Failed to update resume", 500)
        
    return success_response({
        "resume_id": res.data[0]["id"],
        "parsed_data": res.data[0]["parsed_data"],
        "updated_at": res.data[0].get("updated_at")
    })

@app.delete("/resumes/{resume_id}")
@app.delete("/api/v1/resumes/{resume_id}")
def delete_resume(resume_id: UUID, token_data: Dict[str, Any] = Depends(require_access_token)):
    user_id = token_data.get("sub")
    supabase = get_supabase_client()
    res = supabase.table("resumes").delete().eq("id", str(resume_id)).eq("user_id", user_id).execute()
    if not res.data:
        raise FitGapException("NOT_FOUND", "Resume not found or already deleted", 404)
    return success_response({"message": "서류가 삭제되었습니다."})

# --- Job Posting API ---

@app.post("/postings", status_code=201)
@app.post("/api/v1/postings", status_code=201)
async def create_posting(posting: PostingCreate, token_data: Dict[str, Any] = Depends(require_access_token)):
    user_id = token_data.get("sub")
    role = token_data.get("role")
    if role != "COMPANY":
        raise FitGapException("FORBIDDEN", "Only company accounts can create postings", 403)
    if len(posting.raw_text) < 100:
        raise FitGapException("TEXT_TOO_SHORT", "Job posting text must be at least 100 characters", 400)
        
    try:
        parsed_data = await parse_posting_with_llm(posting.raw_text)
        supabase = get_supabase_client()
        existing = (
            supabase.table("job_postings")
            .select("id")
            .eq("created_by", user_id)
            .execute()
        ).data or []
        if len(existing) >= 3:
            raise FitGapException("LIMIT_EXCEEDED", "Only 3 postings are allowed per account", 400)
        db_data = {
            "company_name": posting.company_name,
            "raw_text": posting.raw_text,
            "parsed_data": parsed_data.dict(),
            "created_by": user_id,
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

@app.get("/postings/{posting_id}")
@app.get("/api/v1/postings/{posting_id}")
def get_posting(posting_id: UUID, token_data: Dict[str, Any] = Depends(require_access_token)):
    user_id = token_data.get("sub")
    supabase = get_supabase_client()
    res = (
        supabase.table("job_postings")
        .select("*")
        .eq("id", str(posting_id))
        .eq("created_by", user_id)
        .single()
        .execute()
    )
    
    if not res.data:
        raise FitGapException("NOT_FOUND", "Job posting not found", 404)
        
    return success_response({
        "posting_id": res.data["id"],
        "company_name": res.data.get("company_name"),
        "parsed_data": res.data["parsed_data"],
        "created_at": res.data.get("created_at")
    })

@app.patch("/postings/{posting_id}")
@app.patch("/api/v1/postings/{posting_id}")
async def update_posting(posting_id: UUID, update: PostingUpdate, token_data: Dict[str, Any] = Depends(require_access_token)):
    user_id = token_data.get("sub")
    supabase = get_supabase_client()
    
    # 1. Fetch current
    current = (
        supabase.table("job_postings")
        .select("*")
        .eq("id", str(posting_id))
        .eq("created_by", user_id)
        .single()
        .execute()
    )
    if not current.data:
        raise FitGapException("NOT_FOUND", "Job posting not found", 404)
        
    update_data = {}
    if update.company_name:
        update_data["company_name"] = update.company_name
        
    if update.raw_text:
        if len(update.raw_text) < 100:
            raise FitGapException("TEXT_TOO_SHORT", "Job posting text must be at least 100 characters", 400)
        update_data["raw_text"] = update.raw_text
        # Re-parse
        parsed_data = await parse_posting_with_llm(update.raw_text)
        update_data["parsed_data"] = parsed_data.dict()
        
    if not update_data:
        raise FitGapException("INVALID_REQUEST", "No update fields provided", 400)
        
    # 2. Update
    res = supabase.table("job_postings").update(update_data).eq("id", str(posting_id)).execute()
    
    if not res.data:
        raise FitGapException("INTERNAL_ERROR", "Failed to update posting", 500)
        
    return success_response({
        "posting_id": res.data[0]["id"],
        "company_name": res.data[0].get("company_name"),
        "parsed_data": res.data[0]["parsed_data"],
        "updated_at": res.data[0].get("updated_at")
    })

@app.delete("/postings/{posting_id}")
@app.delete("/api/v1/postings/{posting_id}")
def delete_posting(posting_id: UUID, token_data: Dict[str, Any] = Depends(require_access_token)):
    user_id = token_data.get("sub")
    supabase = get_supabase_client()
    res = supabase.table("job_postings").delete().eq("id", str(posting_id)).eq("created_by", user_id).execute()
    if not res.data:
        raise FitGapException("NOT_FOUND", "Job posting not found or already deleted", 404)
    return success_response({"message": "공고가 삭제되었습니다."})
