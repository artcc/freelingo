import type { NextRequest } from 'next/server'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { POST } from '@/app/api/tts/route'
import { float32ToWav } from '@/lib/audio'

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
          },
        })
      )
      vi.stubGlobal('fetch', backendFetch)
      const body = JSON.stringify({ text: 'Hello', voice: 'female' })
      const request = {
        text: vi.fn().mockResolvedValue(body),
        headers: new Headers({ Authorization: 'Bearer token' }),
      } as unknown as NextRequest

      const response = await POST(request)

      expect(response.status).toBe(200)
      expect(response.headers.get('Content-Type')).toBe(contentType)
      expect(response.headers.get('X-TTS-Trace-ID')).toBe('backend-trace')
      expect(response.headers.get('X-TTS-Backend-Synth-Ms')).toBe('12.0')
      expect(await response.arrayBuffer()).toEqual(bytes)
      expect(backendFetch).toHaveBeenCalledWith(
        'http://backend:8000/api/tts',
        expect.objectContaining({ method: 'POST', body })
      )
      expect(backendFetch.mock.calls[0][1].headers.get('Authorization')).toBe(
        'Bearer token'
      )
    }
  )
})
