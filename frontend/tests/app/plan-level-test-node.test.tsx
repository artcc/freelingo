import { beforeEach, describe, expect, it, vi } from 'vitest'
import { act, fireEvent, render, screen, waitFor } from '@testing-library/react'
import React from 'react'
import { useLanguageStore } from '@/store/language'
import { getLanguageByCode } from '@/lib/target-languages'
import { useLoadingStore } from '@/store/loading'

const { mockApiFetch, mockPush } = vi.hoisted(() => ({
  mockApiFetch: vi.fn(),
  mockPush: vi.fn(),
}))

vi.mock('next-intl', () => ({
  useTranslations: () => (key: string) => key,
}))

vi.mock('next/navigation', () => {
  const router = { push: mockPush }
  return { useRouter: () => router }
})

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
    useLanguageStore.setState({
      activeLanguage: getLanguageByCode('en-US') ?? null,
      userLanguages: [],
      needsRefresh: false,
      isSwitching: false,
    })
    useLoadingStore.setState({ count: 0 })
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

  it.each([429, 503])(
    'offers a curriculum-only retry after HTTP %s',
    async (status) => {
      mockPlan('in_progress')
      const normal = mockApiFetch.getMockImplementation()!
      let recover = false
      mockApiFetch.mockImplementation((url: string) =>
        url.startsWith('/api/curriculum/') && !recover
          ? Promise.resolve(jsonResponse({}, status))
          : normal(url)
      )
      render(<PlanPage />)
      expect(await screen.findByRole('alert')).toHaveTextContent('errorMessage')
      expect(screen.queryByText('noUnitsForLevel')).not.toBeInTheDocument()
      expect(screen.getByText('unitsLabel').parentElement).toHaveTextContent(
        '—'
      )
      const planRequests = mockApiFetch.mock.calls.filter(
        ([url]) => url === '/api/study-plan/current'
      ).length
      recover = true
      fireEvent.click(screen.getByRole('button', { name: 'retry' }))
      expect(await screen.findByText('Unit One')).toBeInTheDocument()
      expect(screen.queryByRole('alert')).not.toBeInTheDocument()
      expect(
        mockApiFetch.mock.calls.filter(
          ([url]) => url === '/api/study-plan/current'
        )
      ).toHaveLength(planRequests)
    }
  )

  it('shows no units only after a successful empty curriculum response', async () => {
    mockPlan('in_progress')
    const normal = mockApiFetch.getMockImplementation()!
    let finish!: (response: Response) => void
    const pending = new Promise<Response>((resolve) => {
      finish = resolve
    })
    mockApiFetch.mockImplementation((url: string) =>
      url.startsWith('/api/curriculum/') ? pending : normal(url)
    )
    render(<PlanPage />)
    await screen.findByText('unitsLabel')
    expect(screen.queryByText('noUnitsForLevel')).not.toBeInTheDocument()
    expect(screen.getByText('unitsLabel').parentElement).toHaveTextContent('—')
    await act(async () => finish(jsonResponse([])))
    expect(screen.getByText('noUnitsForLevel')).toBeInTheDocument()
    expect(screen.queryByRole('alert')).not.toBeInTheDocument()
  })

  it('ignores the old curriculum response after a language change', async () => {
    mockPlan('in_progress')
    const normal = mockApiFetch.getMockImplementation()!
    let finishOld!: (response: Response) => void
    const pending = new Promise<Response>((resolve) => {
      finishOld = resolve
    })
    mockApiFetch.mockImplementation((url: string) =>
      url === '/api/curriculum/A1?language=en-US' ? pending : normal(url)
    )
    render(<PlanPage />)
    await waitFor(() =>
      expect(mockApiFetch).toHaveBeenCalledWith(
        '/api/curriculum/A1?language=en-US'
      )
    )
    act(() =>
      useLanguageStore.setState({
        activeLanguage: getLanguageByCode('de-DE') ?? null,
      })
    )
    expect(await screen.findByText('Unit One')).toBeInTheDocument()
    await act(async () => finishOld(jsonResponse({}, 503)))
    expect(screen.queryByRole('alert')).not.toBeInTheDocument()
    expect(screen.getByText('Unit One')).toBeInTheDocument()
  })

  it('recovers missing language context before loading the plan and releases loading after failure', async () => {
    useLanguageStore.setState({ activeLanguage: null })
    mockPlan('in_progress')
    const normal = mockApiFetch.getMockImplementation()!
    let recover = false
    mockApiFetch.mockImplementation((url: string) =>
      url === '/api/languages'
        ? Promise.resolve(
            recover
              ? jsonResponse({
                  languages: [{ target_language: 'de-DE', is_active: true }],
                })
              : jsonResponse({}, 503)
          )
        : normal(url)
    )
    render(<PlanPage />)
    expect(await screen.findByRole('alert')).toHaveTextContent('errorMessage')
    expect(useLoadingStore.getState().count).toBe(0)
    expect(
      mockApiFetch.mock.calls.every(([url]) => url === '/api/languages')
    ).toBe(true)
    recover = true
    fireEvent.click(screen.getByRole('button', { name: 'retry' }))
    expect(await screen.findByText('Unit One')).toBeInTheDocument()
    expect(mockApiFetch).toHaveBeenCalledWith(
      '/api/curriculum/A1?language=de-DE'
    )
    expect(screen.queryByRole('alert')).not.toBeInTheDocument()
    expect(useLoadingStore.getState().count).toBe(0)
  })

  it.each([200, 503])(
    'ignores a previous full plan load (HTTP %s) after switching',
    async (status) => {
      mockPlan('ready', { cefr_level: 'B1' })
      const old = mockApiFetch.getMockImplementation()!
      let finish!: (response: Response) => void
      const pending = new Promise<Response>((resolve) => {
        finish = resolve
      })
      mockApiFetch.mockImplementation((url: string) =>
        url === '/api/study-plan/current' ? pending : old(url)
      )
      render(<PlanPage />)
      const signal = mockApiFetch.mock.calls.find(
        ([url]) => url === '/api/study-plan/current'
      )![1].signal as AbortSignal
      act(() => useLanguageStore.setState({ isSwitching: true }))
      expect(signal.aborted).toBe(true)
      mockPlan('in_progress', { id: 28, cefr_level: 'B2' })
      act(() =>
        useLanguageStore.setState({
          activeLanguage: getLanguageByCode('de-DE') ?? null,
          isSwitching: false,
        })
      )
      expect(await screen.findByText('B2')).toBeInTheDocument()
      await screen.findByText('Unit One')
      await act(async () =>
        finish(jsonResponse({ ...planPayload, cefr_level: 'B1' }, status))
      )
      expect(screen.getByText('B2')).toBeInTheDocument()
      expect(screen.queryByText('B1')).not.toBeInTheDocument()
      expect(screen.queryByText('levelComplete')).not.toBeInTheDocument()
      expect(screen.queryByRole('alert')).not.toBeInTheDocument()
      expect(mockPush).not.toHaveBeenCalled()
    }
  )

  it('does not load a plan while a cached language needs reconciliation', async () => {
    useLanguageStore.setState({ needsRefresh: true })
    mockApiFetch.mockResolvedValue(jsonResponse({}, 503))
    render(<PlanPage />)
    await screen.findByRole('alert')
    expect(mockApiFetch.mock.calls.map(([url]) => url)).toEqual([
      '/api/languages',
    ])
  })
})
