import createNextIntlPlugin from 'next-intl/plugin'
import type { NextConfig } from 'next'

const withNextIntl = createNextIntlPlugin('./src/i18n/request.ts')

const nextConfig: NextConfig = {
  poweredByHeader: false,
  output: 'standalone',
  typescript: {
    tsconfigPath: 'tsconfig.build.json',
  },
  webpack(config, { isServer }) {
    if (isServer) {
      // Prevent SSR bundling of WASM-heavy packages; ConversationMode is
      // always loaded with dynamic({ ssr: false }) but this guards against
      // accidental server-side imports.
      const externals = Array.isArray(config.externals) ? config.externals : []
      config.externals = [
        ...externals,
        '@ricky0123/vad-react',
        '@ricky0123/vad-web',
        'onnxruntime-web',
      ]
    }
    return config
  },
  async headers() {
    const headers: Array<{ key: string; value: string }> = [
      { key: 'Strict-Transport-Security', value: 'max-age=31536000; includeSubDomains' },
      { key: 'X-Content-Type-Options', value: 'nosniff' },
      { key: 'X-Frame-Options', value: 'DENY' },
      { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
      { key: 'Permissions-Policy', value: 'camera=(), microphone=(self), geolocation=()' },
      // Required for SharedArrayBuffer (onnxruntime-web threaded WASM).
      // credentialless COEP is more permissive than require-corp and works
      // with client-side navigation in Next.js (headers must be global).
      { key: 'Cross-Origin-Opener-Policy', value: 'same-origin' },
      { key: 'Cross-Origin-Embedder-Policy', value: 'credentialless' },
    ]

    if (process.env.NODE_ENV === 'production') {
      headers.push({
        key: 'Content-Security-Policy',
        value: [
          "default-src 'self'",
          "script-src 'self' 'unsafe-inline' 'wasm-unsafe-eval'",
          "style-src 'self' 'unsafe-inline'",
          "connect-src 'self' ws: wss:",
          "img-src 'self' data: blob:",
          "media-src 'self' blob:",
          "worker-src 'self' blob:",
          "font-src 'self'",
          "object-src 'none'",
          "base-uri 'self'",
        ].join('; '),
      })
    }

    return [
      {
        source: '/(.*)',
        headers,
      },
    ]
  },
  async rewrites() {
    return {
      fallback: [
        {
          source: '/api/:path*',
          destination: `${process.env.BACKEND_URL || 'http://backend:8000'}/api/:path*`,
        },
      ],
    }
  },
}

export default withNextIntl(nextConfig)
