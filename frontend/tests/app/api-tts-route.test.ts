import type { NextRequest } from 'next/server'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { POST } from '@/app/api/tts/route'
import { float32ToWav } from '@/lib/audio'

let deadline: AbortController

function makeRequest(signal = new AbortController().signal) {
  return {
    text: vi.fn().mockResolvedValue(JSON.stringify({ text: 'Hello' })),
    headers: new Headers(),
    signal,
  } as unknown as NextRequest
}

beforeEach(() => {
  deadline = new AbortController()
  vi.spyOn(AbortSignal, 'timeout').mockReturnValue(deadline.signal)
})

afterEach(() => {
  vi.unstubAllGlobals()
})

describe('TTS API proxy', () => {
  it.each(['audio/mpeg', 'audio/wav'])(
    'preserves %s bytes and content type',
    async (contentType) => {
      const bytes =
        contentType === 'audio/wav'
          ? float32ToWav(new Float32Array([0.5, -0.5]), 24000)
          : new TextEncoder().encode('ID3audio').buffer
      const backendFetch = vi.fn().mockResolvedValue(
        new Response(bytes, {
          headers: {
            'Content-Type': contentType,
            'X-TTS-Trace-ID': 'backend-trace',
            'X-TTS-Backend-Synth-Ms': '12.0',
            'X-TTS-Backend-Total-Ms': '15.0',
          },
        })
      )
      vi.stubGlobal('fetch', backendFetch)
      const body = JSON.stringify({ text: 'Hello', voice: 'female' })
      const request = {
        text: vi.fn().mockResolvedValue(body),
        headers: new Headers({
          Authorization: 'Bearer token',
          Cookie: 'refresh_token=test',
          'X-TTS-Trace-ID': 'client-trace',
        }),
        signal: new AbortController().signal,
      } as unknown as NextRequest

      const response = await POST(request)

      expect(response.status).toBe(200)
      expect(response.headers.get('Content-Type')).toBe(contentType)
      expect(response.headers.get('X-TTS-Trace-ID')).toBe('backend-trace')
      expect(response.headers.get('X-TTS-Backend-Synth-Ms')).toBe('12.0')
      expect(response.headers.get('X-TTS-Backend-Total-Ms')).toBe('15.0')
      for (const phase of ['Fetch', 'Buffer', 'Total']) {
        expect(response.headers.get(`X-TTS-Proxy-${phase}-Ms`)).toMatch(
          /^\d+\.\d$/
        )
      }
      expect(await response.arrayBuffer()).toEqual(bytes)
      expect(backendFetch).toHaveBeenCalledWith(
        'http://backend:8000/api/tts',
        expect.objectContaining({ method: 'POST', body })
      )
      expect(backendFetch.mock.calls[0][1].headers.get('Authorization')).toBe(
        'Bearer token'
      )
      expect(backendFetch.mock.calls[0][1].headers.get('Cookie')).toBe(
        'refresh_token=test'
      )
      expect(backendFetch.mock.calls[0][1].headers.get('X-TTS-Trace-ID')).toBe(
        'client-trace'
      )
      expect(AbortSignal.timeout).toHaveBeenCalledWith(60_000)
    }
  )

  it.each([401, 422, 503])(
    'preserves backend error %s and its body',
    async (status) => {
      const body = JSON.stringify({ detail: 'Backend error' })
      vi.stubGlobal(
        'fetch',
        vi.fn().mockResolvedValue(new Response(body, { status }))
      )
      const response = await POST(makeRequest())
      expect(response.status).toBe(status)
      expect(await response.text()).toBe(body)
    }
  )

  it('returns 502 on transport failure', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new TypeError('Offline')))
    const response = await POST(makeRequest())
    expect(response.status).toBe(502)
    expect(await response.json()).toEqual({
      detail: 'Speech synthesis is unavailable',
    })
  })

  it('does not dispatch an already canceled request', async () => {
    const client = new AbortController()
    client.abort()
    const backendFetch = vi.fn()
    vi.stubGlobal('fetch', backendFetch)
    expect((await POST(makeRequest(client.signal))).status).toBe(504)
    expect(backendFetch).not.toHaveBeenCalled()
  })

  describe.each(['client', 'deadline'] as const)('%s cancellation', (cause) => {
    it.each(['headers', 'audio', 'error'] as const)(
      'aborts upstream work while reading %s',
      async (stage) => {
        const client = new AbortController()
        let started!: () => void
        const pending = new Promise<void>((resolve) => {
          started = resolve
        })
        let upstreamSignal!: AbortSignal
        const backendFetch = vi.fn((_url: string, options: RequestInit) => {
          upstreamSignal = options.signal as AbortSignal
          if (stage === 'headers') {
            return new Promise<Response>((_, reject) => {
              upstreamSignal.addEventListener('abort', () =>
                reject(upstreamSignal.reason)
              )
              started()
            })
          }
          const stream = new ReadableStream<Uint8Array>({
            start(controller) {
              controller.enqueue(new Uint8Array([1, 2]))
              upstreamSignal.addEventListener('abort', () =>
                controller.error(upstreamSignal.reason)
              )
            },
          })
          const response = new Response(stream, {
            status: stage === 'error' ? 503 : 200,
          })
          if (stage === 'audio') {
            const read = response.arrayBuffer.bind(response)
            vi.spyOn(response, 'arrayBuffer').mockImplementation(() => {
              started()
              return read()
            })
          } else {
            const read = response.text.bind(response)
            vi.spyOn(response, 'text').mockImplementation(() => {
              started()
              return read()
            })
          }
          return Promise.resolve(response)
        })
        vi.stubGlobal('fetch', backendFetch)
        const result = POST(makeRequest(client.signal))
        await pending
        expect(upstreamSignal.aborted).toBe(false)
        if (cause === 'client') client.abort()
        else deadline.abort(new DOMException('Timed out', 'TimeoutError'))
        expect(upstreamSignal.aborted).toBe(true)
        const response = await result
        expect(response.status).toBe(504)
        expect(await response.json()).toEqual({
          detail: 'Speech synthesis is unavailable',
        })
        expect(backendFetch).toHaveBeenCalledTimes(1)
      }
    )
  })

  it('returns 502 when the backend audio stream fails mid-buffer', async () => {
    const stream = new ReadableStream<Uint8Array>({
      start(controller) {
        controller.enqueue(new Uint8Array([1, 2]))
        controller.error(new TypeError('Connection reset'))
      },
    })
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(new Response(stream)))
    expect((await POST(makeRequest())).status).toBe(502)
  })
})
