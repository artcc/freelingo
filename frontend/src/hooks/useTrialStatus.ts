'use client'

import { useEffect, useState } from 'react'
import { useAuthStore, isSubscribed } from '@/store/auth'
import { useConfigStore } from '@/store/config'

const DAY_MS = 86_400_000

export function useTrialStatus() {
  const user = useAuthStore((s) => s.user)
  const stripeEnabled = useConfigStore((s) => s.stripeEnabled)
  const freemiumTrialEnabled = useConfigStore((s) => s.freemiumTrialEnabled)
  const [now, setNow] = useState(Date.now)
  const freemiumEnd =
    stripeEnabled && freemiumTrialEnabled
      ? Date.parse(user?.freemium_trial_ends_at ?? '')
      : NaN
  const subscriptionEnd =
    stripeEnabled && user?.subscription_status === 'trialing'
      ? Date.parse(user.subscription_ends_at ?? '')
      : NaN

  useEffect(() => {
    let timer: ReturnType<typeof setTimeout> | undefined
    function update() {
      clearTimeout(timer)
      const time = Date.now()
      setNow(time)
      const delays = [freemiumEnd, subscriptionEnd]
        .filter((end) => Number.isFinite(end) && end > time)
        .map((end) => {
          const remaining = end - time
          return remaining - (Math.ceil(remaining / DAY_MS) - 1) * DAY_MS
        })
      if (delays.length) timer = setTimeout(update, Math.min(...delays))
    }
    function onVisible() {
      if (document.visibilityState === 'visible') update()
    }
    update()
    window.addEventListener('focus', update)
    document.addEventListener('visibilitychange', onVisible)
    return () => {
      clearTimeout(timer)
      window.removeEventListener('focus', update)
      document.removeEventListener('visibilitychange', onVisible)
    }
  }, [freemiumEnd, subscriptionEnd])

  const freemiumTrialDaysLeft = Number.isFinite(freemiumEnd)
    ? Math.max(0, Math.ceil((freemiumEnd - now) / DAY_MS))
    : 0
  const subscriptionTrialDaysLeft = Number.isFinite(subscriptionEnd)
    ? Math.max(0, Math.ceil((subscriptionEnd - now) / DAY_MS))
    : 0

  return {
    freemiumTrialActive: freemiumTrialDaysLeft > 0,
    freemiumTrialDaysLeft,
    trialDaysLeft: isSubscribed(user, stripeEnabled)
      ? subscriptionTrialDaysLeft
      : freemiumTrialDaysLeft,
  }
}
