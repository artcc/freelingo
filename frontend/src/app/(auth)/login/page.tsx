'use client'

import { Suspense, useCallback, useState } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import Link from 'next/link'
import Image from 'next/image'
import { useTranslations } from 'next-intl'
import { Loader2 } from 'lucide-react'
import { apiFetch } from '@/lib/api'
import { mapUser } from '@/lib/mappers'
import { useAuthStore } from '@/store/auth'

function LoginForm() {
  const t = useTranslations('auth.login')
  const tCommon = useTranslations('common')
  const router = useRouter()
  const searchParams = useSearchParams()
  const registered = searchParams.get('registered') === 'true'
  const setTokens = useAuthStore((s) => s.setTokens)
  const setUser = useAuthStore((s) => s.setUser)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = useCallback(
    async (e: React.FormEvent) => {
      e.preventDefault()
      setError('')
      if (!email.trim()) {
        setError(t('emailRequired'))
        return
      }
      if (!password) {
        setError(t('passwordRequired'))
        return
      }
      setLoading(true)
      try {
        const res = await apiFetch('/api/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password }),
        })
        if (!res.ok) {
          const data = await res.json().catch(() => ({}))
          if (Array.isArray(data.detail) && data.detail.length > 0) {
            const first = data.detail[0] as { loc?: string[]; msg?: string }
            const loc = (first.loc ?? []).join('.')
            if (
              loc.includes('email') ||
              first.msg?.toLowerCase().includes('email')
            ) {
              throw new Error(t('invalidEmail'))
            }
          }
          throw new Error(t('error'))
        }
        const { access_token } = await res.json()
        setTokens(access_token)
        const meRes = await apiFetch('/api/auth/me')
        if (meRes.ok) setUser(mapUser(await meRes.json()))
        router.push('/dashboard')
      } catch (err: unknown) {
        setError(err instanceof Error ? err.message : t('loginFailed'))
      } finally {
        setLoading(false)
      }
    },
    [email, password, router, setTokens, setUser, t]
  )

  return (
    <div className="bg-fl-bg flex min-h-screen items-center justify-center px-4">
      <div className="w-full max-w-sm">
        {/* Brand */}
        <div className="mb-10 flex flex-col items-center">
          <Image
            src="/logo.png"
            alt="FreeLingo"
            width={100}
            height={100}
            className="mb-4"
          />
          <h1 className="text-fl-fg font-code text-xl font-bold tracking-widest uppercase">
            FreeLingo
          </h1>
          <p className="text-fl-caption text-fl-muted-2 mt-1 font-mono tracking-widest uppercase">
            {tCommon('tagline')}
          </p>
        </div>

        <div className="border-fl-border bg-fl-surface border p-8">
          {/* Header */}
          <div className="border-fl-border mb-6 flex items-center gap-2 border-b pb-4">
            <span className="text-fl-label text-fl-muted-2">●</span>
            <span className="text-fl-muted-2 font-mono text-xs tracking-widest uppercase">
              {t('title')}
            </span>
          </div>

          {registered && (
            <div className="border-fl-border text-fl-muted-1 mb-5 border px-4 py-3 font-mono text-xs tracking-wide">
              ✓ {t('accountCreated')}
            </div>
          )}
          {error && (
            <div className="border-fl-error/40 text-fl-error mb-5 border px-4 py-3 font-mono text-xs tracking-wide">
              ✕ {error}
            </div>
          )}

          <form onSubmit={handleSubmit} noValidate className="space-y-4">
            <div>
              <label className="text-fl-muted-2 mb-2 block font-mono text-xs tracking-widest uppercase">
                {t('email')}
              </label>
              <input
                type="text"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                autoComplete="username"
                autoCorrect="off"
                autoCapitalize="none"
                spellCheck={false}
                className="bg-fl-bg border-fl-border text-fl-fg focus:border-fl-border-2 w-full border px-4 py-3 font-mono text-sm transition-colors focus:outline-none"
              />
            </div>
            <div>
              <label className="text-fl-muted-2 mb-2 block font-mono text-xs tracking-widest uppercase">
                {t('password')}
              </label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  autoComplete="current-password"
                  autoCorrect="off"
                  autoCapitalize="none"
                  spellCheck={false}
                  className="bg-fl-bg border-fl-border text-fl-fg focus:border-fl-border-2 w-full border px-4 py-3 pr-11 font-mono text-sm transition-colors focus:outline-none"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword((v) => !v)}
                  className="text-fl-muted-4 hover:text-fl-muted-0 absolute inset-y-0 right-0 flex items-center px-3 transition-colors"
                  aria-label={
                    showPassword ? t('hidePassword') : t('showPassword')
                  }
                >
                  {showPassword ? (
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="16"
                      height="16"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    >
                      <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94" />
                      <path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19" />
                      <line x1="1" y1="1" x2="23" y2="23" />
                    </svg>
                  ) : (
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="16"
                      height="16"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    >
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                      <circle cx="12" cy="12" r="3" />
                    </svg>
                  )}
                </button>
              </div>
            </div>
            <button
              type="submit"
              disabled={loading}
              className="bg-fl-accent text-fl-accent-fg hover:bg-fl-accent/90 mt-2 w-full py-3 font-mono text-sm font-bold tracking-widest uppercase transition-colors disabled:opacity-40"
            >
              {loading ? (
                <>
                  <Loader2 className="mr-2 inline h-4 w-4 animate-spin" />
                  {t('signingIn')}
                </>
              ) : (
                t('submit')
              )}
            </button>
          </form>

          <p className="text-fl-label text-fl-muted-2 mt-6 text-center font-mono tracking-wide">
            {t('noAccount')}{' '}
            <Link
              href="/register"
              className="text-fl-muted-1 hover:text-fl-fg transition-colors"
            >
              {t('register')}
            </Link>
          </p>
          <p className="text-fl-label text-fl-muted-4 mt-3 text-center font-mono tracking-wide">
            <Link
              href="/forgot-password"
              className="hover:text-fl-muted-2 transition-colors"
            >
              {t('forgotPassword')}
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}

export default function LoginPage() {
  return (
    <Suspense>
      <LoginForm />
    </Suspense>
  )
}
