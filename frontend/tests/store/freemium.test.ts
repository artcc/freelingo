import { beforeEach, describe, expect, it, vi } from 'vitest'

const apiFetchMock = vi.fn()

vi.mock('@/lib/api', () => ({
  apiFetch: (...args: unknown[]) => apiFetchMock(...args),
}))

import { useFreemiumStore } from '@/store/freemium'
import { useAuthStore } from '@/store/auth'

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
    useFreemiumStore.setState({ status: null, loaded: false, lastFetch: 0 })
  })

  it('uses the cached status during the cache window', async () => {
    useFreemiumStore.setState({ status, loaded: true, lastFetch: Date.now() })

    await useFreemiumStore.getState().fetchStatus()

    expect(apiFetchMock).not.toHaveBeenCalled()
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
    apiFetchMock
      .mockResolvedValueOnce({ ok: false })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ ...status, reading_remaining: 0 }),
      })
    await useFreemiumStore.getState().fetchStatus(true)
    await useFreemiumStore.getState().fetchStatus()
    expect(apiFetchMock).toHaveBeenCalledTimes(2)
    expect(useFreemiumStore.getState().status?.reading_remaining).toBe(0)
  })
})
