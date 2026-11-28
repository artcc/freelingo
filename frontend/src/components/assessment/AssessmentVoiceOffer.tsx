'use client'

import { useEffect, useState } from 'react'
import { useLocale, useTranslations } from 'next-intl'
import { useTrialStatus } from '@/hooks/useTrialStatus'
import { apiFetch } from '@/lib/api'
import { formatVoiceDuration } from '@/lib/voice-duration'
import { isSubscribed, useAuthStore } from '@/store/auth'
import { useConfigStore } from '@/store/config'
import { useFreemiumStore } from '@/store/freemium'
import { type QuotaStatus } from '@/types/api'

function isCount(value: unknown): value is number {
  return typeof value === 'number' && Number.isSafeInteger(value) && value >= 0
}

function remainingTime(quota: QuotaStatus | null): number | undefined {
  if (!quota) return
  const {
    daily_remaining_seconds: daily,
    weekly_remaining_seconds: weekly,
    sessions_this_week: sessions,
    sessions_limit: sessionLimit,
    tokens_this_month: tokens,
    tokens_monthly_limit: tokenLimit,
  } = quota
  if (
    daily === 0 ||
    weekly === 0 ||
    (isCount(sessions) &&
      isCount(sessionLimit) &&
      sessionLimit > 0 &&
      sessions >= sessionLimit) ||
    (isCount(tokens) &&
      isCount(tokenLimit) &&
      tokenLimit > 0 &&
      tokens >= tokenLimit)
  )
    return 0
  if (
    !(daily === null || isCount(daily)) ||
    !(weekly === null || isCount(weekly)) ||
    !isCount(sessions) ||
    !isCount(sessionLimit) ||
    !isCount(tokens) ||
    !isCount(tokenLimit)
  )
    return
  return Math.min(daily ?? Infinity, weekly ?? Infinity)
}

export default function AssessmentVoiceOffer({
  demoSeconds,
  onOpen,
}: {
  demoSeconds?: number
  onOpen: (useDemo: boolean) => void
}) {
  const t = useTranslations('assessment')
  const tConversation = useTranslations('conversation')
  const locale = useLocale()
  const user = useAuthStore((s) => s.user)
  const subscribed = useConfigStore(
    (s) => s.loaded && user !== null && isSubscribed(user, s.stripeEnabled)
  )
  const { freemiumTrialActive } = useTrialStatus()
  const status = useFreemiumStore((s) => (s.lastFetch ? s.status : null))
  const lastFetch = useFreemiumStore((s) => s.lastFetch)
  const fetchStatus = useFreemiumStore((s) => s.fetchStatus)
  const [quota, setQuota] = useState<QuotaStatus | null>(null)

  useEffect(() => {
    let controller: AbortController
    async function refresh() {
      controller?.abort()
      controller = new AbortController()
      const { signal } = controller
      const owner = useAuthStore.getState()
      setQuota(null)
      void fetchStatus(true)
      try {
        const response = await apiFetch('/api/auth/quota', { signal })
        if (!response.ok) return
        const data: QuotaStatus = await response.json()
        const current = useAuthStore.getState()
        if (
          !signal.aborted &&
          current.sessionVersion === owner.sessionVersion &&
          current.user?.id === owner.user?.id
        )
          setQuota(data)
      } catch {
        // The offer remains usable without a duration estimate.
      }
    }
    void refresh()
    window.addEventListener('focus', refresh)
    return () => {
      window.removeEventListener('focus', refresh)
      controller.abort()
    }
  }, [fetchStatus])

  useEffect(() => {
    if (!status?.trial_active) return
    const expiry = Date.parse(status.trial_ends_at ?? '')
    if (!(expiry > lastFetch)) return
    const remaining = Math.min(Math.max(0, expiry - Date.now()), 2_147_483_647)
    const timer = setTimeout(() => void fetchStatus(true), remaining)
    return () => clearTimeout(timer)
  }, [fetchStatus, lastFetch, status])

  const cap = remainingTime(quota)
  const balance = status?.voice_remaining_seconds
  const sessionLimit = user?.conversation_max_duration
  let description = t('voiceOfferCheck')
  let action = t('voiceOpen')
  // If a balance read fails, let the server resolve access with the valid token.
  // An explicitly offered ordinary session must not spend it if access changes.
  let useDemo = true
  if (
    subscribed ||
    (!status && freemiumTrialActive) ||
    (status?.trial_active && Date.parse(status.trial_ends_at ?? '') > lastFetch)
  ) {
    useDemo = false
    description = t('voiceIncludedDemoSaved')
  } else if (status?.trial_active === false && isCount(balance)) {
    if (balance > 0) {
      useDemo = false
      const balanceLabel = tConversation('freeBalance', {
        duration: formatVoiceDuration(balance, locale),
      })
      description = `${balanceLabel} ${t('voiceFreeDemoSaved')}`
      if (cap && isCount(sessionLimit) && sessionLimit > 0) {
        action = t('voiceFreeAction', {
          duration: formatVoiceDuration(
            Math.min(balance, sessionLimit, cap),
            locale
          ),
        })
      }
    } else {
      // The backend uses the token duration instead of the regular session limit for a demo.
      description =
        cap && isCount(demoSeconds) && demoSeconds > 0
          ? t('voiceDemoOffer', {
              duration: formatVoiceDuration(Math.min(demoSeconds, cap), locale),
            })
          : t('voiceDemoCheck')
    }
  }

  return (
    <>
      <div className="border-fl-border bg-fl-surface-2 border px-4 py-5">
        <p className="text-fl-fg mb-2 font-mono text-base font-bold">
          {t('voiceTrialTitle')}
        </p>
        <p className="text-fl-muted-1 font-mono text-xs leading-relaxed">
          {description}
        </p>
        {cap === 0 && (
          <p className="text-fl-muted-1 mt-2 font-mono text-xs leading-relaxed">
            {t('voiceLimitReached')}
          </p>
        )}
      </div>
      <button
        onClick={() => onOpen(useDemo)}
        className="bg-fl-accent text-fl-accent-fg hover:bg-fl-accent/90 w-full py-3 font-mono text-sm font-bold tracking-widest uppercase transition-colors"
      >
        {action} →
      </button>
    </>
  )
}
