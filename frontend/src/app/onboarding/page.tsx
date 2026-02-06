"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";

type Role = "JOBSEEKER" | "COMPANY";

export const dynamic = "force-dynamic";

export default function OnboardingPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [role, setRole] = useState<Role>("JOBSEEKER");
  const [jobseekerType, setJobseekerType] = useState("NEW_GRAD");
  const [nickname, setNickname] = useState("");
  const [companyName, setCompanyName] = useState("");
  const [bizRegNo, setBizRegNo] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const apiBase = useMemo(
    () => process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000",
    []
  );
  const authToken = searchParams.get("authToken") || "";

  useEffect(() => {
    if (authToken) {
      sessionStorage.setItem("authToken", authToken);
      sessionStorage.setItem("signupToken", authToken);
      router.replace("/onboarding");
    }
  }, [authToken, router]);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setError("");
    setLoading(true);

    const payload =
      role === "JOBSEEKER"
        ? { role, jobseekerType, nickname }
        : { role, companyName, bizRegNo };

    try {
      const currentAuthToken = sessionStorage.getItem("authToken") || "";
      if (!currentAuthToken) {
        throw new Error("authToken이 없습니다. 다시 로그인 해주세요.");
      }

      const res = await fetch(`${apiBase}/api/onboarding/complete`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${currentAuthToken}`,
        },
        credentials: "include",
        body: JSON.stringify(payload),
      });

      const data = await res.json().catch(() => null);
      if (!res.ok) {
        const message = data?.error?.message || data?.detail || "온보딩 실패";
        throw new Error(message);
      }

      const accessToken = data?.data?.access_token;
      if (accessToken) {
        localStorage.setItem("accessToken", accessToken);
      }
      const userId = data?.data?.user_id;
      const userRole = data?.data?.role;
      const nicknameValue = data?.data?.nickname;
      if (userId || userRole || nicknameValue) {
        localStorage.setItem(
          "user",
          JSON.stringify({ id: userId, role: userRole, nickname: nicknameValue })
        );
      }

      router.push("/");
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "온보딩 실패");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 px-6 py-12 text-slate-100">
      <div className="mx-auto w-full max-w-2xl">
        <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-8 shadow-2xl">
          <p className="text-xs font-semibold uppercase tracking-[0.3em] text-blue-400">
            Fit-Gap Onboarding
          </p>
          <h1 className="mt-3 text-3xl font-semibold text-white">
            역할을 선택해 주세요
          </h1>
          <p className="mt-2 text-sm text-slate-300">
            계정 유형에 따라 필요한 정보를 입력하면 바로 시작할 수 있어요.
          </p>

          <form onSubmit={handleSubmit} className="mt-8 space-y-6">
            <div>
              <label className="text-sm font-semibold text-slate-200">역할</label>
              <div className="mt-3 flex flex-wrap gap-3">
                {(["JOBSEEKER", "COMPANY"] as Role[]).map((value) => (
                  <button
                    key={value}
                    type="button"
                    onClick={() => setRole(value)}
                    className={`rounded-xl px-4 py-2 text-sm font-semibold transition ${
                      role === value
                        ? "bg-blue-500 text-white shadow-lg shadow-blue-500/30"
                        : "bg-slate-800 text-slate-200 hover:bg-slate-700"
                    }`}
                  >
                    {value === "JOBSEEKER" ? "구직자" : "기업"}
                  </button>
                ))}
              </div>
            </div>

            {role === "JOBSEEKER" ? (
              <>
                <div>
                  <label className="text-sm font-semibold text-slate-200">
                    구직자 유형
                  </label>
                  <select
                    value={jobseekerType}
                    onChange={(e) => setJobseekerType(e.target.value)}
                    className="mt-3 w-full rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 text-sm text-slate-100 focus:border-blue-400 focus:outline-none"
                  >
                    <option value="NEW_GRAD">신입</option>
                    <option value="EXPERIENCED">경력</option>
                    <option value="FREELANCER">프리랜서</option>
                  </select>
                </div>
                <div>
                  <label className="text-sm font-semibold text-slate-200">
                    닉네임
                  </label>
                  <input
                    value={nickname}
                    onChange={(e) => setNickname(e.target.value)}
                    className="mt-3 w-full rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 text-sm text-slate-100 focus:border-blue-400 focus:outline-none"
                    placeholder="예) 원웨이브"
                  />
                </div>
              </>
            ) : (
              <div className="space-y-4">
                <div>
                  <label className="text-sm font-semibold text-slate-200">
                    회사명
                  </label>
                  <input
                    value={companyName}
                    onChange={(e) => setCompanyName(e.target.value)}
                    className="mt-3 w-full rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 text-sm text-slate-100 focus:border-blue-400 focus:outline-none"
                    placeholder="예) 원웨이브"
                  />
                </div>
                <div>
                  <label className="text-sm font-semibold text-slate-200">
                    사업자 등록번호
                  </label>
                  <input
                    value={bizRegNo}
                    onChange={(e) => setBizRegNo(e.target.value)}
                    className="mt-3 w-full rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 text-sm text-slate-100 focus:border-blue-400 focus:outline-none"
                    placeholder="예) 123-45-67890"
                  />
                </div>
              </div>
            )}

            {error ? (
              <div className="rounded-xl border border-red-500/40 bg-red-500/10 px-4 py-3 text-sm text-red-200">
                {error}
              </div>
            ) : null}

            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-xl bg-blue-500 px-4 py-3 text-sm font-semibold text-white transition hover:bg-blue-400 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {loading ? "처리 중..." : "온보딩 완료"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
