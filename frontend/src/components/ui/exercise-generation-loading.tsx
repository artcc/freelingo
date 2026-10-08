'use client'

import { useEffect, useMemo } from 'react'
import { useLoadingStore } from '@/store/loading'
import { usePageLoadingPresentation } from './page-loading-boundary'
import { PageLoadingPresentation } from './page-loading'

interface ExerciseGenerationLoadingProps {
  label: string
  description: string
  warning?: string
}

export function ExerciseGenerationLoading({
  label,
  description,
  warning,
}: ExerciseGenerationLoadingProps) {
  useEffect(() => {
    // Preserve PageLoading's global activity slot throughout generation.
    const { inc, dec } = useLoadingStore.getState()
    inc()
    return () => {
      dec()
    }
  }, [])

  const presentation = useMemo(
    () => (
      <PageLoadingPresentation
        label={label}
        subtext={description}
        warning={warning}
        animation="pensando"
        heading
      />
    ),
    [label, description, warning]
  )
  const managed = usePageLoadingPresentation(presentation)
  return managed ? null : <div className="h-dvh">{presentation}</div>
}
