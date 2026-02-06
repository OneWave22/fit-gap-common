# Product Guidelines

## Voice and Tone
- **Professional & Objective:** All generated analysis and recommendations must be presented in a neutral, data-driven, and direct manner. Avoid flowery language or subjective adjectives.

## API Design Principles
- **Predictability & Consistency:** The API must strictly adhere to RESTful conventions, using standard HTTP methods and status codes consistently across all endpoints.
- **Developer Experience (DX):** Prioritize clarity and ease of use. Every error response must include a descriptive message and, where possible, a hint for resolution.

## Data Privacy & Security
- **Encrypted Storage:** All personally identifiable information (PII) extracted from resumes or provided by users must be encrypted at rest within the database to ensure user privacy.

## Error Handling
- **Standardized Responses:** All errors must return a consistent JSON payload structure, including a specific error code (e.g., invalid_resume_format) and a clear description to facilitate automated and manual debugging.
