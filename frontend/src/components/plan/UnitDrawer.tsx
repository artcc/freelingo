'use client'

import { useRef } from 'react'
import { useTranslations } from 'next-intl'
import { Dialog } from '@base-ui/react/dialog'
import { ArrowRight, Check, ChevronDown, Circle, X } from 'lucide-react'
import type { CurriculumUnit } from '@/data/curriculum'
import { TargetLanguageText } from '@/components/TargetLanguageText'

interface Lesson {
  id: number | null
  title: string
  lesson_type: string
  week: number
  day: number
  completed: boolean
  action?: 'start' | 'continue' | 'review'
}

interface Props {
  unit: CurriculumUnit
  lessons: Lesson[]
  onClose: () => void
  onStartLesson: (lessonId: number) => void
  languageCode?: string
}

export default function UnitDrawer({
  unit,
  lessons,
  onClose,
  onStartLesson,
  languageCode,
}: Props) {
  const t = useTranslations('plan')
  const tCommon = useTranslations('common')
  const titleRef = useRef<HTMLHeadingElement>(null)
  const completedCount = lessons.filter((lesson) => lesson.completed).length
  const progress = lessons.length
    ? Math.round((completedCount / lessons.length) * 100)
    : 0
  const progressSummary = t('progressSummary', {
    completed: completedCount,
    total: lessons.length,
  })

  const lessonTypeLabel: Record<string, string> = {
    grammar: t('lessonTypes.grammar'),
    vocabulary: t('lessonTypes.vocabulary'),
    reading: t('lessonTypes.reading'),
    writing: t('lessonTypes.writing'),
    listening: t('lessonTypes.listening'),
    conversation: t('lessonTypes.conversation'),
    review: t('lessonTypes.review'),
    level_test: t('lessonTypes.level_test'),
  }

  return (
    <Dialog.Root
      open
      onOpenChange={(open) => {
        if (!open) onClose()
      }}
    >
      <Dialog.Portal>
        <Dialog.Backdrop
          data-slot="unit-dialog-backdrop"
          className="bg-fl-bg/80 fixed inset-0 z-50 backdrop-blur-sm"
        />
        <Dialog.Popup
          initialFocus={titleRef}
          className="border-fl-border bg-fl-surface text-fl-fg fixed bottom-0 left-1/2 z-50 flex max-h-[90dvh] w-full -translate-x-1/2 flex-col overflow-hidden border shadow-2xl outline-none sm:top-1/2 sm:bottom-auto sm:w-[calc(100%-2rem)] sm:max-w-2xl sm:-translate-y-1/2"
        >
          <header className="border-fl-border shrink-0 space-y-4 border-b p-5 sm:p-6">
            <div className="flex items-start justify-between gap-4">
              <div className="min-w-0 space-y-2">
                <p className="text-fl-accent text-xs font-medium tracking-widest uppercase">
                  <span className="font-code">{unit.level}</span> ·{' '}
                  {t('unitLabel')}{' '}
                  <span className="font-code">
                    {String(unit.unit_number).padStart(2, '0')}
                  </span>
                </p>
                <Dialog.Title
                  ref={titleRef}
                  tabIndex={-1}
                  className="text-xl font-semibold outline-none sm:text-2xl"
                >
                  <TargetLanguageText
                    languageCode={languageCode}
                    className="break-words"
                  >
                    {unit.title}
                  </TargetLanguageText>
                </Dialog.Title>
              </div>
              <Dialog.Close
                aria-label={tCommon('close')}
                className="border-fl-border text-fl-muted-1 hover:bg-fl-surface-2 hover:text-fl-fg focus-visible:outline-fl-fg flex size-10 shrink-0 items-center justify-center border focus-visible:outline-2 focus-visible:outline-offset-2"
              >
                <X className="size-4" aria-hidden="true" />
              </Dialog.Close>
            </div>
            <div className="space-y-2">
              <div className="flex flex-wrap items-baseline justify-between gap-2 text-xs">
                <Dialog.Description className="text-fl-muted-1">
                  {progressSummary}
                </Dialog.Description>
                <span className="text-fl-accent font-code" aria-hidden="true">
                  {progress}%
                </span>
              </div>
              <div
                role="progressbar"
                aria-label={progressSummary}
                aria-valuemin={0}
                aria-valuemax={lessons.length || 1}
                aria-valuenow={completedCount}
                className="bg-fl-border h-1 overflow-hidden"
              >
                <div
                  className="bg-fl-accent h-full"
                  style={{ width: `${progress}%` }}
                />
              </div>
            </div>
          </header>

          <div className="min-h-0 overflow-y-auto overscroll-contain p-5 sm:p-6">
            <h3 className="text-fl-muted-1 mb-3 text-xs font-medium">
              {t('lessonsHeader', { count: lessons.length })}
            </h3>
            {lessons.length === 0 ? (
              <p className="text-fl-muted-1 py-6 text-sm">{t('noLessons')}</p>
            ) : (
              <ol className="space-y-3">
                {lessons.map((lesson) => {
                  const isCurrent =
                    lesson.action === 'start' && !lesson.completed
                  const Icon = lesson.completed
                    ? Check
                    : isCurrent
                      ? ArrowRight
                      : Circle
                  return (
                    <li
                      key={`${lesson.week}:${lesson.day}:${lesson.title}`}
                      aria-current={isCurrent ? 'step' : undefined}
                      className={`border p-4 ${isCurrent ? 'border-fl-accent' : 'border-fl-border'}`}
                    >
                      <div className="flex items-start gap-3">
                        <span
                          role="img"
                          aria-label={t(
                            lesson.completed
                              ? 'completed'
                              : isCurrent
                                ? 'currentLesson'
                                : 'lessonPending'
                          )}
                          className={`mt-0.5 shrink-0 ${isCurrent ? 'text-fl-accent' : 'text-fl-muted-1'}`}
                        >
                          <Icon className="size-5" aria-hidden="true" />
                        </span>
                        <div className="min-w-0 flex-1">
                          {isCurrent && (
                            <p className="text-fl-accent mb-1 text-xs font-medium">
                              {t('currentLesson')}
                            </p>
                          )}
                          <TargetLanguageText
                            as="p"
                            languageCode={languageCode}
                            className="text-fl-fg-2 text-base font-medium break-words"
                          >
                            {lesson.title}
                          </TargetLanguageText>
                          <div className="mt-3 flex flex-wrap items-center justify-between gap-3">
                            <div className="text-fl-muted-1 space-y-1 text-xs">
                              <p>
                                {lessonTypeLabel[lesson.lesson_type] ??
                                  lesson.lesson_type}
                              </p>
                              <p>
                                {t('weekDay', {
                                  week: lesson.week,
                                  day: lesson.day,
                                })}
                              </p>
                            </div>
                            {lesson.id != null && lesson.action && (
                              <button
                                onClick={() => onStartLesson(lesson.id!)}
                                className={`focus-visible:outline-fl-fg w-full shrink-0 px-4 py-2.5 text-sm font-medium transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 sm:w-auto ${
                                  isCurrent
                                    ? 'bg-fl-fg text-fl-bg hover:bg-fl-fg/90'
                                    : 'border-fl-border text-fl-fg hover:bg-fl-surface-2 border'
                                }`}
                              >
                                {lesson.action === 'review'
                                  ? t('reviewLesson')
                                  : lesson.action === 'continue'
                                    ? t('resume')
                                    : `${tCommon('start')} →`}
                              </button>
                            )}
                          </div>
                        </div>
                      </div>
                    </li>
                  )
                })}
              </ol>
            )}

            {unit.grammar_points.length > 0 && (
              <details className="border-fl-border group mt-5 border-t pt-4">
                <summary className="text-fl-muted-1 focus-visible:outline-fl-fg flex cursor-pointer list-none items-center justify-between gap-3 text-sm focus-visible:outline-2 focus-visible:outline-offset-2 [&::-webkit-details-marker]:hidden">
                  {t('grammarCovered')}
                  <ChevronDown
                    className="size-4 shrink-0 transition-transform group-open:rotate-180 motion-reduce:transition-none"
                    aria-hidden="true"
                  />
                </summary>
                <div className="mt-3 flex flex-wrap gap-2">
                  {unit.grammar_points.map((gp) => (
                    <span
                      key={gp}
                      className="border-fl-border text-fl-muted-1 max-w-full border px-2.5 py-1.5 text-xs break-words"
                    >
                      {gp}
                    </span>
                  ))}
                </div>
              </details>
            )}
          </div>

          <footer className="border-fl-border flex shrink-0 justify-end border-t px-5 py-4 sm:px-6">
            <Dialog.Close className="border-fl-border text-fl-fg hover:bg-fl-surface-2 focus-visible:outline-fl-fg w-full border px-5 py-2.5 text-sm focus-visible:outline-2 focus-visible:outline-offset-2 sm:w-auto">
              {tCommon('close')}
            </Dialog.Close>
          </footer>
        </Dialog.Popup>
      </Dialog.Portal>
    </Dialog.Root>
  )
}
