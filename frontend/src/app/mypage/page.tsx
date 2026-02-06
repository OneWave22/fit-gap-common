"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";

type UserInfo = {
  id: string;
  email?: string;
  nickname?: string;
  role?: "JOBSEEKER" | "COMPANY";
  status?: string;
};

type Profile = Record<string, unknown> | null;

type Resume = {
  id: string;
  raw_text?: string;
  created_at?: string;
};

type Posting = {
  id: string;
  company_name?: string;
  created_at?: string;
};

type MyPageData = {
  user: UserInfo;
  profile: Profile;
  resumes: Resume[];
  postings: Posting[];
};

export default function MyPage() {
  const router = useRouter();
  const apiBase = useMemo(() => "", []);
  const [data, setData] = useState<MyPageData | null>(null);
  const [nickname, setNickname] = useState("");
  const [resumeText, setResumeText] = useState("");
  const [resumeId, setResumeId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const accessToken = localStorage.getItem("accessToken");
    if (!accessToken) {
      router.replace("/login");
      return;
    }

    const fetchData = async () => {
      try {
        const res = await fetch(`${apiBase}/api/mypage`, {
          headers: { Authorization: `Bearer ${accessToken}` },
          credentials: "include",
        });
        const json = await res.json().catch(() => null);
        if (!res.ok) {
          throw new Error(json?.error?.message || "마이페이지 조회 실패");
        }
        setData(json?.data || null);
        setNickname(json?.data?.user?.nickname || "");
        const resume = json?.data?.resumes?.[0];
        setResumeText(resume?.raw_text || "");
        setResumeId(resume?.id || null);
      } catch (err) {
        setError(err instanceof Error ? err.message : "마이페이지 조회 실패");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [apiBase, router]);

  const handleSaveNickname = async () => {
    const accessToken = localStorage.getItem("accessToken");
    if (!accessToken) {
      router.replace("/login");
      return;
    }
    setSaving(true);
    setError("");
    try {
      const res = await fetch(`${apiBase}/api/mypage/nickname`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
        credentials: "include",
        body: JSON.stringify({ nickname }),
      });
      const json = await res.json().catch(() => null);
      if (!res.ok) {
        throw new Error(json?.error?.message || "닉네임 수정 실패");
      }
      const updated = json?.data?.nickname || nickname;
      setData((prev) =>
        prev ? { ...prev, user: { ...prev.user, nickname: updated } } : prev
      );
      const rawUser = localStorage.getItem("user");
      if (rawUser) {
        try {
          const parsed = JSON.parse(rawUser);
          localStorage.setItem(
            "user",
            JSON.stringify({ ...parsed, nickname: updated })
          );
        } catch {
          // ignore storage parse errors
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "닉네임 수정 실패");
    } finally {
      setSaving(false);
    }
  };

  const handleSaveResume = async () => {
    const accessToken = localStorage.getItem("accessToken");
    if (!accessToken) {
      router.replace("/login");
      return;
    }
    setSaving(true);
    setError("");
    try {
      const res = await fetch(`${apiBase}/api/mypage/resume`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
        credentials: "include",
        body: JSON.stringify({ raw_text: resumeText }),
      });
      const json = await res.json().catch(() => null);
      if (!res.ok) {
        throw new Error(json?.error?.message || "자기소개서 저장 실패");
      }
      const newId = json?.data?.resume_id;
      if (newId) {
        setResumeId(newId);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "자기소개서 저장 실패");
    } finally {
      setSaving(false);
    }
  };

  const handleDeleteResume = async () => {
    const accessToken = localStorage.getItem("accessToken");
    if (!accessToken) {
      router.replace("/login");
      return;
    }
    if (!resumeId) {
      return;
    }
    if (!confirm("자기소개서를 삭제하시겠습니까?")) {
      return;
    }
    setSaving(true);
    setError("");
    try {
      const res = await fetch(`${apiBase}/api/v1/resumes/${resumeId}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${accessToken}` },
        credentials: "include",
      });
      const json = await res.json().catch(() => null);
      if (!res.ok) {
        throw new Error(json?.error?.message || "자기소개서 삭제 실패");
      }
      setResumeText("");
      setResumeId(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "자기소개서 삭제 실패");
    } finally {
      setSaving(false);
    }
  };

  const handleDeleteAccount = async () => {
    const accessToken = localStorage.getItem("accessToken");
    if (!accessToken) {
      router.replace("/login");
      return;
    }
    if (!confirm("정말로 회원 탈퇴하시겠습니까?")) {
      return;
    }
    try {
      const res = await fetch(`${apiBase}/api/mypage`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${accessToken}` },
        credentials: "include",
      });
      const json = await res.json().catch(() => null);
      if (!res.ok) {
        throw new Error(json?.error?.message || "회원 탈퇴 실패");
      }
      localStorage.removeItem("accessToken");
      localStorage.removeItem("user");
      sessionStorage.removeItem("authToken");
      sessionStorage.removeItem("signupToken");
      router.replace("/");
    } catch (err) {
      setError(err instanceof Error ? err.message : "회원 탈퇴 실패");
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen px-6 pb-16 pt-24">
        <div className="mx-auto w-full max-w-[900px] text-slate-600">
          로딩 중...
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen px-6 pb-16 pt-24">
      <div className="mx-auto w-full max-w-[900px] space-y-6">
        <div className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
          <h1 className="text-2xl font-bold text-slate-900">마이페이지</h1>
          <p className="mt-2 text-sm text-slate-600">
            내 정보와 관리 항목을 확인하세요.
          </p>
        </div>

        {error ? (
          <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
            {error}
          </div>
        ) : null}

        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-lg font-semibold text-slate-900">내 정보</h2>
          <div className="mt-4 grid gap-4 md:grid-cols-2">
            <div>
              <p className="text-xs font-semibold text-slate-500">이메일</p>
              <p className="mt-1 text-sm text-slate-900">{data?.user.email}</p>
            </div>
            <div>
              <p className="text-xs font-semibold text-slate-500">역할</p>
              <p className="mt-1 text-sm text-slate-900">{data?.user.role}</p>
            </div>
          </div>
          <div className="mt-5">
            <p className="text-xs font-semibold text-slate-500">닉네임</p>
            <div className="mt-2 flex flex-wrap gap-3">
              <input
                value={nickname}
                onChange={(e) => setNickname(e.target.value)}
                className="flex-1 rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-900"
              />
              <button
                onClick={handleSaveNickname}
                disabled={saving}
                className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-60"
              >
                저장
              </button>
            </div>
          </div>
        </div>

        {data?.user.role === "JOBSEEKER" ? (
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-900">
              자기소개서
            </h2>
            <p className="mt-2 text-sm text-slate-600">
              계정당 1개의 자기소개서를 작성할 수 있습니다.
            </p>
            <textarea
              value={resumeText}
              onChange={(e) => setResumeText(e.target.value)}
              className="mt-4 min-h-[220px] w-full rounded-lg border border-slate-200 px-4 py-3 text-sm text-slate-700"
              placeholder="자기소개서를 작성해 주세요..."
            />
            <div className="mt-4 flex flex-wrap gap-3">
              <button
                onClick={handleSaveResume}
                disabled={saving}
                className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-60"
              >
                저장
              </button>
              {resumeId ? (
                <button
                  onClick={handleDeleteResume}
                  disabled={saving}
                  className="rounded-lg border border-rose-200 bg-rose-50 px-4 py-2 text-sm font-semibold text-rose-700"
                >
                  삭제
                </button>
              ) : null}
            </div>
          </div>
        ) : (
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-900">공고 관리</h2>
            <div className="mt-4 space-y-2 text-sm text-slate-700">
              {data?.postings?.length ? (
                data.postings.map((posting) => (
                  <div
                    key={posting.id}
                    className="flex items-center justify-between rounded-lg border border-slate-100 px-3 py-2"
                  >
                    <span>
                      {posting.company_name || "회사명"} / 공고 ID: {posting.id}
                    </span>
                    <span className="text-xs text-slate-500">
                      {posting.created_at}
                    </span>
                  </div>
                ))
              ) : (
                <p className="text-sm text-slate-500">등록된 공고가 없습니다.</p>
              )}
            </div>
          </div>
        )}

        <div className="rounded-2xl border border-rose-200 bg-rose-50 p-6">
          <h2 className="text-lg font-semibold text-rose-700">회원 탈퇴</h2>
          <p className="mt-2 text-sm text-rose-600">
            탈퇴 시 모든 데이터가 삭제됩니다.
          </p>
          <button
            onClick={handleDeleteAccount}
            className="mt-4 rounded-lg bg-rose-600 px-4 py-2 text-sm font-semibold text-white"
          >
            회원 탈퇴
          </button>
        </div>
      </div>
    </div>
  );
}
