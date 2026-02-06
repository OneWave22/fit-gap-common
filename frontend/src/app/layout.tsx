import type { Metadata } from "next";
import "./globals.css";
import AppHeader from "./_components/AppHeader";

export const metadata: Metadata = {
  title: "Fit-Gap — AI 채용 분석 플랫폼",
  description:
    "공고(JD)와 서류 사이의 Fit-Gap을 분석하여 구직자와 기업에 근거 기반 피드백을 제공하는 플랫폼.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko">
      <body className="antialiased">
        <AppHeader />
        {children}
      </body>
    </html>
  );
}
