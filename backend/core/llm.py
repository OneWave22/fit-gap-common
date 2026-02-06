import json
import os
from typing import Dict, Any
from models.resume import ResumeParsedData
from models.posting import PostingParsedData
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# --- Resume Parsing ---

def generate_resume_prompt(raw_text: str) -> str:
    return f"""
    Extract structured data from the following resume text. 
    Return ONLY a valid JSON object matching the schema below.
    
    Schema:
    {{
        "skills": [{{ "name": "string", "level": "string", "source": "string" }}],
        "experiences": [{{ "title": "string", "duration": "string", "description": "string", "achievements": ["string"] }}],
        "metrics": [{{ "value": "string", "context": "string" }}],
        "soft_skills": ["string"],
        "keywords": ["string"]
    }}
    
    Resume Text:
    {raw_text}
    """

def parse_llm_resume_response(response_text: str) -> ResumeParsedData:
    clean_text = response_text.strip()
    if clean_text.startswith("```json"):
        clean_text = clean_text[7:]
    if clean_text.endswith("```"):
        clean_text = clean_text[:-3]
    
    data = json.loads(clean_text)
    return ResumeParsedData(**data)

async def parse_resume_with_llm(raw_text: str) -> ResumeParsedData:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = generate_resume_prompt(raw_text)
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    
    return parse_llm_resume_response(response.choices[0].message.content)

# --- Job Posting Parsing ---

def generate_posting_prompt(raw_text: str) -> str:
    return f"""
    Extract structured data from the following job posting text. 
    Return ONLY a valid JSON object matching the schema below.
    
    Schema:
    {{
        "required_skills": [{{ "name": "string", "detail": "string", "source": "string" }}],
        "preferred_skills": [{{ "name": "string", "detail": "string", "source": "string" }}],
        "responsibilities": ["string"],
        "required_experience": ["string"],
        "culture_keywords": ["string"]
    }}
    
    Job Posting Text:
    {raw_text}
    """

def parse_llm_posting_response(response_text: str) -> PostingParsedData:
    clean_text = response_text.strip()
    if clean_text.startswith("```json"):
        clean_text = clean_text[7:]
    if clean_text.endswith("```"):
        clean_text = clean_text[:-3]
    
    data = json.loads(clean_text)
    return PostingParsedData(**data)

async def parse_posting_with_llm(raw_text: str) -> PostingParsedData:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = generate_posting_prompt(raw_text)
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    
    return parse_llm_posting_response(response.choices[0].message.content)