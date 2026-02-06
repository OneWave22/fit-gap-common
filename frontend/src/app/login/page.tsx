export default function LoginPage() {
  return (
    <div className="min-h-screen px-6 pb-16 pt-24">
      <div className="mx-auto flex w-full max-w-[960px] flex-col items-center gap-10">
        <div className="text-center">
          <p className="text-xs font-semibold text-blue-600">Fit-Gap</p>
          <h1 className="mt-2 text-3xl font-bold text-slate-900">
            로그인 / 회원가입
          </h1>
        </div>

        <div className="w-full max-w-md rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
          <button className="flex w-full items-center justify-center gap-3 rounded-xl bg-white px-4 py-3 text-sm font-semibold text-slate-700 shadow-sm ring-1 ring-slate-200 transition hover:bg-slate-50">
            <svg
              aria-hidden
              className="h-5 w-5"
              viewBox="0 0 48 48"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                fill="#EA4335"
                d="M24 9.5c3.54 0 6.72 1.22 9.22 3.22l6.9-6.9C35.74 2.36 30.2 0 24 0 14.62 0 6.51 5.38 2.56 13.22l8.05 6.26C12.45 13.07 17.77 9.5 24 9.5z"
              />
              <path
                fill="#4285F4"
                d="M46.98 24.55c0-1.57-.14-3.08-.4-4.55H24v9.02h12.94c-.56 3.02-2.25 5.58-4.78 7.3l7.62 5.9c4.45-4.1 7.2-10.14 7.2-17.67z"
              />
              <path
                fill="#FBBC05"
                d="M10.61 28.48a14.5 14.5 0 0 1 0-8.96l-8.05-6.26A23.94 23.94 0 0 0 0 24c0 3.87.92 7.54 2.56 10.74l8.05-6.26z"
              />
              <path
                fill="#34A853"
                d="M24 48c6.48 0 11.93-2.14 15.9-5.78l-7.62-5.9c-2.12 1.42-4.85 2.26-8.28 2.26-6.23 0-11.55-3.57-13.39-8.48l-8.05 6.26C6.51 42.62 14.62 48 24 48z"
              />
            </svg>
            Google로 로그인
          </button>
        </div>
      </div>
    </div>
  );
}
