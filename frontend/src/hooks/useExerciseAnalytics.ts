'use client'

import { useCallback, useEffect, useRef } from 'react'
import { apiUrl } from '@/lib/api'
import type { ExerciseContext } from '@/lib/exercise-generation'
import { useAuthStore } from '@/store/auth'
import { useLanguageStore } from '@/store/language'
import { useConfigStore } from '@/store/config'

export function useExerciseAnalytics(feature: 'listening' | 'reading') {
  const attempt = useRef<{
    id: string
    sessionVersion: number
    controller: AbortController
  } | null>(null)

  const reset = useCallback(() => {
    attempt.current?.controller.abort()
    attempt.current = null
  }, [])

  useEffect(() => reset, [reset])
  useEffect(
    () =>
      useConfigStore.subscribe((state) => {
        // Observe disabling even if React batches a subsequent reactivation.
        if (!state.analyticsEnabled) reset()
      }),
    [reset]
  )

  const start = useCallback(
    (exerciseId: number, context: ExerciseContext | null, replay: boolean) => {
      if (!useConfigStore.getState().analyticsEnabled) return
      if (!context) return
      const language = useLanguageStore.getState()
      const plan = language.userLanguages.find((item) => item.is_active)?.plan
      const auth = useAuthStore.getState()
      if (
        !auth.accessToken ||
        language.isSwitching ||
        language.needsRefresh ||
        language.activeLanguage?.code !== context.target_language ||
        plan?.id !== context.study_plan_id ||
        plan?.cefr_level !== context.level
      )
        return
      if (attempt.current?.sessionVersion === auth.sessionVersion) return
      reset()
      try {
        const current = {
          id: crypto.randomUUID(),
          sessionVersion: auth.sessionVersion,
          controller: new AbortController(),
        }
        attempt.current = current
        // No auth refresh or global loading: this signal cannot disrupt practice.
        void fetch(apiUrl(`/api/${feature}/started`), {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${auth.accessToken}`,
            'Content-Type': 'application/json',
            'X-Exercise-Attempt': current.id,
          },
          body: JSON.stringify({ exercise_id: exerciseId, context, replay }),
          signal: AbortSignal.any([
            current.controller.signal,
            AbortSignal.timeout(5_000),
          ]),
        }).catch(() => {})
      } catch {
        // Analytics is optional, including on browsers without UUID support.
      }
    },
    [feature, reset]
  )

  const headers = useCallback((): Record<string, string> => {
    if (!useConfigStore.getState().analyticsEnabled) return {}
    const current = attempt.current
    return current &&
      current.sessionVersion === useAuthStore.getState().sessionVersion
      ? { 'X-Exercise-Attempt': current.id }
      : {}
  }, [])

  return { start, reset, headers }
}
