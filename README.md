# 핏갭 (Fit-Gap)

> **합격과 불합격 사이, 그 간극을 설명하는 양방향 AI 채용 분석 플랫폼**

공고(JD)와 서류(자소서/포트폴리오) 사이의 Fit-Gap을 분석하여, 구직자에게는 **왜 떨어지는지 + 무엇을 고쳐야 하는지**, 기업에게는 **누굴 봐야 하는지 + 공고를 어떻게 고쳐야 하는지**를 근거 기반으로 제공합니다.

---

## 핵심 기능

### 구직자 (B2C)
- **Fit-Gap 분석 리포트** — 공고 대비 서류의 부족(Gap)/일치(Fit)/과잉(Over) 항목을 원문 인용과 함께 시각화
- **적합도 점수** — 0~100점 + 신호등 분류 (🟢 적합 / 🟡 보류 / 🔴 부적합)
- **서류 개선 제안** — Gap 항목별 구체적인 수정 방향 제시

### 기업 HR (B2B)
- **지원자 자동 스크리닝** — 신호등 분류로 상위 후보 즉시 확인
- **공고 개선 인사이트** — 필수 요건 과다, 신입/경력 불일치, 매력도 부족 등 개선 제안

---

## 기술 스택

| 레이어 | 기술 |
|--------|------|
| 프론트엔드 | Next.js 16, React 19, Tailwind CSS 4, TypeScript |
| 백엔드 | FastAPI (Python 3.11+) |
| AI/LLM | Gemini 3 Flash (구조화 추출, 설명 생성) |
| DB | Supabase (PostgreSQL) |
| PDF 파싱 | PyMuPDF |
| 배포 | Vercel (프론트엔드) + Fly.io (백엔드) |

---

## 분석 파이프라인

```
Step 1. 구조화 추출 (LLM Structured Output)
  공고 → {필수기술, 우대기술, 핵심업무, 요구경험, 조직문화키워드}
  서류 → {보유기술, 프로젝트경험, 성과지표, 소프트스킬, 키워드}
      ↓
Step 2. 의미 단위 매칭 (Embedding Similarity)
  유사도 0.75+ → Fit | 0.5~0.75 → 부분 매칭 | 0.5 미만 → Gap
      ↓
Step 3. Gap 분류 (규칙 기반)
  ✅ Fit: 공고 요구 ↔ 서류 근거 대응
  ⚠️ Gap: 공고 요구 있으나 서류에 근거 없음
  📌 Over: 서류에 있으나 공고와 무관
      ↓
Step 4. 점수 산출 (규칙 기반) + 설명 생성 (LLM)
  가중 합산 → 적합도 점수 (원문 인용 기반 설명 포함)
```

### 점수 산출 가중치

| 평가 항목 | 가중치 |
|-----------|--------|
| 필수 기술 스택 일치도 | 35% |
| 직무 경험 관련도 | 25% |
| 우대 사항 충족도 | 15% |
| 소프트스킬/문화 적합도 | 15% |
| 성과/수치 근거 충실도 | 10% |

---

## 프로젝트 구조

```
fit-gap-common/
├── frontend/                # Next.js 프론트엔드
│   └── src/
│       ├── app/             # App Router 페이지
│       │   ├── page.tsx              # 메인 페이지
│       │   ├── login/                # 로그인
│       │   ├── onboarding/           # 온보딩
│       │   ├── resumes/              # 서류 관리
│       │   ├── postings/             # 공고 관리/인사이트
│       │   ├── analysis/[id]/        # 분석 결과
│       │   ├── screening/            # 지원자 스크리닝
│       │   ├── mypage/               # 마이페이지
│       │   └── _components/          # 공통 컴포넌트
│       └── ...
├── backend/                 # FastAPI 백엔드
│   ├── main.py              # 앱 엔트리포인트
│   ├── core/                # 핵심 모듈
│   │   ├── database.py      # Supabase 연동
│   │   ├── llm.py           # LLM (Gemini) 연동
│   │   ├── pdf.py           # PDF 텍스트 추출
│   │   ├── auth.py          # 인증
│   │   ├── google_oauth.py  # Google OAuth
│   │   └── security.py      # 보안
│   ├── models/              # Pydantic 모델
│   │   ├── resume.py        # 서류 스키마
│   │   ├── posting.py       # 공고 스키마
│   │   └── analysis.py      # 분석 결과 스키마
│   ├── logic/               # 비즈니스 로직
│   │   ├── skills.py        # 기술 매칭 로직
│   │   ├── experience.py    # 경험 매칭 로직
│   │   └── recommendations.py  # 개선 제안 생성
│   ├── integrations/        # 외부 서비스 연동
│   ├── tests/               # 테스트
│   ├── schema.sql           # DB 스키마
│   ├── requirements.txt     # Python 의존성
│   ├── Dockerfile           # 컨테이너 설정
│   └── fly.toml             # Fly.io 배포 설정
├── design/                  # 디자인 문서
├── prd.md                   # 제품 요구사항 정의서
├── use_cases.md             # 유스케이스 상세
├── idea_revision.md         # 아이디어 정리
└── CLAUDE.md                # 개발 컨벤션
```

---

## 시작하기

### 사전 요구사항

- **Node.js** 18+
- **Python** 3.11+
- **Supabase** 프로젝트 (PostgreSQL)
- **Gemini API Key**

### 백엔드 실행

```bash
cd backend

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일에 아래 값을 설정:
#   SUPABASE_URL=<your-supabase-url>
#   SUPABASE_KEY=<your-supabase-anon-key>
#   GEMINI_API_KEY=<your-gemini-api-key>
#   GOOGLE_CLIENT_ID=<your-google-oauth-client-id>
#   GOOGLE_CLIENT_SECRET=<your-google-oauth-client-secret>

# DB 스키마 적용 (Supabase SQL Editor에서 실행)
# schema.sql 내용을 Supabase 대시보드에서 실행

# 서버 실행
uvicorn main:app --reload --port 8000
```

### 프론트엔드 실행

```bash
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

### 테스트 실행

```bash
cd backend
pytest
```

---

## API 개요

Base URL: `https://fit-gap-backend.fly.dev`

| 엔드포인트 | 메서드 | 설명 |
|------------|--------|------|
| `/resumes` | POST | 서류 업로드 및 파싱 (PDF) |
| `/resumes/{id}` | GET | 서류 조회 |
| `/resumes/{id}` | PATCH | 파싱 결과 수정 |
| `/resumes/{id}` | DELETE | 서류 삭제 |
| `/postings` | POST | 공고 등록 및 파싱 |
| `/postings/{id}` | GET | 공고 조회 |
| `/postings/{id}` | PATCH | 공고 수정 |
| `/postings/{id}` | DELETE | 공고 삭제 |
| `/analyses` | POST | Fit-Gap 분석 실행 |
| `/analyses/{id}` | GET | 분석 결과 조회 |
| `/analyses?posting_id=` | GET | 공고별 분석 목록 (신호등 정렬) |
| `/analyses/batch` | POST | 일괄 분석 실행 |
| `/postings/{id}/insights` | POST | 공고 인사이트 생성 |
| `/postings/{id}/insights` | GET | 공고 인사이트 조회 |
| `/analyses/{id}/feedback` | POST | 분석 결과 피드백 제출 |

상세 명세는 [`backend/api.md`](backend/api.md)를 참고하세요.

---

## 데이터 모델

```
users                    # 사용자 (JOBSEEKER / COMPANY)
├── oauth_accounts       # OAuth 연동 (Google)
├── jobseeker_profiles   # 구직자 프로필
└── company_profiles     # 기업 프로필

resumes                  # 서류 (PDF 파싱 결과)
job_postings             # 채용 공고 (텍스트 파싱 결과)
analyses                 # Fit-Gap 분석 결과
posting_insights         # 공고 개선 인사이트
```

---

## 사용자 플로우

### 구직자

```
서류 PDF 업로드 → AI 파싱 결과 확인/수정 → 관심 공고 텍스트 입력
  → Fit-Gap 분석 실행 → 적합도 점수 + 신호등 + Fit/Gap/Over 상세 확인
    → 개선 제안 확인 → 서류 수정 후 재분석
```

### 기업 HR

```
공고 텍스트 입력 → 공고 개선 인사이트 확인 → 지원자 서류 업로드
  → 자동 Fit-Gap 분석 + 신호등 분류
    → 지원자 리스트 (🟢🟡🔴) + 부족 사유 확인
```

---

## AI 신뢰도 전략

| 전략 | 설명 |
|------|------|
| 원문 인용 | 모든 분석 결과에 공고/서류 원문 근거 첨부 |
| 역할 분리 | LLM은 추출+분류만, 점수 산출은 규칙 기반 엔진 |
| 확신도 표시 | 각 항목에 High/Medium/Low 확신도 표기 |
| 재현성 | Temperature 0, JSON Schema 강제로 일관성 확보 |
| 피드백 루프 | 분석 결과마다 동의/비동의 수집 |

---

## 개발 컨벤션

- **코드/주석**: 영어 | **UI 텍스트**: 한국어
- **백엔드**: FastAPI + Pydantic 모델, 도메인별 모듈 분리 (`core/`, `models/`, `logic/`)
- **프론트엔드**: App Router, Server Component 기본, Client Component 최소화
- **API 응답**: `{ success: bool, data: {...} }` 또는 `{ success: bool, error: { code, message } }`
- **브랜치 전략**: 기능별 브랜치 생성 후 개발

---

## 문서

| 문서 | 설명 |
|------|------|
| [`prd.md`](prd.md) | 제품 요구사항 정의서 |
| [`use_cases.md`](use_cases.md) | 유스케이스 상세 (UC-01 ~ UC-10) |
| [`idea_revision.md`](idea_revision.md) | 아이디어 정리 및 경쟁 분석 |
| [`backend/api.md`](backend/api.md) | API 명세서 |
| [`backend/schema.sql`](backend/schema.sql) | 데이터베이스 스키마 |