import { beforeEach, describe, expect, it, vi } from 'vitest'
import { apiFetch } from '@/lib/api'
import { practiceRequest, PracticeRequestError } from '@/lib/grammar-practice'

vi.mock('@/lib/api', () => ({ apiFetch: vi.fn() }))

beforeEach(() => vi.clearAllMocks())

describe('grammar practice transport', () => {
  it('keeps structured active-session conflicts and Retry-After', async () => {
    vi.mocked(apiFetch).mockResolvedValue(
      new Response(
        JSON.stringify({
          detail: { code: 'practice_in_progress', session_id: 'saved-uuid' },
        }),
        { status: 409, headers: { 'Retry-After': '12' } }
      )
    )
    await expect(
      practiceRequest('/topics/1/sessions', { method: 'POST' })
    ).rejects.toMatchObject({
      status: 409,
      code: 'practice_in_progress',
      sessionId: 'saved-uuid',
      retryAfter: 12,
    })
  })

  it.each([
    ['grammar_practice', 'freemium_exhausted'],
    ['games', 'unavailable'],
  ])(
    'only accepts quota metadata for this feature (%s)',
    async (feature, code) => {
      vi.mocked(apiFetch).mockResolvedValue(
        new Response(
          JSON.stringify({
            detail: { reason: 'freemium_exhausted', feature },
          }),
          { status: 402 }
        )
      )
      await expect(practiceRequest('/topics/1/sessions')).rejects.toEqual(
        new PracticeRequestError(402, code)
      )
    }
  )

  it('combines caller cancellation with a bounded request and no-cache reads', async () => {
    const controller = new AbortController()
    vi.mocked(apiFetch).mockResolvedValue(new Response('{"topics":[]}'))
    await practiceRequest('/topics', { signal: controller.signal })
    const [path, options] = vi.mocked(apiFetch).mock.calls[0]
    expect(path).toBe('/api/grammar-practice/topics')
    expect(options?.cache).toBe('no-store')
    expect(options?.signal?.aborted).toBe(false)
    controller.abort()
    expect(options?.signal?.aborted).toBe(true)
  })
})
