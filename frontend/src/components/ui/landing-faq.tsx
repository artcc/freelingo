'use client'

import { useState } from 'react'
import { useTranslations } from 'next-intl'

const FAQ_KEYS = [
  'q_start',
  'q_workflow',
  'q_language',
  'q_assessment',
  'q_studyPlan',
  'q_resources',
  'q_flashcards',
  'q_vocabulary',
  'q_tutor',
  'q_voice',
  'q_listening',
  'q_reading',
]

export function LandingFAQ() {
  const t = useTranslations('faq')
  const [open, setOpen] = useState<number | null>(null)

  const strong = (chunks: React.ReactNode) => (
    <strong className="text-fl-fg">{chunks}</strong>
  )

  const renderAnswer = (key: string) => {
    const answerKey = `a_${key.replace('q_', '')}`

    if (key === 'q_workflow') {
      const steps = [
        t('workflowStep1'),
        t('workflowStep2'),
        t('workflowStep3'),
        t('workflowStep4'),
        t('workflowStep5'),
        t('workflowStep6'),
      ]
      return (
        <ol className="list-none space-y-1">
          {steps.map((step, i) => (
            <li key={i} className="flex items-start gap-3">
              <span className="text-fl-label text-fl-muted-4 mt-0.5 shrink-0 font-mono">
                {i + 1}.
              </span>
              <span>{step}</span>
            </li>
          ))}
        </ol>
      )
    }

    // For rich-text answers that use <strong> tags
    if (
      [
        'q_start',
        'q_studyPlan',
        'q_resources',
        'q_flashcards',
        'q_vocabulary',
        'q_voice',
        'q_listening',
        'q_reading',
      ].includes(key)
    ) {
      return t.rich(answerKey, { strong })
    }

    return t(answerKey)
  }

  return (
    <div className="border-fl-border border">
      {FAQ_KEYS.map((key, i) => (
        <div
          key={key}
          className={i < FAQ_KEYS.length - 1 ? 'border-fl-border border-b' : ''}
        >
          <button
            onClick={() => setOpen(open === i ? null : i)}
            className="hover:bg-fl-surface flex w-full items-center justify-between px-5 py-4 text-left transition-colors"
          >
            <span className="text-fl-fg pr-4 font-sans text-sm">{t(key)}</span>
            <span className="text-fl-muted-2 shrink-0 font-mono text-sm">
              {open === i ? '−' : '+'}
            </span>
          </button>
          {open === i && (
            <div className="text-fl-muted-1 border-fl-border bg-fl-bg-alt border-t px-5 pt-4 pb-5 font-sans text-sm leading-relaxed">
              <div className="max-w-[70ch]">{renderAnswer(key)}</div>
            </div>
          )}
        </div>
      ))}
    </div>
  )
}
