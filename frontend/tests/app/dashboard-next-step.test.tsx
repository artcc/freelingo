import { beforeEach, describe, expect, it, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import React from 'react'

const { mockApiFetch, mockPush } = vi.hoisted(() => ({
  mockApiFetch: vi.fn(),
  mockPush: vi.fn(),
}))

vi.mock('next-intl', () => ({
  useTranslations: () => (key: string) => key,
}))

vi.mock('next/navigation', () => ({
  useRouter: () => ({ push: mockPush }),
}))

vi.mock('next/link', () => ({
  default: ({
    href,
    children,
    ...props
  }: React.AnchorHTMLAttributes<HTMLAnchorElement>) =>
    React.createElement('a', { href: String(href), ...props }, children),
}))

vi.mock('@/lib/api', () => ({
  apiFetch: mockApiFetch,
}))

vi.mock('@/components/tour/OnboardingTour', () => ({ default: () => null }))
vi.mock('@/components/whats-new/WhatsNew', () => ({ default: () => null }))
vi.mock('@/components/dashboard/DashboardAnnouncement', () => ({
  DashboardAnnouncement: () => null,
}))
vi.mock('@/components/billing/SubscriptionPlanButtons', () => ({
  default: () => null,
}))

import DashboardPage from '@/app/(app)/dashboard/page'

function jsonResponse(data: unknown, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  })
}

function todayPayload(overrides: Record<string, unknown>) {
  return {
    plan_id: 7,
    cefr_level: 'A1',
    lessons: [],
    progress_day: 0,
    total_days: 16,
    pending_count: 0,
    completion: {
      state: 'in_progress',
      score: null,
      recommendation: null,
      next_level: null,
    },
    ...overrides,
  }
}

function mockToday(payload: Record<string, unknown>) {
  mockApiFetch.mockImplementation((url: string) => {
    if (url === '/api/progress/summary') {
      return Promise.resolve(jsonResponse({}))
    }
    if (url === '/api/study-plan/today') {
      return Promise.resolve(jsonResponse(payload))
    }
    return Promise.resolve(jsonResponse({}, 404))
  })
}

describe('dashboard end-of-plan next step', () => {
  beforeEach(() => {
    mockApiFetch.mockReset()
    mockPush.mockReset()
  })

  it('offers the real level test when the plan reached its final position', async () => {
    mockToday(
      todayPayload({
        progress_day: 15,
        completion: {
          state: 'ready',
          score: null,
          recommendation: null,
          next_level: null,
        },
      })
    )

    render(<DashboardPage />)

    expect(
      (await screen.findAllByText('levelTestReady')).length
    ).toBeGreaterThan(0)
    expect(screen.queryByText('allCaughtUp')).not.toBeInTheDocument()
    const link = screen.getByRole('link', { name: 'beginLevelTest' })
    expect(link).toHaveAttribute('href', '/assessment/level-test?plan=7')
  })

  it('shows the persisted result and the retake-assessment action after an advance', async () => {
    mockToday(
      todayPayload({
        progress_day: 15,
        completion: {
          state: 'taken',
          score: 0.82,
          recommendation: 'advance',
          next_level: 'A2',
        },
      })
    )

    render(<DashboardPage />)

    expect(
      (await screen.findAllByText('levelTestCompleted')).length
    ).toBeGreaterThan(0)
    expect(screen.getByText('levelTestScoreLine')).toBeInTheDocument()
    const link = screen.getByRole('link', { name: 'retake' })
    expect(link).toHaveAttribute('href', '/assessment')
  })

  it('routes to My Plan when the CEFR scale is exhausted', async () => {
    mockToday(
      todayPayload({
        progress_day: 15,
        completion: {
          state: 'taken',
          score: 0.9,
          recommendation: 'advance',
          next_level: null,
        },
      })
    )

    render(<DashboardPage />)

    expect(
      (await screen.findAllByText('levelTestCompleted')).length
    ).toBeGreaterThan(0)
    const links = await screen.findAllByRole('link', { name: 'goToMyPlan' })
    expect(links.some((link) => link.getAttribute('href') === '/plan')).toBe(
      true
    )
    expect(
      screen.queryByRole('link', { name: 'retake' })
    ).not.toBeInTheDocument()
  })

  it('routes back to My Plan when the result recommends reinforcement', async () => {
    mockToday(
      todayPayload({
        progress_day: 15,
        completion: {
          state: 'taken',
          score: 0.4,
          recommendation: 'repeat',
          next_level: null,
        },
      })
    )

    render(<DashboardPage />)

    const links = await screen.findAllByRole('link', { name: 'goToMyPlan' })
    expect(links.some((link) => link.getAttribute('href') === '/plan')).toBe(
      true
    )
  })

  it('keeps the normal lesson next step while the plan is in progress', async () => {
    mockToday(
      todayPayload({
        lessons: [
          {
            id: 5,
            title: 'Lesson A',
            lesson_type: 'grammar',
            week: 1,
            day: 1,
            objectives: [],
            estimated_minutes: 25,
            is_completed: false,
          },
        ],
      })
    )

    render(<DashboardPage />)

    expect((await screen.findAllByText('Lesson A')).length).toBeGreaterThan(0)
    expect(screen.queryByText('levelTestReady')).not.toBeInTheDocument()
    const lessonLinks = screen
      .getAllByRole('link')
      .filter((link) => link.getAttribute('href') === '/lesson/5')
    expect(lessonLinks.length).toBeGreaterThan(0)
  })
})
