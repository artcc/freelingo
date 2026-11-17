'use client'

import { useState } from 'react'
import Link from 'next/link'
import { useTranslations } from 'next-intl'
import { useAuthStore } from '@/store/auth'
import { useConfigStore } from '@/store/config'
import { trackBrowserEvent } from '@/lib/analytics'
import { useTargetLanguageList } from '@/hooks/useTargetLanguageList'

interface FAQItem {
  id: string
  q: string
  a: React.ReactNode
}

interface FAQSection {
  id: string
  title: string
  items: FAQItem[]
}

export default function FAQPage() {
  const t = useTranslations('faq')
  const languages = useTargetLanguageList()
  const [open, setOpen] = useState<string | null>(null)
  const isAdmin = useAuthStore((s) => s.user?.role === 'admin')
  const showSubscription = useConfigStore((s) => s.loaded && s.stripeEnabled)

  const strong = (chunks: React.ReactNode) => (
    <strong className="text-fl-fg">{chunks}</strong>
  )
  const code = (chunks: React.ReactNode) => (
    <code className="text-fl-fg bg-fl-surface-2 px-1">{chunks}</code>
  )
  const link = (href: string) =>
    function FAQLink(chunks: React.ReactNode) {
      return (
        <Link href={href} className="text-fl-fg underline underline-offset-2">
          {chunks}
        </Link>
      )
    }
  const adminLink = link('/admin/users')
  const settingsLink = link('/settings')
  const feedbackLink = link('/feedback')
  const languagesLink = link('/settings/languages')
  const grammarLink = link('/grammar')
  const gamesLink = link('/games')
  const memoriesLink = link('/settings/memories')
  const billingLink = link('/settings#plan')

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

  const sections: FAQSection[] = [
    {
      id: 'getting-started',
      title: t('sectionGettingStarted'),
      items: [
        { id: 'start', q: t('q_start'), a: t.rich('a_start', { strong }) },
        {
          id: 'workflow',
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
        {
          id: 'language',
          q: t('q_language'),
          a: t('a_language', { languages }),
        },
        {
          id: 'multiLanguage',
          q: t('q_multiLanguage'),
          a: t.rich('a_multiLanguage', { languagesLink }),
        },
        { id: 'assessment', q: t('q_assessment'), a: t('a_assessment') },
        {
          id: 'studyPlan',
          q: t('q_studyPlan'),
          a: t.rich('a_studyPlan', { strong }),
        },
      ],
    },
    {
      id: 'practice',
      title: t('sectionPractice'),
      items: [
        {
          id: 'resources',
          q: t('q_resources'),
          a: t.rich('a_resources', { strong }),
        },
        {
          id: 'grammarPractice',
          q: t('q_grammarPractice'),
          a: t.rich('a_grammarPractice', { grammarLink, strong }),
        },
        {
          id: 'games',
          q: t('q_games'),
          a: t.rich('a_games', { gamesLink }),
        },
        {
          id: 'flashcards',
          q: t('q_flashcards'),
          a: t.rich('a_flashcards', { strong }),
        },
        {
          id: 'vocabulary',
          q: t('q_vocabulary'),
          a: t.rich('a_vocabulary', { strong }),
        },
        {
          id: 'listening',
          q: t('q_listening'),
          a: t.rich('a_listening', { strong }),
        },
        {
          id: 'reading',
          q: t('q_reading'),
          a: t.rich('a_reading', { strong }),
        },
      ],
    },
    {
      id: 'lingu',
      title: t('sectionLingu'),
      items: [
        { id: 'tutor', q: t('q_tutor'), a: t('a_tutor') },
        {
          id: 'voice',
          q: t('q_voice'),
          a: t.rich('a_voice', { strong, settingsLink }),
        },
        {
          id: 'memories',
          q: t('q_memories'),
          a: t.rich('a_memories', { memoriesLink }),
        },
      ],
    },
  ]

  if (showSubscription) {
    sections.push({
      id: 'subscription',
      title: t('sectionSubscription'),
      items: [
        { id: 'plans', q: t('q_plans'), a: t.rich('a_plans', { billingLink }) },
        {
          id: 'quotas',
          q: t('q_quotas'),
          a: t.rich('a_quotas', { billingLink }),
        },
        {
          id: 'cancelSubscription',
          q: t('q_cancelSubscription'),
          a: t.rich('a_cancelSubscription', { billingLink, strong }),
        },
      ],
    })
  }

  sections.push({
    id: 'account',
    title: t('sectionAccount'),
    items: [
      {
        id: 'password',
        q: t('q_password'),
        a: t.rich('a_password', { settingsLink }),
      },
      {
        id: 'uiLanguage',
        q: t('q_uiLanguage'),
        a: t.rich('a_uiLanguage', { settingsLink, strong }),
      },
      {
        id: 'feedback',
        q: t('q_feedback'),
        a: t.rich('a_feedback', { feedbackLink }),
      },
    ],
  })

  if (isAdmin) {
    sections.push({
      id: 'admin',
      title: t('sectionAdmin'),
      items: [
        {
          id: 'providers',
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
        {
          id: 'invite',
          q: t('q_invite'),
          a: t.rich('a_invite', { adminLink, code }),
        },
      ],
    })
  }

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

      <div className="space-y-8">
        {sections.map((section) => (
          <section key={section.id} aria-labelledby={`faq-${section.id}`}>
            <h2
              id={`faq-${section.id}`}
              className="text-fl-fg mb-3 font-sans text-base font-semibold"
            >
              {section.title}
            </h2>
            <div className="border-fl-border border">
              {section.items.map((item, i) => (
                <div
                  key={item.id}
                  className={
                    i < section.items.length - 1
                      ? 'border-fl-border border-b'
                      : ''
                  }
                >
                  <h3>
                    <button
                      type="button"
                      id={`faq-${item.id}-question`}
                      aria-expanded={open === item.id}
                      aria-controls={`faq-${item.id}-answer`}
                      onClick={() => {
                        if (open !== item.id) trackBrowserEvent('faq_viewed')
                        setOpen(open === item.id ? null : item.id)
                      }}
                      className="hover:bg-fl-surface focus-visible:outline-fl-accent flex w-full items-center justify-between px-5 py-4 text-left transition-colors focus-visible:outline-2 focus-visible:outline-offset-2"
                    >
                      <span className="text-fl-fg pr-4 font-sans text-sm tracking-wide">
                        {item.q}
                      </span>
                      <span
                        aria-hidden="true"
                        className="text-fl-muted-2 shrink-0 font-sans text-sm"
                      >
                        {open === item.id ? '−' : '+'}
                      </span>
                    </button>
                  </h3>
                  <div
                    id={`faq-${item.id}-answer`}
                    role="region"
                    aria-labelledby={`faq-${item.id}-question`}
                    hidden={open !== item.id}
                    className="text-fl-muted-1 border-fl-border bg-fl-bg-alt border-t px-5 pt-4 pb-5 font-sans text-sm leading-relaxed"
                  >
                    {item.a}
                  </div>
                </div>
              ))}
            </div>
          </section>
        ))}
      </div>
    </div>
  )
}
