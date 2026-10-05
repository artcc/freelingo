'use client'

import { useCallback, useEffect, useRef } from 'react'
import { useTranslations } from 'next-intl'
import {
  ExerciseGenerationError,
  resolveExercise,
} from '@/lib/exercise-generation'

export function useExerciseGeneration<T>({
  feature,
  language,
  onExercise,
  setPageState,
  setError,
  dismissTooltip,
}: {
  feature: 'listening' | 'reading'
  language: string | undefined
  onExercise: (exercise: T) => void
  setPageState: (state: 'loading' | 'generating' | 'idle' | 'exercise') => void
  setError: (error: string) => void
  dismissTooltip: () => void
}) {
  const t = useTranslations('exerciseGeneration')
  const tCommon = useTranslations('common')
  const active = useRef<AbortController | null>(null)

  const run = useCallback(
    async (generate: boolean, voice = '') => {
      // Prevent repeated clicks from starting concurrent operations, including before POST returns.
      if (generate && active.current) return
      active.current?.abort()
      const controller = new AbortController()
      active.current = controller
      setError('')
      dismissTooltip()
      setPageState(generate ? 'generating' : 'loading')
      try {
        const exercise = await resolveExercise<T>({
          feature,
          signal: controller.signal,
          generate,
          voice,
          onGenerating: () => {
            if (!controller.signal.aborted) setPageState('generating')
          },
        })
        if (controller.signal.aborted) return
        if (exercise) onExercise(exercise)
        setPageState(exercise ? 'exercise' : 'idle')
      } catch (error) {
        if (controller.signal.aborted) return
        const code =
          error instanceof ExerciseGenerationError ? error.code : 'unavailable'
        setError(code === 'noActivePlan' ? tCommon('noActivePlan') : t(code))
        setPageState('idle')
      } finally {
        if (active.current === controller) active.current = null
      }
    },
    [feature, setError, dismissTooltip, setPageState, onExercise, t, tCommon]
  )

  const loadNext = useCallback(() => run(false), [run])
  const generate = useCallback((voice = '') => run(true, voice), [run])

  useEffect(() => {
    void loadNext()
    return () => {
      active.current?.abort()
      active.current = null
    }
  }, [loadNext, language])

  return { loadNext, generate }
}
