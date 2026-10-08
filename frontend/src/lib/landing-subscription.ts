import { requestAccessToken } from '@/lib/api'
import { useAuthStore } from '@/store/auth'

interface LandingSubscriptionState {
  subscribed: boolean
  trialUsed: boolean
}

let subscriptionStatusPromise: Promise<LandingSubscriptionState> | null = null
let subscriptionSession: number | null = null

export async function getLandingSubscriptionState(): Promise<LandingSubscriptionState> {
  const { sessionVersion } = useAuthStore.getState()
  if (subscriptionStatusPromise && subscriptionSession === sessionVersion)
    return subscriptionStatusPromise
  subscriptionSession = sessionVersion

  const promise = (async () => {
    // An in-memory token can have expired while browsing public pages. Share
    // refresh before /me, without apiFetch's authenticated-page redirect.
    const access_token = await requestAccessToken()
    if (useAuthStore.getState().sessionVersion !== sessionVersion)
      throw new DOMException('Authentication session changed', 'AbortError')

    const meRes = await fetch('/api/auth/me', {
      headers: { Authorization: `Bearer ${access_token}` },
      credentials: 'include',
    })
    if (!meRes.ok) throw new Error('Subscription lookup failed')

    const me = await meRes.json()
    if (useAuthStore.getState().sessionVersion !== sessionVersion)
      throw new DOMException('Authentication session changed', 'AbortError')
    const status: string = me.subscription_status ?? 'none'
    return {
      subscribed: status === 'active' || status === 'trialing',
      trialUsed: Boolean(me.trial_used),
    }
  })().catch(() => {
    // A failed lookup is a temporary fallback, not a cached subscription state.
    if (subscriptionStatusPromise === promise) subscriptionStatusPromise = null
    return { subscribed: false, trialUsed: false }
  })
  subscriptionStatusPromise = promise

  return subscriptionStatusPromise
}

export async function hasActiveLandingSubscription(): Promise<boolean> {
  const state = await getLandingSubscriptionState()
  return state.subscribed
}
