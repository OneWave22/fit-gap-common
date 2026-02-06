const rows = [
  {
    name: "김**",
    exp: "3년",
    edu: "컴공 / 서울",
    score: 89,
    signal: "🟢",
    summary: "필수 스택 충족, 리더십 우수",
  },
  {
    name: "박**",
    exp: "1년",
    edu: "정보보안 / 부산",
    score: 62,
    signal: "🟡",
    summary: "기술 적합도는 높으나 영어 요건 미달",
  },
  {
    name: "이**",
    exp: "5년",
    edu: "전산 / 대전",
    score: 41,
    signal: "🔴",
    summary: "MSA 경험 부족, 핵심 업무 이해도 낮음",
  },
];

export default function ScreeningPage() {
  return (
    <div className="min-h-screen px-6 pb-16 pt-24">
      <div className="mx-auto flex w-full max-w-[1200px] flex-col gap-6">
        <header className="flex flex-col gap-3">
          <h1 className="text-2xl font-bold text-slate-900">
            Back-end DevOps Engineer 공고 지원자 현황
          </h1>
          <div className="flex flex-wrap gap-2 text-xs font-semibold">
            <span className="rounded-full bg-slate-100 px-3 py-1 text-slate-600">
              전체 124
            </span>
            <span className="rounded-full bg-emerald-50 px-3 py-1 text-emerald-700">
              🟢 적합 12
            </span>
            <span className="rounded-full bg-amber-50 px-3 py-1 text-amber-700">
              🟡 보류 45
            </span>
            <span className="rounded-full bg-rose-50 px-3 py-1 text-rose-700">
              🔴 부적합 67
            </span>
          </div>
        </header>

        <section className="space-y-3">
          {rows.map((row) => (
            <div
              key={row.name}
              className="flex flex-col gap-3 rounded-2xl border border-slate-200 bg-white px-6 py-4 shadow-sm transition hover:-translate-y-1 hover:shadow-lg md:flex-row md:items-center md:justify-between"
            >
              <div className="flex items-center gap-4">
                <div className="text-2xl">{row.signal}</div>
                <div>
                  <p className="text-sm font-semibold text-slate-900">
                    {row.name}
                  </p>
                  <p className="text-xs text-slate-500">
                    경력 {row.exp} · {row.edu}
                  </p>
                </div>
              </div>
              <div className="text-lg font-bold text-slate-900">
                {row.score}점
              </div>
              <p className="text-xs font-semibold text-slate-600 md:max-w-[280px]">
                {row.summary}
              </p>
              <div className="flex items-center gap-2">
                <button className="rounded-lg border border-slate-200 bg-white px-3 py-2 text-xs font-semibold text-slate-700">
                  상세 보기
                </button>
                <button className="rounded-lg bg-slate-900 px-3 py-2 text-xs font-semibold text-white">
                  피드백 메일
                </button>
              </div>
            </div>
          ))}
        </section>
      </div>
    </div>
  );
}
