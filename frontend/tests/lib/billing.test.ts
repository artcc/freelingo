import { beforeEach, describe, expect, it, vi } from 'vitest'
import { createCheckout } from '@/lib/billing'
import { useAuthStore } from '@/store/auth'

const { mockApiFetch } = vi.hoisted(() => ({ mockApiFetch: vi.fn() }))
vi.mock('@/lib/api', () => ({ apiFetch: mockApiFetch }))

const activeProfile = {
  id: 1,
  username: 'learner',
  display_name: 'Learner',
  role: 'user',
  subscription_status: 'active',
}

function response(data: unknown, status = 200) {
  return new Response(JSON.stringify(data), { status })
}

function alreadyActive() {
  return response({ detail: 'subscription_already_active' }, 409)
}

beforeEach(() => {
  mockApiFetch.mockReset()
  useAuthStore.getState().startSession('token')
})

describe('checkout recovery', () => {
  it('returns the Checkout destination without requesting a profile', async () => {
    mockApiFetch.mockResolvedValueOnce(
      response({ url: 'https://checkout.stripe.com/session' })
    )
    await expect(
      createCheckout('monthly', new AbortController().signal)
    ).resolves.toBe('https://checkout.stripe.com/session')
    expect(mockApiFetch).toHaveBeenCalledTimes(1)
  })

  it.each(['active', 'trialing'])(
    'recovers an already-active conflict only after confirming %s',
    async (status) => {
      mockApiFetch
        .mockResolvedValueOnce(alreadyActive())
        .mockResolvedValueOnce(
          response({ ...activeProfile, subscription_status: status })
        )
      await expect(
        createCheckout('yearly', new AbortController().signal)
      ).resolves.toBeNull()
      expect(useAuthStore.getState().user?.subscription_status).toBe(status)
    }
  )

  it('does not treat a pending payment as an active subscription', async () => {
    mockApiFetch.mockResolvedValueOnce(
      response({ detail: 'subscription_payment_pending' }, 409)
    )
    await expect(
      createCheckout('monthly', new AbortController().signal)
    ).rejects.toThrow('Checkout failed')
    expect(mockApiFetch).toHaveBeenCalledTimes(1)
    expect(useAuthStore.getState().user).toBeNull()
  })

  it.each([503, 401])('does not claim Premium after a failed profile read (%s)', async (status) => {
    mockApiFetch
      .mockResolvedValueOnce(alreadyActive())
      .mockResolvedValueOnce(response({}, status))
    await expect(
      createCheckout('monthly', new AbortController().signal)
    ).rejects.toThrow('Subscription profile refresh failed')
    expect(useAuthStore.getState().user).toBeNull()
  })

  it('does not claim Premium when the refreshed profile is still unsubscribed', async () => {
    mockApiFetch
      .mockResolvedValueOnce(alreadyActive())
      .mockResolvedValueOnce(
        response({ ...activeProfile, subscription_status: 'none' })
      )
    await expect(
      createCheckout('monthly', new AbortController().signal)
    ).rejects.toThrow('Checkout failed')
    expect(useAuthStore.getState().user?.subscription_status).toBe('none')
  })

  it.each(['session', 'abort'])(
    'ignores a profile whose body finishes after %s invalidation',
    async (invalidation) => {
      let finish!: (data: unknown) => void
      const body = new Promise((resolve) => {
        finish = resolve
      })
      const json = vi.fn(() => body)
      mockApiFetch
        .mockResolvedValueOnce(alreadyActive())
        .mockResolvedValueOnce({ ok: true, json })
      const controller = new AbortController()
      const pending = createCheckout('monthly', controller.signal)
      const rejected = expect(pending).rejects.toMatchObject({ name: 'AbortError' })
      await vi.waitFor(() => expect(json).toHaveBeenCalledOnce())
      if (invalidation === 'session') {
        useAuthStore.getState().startSession('other-account')
      } else {
        controller.abort()
      }
      finish(activeProfile)
      await rejected
      expect(useAuthStore.getState().user).toBeNull()
    }
  )

  it('does not reload a profile for a checkout completed in an old session', async () => {
    let finish!: (value: Response) => void
    mockApiFetch.mockReturnValueOnce(
      new Promise<Response>((resolve) => {
        finish = resolve
      })
    )
    const pending = createCheckout('monthly', new AbortController().signal)
    const rejected = expect(pending).rejects.toMatchObject({ name: 'AbortError' })
    useAuthStore.getState().startSession('other-account')
    finish(alreadyActive())
    await rejected
    expect(mockApiFetch).toHaveBeenCalledTimes(1)
  })
})
