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

-- 5. Users & Auth Tables
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255),
    nickname VARCHAR(80),
    role VARCHAR(30), -- JOBSEEKER / COMPANY
    status VARCHAR(30) DEFAULT 'PENDING_ONBOARDING', -- PENDING_ONBOARDING / ACTIVE
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now())
);

CREATE TABLE IF NOT EXISTS oauth_accounts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    provider VARCHAR(30) NOT NULL, -- GOOGLE
    provider_sub VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now())
);

CREATE UNIQUE INDEX IF NOT EXISTS oauth_provider_sub_uniq
    ON oauth_accounts (provider, provider_sub);

CREATE TABLE IF NOT EXISTS jobseeker_profiles (
    user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(30),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now())
);

CREATE TABLE IF NOT EXISTS company_profiles (
    user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    company_name VARCHAR(255),
    biz_reg_no VARCHAR(50),
    biz_verified BOOLEAN DEFAULT FALSE,
    biz_verified_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now())
);
