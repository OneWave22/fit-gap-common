-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Resumes Table
CREATE TABLE IF NOT EXISTS resumes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID, -- Can be NULL for anonymous MVP usage
    raw_text TEXT,
    parsed_data JSONB,
    is_stored BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now())
);

-- 2. Job Postings Table
CREATE TABLE IF NOT EXISTS job_postings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_name VARCHAR(255),
    raw_text TEXT,
    parsed_data JSONB,
    created_by UUID, -- Can be NULL
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now())
);

-- 3. Analyses Table
CREATE TABLE IF NOT EXISTS analyses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    resume_id UUID REFERENCES resumes(id) ON DELETE CASCADE,
    posting_id UUID REFERENCES job_postings(id) ON DELETE CASCADE,
    overall_score INTEGER,
    category_scores JSONB,
    fit_items JSONB,
    gap_items JSONB,
    over_items JSONB,
    explanation TEXT,
    confidence VARCHAR(50), -- High, Medium, Low
    feedback VARCHAR(50), -- thumbs_up, thumbs_down
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now())
);

-- 4. Posting Insights Table
CREATE TABLE IF NOT EXISTS posting_insights (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    posting_id UUID REFERENCES job_postings(id) ON DELETE CASCADE,
    insights JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now())
);
