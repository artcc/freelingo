import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { apiFetch, requestAccessToken, restoreAccessToken } from '@/lib/api'
import { useAuthStore } from '@/store/auth'
import { useLoadingStore } from '@/store/loading'

function deferredResponse() {
  let resolve!: (response: Response) => void
  const promise = new Promise<Response>((done) => {
    resolve = done
  })
  return { promise, resolve }
}

function tokenResponse(token: string) {
  return new Response(JSON.stringify({ access_token: token }))
}

describe('apiFetch', () => {
  it('does not publish restoration into a replaced session', async () => {
    const pending = deferredResponse()
    vi.mocked(fetch).mockReturnValueOnce(pending.promise)
    const restoration = restoreAccessToken()
    const rejected = expect(restoration).rejects.toMatchObject({
      name: 'AbortError',
    })
    useAuthStore.getState().startSession('new-session')
    pending.resolve(tokenResponse('old-session'))
    await rejected
    expect(useAuthStore.getState().accessToken).toBe('new-session')
  })

  it('cancels a restoration consumer without cancelling shared restoration', async () => {
    const pending = deferredResponse()
    vi.mocked(fetch).mockReturnValueOnce(pending.promise)
    const controller = new AbortController()
    const cancelled = restoreAccessToken(controller.signal)
    const rejected = expect(cancelled).rejects.toMatchObject({
      name: 'AbortError',
    })
    const current = restoreAccessToken()
    controller.abort()
    pending.resolve(tokenResponse('restored'))
    await rejected
    expect(await current).toBe('restored')
    expect(useAuthStore.getState().accessToken).toBe('restored')
    expect(fetch).toHaveBeenCalledTimes(1)
  })
  const originalFetch = global.fetch

  beforeEach(() => {
    useAuthStore.setState({ accessToken: null, user: null })
    useLoadingStore.setState({ count: 0 })
    vi.stubGlobal('fetch', vi.fn())
  })

  afterEach(() => {
    global.fetch = originalFetch
    vi.unstubAllGlobals()
  })

  it('attaches Bearer token when accessToken is set', async () => {
    useAuthStore.setState({ accessToken: 'test-token' })
    vi.mocked(fetch).mockResolvedValueOnce(new Response('ok', { status: 200 }))

    await apiFetch('/api/test')

    expect(fetch).toHaveBeenCalledWith(
      '/api/test',
      expect.objectContaining({
        headers: expect.objectContaining({
          Authorization: 'Bearer test-token',
        }),
        credentials: 'include',
      })
    )
  })

  it('does not attach Authorization header when no token', async () => {
    vi.mocked(fetch).mockResolvedValueOnce(new Response('ok', { status: 200 }))

    await apiFetch('/api/test')

    const callArgs = vi.mocked(fetch).mock.calls[0]
    const headers = callArgs[1]?.headers as Record<string, string>
    expect(headers.Authorization).toBeUndefined()
  })

  it('retries with new token on 401', async () => {
    useAuthStore.setState({ accessToken: 'old-token' })

    vi.mocked(fetch)
      .mockResolvedValueOnce(new Response('unauthorized', { status: 401 }))
      .mockResolvedValueOnce(
        new Response(JSON.stringify({ access_token: 'new-token' }), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        })
      )
      .mockResolvedValueOnce(new Response('ok', { status: 200 }))

    const res = await apiFetch('/api/test')

    expect(fetch).toHaveBeenCalledTimes(3)
    expect(res.status).toBe(200)
    expect(useAuthStore.getState().accessToken).toBe('new-token')
  })

  it('calls logout and redirects on refresh failure', async () => {
    useAuthStore.setState({ accessToken: 'old-token' })
    window.history.pushState({}, '', '/login')

    vi.mocked(fetch)
      .mockResolvedValueOnce(new Response('unauthorized', { status: 401 }))
      .mockResolvedValueOnce(new Response('refresh failed', { status: 401 }))

    const res = await apiFetch('/api/test')

    expect(useAuthStore.getState().accessToken).toBeNull()
    expect(useAuthStore.getState().user).toBeNull()
    expect(res.status).toBe(401)
  })

  it('deduplicates concurrent refresh calls', async () => {
    useAuthStore.setState({ accessToken: 'old-token' })

    let refreshCallCount = 0
    vi.mocked(fetch).mockImplementation(async (url: any) => {
      const urlStr = typeof url === 'string' ? url : url.toString()
      if (urlStr.includes('/api/auth/refresh')) {
        refreshCallCount++
        return new Response(JSON.stringify({ access_token: 'new-token' }), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        })
      }
      return new Response('unauthorized', { status: 401 })
    })

    await Promise.all([apiFetch('/api/test1'), apiFetch('/api/test2')])

    expect(refreshCallCount).toBe(1)
  })

  it('ignores a late 401 from a previous session, even if its token string is reused', async () => {
    useAuthStore.getState().startSession('same-token')
    const pending = deferredResponse()
    vi.mocked(fetch).mockReturnValueOnce(pending.promise)
    const request = apiFetch('/api/auth/me')
    const rejected = expect(request).rejects.toMatchObject({
      name: 'AbortError',
    })
    useAuthStore.getState().startSession('same-token')
    pending.resolve(new Response(null, { status: 401 }))
    await rejected
    expect(fetch).toHaveBeenCalledTimes(1)
    expect(useAuthStore.getState().accessToken).toBe('same-token')
  })

  it.each([200, 401])(
    'does not apply a refresh response (%s) to a later session',
    async (status) => {
      useAuthStore.getState().startSession('old-token')
      const pending = deferredResponse()
      vi.mocked(fetch)
        .mockResolvedValueOnce(new Response(null, { status: 401 }))
        .mockReturnValueOnce(pending.promise)
      const request = apiFetch('/api/auth/me')
      const rejected = expect(request).rejects.toMatchObject({
        name: 'AbortError',
      })
      await vi.waitFor(() => expect(fetch).toHaveBeenCalledTimes(2))
      const logout = vi.spyOn(useAuthStore.getState(), 'logout')
      useAuthStore.getState().startSession('current-token')
      pending.resolve(
        status === 200
          ? tokenResponse('obsolete-token')
          : new Response(null, { status })
      )
      await rejected
      expect(useAuthStore.getState().accessToken).toBe('current-token')
      expect(logout).not.toHaveBeenCalled()
      expect(fetch).toHaveBeenCalledTimes(2)
      expect(useLoadingStore.getState().count).toBe(0)
    }
  )

  it('keeps the new session refresh shared when an old session refresh finishes', async () => {
    const oldRefresh = deferredResponse()
    const newRefresh = deferredResponse()
    let refreshes = 0
    vi.mocked(fetch).mockImplementation(async (url, options) => {
      if (url === '/api/auth/refresh') {
        refreshes++
        return refreshes === 1 ? oldRefresh.promise : newRefresh.promise
      }
      return new Response(null, {
        status:
          new Headers(options?.headers).get('Authorization') ===
          'Bearer rotated-new'
            ? 200
            : 401,
      })
    })
    useAuthStore.getState().startSession('old-token')
    const old = apiFetch('/api/old')
    const rejected = expect(old).rejects.toMatchObject({ name: 'AbortError' })
    await vi.waitFor(() => expect(refreshes).toBe(1))
    useAuthStore.getState().startSession('new-token')
    const current = apiFetch('/api/current')
    await vi.waitFor(() => expect(refreshes).toBe(2))
    oldRefresh.resolve(tokenResponse('rotated-old'))
    await rejected
    const sibling = apiFetch('/api/sibling')
    // Let the sibling's 401 join the new session's pending rotation.
    await Promise.resolve()
    await Promise.resolve()
    expect(refreshes).toBe(2)
    newRefresh.resolve(tokenResponse('rotated-new'))
    expect((await current).ok).toBe(true)
    expect((await sibling).ok).toBe(true)
    expect(refreshes).toBe(2)
    expect(useAuthStore.getState().accessToken).toBe('rotated-new')
  })

  it('retries a delayed 401 with the token already rotated by a sibling', async () => {
    useAuthStore.getState().startSession('old-token')
    const delayed = deferredResponse()
    vi.mocked(fetch)
      .mockReturnValueOnce(delayed.promise)
      .mockResolvedValueOnce(new Response(null, { status: 401 }))
      .mockResolvedValueOnce(tokenResponse('new-token'))
      .mockResolvedValueOnce(new Response(null))
      .mockResolvedValueOnce(new Response(null))
    const late = apiFetch('/api/late')
    expect((await apiFetch('/api/sibling')).ok).toBe(true)
    delayed.resolve(new Response(null, { status: 401 }))
    expect((await late).ok).toBe(true)
    expect(
      vi.mocked(fetch).mock.calls.filter(([url]) => url === '/api/auth/refresh')
    ).toHaveLength(1)
    expect(fetch).toHaveBeenLastCalledWith(
      '/api/late',
      expect.objectContaining({
        headers: expect.objectContaining({ Authorization: 'Bearer new-token' }),
      })
    )
  })

  it('shares the HTTP rotation between session restoration and API recovery', async () => {
    useAuthStore.setState({ accessToken: 'old-token' })
    let completeRefresh!: (response: Response) => void
    const pending = new Promise<Response>((resolve) => {
      completeRefresh = resolve
    })
    let started!: () => void
    const refreshStarted = new Promise<void>((resolve) => {
      started = resolve
    })
    vi.mocked(fetch).mockImplementation(async (url, options) => {
      if (url === '/api/auth/refresh') {
        started()
        return pending
      }
      const authenticated =
        new Headers(options?.headers).get('Authorization') ===
        'Bearer new-token'
      return new Response(null, { status: authenticated ? 200 : 401 })
    })

    const request = apiFetch('/api/test')
    await refreshStarted
    const restoration = requestAccessToken()
    completeRefresh(new Response(JSON.stringify({ access_token: 'new-token' })))
    const [response, token] = await Promise.all([request, restoration])

    expect(response.ok).toBe(true)
    expect(token).toBe('new-token')
    expect(useAuthStore.getState().accessToken).toBe('new-token')
    expect(
      vi.mocked(fetch).mock.calls.filter(([url]) => url === '/api/auth/refresh')
    ).toHaveLength(1)
  })

  it('allows another rotation after failure and leaves authentication decisions to the consumer', async () => {
    useAuthStore.setState({ accessToken: 'current-token' })
    vi.mocked(fetch)
      .mockResolvedValueOnce(new Response(null, { status: 401 }))
      .mockResolvedValueOnce(
        new Response(JSON.stringify({ access_token: 'new-token' }))
      )

    await expect(requestAccessToken()).rejects.toThrow('refresh failed')
    expect(useAuthStore.getState().accessToken).toBe('current-token')
    await expect(requestAccessToken()).resolves.toBe('new-token')
    expect(useAuthStore.getState().accessToken).toBe('current-token')
    expect(fetch).toHaveBeenCalledTimes(2)
  })

  it('increments and decrements loading counter', async () => {
    vi.mocked(fetch).mockResolvedValueOnce(new Response('ok', { status: 200 }))

    expect(useLoadingStore.getState().count).toBe(0)
    await apiFetch('/api/test')
    expect(useLoadingStore.getState().count).toBe(0)
  })

  it('decrements loading counter even on error', async () => {
    vi.mocked(fetch).mockRejectedValueOnce(new Error('network error'))

    await expect(apiFetch('/api/test')).rejects.toThrow('network error')
    expect(useLoadingStore.getState().count).toBe(0)
  })

  it('preserves custom headers', async () => {
    useAuthStore.setState({ accessToken: 'token' })
    vi.mocked(fetch).mockResolvedValueOnce(new Response('ok', { status: 200 }))

    await apiFetch('/api/test', {
      headers: { 'Content-Type': 'application/json' },
    })

    const callArgs = vi.mocked(fetch).mock.calls[0]
    const headers = callArgs[1]?.headers as Record<string, string>
    expect(headers['Content-Type']).toBe('application/json')
    expect(headers['Authorization']).toBe('Bearer token')
  })

  it.each(['AbortError', 'TimeoutError'])(
    'releases a %s consumer without cancelling shared refresh',
    async (reason) => {
      useAuthStore.setState({ accessToken: 'old-token' })
      const controller = new AbortController()
      let completeRefresh: (response: Response) => void = () => {}
      const pendingRefresh = new Promise<Response>((resolve) => {
        completeRefresh = resolve
      })
      let refreshStarted: () => void = () => {}
      const started = new Promise<void>((resolve) => {
        refreshStarted = resolve
      })
      vi.mocked(fetch).mockImplementation(async (url, options) => {
        if (url === '/api/auth/refresh') {
          refreshStarted()
          return pendingRefresh
        }
        if (
          (options?.headers as Record<string, string>)?.Authorization ===
          'Bearer new-token'
        ) {
          return new Response('ok')
        }
        return new Response(null, { status: 401 })
      })
      const cancelled = apiFetch('/api/reading/next', {
        signal: controller.signal,
      })
      const result = expect(cancelled).rejects.toMatchObject({ name: reason })
      await started
      const survivor = apiFetch('/api/listening/next')
      controller.abort(new DOMException('Consumer cancelled', reason))
      await result
      expect(useLoadingStore.getState().count).toBe(1)
      completeRefresh(
        new Response(JSON.stringify({ access_token: 'new-token' }))
      )
      expect((await survivor).ok).toBe(true)
      expect(useLoadingStore.getState().count).toBe(0)
      expect(useAuthStore.getState().accessToken).toBe('new-token')
      expect(
        vi
          .mocked(fetch)
          .mock.calls.filter(([url]) => url === '/api/auth/refresh')
      ).toHaveLength(1)
      expect(
        vi
          .mocked(fetch)
          .mock.calls.filter(([url]) => url === '/api/reading/next')
      ).toHaveLength(1)
    }
  )
})
