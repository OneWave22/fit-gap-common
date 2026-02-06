export default function AnalysisPage() {
  return (
    <div className="min-h-screen px-6 pb-16 pt-24">
      <div className="mx-auto flex w-full max-w-[1200px] flex-col gap-6">
        <header className="grid gap-6 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm md:grid-cols-[1fr_1.2fr_0.8fr]">
          <div className="flex items-center gap-6">
            <div className="relative flex h-24 w-24 items-center justify-center rounded-full border-[10px] border-amber-200 text-2xl font-bold text-amber-600">
              78
            </div>
            <div>
              <p className="text-xs font-semibold text-slate-500">Total Score</p>
              <p className="text-lg font-bold text-slate-900">
                보류 (Hold)
              </p>
            </div>
          </div>
          <div className="flex flex-col justify-center gap-2">
            <p className="text-xs font-semibold text-slate-500">One-line</p>
            <p className="text-sm font-semibold text-slate-800">
              기술 핏은 좋으나, 리더십 경험 증명이 부족합니다.
            </p>
          </div>
          <div className="flex flex-wrap items-center gap-3">
            <button className="rounded-lg border border-slate-200 bg-white px-4 py-2 text-xs font-semibold text-slate-700">
              서류 수정하기
            </button>
            <button className="rounded-lg border border-slate-300 bg-slate-900 px-4 py-2 text-xs font-semibold text-white">
              다른 공고 분석
            </button>
          </div>
        </header>

        <section className="grid gap-6 lg:grid-cols-3">
          <div className="rounded-2xl border border-slate-200 bg-white p-6">
            <h2 className="text-sm font-semibold text-slate-800">
              상세 점수
            </h2>
            <div className="mt-4 h-40 rounded-xl border border-dashed border-slate-200 bg-slate-50" />
            <div className="mt-4 space-y-2 text-xs text-slate-600">
              <div className="flex items-center justify-between">
                <span>기술 일치도</span>
                <span className="font-semibold text-slate-800">
                  90점 (Medium)
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span>직무 경험</span>
                <span className="font-semibold text-slate-800">
                  72점 (High)
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span>소프트 스킬</span>
                <span className="font-semibold text-slate-800">
                  61점 (Low)
                </span>
              </div>
            </div>
          </div>

          <div className="rounded-2xl border border-emerald-100 bg-emerald-50/40 p-6">
            <h2 className="text-sm font-semibold text-emerald-700">
              매칭 포인트 (3)
            </h2>
            <div className="mt-4 space-y-4">
              {[
                {
                  title: "Spring Framework 숙련도",
                  desc: "공고에서 3년 이상을 요구했으며, 서류 프로젝트 A, B에서 메인 스택으로 사용됨.",
                },
                {
                  title: "대용량 트래픽 대응",
                  desc: "캐시 전략과 배치 처리 경험이 공고의 핵심 업무와 일치.",
                },
              ].map((item) => (
                <div
                  key={item.title}
                  className="rounded-xl border border-emerald-100 bg-white p-4 text-xs text-slate-600 shadow-sm"
                >
                  <p className="text-sm font-semibold text-slate-800">
                    {item.title}
                  </p>
                  <p className="mt-1">{item.desc}</p>
                  <div className="mt-3 rounded-md bg-slate-50 px-3 py-2 text-[11px] text-slate-500">
                    공고: "Spring 3년 이상" · 서류: "Spring 기반 4년 부하 분산 경험"
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="rounded-2xl border border-rose-100 bg-rose-50/40 p-6">
            <h2 className="text-sm font-semibold text-rose-600">
              보완 필요 (2)
            </h2>
            <div className="mt-4 space-y-4">
              {[
                {
                  title: "MSA 경험 부재",
                  desc: "공고는 MSA 환경 경험을 우대하지만, 서류에는 Monolithic 경험만 기술됨.",
                  insight:
                    "프로젝트 A 설명에 모듈 간 통신이나 API 설계 경험을 구체적으로 추가하세요.",
                },
              ].map((item) => (
                <div
                  key={item.title}
                  className="rounded-xl border border-rose-200 bg-white p-4 text-xs text-slate-600 shadow-sm"
                >
                  <p className="text-sm font-semibold text-slate-800">
                    {item.title}
                  </p>
                  <p className="mt-1">{item.desc}</p>
                  <div className="mt-3 rounded-lg border border-rose-200 bg-rose-50 px-3 py-2 text-[11px] text-rose-600">
                    💡 {item.insight}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        <footer className="rounded-2xl border border-slate-200 bg-white p-6 text-sm text-slate-600">
          이 분석 결과가 도움이 되었나요?
          <div className="mt-3 flex gap-2">
            <button className="rounded-full bg-slate-900 px-4 py-2 text-xs font-semibold text-white">
              👍 도움됨
            </button>
            <button className="rounded-full border border-slate-300 bg-white px-4 py-2 text-xs font-semibold text-slate-600">
              👎 별로임
            </button>
          </div>
        </footer>
      </div>
    </div>
  );
}
