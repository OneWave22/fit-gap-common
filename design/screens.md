# 화면 설계서 (UI Specification for Design AI)

**문서 정보**
- **목적:** 디자인 AI 툴(Galileo AI, Uizard, v0 등)에 직접 입력하기 위한 초상세 UI 명세서
- **업데이트:** 2026-02-07 (Ultra-Detailed Revision)
- **참조:** [prd.md](../prd.md), [use_cases.md](../use_cases.md), [design/screens.md](./screens.md)

---

## 🎨 Global Design System

### Design Tokens

**Layout**
- Container Max Width: `1280px`
- Content Max Width: `1024px`
- Narrow Column: `800px`
- Gutter: `24px` (Desktop), `16px` (Mobile)
- Grid Columns: `12 columns`
- Grid Gap: `24px`

**Spacing Scale (8pt Grid)**
- `xs`: `4px`
- `sm`: `8px`
- `md`: `16px`
- `lg`: `24px`
- `xl`: `32px`
- `2xl`: `48px`
- `3xl`: `64px`
- `4xl`: `96px`

**Color System**

*Primary Brand*
- Blue 600: `#3B82F6` (Main CTA, Links)
- Blue 700: `#2563EB` (Hover)
- Blue 500: `#60A5FA` (Light accent)
- Blue 50: `#EFF6FF` (Background tint)

*Traffic Light System*
- Green 500 (Fit): `#10B981`
- Green 100: `#ECFDF5` (Background)
- Green 200: `#A7F3D0` (Border)
- Amber 500 (Hold): `#F59E0B`
- Amber 100: `#FFFBEB`
- Amber 200: `#FDE68A`
- Rose 500 (Gap): `#F43F5E`
- Rose 100: `#FFF1F2`
- Rose 200: `#FECDD3`

*Neutral Palette*
- Gray 900: `#0F172A` (Heading text)
- Gray 700: `#334155` (Body text)
- Gray 500: `#64748B` (Caption, placeholder)
- Gray 300: `#CBD5E1` (Border)
- Gray 100: `#F1F5F9` (Light background)
- Gray 50: `#F8FAFC` (Main background)
- White: `#FFFFFF`

**Typography**

*Font Families*
- Korean: `'Pretendard Variable', -apple-system, sans-serif`
- English/Numbers: `'Inter', sans-serif`
- Monospace: `'JetBrains Mono', monospace`

*Font Sizes & Weights*
- Display: `48px / 56px line-height / 800 weight / -0.02em tracking`
- H1: `36px / 44px / 700 / -0.01em`
- H2: `24px / 32px / 700 / -0.01em`
- H3: `20px / 28px / 600 / 0em`
- Body Large: `16px / 24px / 400 / 0em`
- Body: `15px / 22px / 400 / 0em`
- Caption: `13px / 18px / 500 / 0em`
- Small: `12px / 16px / 400 / 0em`

**Border Radius**
- `xs`: `4px` (Tags, badges)
- `sm`: `6px` (Buttons)
- `md`: `8px` (Cards)
- `lg`: `12px` (Modals, large cards)
- `xl`: `16px` (Hero sections)
- `full`: `9999px` (Pills, circular)

**Shadows**
- `sm`: `0 1px 2px 0 rgba(0, 0, 0, 0.05)`
- `md`: `0 4px 6px -1px rgba(0, 0, 0, 0.1)`
- `lg`: `0 10px 15px -3px rgba(0, 0, 0, 0.1)`
- `xl`: `0 20px 25px -5px rgba(0, 0, 0, 0.1)`
- `2xl`: `0 25px 50px -12px rgba(0, 0, 0, 0.25)`

**Component Specs**

*Button*
- Primary: `bg-blue-600`, `text-white`, `px-24px py-12px`, `border-radius-6px`, `font-size-15px weight-600`, `shadow-sm`
  - Hover: `bg-blue-700`, `shadow-md`, `transform scale(1.02)`
  - Active: `bg-blue-800`, `shadow-sm`, `scale(0.98)`
  - Disabled: `bg-gray-300`, `text-gray-500`, `cursor-not-allowed`
- Secondary: `bg-white`, `text-gray-700`, `border-1px gray-300`, Same padding/size
  - Hover: `bg-gray-50`, `border-gray-400`
- Ghost: `bg-transparent`, `text-gray-700`, Same padding
  - Hover: `bg-gray-100`

*Card*
- Background: `white`
- Border: `1px solid gray-200` or `none`
- Radius: `12px`
- Padding: `24px`
- Shadow: `md` (default), `lg` on hover
- Hover: `transform translateY(-4px)`, `shadow-xl`, `transition 200ms ease`

*Input Field*
- Height: `44px`
- Padding: `12px 16px`
- Border: `1px solid gray-300`
- Border Radius: `6px`
- Font: `15px / gray-900`
- Placeholder: `gray-500`
- Focus: `border-blue-500`, `ring-2px blue-100`, `outline-none`

*Tag/Chip*
- Height: `28px`
- Padding: `6px 12px`
- Border Radius: `4px`
- Font: `13px / 500`
- Background: `gray-100`
- Text: `gray-700`
- With close icon: `padding-right 8px`, `icon size 16px`

---

## 🖥️ Screen 1. 랜딩 페이지 (Landing Page)

**ID:** SCR-01
**Route:** `/`
**Type:** Marketing Page

### 1.1 UI Specification (Desktop)

**Layout: Single Column Scroll**

*   **Header (Fixed Top, Blur Effect):**
    *   **Left:** 로고 `Fit-Gap` (Bold, Blue color).
    *   **Center:** 네비게이션 `기능 소개`, `요금제`, `문의하기`. (Hover 시 밑줄 애니메이션).
    *   **Right:**
        *   `로그인` (Text Button, Gray).
        *   `무료로 시작하기` (Primary Button, Radius 8px, Blue).
*   **Section 1: Hero (Center Aligned, Padding Top 120px):**
    *   **Badge:** "AI 기반 채용 분석 솔루션" (Pill Shape, Blue Light Bg).
    *   **Headline:** "합격과 불합격 사이,<br/>그 **1%의 차이**를 분석합니다." (H1, 48px, Keyword **Dark Blue** 강조).
    *   **Sub-text:** "무지성 지원은 그만. 공고(JD)와 내 서류의 **Fit-Gap**을 정밀 분석하여<br/>부족한 역량과 합격 가능성을 신호등으로 확인하세요." (Gray-600).
    *   **CTA Group:**
        *   `구직자 시작하기` (Primary Blue, Right Arrow Icon, Shadow-lg).
        *   `기업 HR 도입문의` (Outline Gray, Business Icon).
*   **Section 2: Visual Demo (Interactive Container):**
    *   **Container:** 맥북 프레임 또는 브라우저 창 목업 이미지.
    *   **Animation:** 좌측에서 '이력서 PDF' 아이콘이 날아오고, 우측에서 '공고 텍스트'가 날아와 중앙에서 만나 스파크가 튀며 분석 리포트(차트)가 생성되는 **Lottie** 애니메이션.
*   **Section 3: Feature Grid (3 Columns):**
    *   **Card Style:** White Bg, Hover 시 Y축 -5px 이동 및 Shadow 강화.
    *   **Card 1 (Deep Analysis):** 아이콘(돋보기+문서) + "단순 매칭이 아닙니다" + "의미 단위로 경력을 분석해 정확한 Fit을 찾아냅니다."
    *   **Card 2 (Traffic Light):** 아이콘(신호등) + "3초 만에 판단하는 합격률" + "직관적인 신호등 등급으로 지원 여부를 결정하세요."
    *   **Card 3 (Action Item):** 아이콘(나침반) + "구체적인 개선 가이드" + "'Redis 경험 추가' 같은 실행 가능한 조언을 제공합니다."

### 1.2 UX & Micro-interactions
*   **Scroll Reveal:** 스크롤 시 각 섹션이 `Fade-in Up` 되며 나타남.
*   **Sticky Header:** 스크롤 시작 시 헤더 배경이 불투명해지며 `Box-shadow` 생성.

### 1.3 Mobile Considerations
*   **Hero:** 텍스트 크기 축소 (H1 32px), 줄바꿈 최적화.
*   **CTA:** 버튼을 세로로 배치 (Stack)하여 터치 영역 확보.
*   **Visual:** 애니메이션을 정지 이미지(GIF)로 대체하거나 크기 축소.

---

## 📄 Screen 2. 서류 업로드 및 파싱 (Resume Upload)

**ID:** SCR-02
**Route:** `/resumes`
**Type:** Form / Utility

### 2.1 UI Specification (Desktop)

**Layout: Split Screen (Left: Upload / Right: Preview)**

*   **Left Panel (Upload Zone, 40% width):**
    *   **Dropzone:** 화면 중앙 배치. 점선 테두리 (`border-dashed`, `border-blue-200`). 배경색 Hover 시 `alice-blue`.
    *   **Content:**
        *   Cloud Upload Icon (Large, Gray-400).
        *   Text: "PDF 파일을 이곳에 드래그하세요".
        *   Button: `파일 선택하기` (Secondary Style).
        *   Caption: "텍스트 복사 가능한 PDF만 지원 (Max 10MB)".
*   **Right Panel (Parsing Result, 60% width, Gray Bg):**
    *   **State 1 (Empty):** "서류를 업로드하면 AI가 핵심 역량을 추출합니다" 안내 일러스트.
    *   **State 2 (Loading):** 스켈레톤 UI + "AI가 문서를 분석 중입니다..." 텍스트 + Progress Bar.
    *   **State 3 (Complete - Review Mode):**
        *   **Header:** "추출된 데이터 확인" + `재직무/직군 수정` 드롭다운.
        *   **Section: 기술 스택 (Skills):**
            *   Tags Container. 각 태그는 `Removable Chip` 스타일 (X 버튼 포함).
            *   Interaction: 빈 곳 클릭 시 텍스트 입력하여 태그 추가 가능.
        *   **Section: 주요 경험 (Experience):**
            *   List items. 각 항목에 `Edit(Pencil)` 아이콘.
            *   클릭 시 모달이나 인라인 에디터로 내용 수정.
*   **Bottom Action Bar (Floating):**
    *   **Right:** `저장하고 공고 입력하기` (Primary Button, Disabled until upload complete).

### 2.2 UX & Micro-interactions
*   **Drag & Drop:** 파일 진입 시 Dropzone 테두리가 진한 파란색으로 변경 (`drag-over`).
*   **Toast Alert:** 파일 형식이 틀리거나(이미지 등) 파싱 실패 시 상단에 에러 토스트 메시지 출력.

---

## 📝 Screen 3. 공고 입력 (Job Posting Input)

**ID:** SCR-03
**Route:** `/postings`
**Type:** Form / Input

### 3.1 UI Specification (Desktop)

**Layout: Centered Single Column (Max-width 800px)**

*   **Step Indicator:** `서류 업로드(완료)` - `**공고 입력(Current)**` - `분석 결과(Next)`
*   **Main Card:**
    *   **Title:** "분석하고 싶은 채용 공고를 입력해주세요" (H2).
    *   **Input 1: 기업/공고명:** Placeholder "예: 토스 / 백엔드 개발자".
    *   **Input 2: 공고 내용 (Textarea):**
        *   Height: 400px 이상 충분한 공간.
        *   Placeholder: "채용 공고의 [자격 요건]과 [우대 사항] 부분을 복사해서 붙여넣으세요..."
        *   **Smart Feature:** 텍스트 붙여넣기 시, 하단에 **"감지된 키워드"**들이 실시간으로 페이드인 됨. (예: `Java`, `Spring`, `MSA`). → *사용자가 "아, 잘 인식되고 있구나"를 느끼게 함.*
*   **Action Area:**
    *   `분석 시작하기` (Primary, Large, W-Full or Wide).
    *   클릭 시 로딩 오버레이 작동.

### 3.2 Loading Overlay (Critical UX)
*   **Design:** 전체 화면 흐림 처리(`backdrop-blur`). 중앙에 로딩 스피너.
*   **Progress Text Cycling:**
    1.  "공고의 핵심 요구사항을 추출하고 있습니다..."
    2.  "내 서류와 비교 분석 중입니다..."
    3.  "개선 제안을 생성하고 있습니다..."
*   **Purpose:** 10~30초 소요되는 분석 시간 동안 이탈 방지.

---

## 📊 Screen 4. 분석 결과 (Analysis Dashboard)

**ID:** SCR-04
**Route:** `/analysis/[id]`
**Type:** Dashboard / Data Visualization

### 4.1 UI Specification (Desktop)

**Layout: Dashboard Grid (Header + 3 Columns Body)**

*   **Header (Score Card):**
    *   **Left:** **Total Score Donut Chart.** 중앙에 점수(예: `78`) 표시. 점수 색상은 트래픽 라이트(🟡노랑).
    *   **Center:**
        *   **Verdict:** "보류 (Hold)" 배지 (Large).
        *   **One-line Feedback:** "기술 핏은 좋으나, 리더십 경험 증명이 부족합니다." (Typing effect).
    *   **Right:** `서류 수정하기` (Ghost Button), `다른 공고 분석` (Outline Button).

*   **Body Grid (3 Columns, Gap 24px):**
    
    *   **Column 1: Breakdown (상세 점수)**
        *   **Chart:** Radar Chart (5각형: 기술, 경험, 소프트스킬, 우대사항, 성과).
        *   **Stats List:** 각 항목별 점수와 `Confidence(확신도)` 표시.
            *   예: 기술 일치도 90점 (Medium Confidence).
            *   확신도 `Low`인 경우 툴팁 아이콘(?): "텍스트 정보가 부족해 정확한 판단이 어렵습니다."

    *   **Column 2: ✅ Fit (강점 분석)**
        *   **Header:** "매칭 포인트 (3)" (Green Text).
        *   **Card Item:**
            *   Title: "Spring Framework 숙련도".
            *   Reason: "공고에서 3년 이상을 요구했으며, 서류 프로젝트 A, B에서 메인 스택으로 사용됨."
            *   **Citation (인용):** 공고 원문(`"Spring 3년 이상"`)과 서류 원문(`"Spring 기반 4년 부하 분산 경험"`)을 작은 회색 박스로 하단에 매칭 표시.

    *   **Column 3: ⚠️ Gap (보완 필요) - 가장 중요**
        *   **Header:** "보완 필요 (2)" (Red Text).
        *   **Card Item (Highlight):**
            *   Border: Red-200, Bg: Red-50.
            *   Title: "MSA 경험 부재".
            *   Desc: "공고는 MSA 환경 경험을 우대하지만, 서류에는 Monolithic 경험만 기술됨."
            *   **💡 Actionable Insight (Box):** "서류의 [프로젝트 A] 설명에 모듈 간 통신이나 API 설계 경험을 구체적으로 추가하여 간접 어필해보세요."

*   **Footer Feedback:**
    *   "이 분석 결과가 도움이 되었나요?" 👍 / 👎 버튼.
    *   👎 클릭 시 "이유를 알려주세요" 팝오버 (객관식 선택).

### 4.2 UX & Micro-interactions
*   **Citation Hover:** Fit/Gap 카드의 내용을 호버하면, 분석의 근거가 된 문장이 하이라이트 되거나 툴팁으로 원문이 뜸.
*   **Expansion:** `Over Spec(과잉 스펙)` 항목은 기본적으로 접혀있고 ("과잉 항목 1개 더보기"), 클릭 시 펼쳐짐.

### 4.3 Mobile Considerations
*   **Tab Navigation:** 상단 점수는 고정하고, 하단을 `[전체]`, `[강점(Fit)]`, `[보완(Gap)]` 탭으로 분리하여 스와이프 가능한 뷰로 제공.
*   **Focus:** 모바일에서는 차트보다 **텍스트 피드백과 개선 제안**이 먼저 보이도록 배치 순서 변경.

---

## 🚦 Screen 5. 기업용 스크리닝 리스트 (Employer Dashboard)

**ID:** SCR-05
**Route:** `/screening`
**Type:** Admin / List

### 5.1 UI Specification (Desktop)

**Layout: Sidebar + Main List**

*   **Header:**
    *   Title: "Back-end DevOps Engineer 공고 지원자 현황".
    *   Stats Chips: `전체 124` | `🟢 적합 12` | `🟡 보류 45` | `🔴 부적합 67`. (클릭 시 필터링).

*   **List Table (Card List Style):**
    *   **Row Item (Height: 80px, White Bg, Round 12px, Hover-Shadow):**
        *   **Col 1 (Signal):** 신호등 원형 아이콘 (🔴/🟡/🟢).
        *   **Col 2 (Profile):** 이름(김**), 경력(3년), 학력 요약.
        *   **Col 3 (Score):** **89점** (Color coded).
        *   **Col 4 (AI Summary - 핵심):** "필수 스택 충족, 리더십 우수" 또는 "영어 요건 미달(Gap)".
            *   *Gap 요소는 빨간색 텍스트로 강조.*
        *   **Col 5 (Action):** `상세 보기` 버튼, `피드백 메일` 아이콘.

*   **Feature: Feedback Mail (Modal):**
    *   부적합(🔴) 지원자의 메일 아이콘 클릭 시 모달 팝업.
    *   **Title:** "김**님 불합격 통보 메일 생성".
    *   **Content (AI Generated):** " ~한 강점이 인상 깊었으나, [MSA 경험] 부분에서 아쉬움이 있어..." (AI가 생성한 정중한 거절 멘트).
    *   **Actions:** `복사하기`, `보내기`.

### 5.2 Mobile Considerations
*   **View:** 테이블 구조를 **카드 리스트**로 변경.
*   **Content:** 이름, 점수, 신호등, 핵심 한 줄 요약만 표시.

---

## 📢 Screen 6. 공고 개선 인사이트 (Job Posting Review)

**ID:** SCR-06
**Route:** `/postings/[id]/insight`
**Type:** Editorial / Analysis

### 6.1 UI Specification (Desktop)

**Layout: Split (Left: Original Text / Right: Insight Cards)**

*   **Left Panel (Source Text):**
    *   공고 원문 표시.
    *   **Interaction:** AI가 지적한 문장(예: "경력 10년 이상")에 **노란색/빨간색 밑줄(Squiggly underline)** 표시.
    *   밑줄 호버 시 우측 해당 인사이트 카드로 포커스 이동.

*   **Right Panel (Insights):**
    *   **Header:** "공고 매력도 분석 결과".
    *   **Card 1 (Critical):** "⚠️ 필수 요건 과다".
        *   Desc: "신입 공고에 8개 이상의 필수 기술을 요구합니다. 지원 장벽이 높습니다."
        *   Suggestion: "핵심 3개로 줄이고 나머지는 우대사항으로 이동하세요."
    *   **Card 2 (Info):** "ℹ️ 복지 혜택 구체화 필요".
        *   Desc: "금전적 보상 외의 성장 기회에 대한 언급이 부족합니다."
    *   **Floating Action:** `수정 모드로 전환` (하단 고정).

### 6.2 UX Detail
*   **Sync Scroll:** 왼쪽 본문을 스크롤하면 관련된 오른쪽 인사이트 카드가 활성화(Active State)됨. IDE의 에러 체크 UX와 유사.

---
