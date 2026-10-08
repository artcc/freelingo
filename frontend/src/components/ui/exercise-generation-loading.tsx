'use client'

import { useEffect } from 'react'
import LinguAvatar from '@/components/lingu/LinguAvatar'
import { useLoadingStore } from '@/store/loading'

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

  return (
    <div
      className="flex min-h-[calc(100vh-56px)] items-center justify-center px-6 py-10 md:min-h-screen"
      role="status"
      aria-label={label}
      aria-busy="true"
    >
      <div className="flex w-full max-w-sm flex-col items-center gap-6 text-center">
        <LinguAvatar
          animation="pensando"
          className="h-[150px] w-[150px] shrink-0 md:h-[195px] md:w-[195px]"
        />
        <div className="space-y-2">
          <h1 className="text-fl-fg font-sans text-lg font-medium">{label}</h1>
          <p className="text-fl-muted-1 font-sans text-sm leading-relaxed">
            {description}
          </p>
        </div>
        <p className="text-fl-muted-2 min-h-10 font-sans text-sm leading-5">
          {warning}
        </p>
      </div>
    </div>
  )
}
