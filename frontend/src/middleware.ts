import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { normalizeLocale, SUPPORTED_LOCALES, type Locale } from '@/lib/locales'
import { isProtectedPath, loginRedirectPath } from '@/lib/protected-routes'

// Every route under src/app/(app) requires authentication (see
// lib/protected-routes.ts); anything else passes through so unknown URLs reach
// Next.js's 404 handler instead of being redirected to /login.

function detectLocale(req: NextRequest): Locale {
  // 1. An explicit /:locale URL prefix always wins, including regional aliases
  // such as /en-GB or /ar-DZ.
  const firstSegment = req.nextUrl.pathname.split('/').filter(Boolean)[0]
  if (firstSegment) {
    const normalized = normalizeLocale(firstSegment)
    const raw = firstSegment.trim().replace(/_/g, '-').toLowerCase()
    const knownLocale = (SUPPORTED_LOCALES as readonly string[]).includes(raw)
    const regionalAlias = raw.includes('-') && (normalized !== 'en' || raw.startsWith('en-'))
    if (knownLocale || regionalAlias) return normalized
  }

  // 2. Cookie already set — respect the user's explicit choice, including
  // older regional cookie values.
  const cookie = req.cookies.get('NEXT_LOCALE')?.value
  if (cookie) {
    const normalized = normalizeLocale(cookie)
    if ((SUPPORTED_LOCALES as readonly string[]).includes(normalized)) return normalized
  }

  // 3. Use the visitor's country when the hosting/CDN exposes it.
  const country = (
    req.headers.get('x-vercel-ip-country') ??
    req.headers.get('cf-ipcountry') ??
    req.headers.get('x-country-code') ??
    ''
  ).trim().toUpperCase()

  const countryLocale: Record<string, Locale> = {
    DZ: 'ar', MA: 'fr', TN: 'fr', EG: 'ar', SA: 'ar', AE: 'ar', QA: 'ar',
    KW: 'ar', BH: 'ar', OM: 'ar', JO: 'ar', LB: 'ar', IQ: 'ar', SY: 'ar', YE: 'ar',
    FR: 'fr', BE: 'fr', LU: 'fr', CH: 'fr', ES: 'es', MX: 'es', AR: 'es', CL: 'es',
    CO: 'es', PE: 'es', DE: 'de', AT: 'de', IT: 'it', PT: 'pt', BR: 'pt',
    PL: 'pl', NL: 'nl', RO: 'ro', RU: 'ru', UA: 'ru', GB: 'en', US: 'en',
    CA: 'en', AU: 'en', NZ: 'en',
  }

  const locationLocale = countryLocale[country]
  if (locationLocale) return locationLocale

  // 4. Parse Accept-Language header with q-weight sorting.
  const accept = req.headers.get('accept-language') ?? ''
  const parsed = accept
    .split(',')
    .map((part) => {
      const [langTag, ...params] = part.trim().split(';')
      const qParam = params.find((p) => p.trim().startsWith('q='))
      const q = qParam ? parseFloat(qParam.split('=')[1]) : 1.0
      return { langTag: langTag.trim(), q: Number.isNaN(q) ? 0 : q }
    })
    .sort((a, b) => b.q - a.q)

  for (const { langTag } of parsed) {
    const normalized = normalizeLocale(langTag)
    if ((SUPPORTED_LOCALES as readonly string[]).includes(normalized)) return normalized
  }

  // 5. Default to English.
  return 'en'
}

export function middleware(req: NextRequest) {
  // Detect locale first so we can forward it as a request header.
  // This is needed because request.ts reads incoming request headers/cookies;
  // a cookie set only on the response is not visible on that same request cycle.
  const locale = detectLocale(req)
  const pathname = req.nextUrl.pathname
  const firstSegment = pathname.split('/').filter(Boolean)[0]?.toLowerCase()
  const hasLocalePrefix = Boolean(
    firstSegment && (SUPPORTED_LOCALES as readonly string[]).includes(firstSegment)
  )
  const normalizedPath = hasLocalePrefix
    ? pathname.slice(firstSegment!.length + 1) || '/'
    : pathname

  const hasRefreshToken = req.cookies.has('refresh_token')
  const isProtected = isProtectedPath(normalizedPath)

  if (!hasRefreshToken && isProtected) {
    // Keep /ar, /fr, ... on the login page so the user's language survives
    // the authentication redirect, and remember where they were going.
    const target = loginRedirectPath(
      normalizedPath,
      req.nextUrl.search,
      hasLocalePrefix ? firstSegment! : null,
    )
    const response = NextResponse.redirect(new URL(target, req.url))
    if (hasLocalePrefix || !req.cookies.has('NEXT_LOCALE')) {
      response.cookies.set('NEXT_LOCALE', locale, {
        path: '/',
        sameSite: 'lax',
        secure: process.env.NODE_ENV === 'production' && process.env.BUILD_TARGET !== 'desktop',
        maxAge: 60 * 60 * 24 * 365,
      })
    }
    return response
  }

  // Support public links such as /ar and /fr without requiring a separate
  // App Router segment for every locale. The browser URL remains unchanged.
  if (hasLocalePrefix) {
    const target = req.nextUrl.clone()
    target.pathname = normalizedPath
    const requestHeaders = new Headers(req.headers)
    requestHeaders.set('x-next-locale', locale)

    const response = NextResponse.rewrite(target, {
      request: { headers: requestHeaders },
    })

    // An explicit /:locale URL is an explicit user choice. Persist it so
    // the selection survives navigation to unprefixed application routes.
    response.cookies.set('NEXT_LOCALE', locale, {
      path: '/',
      sameSite: 'lax',
      secure:
        process.env.NODE_ENV === 'production' &&
        process.env.BUILD_TARGET !== 'desktop',
      maxAge: 60 * 60 * 24 * 365,
    })

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
      secure: process.env.NODE_ENV === 'production' && process.env.BUILD_TARGET !== 'desktop',
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
