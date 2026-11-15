'use client'

import { useCallback, useEffect, useRef, useState } from 'react'
import { isFreemiumTrialActive, isSubscribed, useAuthStore } from '@/store/auth'
import { useConfigStore } from '@/store/config'
import { useFreemiumStore } from '@/store/freemium'

type Feature = 'chat' | 'lessons' | 'listening' | 'reading' | 'games' | 'voice'

export function getFreemiumAccessFailure(
  status: number,
  body: unknown,
  feature: Feature
): 'exhausted' | 'unavailable' | null {
  if (status !== 402 || !body || typeof body !== 'object') return null
  const detail = (body as { detail?: unknown }).detail
  if (detail === 'subscription_required') return 'exhausted'
  if (!detail || typeof detail !== 'object') return null
  const value = detail as { reason?: unknown; feature?: unknown }
  if (value.feature !== feature) return null
  if (value.reason === 'freemium_exhausted') return 'exhausted'
  if (value.reason === 'freemium_unavailable') return 'unavailable'
  return null
}

/** Keep a confirmed denial visible even if the advisory quota refresh fails. */
export function useFreemiumAccessRecovery(feature: Feature) {
  const sessionVersion = useAuthStore((s) => s.sessionVersion)
  const userId = useAuthStore((s) => s.user?.id)
  const stripeEnabled = useConfigStore((s) => s.stripeEnabled)
  const [deniedFor, setDeniedFor] = useState<{
    feature: Feature
    sessionVersion: number
    userId: number | undefined
  } | null>(null)
  const denial = useRef<{
    feature: Feature
    sessionVersion: number
    user: ReturnType<typeof useAuthStore.getState>['user']
    status: ReturnType<typeof useFreemiumStore.getState>['status']
    freemiumTrialEnabled: boolean
  } | null>(null)
  const reconcile = useCallback(() => {
    const rejected = denial.current
    if (!rejected) return
    const { user, sessionVersion } = useAuthStore.getState()
    const { stripeEnabled, freemiumTrialEnabled } = useConfigStore.getState()
    const { status, lastFetch } = useFreemiumStore.getState()
    const remainingKey =
      feature === 'voice'
        ? 'voice_remaining_seconds'
        : (`${feature}_remaining` as const)
    const remaining = status?.[remainingKey]
    const quotaRecovered =
      status !== rejected.status &&
      lastFetch > 0 &&
      status !== null &&
      (status.trial_active || (remaining !== undefined && remaining > 0))
    const profileRecovered =
      (user?.subscription_status !== rejected.user?.subscription_status &&
        isSubscribed(user, true)) ||
      ((user?.freemium_trial_ends_at !==
        rejected.user?.freemium_trial_ends_at ||
        (!rejected.freemiumTrialEnabled && freemiumTrialEnabled)) &&
        isFreemiumTrialActive(user, true))
    if (
      rejected.feature !== feature ||
      rejected.sessionVersion !== sessionVersion ||
      rejected.user?.id !== user?.id ||
      !stripeEnabled ||
      quotaRecovered ||
      profileRecovered
    ) {
      // Retire this denial on the confirming store event, even if another forced
      // read invalidates the cache before React renders the recovered snapshot.
      denial.current = null
      setDeniedFor(null)
    } else {
      rejected.freemiumTrialEnabled = freemiumTrialEnabled
    }
  }, [feature])
  useEffect(() => {
    const unsubscribe = [
      useAuthStore.subscribe(reconcile),
      useConfigStore.subscribe(reconcile),
      useFreemiumStore.subscribe(reconcile),
    ]
    reconcile()
    return () => unsubscribe.forEach((stop) => stop())
  }, [reconcile])
  const reportAccessDenied = useCallback(() => {
    const config = useConfigStore.getState()
    if (!config.stripeEnabled) return
    const auth = useAuthStore.getState()
    denial.current = {
      feature,
      sessionVersion: auth.sessionVersion,
      user: auth.user,
      status: useFreemiumStore.getState().status,
      freemiumTrialEnabled: config.freemiumTrialEnabled,
    }
    setDeniedFor({
      feature,
      sessionVersion: auth.sessionVersion,
      userId: auth.user?.id,
    })
    void useFreemiumStore.getState().fetchStatus(true)
  }, [feature])
  return {
    accessDenied:
      stripeEnabled &&
      deniedFor !== null &&
      deniedFor.feature === feature &&
      deniedFor.sessionVersion === sessionVersion &&
      deniedFor.userId === userId,
    reportAccessDenied,
  }
}
