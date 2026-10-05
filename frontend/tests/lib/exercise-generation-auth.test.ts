import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { resolveExercise } from '@/lib/exercise-generation'
import { useAuthStore } from '@/store/auth'
import { useLoadingStore } from '@/store/loading'

describe('exercise polling with the real auth interceptor', () => {
  beforeEach(() => {
    vi.useFakeTimers()
    useAuthStore.setState({ accessToken: 'old-token', user: null })
    useLoadingStore.setState({ count: 0 })
    vi.stubGlobal('fetch', vi.fn())
    // Drive the native timeout signal with the test clock; apiFetch itself is not mocked.
    vi.spyOn(AbortSignal, 'timeout').mockImplementation((ms) => {
      const controller = new AbortController()
      setTimeout(
        () => controller.abort(new DOMException('Timed out', 'TimeoutError')),
        ms
      )
      return controller.signal
    })
  })

  afterEach(() => {
    vi.restoreAllMocks()
    vi.unstubAllGlobals()
    vi.useRealTimers()
  })

  it('times out the consumer at 20 seconds while refresh remains pending', async () => {
    let finishRefresh: (response: Response) => void = () => {}
    const pending = new Promise<Response>((resolve) => {
      finishRefresh = resolve
    })
    vi.mocked(fetch).mockImplementation(async (url) => {
      if (url === '/api/auth/refresh') return pending
      return new Response(null, { status: 401 })
    })
    const controller = new AbortController()
    const result = expect(
      resolveExercise({
        feature: 'reading',
        context: { target_language: 'en-GB' },
        signal: controller.signal,
        onGenerating: vi.fn(),
      })
    ).rejects.toMatchObject({ name: 'AbortError' })
    await vi.advanceTimersByTimeAsync(19_999)
    expect(useLoadingStore.getState().count).toBe(1)
    await vi.advanceTimersByTimeAsync(1)
    expect(useLoadingStore.getState().count).toBe(0)
    // Leaving the page cancels the recovery timer; a later refresh must not resend the old GET.
    controller.abort()
    await result
    finishRefresh(new Response(JSON.stringify({ access_token: 'new-token' })))
    await vi.advanceTimersByTimeAsync(0)
    expect(fetch).toHaveBeenCalledTimes(2)
    expect(useAuthStore.getState().accessToken).toBe('new-token')
  })

  it('bounds the final pending request by the ten-second grace period', async () => {
    const context = { study_plan_id: 7, target_language: 'en-GB', level: 'B1' }
    vi.mocked(fetch)
      .mockResolvedValueOnce(
        new Response(
          JSON.stringify({
            available: false,
            exercise: null,
            context,
            generation_status: 'generating',
            generation_error: null,
            generation_deadline: null,
            generation_remaining_seconds: 10,
          })
        )
      )
      .mockImplementationOnce(
        (_url, options) =>
          new Promise((_resolve, reject) => {
            options?.signal?.addEventListener(
              'abort',
              () => reject(options.signal?.reason),
              { once: true }
            )
          })
      )
    const result = expect(
      resolveExercise({
        feature: 'reading',
        context,
        signal: new AbortController().signal,
        onGenerating: vi.fn(),
      })
    ).rejects.toMatchObject({ code: 'timeout' })
    await vi.advanceTimersByTimeAsync(20_000)
    await result
    expect(fetch).toHaveBeenCalledTimes(2)
    expect(useLoadingStore.getState().count).toBe(0)
  })
})
