"use client";

import { useEffect, useMemo, useState } from "react";
import { useParams, useRouter } from "next/navigation";

type AnalysisData = {
  analysis_id: string;
  overall_score: number;
  signal: "green" | "yellow" | "red";
  fit_items: string[];
  gap_items: string[];
  summary?: string;
  confidence?: string;
};

const signalLabels = {
  green: "적합 (Good)",
  yellow: "보류 (Hold)",
  red: "부적합 (Risk)",
};

const signalStyles = {
  green: "border-emerald-200 text-emerald-600 bg-emerald-50/40",
  yellow: "border-amber-200 text-amber-600 bg-amber-50/40",
  red: "border-rose-200 text-rose-600 bg-rose-50/40",
};

export default function AnalysisPage() {
  const router = useRouter();
  const params = useParams<{ id: string }>();
  const apiBase = useMemo(
    () => process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000",
    []
  );
  const [data, setData] = useState<AnalysisData | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    const accessToken = localStorage.getItem("accessToken");
    if (!accessToken) {
      router.replace("/login");
      return;
    }
    const fetchData = async () => {
      try {
        const res = await fetch(`${apiBase}/api/v1/analyze/session/${params.id}`, {
          headers: { Authorization: `Bearer ${accessToken}` },
          credentials: "include",
        });
        const json = await res.json().catch(() => null);
        if (!res.ok) {
          throw new Error(json?.error?.message || "분석 결과 조회 실패");
        }
        setData(json?.data || null);
      } catch (err) {
        setError(err instanceof Error ? err.message : "분석 결과 조회 실패");
      }
    };
    fetchData();
  }, [apiBase, params.id, router]);

  if (error) {
    return (
      <div className="min-h-screen px-6 pb-16 pt-24">
        <div className="mx-auto w-full max-w-[900px] text-red-600">
          {error}
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="min-h-screen px-6 pb-16 pt-24">
        <div className="mx-auto w-full max-w-[900px] text-slate-600">
          분석 결과를 불러오는 중...
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen px-6 pb-16 pt-24">
      <div className="mx-auto flex w-full max-w-[1200px] flex-col gap-6">
        <header className="grid gap-6 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm md:grid-cols-[1fr_1.2fr_0.8fr]">
          <div className="flex items-center gap-6">
            <div
              className={`relative flex h-24 w-24 items-center justify-center rounded-full border-[10px] text-2xl font-bold ${signalStyles[data.signal]}`}
            >
              {data.overall_score}
            </div>
            <div>
              <p className="text-xs font-semibold text-slate-500">Total Score</p>
              <p className="text-lg font-bold text-slate-900">
                {signalLabels[data.signal]}
              </p>
            </div>
          </div>
          <div className="flex flex-col justify-center gap-2">
            <p className="text-xs font-semibold text-slate-500">One-line</p>
            <p className="text-sm font-semibold text-slate-800">
              {data.summary || "공고와 서류를 비교한 결과입니다."}
            </p>
          </div>
          <div className="flex flex-wrap items-center gap-3">
            <button className="rounded-lg border border-slate-200 bg-white px-4 py-2 text-xs font-semibold text-slate-700">
              서류 수정하기
            </button>
            <button
              onClick={() => router.push("/postings")}
              className="rounded-lg border border-slate-300 bg-slate-900 px-4 py-2 text-xs font-semibold text-white"
            >
              다른 공고 분석
            </button>
          </div>
        </header>

        <section className="grid gap-6 lg:grid-cols-2">
          <div className="rounded-2xl border border-emerald-100 bg-emerald-50/40 p-6">
            <h2 className="text-sm font-semibold text-emerald-700">
              매칭 포인트 ({data.fit_items.length})
            </h2>
            <div className="mt-4 space-y-3 text-sm text-slate-700">
              {data.fit_items.length ? (
                data.fit_items.map((item) => (
                  <div
                    key={item}
                    className="rounded-xl border border-emerald-100 bg-white p-4 text-xs text-slate-600 shadow-sm"
                  >
                    <p className="text-sm font-semibold text-slate-800">{item}</p>
                  </div>
                ))
              ) : (
                <p className="text-sm text-slate-500">매칭 포인트가 없습니다.</p>
              )}
            </div>
          </div>

          <div className="rounded-2xl border border-rose-100 bg-rose-50/40 p-6">
            <h2 className="text-sm font-semibold text-rose-600">
              보완 필요 ({data.gap_items.length})
            </h2>
            <div className="mt-4 space-y-3 text-sm text-slate-700">
              {data.gap_items.length ? (
                data.gap_items.map((item) => (
                  <div
                    key={item}
                    className="rounded-xl border border-rose-200 bg-white p-4 text-xs text-slate-600 shadow-sm"
                  >
                    <p className="text-sm font-semibold text-slate-800">{item}</p>
                  </div>
                ))
              ) : (
                <p className="text-sm text-slate-500">보완 항목이 없습니다.</p>
              )}
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}
