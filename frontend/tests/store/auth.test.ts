import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import {
  isSubscribed,
  isFreemiumTrialActive,
  useAuthStore,
  type User,
} from '@/store/auth'
import { useConfigStore } from '@/store/config'

describe('isSubscribed', () => {
  const baseUser: User = {
    id: 1,
    username: 'test',
    displayName: 'Test',
    role: 'user',
    conversation_max_duration: 300,
    conversation_inactivity_timeout: 30,
  }

  it('returns true when Stripe is disabled (self-hosted)', () => {
    expect(isSubscribed(null, false)).toBe(true)
    expect(isSubscribed(baseUser, false)).toBe(true)
  })

  it('returns false when Stripe is enabled and user is null', () => {
    expect(isSubscribed(null, true)).toBe(false)
  })

  it('returns true for active subscription', () => {
    const user = { ...baseUser, subscription_status: 'active' as const }
    expect(isSubscribed(user, true)).toBe(true)
  })

  it('returns true for trialing subscription', () => {
    const user = { ...baseUser, subscription_status: 'trialing' as const }
    expect(isSubscribed(user, true)).toBe(true)
  })

  it('returns false for past_due subscription', () => {
    const user = { ...baseUser, subscription_status: 'past_due' as const }
    expect(isSubscribed(user, true)).toBe(false)
  })

  it('returns false for canceled subscription', () => {
    const user = { ...baseUser, subscription_status: 'canceled' as const }
    expect(isSubscribed(user, true)).toBe(false)
  })

  it('returns false for none subscription', () => {
    const user = { ...baseUser, subscription_status: 'none' as const }
    expect(isSubscribed(user, true)).toBe(false)
  })

  it('returns false when subscription_status is undefined', () => {
    expect(isSubscribed(baseUser, true)).toBe(false)
  })
})

describe('freemium trial expiration', () => {
  afterEach(() => vi.useRealTimers())

  it.each(['2030-01-01T12:00:00+00:00', '2030-07-01T12:00:00+00:00'])(
    'uses the exact UTC instant for %s',
    (expiration) => {
      useConfigStore.setState({ freemiumTrialEnabled: true })
      vi.useFakeTimers()
      const user: User = {
        id: 1,
        username: 'learner',
        displayName: 'Learner',
        role: 'user',
        conversation_max_duration: 1800,
        conversation_inactivity_timeout: 180,
        freemium_trial_ends_at: expiration,
      }
      const expiresAt = Date.parse(expiration.replace('+00:00', 'Z'))
      vi.setSystemTime(expiresAt - 3600_000)
      expect(isFreemiumTrialActive(user, true)).toBe(true)
      vi.setSystemTime(expiresAt)
      expect(isFreemiumTrialActive(user, true)).toBe(false)
      vi.setSystemTime(expiresAt + 3600_000)
      expect(isFreemiumTrialActive(user, true)).toBe(false)
    }
  )
})

describe('useAuthStore', () => {
  beforeEach(() => {
    useAuthStore.setState({ accessToken: null, user: null })
    localStorage.clear()
  })

  it('setTokens updates accessToken', () => {
    const version = useAuthStore.getState().sessionVersion
    useAuthStore.getState().setTokens('abc123')
    expect(useAuthStore.getState().accessToken).toBe('abc123')
    expect(useAuthStore.getState().sessionVersion).toBe(version)
  })

  it('advances session identity on login and logout, even with the same token', () => {
    const version = useAuthStore.getState().sessionVersion
    useAuthStore.getState().startSession('same-token')
    useAuthStore.getState().startSession('same-token')
    expect(useAuthStore.getState().sessionVersion).toBe(version + 2)
    useAuthStore.getState().logout()
    expect(useAuthStore.getState().sessionVersion).toBe(version + 3)
  })

  it('setUser updates user', () => {
    const user: User = {
      id: 1,
      username: 'test',
      displayName: 'Test',
      role: 'user',
      conversation_max_duration: 300,
      conversation_inactivity_timeout: 30,
    }
    useAuthStore.getState().setUser(user)
    expect(useAuthStore.getState().user).toEqual(user)
  })

  it('updates the dismissed dashboard banner revision on the current user', () => {
    useAuthStore.setState({ user: { id: 1 } as User })

    useAuthStore.getState().setDismissedDashboardBannerRevision(8)

    expect(
      useAuthStore.getState().user?.dismissed_dashboard_banner_revision
    ).toBe(8)
  })

  it('logout clears token, user, and the current tour completion flag', () => {
    useAuthStore.setState({ accessToken: 'token', user: { id: 1 } as User })
    localStorage.setItem('fl_tour_done_v2', 'true')

    useAuthStore.getState().logout()

    expect(useAuthStore.getState().accessToken).toBeNull()
    expect(useAuthStore.getState().user).toBeNull()
    expect(localStorage.getItem('fl_tour_done_v2')).toBeNull()
  })
})
