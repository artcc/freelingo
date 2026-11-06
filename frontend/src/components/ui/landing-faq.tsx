'use client'

import { useEffect, useId, useState } from 'react'
import { useTranslations } from 'next-intl'
import { trackBrowserEvent } from '@/lib/analytics'
import { useConfigStore } from '@/store/config'
import { useTargetLanguageList } from '@/hooks/useTargetLanguageList'

const FAQ_KEYS = ['modes', 'free', 'hosting', 'data', 'languages', 'start']

export function LandingFAQ() {
  const t = useTranslations('landing.faq')
  const languages = useTargetLanguageList()
  const id = useId()
  const [open, setOpen] = useState<number | null>(null)

  useEffect(() => {
    void useConfigStore.getState().load()
  }, [])

  return (
    <div className="border-fl-border border">
      {FAQ_KEYS.map((key, i) => (
        <div
          key={key}
          className={i < FAQ_KEYS.length - 1 ? 'border-fl-border border-b' : ''}
        >
          <button
            type="button"
            id={`${id}-${key}-question`}
            aria-expanded={open === i}
            aria-controls={`${id}-${key}-answer`}
            onClick={() => {
              if (open !== i) trackBrowserEvent('faq_viewed')
              setOpen(open === i ? null : i)
            }}
            className="hover:bg-fl-surface focus-visible:outline-fl-accent flex w-full items-center justify-between px-5 py-4 text-left transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 motion-reduce:transition-none"
          >
            <span className="text-fl-fg pr-4 font-sans text-sm">
              {t(`${key}.question`)}
            </span>
            <span
              className="text-fl-muted-2 shrink-0 font-mono text-sm"
              aria-hidden="true"
            >
              {open === i ? '−' : '+'}
            </span>
          </button>
          <div
            id={`${id}-${key}-answer`}
            role="region"
            aria-labelledby={`${id}-${key}-question`}
            hidden={open !== i}
            className="text-fl-muted-1 border-fl-border bg-fl-bg-alt border-t px-5 pt-4 pb-5 font-sans text-sm leading-relaxed"
          >
            <p className="max-w-[70ch]">
              {key === 'languages'
                ? t('languages.answer', { languages })
                : t(`${key}.answer`)}
            </p>
          </div>
        </div>
      ))}
    </div>
  )
}
