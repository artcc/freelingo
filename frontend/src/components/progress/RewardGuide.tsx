'use client'

import Link from 'next/link'
import { ArrowUpRight, ChevronDown, Sparkles } from 'lucide-react'
import { useTranslations } from 'next-intl'

const REWARDS = [
  { key: 'lessons', links: [{ label: 'myPlan', href: '/plan' }] },
  { key: 'flashcards', links: [{ label: 'flashcards', href: '/flashcards' }] },
  { key: 'voice', links: [{ label: 'conversation', href: '/conversation' }] },
  { key: 'chat', links: [{ label: 'tutor', href: '/chat' }] },
  {
    key: 'comprehension',
    links: [
      { label: 'reading', href: '/reading' },
      { label: 'listening', href: '/listening' },
    ],
  },
  { key: 'games', links: [{ label: 'games', href: '/games' }] },
  { key: 'milestones', links: [{ label: 'myPlan', href: '/plan' }] },
] as const

export function RewardGuide() {
  const t = useTranslations('progressRewards')
  const nav = useTranslations('nav')

  return (
    <details className="border-fl-border bg-fl-surface group border">
      <summary className="text-fl-fg flex cursor-pointer list-none items-center gap-3 p-5 font-semibold focus-visible:outline-2 focus-visible:outline-offset-2 [&::-webkit-details-marker]:hidden">
        <Sparkles
          className="text-fl-accent size-5 shrink-0"
          aria-hidden="true"
        />
        {t('title')}
        <ChevronDown
          className="text-fl-muted-2 ml-auto size-4 shrink-0 group-open:rotate-180"
          aria-hidden="true"
        />
      </summary>
      <div className="border-fl-border border-t p-5">
        <p className="text-fl-muted-2 mb-5 text-sm leading-relaxed">
          {t('scope')}
        </p>
        <ul className="grid gap-5 sm:grid-cols-2">
          {REWARDS.map(({ key, links }) => (
            <li key={key} className="space-y-2">
              <p className="text-fl-muted-1 text-sm leading-relaxed">
                {t(key)}
              </p>
              <div className="flex flex-wrap gap-3">
                {links.map(({ label, href }) => (
                  <Link
                    key={href}
                    href={href}
                    className="text-fl-accent inline-flex items-center gap-1 text-sm font-medium hover:underline"
                  >
                    {nav(label)}
                    <ArrowUpRight className="size-4" aria-hidden="true" />
                  </Link>
                ))}
              </div>
            </li>
          ))}
        </ul>
      </div>
    </details>
  )
}
