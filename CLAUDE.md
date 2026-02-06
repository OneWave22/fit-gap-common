# Fit-Gap: AI Hiring Analysis Platform

## Project Summary
Fit-Gap cross-analyzes job postings (JD) vs resumes to classify each requirement as Fit/Gap/Over, producing a 0-100 score with citation-based explanations. Two-sided: job seekers get improvement advice, employers get applicant screening + posting insights.

## Repository Structure
- `frontend/` -- Next.js 16 + React 19 + Tailwind CSS 4 (deployed on Vercel)
- `backend/` -- FastAPI Python (deployed on Fly.io)
- Docs at root: `prd.md`, `api.md`, `use_cases.md`, `idea_revision.md`

## Tech Stack
| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 16, React 19, Tailwind CSS 4, TypeScript |
| Backend | FastAPI (Python 3.11+) |
| AI | OpenAI GPT-4o (structured extraction), text-embedding-3-small (semantic matching) |
| DB | Supabase (PostgreSQL) |
| PDF | pdfplumber |
| Deploy | Vercel (front) + Fly.io (back) |

## Key Reference Docs
- **PRD**: `prd.md` -- full product requirements, analysis pipeline, scoring weights
- **API spec**: `api.md` -- all endpoints with request/response examples
- **Use cases**: `use_cases.md` -- UC-01 through UC-10 detailed flows
- **DB schema**: `backend/schema.sql` -- resumes, job_postings, analyses, posting_insights

## Analysis Pipeline (4 steps)
1. Structured extraction via LLM (JSON Schema, temperature 0)
2. Embedding-based semantic matching (threshold: 0.75+ Fit, 0.5-0.75 partial, <0.5 Gap)
3. Rule-based Fit/Gap/Over classification
4. Weighted score (required_skills 35%, preferred 15%, experience 25%, soft_skills 15%, achievements 10%) + LLM explanation generation

## Conventions
- Language: Code and comments in English. UI text in Korean.
- Backend: follow FastAPI patterns with Pydantic models. Group by domain (routers/, services/, schemas/).
- Frontend: App Router. Components in `src/components/`, API calls in `src/lib/api.ts`. Server components by default, client components only when needed.
- API responses follow `{ success: bool, data: {...} }` or `{ success: bool, error: { code, message } }` pattern.
- All analysis results must include source citations from original text.
- Environment variables: never commit `.env`. See `backend/.env.example` for required keys.

## Development Plans
- `frontend/plan.md` -- phased frontend implementation
- `backend/plan.md` -- phased backend implementation
