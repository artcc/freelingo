'use client'

import Link from 'next/link'
import { useLocale, useTranslations } from 'next-intl'
import {
  ArrowUpRight,
  BookOpen,
  Check,
  Flame,
  Sparkles,
  Target,
} from 'lucide-react'

export interface ActivityDay {
  date: string
  active: boolean
  xp: number
}

export function ProgressOverview({
  xp,
  todayXp,
  streak,
  activity,
  lessons,
  correct,
  total,
  showDetails = true,
}: {
  xp: number
  todayXp: number
  streak: number
  activity: ActivityDay[]
  lessons: number
  correct: number
  total: number
  showDetails?: boolean
}) {
  const t = useTranslations('dashboardProgress')
  const locale = useLocale()
  const number = new Intl.NumberFormat(locale)
  const todayActive = activity.at(-1)?.active ?? false
  const maxXp = Math.max(1, ...activity.map((day) => day.xp))

  return (
    <section
      aria-labelledby="dashboard-progress-title"
      className="mb-8 space-y-3"
    >
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <h2
            id="dashboard-progress-title"
            className="text-fl-fg text-lg font-semibold"
          >
            {t('title')}
          </h2>
          <p className="text-fl-muted-2 mt-1 text-sm">{t('scope')}</p>
        </div>
        {showDetails && (
          <Link
            href="/progress"
            className="text-fl-accent inline-flex items-center gap-1 text-sm font-medium hover:underline"
          >
            {t('details')}
            <ArrowUpRight className="size-4" aria-hidden="true" />
          </Link>
        )}
      </div>
      <div className="grid gap-3 sm:grid-cols-2">
        <div className="border-fl-accent/35 bg-fl-surface relative overflow-hidden border p-5 sm:p-6">
          <div
            className="bg-fl-accent absolute inset-y-0 left-0 w-1"
            aria-hidden="true"
          />
          <div className="flex items-center justify-between gap-3">
            <span className="text-fl-muted-1 flex items-center gap-2 text-sm font-medium">
              <Sparkles className="text-fl-accent size-5" aria-hidden="true" />
              {t('experience')}
            </span>
            <span className="bg-fl-accent/10 text-fl-accent px-2.5 py-1 text-xs font-semibold tabular-nums">
              {t('todayXp', { xp: number.format(todayXp) })}
            </span>
          </div>
          <div className="mt-5 flex items-end justify-between gap-4">
            <p className="text-fl-fg min-w-0 text-4xl font-semibold tracking-tight break-words tabular-nums sm:text-5xl">
              {number.format(xp)}
              <span className="text-fl-muted-2 ml-2 text-sm font-medium tracking-normal">
                XP
              </span>
            </p>
            <div
              className="flex h-12 shrink-0 items-end gap-1.5"
              aria-hidden="true"
            >
              {activity.map((day) => (
                <div
                  key={day.date}
                  className={`w-2.5 transition-[height] duration-500 motion-reduce:transition-none ${day.xp ? 'bg-fl-accent' : 'bg-fl-border'}`}
                  style={{ height: `${Math.max(8, (day.xp / maxXp) * 100)}%` }}
                />
              ))}
            </div>
          </div>
          <p className="text-fl-muted-2 mt-4 text-sm">{t('experienceHint')}</p>
        </div>
        <div className="border-fl-border bg-fl-surface border p-5 sm:p-6">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <span className="text-fl-muted-1 flex items-center gap-2 text-sm font-medium">
              <Flame className="text-fl-accent size-5" aria-hidden="true" />
              {t('streak')}
            </span>
            <span
              className={`inline-flex items-center gap-1.5 text-xs font-medium ${todayActive ? 'text-fl-accent' : 'text-fl-muted-2'}`}
            >
              {todayActive && <Check className="size-3.5" aria-hidden="true" />}
              {t(todayActive ? 'practisedToday' : 'readyToday')}
            </span>
          </div>
          <p className="text-fl-fg mt-4 text-4xl font-semibold tracking-tight tabular-nums">
            {number.format(streak)}
            <span className="text-fl-muted-2 ml-2 text-sm font-medium tracking-normal">
              {t('days', { count: streak })}
            </span>
          </p>
          <ul aria-label={t('week')} className="mt-4 grid grid-cols-7 gap-2">
            {activity.map((day, index) => {
              const date = new Date(`${day.date}T12:00:00Z`)
              const fullDate = new Intl.DateTimeFormat(locale, {
                dateStyle: 'medium',
                timeZone: 'UTC',
              }).format(date)
              return (
                <li
                  key={day.date}
                  aria-label={`${fullDate}: ${t(day.active ? 'activeDay' : 'inactiveDay')}`}
                  className="text-center"
                >
                  <span
                    className={`mx-auto flex size-7 items-center justify-center border ${day.active ? 'border-fl-accent bg-fl-accent text-fl-accent-fg' : 'border-fl-border text-fl-muted-3'} ${index === activity.length - 1 ? 'outline-fl-accent/50 outline outline-offset-2' : ''}`}
                    aria-hidden="true"
                  >
                    {day.active ? (
                      <Check className="size-4" />
                    ) : (
                      <span className="size-1 bg-current" />
                    )}
                  </span>
                  <span
                    className="text-fl-muted-2 mt-2 block text-xs"
                    aria-hidden="true"
                  >
                    {new Intl.DateTimeFormat(locale, {
                      weekday: 'narrow',
                      timeZone: 'UTC',
                    }).format(date)}
                  </span>
                </li>
              )
            })}
          </ul>
          <p className="text-fl-muted-2 mt-3 text-xs">{t('utcHint')}</p>
        </div>
      </div>
      <div className="border-fl-border bg-fl-surface grid border sm:grid-cols-2">
        <div className="border-fl-border flex items-center gap-4 border-b px-5 py-4 sm:border-r sm:border-b-0">
          <BookOpen
            className="text-fl-muted-2 size-5 shrink-0"
            aria-hidden="true"
          />
          <div>
            <p className="text-fl-muted-1 text-sm">{t('lessons')}</p>
            <p className="text-fl-fg mt-1 text-2xl font-semibold tabular-nums">
              {number.format(lessons)}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-4 px-5 py-4">
          <Target
            className="text-fl-muted-2 size-5 shrink-0"
            aria-hidden="true"
          />
          <div>
            <p className="text-fl-muted-1 text-sm">{t('accuracy')}</p>
            <p className="text-fl-fg mt-1 text-2xl font-semibold tabular-nums">
              {total
                ? `${number.format(Math.round((correct / total) * 100))}%`
                : '—'}
            </p>
            <p className="text-fl-muted-2 mt-1 text-xs">
              {total
                ? t('correctAnswers', {
                    correct: number.format(correct),
                    total: number.format(total),
                  })
                : t('noExercises')}
            </p>
          </div>
        </div>
      </div>
    </section>
  )
}
