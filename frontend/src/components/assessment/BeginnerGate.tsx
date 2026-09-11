'use client'

import { useTranslations } from 'next-intl'

interface Props {
  onBeginner: () => void
  onHasExperience: () => void
  languageCode: string
}

export default function BeginnerGate({
  onBeginner,
  onHasExperience,
  languageCode,
}: Props) {
  const t = useTranslations('assessment')
  const tLang = useTranslations('targetLanguages')

  return (
    <div className="flex min-h-[60vh] items-center justify-center p-6">
      <div className="border-fl-border bg-fl-surface w-full max-w-md border">
        <div className="border-fl-border flex items-center gap-2 border-b px-6 py-4">
          <span className="text-fl-label text-fl-muted-3">●</span>
          <span className="text-fl-label text-fl-muted-2 font-mono tracking-widest uppercase">
            {t('step1')}
          </span>
        </div>
        <div className="space-y-6 p-8">
          <div className="space-y-2 text-center">
            <p className="text-fl-body text-fl-fg font-mono">
              {t('studiedBefore', { language: tLang(languageCode) })}
            </p>
            <p className="text-fl-label text-fl-muted-3 font-mono">
              {t('studiedBeforeHint')}
            </p>
          </div>
          <div className="flex flex-col gap-3">
            <button
              onClick={onBeginner}
              className="border-fl-border text-fl-muted-2 hover:border-fl-border-2 hover:text-fl-fg w-full border px-5 py-4 text-left font-mono text-sm tracking-widest uppercase transition-colors"
            >
              <span className="text-fl-muted-3 mr-3">○</span>
              {t('beginnerOption')}
              <span className="text-fl-hint text-fl-muted-3 mt-1 ml-6 block normal-case">
                {t('beginnerOptionHint')}
              </span>
            </button>
            <button
              onClick={onHasExperience}
              className="bg-fl-fg text-fl-bg hover:bg-fl-fg-bright w-full px-5 py-4 text-left font-mono text-sm font-bold tracking-widest uppercase transition-colors"
            >
              <span className="mr-3">●</span>
              {t('hasExperienceOption')}
              <span className="text-fl-hint mt-1 ml-6 block font-normal normal-case opacity-70">
                {t('hasExperienceOptionHint')}
              </span>
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
