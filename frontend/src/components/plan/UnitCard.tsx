'use client'

import { useId, type ReactNode } from 'react'
import { useTranslations } from 'next-intl'
import { Check, ChevronRight, Circle, Flag } from 'lucide-react'
import { TargetLanguageText } from '@/components/TargetLanguageText'

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
  progress: number // 0–1: lesson completion ratio, or assessment score for the level test
  status: UnitStatus
  onClick: () => void
  /** When provided and status.active, an EMPEZAR CTA is rendered on the card */
  onStartLesson?: () => void
  languageCode?: string
  children?: ReactNode
}

function StatusIcon({
  status,
  id,
}: {
  status: UnitStatus
  id: string
}): ReactNode {
  const t = useTranslations('plan')
  const { label, Icon, className } = status.isLevelTest
    ? {
        label: 'levelTestLabel',
        Icon: Flag,
        className: 'text-fl-muted-1 size-4',
      }
    : status.completed
      ? { label: 'completed', Icon: Check, className: 'text-fl-fg size-4' }
      : status.active
        ? {
            label: 'currentUnit',
            Icon: Circle,
            className:
              'text-fl-fg size-2 animate-pulse fill-current motion-reduce:animate-none',
          }
        : status.locked
          ? {
              label: 'unitLocked',
              Icon: Circle,
              className: 'text-fl-muted-3 size-4',
            }
          : {
              label: 'unitAvailable',
              Icon: Circle,
              className: 'text-fl-muted-2 size-2',
            }

  return (
    <span
      id={id}
      role="img"
      aria-label={t(label)}
      className={`bg-fl-bg absolute top-5 -left-12 inline-flex size-9 items-center justify-center rounded-full border sm:-left-14 ${
        status.active
          ? 'border-fl-accent ring-fl-accent/15 ring-4'
          : 'border-fl-border'
      }`}
    >
      <Icon className={className} aria-hidden="true" />
    </span>
  )
}

export default function UnitCard({
  title,
  index,
  lessonCount,
  grammarCount,
  progress,
  status,
  onClick,
  onStartLesson,
  languageCode,
  children,
}: Props) {
  const t = useTranslations('plan')
  const tCommon = useTranslations('common')
  const statusId = useId()
  const barWidth = Math.round(progress * 100)

  return (
    <div
      className={`relative w-full border transition-colors ${
        status.active
          ? 'border-fl-accent bg-fl-surface'
          : status.isLevelTest
            ? 'border-fl-border-2 bg-fl-surface'
            : 'border-fl-border bg-fl-surface'
      }`}
      aria-current={status.active ? 'step' : undefined}
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
        aria-describedby={statusId}
      >
        {/* Top bar: status + index + title */}
        <div className="flex items-center gap-3 px-4 py-4 sm:px-5">
          <StatusIcon status={status} id={statusId} />
          <div className="min-w-0 flex-1">
            <div className="mb-2 flex flex-wrap items-center gap-2">
              <span className="text-fl-muted-1 font-code text-xs">
                {String(index + 1).padStart(2, '0')}
              </span>
              {status.active && !status.isLevelTest && (
                <span className="text-fl-accent text-xs font-medium">
                  {t('currentUnit')}
                </span>
              )}
              {status.completed && !status.isLevelTest && (
                <span className="text-fl-muted-1 text-xs">
                  {t('completed')}
                </span>
              )}
              {status.locked && !status.isLevelTest && (
                <span className="text-fl-muted-1 text-xs">
                  {t('unitLocked')}
                </span>
              )}
              {status.isLevelTest && (
                <span className="text-fl-accent text-xs font-medium">
                  {t('levelTestLabel')}
                </span>
              )}
            </div>
            <TargetLanguageText
              languageCode={languageCode}
              className={`block font-medium break-words ${
                status.active ? 'text-fl-fg text-xl' : 'text-fl-fg-2 text-base'
              }`}
            >
              {title}
            </TargetLanguageText>
            <div className="text-fl-muted-1 mt-2 flex flex-wrap items-center gap-x-3 gap-y-1 text-xs">
              <span>{t('nLessons', { count: lessonCount })}</span>
              {grammarCount > 0 && (
                <span>{t('nGrammar', { count: grammarCount })}</span>
              )}
            </div>
          </div>
          {!status.locked && (
            <div className="text-fl-muted-1 flex shrink-0 flex-col items-end gap-2">
              <span className="font-code text-xs">
                {status.isLevelTest && status.completed && `${t('testScore')} `}
                {barWidth}%
              </span>
              <ChevronRight className="size-4" aria-hidden="true" />
            </div>
          )}
        </div>

        {/* Progress bar */}
        {!status.locked && !status.completed && (
          <div className="bg-fl-border h-1">
            <div
              className="bg-fl-fg h-full transition-[width] duration-300 motion-reduce:transition-none"
              style={{ width: `${barWidth}%` }}
            />
          </div>
        )}
      </button>

      {status.active && children}

      {/* EMPEZAR CTA — only shown on the active unit when a lesson is ready */}
      {status.active && onStartLesson && (
        <div className="border-fl-border flex justify-end border-t px-4 py-4 sm:px-5">
          <button
            onClick={onStartLesson}
            className="bg-fl-fg text-fl-bg hover:bg-fl-fg/90 focus-visible:outline-fl-fg w-full px-5 py-3 text-sm font-semibold transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 sm:w-auto"
          >
            {tCommon('start')} →
          </button>
        </div>
      )}
    </div>
  )
}
