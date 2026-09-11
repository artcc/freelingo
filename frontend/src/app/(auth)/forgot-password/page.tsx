'use client'

import { useState } from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { useTranslations } from 'next-intl'
import { Loader2 } from 'lucide-react'
import { apiFetch } from '@/lib/api'

export default function ForgotPasswordPage() {
  const t = useTranslations('auth.forgotPassword')
  const [email, setEmail] = useState('')
  const [sent, setSent] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const res = await apiFetch('/api/auth/forgot-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      })
      if (!res.ok) throw new Error(t('error'))
      setSent(true)
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : t('error'))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-fl-bg flex min-h-screen items-center justify-center px-4">
      <div className="w-full max-w-sm">
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
        </div>

        <div className="border-fl-border bg-fl-surface space-y-6 border p-8">
          <div className="flex items-center gap-2">
            <span className="text-fl-label text-fl-muted-2">●</span>
            <span className="text-fl-caption text-fl-muted-2 font-mono tracking-widest uppercase">
              {t('title')}
            </span>
          </div>

          {sent ? (
            <div className="space-y-4">
              <p className="text-fl-muted-1 font-mono text-sm leading-relaxed">
                {t('sent')}
              </p>
              <Link
                href="/login"
                className="text-fl-muted-2 hover:text-fl-fg block font-mono text-xs underline transition-colors"
              >
                {t('backToLogin')}
              </Link>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-4">
              <p className="text-fl-muted-2 font-mono text-sm leading-relaxed">
                {t('description')}
              </p>
              {error && (
                <div className="border-fl-error/40 text-fl-error border px-4 py-3 font-mono text-xs">
                  ✕ {error}
                </div>
              )}
              <input
                type="email"
                placeholder={t('emailPlaceholder')}
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                autoCorrect="off"
                autoCapitalize="none"
                spellCheck={false}
                className="bg-fl-bg border-fl-border text-fl-fg placeholder:text-fl-muted-4 focus:border-fl-border-2 w-full border px-4 py-3 font-mono text-xs transition-colors focus:outline-none"
              />
              <button
                type="submit"
                disabled={loading}
                className="bg-fl-accent text-fl-accent-fg hover:bg-fl-accent/90 w-full py-3 font-mono text-sm font-bold tracking-widest uppercase transition-colors disabled:opacity-50"
              >
                {loading ? (
                  <>
                    <Loader2 className="mr-2 inline h-4 w-4 animate-spin" />
                    {t('sending')}
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
