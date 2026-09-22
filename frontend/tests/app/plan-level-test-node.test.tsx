import { beforeEach, describe, expect, it, vi } from 'vitest'
import { fireEvent, render, screen } from '@testing-library/react'
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

vi.mock('@/store/language', () => ({
  useLanguageStore: (
    selector: (state: {
      activeLanguage: { code: string; name: string }
    }) => unknown
  ) => selector({ activeLanguage: { code: 'en-US', name: 'English' } }),
}))

import PlanPage from '@/app/(app)/plan/page'

function jsonResponse(data: unknown, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  })
}

const planPayload = {
  id: 7,
  cefr_level: 'A1',
  duration_weeks: 1,
  days_per_week: 2,
  current_unit: 'a1_unit_1',
  completion_test_taken: false,
  completion_test_score: null,
  completion_test_recommendation: null,
  generated_plan: {
    weekly_plan: [
      {
        week: 1,
        days: [
          {
            day: 1,
            title: 'Day 1 Lesson',
            lesson_type: 'grammar',
            unit_id: 'a1_unit_1',
          },
          {
            day: 2,
            title: 'Level A1 Completion Test',
            lesson_type: 'review',
            unit_id: 'completion-test',
          },
        ],
      },
    ],
  },
}

function mockPlan(
  completionState: 'in_progress' | 'ready' | 'taken' | 'unavailable',
  planOverrides: Record<string, unknown> = {}
) {
  const currentPlan = { ...planPayload, ...planOverrides }
  mockApiFetch.mockImplementation((url: string) => {
    if (url === '/api/study-plan/current') {
      return Promise.resolve(jsonResponse(currentPlan))
    }
    if (url === '/api/progress/competencies') {
      return Promise.resolve(jsonResponse([]))
    }
    if (url === '/api/study-plan/today') {
      if (completionState === 'unavailable') {
        return Promise.resolve(jsonResponse({}, 500))
      }
      return Promise.resolve(
        jsonResponse({
          lessons: [],
          completion: {
            state: completionState,
            score: null,
            recommendation: null,
            next_level: null,
          },
        })
      )
    }
    if (
      url === '/api/study-plan/pending-lessons' ||
      url === '/api/study-plan/lessons'
    ) {
      return Promise.resolve(jsonResponse([]))
    }
    if (url.startsWith('/api/curriculum/')) {
      return Promise.resolve(
        jsonResponse([
          {
            id: 'a1_unit_1',
            level: 'A1',
            unit_number: 1,
            title: 'Unit One',
            default_weeks: 2,
            grammar_points: ['g1'],
            vocabulary_set_ids: ['v1'],
            lesson_types: ['grammar'],
            competency_checklist: ['c1'],
          },
        ])
      )
    }
    return Promise.resolve(jsonResponse({}, 404))
  })
}

describe('My Plan level test node', () => {
  beforeEach(() => {
    mockApiFetch.mockReset()
    mockPush.mockReset()
  })

  it('opens the real level test when the final position is reached', async () => {
    mockPlan('ready')

    render(<PlanPage />)

    expect(await screen.findByText('levelComplete')).toBeInTheDocument()
    const title = await screen.findByText('completionTestTitle')
    const cardButton = title.closest('button')
    expect(cardButton).not.toBeNull()
    fireEvent.click(cardButton as HTMLButtonElement)
    expect(mockPush).toHaveBeenCalledWith('/assessment/level-test?plan=7')
  })

  it('keeps the level test locked while the plan is in progress', async () => {
    mockPlan('in_progress')

    render(<PlanPage />)

    expect(await screen.findByText('completionTestTitle')).toBeInTheDocument()
    expect(screen.queryByText('levelComplete')).not.toBeInTheDocument()
    const title = screen.getByText('completionTestTitle')
    const cardButton = title.closest('button')
    expect(cardButton).toBeDisabled()
    fireEvent.click(cardButton as HTMLButtonElement)
    expect(mockPush).not.toHaveBeenCalled()
  })

  it('shows the persisted result once the level test is taken', async () => {
    mockPlan('taken', {
      completion_test_taken: true,
      completion_test_score: 0.82,
      completion_test_recommendation: 'advance',
    })

    render(<PlanPage />)

    expect(await screen.findByText('levelTestResult')).toBeInTheDocument()
    expect(screen.queryByText('levelComplete')).not.toBeInTheDocument()
    const title = await screen.findByText('completionTestTitle')
    const cardButton = title.closest('button')
    expect(cardButton).not.toBeDisabled()
    fireEvent.click(cardButton as HTMLButtonElement)
    expect(mockPush).not.toHaveBeenCalled()
  })

  it('keeps the level test locked when the completion state cannot be loaded', async () => {
    mockPlan('unavailable')

    render(<PlanPage />)

    const title = await screen.findByText('completionTestTitle')
    const cardButton = title.closest('button')
    expect(cardButton).toBeDisabled()
    fireEvent.click(cardButton as HTMLButtonElement)
    expect(mockPush).not.toHaveBeenCalled()
  })
})
