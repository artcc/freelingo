import { useFormatter, useTranslations } from 'next-intl'
import { AdminPanel } from '@/components/admin/AdminShell'
import { AnalyticsTable } from '@/components/admin/AnalyticsTable'
import { LearnerShare } from './LearnerShare'

const populationBands = [
  ['last_7', 'last7', 'bg-fl-accent'],
  ['days_8_30', 'days8to30', 'bg-fl-fg-2'],
  ['over_30', 'over30', 'bg-fl-muted-2'],
  ['never', 'neverPractised', 'bg-fl-border-2'],
] as const

const frequencyBands = [
  ['one', '1'],
  ['two_three', '2–3'],
  ['four_seven', '4–7'],
  ['eight_thirteen', '8–13'],
  ['fourteen_plus', '14–28'],
] as const

const movementGroups = [
  ['new', 'newLearners', 'bg-fl-accent'],
  ['continuing', 'continuing', 'bg-fl-fg-2'],
  ['reactivated', 'reactivated', 'bg-fl-muted-2'],
] as const

interface MovementWeek {
  week: string
  new: number
  continuing: number
  reactivated: number
  not_returned: number
}

export interface ActivityBreakdown {
  population: Record<(typeof populationBands)[number][0], number>
  frequency: Record<(typeof frequencyBands)[number][0], number>
  movement: MovementWeek[]
}

function PopulationPanel({
  population,
}: {
  population: ActivityBreakdown['population']
}) {
  const t = useTranslations('adminAnalytics')
  const total = populationBands.reduce((sum, [key]) => sum + population[key], 0)
  return (
    <AdminPanel title={t('population')}>
      <div className="space-y-3 p-5">
        <p className="text-fl-muted-2 text-sm">{t('populationDesc')}</p>
        <div aria-hidden="true" className="bg-fl-bg flex h-4">
          {total > 0 &&
            populationBands.map(([key, , color]) => (
              <span
                key={key}
                className={color}
                style={{ width: `${(population[key] / total) * 100}%` }}
              />
            ))}
        </div>
        {total === 0 && <p>{t('noLearners')}</p>}
        <dl aria-label={t('population')} className="space-y-2 text-sm">
          {populationBands.map(([key, label, color]) => (
            <div
              key={key}
              className="flex items-baseline justify-between gap-3"
            >
              <dt>
                <span
                  aria-hidden="true"
                  className={`me-2 inline-block size-2 ${color}`}
                />
                {t(label)}
              </dt>
              <dd className="tabular-nums">
                {total === 0 ? (
                  0
                ) : (
                  <LearnerShare count={population[key]} total={total} />
                )}
              </dd>
            </div>
          ))}
        </dl>
      </div>
    </AdminPanel>
  )
}

function FrequencyPanel({
  frequency,
}: {
  frequency: ActivityBreakdown['frequency']
}) {
  const t = useTranslations('adminAnalytics')
  const maximum = Math.max(1, ...frequencyBands.map(([key]) => frequency[key]))
  return (
    <AdminPanel title={t('frequency')}>
      <div className="space-y-3 p-5">
        <p className="text-fl-muted-2 text-sm">{t('frequencyDesc')}</p>
        <dl
          aria-label={t('frequency')}
          className="grid grid-cols-[auto_1fr] items-center gap-x-3 gap-y-2 text-sm"
        >
          {frequencyBands.map(([key, range]) => (
            <div key={key} className="col-span-2 grid grid-cols-subgrid">
              <dt>{t('dayBand', { range })}</dt>
              <dd className="flex items-center gap-2">
                <span aria-hidden="true" className="bg-fl-bg flex h-2 flex-1">
                  <span
                    className="bg-fl-accent"
                    style={{ width: `${(frequency[key] / maximum) * 100}%` }}
                  />
                </span>
                <span
                  className="text-end tabular-nums"
                  style={{ width: `${String(maximum).length}ch` }}
                >
                  {frequency[key]}
                </span>
              </dd>
            </div>
          ))}
        </dl>
      </div>
    </AdminPanel>
  )
}

function activeLearners(week: MovementWeek) {
  return week.new + week.continuing + week.reactivated
}

function MovementPanel({ movement }: { movement: MovementWeek[] }) {
  const t = useTranslations('adminAnalytics')
  const format = useFormatter()
  const maximum = Math.max(1, ...movement.map(activeLearners))
  return (
    <AdminPanel title={t('movement')}>
      <div className="space-y-3 p-5">
        <p className="text-fl-muted-2 text-sm">{t('movementDesc')}</p>
        <AnalyticsTable
          title={t('movement')}
          headers={[
            t('week'),
            t('learners'),
            ...movementGroups.map(([, label]) => t(label)),
            t('notReturned'),
          ]}
          rows={movement.map((week) => ({
            key: week.week,
            cells: [
              format.dateTime(new Date(week.week), {
                dateStyle: 'medium',
                timeZone: 'UTC',
              }),
              <div key="active" className="flex items-center gap-2">
                <span style={{ width: `${String(maximum).length}ch` }}>
                  {activeLearners(week)}
                </span>
                <span
                  aria-hidden="true"
                  className="bg-fl-bg flex h-2 min-w-16 flex-1"
                >
                  {movementGroups.map(([key, , color]) => (
                    <span
                      key={key}
                      className={color}
                      style={{ width: `${(week[key] / maximum) * 100}%` }}
                    />
                  ))}
                </span>
              </div>,
              ...movementGroups.map(([key, , color]) => (
                <span key={key} className="whitespace-nowrap">
                  <span
                    aria-hidden="true"
                    className={`me-2 inline-block size-2 ${color}`}
                  />
                  {week[key]}
                </span>
              )),
              week.not_returned,
            ],
          }))}
        />
      </div>
    </AdminPanel>
  )
}

export function ActivityBreakdownPanels({
  population,
  frequency,
  movement,
}: ActivityBreakdown) {
  return (
    <>
      <div className="grid items-start gap-4 xl:grid-cols-2">
        <PopulationPanel population={population} />
        <FrequencyPanel frequency={frequency} />
      </div>
      <MovementPanel movement={movement} />
    </>
  )
}
