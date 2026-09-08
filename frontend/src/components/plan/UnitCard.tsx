'use client'

import { type ReactNode } from 'react'
import { useTranslations } from 'next-intl'

interface UnitStatus {
  completed: boolean
  active: boolean
  locked: boolean
  isLevelTest: boolean
}

interface Props {
  title: string
  index: number
  lessonCount: number
  grammarCount: number
  competency: number // 0–1, completion ratio
  status: UnitStatus
  onClick: () => void
  /** When provided and status.active, an EMPEZAR CTA is rendered on the card */
  onStartLesson?: () => void
}

function StatusIcon({ status }: { status: UnitStatus }): ReactNode {
  if (status.isLevelTest) return <span className="text-fl-muted-1">⊞</span>
  if (status.completed) return <span className="text-fl-fg">✓</span>
  if (status.active) return <span className="text-fl-fg animate-pulse">●</span>
  if (status.locked) return <span className="text-fl-muted-3">○</span>
  return <span className="text-fl-muted-2">◦</span>
}

export default function UnitCard({
  title,
  index,
  lessonCount,
  grammarCount,
  competency,
  status,
  onClick,
  onStartLesson,
}: Props) {
  const t = useTranslations('plan')
  const tCommon = useTranslations('common')
  const barWidth = Math.round(competency * 100)

  return (
    <div
      className={`w-full border transition-colors ${
        status.locked
          ? 'border-fl-border opacity-40'
          : status.active
            ? 'border-fl-fg bg-fl-surface'
            : 'border-fl-border bg-fl-surface'
      }`}
    >
      {/* Clickable card header — opens drawer */}
      <button
        onClick={onClick}
        disabled={status.locked}
        className={`group focus-visible:outline-fl-fg w-full text-left focus-visible:outline-2 focus-visible:outline-offset-2 ${
          status.locked
            ? 'cursor-default'
            : status.active
              ? 'hover:bg-fl-surface-2'
              : 'hover:border-fl-border-2'
        }`}
        aria-label={t('unitAriaLabel', { index: index + 1, title })}
      >
        {/* Top bar: status + index + title */}
        <div className="flex items-center gap-3 px-4 py-3">
          <span className="w-4 shrink-0 font-mono text-base">
            <StatusIcon status={status} />
          </span>
          <div className="min-w-0 flex-1">
            <div className="flex items-center gap-2">
              <span className="text-fl-hint text-fl-muted-3 shrink-0 font-mono tracking-widest uppercase">
                {String(index + 1).padStart(2, '0')}
              </span>
              <span
                className={`text-fl-caption truncate font-mono ${
                  status.locked
                    ? 'text-fl-muted-3'
                    : 'text-fl-fg-2 group-hover:text-fl-fg'
                }`}
              >
                {title}
              </span>
            </div>
            <div className="mt-1 flex flex-wrap items-center gap-x-3 gap-y-1">
              <span className="text-fl-caption text-fl-muted-1 font-mono">
                {t('nLessons', { count: lessonCount })}
              </span>
              {grammarCount > 0 && (
                <span className="text-fl-caption text-fl-muted-1 font-mono">
                  {t('nGrammar', { count: grammarCount })}
                </span>
              )}
              {status.isLevelTest && (
                <span className="text-fl-hint text-fl-muted-2 border-fl-border border px-1.5 py-0.5 font-mono tracking-widest uppercase">
                  {t('levelTestLabel')}
                </span>
              )}
            </div>
          </div>
          {!status.locked && (
            <span className="text-fl-caption text-fl-muted-1 shrink-0 font-mono">
              {barWidth}%
            </span>
          )}
        </div>

        {/* Progress bar */}
        {!status.locked && (
          <div className="bg-fl-border h-1">
            <div
              className="bg-fl-fg h-full transition-[width] duration-300 motion-reduce:transition-none"
              style={{ width: `${barWidth}%` }}
            />
          </div>
        )}
      </button>

      {/* EMPEZAR CTA — only shown on the active unit when a lesson is ready */}
      {status.active && onStartLesson && (
        <div className="border-fl-fg/30 flex justify-end border-t px-4 py-2.5">
          <button
            onClick={onStartLesson}
            className="bg-fl-fg text-fl-bg hover:bg-fl-fg/90 focus-visible:outline-fl-fg px-4 py-2 font-mono text-xs font-bold tracking-widest uppercase transition-colors focus-visible:outline-2 focus-visible:outline-offset-2"
          >
            {tCommon('start')} →
          </button>
        </div>
      )}
    </div>
  )
}
