'use client'

import { useEffect, useMemo } from 'react'
import Image from 'next/image'
import { useTranslations } from 'next-intl'
import { Loader2 } from 'lucide-react'
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

/** A fixed indicator slot anchors both phases independently of all wrapping text. */
export function PageLoadingPresentation({
  label,
  subtext,
  warning,
  artwork = false,
  heading = false,
  className = '',
}: {
  label: string
  subtext?: string
  warning?: string
  artwork?: boolean
  heading?: boolean
  className?: string
}) {
  const Label = heading ? 'h1' : 'p'

  return (
    <div
      className={`h-full overflow-y-auto px-6 text-center ${className}`}
      role="status"
      aria-label={label}
      tabIndex={0}
    >
      <div
        className={`grid h-full justify-items-center ${
          artwork
            ? 'min-h-[123px] grid-rows-[minmax(1.5rem,1fr)_75px_minmax(1.5rem,1fr)] md:min-h-[198px] md:grid-rows-[minmax(1.5rem,1fr)_150px_minmax(1.5rem,1fr)]'
            : 'min-h-[72px] grid-rows-[minmax(1.5rem,1fr)_24px_minmax(1.5rem,1fr)]'
        }`}
      >
        <div aria-hidden="true" />
        <div
          aria-hidden="true"
          className={`relative flex items-center justify-center ${
            artwork ? 'size-[75px] md:size-[150px]' : 'size-6'
          }`}
        >
          {artwork ? (
            <Image
              src="/logo.png"
              alt=""
              width={150}
              height={150}
              sizes="(min-width: 768px) 150px, 75px"
              className="h-full w-full object-contain"
            />
          ) : (
            <Loader2 className="text-fl-muted-2 size-6 motion-safe:animate-spin" />
          )}
        </div>
        <div
          className={`w-full max-w-sm space-y-2 self-start pb-6 ${artwork ? 'pt-6' : 'pt-4'}`}
        >
          <Label className="text-fl-fg font-sans text-lg leading-7 font-medium">
            {label}
          </Label>
          {subtext && (
            <p className="text-fl-muted-1 font-sans text-sm leading-relaxed">
              {subtext}
            </p>
          )}
          {warning && (
            <p className="text-fl-muted-2 pt-4 font-sans text-sm leading-5">
              {warning}
            </p>
          )}
        </div>
      </div>
    </div>
  )
}
