'use client'

import { useCallback, useEffect, useRef } from 'react'
import { useTranslations } from 'next-intl'
import { useLanguageStore } from '@/store/language'
import {
  ExerciseGenerationError,
  resolveExercise,
} from '@/lib/exercise-generation'

export function useExerciseGeneration<T>({
  feature,
  language,
  studyPlanId,
  level,
  onExercise,
  setPageState,
  setError,
  dismissTooltip,
}: {
  feature: 'listening' | 'reading'
  language: string | undefined
  studyPlanId?: number
  level?: string | null
  onExercise: (exercise: T) => void
  setPageState: (state: 'loading' | 'generating' | 'idle' | 'exercise') => void
  setError: (error: string) => void
  dismissTooltip: () => void
}) {
  const t = useTranslations('exerciseGeneration')
  const tCommon = useTranslations('common')
  const active = useRef<AbortController | null>(null)
  const needsRefresh = useLanguageStore((s) => s.needsRefresh)
  const fetchLanguages = useLanguageStore((s) => s.fetchLanguages)

  const run = useCallback(
    async (generate: boolean, voice = '') => {
      // Prevent repeated clicks from starting concurrent operations, including before POST returns.
      if (generate && active.current) return
      active.current?.abort()
      const controller = new AbortController()
      active.current = controller
      setError('')
      dismissTooltip()
      setPageState(
        generate && language && !needsRefresh ? 'generating' : 'loading'
      )
      try {
        if (!language || needsRefresh) {
          const loaded = await fetchLanguages(controller.signal)
          if (controller.signal.aborted) return
          if (!loaded || !useLanguageStore.getState().activeLanguage) {
            throw new ExerciseGenerationError('unavailable')
          }
          // The updated context reruns the effect below with a read-only lookup.
          return
        }
        const exercise = await resolveExercise<T>({
          feature,
          context: {
            target_language: language,
            study_plan_id: studyPlanId,
            level: level ?? undefined,
          },
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
    [
      feature,
      language,
      studyPlanId,
      level,
      needsRefresh,
      fetchLanguages,
      setError,
      dismissTooltip,
      setPageState,
      onExercise,
      t,
      tCommon,
    ]
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

  return { loadNext, generate, needsContext: !language || needsRefresh }
}
