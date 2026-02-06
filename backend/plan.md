# Backend Implementation Plan

## Current State
- `main.py`: FastAPI app with single hello-world route
- `schema.sql`: 4 tables (resumes, job_postings, analyses, posting_insights)
- `requirements.txt`: fastapi, uvicorn, supabase, python-dotenv
- `.env.example`: SUPABASE_URL, SUPABASE_KEY, GEMINI_API_KEY

---

## Phase 0: Project Structure & DB Connection

### 0-1. Restructure project layout
```
backend/
  main.py                  # FastAPI app, CORS, router registration
  requirements.txt
  schema.sql
  .env.example
  app/
    __init__.py
    config.py              # Settings via pydantic-settings (env vars)
    database.py            # Supabase client singleton
    routers/
      __init__.py
      resumes.py           # /resumes endpoints
      postings.py          # /postings endpoints
      analyses.py          # /analyses endpoints
      insights.py          # /postings/{id}/insights endpoints
    schemas/
      __init__.py
      common.py            # SuccessResponse, ErrorResponse
      resume.py            # ResumeCreate, ResumeResponse, ParsedResumeData
      posting.py           # PostingCreate, PostingResponse, ParsedPostingData
      analysis.py          # AnalysisRequest, AnalysisResponse, FitItem, GapItem, OverItem
      insight.py           # InsightResponse, InsightCard
      feedback.py          # FeedbackRequest
    services/
      __init__.py
      pdf_parser.py        # pdfplumber text extraction
      llm_extractor.py     # Gemini 3 Flash structured extraction
      embedding.py         # Gemini text-embedding-004
      matching.py          # Semantic matching (cosine similarity)
      scorer.py            # Rule-based Fit/Gap/Over classification + weighted scoring
      explainer.py         # Gemini 3 Flash explanation generation with citations
      insight_generator.py # Posting insight analysis
```

### 0-2. Install additional dependencies
Add to requirements.txt:
- `pydantic-settings` (env config)
- `google-genai` (Gemini 3 Flash + embeddings)
- `pdfplumber` (PDF text extraction)
- `python-multipart` (file upload support)
- `numpy` (cosine similarity)

### 0-3. Supabase setup
- Run `schema.sql` in Supabase SQL Editor
- Create `app/database.py` with Supabase client init
- Create `app/config.py` with pydantic-settings reading .env

### 0-4. Update main.py
- CORS middleware (allow frontend origin)
- Register routers with `/v1` prefix
- Global exception handler (standard error format)

---

## Phase 1: Resume API (F-01)

### 1-1. PDF parsing service (`app/services/pdf_parser.py`)
- `extract_text_from_pdf(file: UploadFile) -> str`
- pdfplumber page-by-page extraction
- Validate: non-empty text (reject image-based PDF), file size <= 10MB

### 1-2. LLM structured extraction (`app/services/llm_extractor.py`)
- `extract_resume_structure(raw_text: str) -> ParsedResumeData`
- Gemini 3 Flash with JSON Schema response_format
- Schema: { skills[], experiences[], metrics[], soft_skills[], keywords[] }
- Temperature: 0

### 1-3. Resume router (`app/routers/resumes.py`)
- `POST /v1/resumes` -- upload PDF, parse, extract, store, return parsed_data
- `GET /v1/resumes/{resume_id}` -- fetch
- `PATCH /v1/resumes/{resume_id}` -- merge updated parsed_data
- `DELETE /v1/resumes/{resume_id}` -- delete

### 1-4. Pydantic schemas (`app/schemas/resume.py`)
- ParsedResumeData, ResumeResponse

---

## Phase 2: Job Posting API (F-02)

### 2-1. LLM structured extraction for postings
- `extract_posting_structure(raw_text: str) -> ParsedPostingData`
- Schema: { required_skills[], preferred_skills[], responsibilities[], required_experience[], culture_keywords[] }

### 2-2. Posting router (`app/routers/postings.py`)
- `POST /v1/postings` -- parse text, store, return parsed_data
- `GET /v1/postings/{posting_id}` -- fetch
- `PATCH /v1/postings/{posting_id}` -- re-parse if raw_text changed
- `DELETE /v1/postings/{posting_id}` -- delete

### 2-3. Pydantic schemas (`app/schemas/posting.py`)

---

## Phase 3: Analysis Engine (F-03, F-04)

### 3-1. Embedding service (`app/services/embedding.py`)
- `get_embeddings(texts: list[str]) -> list[list[float]]`
- Gemini text-embedding-004, batch embed

### 3-2. Matching service (`app/services/matching.py`)
- `compute_similarity_matrix(posting_embeddings, resume_embeddings) -> matrix`
- Cosine similarity, return best-match pairs with scores

### 3-3. Scoring service (`app/services/scorer.py`)
- `classify_and_score(posting_parsed, resume_parsed, similarity_matrix) -> AnalysisResult`
- Thresholds: >= 0.75 Fit, 0.5-0.75 partial, < 0.5 Gap
- Over: resume items with no posting match
- Weights: required_skills(35%), preferred(15%), experience(25%), soft_skills(15%), achievements(10%)
- Signal: 80-100 green, 40-79 yellow, 0-39 red

### 3-4. Explanation service (`app/services/explainer.py`)
- `generate_explanation(analysis_result, posting_text, resume_text) -> str`
- Single Gemini 3 Flash call: summary + per-item explanations with source citations + gap suggestions

### 3-5. Analysis router (`app/routers/analyses.py`)
- `POST /v1/analyses` -- full pipeline: fetch -> embed -> match -> score -> explain -> store
- `GET /v1/analyses/{analysis_id}` -- single result
- `GET /v1/analyses?posting_id=` -- list with pagination, filtering, sorting
- `POST /v1/analyses/batch` -- iterate resume_ids (sequential for MVP)
- `POST /v1/analyses/{analysis_id}/feedback` -- store rating + reasons

---

## Phase 4: Posting Insights (F-05)

### 4-1. Insight generator (`app/services/insight_generator.py`)
- `generate_insights(posting_parsed, raw_text) -> list[InsightCard]`
- LLM analysis: excessive_requirements, level_mismatch, culture_description_weak, benefit_missing, ambiguous_responsibility
- Return 2-3 cards with type, severity, title, description, source, action

### 4-2. Insights router (`app/routers/insights.py`)
- `POST /v1/postings/{posting_id}/insights` -- generate and store
- `GET /v1/postings/{posting_id}/insights` -- fetch

---

## Phase 5: Deployment & Testing

### 5-1. Dockerfile
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### 5-2. Fly.io config (`fly.toml`)
- Region: nrt (Korea proximity)
- Internal port 8080
- Secrets: `fly secrets set SUPABASE_URL=... SUPABASE_KEY=... GEMINI_API_KEY=...`

### 5-3. Testing
- Unit tests: each service in isolation (mock Gemini API)
- Integration tests: full pipeline with sample data
- Sample fixtures: `tests/fixtures/` with sample resume PDF + posting text
