const nextConfig = {
  poweredByHeader: false,
  async rewrites() {
    return [{ source: '/api/v1/:path*', destination: `${process.env.INTERNAL_API_BASE_URL || 'http://127.0.0.1:8000'}/api/v1/:path*` }];
  },
};
export default nextConfig;
