'use client'

import Link from 'next/link'
import { useEffect, useRef, useState } from 'react'
import { useTranslations } from 'next-intl'
import { X } from 'lucide-react'
import { useAuthStore, isSubscribed, needsPaymentRecovery } from '@/store/auth'
import { useConfigStore } from '@/store/config'
import { useFreemiumStore } from '@/store/freemium'
import { useTrialStatus } from '@/hooks/useTrialStatus'
import { claimPremiumResultOffer } from '@/lib/premium-prompts'
import { PaywallBanner } from '@/components/billing/PaywallBanner'

type ResultFeature =
  'voice' | 'lessons' | 'listening' | 'reading' | 'games' | 'flashcards'

interface PremiumResultOfferProps {
  feature: ResultFeature
  blocked?: boolean
  accessExhausted?: boolean
  className?: string
}

/** Mount only for a newly completed activity, never for saved history or review. */
export function PremiumResultOffer({
  feature,
  blocked = false,
  accessExhausted = false,
  className = '',
}: PremiumResultOfferProps) {
  const user = useAuthStore((s) => s.user)
  const sessionVersion = useAuthStore((s) => s.sessionVersion)
  const loaded = useConfigStore((s) => s.loaded)
  const stripeEnabled = useConfigStore((s) => s.stripeEnabled)
  if (
    blocked ||
    !loaded ||
    !user ||
    !stripeEnabled ||
    isSubscribed(user, stripeEnabled)
  ) {
    return null
  }
  return (
    <ResultOffer
      key={`${sessionVersion}:${user.id}:${feature}`}
      userId={user.id}
      feature={feature}
      className={className}
      accessExhausted={accessExhausted}
    />
  )
}

function ResultOffer({
  userId,
  feature,
  className,
  accessExhausted,
}: {
  userId: number
  feature: ResultFeature
  className: string
  accessExhausted: boolean
}) {
  const t = useTranslations('premiumOffer')
  const tCommon = useTranslations('common')
  const status = useFreemiumStore((s) => s.status)
  const paymentRecovery = useAuthStore((s) => needsPaymentRecovery(s.user))
  const { freemiumTrialActive } = useTrialStatus()
  const remaining =
    feature === 'flashcards'
      ? undefined
      : feature === 'voice'
        ? status?.voice_remaining_seconds
        : status?.[`${feature}_remaining`]
  const limit =
    feature === 'flashcards'
      ? undefined
      : feature === 'voice'
        ? status?.voice_limit_seconds
        : status?.[`${feature}_limit`]
  const exhausted =
    !freemiumTrialActive &&
    (accessExhausted ||
      (status?.trial_active === false &&
        remaining !== undefined &&
        remaining <= 0))
  const [offered, setOffered] = useState(false)
  const [dismissed, setDismissed] = useState(false)
  const anchor = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (paymentRecovery || exhausted || offered || dismissed) return
    const element = anchor.current
    if (!element) return
    let visible = false
    function offer() {
      if (!visible || document.visibilityState === 'hidden') return
      if (claimPremiumResultOffer(userId)) setOffered(true)
    }
    if (typeof IntersectionObserver === 'undefined') {
      visible = true
      offer()
      document.addEventListener('visibilitychange', offer)
      return () => document.removeEventListener('visibilitychange', offer)
    }
    const observer = new IntersectionObserver(([entry]) => {
      visible = !!entry?.isIntersecting
      offer()
    })
    observer.observe(element)
    document.addEventListener('visibilitychange', offer)
    return () => {
      observer.disconnect()
      document.removeEventListener('visibilitychange', offer)
    }
  }, [userId, paymentRecovery, exhausted, offered, dismissed])

  if (paymentRecovery) {
    return exhausted && feature !== 'flashcards' ? (
      <PaywallBanner feature={feature} compact />
    ) : null
  }

  if (dismissed && !exhausted) return null
  if (!exhausted && !offered)
    return <div ref={anchor} className="min-h-px" aria-hidden="true" />

  return (
    <aside
      aria-label={t('resultTitle')}
      className={`border-fl-border bg-fl-surface relative border p-4 ${className}`}
    >
      {!exhausted && (
        <button
          type="button"
          onClick={() => setDismissed(true)}
          aria-label={tCommon('close')}
          className="text-fl-muted-2 hover:text-fl-fg focus-visible:outline-fl-accent absolute top-2 right-2 p-2 focus-visible:outline-2"
        >
          <X className="size-4" aria-hidden="true" />
        </button>
      )}
      <h3 className="text-fl-fg pr-8 font-sans text-base font-semibold">
        {t(exhausted ? 'exhaustedTitle' : 'resultTitle')}
      </h3>
      <p className="text-fl-muted-1 mt-2 font-sans text-sm leading-relaxed">
        {t(`result.${feature}`)}
      </p>
      {freemiumTrialActive && (
        <p className="text-fl-muted-2 mt-2 font-sans text-sm">
          {t('trialResultNote')}
        </p>
      )}
      {exhausted && limit !== undefined && limit > 0 && (
        <p className="text-fl-muted-2 mt-2 font-sans text-sm">
          {t(
            feature === 'voice' ||
              feature === 'listening' ||
              feature === 'reading'
              ? 'weeklyReset'
              : 'dailyReset'
          )}
        </p>
      )}
      <Link
        href="/settings#plan"
        className="bg-fl-accent text-fl-accent-fg hover:bg-fl-accent/90 focus-visible:outline-fl-accent mt-3 inline-flex px-4 py-2 font-sans text-sm font-semibold focus-visible:outline-2 focus-visible:outline-offset-2"
      >
        {t(exhausted ? 'continuePremium' : 'viewPremium')}
      </Link>
    </aside>
  )
}
