'use client'

import Link from 'next/link'
import { useTranslations } from 'next-intl'

export default function BillingCanceledPage() {
  const t = useTranslations('billing')

  return (
    <div className="bg-fl-bg flex min-h-screen items-center justify-center px-4">
      <div className="border-fl-border bg-fl-surface w-full max-w-sm space-y-5 border p-8 text-center">
        <div className="text-fl-muted-2 text-2xl">△</div>
        <p className="text-fl-label text-fl-muted-2 font-mono tracking-widest uppercase">
          {t('canceledLabel')}
        </p>
        <h1 className="text-fl-fg font-mono text-base font-bold">
          {t('canceledTitle')}
        </h1>
        <p className="text-fl-muted-1 font-mono text-xs leading-relaxed">
          {t('canceledDesc')}
        </p>
        <div className="flex flex-col gap-2">
          <Link
            href="/dashboard"
            className="bg-fl-accent text-fl-accent-fg hover:bg-fl-accent/90 block py-3 font-mono text-sm font-bold tracking-widest uppercase transition-colors"
          >
            {t('canceledCtaDashboard')}
          </Link>
          <Link
            href="/settings"
            className="border-fl-border text-fl-muted-1 hover:text-fl-fg hover:border-fl-border-2 block border py-3 font-mono text-xs tracking-widest uppercase transition-colors"
          >
            {t('canceledCtaSettings')}
          </Link>
        </div>
        <p className="text-fl-hint text-fl-muted-3 font-mono tracking-widest uppercase">
          {t('canceledNoCharge')}
        </p>
      </div>
    </div>
  )
}
