const highlights = [
  {
    label: "⚠️ 필수 요건 과다",
    desc: "신입 공고에 8개 이상의 필수 기술을 요구합니다. 지원 장벽이 높습니다.",
    suggestion: "핵심 3개로 줄이고 나머지는 우대사항으로 이동하세요.",
  },
  {
    label: "ℹ️ 복지 혜택 구체화 필요",
    desc: "금전적 보상 외의 성장 기회에 대한 언급이 부족합니다.",
    suggestion: "성장 로드맵, 멘토링, 교육 지원을 명시하세요.",
  },
];

export default function InsightPage() {
  return (
    <div className="min-h-screen px-6 pb-16 pt-24">
      <div className="mx-auto grid w-full max-w-[1200px] gap-6 lg:grid-cols-[1.2fr_0.8fr]">
        <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h1 className="text-lg font-semibold text-slate-900">
            공고 원문
          </h1>
          <div className="mt-4 space-y-4 text-sm text-slate-700">
            <p className="leading-relaxed">
              우리는 백엔드 개발자를 찾고 있습니다.{" "}
              <span className="border-b-2 border-rose-300 text-rose-600">
                경력 10년 이상
              </span>{" "}
              및{" "}
              <span className="border-b-2 border-amber-300 text-amber-700">
                8개 이상의 필수 기술 스택
              </span>
              을 요구합니다. MSA, Kubernetes, Kafka 등 실무 경험이 필요합니다.
            </p>
            <p className="leading-relaxed">
              복지와 문화는 유연한 근무 환경을 제공합니다.{" "}
              <span className="border-b-2 border-amber-300 text-amber-700">
                성장 지원 관련 문구가 부족
              </span>
              합니다.
            </p>
          </div>
        </section>

        <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-slate-900">
              공고 매력도 분석 결과
            </h2>
            <span className="rounded-full bg-rose-50 px-3 py-1 text-xs font-semibold text-rose-600">
              개선 필요
            </span>
          </div>
          <div className="mt-4 space-y-4">
            {highlights.map((item) => (
              <article
                key={item.label}
                className="rounded-xl border border-slate-200 bg-slate-50 p-4 text-sm"
              >
                <p className="font-semibold text-slate-900">{item.label}</p>
                <p className="mt-2 text-xs text-slate-600">{item.desc}</p>
                <p className="mt-3 text-xs font-semibold text-blue-700">
                  {item.suggestion}
                </p>
              </article>
            ))}
          </div>
          <button className="mt-6 w-full rounded-lg bg-blue-600 px-4 py-3 text-sm font-semibold text-white">
            수정 모드로 전환
          </button>
        </section>
      </div>
    </div>
  );
}
