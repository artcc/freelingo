'use client'

import { useState } from 'react'
import Link from 'next/link'
import { useTranslations } from 'next-intl'
import { useAuthStore } from '@/store/auth'
import { trackBrowserEvent } from '@/lib/analytics'

interface FAQItem {
  q: string
  a: React.ReactNode
}

export default function FAQPage() {
  const t = useTranslations('faq')
  const [open, setOpen] = useState<number | null>(null)
  const isAdmin = useAuthStore((s) => s.user?.role === 'admin')

  const strong = (chunks: React.ReactNode) => (
    <strong className="text-fl-fg">{chunks}</strong>
  )
  const code = (chunks: React.ReactNode) => (
    <code className="text-fl-fg bg-fl-surface-2 px-1">{chunks}</code>
  )
  const adminLink = (chunks: React.ReactNode) => (
    <Link
      href="/admin/users"
      className="text-fl-fg underline underline-offset-2"
    >
      {chunks}
    </Link>
  )
  const settingsLink = (chunks: React.ReactNode) => (
    <Link href="/settings" className="text-fl-fg underline underline-offset-2">
      {chunks}
    </Link>
  )
  const feedbackLink = (chunks: React.ReactNode) => (
    <Link href="/feedback" className="text-fl-fg underline underline-offset-2">
      {chunks}
    </Link>
  )

  const workflowSteps = [
    t('workflowStep1'),
    t('workflowStep2'),
    t('workflowStep3'),
    t('workflowStep4'),
    t('workflowStep5'),
    t('workflowStep6'),
  ]

  const providers: [string, string][] = [
    ['ollama', t('provider_ollama')],
    ['openai', t('provider_openai')],
    ['anthropic', t('provider_anthropic')],
    ['deepseek', t('provider_deepseek')],
  ]

  const faqs: FAQItem[] = (() => {
    const items: FAQItem[] = [
      { q: t('q_start'), a: t.rich('a_start', { strong }) },
      { q: t('q_language'), a: t('a_language') },
      {
        q: t('q_workflow'),
        a: (
          <ol className="list-none space-y-1">
            {workflowSteps.map((step, i) => (
              <li key={i} className="flex items-start gap-3">
                <span className="text-fl-label text-fl-muted-4 mt-0.5 shrink-0 font-mono">
                  {i + 1}.
                </span>
                <span>{step}</span>
              </li>
            ))}
          </ol>
        ),
      },
      { q: t('q_assessment'), a: t('a_assessment') },
      { q: t('q_studyPlan'), a: t.rich('a_studyPlan', { strong }) },
      { q: t('q_resources'), a: t.rich('a_resources', { strong }) },
      { q: t('q_flashcards'), a: t.rich('a_flashcards', { strong }) },
      { q: t('q_vocabulary'), a: t.rich('a_vocabulary', { strong }) },
      { q: t('q_tutor'), a: t('a_tutor') },
      { q: t('q_voice'), a: t.rich('a_voice', { strong }) },
      { q: t('q_listening'), a: t.rich('a_listening', { strong }) },
      { q: t('q_reading'), a: t.rich('a_reading', { strong }) },
      { q: t('q_feedback'), a: t.rich('a_feedback', { feedbackLink }) },
      { q: t('q_password'), a: t.rich('a_password', { settingsLink }) },
      {
        q: t('q_uiLanguage'),
        a: t.rich('a_uiLanguage', { settingsLink, strong }),
      },
    ]

    if (isAdmin) {
      items.push(
        {
          q: t('q_providers'),
          a: (
            <>
              {t.rich('a_providers_intro', { code })}
              <ul className="mt-2 list-none space-y-1">
                {providers.map(([name, desc]) => (
                  <li key={name} className="flex items-start gap-2">
                    <code className="text-fl-muted-1 shrink-0">{name}</code>
                    <span className="text-fl-muted-2">— {desc}</span>
                  </li>
                ))}
              </ul>
            </>
          ),
        },
        { q: t('q_invite'), a: t.rich('a_invite', { adminLink, code }) }
      )
    }

    return items
  })()

  return (
    <div className="mx-auto max-w-4xl p-6">
      {/* Header */}
      <div className="border-fl-border mb-8 border-b pb-4">
        <p className="text-fl-label text-fl-muted-2 mb-1 font-mono tracking-widest uppercase">
          {t('title')}
        </p>
        <h1 className="text-fl-fg font-mono text-2xl font-bold tracking-tight">
          {t('subtitle')}
        </h1>
      </div>

      {/* Accordion */}
      <div className="border-fl-border border">
        {faqs.map((item, i) => (
          <div
            key={i}
            className={i < faqs.length - 1 ? 'border-fl-border border-b' : ''}
          >
            <button
              onClick={() => {
                if (open !== i) trackBrowserEvent('faq_viewed')
                setOpen(open === i ? null : i)
              }}
              className="hover:bg-fl-surface flex w-full items-center justify-between px-5 py-4 text-left transition-colors"
            >
              <span className="text-fl-fg pr-4 font-mono text-xs tracking-wide">
                {item.q}
              </span>
              <span className="text-fl-muted-2 shrink-0 font-mono text-sm">
                {open === i ? '−' : '+'}
              </span>
            </button>
            {open === i && (
              <div className="text-fl-muted-1 border-fl-border bg-fl-bg-alt border-t px-5 pt-4 pb-5 font-mono text-xs leading-relaxed">
                {item.a}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
