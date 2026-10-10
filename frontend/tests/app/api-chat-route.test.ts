import type { NextRequest } from 'next/server'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { POST } from '@/app/api/chat/route'

describe('Chat API route', () => {
  afterEach(() => vi.unstubAllGlobals())

  it('preserves the browser User-Agent while streaming the backend response', async () => {
    const stream = 'data: {"done":true}\n\n'
    const backendFetch = vi.fn().mockResolvedValue(new Response(stream))
    vi.stubGlobal('fetch', backendFetch)
    const request = {
      text: vi.fn().mockResolvedValue('{"message":"Private content"}'),
      headers: new Headers({
        Authorization: 'Bearer token',
        'User-Agent': 'Browser test agent',
      }),
    } as unknown as NextRequest

    const response = await POST(request)

    expect(await response.text()).toBe(stream)
    expect(response.headers.get('Content-Type')).toBe('text/event-stream')
    const headers = backendFetch.mock.calls[0][1].headers as Headers
    expect(headers.get('User-Agent')).toBe('Browser test agent')
    expect(headers.get('Authorization')).toBe('Bearer token')
  })
})
