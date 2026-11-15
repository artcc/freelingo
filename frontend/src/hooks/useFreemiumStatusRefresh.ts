'use client'

import { useEffect, useRef } from 'react'
import { useAuthStore, isSubscribed } from '@/store/auth'
import { useConfigStore } from '@/store/config'
import { useFreemiumStore } from '@/store/freemium'

const DAY_MS = 86_400_000

/** Refresh only at quota/trial boundaries and when returning to a stale tab. */
export function useFreemiumStatusRefresh(ready: boolean) {
  const user = useAuthStore((s) => s.user)
  const sessionVersion = useAuthStore((s) => s.sessionVersion)
  const stripeEnabled = useConfigStore((s) => s.stripeEnabled)
  const freemiumTrialEnabled = useConfigStore((s) => s.freemiumTrialEnabled)
  const enabled = ready && !!user && !isSubscribed(user, stripeEnabled)
  const trialEndsAt = user?.freemium_trial_ends_at
  const previousTrialEnabled = useRef(freemiumTrialEnabled)

  useEffect(() => {
    const configChanged = previousTrialEnabled.current !== freemiumTrialEnabled
    previousTrialEnabled.current = freemiumTrialEnabled
    if (!enabled) return
    let timer: ReturnType<typeof setTimeout> | undefined
    let pendingBoundary = configChanged
    const trialEnd = freemiumTrialEnabled ? Date.parse(trialEndsAt ?? '') : NaN

    function refresh(force = false) {
      pendingBoundary ||= force
      const auth = useAuthStore.getState()
      if (
        auth.sessionVersion !== sessionVersion ||
        !auth.accessToken ||
        document.visibilityState !== 'visible'
      )
        return
      void useFreemiumStore.getState().fetchStatus(pendingBoundary)
      pendingBoundary = false
    }
    function schedule() {
      clearTimeout(timer)
      const now = Date.now()
      const midnight = (Math.floor(now / DAY_MS) + 1) * DAY_MS
      const next = trialEnd > now ? Math.min(midnight, trialEnd) : midnight
      timer = setTimeout(() => {
        refresh(true)
        schedule()
      }, next - now)
    }
    function onFocus() {
      refresh()
      schedule()
    }
    refresh(configChanged)
    schedule()
    window.addEventListener('focus', onFocus)
    document.addEventListener('visibilitychange', onFocus)
    return () => {
      clearTimeout(timer)
      window.removeEventListener('focus', onFocus)
      document.removeEventListener('visibilitychange', onFocus)
    }
  }, [enabled, sessionVersion, freemiumTrialEnabled, trialEndsAt])
}
