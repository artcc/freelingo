import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { POST } from '@/app/umami/api/[...path]/route'
import { getUmamiConfig } from '@/lib/umami-config'

const website = '94db1cb1-74f4-4a40-ad6c-962362670409'
const pageview = (url: string) => ({
  type: 'event',
  payload: {
    website,
    url,
    hostname: 'untrusted',
    title: 'Private text',
    referrer: '/reset-password?token=private',
    id: 'user-42',
    ip: '203.0.113.1',
    data: { email: 'private@example.com' },
    screen: '1920x1080',
    language: 'en-GB',
  },
})

function send(body: unknown, endpoint = 'send') {
  return POST(
    new Request('https://freelingo.app/umami/api/send', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'Browser',
        Cookie: 'private',
        Authorization: 'Bearer secret',
      },
      body: JSON.stringify(body),
    }),
    { params: Promise.resolve({ path: [endpoint] }) }
  )
}

beforeEach(() => {
  vi.stubEnv(
    'NEXT_PUBLIC_UMAMI_SCRIPT_URL',
    'https://analytics.example:8443/umami/script.js'
  )
  vi.stubEnv('NEXT_PUBLIC_UMAMI_WEBSITE_ID', website)
  vi.stubGlobal(
    'fetch',
    vi.fn().mockResolvedValue(Response.json({ sessionId: 'session' }))
  )
})
afterEach(() => {
  vi.unstubAllEnvs()
  vi.unstubAllGlobals()
})

describe('anonymous browser collection boundary', () => {
  it.each([
    ['/lesson/123?token=private#secret', '/lesson'],
    ['/admin/users/42', '/admin'],
    ['/verify-email?token=private', '/verify-email'],
    ['/grammar/private-topic', '/grammar'],
  ])(
    'normalizes %s and drops all free-form or identifying fields',
    async (url, expected) => {
      expect((await send(pageview(url))).status).toBe(200)
      const [target, options] = vi.mocked(fetch).mock.calls[0]
      expect(target).toBe('https://analytics.example:8443/api/send')
      expect(JSON.parse(String(options?.body))).toEqual({
        type: 'event',
        payload: {
          website,
          hostname: 'freelingo.app',
          url: expected,
          title: expected,
          referrer: '',
          screen: '1920x1080',
          language: 'en-GB',
        },
      })
      const headers = new Headers(options?.headers)
      expect(headers.has('Cookie')).toBe(false)
      expect(headers.has('Authorization')).toBe(false)
      expect(headers.has('X-Forwarded-For')).toBe(false)
      expect(options?.redirect).toBe('error')
    }
  )

  it('blocks identify, browser custom events, foreign websites and unknown endpoints', async () => {
    await send({ ...pageview('/dashboard'), type: 'identify' })
    const custom = pageview('/dashboard')
    await send({
      ...custom,
      payload: { ...custom.payload, name: 'private-event' },
    })
    await send({
      ...custom,
      payload: { ...custom.payload, website: 'other-site' },
    })
    expect((await send(custom, '../users')).status).toBe(404)
    expect(fetch).not.toHaveBeenCalled()
  })

  it('sanitizes batch collection as well', async () => {
    await send(
      [pageview('/chat/99'), { type: 'identify', payload: { id: 'user-1' } }],
      'batch'
    )
    const events = JSON.parse(String(vi.mocked(fetch).mock.calls[0][1]?.body))
    expect(events).toHaveLength(1)
    expect(events[0].payload.url).toBe('/chat')
    expect(events[0].payload.id).toBeUndefined()
  })

  it('requires both valid runtime settings and does not cache their initial values', async () => {
    expect(getUmamiConfig()?.websiteId).toBe(website)
    vi.stubEnv('NEXT_PUBLIC_UMAMI_WEBSITE_ID', '')
    expect(getUmamiConfig()).toBeNull()
    expect((await send(pageview('/dashboard'))).status).toBe(404)
    expect(fetch).not.toHaveBeenCalled()
    vi.stubEnv('NEXT_PUBLIC_UMAMI_WEBSITE_ID', website)
    vi.stubEnv(
      'NEXT_PUBLIC_UMAMI_SCRIPT_URL',
      'https://user:password@analytics.example/script.js'
    )
    expect(getUmamiConfig()).toBeNull()
  })
})
