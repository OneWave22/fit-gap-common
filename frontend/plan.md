# Frontend Implementation Plan

## Current State
- Next.js 16.1.6 + React 19 + Tailwind CSS 4 scaffold
- Only default `page.tsx` (template content)
- App Router with `@/*` path alias, Geist font

---

## Phase 0: Project Foundation

### 0-1. Directory structure
```
frontend/src/
  app/
    layout.tsx              # Root layout (Korean lang, metadata, Header)
    page.tsx                # Landing page
    resumes/
      page.tsx              # Resume upload page (UC-01)
    postings/
      page.tsx              # Job posting input page (UC-02)
      [id]/
        page.tsx            # Posting detail + insights view (UC-07)
    analyses/
      [id]/
        page.tsx            # Analysis result detail (UC-04, UC-05)
    screening/
      page.tsx              # Applicant screening list (UC-06)
  components/
    ui/                     # Reusable UI primitives
      Button.tsx
      Card.tsx
      Badge.tsx
      FileUpload.tsx
      TextArea.tsx
      Modal.tsx
      Spinner.tsx
    layout/
      Header.tsx
      Footer.tsx
    resume/
      ResumeUploader.tsx    # PDF drag-and-drop upload
      ParsedResumeView.tsx  # Display/edit parsed resume data
    posting/
      PostingForm.tsx       # Text input form
      ParsedPostingView.tsx # Display/edit parsed posting data
    analysis/
      ScoreOverview.tsx     # Overall score + signal light
      CategoryChart.tsx     # Bar/radar chart for category scores
      FitItemCard.tsx       # Fit item card with citation
      GapItemCard.tsx       # Gap item card with suggestion
      OverItemCard.tsx      # Over item card
      FeedbackWidget.tsx    # Thumbs up/down + reason selector
    screening/
      ApplicantTable.tsx    # Sortable/filterable applicant list
      SignalBadge.tsx       # Green/Yellow/Red indicator
      ApplicantCard.tsx     # Summary card per applicant
    insight/
      InsightCard.tsx       # Posting improvement insight card
  lib/
    api.ts                  # API client (fetch wrapper, base URL, error handling)
    types.ts                # TypeScript types matching backend schemas
    constants.ts            # Signal thresholds, category weights
    utils.ts                # Formatting helpers
  hooks/
    useAnalysis.ts          # Data fetching for analysis
    useResume.ts            # Data fetching for resume
    usePosting.ts           # Data fetching for posting
```

### 0-2. Install additional dependencies
```bash
npm install recharts        # Charts for category scores
npm install react-dropzone  # File upload drag-and-drop
npm install clsx            # Conditional class names
```

### 0-3. API client (`src/lib/api.ts`)
- Base URL from `NEXT_PUBLIC_API_URL` env variable
- Typed fetch wrapper returning `{ success, data }` or `{ success, error }`

### 0-4. Update root layout
- `lang="ko"` in html tag
- Metadata: title "Fit-Gap | AI 채용 분석", description
- Add Header component with navigation

### 0-5. TypeScript types (`src/lib/types.ts`)
- Mirror backend Pydantic schemas as TS interfaces
- ParsedResumeData, ParsedPostingData, AnalysisResponse, InsightCard, etc.

---

## Phase 1: Resume Upload Page (UC-01)

### 1-1. ResumeUploader component
- Drag-and-drop zone (react-dropzone)
- PDF only, max 10MB validation
- Upload progress indicator
- Calls `POST /v1/resumes` with FormData

### 1-2. ParsedResumeView component
- Editable card layout: skills (tag chips), experiences (expandable), metrics, soft_skills, keywords
- "Save changes" → `PATCH /v1/resumes/{id}`
- "Proceed to analysis" → navigate to posting input

### 1-3. Resume page (`app/resumes/page.tsx`)
- Flow: upload → loading → parsed result display
- Error states: file too large, unsupported type, parse failure + retry

---

## Phase 2: Job Posting Input Page (UC-02)

### 2-1. PostingForm component
- Large textarea for pasting job posting text
- Optional company name field
- Min 100 char validation + character count
- Submit → `POST /v1/postings`

### 2-2. ParsedPostingView component
- Display: required_skills, preferred_skills, responsibilities, required_experience, culture_keywords
- Editable fields with save
- "Run Analysis" button (when resume + posting exist)
- "Get Insights" button (employer view)

### 2-3. Posting page (`app/postings/page.tsx`)
- Accept resume_id as query param for flow context
- Flow: input → loading → parsed result

---

## Phase 3: Analysis Result Page (UC-03, UC-04, UC-05)

### 3-1. ScoreOverview component
- Large circular/semi-circular score display (0-100)
- Signal light badge (green/yellow/red) with Korean label
- Confidence indicator
- Disclaimer text

### 3-2. CategoryChart component
- Bar or radar chart (recharts)
- 5 categories with scores and weights
- Color coding per category

### 3-3. Fit/Gap/Over item cards
- FitItemCard: green accent, posting source + resume source + match score + explanation
- GapItemCard: red accent, posting requirement + "not found" + suggestion
- OverItemCard: gray accent, resume item with no posting match

### 3-4. FeedbackWidget component
- Thumbs up/down buttons
- On thumbs down: reason selector (checkboxes) + optional comment
- Calls `POST /v1/analyses/{id}/feedback`

### 3-5. Analysis page (`app/analyses/[id]/page.tsx`)
- Fetch analysis by ID
- Sections: Overview | Fit Items | Gap Items | Over Items | Improvement Suggestions
- Summary text + disclaimer banner

---

## Phase 4: Screening List Page (UC-06)

### 4-1. ApplicantTable component
- Table/list of all analyses for a posting
- Columns: signal badge, score, candidate summary, top gap, top strength
- Sorting by score, filtering by signal

### 4-2. Summary bar
- Total count + breakdown: N green, N yellow, N red
- Filter buttons

### 4-3. Screening page (`app/screening/page.tsx`)
- posting_id as query param
- Pagination support
- Batch upload: multiple PDFs for employer flow

---

## Phase 5: Posting Insights Page (UC-07)

### 5-1. InsightCard component
- Severity icon (critical=red, warning=orange, info=blue)
- Title, description, source, suggested action
- Expandable detail

### 5-2. Insights section (`app/postings/[id]/page.tsx`)
- Fetch/generate insights
- Display 2-3 insight cards

---

## Phase 6: Landing Page & Navigation

### 6-1. Landing page (`app/page.tsx`)
- Hero: "합격과 불합격 사이, 그 1%의 이유를 찾아주는 AI"
- Two CTAs: "구직자로 시작" → /resumes, "기업 HR로 시작" → /postings
- Feature overview (3 cards: Fit-Gap Analysis, Signal Screening, Posting Insights)

### 6-2. Header component
- Logo / service name
- Nav: Home, Resume Upload, Job Posting, Screening
- Responsive mobile menu

### 6-3. Footer component
- Disclaimer text
- Copyright

---

## Phase 7: Deployment & Polish

### 7-1. Vercel deployment
- `NEXT_PUBLIC_API_URL` pointing to Fly.io backend
- Root directory: `frontend/`

### 7-2. Responsive design
- Mobile-first: 375px / 768px / 1024px+

### 7-3. Loading states
- Skeleton loaders for data fetching
- Analysis progress indicator (up to 30s)

### 7-4. Error handling
- Toast notifications for API errors
- Retry buttons for failed LLM calls

### 7-5. Accessibility
- Semantic HTML, ARIA labels for signal colors
- Keyboard navigation
