import { requestAccessToken } from '@/lib/api'
import { useAuthStore } from '@/store/auth'

interface LandingSubscriptionState {
  subscribed: boolean
  trialUsed: boolean
}

let subscriptionStatusPromise: Promise<LandingSubscriptionState> | null = null
let subscriptionSession: number | null = null

export async function getLandingSubscriptionState(): Promise<LandingSubscriptionState> {
  const { sessionVersion, accessToken } = useAuthStore.getState()
  if (subscriptionStatusPromise && subscriptionSession === sessionVersion)
    return subscriptionStatusPromise
  subscriptionSession = sessionVersion

  subscriptionStatusPromise = (async () => {
    try {
      const access_token = accessToken ?? (await requestAccessToken())
      if (useAuthStore.getState().sessionVersion !== sessionVersion)
        return { subscribed: false, trialUsed: false }

      const meRes = await fetch('/api/auth/me', {
        headers: { Authorization: `Bearer ${access_token}` },
        credentials: 'include',
      })
      if (!meRes.ok) return { subscribed: false, trialUsed: false }

      const me = await meRes.json()
      if (useAuthStore.getState().sessionVersion !== sessionVersion)
        return { subscribed: false, trialUsed: false }
      const status: string = me.subscription_status ?? 'none'
      return {
        subscribed: status === 'active' || status === 'trialing',
        trialUsed: Boolean(me.trial_used),
      }
    } catch {
      return { subscribed: false, trialUsed: false }
    }
  })()

  return subscriptionStatusPromise
}

export async function hasActiveLandingSubscription(): Promise<boolean> {
  const state = await getLandingSubscriptionState()
  return state.subscribed
}
