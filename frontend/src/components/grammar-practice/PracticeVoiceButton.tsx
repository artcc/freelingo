'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useLocale, useTranslations } from 'next-intl'
import { Mic } from 'lucide-react'
import { ConfirmDialog } from '@/components/ui/confirm-dialog'
import { TargetLanguageText } from '@/components/TargetLanguageText'
import {
  practiceButton,
  practiceScope,
  canActInPractice,
} from './PracticeScope'

export function PracticeVoiceButton({
  sessionId,
  title,
  targetLanguage,
}: {
  sessionId: string
  title: string
  targetLanguage: string
}) {
  const t = useTranslations('lessonPractice')
  const practice = useTranslations('grammarPractice')
  const locale = useLocale()
  const router = useRouter()
  const [open, setOpen] = useState(false)
  const scope = practiceScope()
  return (
    <>
      <button
        type="button"
        className={`${practiceButton} inline-flex items-center gap-2`}
        onClick={() => setOpen(true)}
      >
        <Mic className="size-4" aria-hidden="true" />
        {practice('voiceAction')}
      </button>
      <ConfirmDialog
        open={open}
        title={
          <span lang={locale} className="font-sans tracking-normal normal-case">
            {t.rich('title', {
              title,
              topic: (chunks) => (
                <TargetLanguageText languageCode={targetLanguage}>
                  {chunks}
                </TargetLanguageText>
              ),
            })}
          </span>
        }
        message={practice('voiceDescription')}
        confirmLabel={t('start')}
        cancelLabel={t('cancel')}
        onCancel={() => setOpen(false)}
        onConfirm={() => {
          setOpen(false)
          if (canActInPractice(scope))
            router.push(`/conversation?grammarPractice=${sessionId}`)
        }}
      />
    </>
  )
}
