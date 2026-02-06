"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";

type Posting = {
  id: string;
  company_name?: string;
  created_at?: string;
};

export default function PostingsPage() {
  const router = useRouter();
  const apiBase = useMemo(
    () => process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000",
    []
  );
  const [companyName, setCompanyName] = useState("");
  const [rawText, setRawText] = useState("");
  const [postings, setPostings] = useState<Posting[]>([]);
  const [signals, setSignals] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const accessToken = localStorage.getItem("accessToken");
    const rawUser = localStorage.getItem("user");
    if (!accessToken) {
      router.replace("/login");
      return;
    }
    if (rawUser) {
      try {
        const parsed = JSON.parse(rawUser);
        if (parsed?.role && parsed.role !== "COMPANY") {
          setError("기업 계정만 공고를 작성할 수 있습니다.");
          setLoading(false);
          return;
        }
      } catch {
        // ignore
      }
    }

    const fetchData = async () => {
      try {
        const res = await fetch(`${apiBase}/api/mypage`, {
          headers: { Authorization: `Bearer ${accessToken}` },
          credentials: "include",
        });
        const json = await res.json().catch(() => null);
        if (!res.ok) {
          throw new Error(json?.error?.message || "공고 조회 실패");
        }
        const nextPostings = json?.data?.postings || [];
        setPostings(nextPostings);
        if (nextPostings.length) {
          const signalEntries = await Promise.all(
            nextPostings.map(async (posting: Posting) => {
              try {
                const signalRes = await fetch(
                  `${apiBase}/api/v1/analyze/session/by-posting/${posting.id}`,
                  {
                    headers: { Authorization: `Bearer ${accessToken}` },
                    credentials: "include",
                  }
                );
                const signalJson = await signalRes.json().catch(() => null);
                const signal = signalJson?.data?.analysis?.signal || null;
                return [posting.id, signal] as const;
              } catch {
                return [posting.id, null] as const;
              }
            })
          );
          const nextSignals: Record<string, string> = {};
          for (const [id, signal] of signalEntries) {
            if (signal) {
              nextSignals[id] = signal;
            }
          }
          setSignals(nextSignals);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : "공고 조회 실패");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [apiBase, router]);

  const handleSubmit = async () => {
    const accessToken = localStorage.getItem("accessToken");
    if (!accessToken) {
      router.replace("/login");
      return;
    }
    if (!rawText.trim()) {
      setError("공고 내용을 입력해주세요.");
      return;
    }
    if (postings.length >= 3) {
      setError("공고는 최대 3개까지 작성할 수 있습니다.");
      return;
    }
    setSubmitting(true);
    setError("");
    try {
      const res = await fetch(`${apiBase}/postings`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
        credentials: "include",
        body: JSON.stringify({ company_name: companyName, raw_text: rawText }),
      });
      const json = await res.json().catch(() => null);
      if (!res.ok) {
        throw new Error(json?.error?.message || "공고 등록 실패");
      }
      const newPosting = {
        id: json?.data?.posting_id,
        company_name: json?.data?.company_name || companyName,
        created_at: json?.data?.created_at,
      };
      setPostings([newPosting, ...postings]);
      if (newPosting.id) {
        const resumeId = sessionStorage.getItem("resumeId");
        const analysisRes = await fetch(`${apiBase}/api/v1/analyze/session`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${accessToken}`,
          },
          credentials: "include",
          body: JSON.stringify({
            posting_id: newPosting.id,
            ...(resumeId ? { resume_id: resumeId } : {}),
          }),
        });
        const analysisJson = await analysisRes.json().catch(() => null);
        if (analysisRes.ok && analysisJson?.data?.analysis_id) {
          router.push(`/analysis/${analysisJson.data.analysis_id}`);
          return;
        }
        const signal = analysisJson?.data?.signal;
        if (signal) {
          setSignals((prev) => ({ ...prev, [newPosting.id]: signal }));
        }
      }
      setCompanyName("");
      setRawText("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "공고 등록 실패");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen px-6 pb-16 pt-24">
      <div className="mx-auto flex w-full max-w-[900px] flex-col gap-8">
        <div className="flex items-center gap-2 text-xs font-semibold text-slate-500">
          <span className="rounded-full bg-emerald-50 px-3 py-1 text-emerald-700">
            기업 계정
          </span>
          <span className="rounded-full bg-blue-600 px-3 py-1 text-white">
            공고 입력
          </span>
        </div>

        {error ? (
          <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
            {error}
          </div>
        ) : null}

        <div className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
          <h1 className="text-2xl font-bold text-slate-900">
            채용 공고를 입력해주세요
          </h1>
          <p className="mt-2 text-sm text-slate-600">
            공고의 자격 요건과 우대 사항을 복사해서 붙여넣으면 자동으로 핵심
            키워드를 감지합니다.
          </p>

          <div className="mt-6 grid gap-4">
            <input
              value={companyName}
              onChange={(e) => setCompanyName(e.target.value)}
              className="h-11 rounded-lg border border-slate-200 px-4 text-sm text-slate-700 placeholder:text-slate-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-100"
              placeholder="예: 토스 / 백엔드 개발자"
            />
            <textarea
              value={rawText}
              onChange={(e) => setRawText(e.target.value)}
              className="min-h-[320px] rounded-lg border border-slate-200 px-4 py-3 text-sm text-slate-700 placeholder:text-slate-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-100"
              placeholder="채용 공고의 [자격 요건]과 [우대 사항] 부분을 복사해서 붙여넣으세요..."
            />
          </div>

          <div className="mt-8">
            <button
              onClick={handleSubmit}
              disabled={submitting || postings.length >= 3}
              className="w-full rounded-xl bg-blue-600 px-6 py-4 text-sm font-semibold text-white shadow-lg shadow-blue-200 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {postings.length >= 3 ? "공고는 최대 3개입니다" : "공고 등록"}
            </button>
          </div>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-6 text-sm text-slate-700">
          <h2 className="text-lg font-semibold text-slate-900">내 공고</h2>
          <div className="mt-4 space-y-2">
            {loading ? (
              <p className="text-sm text-slate-500">로딩 중...</p>
            ) : postings.length ? (
              postings.map((posting) => (
                <div
                  key={posting.id}
                  className="flex items-center justify-between rounded-lg border border-slate-100 px-3 py-2"
                >
                  <span>
                    {posting.company_name || "회사명"} / 공고 ID: {posting.id}
                  </span>
                  <div className="flex items-center gap-3 text-xs text-slate-500">
                    {signals[posting.id] ? (
                      <span className="flex items-center gap-2 text-xs font-semibold text-slate-600">
                        <span
                          className={`h-2.5 w-2.5 rounded-full ${
                            signals[posting.id] === "green"
                              ? "bg-emerald-500"
                              : signals[posting.id] === "yellow"
                                ? "bg-amber-400"
                                : "bg-rose-500"
                          }`}
                        />
                        {signals[posting.id] === "green"
                          ? "양호"
                          : signals[posting.id] === "yellow"
                            ? "주의"
                            : "위험"}
                      </span>
                    ) : null}
                    <span>{posting.created_at}</span>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-sm text-slate-500">등록된 공고가 없습니다.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
