'use client'

import { Suspense, useCallback, useEffect, useRef, useState } from 'react'
import { useSearchParams } from 'next/navigation'
import Link from 'next/link'
import { useTranslations } from 'next-intl'
import { apiFetch } from '@/lib/api'
import { PageLoading } from '@/components/ui/page-loading'

const VERIFY_TIMEOUT_MS = 15_000

function VerifyEmailContent() {
  const t = useTranslations('auth.verifyEmail')
  const tCommon = useTranslations('common')
  const searchParams = useSearchParams()
  const token = searchParams.get('token')
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>(
    'loading'
  )
  const controllerRef = useRef<AbortController | null>(null)

  const verify = useCallback(() => {
    if (!token) {
      setStatus('error')
      return
    }

    setStatus('loading')

    controllerRef.current?.abort()
    const controller = new AbortController()
    controllerRef.current = controller
    const timeoutId = setTimeout(() => controller.abort(), VERIFY_TIMEOUT_MS)

    apiFetch(`/api/auth/verify-email?token=${encodeURIComponent(token)}`, {
      signal: controller.signal,
    })
      .then((res) => setStatus(res.ok ? 'success' : 'error'))
      .catch((err) => {
        if (err instanceof DOMException && err.name === 'AbortError') {
          setStatus('error')
        } else {
          setStatus('error')
        }
      })
      .finally(() => {
        clearTimeout(timeoutId)
        controllerRef.current = null
      })
  }, [token])

  useEffect(() => {
    verify()
    return () => {
      controllerRef.current?.abort()
    }
  }, [verify])

  return (
    <div className="bg-fl-bg bg-dot-grid flex min-h-screen items-center justify-center px-4">
      <div className="w-full max-w-sm">
        <div className="mb-10 flex flex-col items-center">
          <h1 className="text-fl-fg font-code text-xl font-bold tracking-widest uppercase">
            FreeLingo
          </h1>
        </div>
        <div className="border-fl-border bg-fl-surface space-y-6 border p-8 text-center">
          <div className="flex items-center justify-center gap-2">
            <span className="text-fl-label text-fl-muted-2">●</span>
            <span className="text-fl-caption text-fl-muted-2 font-mono tracking-widest uppercase">
              {t('title')}
            </span>
          </div>

          {status === 'loading' && <PageLoading fullScreen={false} />}

          {status === 'success' && (
            <>
              <p className="text-fl-fg font-mono text-sm">{t('success')}</p>
              <Link
                href="/login"
                className="bg-fl-accent text-fl-accent-fg hover:bg-fl-accent/90 block w-full py-3 text-center font-mono text-xs font-bold tracking-widest uppercase transition-colors"
              >
                {t('goToLogin')}
              </Link>
            </>
          )}

          {status === 'error' && (
            <>
              <p className="text-fl-error font-mono text-xs">{t('error')}</p>
              <button
                onClick={verify}
                className="bg-fl-accent text-fl-accent-fg hover:bg-fl-accent/90 block w-full py-3 text-center font-mono text-xs font-bold tracking-widest uppercase transition-colors"
              >
                {tCommon('retry')}
              </button>
              <Link
                href="/login"
                className="text-fl-muted-2 hover:text-fl-fg block font-mono text-xs underline transition-colors"
              >
                {t('goToLogin')}
              </Link>
            </>
          )}
        </div>
      </div>
    </div>
  )
}

export default function VerifyEmailPage() {
  return (
    <Suspense>
      <VerifyEmailContent />
    </Suspense>
  )
}
