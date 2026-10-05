import { act, renderHook, waitFor } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { useExerciseGeneration } from '@/hooks/useExerciseGeneration'
import { resolveExercise } from '@/lib/exercise-generation'

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
      .mockResolvedValueOnce({ id: 2, target_language: 'es' })
    const { rerender } = renderHook(
      ({ language }) => useExerciseGeneration({ ...options, language }),
      {
        initialProps: { language: 'en-GB' },
      }
    )
    const oldSignal = resolve.mock.calls[0][0].signal
    rerender({ language: 'es' })
    await waitFor(() =>
      expect(onExercise).toHaveBeenCalledWith({ id: 2, target_language: 'es' })
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
})
