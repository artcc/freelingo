'use client'

import { useLocale, useTranslations } from 'next-intl'
import { formatVoiceDuration } from '@/lib/voice-duration'

export default function FreeVoiceBalance({ seconds }: { seconds: number }) {
  const t = useTranslations('conversation')
  const locale = useLocale()
  return (
    <p
      className={`text-fl-label font-mono tracking-widest uppercase ${seconds === 0 ? 'text-fl-error' : 'text-fl-muted-2'}`}
    >
      {t('freeBalance', { duration: formatVoiceDuration(seconds, locale) })}
      {seconds === 0 && ` ${t('weeklyReset')}`}
    </p>
  )
}
