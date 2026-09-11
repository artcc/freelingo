'use client'

import { Suspense, useState } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import Link from 'next/link'
import { useTranslations } from 'next-intl'
import { Loader2 } from 'lucide-react'
import { apiFetch } from '@/lib/api'

function ResetPasswordContent() {
  const t = useTranslations('auth.resetPassword')
  const router = useRouter()
  const searchParams = useSearchParams()
  const token = searchParams.get('token') ?? ''
  const [password, setPassword] = useState('')
  const [confirm, setConfirm] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [done, setDone] = useState(false)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError('')
    if (password !== confirm) {
      setError(t('mismatch'))
      return
    }
    if (password.length < 8) {
      setError(t('tooShort'))
      return
    }
    setLoading(true)
    try {
      const res = await apiFetch('/api/auth/reset-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token, new_password: password }),
      })
      if (!res.ok) {
        const data = await res.json().catch(() => ({}))
        throw new Error(data.detail || t('error'))
      }
      setDone(true)
      setTimeout(() => router.push('/login'), 2000)
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : t('error'))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-fl-bg bg-dot-grid flex min-h-screen items-center justify-center px-4">
      <div className="w-full max-w-sm">
        <div className="mb-10 flex flex-col items-center">
          <h1 className="text-fl-fg font-code text-xl font-bold tracking-widest uppercase">
            FreeLingo
          </h1>
        </div>

        <div className="border-fl-border bg-fl-surface space-y-6 border p-8">
          <div className="flex items-center gap-2">
            <span className="text-fl-label text-fl-muted-2">●</span>
            <span className="text-fl-caption text-fl-muted-2 font-mono tracking-widest uppercase">
              {t('title')}
            </span>
          </div>

          {done ? (
            <p className="text-fl-muted-1 font-mono text-xs leading-relaxed">
              {t('success')}
            </p>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-4">
              {!token && (
                <div className="border-fl-error/40 text-fl-error border px-4 py-3 font-mono text-xs">
                  {t('missingToken')}
                </div>
              )}
              {error && (
                <div className="border-fl-error/40 text-fl-error border px-4 py-3 font-mono text-xs">
                  ✕ {error}
                </div>
              )}
              <input
                type="password"
                placeholder={t('newPassword')}
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                autoComplete="new-password"
                className="bg-fl-bg border-fl-border text-fl-fg placeholder:text-fl-muted-4 focus:border-fl-border-2 w-full border px-4 py-3 font-mono text-xs transition-colors focus:outline-none"
              />
              <input
                type="password"
                placeholder={t('confirmPassword')}
                required
                value={confirm}
                onChange={(e) => setConfirm(e.target.value)}
                autoComplete="new-password"
                className="bg-fl-bg border-fl-border text-fl-fg placeholder:text-fl-muted-4 focus:border-fl-border-2 w-full border px-4 py-3 font-mono text-xs transition-colors focus:outline-none"
              />
              <button
                type="submit"
                disabled={loading || !token}
                className="bg-fl-accent text-fl-accent-fg hover:bg-fl-accent/90 w-full py-3 font-mono text-xs font-bold tracking-widest uppercase transition-colors disabled:opacity-50"
              >
                {loading ? (
                  <>
                    <Loader2 className="mr-2 inline h-4 w-4 animate-spin" />
                    {t('saving')}
                  </>
                ) : (
                  t('submit')
                )}
              </button>
              <Link
                href="/login"
                className="text-fl-muted-4 hover:text-fl-muted-2 block text-center font-mono text-xs transition-colors"
              >
                {t('backToLogin')}
              </Link>
            </form>
          )}
        </div>
      </div>
    </div>
  )
}

export default function ResetPasswordPage() {
  return (
    <Suspense>
      <ResetPasswordContent />
    </Suspense>
  )
}
