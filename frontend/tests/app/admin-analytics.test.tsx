import { beforeEach, describe, expect, it, vi } from 'vitest'
import { act, fireEvent, render, screen, within } from '@testing-library/react'
import AdminAnalyticsPage from '@/app/(app)/admin/analytics/page'
import { apiFetch } from '@/lib/api'
import en from '../../../messages/en.json'
import es from '../../../messages/es.json'

const i18n = vi.hoisted(() => ({ locale: 'en' as 'en' | 'es' }))

vi.mock('@/components/admin/AdminNav', () => ({ AdminNav: () => null }))
vi.mock('next-intl', () => ({
  useLocale: () => (i18n.locale === 'en' ? 'en-GB' : 'es'),
  useFormatter: () => ({
    dateTime: (value: Date, options: Intl.DateTimeFormatOptions) =>
      new Intl.DateTimeFormat(i18n.locale, options).format(value),
    number: (value: number, options?: Intl.NumberFormatOptions) =>
      new Intl.NumberFormat(i18n.locale, options).format(value),
  }),
  useTranslations:
    () => (key: string, values?: Record<string, string | number>) => {
      if (key === 'days') return `${values?.days} days`
      if (key === 'dayBand') return `Days: ${values?.range}`
      if (key === 'previous') return `Previous: ${values?.count}`
      const nav = i18n.locale === 'es' ? es.nav : en.nav
      if (key === 'nav.games') return nav.games
      if (key === 'nav.conversation') return nav.conversation
      return key
    },
}))
vi.mock('@/lib/api', () => ({ apiFetch: vi.fn() }))

const fetchReport = vi.mocked(apiFetch)
const report = {
  days: [{ date: '2026-11-24', learners: 5 }],
  weekly: { current: 5, previous: 0 },
  monthly: { current: 13, previous: 11 },
  repeat_weekly: { current: 4, previous: 2 },
  population: { last_7: 5, days_8_30: 8, over_30: 5, never: 2 },
  frequency: {
    one: 5,
    two_three: 0,
    four_seven: 2,
    eight_thirteen: 1,
    fourteen_plus: 4,
  },
  movement: [
    '2026-09-28',
    '2026-10-05',
    '2026-10-12',
    '2026-10-19',
    '2026-10-26',
    '2026-11-02',
    '2026-11-09',
    '2026-11-16',
  ].map((week, index) => ({
    week,
    new: index,
    continuing: 3,
    reactivated: 1,
    not_returned: index,
  })),
  features: [
    { feature: 'lessons', learners: 8, repeat_learners: 3, volume: 15 },
  ],
  activation: [
    { week: '2026-11-02', registered: 4, planned: 2, practised: 1 },
    { week: '2026-11-09', registered: 0, planned: 0, practised: 0 },
  ],
  retention: [
    { week: '2026-10-26', started: 4, returned: 0 },
    { week: '2026-11-02', started: 0, returned: 0 },
    { week: '2026-11-09', started: 1, returned: null },
    { week: '2026-11-16', started: 0, returned: null },
  ],
}

function valuesForRole(container: HTMLElement, role: string) {
  return within(container)
    .getAllByRole(role)
    .map((element) => element.textContent)
}

describe('AdminAnalyticsPage', () => {
  beforeEach(() => {
    fetchReport.mockReset()
    i18n.locale = 'en'
  })

  it.each([
    ['en', [en.nav.games, en.nav.conversation]],
    ['es', [es.nav.conversation, es.nav.games]],
  ] as const)(
    'sorts feature labels in the %s interface',
    async (locale, expected) => {
      i18n.locale = locale
      fetchReport.mockResolvedValueOnce(
        Response.json({
          ...report,
          features: [
            { feature: 'voice', learners: 9, repeat_learners: 2, volume: 12 },
            { feature: 'games', learners: 1, repeat_learners: 0, volume: 4 },
          ],
        })
      )
      render(<AdminAnalyticsPage />)
      const table = await screen.findByRole('table', { name: 'features' })
      expect(
        within(table)
          .getAllByRole('rowheader')
          .map((row) => row.textContent)
      ).toEqual(expected)
      const games = within(table).getByRole('row', {
        name: new RegExp(locale === 'en' ? en.nav.games : es.nav.games),
      })
      const zeroPercent = new Intl.NumberFormat(locale, {
        style: 'percent',
      }).format(0)
      expect(within(games).getAllByRole('cell')[1].textContent).toBe(
        `0 (${zeroPercent})`
      )
    }
  )

  it('shows period comparisons and distinguishes zero, empty and immature cohorts', async () => {
    fetchReport.mockResolvedValueOnce(Response.json(report))

    render(<AdminAnalyticsPage />)

    const activation = await screen.findByRole('table', { name: 'activation' })
    expect(
      screen.getByRole('button', { name: '30 days', pressed: true })
    ).toBeDefined()
    expect(screen.getByText('Previous: 0')).toBeDefined()
    expect(within(activation).getByText('2 (50%)')).toBeDefined()
    expect(within(activation).getByText('1 (25%)')).toBeDefined()
    expect(within(activation).getAllByText('noLearners')).toHaveLength(2)
    const retention = screen.getByRole('table', { name: 'retention' })
    expect(within(retention).getByText('0 (0%)')).toBeDefined()
    const retentionRows = within(retention).getAllByRole('row').slice(1)
    expect(
      retentionRows.map((row) => row.lastElementChild?.textContent)
    ).toEqual(['0 (0%)', 'noLearners', 'pending', 'noLearners'])
    const features = screen.getByRole('table', { name: 'features' })
    expect(
      within(features).getByRole('columnheader', { name: 'repeatLearners' })
    ).toBeDefined()
    expect(within(features).getByText('3 (37.5%)')).toBeDefined()
    expect(screen.queryByRole('alert')).toBeNull()
    expect(screen.queryByText('empty')).toBeNull()
  })

  it('shows all population and frequency bands and keeps non-returners outside weekly totals', async () => {
    fetchReport.mockResolvedValueOnce(Response.json(report))
    render(<AdminAnalyticsPage />)

    const population = await screen.findByLabelText('population')
    expect(valuesForRole(population, 'term')).toEqual([
      'last7',
      'days8to30',
      'over30',
      'neverPractised',
    ])
    expect(valuesForRole(population, 'definition')).toEqual([
      '5 (25%)',
      '8 (40%)',
      '5 (25%)',
      '2 (10%)',
    ])
    const frequency = screen.getByLabelText('frequency')
    expect(valuesForRole(frequency, 'term')).toEqual(
      ['1', '2–3', '4–7', '8–13', '14–28'].map((band) => `Days: ${band}`)
    )
    expect(valuesForRole(frequency, 'definition')).toEqual([
      '5',
      '0',
      '2',
      '1',
      '4',
    ])
    const movement = screen.getByRole('table', { name: 'movement' })
    expect(valuesForRole(movement, 'columnheader')).toEqual([
      'week',
      'learners',
      'newLearners',
      'continuing',
      'reactivated',
      'notReturned',
    ])
    const weeks = within(movement).getAllByRole('row').slice(1)
    expect(weeks).toHaveLength(8)
    expect(valuesForRole(weeks[7], 'cell')).toEqual(['11', '7', '3', '1', '7'])
  })

  it('reports an initial error without substituting empty data or zero counts', async () => {
    fetchReport.mockResolvedValueOnce(Response.json({}, { status: 503 }))
    render(<AdminAnalyticsPage />)

    expect((await screen.findByRole('alert')).textContent).toBe('errorMessage')
    expect(screen.queryByRole('status')).toBeNull()
    expect(screen.queryByText('noLearners')).toBeNull()
    expect(screen.queryByText('empty')).toBeNull()
    expect(screen.queryByLabelText('population')).toBeNull()
    expect(screen.queryByLabelText('frequency')).toBeNull()
    expect(screen.queryByRole('table', { name: 'movement' })).toBeNull()
  })

  it('distinguishes initial loading, an empty series and observed zero counts', async () => {
    const result = Promise.withResolvers<Response>()
    fetchReport.mockReturnValueOnce(result.promise)
    render(<AdminAnalyticsPage />)
    expect(screen.getByRole('status').textContent).toBe('loading')
    expect(screen.queryByText('empty')).toBeNull()
    expect(screen.queryByText('noLearners')).toBeNull()
    await act(async () =>
      result.resolve(
        Response.json({
          ...report,
          population: { last_7: 0, days_8_30: 0, over_30: 0, never: 0 },
          frequency: {
            one: 0,
            two_three: 0,
            four_seven: 0,
            eight_thirteen: 0,
            fourteen_plus: 0,
          },
          movement: [],
          activation: [],
          retention: [],
        })
      )
    )
    expect(screen.queryByRole('status')).toBeNull()
    expect(screen.getAllByText('empty')).toHaveLength(3)
    expect(screen.getByText('noLearners')).toBeDefined()
    expect(
      within(screen.getByLabelText('population')).getAllByText('0')
    ).toHaveLength(4)
    expect(
      within(screen.getByLabelText('frequency')).getAllByText('0')
    ).toHaveLength(5)
    expect(screen.queryByRole('alert')).toBeNull()
  })

  it('changes only feature usage and ignores late responses from superseded ranges', async () => {
    const late = Promise.withResolvers<Response>()
    fetchReport.mockImplementation(async (url) => {
      if (url.endsWith('=30')) return Response.json(report)
      if (url.endsWith('=7')) return late.promise
      return Response.json({
        ...report,
        days: [{ date: '2026-11-25', learners: 6 }],
        features: [
          { feature: 'reading', learners: 0, repeat_learners: 0, volume: 0 },
        ],
      })
    })

    render(<AdminAnalyticsPage />)
    await screen.findByText('progress.lessons')
    function fixedBreakdown() {
      return [
        screen.getByLabelText('population'),
        screen.getByRole('table', { name: 'movement' }),
        screen.getByLabelText('frequency'),
      ].map((element) => element.textContent)
    }
    const initialBreakdown = fixedBreakdown()
    fireEvent.click(screen.getByRole('button', { name: '7 days' }))
    expect(screen.queryByRole('table', { name: 'features' })).toBeNull()
    expect(screen.getByRole('table', { name: 'activation' })).toBeDefined()
    expect(fixedBreakdown()).toEqual(initialBreakdown)
    fireEvent.click(screen.getByRole('button', { name: '90 days' }))

    const features = await screen.findByRole('table', { name: 'features' })
    expect(within(features).getByText('nav.reading')).toBeDefined()
    expect(within(features).getAllByText('0')).toHaveLength(2)
    expect(within(features).getByText('noLearners')).toBeDefined()
    expect(fixedBreakdown()).toEqual(initialBreakdown)
    expect(screen.getByTitle('25 Nov 2026: 6')).toBeDefined()
    await act(async () => late.resolve(Response.json(report)))
    expect(screen.queryByText('progress.lessons')).toBeNull()
    expect(fetchReport.mock.calls.map(([url]) => url).sort()).toEqual([
      '/api/admin/analytics?days=30',
      '/api/admin/analytics?days=7',
      '/api/admin/analytics?days=90',
    ])
  })

  it('does not display the previous feature counts when a different range fails', async () => {
    fetchReport.mockImplementation(async (url) => {
      if (url.endsWith('=30')) return Response.json(report)
      return Response.json({}, { status: 503 })
    })

    render(<AdminAnalyticsPage />)
    await screen.findByText('progress.lessons')
    fireEvent.click(screen.getByRole('button', { name: '7 days' }))

    expect((await screen.findByRole('alert')).textContent).toBe('errorMessage')
    expect(screen.queryByRole('table', { name: 'features' })).toBeNull()
    expect(screen.getByRole('table', { name: 'retention' })).toBeDefined()
    expect(screen.getByLabelText('population')).toBeDefined()
    expect(screen.getByLabelText('frequency')).toBeDefined()
    expect(screen.getByRole('table', { name: 'movement' })).toBeDefined()
  })
})
