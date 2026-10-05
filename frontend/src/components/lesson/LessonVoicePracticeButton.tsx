'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useTranslations } from 'next-intl'
import { Mic } from 'lucide-react'
import { ConfirmDialog } from '@/components/ui/confirm-dialog'
import { TargetLanguageText } from '@/components/TargetLanguageText'

export function LessonVoicePracticeButton({
  lessonId,
  title,
  targetLanguage,
}: {
  lessonId: number
  title: string
  targetLanguage?: string
}) {
  const t = useTranslations('lessonPractice')
  const router = useRouter()
  const [open, setOpen] = useState(false)

  return (
    <>
      <button
        type="button"
        onClick={() => setOpen(true)}
        className="border-fl-border text-fl-fg hover:bg-fl-surface-2 inline-flex items-center justify-center gap-2 border px-4 py-3 font-sans text-sm transition-colors"
      >
        <Mic className="size-4 shrink-0" aria-hidden="true" />
        {t('action')}
      </button>
      <ConfirmDialog
        open={open}
        title={
          <TargetLanguageText
            languageCode={targetLanguage}
            className="font-sans tracking-normal normal-case"
          >
            {t('title', { title })}
          </TargetLanguageText>
        }
        message={t('description')}
        confirmLabel={t('start')}
        cancelLabel={t('cancel')}
        onCancel={() => setOpen(false)}
        onConfirm={() => {
          setOpen(false)
          router.push(`/conversation?lesson=${lessonId}`)
        }}
      />
    </>
  )
}
