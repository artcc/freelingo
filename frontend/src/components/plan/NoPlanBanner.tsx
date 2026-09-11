'use client'

import { useRouter } from 'next/navigation'
import { useTranslations } from 'next-intl'
import { BookOpen } from 'lucide-react'

export default function NoPlanBanner() {
  const t = useTranslations('plan')
  const router = useRouter()

  return (
    <div className="flex min-h-[60vh] flex-col items-center justify-center px-6 py-16 text-center">
      <div className="border-fl-border bg-fl-surface w-full max-w-md border p-8">
        <BookOpen
          className="text-fl-muted-2 mx-auto mb-4 h-6 w-6"
          aria-hidden="true"
        />

        <p className="text-fl-label text-fl-muted-2 mb-2 font-mono tracking-widest uppercase">
          {t('noPlanLabel')}
        </p>
        <h2 className="text-fl-fg mb-3 font-mono text-base font-bold">
          {t('noPlanTitle')}
        </h2>
        <p className="text-fl-muted-1 mb-6 font-mono text-sm leading-relaxed">
          {t('noPlanDesc')}
        </p>

        <button
          onClick={() => router.push('/assessment')}
          className="bg-fl-accent text-fl-accent-fg hover:bg-fl-accent/90 w-full px-4 py-3 font-mono text-sm font-bold tracking-widest uppercase transition-colors"
        >
          {t('startAssessment')}
        </button>

        <p className="text-fl-hint text-fl-muted-3 mt-6 font-mono tracking-widest uppercase">
          {t('noPlanHint')}
        </p>
      </div>
    </div>
  )
}
