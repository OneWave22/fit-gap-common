import type { NextConfig } from "next";

const backendBase = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

const nextConfig: NextConfig = {
  reactCompiler: true,
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: `${backendBase}/api/:path*`,
      },
      {
        source: "/auth/:path*",
        destination: `${backendBase}/auth/:path*`,
      },
    ];
  },
};

export default nextConfig;
