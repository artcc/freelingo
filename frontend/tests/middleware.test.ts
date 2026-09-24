import { describe, it, expect, vi, beforeEach } from 'vitest'
import { middleware } from '@/middleware'
import { NextRequest } from 'next/server'

function createRequest(
  path: string,
  options: {
    cookies?: Record<string, string>
    acceptLanguage?: string
  } = {}
): NextRequest {
  const url = `http://localhost:3000${path}`
  const headers = new Headers()
  if (options.acceptLanguage) {
    headers.set('accept-language', options.acceptLanguage)
  }

  const req = new NextRequest(url, { headers })

  if (options.cookies) {
    Object.entries(options.cookies).forEach(([key, value]) => {
      req.cookies.set(key, value)
    })
  }

  return req
}

describe('middleware', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('route protection', () => {
    it('redirects to /login for protected routes without refresh_token', () => {
      const req = createRequest('/dashboard')
      const res = middleware(req)

      expect(res.status).toBe(307)
      expect(res.headers.get('location')).toContain('/login')
    })

    it('allows protected routes with refresh_token', () => {
      const req = createRequest('/dashboard', {
        cookies: { refresh_token: 'valid-token' },
      })
      const res = middleware(req)

      expect(res.status).toBe(200)
    })

    it('allows public routes without refresh_token', () => {
      const req = createRequest('/login')
      const res = middleware(req)

      expect(res.status).toBe(200)
    })

    it('redirects for nested protected routes', () => {
      const req = createRequest('/admin/users')
      const res = middleware(req)

      expect(res.status).toBe(307)
      expect(res.headers.get('location')).toContain('/login')
    })

    it('redirects for lesson routes', () => {
      const req = createRequest('/lesson/123')
      const res = middleware(req)

      expect(res.status).toBe(307)
    })
  })

  describe('locale detection', () => {
    it('respects NEXT_LOCALE cookie and sets it in response', () => {
      const req = createRequest('/login', {
        cookies: { NEXT_LOCALE: 'es' },
        acceptLanguage: 'fr',
      })
      const res = middleware(req)

      const setCookie = res.headers.get('set-cookie')
      expect(setCookie).toBeNull()
    })

    it('detects locale from Accept-Language header and sets cookie', () => {
      const req = createRequest('/login', {
        acceptLanguage: 'es-ES,es;q=0.9,en;q=0.8',
      })
      const res = middleware(req)

      const setCookie = res.headers.get('set-cookie')
      expect(setCookie).toContain('NEXT_LOCALE=es')
    })

    it('detects Swedish browser language from sv-SE', () => {
      const req = createRequest('/login', {
        acceptLanguage: 'sv-SE,sv;q=0.9,en;q=0.8',
      })

      const res = middleware(req)
      expect(res.headers.get('set-cookie')).toContain('NEXT_LOCALE=sv')
    })

    it('detects Danish browser language from da-DK', () => {
      const req = createRequest('/login', {
        acceptLanguage: 'da-DK,da;q=0.9,en;q=0.8',
      })

      const res = middleware(req)
      expect(res.headers.get('set-cookie')).toContain('NEXT_LOCALE=da')
    })

    it('detects Finnish browser language from fi-FI', () => {
      const req = createRequest('/login', {
        acceptLanguage: 'fi-FI,fi;q=0.9,en;q=0.8',
      })

      const res = middleware(req)
      expect(res.headers.get('set-cookie')).toContain('NEXT_LOCALE=fi')
    })

    it('falls back to en when no locale detected', () => {
      const req = createRequest('/login')
      const res = middleware(req)

      const setCookie = res.headers.get('set-cookie')
      expect(setCookie).toContain('NEXT_LOCALE=en')
    })

    it('parses complex Accept-Language headers', () => {
      const req = createRequest('/login', {
        acceptLanguage: 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
      })
      const res = middleware(req)

      const setCookie = res.headers.get('set-cookie')
      expect(setCookie).toContain('NEXT_LOCALE=fr')
    })

    it('sets NEXT_LOCALE cookie when not present', () => {
      const req = createRequest('/login', {
        acceptLanguage: 'es',
      })
      const res = middleware(req)

      const setCookie = res.headers.get('set-cookie')
      expect(setCookie).toContain('NEXT_LOCALE=es')
    })

    it('does not overwrite existing NEXT_LOCALE cookie', () => {
      const req = createRequest('/login', {
        cookies: { NEXT_LOCALE: 'fr' },
        acceptLanguage: 'es',
      })
      const res = middleware(req)

      const setCookie = res.headers.get('set-cookie')
      expect(setCookie).toBeNull()
    })

    it('sets locale cookie on redirect to /login', () => {
      const req = createRequest('/dashboard', {
        acceptLanguage: 'es',
      })
      const res = middleware(req)

      const setCookie = res.headers.get('set-cookie')
      expect(setCookie).toContain('NEXT_LOCALE=es')
    })
  })
})
