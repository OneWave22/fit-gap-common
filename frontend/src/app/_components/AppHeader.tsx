export default function AppHeader() {
  return (
    <header className="fixed left-0 right-0 top-0 z-20 border-b border-slate-200/60 bg-white/80 shadow-sm backdrop-blur-md">
      <div className="mx-auto flex w-full max-w-[1200px] items-center justify-between px-6 py-4">
        <a className="text-lg font-extrabold text-blue-700" href="/">
          Fit-Gap
        </a>
        <nav className="hidden items-center gap-6 text-sm font-semibold text-slate-700 md:flex">
          <a className="transition hover:text-slate-900" href="/#features">
            기능 소개
          </a>
          <a className="transition hover:text-slate-900" href="/#pricing">
            요금제
          </a>
          <a className="transition hover:text-slate-900" href="/#contact">
            문의하기
          </a>
        </nav>
        <div className="flex items-center gap-3">
          <a
            className="rounded-lg border border-blue-200 bg-white px-4 py-2 text-sm font-semibold text-blue-700 shadow-sm transition hover:border-blue-300 hover:bg-blue-50"
            href="/login"
          >
            로그인/회원가입
          </a>
        </div>
      </div>
    </header>
  );
}
