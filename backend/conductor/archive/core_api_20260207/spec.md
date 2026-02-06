# Specification: Core Resources API (Resumes & Postings)

## Overview
This track implements the core resource management APIs for the Fit-Gap platform. It covers the full lifecycle (Create, Read, Update, Delete) for **Resumes** and **Job Postings**, including real PDF text extraction, LLM-based parsing, and Supabase integration.

## Functional Requirements

### 1. Authentication
- **Mechanism:** Simplified API Key authentication (Authorization: Bearer {api_key}).
- **Validation:** Middleware to verify the key against a stored environment variable or secure config.
- **Scope:** All endpoints defined below must be protected.

### 2. Resume API (/resumes)
- **POST /resumes:**
  - **Input:** Multipart form data with ile (PDF, max 10MB) and optional store_original (bool).
  - **Processing:**
    1. Validate file size and type (PDF only).
    2. Extract raw text from PDF (using PyMuPDF or similar).
    3. **LLM Parsing:** Send raw text to an LLM (e.g., Gemini 3 Flash) to extract structured data (skills, experience, etc.) matching the schema in @api.md.
    4. **Storage:** Save parsed_data and metadata to Supabase esumes table.
    5. **File Storage:** If store_original is true, upload the PDF to Supabase Storage.
  - **Output:** 201 Created with esume_id and parsed_data.
- **GET /resumes/{resume_id}:** Retrieve resume details.
- **PATCH /resumes/{resume_id}:** Update parsed_data (merge logic).
- **DELETE /resumes/{resume_id}:** Delete resume record and associated file (if any).

### 3. Job Posting API (/postings)
- **POST /postings:**
  - **Input:** JSON with company_name and aw_text.
  - **Processing:**
    1. **LLM Parsing:** Send aw_text to LLM to extract requirements, preferred skills, etc.
    2. **Storage:** Save to Supabase job_postings table.
  - **Output:** 201 Created with posting_id and parsed_data.
- **GET /postings/{posting_id}:** Retrieve posting details.
- **PATCH /postings/{posting_id}:** Update text (triggering re-parsing) or metadata.
- **DELETE /postings/{posting_id}:** Delete posting record.

## Non-Functional Requirements
- **Error Handling:** Adhere to the standard error response format defined in @api.md.
- **Performance:** PDF parsing and LLM calls should be handled efficiently (consider async/await).
- **Security:** Ensure uploaded files are validated to prevent malicious content.

## Out of Scope
- /analyses endpoints (Fit-Gap analysis logic).
- Batch operations, insights, feedback, simulation, and feedback letter APIs.
- OAuth 2.0 implementation (MVP uses API Key).
