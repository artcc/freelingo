import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { SUPPORTED_LOCALES, type Locale } from '@/lib/locales'

// Routes that require authentication — anything else passes through so unknown
// URLs reach Next.js's 404 handler instead of being redirected to /login.
const PROTECTED_ROUTES = [
  '/admin',
  '/assessment',
  '/billing',
  '/chat',
  '/conversation',
  '/dashboard',
  '/faq',
  '/feedback',
  '/flashcards',
  '/grammar',
  '/lesson',
  '/listening',
  '/onboarding',
  '/phrasebook',
  '/plan',
  '/progress',
  '/settings',
  '/vocabulary',
]

function detectLocale(req: NextRequest): Locale {
  // 1. Cookie already set — respect user choice
  const cookie = req.cookies.get('NEXT_LOCALE')?.value
  if (cookie && (SUPPORTED_LOCALES as readonly string[]).includes(cookie)) {
    return cookie as Locale
  }

  // 2. Parse Accept-Language header with q-weight sorting
  const accept = req.headers.get('accept-language') ?? ''
  const parsed = accept
    .split(',')
    .map((part) => {
      const [langTag, ...params] = part.trim().split(';')
      const qParam = params.find((p) => p.trim().startsWith('q='))
      const q = qParam ? parseFloat(qParam.split('=')[1]) : 1.0
      const lang = langTag.trim().split(/[-_]/)[0].toLowerCase()
      return { lang, q: isNaN(q) ? 0 : q }
    })
    .filter(({ q }) => q > 0 && q <= 1)
    .sort((a, b) => b.q - a.q)

  for (const { lang } of parsed) {
    if ((SUPPORTED_LOCALES as readonly string[]).includes(lang)) {
      return lang as Locale
    }
  }

  // 3. Default to English
  return 'en'
}

export function middleware(req: NextRequest) {
  // Detect locale first so we can forward it as a request header.
  // This is needed because request.ts reads incoming request headers/cookies;
  // a cookie set only on the response is not visible on that same request cycle.
  const locale = detectLocale(req)

  const hasRefreshToken = req.cookies.has('refresh_token')
  const isProtected = PROTECTED_ROUTES.some((r) =>
    req.nextUrl.pathname.startsWith(r)
  )

  if (!hasRefreshToken && isProtected) {
    const response = NextResponse.redirect(new URL('/login', req.url))
    if (!req.cookies.has('NEXT_LOCALE')) {
      response.cookies.set('NEXT_LOCALE', locale, {
        path: '/',
        sameSite: 'lax',
        secure: process.env.NODE_ENV === 'production',
        maxAge: 60 * 60 * 24 * 365,
      })
    }
    return response
  }

  // Inject locale as a request header so request.ts picks it up immediately
  // (even on the very first visit when no NEXT_LOCALE cookie exists yet)
  const requestHeaders = new Headers(req.headers)
  requestHeaders.set('x-next-locale', locale)

  const response = NextResponse.next({ request: { headers: requestHeaders } })

  // Persist as cookie for subsequent requests
  if (!req.cookies.has('NEXT_LOCALE')) {
    response.cookies.set('NEXT_LOCALE', locale, {
      path: '/',
      sameSite: 'lax',
      secure: process.env.NODE_ENV === 'production',
      maxAge: 60 * 60 * 24 * 365,
    })
  }

  return response
}

export const config = {
  matcher: [
    '/((?!_next|favicon\.ico|api|.*\.(?:svg|png|jpg|jpeg|gif|webp|ico)$).*)',
  ],
}
