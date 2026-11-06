import { apiFetch } from '@/lib/api'
import type { BillingInterval } from '@/lib/billing-copy'
import { mapUser } from '@/lib/mappers'
import { isSubscribed, useAuthStore } from '@/store/auth'

/** A null destination means the refreshed profile already confirms Premium. */
export async function createCheckout(
  plan: BillingInterval,
  signal: AbortSignal
): Promise<string | null> {
  const { sessionVersion } = useAuthStore.getState()
  const assertCurrent = () => {
    signal.throwIfAborted()
    if (useAuthStore.getState().sessionVersion !== sessionVersion) {
      throw new DOMException('Authentication session changed', 'AbortError')
    }
  }
  assertCurrent()
  const response = await apiFetch('/api/billing/checkout', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ plan }),
    signal,
  })
  assertCurrent()
  if (response.status === 409) {
    const conflict = await response.json()
    assertCurrent()
    if (conflict?.detail === 'subscription_already_active') {
      const profile = await apiFetch('/api/auth/me', { signal })
      assertCurrent()
      if (!profile.ok) throw new Error('Subscription profile refresh failed')
      const data = await profile.json()
      assertCurrent()
      const user = mapUser(data)
      useAuthStore.getState().setUser(user)
      if (isSubscribed(user, true)) return null
    }
  }
  if (!response.ok) throw new Error('Checkout failed')
  const { url } = await response.json()
  assertCurrent()
  return url
}
