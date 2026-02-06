# Specification: Gap Analysis Engine

## Overview
The Gap Analysis engine is the core intelligence of the Fit-Gap platform. It compares a candidate's resume (parsed data) against a job posting (parsed data) to determine alignment and identify missing skills or experiences.

## Core Requirements
- **Alignment Score:** Calculate a percentage (0-100%) based on skill matching, experience levels, and keyword relevance.
- **Gap Identification:** Explicitly list skills, certifications, or keywords present in the job description but missing from the resume.
- **Actionable Recommendations:** For each identified gap, generate a specific recommendation (e.g., "Consider gaining experience with Docker to match this requirement").

## Input Data (JSON)
- esume_data: Object containing extracted skills, experience (years/roles), and education.
- job_data: Object containing required skills, preferred skills, minimum experience, and key responsibilities.

## Output Data (JSON)
- overall_score: float
- matched_skills: list[string]
- missing_skills: list[string]
- ecommendations: list[string]
- experience_alignment: string (e.g., "Exceeds", "Matches", "Partial", "Below")

## Logic Phases
1. **Skill Matching:** Exact and fuzzy matching between resume skills and job requirements.
2. **Experience Validation:** Comparing years of experience and seniority levels.
3. **Recommendation Generation:** Mapping missing skills to predefined or LLM-generated advice.
