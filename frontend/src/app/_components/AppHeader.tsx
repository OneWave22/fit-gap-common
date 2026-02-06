"use client";

import { useEffect, useState } from "react";

type UserInfo = {
  id?: string;
  role?: string;
  nickname?: string;
};

export default function AppHeader() {
  const [user, setUser] = useState<UserInfo | null>(null);

  useEffect(() => {
    const accessToken = localStorage.getItem("accessToken");
    if (!accessToken) {
      setUser(null);
      return;
    }
    const raw = localStorage.getItem("user");
    if (raw) {
      try {
        setUser(JSON.parse(raw));
      } catch {
        setUser(null);
      }
    }
  }, []);

  const handleLogout = async () => {
    try {
      await fetch("http://localhost:8000/api/auth/logout", {
        method: "POST",
        credentials: "include",
      });
    } catch {
      // ignore
    } finally {
      localStorage.removeItem("accessToken");
      localStorage.removeItem("user");
      sessionStorage.removeItem("authToken");
      sessionStorage.removeItem("signupToken");
      window.location.href = "/";
    }
  };
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
          {user?.nickname ? (
            <>
              <span className="rounded-lg border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-700 shadow-sm">
                {user.nickname}
              </span>
              <a
                className="rounded-lg border border-blue-200 bg-white px-4 py-2 text-sm font-semibold text-blue-700 shadow-sm transition hover:border-blue-300 hover:bg-blue-50"
                href="/mypage"
              >
                마이페이지
              </a>
              <button
                onClick={handleLogout}
                className="rounded-lg border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-600 shadow-sm transition hover:border-slate-300 hover:bg-slate-50"
              >
                로그아웃
              </button>
            </>
          ) : (
            <a
              className="rounded-lg border border-blue-200 bg-white px-4 py-2 text-sm font-semibold text-blue-700 shadow-sm transition hover:border-blue-300 hover:bg-blue-50"
              href="/login"
            >
              로그인/회원가입
            </a>
          )}
        </div>
      </div>
    </header>
  );
}
