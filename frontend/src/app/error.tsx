'use client'

import { useEffect } from 'react'
import { useTranslations } from 'next-intl'
import { getLogger } from '@/lib/logger'

const errorLogger = getLogger('global-error')

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  const t = useTranslations('error')

  useEffect(() => {
    errorLogger.error('Unhandled error', error)
  }, [error])

  return (
    <div className="bg-fl-bg flex min-h-screen items-center justify-center p-6">
      <div className="border-fl-border bg-fl-surface w-full max-w-md border">
        {/* Header */}
        <div className="border-fl-border flex items-center gap-3 border-b px-8 py-6">
          <span className="text-fl-muted-2 font-mono text-sm">●</span>
          <span className="text-fl-muted-2 font-code text-xs tracking-widest uppercase">
            FreeLingo
          </span>
        </div>

        {/* Body */}
        <div className="space-y-6 px-8 py-8">
          <div className="space-y-1">
            <p className="text-fl-label text-fl-muted-2 font-mono tracking-widest uppercase">
              {t('label')}
            </p>
            <h1 className="text-fl-fg font-mono text-xl font-bold tracking-tight">
              {t('title')}
            </h1>
          </div>

          <p className="text-fl-fg-2 font-mono text-sm leading-relaxed">
            {t('body')}
          </p>

          {error.digest && (
            <p className="text-fl-hint text-fl-muted-2 font-mono tracking-wide">
              {t('digest')}:{' '}
              <span className="text-fl-muted-1">{error.digest}</span>
            </p>
          )}

          <div className="flex flex-col gap-3 pt-2 sm:flex-row">
            <button
              onClick={reset}
              className="bg-fl-fg text-fl-bg hover:bg-fl-fg-bright flex-1 px-6 py-3 font-mono text-sm tracking-widest uppercase transition-colors"
            >
              {t('retry')}
            </button>
            <a
              href="/dashboard"
              className="border-fl-border text-fl-fg-2 hover:bg-fl-surface-2 flex-1 border px-6 py-3 text-center font-mono text-xs tracking-widest uppercase transition-colors"
            >
              {t('dashboard')}
            </a>
          </div>
        </div>

        {/* Footer */}
        <div className="border-fl-border border-t px-8 py-4">
          <p className="text-fl-hint text-fl-muted-2 text-center font-mono">
            &copy; FreeLingo
          </p>
        </div>
      </div>
    </div>
  )
}
