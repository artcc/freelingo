import { act, cleanup, renderHook } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { useExerciseAnalytics } from '@/hooks/useExerciseAnalytics'
import { useAuthStore } from '@/store/auth'
import { useLanguageStore } from '@/store/language'
import { getLanguageByCode } from '@/lib/target-languages'

const context = { study_plan_id: 8, target_language: 'en-GB', level: 'A1' }

beforeEach(() => {
  vi.stubGlobal(
    'fetch',
    vi.fn().mockResolvedValue(new Response(null, { status: 204 }))
  )
  useAuthStore.getState().startSession('token')
  useLanguageStore.setState({
    activeLanguage: getLanguageByCode('en-GB') ?? null,
    userLanguages: [
      {
        target_language: 'en-GB',
        is_active: true,
        plan: {
          id: 8,
          cefr_level: 'A1',
          progress_day: 0,
          total_days: 48,
          completion_pct: 0,
        },
        progress: null,
      },
    ],
    needsRefresh: false,
    isSwitching: false,
  })
})

afterEach(() => {
  cleanup()
  vi.unstubAllGlobals()
})

describe.each(['listening', 'reading'] as const)('%s analytics', (feature) => {
  it('waits for interaction and uses one nonpersistent operation UUID until reset', () => {
    const { result, unmount } = renderHook(() => useExerciseAnalytics(feature))
    expect(fetch).not.toHaveBeenCalled()
    expect(result.current.headers()).toEqual({})
    act(() => {
      result.current.start(42, context, false)
      result.current.start(42, context, false)
    })
    expect(fetch).toHaveBeenCalledTimes(1)
    const first = result.current.headers()['X-Exercise-Attempt']
    expect(first).toMatch(/^[0-9a-f-]{36}$/)
    const options = vi.mocked(fetch).mock.calls[0][1]!
    expect(new Headers(options.headers).get('X-Exercise-Attempt')).toBe(first)
    expect(JSON.parse(String(options.body))).toEqual({
      exercise_id: 42,
      context,
      replay: false,
    })
    expect(localStorage.setItem).not.toHaveBeenCalled()
    act(() => {
      result.current.reset()
      result.current.start(42, context, true)
    })
    expect(options.signal?.aborted).toBe(true)
    expect(fetch).toHaveBeenCalledTimes(2)
    expect(result.current.headers()['X-Exercise-Attempt']).not.toBe(first)
    const replay = vi.mocked(fetch).mock.calls[1][1]!
    expect(JSON.parse(String(replay.body)).replay).toBe(true)
    unmount()
    expect(replay.signal?.aborted).toBe(true)
  })

  it.each(['401', 'transport'])(
    'ignores %s errors without auth refresh',
    async (failure) => {
      if (failure === 'transport')
        vi.mocked(fetch).mockRejectedValue(new TypeError('Unavailable'))
      else
        vi.mocked(fetch).mockResolvedValue(new Response(null, { status: 401 }))
      const { result } = renderHook(() => useExerciseAnalytics(feature))
      await act(async () => result.current.start(42, context, false))
      expect(useAuthStore.getState().accessToken).toBe('token')
      expect(fetch).toHaveBeenCalledTimes(1)
      expect(vi.mocked(fetch).mock.calls[0][0]).toBe(`/api/${feature}/started`)
      expect(result.current.headers()['X-Exercise-Attempt']).toBeTruthy()
    }
  )

  it('rejects stale context and never reuses an operation in a new auth session', () => {
    const { result } = renderHook(() => useExerciseAnalytics(feature))
    act(() => result.current.start(42, { ...context, study_plan_id: 9 }, false))
    expect(fetch).not.toHaveBeenCalled()
    act(() => result.current.start(42, context, false))
    const first = result.current.headers()['X-Exercise-Attempt']
    const signal = vi.mocked(fetch).mock.calls[0][1]?.signal
    act(() => useAuthStore.getState().startSession('new-token'))
    expect(result.current.headers()).toEqual({})
    act(() => result.current.start(42, context, false))
    expect(signal?.aborted).toBe(true)
    expect(result.current.headers()['X-Exercise-Attempt']).not.toBe(first)
  })
})
