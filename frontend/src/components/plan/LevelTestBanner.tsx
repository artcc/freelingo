'use client'

import { useRouter } from 'next/navigation'
import { useTranslations } from 'next-intl'

interface Props {
  planId: number
  level: string
}

export default function LevelTestBanner({ planId, level }: Props) {
  const t = useTranslations('plan')
  const router = useRouter()

  return (
    <div className="border-fl-fg bg-fl-surface mt-2 border">
      <div className="border-fl-fg/20 flex items-center gap-2 border-b px-6 py-4">
        <span className="text-fl-label text-fl-fg font-mono">⊞</span>
        <span className="text-fl-label text-fl-fg font-mono tracking-widest uppercase">
          {t('levelComplete', { level })}
        </span>
      </div>
      <div className="space-y-4 p-6">
        <p className="text-fl-label text-fl-muted-1 font-mono leading-relaxed">
          {t('levelCompleteDesc', { level })}
        </p>
        <p className="text-fl-hint text-fl-muted-3 font-mono">
          {t('levelCompleteHint')}
        </p>
        <button
          onClick={() => router.push(`/assessment/level-test?plan=${planId}`)}
          className="bg-fl-fg text-fl-bg hover:bg-fl-fg-bright px-6 py-3 font-mono text-sm font-bold tracking-widest uppercase transition-colors"
        >
          {t('beginLevelTest')} →
        </button>
      </div>
    </div>
  )
}
