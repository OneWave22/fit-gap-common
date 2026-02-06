"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function LoginCallbackPage() {
  const router = useRouter();
  useEffect(() => {
    let isMounted = true;

    const syncSession = async () => {
      try {
        if (window.location.hash.startsWith("#")) {
          const params = new URLSearchParams(window.location.hash.slice(1));
          const idToken = params.get("idToken");
          if (idToken) {
            sessionStorage.setItem("idToken", idToken);
          }
        }
        const res = await fetch("http://localhost:8000/api/auth/session", {
          method: "POST",
          credentials: "include",
        });
        const data = await res.json().catch(() => null);
        if (!res.ok) {
          throw new Error(data?.error?.message || "세션 동기화 실패");
        }
        const accessToken = data?.data?.access_token;
        if (accessToken) {
          localStorage.setItem("accessToken", accessToken);
        }
        const userId = data?.data?.user_id;
        const role = data?.data?.role;
        const nickname = data?.data?.nickname;
        if (userId || role || nickname) {
          localStorage.setItem(
            "user",
            JSON.stringify({ id: userId, role, nickname })
          );
        }
        if (isMounted) {
          router.replace("/");
        }
      } catch {
        if (isMounted) {
          router.replace("/login");
        }
      }
    };

    syncSession();

    return () => {
      isMounted = false;
    };
  }, [router]);

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-950 text-slate-100">
      <div className="text-sm text-slate-300">로그인 처리 중...</div>
    </div>
  );
}
