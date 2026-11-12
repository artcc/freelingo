import { NextRequest } from 'next/server'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { GET as preview } from '@/app/api/tts/preview/[voice]/route'
import { GET as phrasebook } from '@/app/api/phrasebook/audio/[categoryId]/[phraseIndex]/route'
import nextConfig from '../../next.config'

const routes = [
  {
    name: 'voice preview',
    path: '/api/tts/preview/female',
    get: (request: NextRequest) =>
      preview(request, { params: Promise.resolve({ voice: 'female' }) }),
  },
  {
    name: 'Phrasebook audio',
    path: '/api/phrasebook/audio/greetings/0?language=pt-PT',
    get: (request: NextRequest) =>
      phrasebook(request, {
        params: Promise.resolve({ categoryId: 'greetings', phraseIndex: '0' }),
      }),
  },
]

let deadline: AbortController

beforeEach(() => {
  deadline = new AbortController()
  vi.spyOn(AbortSignal, 'timeout').mockReturnValue(deadline.signal)
})

afterEach(() => {
  vi.useRealTimers()
  vi.unstubAllGlobals()
})

it('resolves dynamic audio handlers before the generic backend rewrite', async () => {
  expect(await nextConfig.rewrites!()).toEqual({
    fallback: [
      {
        source: '/api/:path*',
        destination: `${process.env.BACKEND_URL || 'http://backend:8000'}/api/:path*`,
      },
    ],
  })
})

describe.each(routes)('$name proxy', ({ path, get }) => {
  function request(signal = new AbortController().signal) {
    return new NextRequest(`http://localhost:3000${path}`, {
      headers: {
        Authorization: 'Bearer test-token',
        Cookie: 'refresh_token=test',
        'X-Real-IP': '192.0.2.1',
        'X-Forwarded-For': '192.0.2.1',
      },
      signal,
    })
  }

  it.each(['audio/wav', 'audio/mpeg'])(
    'preserves %s bytes, query, credentials and client IP',
    async (mime) => {
      const bytes = new Uint8Array([0, 255, 12, 128]).buffer
      const backendFetch = vi.fn().mockResolvedValue(
        new Response(bytes, {
          headers: { 'Content-Type': mime },
        })
      )
      vi.stubGlobal('fetch', backendFetch)

      const response = await get(request())

      expect(response.status).toBe(200)
      expect(response.headers.get('Content-Type')).toBe(mime)
      expect(response.headers.get('Cache-Control')).toBe('no-store')
      expect(await response.arrayBuffer()).toEqual(bytes)
      const [url, options] = backendFetch.mock.calls[0]
      expect(String(url)).toBe(`http://backend:8000${path}`)
      expect(options).toMatchObject({ method: 'GET', cache: 'no-store' })
      request().headers.forEach((value, name) => {
        expect(options.headers.get(name)).toBe(value)
      })
      expect(AbortSignal.timeout).toHaveBeenCalledWith(60_000)
    }
  )

  it('allows a cache-miss synthesis lasting 35 seconds', async () => {
    vi.useFakeTimers()
    vi.mocked(AbortSignal.timeout).mockImplementation((ms) => {
      setTimeout(() => deadline.abort(), ms)
      return deadline.signal
    })
    vi.stubGlobal(
      'fetch',
      vi.fn(
        (_url: unknown, { signal }: RequestInit) =>
          new Promise<Response>((resolve, reject) => {
            const abort = () => reject(signal!.reason)
            signal!.addEventListener('abort', abort, { once: true })
            setTimeout(() => {
              signal!.removeEventListener('abort', abort)
              resolve(
                new Response('audio', {
                  headers: { 'Content-Type': 'audio/wav' },
                })
              )
            }, 35_000)
          })
      )
    )
    const completed = vi.fn()
    const result = get(request()).then((response) => {
      completed()
      return response
    })

    await vi.advanceTimersByTimeAsync(30_000)
    expect(completed).not.toHaveBeenCalled()
    expect(deadline.signal.aborted).toBe(false)
    await vi.advanceTimersByTimeAsync(5_000)
    expect((await result).status).toBe(200)
    expect(await (await result).text()).toBe('audio')
    vi.clearAllTimers()
  })

  it.each([400, 401, 404, 416, 429, 503])(
    'preserves backend error %s and retry metadata',
    async (status) => {
      const body = JSON.stringify({ detail: 'Backend error' })
      vi.stubGlobal(
        'fetch',
        vi.fn().mockResolvedValue(
          new Response(body, {
            status,
            headers: {
              'Content-Type': 'application/json',
              'Retry-After': '15',
            },
          })
        )
      )
      const response = await get(request())
      expect(response.status).toBe(status)
      expect(response.headers.get('Content-Type')).toBe('application/json')
      expect(response.headers.get('Retry-After')).toBe('15')
      expect(await response.text()).toBe(body)
    }
  )

  it('preserves partial audio requests and responses', async () => {
    const backendFetch = vi.fn().mockResolvedValue(
      new Response('RIFF', {
        status: 206,
        headers: {
          'Content-Type': 'audio/wav',
          'Accept-Ranges': 'bytes',
          'Content-Range': 'bytes 0-3/48',
          ETag: '"audio-version"',
        },
      })
    )
    vi.stubGlobal('fetch', backendFetch)
    const incoming = request()
    incoming.headers.set('Range', 'bytes=0-3')
    incoming.headers.set('If-Range', '"audio-version"')

    const response = await get(incoming)

    expect(backendFetch.mock.calls[0][1].headers.get('Range')).toBe('bytes=0-3')
    expect(backendFetch.mock.calls[0][1].headers.get('If-Range')).toBe(
      '"audio-version"'
    )
    expect(response.status).toBe(206)
    expect(response.headers.get('Content-Range')).toBe('bytes 0-3/48')
    expect(response.headers.get('Accept-Ranges')).toBe('bytes')
    expect(response.headers.get('ETag')).toBe('"audio-version"')
    expect(await response.text()).toBe('RIFF')
  })

  it('does not dispatch an already cancelled request', async () => {
    const client = new AbortController()
    client.abort()
    const backendFetch = vi.fn()
    vi.stubGlobal('fetch', backendFetch)
    expect((await get(request(client.signal))).status).toBe(504)
    expect(backendFetch).not.toHaveBeenCalled()
  })

  describe.each(['client', 'deadline'])('%s cancellation', (cause) => {
    it.each(['headers', 'audio', 'error'])(
      'aborts the upstream while reading %s',
      async (stage) => {
        const client = new AbortController()
        let started!: () => void
        const pending = new Promise<void>((resolve) => {
          started = resolve
        })
        let upstream!: AbortSignal
        vi.stubGlobal(
          'fetch',
          vi.fn((_url: unknown, options: RequestInit) => {
            upstream = options.signal as AbortSignal
            if (stage === 'headers') {
              return new Promise<Response>((_, reject) => {
                upstream.addEventListener('abort', () =>
                  reject(upstream.reason)
                )
                started()
              })
            }
            const stream = new ReadableStream<Uint8Array>({
              start(controller) {
                controller.enqueue(new Uint8Array([1, 2]))
                upstream.addEventListener('abort', () =>
                  controller.error(upstream.reason)
                )
              },
            })
            const response = new Response(stream, {
              status: stage === 'error' ? 503 : 200,
            })
            const read = response.arrayBuffer.bind(response)
            vi.spyOn(response, 'arrayBuffer').mockImplementation(() => {
              started()
              return read()
            })
            return Promise.resolve(response)
          })
        )
        const result = get(request(client.signal))
        await pending
        expect(upstream.aborted).toBe(false)
        if (cause === 'client') client.abort()
        else deadline.abort()
        expect(upstream.aborted).toBe(true)
        expect((await result).status).toBe(504)
      }
    )
  })

  it('returns 502 on transport failure', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new TypeError('Offline')))
    expect((await get(request())).status).toBe(502)
  })
})
