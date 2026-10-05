import { act, renderHook, waitFor } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { useExerciseGeneration } from '@/hooks/useExerciseGeneration'
import { resolveExercise } from '@/lib/exercise-generation'
import { useLanguageStore } from '@/store/language'
import { StrictMode } from 'react'

vi.mock('@/lib/exercise-generation', async (importOriginal) => ({
  ...(await importOriginal<typeof import('@/lib/exercise-generation')>()),
  resolveExercise: vi.fn(),
}))
vi.mock('next-intl', () => {
  const translate = (key: string) => key
  return { useTranslations: () => translate }
})

const resolve = vi.mocked(resolveExercise)

describe('useExerciseGeneration lifecycle', () => {
  const onExercise = vi.fn()
  const setPageState = vi.fn()
  const setError = vi.fn()
  const dismissTooltip = vi.fn()
  const options = {
    feature: 'reading' as const,
    onExercise,
    setPageState,
    setError,
    dismissTooltip,
  }

  beforeEach(() => {
    vi.resetAllMocks()
    useLanguageStore.setState({ isSwitching: false, needsRefresh: false })
  })

  it('ignores late responses from the previous language', async () => {
    let finishOld: (value: object) => void = () => {}
    resolve
      .mockImplementationOnce(
        () =>
          new Promise((done) => {
            finishOld = done
          })
      )
      .mockImplementationOnce(async ({ onContext }) => {
        onContext?.({ study_plan_id: 2, target_language: 'es', level: 'B1' })
        return { id: 2, target_language: 'es' }
      })
    const { rerender } = renderHook(
      ({ language }) => useExerciseGeneration({ ...options, language }),
      {
        initialProps: { language: 'en-GB' },
      }
    )
    const oldSignal = resolve.mock.calls[0][0].signal
    rerender({ language: 'es' })
    await waitFor(() =>
      expect(onExercise).toHaveBeenCalledWith(
        { id: 2, target_language: 'es' },
        { study_plan_id: 2, target_language: 'es', level: 'B1' }
      )
    )
    await act(async () => {
      finishOld({ id: 1, target_language: 'en-GB' })
    })
    expect(oldSignal.aborted).toBe(true)
    expect(onExercise).toHaveBeenCalledTimes(1)
  })

  it('blocks double clicks before POST has completed', async () => {
    resolve
      .mockResolvedValueOnce(null)
      .mockImplementationOnce(() => new Promise(() => {}))
    const { result, unmount } = renderHook(() =>
      useExerciseGeneration({ ...options, language: 'en-GB' })
    )
    await waitFor(() => expect(setPageState).toHaveBeenCalledWith('idle'))
    act(() => {
      void result.current.generate()
      void result.current.generate()
    })
    expect(resolve).toHaveBeenCalledTimes(2)
    const signal = resolve.mock.calls[1][0].signal
    unmount()
    expect(signal.aborted).toBe(true)
  })

  it('does not update the page after unmount', async () => {
    let finish: (value: object) => void = () => {}
    resolve.mockImplementationOnce(
      () =>
        new Promise((done) => {
          finish = done
        })
    )
    const { unmount } = renderHook(() =>
      useExerciseGeneration({ ...options, language: 'en-GB' })
    )
    unmount()
    setPageState.mockClear()
    await act(async () => {
      finish({ id: 1 })
    })
    expect(onExercise).not.toHaveBeenCalled()
    expect(setPageState).not.toHaveBeenCalled()
  })

  it('cancels when the plan changes without changing language', async () => {
    resolve
      .mockImplementationOnce(() => new Promise(() => {}))
      .mockResolvedValueOnce(null)
    const { rerender } = renderHook(
      ({ studyPlanId, level }) =>
        useExerciseGeneration({
          ...options,
          language: 'en-GB',
          studyPlanId,
          level,
        }),
      { initialProps: { studyPlanId: 7, level: 'B1' } }
    )
    const signal = resolve.mock.calls[0][0].signal
    rerender({ studyPlanId: 8, level: 'B2' })
    await waitFor(() => expect(resolve).toHaveBeenCalledTimes(2))
    expect(signal.aborted).toBe(true)
    expect(resolve.mock.calls[1][0].context).toEqual({
      study_plan_id: 8,
      target_language: 'en-GB',
      level: 'B2',
    })
  })

  it('resumes an interrupted lookup after a rejected switch', async () => {
    resolve
      .mockImplementationOnce(() => new Promise(() => {}))
      .mockResolvedValueOnce(null)
    renderHook(() => useExerciseGeneration({ ...options, language: 'en-GB' }))
    const signal = resolve.mock.calls[0][0].signal
    act(() => useLanguageStore.setState({ isSwitching: true }))
    expect(signal.aborted).toBe(true)
    expect(resolve).toHaveBeenCalledTimes(1)
    act(() => useLanguageStore.setState({ isSwitching: false }))
    await waitFor(() => expect(setPageState).toHaveBeenCalledWith('idle'))
    expect(resolve).toHaveBeenCalledTimes(2)
    expect(resolve.mock.calls[1][0].generate).toBe(false)
  })

  it('restarts the initial lookup after StrictMode effect cleanup', async () => {
    resolve
      .mockImplementationOnce(() => new Promise(() => {}))
      .mockResolvedValueOnce(null)
    renderHook(() => useExerciseGeneration({ ...options, language: 'en-GB' }), {
      wrapper: StrictMode,
    })
    await waitFor(() => expect(setPageState).toHaveBeenCalledWith('idle'))
    expect(resolve).toHaveBeenCalledTimes(2)
    expect(resolve.mock.calls[0][0].signal.aborted).toBe(true)
  })
})
