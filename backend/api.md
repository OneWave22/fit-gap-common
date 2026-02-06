# API 명세서: 핏갭 (Fit-Gap)

버전: 1.0
작성일: 2026-02-06
Base URL: `https://api.fitgap.kr/v1`

---

## 1. 공통 사항

### 1.1 인증

MVP에서는 간소화된 API Key 인증을 사용한다. 정식 출시 시 OAuth 2.0으로 전환.

```
Authorization: Bearer {api_key}
```

### 1.2 공통 응답 형식

**성공 응답**

```json
{
  "success": true,
  "data": { ... }
}
```

**에러 응답**

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "사람이 읽을 수 있는 에러 메시지"
  }
}
```

### 1.3 공통 에러 코드

| HTTP 상태 | 에러 코드                   | 설명 |
|-----------|-------------------------|------|
| 400 | `INVALID_REQUEST`       | 요청 파라미터 누락 또는 형식 오류 |
| 400 | `FILE_TOO_LARGE`        | 파일 크기 초과 (최대 10MB) |
| 400 | `UNSUPPORTED_FILE_TYPE` | 지원하지 않는 파일 형식 |
| 400 | `TEXT_TOO_SHORT`        | 입력 텍스트가 최소 길이 미만 |
| 401 | `UNAUTHORIZED`          | 인증 실패 |
| 403 | `FORBIDDEN`             | 접근 제한 |
| 404 | `NOT_FOUND`             | 리소스를 찾을 수 없음 |
| 429 | `RATE_LIMIT_EXCEEDED`   | 요청 횟수 초과 |
| 500 | `INTERNAL_ERROR`        | 서버 내부 오류 |
| 502 | `LLM_API_ERROR`         | LLM API 호출 실패 |
| 504 | `ANALYSIS_TIMEOUT`      | 분석 처리 시간 초과 |

---

## 2. 서류(Resume) API

### 2.1 서류 업로드 및 파싱

자소서 PDF를 업로드하면 텍스트를 추출하고 구조화된 데이터로 변환한다.

```
POST /resumes
Content-Type: multipart/form-data
```

**요청**

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `file` | File | O | PDF 파일 (최대 10MB, 텍스트 기반 PDF) |
| `store_original` | boolean | X | 원문 보관 여부 (기본값: false) |

**응답 (201 Created)**

```json
{
  "success": true,
  "data": {
    "resume_id": "550e8400-e29b-41d4-a716-446655440000",
    "parsed_data": {
      "skills": [
        { "name": "Spring Boot", "level": "실무", "source": "2년간 REST API 개발에 활용" },
        { "name": "AWS", "level": "실무", "source": "EC2, S3, RDS를 이용한 서비스 배포 경험" },
        { "name": "Java", "level": "숙련", "source": "주력 언어로 3개 프로젝트 수행" }
      ],
      "experiences": [
        {
          "title": "커머스 플랫폼 백엔드 개발",
          "duration": "2025.03 - 2025.08",
          "description": "Spring Boot 기반 주문/결제 API 개발, 일 5만 건 처리",
          "achievements": ["응답 시간 40% 개선", "테스트 커버리지 85% 달성"]
        }
      ],
      "metrics": [
        { "value": "응답 시간 40% 개선", "context": "캐싱 도입으로 평균 응답 200ms → 120ms" }
      ],
      "soft_skills": ["팀 협업", "문제 해결"],
      "keywords": ["REST API", "MSA", "CI/CD", "코드 리뷰"]
    },
    "created_at": "2026-02-06T17:30:00Z"
  }
}
```

**에러**

| 상황 | 에러 코드 |
|------|-----------|
| 10MB 초과 | `FILE_TOO_LARGE` |
| PDF가 아닌 파일 | `UNSUPPORTED_FILE_TYPE` |
| 이미지 기반 PDF (텍스트 추출 불가) | `INVALID_REQUEST` (message: "텍스트 기반 PDF만 지원됩니다") |

---

### 2.2 서류 조회

```
GET /resumes/{resume_id}
```

**응답 (200 OK)**

```json
{
  "success": true,
  "data": {
    "resume_id": "550e8400-e29b-41d4-a716-446655440000",
    "parsed_data": { "..." },
    "created_at": "2026-02-06T17:30:00Z"
  }
}
```

---

### 2.3 서류 파싱 결과 수정

사용자가 자동 파싱 결과를 수정할 때 사용한다.

```
PATCH /resumes/{resume_id}
Content-Type: application/json
```

**요청**

```json
{
  "parsed_data": {
    "skills": [
      { "name": "Spring Boot", "level": "실무", "source": "2년간 REST API 개발에 활용" },
      { "name": "Redis", "level": "학습", "source": "사이드 프로젝트에서 캐싱 용도로 사용" }
    ]
  }
}
```

> `parsed_data` 내의 최상위 필드 단위로 병합(merge)된다. 제공된 필드만 업데이트되고, 제공되지 않은 필드는 기존 값을 유지한다.

**응답 (200 OK)**

```json
{
  "success": true,
  "data": {
    "resume_id": "550e8400-e29b-41d4-a716-446655440000",
    "parsed_data": { "... (병합된 결과)" },
    "updated_at": "2026-02-06T17:35:00Z"
  }
}
```

---

### 2.4 서류 삭제

```
DELETE /resumes/{resume_id}
```

**응답 (200 OK)**

```json
{
  "success": true,
  "data": {
    "message": "서류가 삭제되었습니다."
  }
}
```

---

## 3. 공고(Job Posting) API

### 3.1 공고 등록 및 파싱

```
POST /postings
Content-Type: application/json
```

**요청**

```json
{
  "company_name": "테크스타트업 A사",
  "raw_text": "모집부문: 백엔드 개발자\n\n[필수 요건]\n- Spring Boot 기반 API 개발 경험 2년 이상\n- RDBMS(MySQL/PostgreSQL) 활용 경험\n- Redis를 이용한 캐싱 구현 경험\n\n[우대 사항]\n- AWS 인프라 운영 경험\n- MSA 환경 개발 경험\n- 코드 리뷰 문화에 익숙한 분\n\n[주요 업무]\n- 커머스 플랫폼 백엔드 개발\n- 결제/정산 시스템 설계 및 구현\n- 서비스 성능 모니터링 및 최적화\n\n[이런 분을 원합니다]\n- 팀원과의 소통을 중시하는 분\n- 문제 발생 시 주도적으로 해결하는 분"
}
```

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `company_name` | string | X | 회사명 |
| `raw_text` | string | O | 공고 전체 텍스트 (최소 100자) |

**응답 (201 Created)**

```json
{
  "success": true,
  "data": {
    "posting_id": "660e8400-e29b-41d4-a716-446655440001",
    "company_name": "테크스타트업 A사",
    "parsed_data": {
      "required_skills": [
        { "name": "Spring Boot", "detail": "API 개발 경험 2년 이상", "source": "필수 요건 1번" },
        { "name": "RDBMS", "detail": "MySQL/PostgreSQL 활용 경험", "source": "필수 요건 2번" },
        { "name": "Redis", "detail": "캐싱 구현 경험", "source": "필수 요건 3번" }
      ],
      "preferred_skills": [
        { "name": "AWS", "detail": "인프라 운영 경험", "source": "우대 사항 1번" },
        { "name": "MSA", "detail": "환경 개발 경험", "source": "우대 사항 2번" }
      ],
      "responsibilities": [
        "커머스 플랫폼 백엔드 개발",
        "결제/정산 시스템 설계 및 구현",
        "서비스 성능 모니터링 및 최적화"
      ],
      "required_experience": [],
      "culture_keywords": ["소통", "주도적 문제 해결", "코드 리뷰"]
    },
    "created_at": "2026-02-06T17:30:00Z"
  }
}
```

---

### 3.2 공고 조회

```
GET /postings/{posting_id}
```

**응답 (200 OK)**: 3.1 응답 `data`와 동일 구조

---

### 3.3 공고 수정

```
PATCH /postings/{posting_id}
Content-Type: application/json
```

**요청**

```json
{
  "raw_text": "(수정된 공고 텍스트)",
  "company_name": "테크스타트업 A사"
}
```

> `raw_text`가 제공되면 재파싱을 수행하여 `parsed_data`를 갱신한다.

**응답 (200 OK)**: 갱신된 공고 데이터

---

### 3.4 공고 삭제

```
DELETE /postings/{posting_id}
```

**응답 (200 OK)**

```json
{
  "success": true,
  "data": {
    "message": "공고가 삭제되었습니다."
  }
}
```

---

## 4. 분석(Analysis) API

### 4.1 Fit-Gap 분석 실행

서류와 공고를 교차 분석하여 Fit/Gap/Over를 분류하고 적합도 점수를 산출한다.

```
POST /analyses
Content-Type: application/json
```

**요청**

```json
{
  "resume_id": "550e8400-e29b-41d4-a716-446655440000",
  "posting_id": "660e8400-e29b-41d4-a716-446655440001"
}
```

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `resume_id` | string (UUID) | O | 분석할 서류 ID |
| `posting_id` | string (UUID) | O | 분석할 공고 ID |

**응답 (201 Created)**

```json
{
  "success": true,
  "data": {
    "analysis_id": "770e8400-e29b-41d4-a716-446655440002",
    "resume_id": "550e8400-e29b-41d4-a716-446655440000",
    "posting_id": "660e8400-e29b-41d4-a716-446655440001",
    "overall_score": 72,
    "signal": "yellow",
    "confidence": "Medium",
    "category_scores": {
      "required_skills": { "score": 78, "weight": 35, "confidence": "High" },
      "preferred_skills": { "score": 60, "weight": 15, "confidence": "High" },
      "experience_relevance": { "score": 75, "weight": 25, "confidence": "Medium" },
      "soft_skills": { "score": 55, "weight": 15, "confidence": "Low" },
      "achievement_evidence": { "score": 70, "weight": 10, "confidence": "Medium" }
    },
    "fit_items": [
      {
        "category": "required_skills",
        "item": "Spring Boot",
        "posting_source": "Spring Boot 기반 API 개발 경험 2년 이상 (필수 요건 1번)",
        "resume_source": "2년간 Spring Boot로 REST API 개발에 활용",
        "match_score": 0.92,
        "confidence": "High",
        "explanation": "공고가 요구하는 Spring Boot API 개발 경험과 서류의 2년 실무 경험이 높은 수준으로 일치합니다."
      },
      {
        "category": "required_skills",
        "item": "RDBMS",
        "posting_source": "MySQL/PostgreSQL 활용 경험 (필수 요건 2번)",
        "resume_source": "RDS(PostgreSQL)를 이용한 서비스 배포",
        "match_score": 0.81,
        "confidence": "High",
        "explanation": "AWS RDS PostgreSQL 사용 경험이 공고의 RDBMS 활용 요건을 충족합니다."
      }
    ],
    "gap_items": [
      {
        "category": "required_skills",
        "item": "Redis",
        "posting_source": "Redis를 이용한 캐싱 구현 경험 (필수 요건 3번)",
        "resume_source": null,
        "match_score": 0,
        "confidence": "High",
        "explanation": "공고에서 Redis 캐싱 경험을 필수로 요구하고 있으나, 서류에서 Redis 관련 경험이 확인되지 않습니다.",
        "suggestion": "Redis를 활용한 캐싱 경험을 추가하세요. 사이드 프로젝트에서라도 Redis를 사용한 사례가 있다면 서술하는 것이 좋습니다."
      },
      {
        "category": "soft_skills",
        "item": "팀 협업 구체성",
        "posting_source": "팀원과의 소통을 중시하는 분",
        "resume_source": "팀 협업 (소프트스킬 항목에서 언급)",
        "match_score": 0.38,
        "confidence": "Low",
        "explanation": "서류에서 '팀 협업'을 소프트스킬로 언급하고 있으나, 구체적인 협업 방식(코드 리뷰, 스프린트 등)에 대한 서술이 부족합니다.",
        "suggestion": "프로젝트 경험에서 코드 리뷰, 스프린트 회의, 타 직군과의 협업 등 구체적인 사례를 추가하세요."
      }
    ],
    "over_items": [
      {
        "category": "keywords",
        "item": "CI/CD",
        "resume_source": "CI/CD 파이프라인 구축 경험",
        "posting_source": null,
        "confidence": "Medium",
        "explanation": "서류에서 CI/CD 경험을 서술하고 있으나, 해당 공고에서는 CI/CD를 요구하거나 우대하지 않습니다. 부정적 요소는 아니나, 이 공고에서는 강점으로 인식되지 않을 수 있습니다."
      }
    ],
    "summary": "Spring Boot, RDBMS 등 핵심 기술 요건은 충족하나, Redis 캐싱 경험 부재와 협업 경험의 구체성 부족이 주요 Gap입니다. 필수 기술 3개 중 2개를 높은 수준으로 충족하고 있어, Redis 경험을 보완하면 적합도가 크게 향상될 수 있습니다.",
    "disclaimer": "본 분석은 참고용이며, 최종 채용/지원 결정은 사용자의 판단에 따릅니다.",
    "created_at": "2026-02-06T17:35:00Z"
  }
}
```

**signal 값**

| 값 | 조건 | 표시 |
|----|------|------|
| `green` | 80~100점 | 🟢 적합/추천 |
| `yellow` | 40~79점 | 🟡 보류 |
| `red` | 0~39점 | 🔴 부적합/비추천 |

---

### 4.2 분석 결과 조회

```
GET /analyses/{analysis_id}
```

**응답 (200 OK)**: 4.1 응답 `data`와 동일 구조

---

### 4.3 분석 결과 목록 조회

특정 공고에 대한 전체 지원자 분석 결과를 신호등 기준으로 정렬하여 반환한다.

```
GET /analyses?posting_id={posting_id}
```

**쿼리 파라미터**

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `posting_id` | string (UUID) | O | 공고 ID |
| `signal` | string | X | 필터: `green`, `yellow`, `red` |
| `sort_by` | string | X | 정렬 기준: `score_desc` (기본값), `score_asc` |
| `page` | integer | X | 페이지 번호 (기본값: 1) |
| `page_size` | integer | X | 페이지 크기 (기본값: 20, 최대: 100) |

**응답 (200 OK)**

```json
{
  "success": true,
  "data": {
    "posting_id": "660e8400-e29b-41d4-a716-446655440001",
    "summary": {
      "total": 50,
      "green": 3,
      "yellow": 12,
      "red": 35
    },
    "analyses": [
      {
        "analysis_id": "770e8400-e29b-41d4-a716-446655440002",
        "resume_id": "550e8400-e29b-41d4-a716-446655440000",
        "overall_score": 92,
        "signal": "green",
        "confidence": "High",
        "top_gap": "MSA 경험 부재",
        "top_strength": "Spring Boot + AWS 실무 2년"
      },
      {
        "analysis_id": "...",
        "resume_id": "...",
        "overall_score": 68,
        "signal": "yellow",
        "confidence": "Medium",
        "top_gap": "Redis 경험 부재",
        "top_strength": "커머스 도메인 경험"
      }
    ],
    "pagination": {
      "page": 1,
      "page_size": 20,
      "total_pages": 3
    }
  }
}
```

---

### 4.4 일괄 분석 실행

기업이 하나의 공고에 대해 여러 서류를 한 번에 분석한다.

```
POST /analyses/batch
Content-Type: application/json
```

**요청**

```json
{
  "resume_ids": [
    "550e8400-e29b-41d4-a716-446655440000",
    "550e8400-e29b-41d4-a716-446655440010",
    "550e8400-e29b-41d4-a716-446655440020"
  ],
  "posting_id": "660e8400-e29b-41d4-a716-446655440001"
}
```

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `resume_ids` | string[] | O | 서류 ID 배열 (최대 50개) |
| `posting_id` | string (UUID) | O | 공고 ID |

**응답 (202 Accepted)**

일괄 분석은 비동기로 처리된다.

```json
{
  "success": true,
  "data": {
    "batch_id": "880e8400-e29b-41d4-a716-446655440003",
    "status": "processing",
    "total": 3,
    "completed": 0,
    "posting_id": "660e8400-e29b-41d4-a716-446655440001"
  }
}
```

---

### 4.5 일괄 분석 상태 조회

```
GET /analyses/batch/{batch_id}
```

**응답 (200 OK)**

```json
{
  "success": true,
  "data": {
    "batch_id": "880e8400-e29b-41d4-a716-446655440003",
    "status": "completed",
    "total": 3,
    "completed": 3,
    "analysis_ids": [
      "770e8400-e29b-41d4-a716-446655440002",
      "770e8400-e29b-41d4-a716-446655440012",
      "770e8400-e29b-41d4-a716-446655440022"
    ]
  }
}
```

| status | 설명 |
|--------|------|
| `processing` | 분석 진행 중 |
| `completed` | 전체 완료 |
| `partial_failure` | 일부 실패 (실패 건은 `failed_resume_ids`에 포함) |

---

## 5. 공고 인사이트(Posting Insights) API

### 5.1 공고 인사이트 생성

```
POST /postings/{posting_id}/insights
```

**요청**: 바디 없음 (posting_id의 parsed_data를 기반으로 분석)

**응답 (201 Created)**

```json
{
  "success": true,
  "data": {
    "insight_id": "990e8400-e29b-41d4-a716-446655440004",
    "posting_id": "660e8400-e29b-41d4-a716-446655440001",
    "insights": [
      {
        "type": "excessive_requirements",
        "severity": "warning",
        "title": "필수 요건 과다",
        "description": "필수 요건 3개(Spring Boot, RDBMS, Redis)는 경력 2~3년차 수준입니다. 신입 대상이라면 1~2개로 축소하고 나머지를 우대 사항으로 이동하는 것을 권장합니다.",
        "source": "필수 요건 항목 분석",
        "action": "Redis를 우대 사항으로 이동 검토"
      },
      {
        "type": "culture_description_weak",
        "severity": "info",
        "title": "조직 문화 서술 부족",
        "description": "팀 문화/근무 환경에 대한 서술이 2문장입니다. 구체적인 팀 문화(코드 리뷰 주기, 스프린트 방식 등)를 추가하면 지원자의 관심을 높일 수 있습니다.",
        "source": "조직문화 키워드 분석",
        "action": "팀 문화 및 근무 환경 상세 서술 추가"
      }
    ],
    "created_at": "2026-02-06T17:40:00Z"
  }
}
```

**인사이트 type**

| type | 설명 |
|------|------|
| `excessive_requirements` | 필수/우대 요건이 직급 대비 과다 |
| `level_mismatch` | 신입/경력 표기와 실제 요구 수준 불일치 |
| `culture_description_weak` | 조직 문화 서술 부족 |
| `benefit_missing` | 복지/처우 정보 부족 |
| `ambiguous_responsibility` | 업무 범위가 모호함 |

**severity**

| severity | 설명 |
|----------|------|
| `critical` | 지원자 유입에 심각한 영향 |
| `warning` | 개선 시 효과가 큼 |
| `info` | 참고 사항 |

---

### 5.2 공고 인사이트 조회

```
GET /postings/{posting_id}/insights
```

**응답 (200 OK)**: 5.1 응답 `data`와 동일 구조

---

## 6. 피드백(Feedback) API

### 6.1 분석 결과 피드백 제출

```
POST /analyses/{analysis_id}/feedback
Content-Type: application/json
```

**요청**

```json
{
  "rating": "thumbs_down",
  "reasons": ["skill_misidentified", "experience_misinterpreted"],
  "comment": "Redis를 사이드 프로젝트에서 사용한 경험이 있는데 인식하지 못했습니다."
}
```

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `rating` | string | O | `thumbs_up` 또는 `thumbs_down` |
| `reasons` | string[] | X | 부정확 사유 코드 배열 (thumbs_down일 때만) |
| `comment` | string | X | 자유 입력 코멘트 (최대 500자) |

**reason 코드**

| 코드 | 설명 |
|------|------|
| `skill_misidentified` | 해당 기술을 보유하고 있음 |
| `experience_misinterpreted` | 경험을 다르게 해석함 |
| `posting_misunderstood` | 공고 요구사항을 잘못 파악함 |
| `score_inaccurate` | 점수가 실제와 맞지 않음 |
| `other` | 기타 |

**응답 (201 Created)**

```json
{
  "success": true,
  "data": {
    "message": "피드백이 등록되었습니다. 감사합니다."
  }
}
```

---

## 7. 시뮬레이션(Simulation) API (확장)

### 7.1 점수 변화 시뮬레이션

Gap 항목을 보완했을 때 적합도 점수가 어떻게 변하는지 미리 계산한다.

```
POST /analyses/{analysis_id}/simulate
Content-Type: application/json
```

**요청**

```json
{
  "resolve_gaps": ["Redis", "팀 협업 구체성"]
}
```

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `resolve_gaps` | string[] | O | Fit으로 전환할 Gap 항목명 배열 |

**응답 (200 OK)**

```json
{
  "success": true,
  "data": {
    "original_score": 72,
    "simulated_score": 88,
    "score_change": 16,
    "original_signal": "yellow",
    "simulated_signal": "green",
    "resolved_items": [
      {
        "item": "Redis",
        "category": "required_skills",
        "score_impact": 12,
        "explanation": "필수 기술 3개 중 3개 충족으로 변경. 필수 기술 점수 78 → 100."
      },
      {
        "item": "팀 협업 구체성",
        "category": "soft_skills",
        "score_impact": 4,
        "explanation": "소프트스킬 항목에서 협업 구체성 보완. 소프트스킬 점수 55 → 80."
      }
    ]
  }
}
```

---

## 8. 피드백 레터(Feedback Letter) API (확장)

### 8.1 피드백 레터 생성

```
POST /analyses/{analysis_id}/feedback-letter
Content-Type: application/json
```

**요청**

```json
{
  "tone": "warm",
  "include_feedback": true
}
```

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `tone` | string | X | `formal` (기본값) 또는 `warm` |
| `include_feedback` | boolean | X | Fit-Gap 기반 구체적 피드백 포함 여부 (기본값: true) |

**응답 (201 Created)**

```json
{
  "success": true,
  "data": {
    "letter_id": "aa0e8400-e29b-41d4-a716-446655440005",
    "analysis_id": "770e8400-e29b-41d4-a716-446655440002",
    "subject": "[테크스타트업 A사] 백엔드 개발자 지원 결과 안내",
    "body": "안녕하세요, 지원자님.\n\n먼저 테크스타트업 A사 백엔드 개발자 포지션에 관심을 가져주셔서 진심으로 감사드립니다.\n\n신중한 검토 끝에, 이번에는 함께하기 어렵다는 결론을 내리게 되었습니다.\n\n지원자님의 Spring Boot와 RDBMS 활용 경험은 인상적이었습니다. 다만, 저희 포지션에서 중요하게 보는 캐싱 시스템(Redis) 실무 경험이 확인되지 않았고, 팀 협업 관련 구체적인 사례가 부족했습니다.\n\nRedis 관련 경험을 쌓으시고, 프로젝트에서의 협업 사례를 구체적으로 정리하신다면 다음 기회에 좋은 결과가 있을 것으로 생각합니다.\n\n지원자님의 앞날을 응원합니다.\n\n테크스타트업 A사 채용팀 드림",
    "created_at": "2026-02-06T18:00:00Z"
  }
}
```

---

## 9. Rate Limit

| 티어 | 제한 |
|------|------|
| Free (B2C) | 분석 3회/월, API 60회/시간 |
| Pro (B2C) | 분석 무제한, API 300회/시간 |
| Starter (B2B) | 스크리닝 100명/월, API 600회/시간 |
| Growth (B2B) | 스크리닝 무제한, API 1200회/시간 |

Rate Limit 초과 시 `429 RATE_LIMIT_EXCEEDED` 응답과 함께 `Retry-After` 헤더를 반환한다.

```
HTTP/1.1 429 Too Many Requests
Retry-After: 60
```
