# Implementation Plan: Core Resources API (Resumes & Postings)

## Phase 1: Authentication & Infrastructure
- [x] Task: Implement API Key Authentication Middleware cf8cf0c
    - [x] Write tests for unauthorized and authorized requests
    - [x] Implement ApiKeyHeader security in FastAPI
- [x] Task: Set up Supabase Client and Table Models ac4784e
    - [x] Write unit tests for database connection and basic query logic
    - [x] Implement Supabase client wrapper and database helper functions
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Authentication & Infrastructure' (Protocol in workflow.md)

## Phase 2: Resume API Implementation (POST)
- [ ] Task: Implement PDF Text Extraction
    - [ ] Write tests for PDF text extraction (valid and invalid PDFs)
    - [ ] Implement extraction logic using PyMuPDF or similar
- [ ] Task: Implement LLM Parsing for Resumes
    - [ ] Write tests for LLM prompt generation and response parsing
    - [ ] Integrate with OpenAI/Claude API to extract structured resume data
- [ ] Task: Implement POST /resumes Endpoint
    - [ ] Write integration tests for resume upload, parsing, and storage
    - [ ] Implement endpoint logic including Supabase Storage for store_original
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Resume API Implementation (POST)' (Protocol in workflow.md)

## Phase 3: Job Posting API Implementation (POST)
- [ ] Task: Implement LLM Parsing for Job Postings
    - [ ] Write tests for job posting parsing logic
    - [ ] Implement LLM integration for requirement extraction
- [ ] Task: Implement POST /postings Endpoint
    - [ ] Write integration tests for job posting creation and parsing
    - [ ] Implement endpoint and Supabase persistence
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Job Posting API Implementation (POST)' (Protocol in workflow.md)

## Phase 4: CRUD Operations & Finalization
- [ ] Task: Implement GET, PATCH, and DELETE for Resumes
    - [ ] Write tests for retrieval, merging updates, and deletion
    - [ ] Implement endpoints: GET /resumes/{id}, PATCH /resumes/{id}, DELETE /resumes/{id}
- [ ] Task: Implement GET, PATCH, and DELETE for Postings
    - [ ] Write tests for retrieval, re-parsing on update, and deletion
    - [ ] Implement endpoints: GET /postings/{id}, PATCH /postings/{id}, DELETE /postings/{id}
- [ ] Task: Conductor - User Manual Verification 'Phase 4: CRUD Operations & Finalization' (Protocol in workflow.md)
