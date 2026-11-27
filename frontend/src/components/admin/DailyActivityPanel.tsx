'use client'

import { useEffect, useState } from 'react'
import { useLocale, useTranslations } from 'next-intl'
import { AdminPanel } from '@/components/admin/AdminShell'
import { AnalyticsTable } from '@/components/admin/AnalyticsTable'
import { apiFetch } from '@/lib/api'

export interface ActivityDay {
  date: string
  learners: number
}

function DailyActivityChart({ days }: { days: ActivityDay[] }) {
  const t = useTranslations('adminAnalytics')
  const locale = useLocale()
  const date = new Intl.DateTimeFormat(locale, {
    dateStyle: 'medium',
    timeZone: 'UTC',
  })
  if (!days.length) return <p>{t('empty')}</p>

  const maximum = Math.max(1, ...days.map((day) => day.learners))
  return (
    <>
      <div aria-hidden="true" className="text-fl-muted-2 text-xs tabular-nums">
        <div className="flex gap-2">
          <div className="flex flex-col justify-between text-end">
            <span>{maximum}</span>
            <span>0</span>
          </div>
          <div className="border-fl-border flex h-28 flex-1 items-end gap-px border-y">
            {days.map((day) => (
              <div
                key={day.date}
                className="flex h-full flex-1 items-end"
                title={`${date.format(new Date(day.date))}: ${day.learners}`}
              >
                <div
                  className="bg-fl-accent w-full"
                  style={{ height: `${(day.learners / maximum) * 100}%` }}
                />
              </div>
            ))}
          </div>
        </div>
        <div className="mt-1 flex justify-between">
          <span>{date.format(new Date(days[0].date))}</span>
          {days.length > 1 && (
            <span>{date.format(new Date(days[days.length - 1].date))}</span>
          )}
        </div>
      </div>
      <details>
        <summary className="text-fl-fg cursor-pointer text-sm">
          {t('dailyValues')}
        </summary>
        <AnalyticsTable
          title={t('daily')}
          headers={[t('date'), t('learners')]}
          rows={days.map((day) => ({
            key: day.date,
            cells: [date.format(new Date(day.date)), day.learners],
          }))}
        />
      </details>
    </>
  )
}

export function OverviewActivityPanel() {
  const [days, setDays] = useState<ActivityDay[] | null>(null)
  const [error, setError] = useState(false)

  useEffect(() => {
    const controller = new AbortController()
    async function load() {
      try {
        const response = await apiFetch('/api/admin/analytics/activity', {
          signal: controller.signal,
          cache: 'no-store',
        })
        if (!response.ok) throw new Error()
        const data: { days: ActivityDay[] } = await response.json()
        if (!controller.signal.aborted) setDays(data.days)
      } catch {
        if (!controller.signal.aborted) setError(true)
      }
    }
    void load()
    return () => controller.abort()
  }, [])

  return <DailyActivityPanel days={days} error={error} />
}

export function DailyActivityPanel({
  days,
  error = false,
}: {
  days: ActivityDay[] | null
  error?: boolean
}) {
  const t = useTranslations('adminAnalytics')
  const common = useTranslations('common')
  return (
    <AdminPanel title={t('daily')}>
      <div className="space-y-3 p-5">
        <p className="text-fl-muted-2 text-sm">{t('dailyDesc')}</p>
        {error ? (
          <p role="alert" className="text-fl-error-fg">
            {common('errorMessage')}
          </p>
        ) : days ? (
          <DailyActivityChart days={days} />
        ) : (
          <p role="status">{common('loading')}</p>
        )}
      </div>
    </AdminPanel>
  )
}
