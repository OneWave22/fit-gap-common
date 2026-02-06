export default function LoginPage() {
  return (
    <div className="min-h-screen px-6 pb-16 pt-24">
      <div className="mx-auto flex w-full max-w-[960px] flex-col items-center gap-10">
        <div className="text-center">
          <p className="text-xs font-semibold text-blue-600">Fit-Gap</p>
          <h1 className="mt-2 text-3xl font-bold text-slate-900">
            로그인
          </h1>
          <p className="mt-3 text-sm text-slate-600">
            OAuth 2.0 기반 Google 로그인만 지원합니다.
          </p>
        </div>

        <div className="w-full max-w-md rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
          <button className="flex w-full items-center justify-center gap-3 rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm font-semibold text-slate-700 shadow-sm transition hover:bg-slate-50">
            <span className="inline-flex h-8 w-8 items-center justify-center rounded-full bg-red-50 text-lg">
              G
            </span>
            Google로 로그인
          </button>
          <div className="mt-6 rounded-lg border border-dashed border-slate-200 bg-slate-50 px-4 py-3 text-xs text-slate-500">
            아직 OAuth 연결이 없어서 실제 로그인은 동작하지 않습니다.
          </div>
        </div>
      </div>
    </div>
  );
}
