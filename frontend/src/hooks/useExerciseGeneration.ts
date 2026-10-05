'use client'

import { useCallback, useEffect, useRef } from 'react'
import { useTranslations } from 'next-intl'
import { useLanguageStore } from '@/store/language'
import {
  ExerciseGenerationError,
  type ExerciseContext,
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
  onExercise: (exercise: T, context: ExerciseContext) => void
  setPageState: (state: 'loading' | 'generating' | 'idle' | 'exercise') => void
  setError: (error: string) => void
  dismissTooltip: () => void
}) {
  const t = useTranslations('exerciseGeneration')
  const tCommon = useTranslations('common')
  const active = useRef<AbortController | null>(null)
  const needsRefresh = useLanguageStore((s) => s.needsRefresh)
  const isSwitching = useLanguageStore((s) => s.isSwitching)
  const fetchLanguages = useLanguageStore((s) => s.fetchLanguages)

  const run = useCallback(
    async (generate: boolean, voice = '') => {
      // A pending switch is not a new exercise load. Keep the current screen intact.
      if (useLanguageStore.getState().isSwitching) return
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
        let exerciseContext: ExerciseContext | undefined
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
          onContext: (context) => {
            exerciseContext = context
          },
          onGenerating: () => {
            if (!controller.signal.aborted) setPageState('generating')
          },
        })
        if (controller.signal.aborted) return
        if (exercise && exerciseContext) onExercise(exercise, exerciseContext)
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
  const lastAutomaticLoad = useRef<typeof loadNext | null>(null)

  useEffect(() => {
    if (isSwitching) {
      // Only interrupted requests need resuming after a rejected switch.
      // A displayed exercise (including a replay) and its answers stay untouched.
      if (active.current) {
        active.current.abort()
        active.current = null
        lastAutomaticLoad.current = null
      }
      return
    }
    if (lastAutomaticLoad.current !== loadNext) {
      lastAutomaticLoad.current = loadNext
      void loadNext()
    }
  }, [loadNext, isSwitching])

  useEffect(() => {
    return () => {
      active.current?.abort()
      active.current = null
      lastAutomaticLoad.current = null
    }
  }, [])

  return { loadNext, generate, needsContext: !language || needsRefresh }
}
