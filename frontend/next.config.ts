import createNextIntlPlugin from 'next-intl/plugin'
import type { NextConfig } from 'next'
import { copyFileSync, existsSync, mkdirSync } from 'node:fs'
import { resolve } from 'node:path'

// The original fonts already live in the repository. Publish them locally before
// dev/build, without downloads or relying on fonts installed on a visitor's OS.
// Docker places the same source directory at /fonts, beside /app.
const fontOutput = resolve(__dirname, 'public/fonts')
const bundledFonts = [
  ['Cairo/Cairo-VariableFont_slnt,wght.ttf', 'Juba-Cairo.ttf'],
  ['Nunito/Nunito-VariableFont_wght.ttf', 'Juba-Nunito.ttf'],
  ['Cairo/OFL.txt', 'Cairo-OFL.txt'],
  ['Nunito/OFL.txt', 'Nunito-OFL.txt'],
]
mkdirSync(fontOutput, { recursive: true })
for (const [source, filename] of bundledFonts) {
  const input = resolve(__dirname, '../fonts', source)
  const output = resolve(fontOutput, filename)
  if (existsSync(input)) copyFileSync(input, output)
  else if (!existsSync(output)) throw new Error(`Missing bundled JUBA font asset: ${source}. Include the repository fonts directory before building.`)
}

const withNextIntl = createNextIntlPlugin('./src/i18n/request.ts')
const withBackend = (path: string) => `${process.env.BACKEND_URL || 'http://localhost:8000'}${path}`
const isDesktopBuild = process.env.BUILD_TARGET === 'desktop'

const nextConfig: NextConfig = {
  poweredByHeader: false,
  output: 'standalone',
  turbopack: { root: __dirname },
  images: {
    unoptimized: true,
    remotePatterns: [
      { protocol: 'http', hostname: 'localhost' },
      { protocol: 'http', hostname: 'backend' },
      { protocol: 'https', hostname: 'raw.githubusercontent.com' },
    ],
  },
  webpack(config, { isServer }) {
    if (isServer) {
      const externals = Array.isArray(config.externals) ? config.externals : []
      config.externals = [...externals, '@ricky0123/vad-react', '@ricky0123/vad-web', 'onnxruntime-web']
    }
    return config
  },
  async headers() {
    const headers: Array<{ key: string; value: string }> = [
      ...(isDesktopBuild ? [] : [{ key: 'Strict-Transport-Security', value: 'max-age=31536000; includeSubDomains' }]),
      { key: 'X-Content-Type-Options', value: 'nosniff' },
      { key: 'X-Frame-Options', value: 'DENY' },
      { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
      { key: 'Permissions-Policy', value: 'camera=(), microphone=(self), geolocation=()' },
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
          isDesktopBuild ? "connect-src 'self' http://127.0.0.1:* http://localhost:* ws: wss:" : "connect-src 'self' ws: wss:",
          isDesktopBuild ? "img-src 'self' http://127.0.0.1:* http://localhost:* data: blob:" : "img-src 'self' https://raw.githubusercontent.com data: blob:",
          isDesktopBuild ? "media-src 'self' http://127.0.0.1:* http://localhost:* blob:" : "media-src 'self' blob:",
          "worker-src 'self' blob:",
          "font-src 'self'",
          "object-src 'none'",
          "base-uri 'self'",
        ].join('; '),
      })
    }
    return [{ source: '/(.*)', headers }]
  },
  async rewrites() {
    return [
      { source: '/api/health', destination: withBackend('/health') },
      { source: '/api/:path*', destination: withBackend('/api/:path*') },
    ]
  },
}

export default withNextIntl(nextConfig)
