import { describe, expect, it, vi, beforeEach } from 'vitest'
import {
  fireEvent,
  render,
  screen,
  waitFor,
  within,
} from '@testing-library/react'
import React from 'react'

const translate = vi.hoisted(() => (key: string) => key)

vi.mock('next-intl', () => ({
  useLocale: () => 'en-GB',
  useTranslations: () => translate,
}))

vi.mock('next/link', () => ({
  default: ({
    href,
    children,
    prefetch,
    ...props
  }: React.AnchorHTMLAttributes<HTMLAnchorElement> & { prefetch?: boolean }) =>
    React.createElement(
      'a',
      { href, 'data-prefetch': prefetch, ...props },
      children
    ),
}))

vi.mock('next/navigation', () => ({
  usePathname: () => '/admin',
}))

const { mockApiFetch } = vi.hoisted(() => ({
  mockApiFetch: vi.fn(),
}))

vi.mock('@/lib/api', () => ({
  apiFetch: mockApiFetch,
}))

import AdminOverviewPage from '@/app/(app)/admin/page'
import { useConfigStore } from '@/store/config'

function jsonResponse(data: unknown, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  })
}

function serveOverview(stats: Response, activity = jsonResponse({ days: [] })) {
  mockApiFetch.mockImplementation(async (url: string) => {
    if (url === '/api/admin/stats') return stats
    if (url === '/api/admin/analytics/activity') return activity
    throw new Error(`Unexpected request: ${url}`)
  })
}

describe('AdminOverviewPage', () => {
  beforeEach(() => {
    mockApiFetch.mockReset()
    useConfigStore.setState({ maintenanceMode: false, stripeEnabled: true })
  })

  it('loads and renders admin overview stats', async () => {
    serveOverview(
      jsonResponse({
        users_total: 12,
        users_active: 10,
        users_inactive: 2,
        subscriptions_active: 4,
        subscriptions_trialing: 3,
        subscriptions_past_due: 1,
        feedback_total: 9,
        feedback_pending: 5,
        feedback_bug_pending: 2,
      }),
      jsonResponse({ days: [{ date: '2026-11-01', learners: 0 }] })
    )

    render(<AdminOverviewPage />)

    await waitFor(() => expect(screen.getByText('12')).toBeDefined())
    expect(mockApiFetch).toHaveBeenCalledWith('/api/admin/stats')
    expect(screen.getByText('10')).toBeDefined()
    expect(screen.getByText('4 / 3')).toBeDefined()
    expect(screen.getByText('5')).toBeDefined()
    expect(screen.getByText('pendingBugs')).toBeDefined()
    expect(screen.getByText('pastDueSubscriptions')).toBeDefined()
    fireEvent.click(await screen.findByText('dailyValues'))
    const table = screen.getByRole('table', { name: 'daily' })
    expect(within(table).getByText('0')).toBeDefined()
    expect(within(table).getByRole('rowheader').textContent).toBe('1 Nov 2026')
    expect(mockApiFetch.mock.calls.map(([url]) => url).sort()).toEqual([
      '/api/admin/analytics/activity',
      '/api/admin/stats',
    ])
    const links = screen
      .getAllByRole('link')
      .filter((link) => link.getAttribute('href') === '/admin/analytics')
    expect(links).toHaveLength(2)
    for (const link of links) {
      expect(link.getAttribute('data-prefetch')).toBe('false')
    }
  })

  it('shows a translated error when stats fail to load', async () => {
    serveOverview(jsonResponse({}, 500))

    render(<AdminOverviewPage />)

    await waitFor(() =>
      expect(screen.getByText('adminStatsError')).toBeDefined()
    )
    expect(screen.queryByText('0 / 0')).toBeNull()
    expect(await screen.findByText('empty')).toBeDefined()
  })

  it('hides subscription metrics and alerts when Stripe is disabled', async () => {
    useConfigStore.setState({ stripeEnabled: false })
    serveOverview(
      jsonResponse({
        users_total: 12,
        users_active: 10,
        subscriptions_active: 4,
        subscriptions_trialing: 3,
        subscriptions_past_due: 1,
        feedback_pending: 5,
        feedback_bug_pending: 2,
        reviews_pending: 1,
      })
    )

    render(<AdminOverviewPage />)

    await waitFor(() => expect(screen.getByText('12')).toBeDefined())
    expect(screen.queryByText('paidAccess')).toBeNull()
    expect(screen.queryByText('4 / 3')).toBeNull()
    expect(screen.queryByText('pastDueSubscriptions')).toBeNull()
  })
})
