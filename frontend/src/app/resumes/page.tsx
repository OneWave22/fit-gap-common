"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";

type Resume = {
  id: string;
  created_at?: string;
};

export default function ResumesPage() {
  const router = useRouter();
  const apiBase = useMemo(
    () => process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000",
    []
  );
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
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
        if (parsed?.role && parsed.role !== "JOBSEEKER") {
          setError("구직자 계정만 이력서를 업로드할 수 있습니다.");
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
          throw new Error(json?.error?.message || "이력서 조회 실패");
        }
        setResumes(json?.data?.resumes || []);
      } catch (err) {
        setError(err instanceof Error ? err.message : "이력서 조회 실패");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [apiBase, router]);

  const handleUpload = async () => {
    const accessToken = localStorage.getItem("accessToken");
    if (!accessToken) {
      router.replace("/login");
      return;
    }
    if (!file) {
      setError("PDF 파일을 선택해 주세요.");
      return;
    }
    setUploading(true);
    setError("");
    try {
      const formData = new FormData();
      formData.append("file", file);
      const res = await fetch(`${apiBase}/resumes`, {
        method: "POST",
        headers: { Authorization: `Bearer ${accessToken}` },
        credentials: "include",
        body: formData,
      });
      const json = await res.json().catch(() => null);
      if (!res.ok) {
        throw new Error(json?.error?.message || "이력서 업로드 실패");
      }
      const resumeId = json?.data?.resume_id;
      setResumes([{ id: resumeId }, ...resumes]);
      if (json?.data?.resume_id) {
        sessionStorage.setItem("resumeId", json.data.resume_id);
      }
      setFile(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "이력서 업로드 실패");
    } finally {
      setUploading(false);
    }
  };

  const isLimitReached = resumes.length >= 1;

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
        </header>

        {error ? (
          <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
            {error}
          </div>
        ) : null}

        <div className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
          <section className="rounded-2xl border border-dashed border-blue-200 bg-white p-8 shadow-sm">
            <div className="flex h-full flex-col items-center justify-center gap-4 text-center">
              <div className="flex h-14 w-14 items-center justify-center rounded-full bg-blue-50 text-xl">
                ☁️
              </div>
              <div>
                <p className="text-sm font-semibold text-slate-800">
                  PDF 파일을 업로드하세요
                </p>
                <p className="mt-1 text-xs text-slate-500">
                  텍스트 복사 가능한 PDF만 지원 (Max 10MB)
                </p>
              </div>
              <input
                type="file"
                accept="application/pdf"
                onChange={(e) => setFile(e.target.files?.[0] || null)}
                className="text-xs text-slate-600"
              />
              <button
                onClick={handleUpload}
                disabled={uploading || isLimitReached}
                className="rounded-lg border border-slate-300 bg-white px-4 py-2 text-xs font-semibold text-slate-700 shadow-sm hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-60"
              >
                {isLimitReached ? "이력서는 1개만 가능합니다" : "업로드"}
              </button>
            </div>
          </section>

          <section className="rounded-2xl border border-slate-200 bg-slate-50 p-6">
            <div className="flex items-center justify-between">
              <h2 className="text-sm font-semibold text-slate-800">
                내 이력서
              </h2>
            </div>
            <div className="mt-4 space-y-2 text-sm text-slate-700">
              {loading ? (
                <p className="text-sm text-slate-500">로딩 중...</p>
              ) : resumes.length ? (
                resumes.map((resume) => (
                  <div
                    key={resume.id}
                    className="flex items-center justify-between rounded-lg border border-slate-200 bg-white px-4 py-3 text-xs text-slate-700"
                  >
                    <span>이력서 ID: {resume.id}</span>
                    <span className="text-slate-400">{resume.created_at}</span>
                  </div>
                ))
              ) : (
                <p className="text-sm text-slate-500">등록된 이력서가 없습니다.</p>
              )}
            </div>
          </section>
        </div>

        <div className="sticky bottom-6 flex justify-end">
          <button
            onClick={async () => {
              const accessToken = localStorage.getItem("accessToken");
              const resumeId =
                sessionStorage.getItem("resumeId") || resumes[0]?.id;
              if (!accessToken) {
                router.replace("/login");
                return;
              }
              if (!resumeId) {
                setError("이력서를 먼저 저장해 주세요.");
                return;
              }
              setAnalyzing(true);
              setError("");
              try {
                const res = await fetch(`${apiBase}/api/v1/analyze/session`, {
                  method: "POST",
                  headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${accessToken}`,
                  },
                  credentials: "include",
                  body: JSON.stringify({
                    resume_id: resumeId,
                  }),
                });
                const json = await res.json().catch(() => null);
                if (!res.ok) {
                  throw new Error(json?.error?.message || "분석 실패");
                }
                const analysisId = json?.data?.analysis_id;
                if (analysisId) {
                  router.push(`/analysis/${analysisId}`);
                }
              } catch (err) {
                setError(err instanceof Error ? err.message : "분석 실패");
              } finally {
                setAnalyzing(false);
              }
            }}
            className="rounded-lg bg-blue-600 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-blue-200 disabled:cursor-not-allowed disabled:opacity-60"
            disabled={analyzing || resumes.length === 0}
          >
            {analyzing ? "분석 중..." : "저장하고 분석하기"}
          </button>
        </div>
      </div>
    </div>
  );
}
