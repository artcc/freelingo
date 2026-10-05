import type { NextRequest } from 'next/server'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { POST } from '@/app/api/conversation/warmup/route'

function request(controller = new AbortController(), body = '') {
  return {
    text: vi.fn().mockResolvedValue(body),
    headers: new Headers({
      Authorization: 'Bearer token',
      Cookie: 'refresh_token=cookie',
      'Content-Type': 'application/json',
    }),
    signal: controller.signal,
  } as unknown as NextRequest
}

function deferBackend() {
  let signal!: AbortSignal
  let resolve!: (response: Response) => void
  const backendFetch = vi.fn((_url: string, options: RequestInit) => {
    signal = options.signal as AbortSignal
    return new Promise<Response>((res, reject) => {
      resolve = res
      signal.addEventListener('abort', () => reject(signal.reason), { once: true })
    })
  })
  vi.stubGlobal('fetch', backendFetch)
  return { resolve: (response: Response) => resolve(response), get signal() { return signal } }
}

afterEach(() => {
  vi.useRealTimers()
  vi.unstubAllGlobals()
})

describe('Conversation warmup proxy', () => {
  it.each([200, 402, 429])('forwards authentication, trial context, and backend status %s', async (status) => {
    const data = status === 200 ? { status: 'ready' } : { detail: 'access denied' }
    const backendFetch = vi.fn().mockResolvedValue(Response.json(data, {
      status,
      headers: { 'Retry-After': '60' },
    }))
    vi.stubGlobal('fetch', backendFetch)
    const response = await POST(request(undefined, '{"trial_token":"trial"}'))
    expect(response.status).toBe(status)
    expect(await response.json()).toEqual(data)
    expect(response.headers.get('Retry-After')).toBe('60')
    expect(backendFetch).toHaveBeenCalledWith('http://backend:8000/api/conversation/warmup',
      expect.objectContaining({ method: 'POST', body: '{"trial_token":"trial"}' }))
    const headers = backendFetch.mock.calls[0][1].headers as Headers
    expect(headers.get('Authorization')).toBe('Bearer token')
    expect(headers.get('Cookie')).toBe('refresh_token=cookie')
    expect(headers.get('Content-Type')).toBe('application/json')
    expect(headers.has('X-Real-IP')).toBe(false)
    expect(headers.has('X-Forwarded-For')).toBe(false)
  })

  it.each([true, false])('preserves distinct client IPs with X-Real-IP present: %s', async (withRealIp) => {
    const backendFetch = vi.fn().mockImplementation(async () => Response.json({ status: 'ready' }))
    vi.stubGlobal('fetch', backendFetch)
    const clientIps = ['192.0.2.10', '2001:db8::20']

    for (const ip of clientIps) {
      const incoming = request()
      if (withRealIp) incoming.headers.set('X-Real-IP', ip)
      incoming.headers.set('X-Forwarded-For', `${ip}, 192.0.2.200`)
      expect((await POST(incoming)).status).toBe(200)
    }

    expect(backendFetch).toHaveBeenCalledTimes(2)
    for (const [index, ip] of clientIps.entries()) {
      const headers = backendFetch.mock.calls[index][1].headers as Headers
      expect(headers.get('X-Real-IP')).toBe(withRealIp ? ip : null)
      expect(headers.get('X-Forwarded-For')).toBe(`${ip}, 192.0.2.200`)
    }
  })

  it('allows a 45-second cold start and clears its deadline after success', async () => {
    vi.useFakeTimers()
    const pending = deferBackend()
    const response = POST(request())
    await vi.advanceTimersByTimeAsync(45_000)
    expect(pending.signal.aborted).toBe(false)
    pending.resolve(Response.json({ status: 'ready' }))
    expect((await response).status).toBe(200)
    await vi.advanceTimersByTimeAsync(80_000)
    expect(pending.signal.aborted).toBe(false)
  })

  it('aborts the backend request at 70 seconds and returns 504', async () => {
    vi.useFakeTimers()
    const pending = deferBackend()
    const response = POST(request())
    await vi.advanceTimersByTimeAsync(69_999)
    expect(pending.signal.aborted).toBe(false)
    await vi.advanceTimersByTimeAsync(1)
    expect(pending.signal.aborted).toBe(true)
    const result = await response
    expect(result.status).toBe(504)
    expect(await result.json()).toEqual({ detail: 'warmup_proxy_timeout' })
  })

  it('propagates client cancellation to the backend fetch', async () => {
    vi.useFakeTimers()
    const pending = deferBackend()
    const controller = new AbortController()
    const response = POST(request(controller))
    const cancelled = expect(response).rejects.toMatchObject({ name: 'AbortError' })
    await vi.advanceTimersByTimeAsync(0)
    controller.abort()
    await cancelled
    expect(pending.signal.aborted).toBe(true)
    expect(vi.getTimerCount()).toBe(0)
  })
})
