export default function ResumesPage() {
  return (
    <div className="min-h-screen px-6 pb-16 pt-24">
      <div className="mx-auto flex w-full max-w-[1200px] flex-col gap-6">
        <header className="flex items-center justify-between">
          <div>
            <p className="text-xs font-semibold text-blue-600">Step 1</p>
            <h1 className="text-2xl font-bold text-slate-900">
              서류 업로드 및 파싱
            </h1>
          </div>
          <button className="rounded-lg border border-slate-200 bg-white px-4 py-2 text-xs font-semibold text-slate-600">
            도움말 보기
          </button>
        </header>

        <div className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
          <section className="rounded-2xl border border-dashed border-blue-200 bg-white p-8 shadow-sm">
            <div className="flex h-full flex-col items-center justify-center gap-4 text-center">
              <div className="flex h-14 w-14 items-center justify-center rounded-full bg-blue-50 text-xl">
                ☁️
              </div>
              <div>
                <p className="text-sm font-semibold text-slate-800">
                  PDF 파일을 이곳에 드래그하세요
                </p>
                <p className="mt-1 text-xs text-slate-500">
                  텍스트 복사 가능한 PDF만 지원 (Max 10MB)
                </p>
              </div>
              <button className="rounded-lg border border-slate-300 bg-white px-4 py-2 text-xs font-semibold text-slate-700 shadow-sm hover:bg-slate-50">
                파일 선택하기
              </button>
            </div>
          </section>

          <section className="rounded-2xl border border-slate-200 bg-slate-50 p-6">
            <div className="flex items-center justify-between">
              <h2 className="text-sm font-semibold text-slate-800">
                추출된 데이터 확인
              </h2>
              <select className="rounded-md border border-slate-200 bg-white px-3 py-1 text-xs text-slate-600">
                <option>백엔드 개발</option>
                <option>프론트엔드 개발</option>
              </select>
            </div>

            <div className="mt-6 grid gap-4">
              <div>
                <p className="text-xs font-semibold text-slate-500">
                  기술 스택
                </p>
                <div className="mt-3 flex flex-wrap gap-2">
                  {["Java", "Spring", "PostgreSQL", "AWS", "Docker"].map(
                    (tag) => (
                      <span
                        key={tag}
                        className="flex items-center gap-1 rounded-md bg-white px-3 py-1 text-xs font-medium text-slate-700 shadow-sm"
                      >
                        {tag}
                        <span className="text-slate-400">×</span>
                      </span>
                    )
                  )}
                </div>
              </div>

              <div>
                <p className="text-xs font-semibold text-slate-500">
                  주요 경험
                </p>
                <div className="mt-3 space-y-2">
                  {[
                    "대용량 트래픽 대응을 위한 캐시 전략 수립",
                    "MSA 전환 프로젝트에서 API 설계 주도",
                  ].map((item) => (
                    <div
                      key={item}
                      className="flex items-start justify-between rounded-lg border border-slate-200 bg-white px-4 py-3 text-xs text-slate-700"
                    >
                      <span>{item}</span>
                      <button className="text-slate-400">✎</button>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </section>
        </div>

        <div className="sticky bottom-6 flex justify-end">
          <button className="rounded-lg bg-blue-600 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-blue-200">
            저장하고 공고 입력하기
          </button>
        </div>
      </div>
    </div>
  );
}
