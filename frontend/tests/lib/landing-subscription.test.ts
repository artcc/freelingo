import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import {
  getLandingSubscriptionState,
  hasActiveLandingSubscription,
} from '@/lib/landing-subscription'
import { requestAccessToken } from '@/lib/api'
import { useAuthStore } from '@/store/auth'

const json = (data: unknown, status = 200) =>
  new Response(JSON.stringify(data), { status })

beforeEach(() => {
  vi.stubGlobal('fetch', vi.fn())
  useAuthStore.getState().startSession('expired-token')
})
afterEach(() => vi.unstubAllGlobals())

describe('landing subscription authentication', () => {
  it.each(['expired-token', null])(
    'recognizes a subscriber with initial token %s',
    async (accessToken) => {
      useAuthStore.setState({ accessToken })
      vi.mocked(fetch).mockImplementation(async (url, options) => {
        if (url === '/api/auth/refresh')
          return json({ access_token: 'fresh-token' })
        if (url === '/api/auth/me') {
          return new Headers(options?.headers).get('Authorization') ===
            'Bearer fresh-token'
            ? json({ subscription_status: 'active', trial_used: true })
            : json({}, 401)
        }
        return json({}, 404)
      })
      expect(await getLandingSubscriptionState()).toEqual({
        subscribed: true,
        trialUsed: true,
      })
      expect(await hasActiveLandingSubscription()).toBe(true)
      expect(fetch).toHaveBeenCalledTimes(2)
      expect(fetch).toHaveBeenNthCalledWith(1, '/api/auth/refresh', {
        method: 'POST',
        credentials: 'include',
      })
      expect(fetch).toHaveBeenNthCalledWith(2, '/api/auth/me', {
        headers: { Authorization: 'Bearer fresh-token' },
        credentials: 'include',
      })
    }
  )

  it('shares pending HTTP renewal with other authentication consumers', async () => {
    let finish!: (response: Response) => void
    vi.mocked(fetch)
      .mockReturnValueOnce(
        new Promise((resolve) => {
          finish = resolve
        })
      )
      .mockResolvedValueOnce(json({ subscription_status: 'trialing' }))
    const restoration = requestAccessToken()
    const pricing = getLandingSubscriptionState()
    const navigation = hasActiveLandingSubscription()
    expect(fetch).toHaveBeenCalledTimes(1)
    finish(json({ access_token: 'fresh-token' }))
    expect(await restoration).toBe('fresh-token')
    expect(await pricing).toMatchObject({ subscribed: true })
    expect(await navigation).toBe(true)
    expect(fetch).toHaveBeenCalledTimes(2)
  })

  it.each(['refresh', 'me-401', 'me-503', 'network'])(
    'does not cache %s failure or log out the public-page visitor',
    async (failure) => {
      const { sessionVersion } = useAuthStore.getState()
      if (failure === 'network')
        vi.mocked(fetch).mockRejectedValueOnce(new TypeError('Offline'))
      else if (failure === 'refresh')
        vi.mocked(fetch).mockResolvedValueOnce(json({}, 401))
      else
        vi.mocked(fetch)
          .mockResolvedValueOnce(json({ access_token: 'fresh-token' }))
          .mockResolvedValueOnce(json({}, failure === 'me-401' ? 401 : 503))
      expect(await getLandingSubscriptionState()).toEqual({
        subscribed: false,
        trialUsed: false,
      })
      expect(useAuthStore.getState()).toMatchObject({
        sessionVersion,
        accessToken: 'expired-token',
      })
      vi.mocked(fetch)
        .mockResolvedValueOnce(json({ access_token: 'fresh-token-2' }))
        .mockResolvedValueOnce(
          json({ subscription_status: 'active', trial_used: true })
        )
      expect(await getLandingSubscriptionState()).toEqual({
        subscribed: true,
        trialUsed: true,
      })
      expect(useAuthStore.getState().sessionVersion).toBe(sessionVersion)
    }
  )

  it('does not replace or clear a newer session cache when an old body completes', async () => {
    let finish!: (data: unknown) => void
    const response = json({})
    const readBody = vi.spyOn(response, 'json').mockReturnValue(
      new Promise((resolve) => {
        finish = resolve
      })
    )
    vi.mocked(fetch)
      .mockResolvedValueOnce(json({ access_token: 'first-token' }))
      .mockResolvedValueOnce(response)
    const old = getLandingSubscriptionState()
    await vi.waitFor(() => expect(readBody).toHaveBeenCalled())
    useAuthStore.getState().startSession('second-token')
    vi.mocked(fetch)
      .mockResolvedValueOnce(json({ access_token: 'second-fresh-token' }))
      .mockResolvedValueOnce(json({ subscription_status: 'active' }))
    expect(await hasActiveLandingSubscription()).toBe(true)
    finish({ subscription_status: 'none' })
    expect(await old).toEqual({ subscribed: false, trialUsed: false })
    expect(await hasActiveLandingSubscription()).toBe(true)
    expect(fetch).toHaveBeenCalledTimes(4)
    expect(useAuthStore.getState().accessToken).toBe('second-token')
  })

  it('caches a successfully authenticated non-subscriber', async () => {
    vi.mocked(fetch)
      .mockResolvedValueOnce(json({ access_token: 'fresh-token' }))
      .mockResolvedValueOnce(
        json({ subscription_status: 'none', trial_used: true })
      )
    expect(await getLandingSubscriptionState()).toEqual({
      subscribed: false,
      trialUsed: true,
    })
    expect(await getLandingSubscriptionState()).toEqual({
      subscribed: false,
      trialUsed: true,
    })
    expect(fetch).toHaveBeenCalledTimes(2)
  })
})
