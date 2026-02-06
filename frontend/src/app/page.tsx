export default function Home() {
  return (
    <div className="min-h-screen text-slate-900">
      <header className="fixed left-0 right-0 top-0 z-20 border-b border-white/50 bg-white/80 backdrop-blur-md">
        <div className="mx-auto flex w-full max-w-[1200px] items-center justify-between px-6 py-4">
          <span className="text-lg font-extrabold text-blue-700">Fit-Gap</span>
          <nav className="hidden items-center gap-6 text-sm font-medium text-slate-600 md:flex">
            <a className="transition hover:text-slate-900" href="#features">
              기능 소개
            </a>
            <a className="transition hover:text-slate-900" href="#pricing">
              요금제
            </a>
            <a className="transition hover:text-slate-900" href="#contact">
              문의하기
            </a>
          </nav>
          <div className="flex items-center gap-3">
            <a
              className="text-sm font-medium text-slate-600 hover:text-slate-900"
              href="/login"
            >
              로그인
            </a>
            <button className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-blue-700">
              무료로 시작하기
            </button>
          </div>
        </div>
      </header>

      <main className="mx-auto flex w-full max-w-[1200px] flex-col gap-24 px-6 pb-20 pt-36">
        <section className="flex flex-col gap-12">
          <div className="flex flex-col gap-6">
            <span className="w-fit rounded-full bg-blue-50 px-4 py-2 text-xs font-semibold text-blue-700">
              AI 기반 채용 분석 솔루션
            </span>
            <h1 className="max-w-2xl text-4xl font-extrabold leading-tight tracking-tight text-slate-900 md:text-5xl">
              합격과 불합격 사이,
              <br />
              그 <span className="text-blue-700">1%의 차이</span>를 분석합니다.
            </h1>
            <p className="max-w-2xl text-base leading-relaxed text-slate-600 md:text-lg">
              무지성 지원은 그만. 공고(JD)와 내 서류의 Fit-Gap을 정밀 분석하여
              부족한 역량과 합격 가능성을 신호등으로 확인하세요.
            </p>
            <div className="flex flex-col gap-3 sm:flex-row">
              <button className="flex items-center justify-center gap-2 rounded-lg bg-blue-600 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-blue-200 transition hover:bg-blue-700">
                구직자 시작하기
                <span aria-hidden>→</span>
              </button>
              <button className="flex items-center justify-center gap-2 rounded-lg border border-slate-300 bg-white px-6 py-3 text-sm font-semibold text-slate-700 transition hover:border-slate-400 hover:bg-slate-50">
                기업 HR 도입문의
              </button>
            </div>
          </div>
        </section>

        <section className="rounded-3xl border border-white/80 bg-white/70 p-10 shadow-xl shadow-blue-100">
          <div className="grid gap-10 md:grid-cols-[1.1fr_0.9fr]">
            <div className="flex flex-col gap-4">
              <h2 className="text-2xl font-bold text-slate-900">
                공고와 서류가 만나는 순간, 분석 리포트가 자동 생성
              </h2>
              <p className="text-sm leading-relaxed text-slate-600">
                좌측에서 이력서 PDF, 우측에서 공고 텍스트가 합쳐지며 실시간으로
                Fit/GAP 요약과 차트를 보여주는 인터랙티브 데모를 제공합니다.
              </p>
              <div className="flex items-center gap-3 text-xs font-medium text-slate-500">
                <span className="rounded-full bg-blue-50 px-3 py-1 text-blue-700">
                  Resume PDF
                </span>
                <span className="rounded-full bg-slate-100 px-3 py-1 text-slate-600">
                  Job Description
                </span>
                <span className="rounded-full bg-emerald-50 px-3 py-1 text-emerald-700">
                  Report
                </span>
              </div>
            </div>
            <div className="relative flex h-60 items-center justify-center overflow-hidden rounded-2xl border border-slate-200 bg-gradient-to-br from-blue-50 via-white to-emerald-50">
              <div className="absolute left-6 top-8 rounded-xl bg-white px-4 py-3 text-xs font-semibold text-slate-500 shadow">
                이력서 PDF
              </div>
              <div className="absolute right-6 top-10 rounded-xl bg-white px-4 py-3 text-xs font-semibold text-slate-500 shadow">
                공고 텍스트
              </div>
              <div className="flex flex-col items-center gap-2">
                <div className="h-12 w-12 rounded-full bg-blue-600/90" />
                <div className="h-16 w-36 rounded-xl border border-slate-200 bg-white shadow-sm" />
              </div>
            </div>
          </div>
        </section>

        <section id="features" className="grid gap-6 md:grid-cols-3">
          {[
            {
              title: "단순 매칭이 아닙니다",
              desc: "의미 단위로 경력을 분석해 정확한 Fit을 찾아냅니다.",
              icon: "🔎",
            },
            {
              title: "3초 만에 판단하는 합격률",
              desc: "직관적인 신호등 등급으로 지원 여부를 결정하세요.",
              icon: "🚦",
            },
            {
              title: "구체적인 개선 가이드",
              desc: "'Redis 경험 추가' 같은 실행 가능한 조언을 제공합니다.",
              icon: "🧭",
            },
          ].map((item) => (
            <article
              key={item.title}
              className="rounded-2xl border border-slate-200 bg-white p-6 shadow-md transition hover:-translate-y-1 hover:shadow-xl"
            >
              <div className="text-2xl">{item.icon}</div>
              <h3 className="mt-4 text-lg font-semibold text-slate-900">
                {item.title}
              </h3>
              <p className="mt-2 text-sm leading-relaxed text-slate-600">
                {item.desc}
              </p>
            </article>
          ))}
        </section>

        <section
          id="pricing"
          className="rounded-3xl border border-slate-200 bg-white p-10"
        >
          <div className="flex flex-col gap-6 md:flex-row md:items-end md:justify-between">
            <div>
              <h2 className="text-2xl font-bold text-slate-900">
                구직자와 기업 모두를 위한 요금제
              </h2>
              <p className="mt-2 text-sm text-slate-600">
                B2C 무료 유입에서 B2B 스크리닝 과금까지 이어지는 구조.
              </p>
            </div>
            <button className="rounded-lg bg-slate-900 px-4 py-2 text-xs font-semibold text-white">
              요금제 자세히 보기
            </button>
          </div>
          <div className="mt-8 grid gap-4 md:grid-cols-3">
            {[
              {
                title: "B2C Free",
                price: "무료",
                desc: "공고 3개 x 서류 3개 Fit-Gap 분석",
              },
              {
                title: "B2C Pro",
                price: "월 9,900원",
                desc: "무제한 분석 + 시뮬레이션 + 개선 제안",
              },
              {
                title: "B2B Growth",
                price: "월 199,000원",
                desc: "스크리닝 무제한 + 공고 개선 인사이트",
              },
            ].map((plan) => (
              <div
                key={plan.title}
                className="rounded-2xl border border-slate-200 bg-slate-50 p-6"
              >
                <p className="text-sm font-semibold text-slate-700">
                  {plan.title}
                </p>
                <p className="mt-2 text-xl font-bold text-slate-900">
                  {plan.price}
                </p>
                <p className="mt-2 text-xs text-slate-600">{plan.desc}</p>
              </div>
            ))}
          </div>
        </section>
      </main>

      <footer
        id="contact"
        className="border-t border-slate-200 bg-white/70 py-10"
      >
        <div className="mx-auto flex w-full max-w-[1200px] flex-col items-start justify-between gap-4 px-6 text-sm text-slate-600 md:flex-row md:items-center">
          <div>
            <p className="font-semibold text-slate-800">Fit-Gap</p>
            <p>문의: contact@fitgap.ai</p>
          </div>
          <p className="text-xs text-slate-500">
            본 서비스의 분석 결과는 참고 자료이며 최종 판단은 사용자에게
            있습니다.
          </p>
        </div>
      </footer>
    </div>
  );
}
