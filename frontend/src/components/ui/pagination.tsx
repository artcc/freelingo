'use client'

import { useEffect, useRef } from 'react'
import { useLoadingStore } from '@/store/loading'

interface PaginationProps {
  /** 0-indexed current page. */
  page: number
  /** Total number of pages. */
  totalPages: number
  /** Disables buttons during fetch. */
  loading?: boolean
  /** Called with the new 0-indexed page number. */
  onPageChange: (page: number) => void
  /** Translated text for the previous button. */
  prevLabel: string
  /** Translated text for the next button. */
  nextLabel: string
  /** Pre-formatted page info shown between buttons (e.g. "2 / 5"). Falls back to "page+1 / totalPages". */
  pageInfo?: string
  /** Extra classes for the outer container. */
  className?: string
}

export function Pagination({
  page,
  totalPages,
  loading = false,
  onPageChange,
  prevLabel,
  nextLabel,
  pageInfo,
  className = '',
}: PaginationProps) {
  const incDone = useRef(false)

  useEffect(() => {
    if (loading && !incDone.current) {
      incDone.current = true
      useLoadingStore.getState().inc()
    }
    if (!loading && incDone.current) {
      useLoadingStore.getState().dec()
      incDone.current = false
    }
    return () => {
      if (incDone.current) {
        useLoadingStore.getState().dec()
        incDone.current = false
      }
    }
  }, [loading])

  if (totalPages <= 1) return null

  const isFirst = page <= 0
  const isLast = page >= totalPages - 1
  const isDisabled = loading

  const info = pageInfo ?? `${page + 1} / ${totalPages}`

  return (
    <div
      className={`border-fl-border bg-fl-surface flex items-center justify-between border px-6 py-3 ${className}`}
    >
      <button
        onClick={() => onPageChange(Math.max(0, page - 1))}
        disabled={isFirst || isDisabled}
        className="border-fl-border text-fl-muted-1 hover:text-fl-fg hover:border-fl-border-2 border px-4 py-2 font-mono text-xs tracking-widest uppercase transition-colors disabled:cursor-not-allowed disabled:opacity-20"
      >
        {prevLabel}
      </button>
      <span className="text-fl-label text-fl-muted-2 font-mono tracking-widest">
        {info}
      </span>
      <button
        onClick={() => onPageChange(page + 1)}
        disabled={isLast || isDisabled}
        className="border-fl-border text-fl-muted-1 hover:text-fl-fg hover:border-fl-border-2 border px-4 py-2 font-mono text-xs tracking-widest uppercase transition-colors disabled:cursor-not-allowed disabled:opacity-20"
      >
        {nextLabel}
      </button>
    </div>
  )
}
