'use client'

import Link from 'next/link'
import { useTranslations } from 'next-intl'
import { useFreemiumStore } from '@/store/freemium'
import { useAuthStore, isSubscribed } from '@/store/auth'
import { useConfigStore } from '@/store/config'
import { useTrialStatus } from '@/hooks/useTrialStatus'

interface FreemiumQuotaBannerProps {
  feature: 'chat' | 'lessons' | 'listening' | 'reading' | 'voice' | 'games'
  className?: string
}

export function FreemiumQuotaBanner({
  feature,
  className = '',
}: FreemiumQuotaBannerProps) {
  const t = useTranslations('freemium')
  const tPremium = useTranslations('premiumOffer')
  const user = useAuthStore((s) => s.user)
  const stripeEnabled = useConfigStore((s) => s.stripeEnabled)
  const status = useFreemiumStore((s) => s.status)
  const { freemiumTrialActive: trial, freemiumTrialDaysLeft: trialDaysLeft } =
    useTrialStatus()

  if (!stripeEnabled) return null
  if (isSubscribed(user, stripeEnabled)) return null

  if (trial) {
    return (
      <div
        className={`border-fl-border bg-fl-surface flex items-center justify-between border px-3 py-2 font-mono text-xs ${className}`}
      >
        <span className="text-fl-muted-2">
          ★ {t('trialDaysLeft', { days: trialDaysLeft })}
        </span>
        <Link
          href="/settings#plan"
          className="text-fl-accent focus-visible:outline-fl-accent tracking-widest uppercase underline-offset-4 hover:underline focus-visible:outline-2 focus-visible:outline-offset-2"
        >
          {t('trialUnlimited')}
        </Link>
      </div>
    )
  }

  if (!status) return null

  const limits: Record<
    string,
    { remaining: number; limit: number; label: string }
  > = {
    games: {
      remaining: status.games_remaining,
      limit: status.games_limit,
      label: t('gamesLabel'),
    },
    chat: {
      remaining: status.chat_remaining,
      limit: status.chat_limit,
      label: t('chatLabel'),
    },
    lessons: {
      remaining: status.lessons_remaining,
      limit: status.lessons_limit,
      label: t('lessonsLabel'),
    },
    listening: {
      remaining: status.listening_remaining,
      limit: status.listening_limit,
      label: t('listeningLabel'),
    },
    reading: {
      remaining: status.reading_remaining,
      limit: status.reading_limit,
      label: t('readingLabel'),
    },
    voice: {
      remaining: Math.ceil(status.voice_remaining_seconds / 60),
      limit: Math.ceil(status.voice_limit_seconds / 60),
      label: t('voiceLabel'),
    },
  }

  const info = limits[feature]
  if (!info) return null

  // Feature blocked entirely for free users (limit === 0)
  if (info.limit === 0) {
    return (
      <div
        className={`border-fl-border bg-fl-surface flex items-center justify-between border px-3 py-2 font-mono text-xs ${className}`}
      >
        <span className="text-fl-muted-2">{info.label}</span>
        <Link
          href="/settings#plan"
          className="text-fl-accent focus-visible:outline-fl-accent tracking-widest uppercase underline-offset-4 hover:underline focus-visible:outline-2 focus-visible:outline-offset-2"
        >
          {t('requiresSubscription')}
        </Link>
      </div>
    )
  }

  const pct = info.limit > 0 ? (info.remaining / info.limit) * 100 : 100
  const low = info.remaining <= 1 || pct <= 25

  return (
    <div
      className={`border-fl-border bg-fl-surface flex flex-wrap items-center justify-between gap-2 border px-3 py-2 font-mono text-xs ${className}`}
    >
      <span className="text-fl-muted-2">
        {info.label}:{' '}
        <span className={low ? 'text-red-500' : 'text-fl-muted-1'}>
          {info.remaining}/{info.limit}
        </span>
      </span>
      {low && (
        <Link
          href="/settings#plan"
          className="text-fl-accent focus-visible:outline-fl-accent tracking-widest uppercase underline-offset-4 hover:underline focus-visible:outline-2 focus-visible:outline-offset-2"
        >
          {t('freeLimit')}
        </Link>
      )}
      {low && (
        <span className="text-fl-muted-2 w-full font-sans text-xs leading-relaxed">
          {tPremium(
            feature === 'voice' ||
              feature === 'listening' ||
              feature === 'reading'
              ? 'weeklyReset'
              : 'dailyReset'
          )}
        </span>
      )}
    </div>
  )
}
