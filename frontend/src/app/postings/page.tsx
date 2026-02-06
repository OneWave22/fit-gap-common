export default function PostingsPage() {
  return (
    <div className="min-h-screen px-6 pb-16 pt-24">
      <div className="mx-auto flex w-full max-w-[900px] flex-col gap-8">
        <div className="flex items-center gap-2 text-xs font-semibold text-slate-500">
          <span className="rounded-full bg-emerald-50 px-3 py-1 text-emerald-700">
            서류 업로드 완료
          </span>
          <span className="rounded-full bg-blue-600 px-3 py-1 text-white">
            공고 입력
          </span>
          <span className="rounded-full bg-slate-100 px-3 py-1 text-slate-500">
            분석 결과
          </span>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
          <h1 className="text-2xl font-bold text-slate-900">
            분석하고 싶은 채용 공고를 입력해주세요
          </h1>
          <p className="mt-2 text-sm text-slate-600">
            공고의 자격 요건과 우대 사항을 복사해서 붙여넣으면 자동으로
            핵심 키워드를 감지합니다.
          </p>

          <div className="mt-6 grid gap-4">
            <input
              className="h-11 rounded-lg border border-slate-200 px-4 text-sm text-slate-700 placeholder:text-slate-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-100"
              placeholder="예: 토스 / 백엔드 개발자"
            />
            <textarea
              className="min-h-[320px] rounded-lg border border-slate-200 px-4 py-3 text-sm text-slate-700 placeholder:text-slate-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-100"
              placeholder="채용 공고의 [자격 요건]과 [우대 사항] 부분을 복사해서 붙여넣으세요..."
            />
          </div>

          <div className="mt-5 flex flex-wrap gap-2">
            {["Java", "Spring", "MSA", "AWS", "Docker"].map((item) => (
              <span
                key={item}
                className="rounded-md bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-600"
              >
                {item}
              </span>
            ))}
          </div>

          <div className="mt-8">
            <button className="w-full rounded-xl bg-blue-600 px-6 py-4 text-sm font-semibold text-white shadow-lg shadow-blue-200">
              분석 시작하기
            </button>
          </div>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white/70 p-6 text-xs text-slate-500">
          분석 중에는 화면이 흐려지고 "공고의 핵심 요구사항을 추출하고 있습니다..."
          등의 문구가 순환 표시됩니다.
        </div>
      </div>
    </div>
  );
}
