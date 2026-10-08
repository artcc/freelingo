import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import {
  clearAvatarCache,
  loadAvatar,
  subscribeAvatar,
} from '@/lib/avatar-cache'
import { apiFetch } from '@/lib/api'
import { useAuthStore } from '@/store/auth'

function deferred() {
  let resolve!: (response: Response) => void
  const promise = new Promise<Response>((done) => {
    resolve = done
  })
  return { promise, resolve }
}

beforeEach(() => {
  vi.stubGlobal('fetch', vi.fn())
  vi.stubGlobal('URL', {
    createObjectURL: vi.fn(() => 'blob:avatar'),
    revokeObjectURL: vi.fn(),
  })
  clearAvatarCache()
  useAuthStore.getState().startSession('old-token')
})

afterEach(() => {
  clearAvatarCache()
  vi.unstubAllGlobals()
})

describe('avatar session isolation', () => {
  it('discards a delayed avatar refresh after a new login', async () => {
    const refresh = deferred()
    vi.mocked(fetch)
      .mockResolvedValueOnce(new Response(null, { status: 401 }))
      .mockReturnValueOnce(refresh.promise)
      .mockResolvedValueOnce(new Response('new-avatar'))
    const old = loadAvatar('/old-avatar', 'old-token')
    await vi.waitFor(() => expect(fetch).toHaveBeenCalledTimes(2))
    useAuthStore.getState().startSession('new-token')
    const publish = vi.fn()
    const unsubscribe = subscribeAvatar(publish)
    expect(await loadAvatar('/new-avatar', 'new-token')).toBe('blob:avatar')
    const publications = publish.mock.calls.length
    refresh.resolve(
      new Response(JSON.stringify({ access_token: 'obsolete-token' }))
    )
    expect(await old).toBeNull()
    expect(useAuthStore.getState().accessToken).toBe('new-token')
    expect(publish).toHaveBeenCalledTimes(publications)
    expect(fetch).toHaveBeenCalledTimes(3)
    unsubscribe()
  })

  it('shares rotation with API recovery and retries with the rotated token', async () => {
    const refresh = deferred()
    vi.mocked(fetch).mockImplementation(async (url, options) => {
      if (url === '/api/auth/refresh') return refresh.promise
      const token = new Headers(options?.headers).get('Authorization')
      return token === 'Bearer rotated'
        ? new Response('ok')
        : new Response(null, { status: 401 })
    })
    const avatar = loadAvatar('/avatar', 'old-token')
    const resource = apiFetch('/api/resource')
    await vi.waitFor(() =>
      expect(
        vi
          .mocked(fetch)
          .mock.calls.filter(([url]) => url === '/api/auth/refresh')
      ).toHaveLength(1)
    )
    refresh.resolve(new Response(JSON.stringify({ access_token: 'rotated' })))
    expect(await avatar).toBe('blob:avatar')
    expect((await resource).ok).toBe(true)
    expect(useAuthStore.getState().accessToken).toBe('rotated')
    expect(
      vi.mocked(fetch).mock.calls.filter(([url]) => url === '/api/auth/refresh')
    ).toHaveLength(1)
  })

  it('does not clear a newer pending avatar when an old request finishes', async () => {
    const oldResponse = deferred()
    const newResponse = deferred()
    vi.mocked(fetch)
      .mockReturnValueOnce(oldResponse.promise)
      .mockReturnValueOnce(newResponse.promise)
    const old = loadAvatar('/avatar', 'old-token')
    useAuthStore.getState().startSession('new-token')
    const current = loadAvatar('/avatar', 'new-token')
    oldResponse.resolve(new Response('obsolete'))
    expect(await old).toBeNull()
    expect(loadAvatar('/avatar', 'new-token')).toBe(current)
    expect(fetch).toHaveBeenCalledTimes(2)
    newResponse.resolve(new Response('current'))
    expect(await current).toBe('blob:avatar')
  })

  it('keeps avatar failure non-fatal when renewal is rejected', async () => {
    vi.mocked(fetch).mockResolvedValue(new Response(null, { status: 401 }))
    expect(await loadAvatar('/avatar', 'old-token')).toBeNull()
    expect(useAuthStore.getState().accessToken).toBe('old-token')
  })
})
