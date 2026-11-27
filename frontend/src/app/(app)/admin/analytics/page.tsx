'use client'

import { useEffect, useState } from 'react'
import { useLocale, useTranslations } from 'next-intl'
import { AdminNav } from '@/components/admin/AdminNav'
import { AdminPageHeader, AdminPanel } from '@/components/admin/AdminShell'
import { AnalyticsTable } from '@/components/admin/AnalyticsTable'
import {
  type ActivityDay,
  DailyActivityPanel,
} from '@/components/admin/DailyActivityPanel'
import { apiFetch } from '@/lib/api'
import {
  ActivityBreakdownPanels,
  type ActivityBreakdown,
} from './ActivityBreakdown'
import { LearnerShare } from './LearnerShare'

const featureLabels = {
  lessons: 'progress.lessons',
  reading: 'nav.reading',
  listening: 'nav.listening',
  games: 'nav.games',
  grammar: 'nav.practiceGrammar',
  chat: 'nav.tutor',
  voice: 'nav.conversation',
} as const

interface PeriodCounts {
  current: number
  previous: number
}

interface AnalyticsReport extends ActivityBreakdown {
  days: ActivityDay[]
  weekly: PeriodCounts
  monthly: PeriodCounts
  repeat_weekly: PeriodCounts
  features: {
    feature: keyof typeof featureLabels
    learners: number
    repeat_learners: number
    volume: number
  }[]
  activation: {
    week: string
    registered: number
    planned: number
    practised: number
  }[]
  retention: { week: string; started: number; returned: number | null }[]
}

function FeatureUsage({ features }: { features: AnalyticsReport['features'] }) {
  const t = useTranslations('adminAnalytics')
  const translate = useTranslations()
  const locale = useLocale()
  const collator = new Intl.Collator(locale)
  const sortedFeatures = features
    .map((row) => ({ ...row, label: translate(featureLabels[row.feature]) }))
    .sort((a, b) => collator.compare(a.label, b.label))
  const maximum = Math.max(1, ...features.map(({ learners }) => learners))

  return (
    <AnalyticsTable
      title={t('features')}
      headers={[t('feature'), t('learners'), t('repeatLearners'), t('volume')]}
      rows={sortedFeatures.map((row) => ({
        key: row.feature,
        cells: [
          row.label,
          <div key="learners" className="flex items-center gap-2">
            <span
              className="shrink-0"
              style={{ width: `${String(maximum).length}ch` }}
            >
              {row.learners}
            </span>
            <div aria-hidden="true" className="bg-fl-bg h-2 min-w-12 flex-1">
              <div
                className="bg-fl-accent h-full"
                style={{ width: `${(row.learners / maximum) * 100}%` }}
              />
            </div>
          </div>,
          <LearnerShare
            key="repeat"
            count={row.repeat_learners}
            total={row.learners}
          />,
          row.volume,
        ],
      }))}
    />
  )
}

function Cohorts({ report }: { report: AnalyticsReport }) {
  const t = useTranslations('adminAnalytics')
  const locale = useLocale()
  const date = new Intl.DateTimeFormat(locale, {
    dateStyle: 'medium',
    timeZone: 'UTC',
  })

  return (
    <div className="grid grid-cols-1 items-start gap-4 xl:grid-cols-2">
      <AdminPanel title={t('activation')}>
        <div className="space-y-3 p-5">
          <p className="text-fl-muted-2 text-sm">{t('activationDesc')}</p>
          <AnalyticsTable
            title={t('activation')}
            headers={[t('week'), t('registered'), t('planned'), t('practised')]}
            rows={report.activation.map(
              ({ week, registered, planned, practised }) => ({
                key: week,
                cells: [
                  date.format(new Date(week)),
                  registered,
                  <LearnerShare
                    key="planned"
                    count={planned}
                    total={registered}
                  />,
                  <LearnerShare
                    key="practised"
                    count={practised}
                    total={registered}
                  />,
                ],
              })
            )}
          />
        </div>
      </AdminPanel>
      <AdminPanel title={t('retention')}>
        <div className="space-y-3 p-5">
          <p className="text-fl-muted-2 text-sm">{t('retentionDesc')}</p>
          <AnalyticsTable
            title={t('retention')}
            headers={[t('week'), t('started'), t('returned')]}
            rows={report.retention.map(({ week, started, returned }) => ({
              key: week,
              cells: [
                date.format(new Date(week)),
                started,
                <LearnerShare
                  key="returned"
                  count={returned}
                  total={started}
                />,
              ],
            }))}
          />
        </div>
      </AdminPanel>
    </div>
  )
}

const ranges = [7, 30, 90] as const
type Range = (typeof ranges)[number]
interface ReportState {
  days: Range
  status: 'loading' | 'ready' | 'error'
  report: AnalyticsReport | null
}

export default function AdminAnalyticsPage() {
  const t = useTranslations('adminAnalytics')
  const admin = useTranslations('admin')
  const common = useTranslations('common')
  const [{ days, status, report }, setResult] = useState<ReportState>({
    days: 30,
    status: 'loading',
    report: null,
  })

  useEffect(() => {
    const controller = new AbortController()
    async function load() {
      try {
        const response = await apiFetch(`/api/admin/analytics?days=${days}`, {
          signal: controller.signal,
          cache: 'no-store',
        })
        if (!response.ok) throw new Error()
        const data: AnalyticsReport = await response.json()
        if (!controller.signal.aborted) {
          setResult((state) =>
            state.days === days
              ? { days, status: 'ready', report: data }
              : state
          )
        }
      } catch {
        if (!controller.signal.aborted) {
          setResult((state) =>
            state.days === days ? { ...state, status: 'error' } : state
          )
        }
      }
    }
    void load()
    return () => controller.abort()
  }, [days])

  function selectRange(next: Range) {
    if (next === days) return
    setResult((state) => ({ ...state, days: next, status: 'loading' }))
  }

  return (
    <div className="mx-auto max-w-6xl space-y-4 p-6">
      <AdminPageHeader eyebrow={admin('title')} title={admin('analytics')} />
      <AdminNav />
      {report && <DailyActivityPanel days={report.days} />}

      {report && (
        <dl className="grid gap-3 md:grid-cols-3">
          {[
            { label: t('weekly'), counts: report.weekly },
            { label: t('monthly'), counts: report.monthly },
            { label: t('repeatWeekly'), counts: report.repeat_weekly },
          ].map(({ label, counts }) => (
            <div
              key={label}
              className="border-fl-border bg-fl-surface space-y-2 border p-4"
            >
              <dt className="text-fl-muted-2 text-sm">{label}</dt>
              <dd className="text-fl-fg text-xl font-semibold tabular-nums">
                {counts.current}
              </dd>
              <dd className="text-fl-muted-2 text-sm">
                {t('previous', { count: counts.previous })}
              </dd>
            </div>
          ))}
        </dl>
      )}

      {report && (
        <ActivityBreakdownPanels
          population={report.population}
          frequency={report.frequency}
          movement={report.movement}
        />
      )}

      <AdminPanel title={t('features')}>
        <div className="space-y-3 p-5">
          <p className="text-fl-muted-2 text-sm">{t('featuresDesc')}</p>
          <fieldset className="flex flex-wrap gap-2">
            <legend className="text-fl-muted-2 mb-2 text-sm">
              {t('range')}
            </legend>
            {ranges.map((range) => (
              <button
                key={range}
                type="button"
                aria-pressed={range === days}
                onClick={() => selectRange(range)}
                className={`border px-3 py-2 text-sm ${
                  range === days
                    ? 'border-fl-accent bg-fl-bg text-fl-fg'
                    : 'border-fl-border text-fl-muted-2'
                }`}
              >
                {t('days', { days: range })}
              </button>
            ))}
          </fieldset>
          {status === 'loading' && <p role="status">{common('loading')}</p>}
          {status === 'error' && (
            <p role="alert" className="text-fl-error-fg">
              {common('errorMessage')}
            </p>
          )}
          {status === 'ready' && report && (
            <FeatureUsage features={report.features} />
          )}
        </div>
      </AdminPanel>

      {report && <Cohorts report={report} />}
    </div>
  )
}
