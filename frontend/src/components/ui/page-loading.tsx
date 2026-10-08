'use client'

import { useEffect, useMemo } from 'react'
import { useTranslations } from 'next-intl'
import { Loader2 } from 'lucide-react'
import LinguAvatar, {
  type LinguAnimation,
} from '@/components/lingu/LinguAvatar'
import { useLoadingStore } from '@/store/loading'
import { usePageLoadingPresentation } from './page-loading-boundary'

interface PageLoadingProps {
  /** Translated label. Defaults to common.loading. */
  label?: string
  /** Optional subtext shown below the main label. */
  subtext?: string
  /** Whether to show the activity indicator in inline mode. Default true. */
  showDot?: boolean
  /** Render as full-screen centered block. Set false for inline usage. */
  fullScreen?: boolean
  /** Extra classes for the outer container / span. */
  className?: string
}

export function PageLoading({
  label,
  subtext,
  showDot = true,
  fullScreen = true,
  className = '',
}: PageLoadingProps) {
  const t = useTranslations('common')

  useEffect(() => {
    const { inc, dec } = useLoadingStore.getState()
    inc()
    return () => {
      dec()
    }
  }, [])

  const text = label ?? t('loading')
  const presentation = useMemo(
    () => (
      <PageLoadingPresentation
        label={text}
        subtext={subtext}
        className={className}
      />
    ),
    [text, subtext, className]
  )
  const managed = usePageLoadingPresentation(fullScreen ? presentation : null)

  if (!fullScreen) {
    return (
      <span
        className={`text-fl-muted-2 font-sans text-sm leading-relaxed ${className}`}
        role="status"
        aria-busy="true"
        aria-label={text}
      >
        {showDot && (
          <Loader2
            aria-hidden="true"
            className="mr-2 inline-block size-3.5 align-middle motion-safe:animate-spin"
          />
        )}
        {text}
      </span>
    )
  }

  return managed ? null : <div className="h-dvh">{presentation}</div>
}

/** Shared geometry: secondary text never moves the centered avatar/title block. */
export function PageLoadingPresentation({
  label,
  subtext,
  warning,
  animation = 'reposo',
  heading = false,
  className = '',
}: {
  label: string
  subtext?: string
  warning?: string
  animation?: LinguAnimation
  heading?: boolean
  className?: string
}) {
  const Label = heading ? 'h1' : 'p'

  return (
    <div
      className={`grid h-full grid-rows-[minmax(1.5rem,1fr)_auto_minmax(1.5rem,1fr)] justify-items-center overflow-y-auto px-6 text-center ${className}`}
      role="status"
      aria-busy="true"
      aria-label={label}
    >
      <div aria-hidden="true" />
      <div className="flex w-full max-w-sm flex-col items-center gap-6">
        <LinguAvatar
          animation={animation}
          className="h-[150px] w-[150px] shrink-0 md:h-[195px] md:w-[195px]"
        />
        <Label className="text-fl-fg font-sans text-lg leading-7 font-medium">
          {label}
        </Label>
      </div>
      <div className="w-full max-w-sm space-y-6 pt-2 pb-6">
        {subtext && (
          <p className="text-fl-muted-1 font-sans text-sm leading-relaxed">
            {subtext}
          </p>
        )}
        {warning && (
          <p className="text-fl-muted-2 font-sans text-sm leading-5">
            {warning}
          </p>
        )}
      </div>
    </div>
  )
}
