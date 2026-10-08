import { beforeEach, describe, expect, it, vi } from 'vitest'

const apiFetchMock = vi.fn()

vi.mock('@/lib/api', () => ({
  apiFetch: (...args: unknown[]) => apiFetchMock(...args),
}))

import { useFreemiumStore } from '@/store/freemium'
import { useAuthStore } from '@/store/auth'
import { useLanguageStore } from '@/store/language'

const status = {
  trial_active: false,
  trial_ends_at: null,
  chat_remaining: 3,
  chat_limit: 3,
  lessons_remaining: 2,
  lessons_limit: 3,
  listening_remaining: 2,
  listening_limit: 2,
  reading_remaining: 2,
  reading_limit: 2,
  games_remaining: 3,
  games_limit: 3,
  voice_remaining_seconds: 900,
  voice_limit_seconds: 900,
}

describe('freemium store', () => {
  beforeEach(() => {
    apiFetchMock.mockReset()
    useAuthStore.getState().startSession('account-a')
    useFreemiumStore.setState({ status: null, loaded: false, lastFetch: 0 })
  })

  it('uses the cached status during the cache window', async () => {
    useFreemiumStore.setState({ status, loaded: true, lastFetch: Date.now() })

    await useFreemiumStore.getState().fetchStatus()

    expect(apiFetchMock).not.toHaveBeenCalled()
  })

  it.each([
    [0, 2],
    [2, 0],
  ])(
    'requests B quota after logout within A cache TTL (%i → %i)',
    async (a, b) => {
      useAuthStore.getState().startSession('account-a')
      apiFetchMock.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ ...status, listening_remaining: a }),
      })
      await useFreemiumStore.getState().fetchStatus()

      useAuthStore.getState().logout()
      useAuthStore.getState().startSession('account-b')
      apiFetchMock.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ ...status, listening_remaining: b }),
      })
      await useFreemiumStore.getState().fetchStatus()

      expect(apiFetchMock).toHaveBeenCalledTimes(2)
      expect(useFreemiumStore.getState().status?.listening_remaining).toBe(b)
    }
  )

  it.each(['logout', 'replacement', 'expired', 'forced'])(
    'clears the snapshot immediately and keeps it empty through failed recovery (%s)',
    async (transition) => {
      apiFetchMock.mockResolvedValueOnce({ ok: true, json: async () => status })
      await useFreemiumStore.getState().fetchStatus()
      if (transition === 'expired')
        useFreemiumStore.setState({ lastFetch: Date.now() - 60_001 })

      if (transition === 'logout') useAuthStore.getState().logout()
      else useAuthStore.getState().startSession('account-b')
      expect(useFreemiumStore.getState()).toMatchObject({
        status: null,
        loaded: false,
        lastFetch: 0,
      })
      if (transition === 'logout')
        useAuthStore.getState().startSession('account-b')

      let finish!: (response: unknown) => void
      apiFetchMock.mockReturnValueOnce(
        new Promise((resolve) => {
          finish = resolve
        })
      )
      const pending = useFreemiumStore
        .getState()
        .fetchStatus(transition === 'forced')
      expect(apiFetchMock).toHaveBeenCalledTimes(2)
      expect(useFreemiumStore.getState().status).toBeNull()
      finish({ ok: false })
      await pending
      expect(useFreemiumStore.getState()).toMatchObject({
        status: null,
        loaded: false,
      })

      apiFetchMock.mockRejectedValueOnce(new Error('offline'))
      await useFreemiumStore.getState().fetchStatus()
      expect(useFreemiumStore.getState().status).toBeNull()
      apiFetchMock.mockResolvedValueOnce({ ok: true, json: async () => status })
      await useFreemiumStore.getState().fetchStatus()
      expect(useFreemiumStore.getState().status).toEqual(status)
    }
  )

  it.each(['headers', 'body'])(
    'rejects late A results across A → B → A (%s)',
    async (stage) => {
      let finish!: (value: unknown) => void
      const delayed = new Promise((resolve) => {
        finish = resolve
      })
      const json = vi.fn(() =>
        stage === 'body' ? delayed : Promise.resolve(status)
      )
      apiFetchMock.mockReturnValueOnce(
        stage === 'headers' ? delayed : Promise.resolve({ ok: true, json })
      )
      const pending = useFreemiumStore.getState().fetchStatus()
      if (stage === 'body')
        await vi.waitFor(() => expect(json).toHaveBeenCalled())
      useAuthStore.getState().logout()
      useAuthStore.getState().startSession('account-b')
      useAuthStore.getState().startSession('account-a')
      finish(stage === 'headers' ? { ok: true, json } : status)
      await pending
      expect(useFreemiumStore.getState()).toMatchObject({
        status: null,
        loaded: false,
      })

      apiFetchMock.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ ...status, chat_remaining: 0 }),
      })
      await useFreemiumStore.getState().fetchStatus()
      expect(useFreemiumStore.getState().status?.chat_remaining).toBe(0)
    }
  )

  it('preserves global quota cache through token rotation and a language switch', async () => {
    apiFetchMock.mockResolvedValueOnce({ ok: true, json: async () => status })
    await useFreemiumStore.getState().fetchStatus()
    const snapshot = useFreemiumStore.getState().status
    const lastFetch = useFreemiumStore.getState().lastFetch
    useAuthStore.getState().setTokens('rotated-a')
    apiFetchMock.mockResolvedValueOnce({ ok: true }).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        languages: [
          {
            target_language: 'es-ES',
            is_active: true,
            plan: null,
            progress: null,
          },
        ],
        all_supported_languages: ['en-GB', 'es-ES'],
      }),
    })
    expect(await useLanguageStore.getState().switchLanguage('es-ES')).toBe(true)
    await useFreemiumStore.getState().fetchStatus()
    expect(
      apiFetchMock.mock.calls.filter(([url]) => url === '/api/freemium/status')
    ).toHaveLength(1)
    expect(useFreemiumStore.getState().status).toBe(snapshot)
    expect(useFreemiumStore.getState().lastFetch).toBe(lastFetch)
  })

  it('refreshes the status when forced', async () => {
    const refreshed = { ...status, lessons_remaining: 1 }
    useFreemiumStore.setState({ status, loaded: true, lastFetch: Date.now() })
    apiFetchMock.mockResolvedValue({
      ok: true,
      json: vi.fn().mockResolvedValue(refreshed),
    })

    await useFreemiumStore.getState().fetchStatus(true)

    expect(apiFetchMock).toHaveBeenCalledWith('/api/freemium/status')
    expect(useFreemiumStore.getState().status).toEqual(refreshed)
  })

  it('ignores an old session response including delayed body decoding', async () => {
    let finish!: (data: unknown) => void
    const json = vi.fn(
      () =>
        new Promise((resolve) => {
          finish = resolve
        })
    )
    apiFetchMock.mockResolvedValue({ ok: true, json })
    const pending = useFreemiumStore.getState().fetchStatus(true)
    await vi.waitFor(() => expect(json).toHaveBeenCalled())
    useAuthStore.getState().startSession('replacement')
    useFreemiumStore.setState({ status, loaded: true })
    finish({ ...status, reading_remaining: 0 })
    await pending
    expect(useFreemiumStore.getState().status).toEqual(status)
  })

  it('ignores an older quota read after a newer read completes', async () => {
    let finish!: (response: unknown) => void
    apiFetchMock
      .mockReturnValueOnce(
        new Promise((resolve) => {
          finish = resolve
        })
      )
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ ...status, reading_remaining: 0 }),
      })
    const old = useFreemiumStore.getState().fetchStatus(true)
    await useFreemiumStore.getState().fetchStatus(true)
    finish({ ok: true, json: async () => status })
    await old
    expect(useFreemiumStore.getState().status?.reading_remaining).toBe(0)
  })

  it('reconciles again if confirmed consumption overlaps the quota snapshot', async () => {
    useFreemiumStore.setState({ status, loaded: true })
    let finish!: (data: unknown) => void
    const json = vi.fn(
      () =>
        new Promise((resolve) => {
          finish = resolve
        })
    )
    apiFetchMock
      .mockResolvedValueOnce({ ok: true, json })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ ...status, reading_remaining: 0 }),
      })
    const pending = useFreemiumStore.getState().fetchStatus(true)
    await vi.waitFor(() => expect(json).toHaveBeenCalled())
    useFreemiumStore.getState().decrement('reading_remaining')
    finish(status)
    await pending
    expect(useFreemiumStore.getState().status?.reading_remaining).toBe(0)
    expect(apiFetchMock).toHaveBeenCalledTimes(2)
  })

  it('allows a later visit to retry a failed forced reconciliation inside the old cache window', async () => {
    useFreemiumStore.setState({ status, loaded: true, lastFetch: Date.now() })
    apiFetchMock.mockResolvedValueOnce({ ok: false }).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ ...status, reading_remaining: 0 }),
    })
    await useFreemiumStore.getState().fetchStatus(true)
    await useFreemiumStore.getState().fetchStatus()
    expect(apiFetchMock).toHaveBeenCalledTimes(2)
    expect(useFreemiumStore.getState().status?.reading_remaining).toBe(0)
  })
})
