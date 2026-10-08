import React from 'react'
import {
  act,
  fireEvent,
  render,
  screen,
  waitFor,
  within,
} from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { NextIntlClientProvider } from 'next-intl'
import messages from '../../../messages/en.json'
import { useLanguageStore } from '@/store/language'
import { getLanguageByCode } from '@/lib/target-languages'
import ProgressPage from '@/app/(app)/progress/page'
import { ActivityHistory } from '@/components/progress/ActivityHistory'

const { mockApiFetch } = vi.hoisted(() => ({ mockApiFetch: vi.fn() }))
vi.mock('@/lib/api', () => ({ apiFetch: mockApiFetch }))
vi.mock('@/components/ui/page-loading', () => ({
  PageLoading: ({ label }: { label: string }) => <p role="status">{label}</p>,
}))

function json(data: unknown, status = 200) {
  return new Response(JSON.stringify(data), { status })
}

function responseFor(url: string, xp = 125) {
  if (url === '/api/progress/summary')
    return json({
      total_xp: xp,
      today_xp: 0,
      current_streak: 1,
      total_lessons: 0,
      total_exercises: 0,
      exercises_correct: 0,
      accuracy: 0,
      skills: {},
      activity_week: Array.from({ length: 7 }, (_, i) => ({
        date: `2026-10-${String(i + 2).padStart(2, '0')}`,
        active: i === 6,
        xp: 0,
      })),
    })
  if (url === '/api/study-plan/current')
    return json({ id: 1, cefr_level: 'A1' })
  if (url === '/api/progress/history')
    return json({ entries: [{ date: '2026-10-08', xp_earned: 0 }] })
  if (url.startsWith('/api/vocabulary?')) return json({ sets: [] })
  return json([])
}

function renderWithMessages(children: React.ReactNode) {
  return render(
    <NextIntlClientProvider locale="en-GB" messages={messages} timeZone="UTC">
      {children}
    </NextIntlClientProvider>
  )
}

describe('progress page', () => {
  beforeEach(() => {
    mockApiFetch.mockReset()
    mockApiFetch.mockImplementation(async (url: string) => responseFor(url))
    useLanguageStore.setState({
      activeLanguage: getLanguageByCode('en-GB')!,
      needsRefresh: false,
      isSwitching: false,
      userLanguages: [],
    })
  })

  it('shows zero-XP activity and leaves accuracy unset before the first exercise', async () => {
    renderWithMessages(<ProgressPage />)
    expect(
      await screen.findByRole('heading', { name: 'Your progress' })
    ).toBeInTheDocument()
    expect(screen.getByText('Practised today')).toBeInTheDocument()
    expect(
      screen.getByText(messages.dashboardProgress.noExercises)
    ).toBeInTheDocument()
    expect(screen.queryByText('0%')).not.toBeInTheDocument()
    expect(
      screen.queryByRole('link', { name: 'View progress' })
    ).not.toBeInTheDocument()
    const history = screen.getByRole('list', { name: 'Your learning rhythm' })
    expect(within(history).getAllByRole('listitem')).toHaveLength(28)
    expect(
      within(history).getByRole('listitem', {
        name: '8 Oct 2026: Practised, 0 XP',
      })
    ).toBeInTheDocument()
    expect(screen.getByText('0 XP · Active days: 1/28')).toBeInTheDocument()
  })

  it('discards a late summary body after switching languages', async () => {
    let resolveOld!: (data: unknown) => void
    const oldBody = new Promise((resolve) => {
      resolveOld = resolve
    })
    const oldJson = vi.fn(() => oldBody)
    mockApiFetch.mockImplementation(async (url: string) =>
      url === '/api/progress/summary'
        ? { ok: true, json: oldJson }
        : responseFor(url)
    )
    renderWithMessages(<ProgressPage />)
    await waitFor(() => expect(oldJson).toHaveBeenCalled())

    mockApiFetch.mockImplementation(async (url: string) =>
      responseFor(url, 777)
    )
    act(() =>
      useLanguageStore.setState({ activeLanguage: getLanguageByCode('de-DE')! })
    )
    expect(await screen.findByText('777')).toBeInTheDocument()
    await act(async () =>
      resolveOld(await responseFor('/api/progress/summary', 999).json())
    )
    expect(screen.getByText('777')).toBeInTheDocument()
    expect(screen.queryByText('999')).not.toBeInTheDocument()
    expect(mockApiFetch).not.toHaveBeenCalledWith(
      '/api/curriculum/A1?language=en-GB'
    )
  })

  it('clears the previous plan when the new language has no plan', async () => {
    renderWithMessages(<ProgressPage />)
    expect(await screen.findByText('125')).toBeInTheDocument()
    mockApiFetch.mockImplementation(async (url: string) =>
      url === '/api/study-plan/current' ? json(null) : responseFor(url)
    )
    act(() =>
      useLanguageStore.setState({ activeLanguage: getLanguageByCode('de-DE')! })
    )
    expect(screen.queryByText('125')).not.toBeInTheDocument()
    await waitFor(() =>
      expect(screen.queryByRole('status')).not.toBeInTheDocument()
    )
    expect(
      screen.queryByRole('heading', { name: 'Your progress' })
    ).not.toBeInTheDocument()
    expect(screen.queryByRole('alert')).not.toBeInTheDocument()
    expect(
      screen.getByRole('button', { name: messages.plan.startAssessment })
    ).toBeInTheDocument()
  })

  it('discards curriculum that finishes loading after a language switch', async () => {
    let resolveOld!: (data: Response) => void
    const oldCurriculum = new Promise<Response>((resolve) => {
      resolveOld = resolve
    })
    mockApiFetch.mockImplementation(async (url: string) =>
      url === '/api/curriculum/A1?language=en-GB'
        ? oldCurriculum
        : responseFor(url)
    )
    renderWithMessages(<ProgressPage />)
    await waitFor(() =>
      expect(mockApiFetch).toHaveBeenCalledWith(
        '/api/curriculum/A1?language=en-GB'
      )
    )
    mockApiFetch.mockImplementation(async (url: string) =>
      responseFor(url, 777)
    )
    act(() =>
      useLanguageStore.setState({ activeLanguage: getLanguageByCode('de-DE')! })
    )
    expect(await screen.findByText('777')).toBeInTheDocument()
    await act(async () =>
      resolveOld(
        json([
          {
            id: 'old-unit',
            unit_number: 1,
            title: 'Old curriculum',
            competency_checklist: [],
          },
        ])
      )
    )
    expect(screen.getByText('777')).toBeInTheDocument()
    expect(screen.queryByText('Old curriculum')).not.toBeInTheDocument()
  })

  it('offers retry on history failure instead of presenting an empty calendar', async () => {
    mockApiFetch.mockImplementation(async (url: string) =>
      url === '/api/progress/history' ? json({}, 503) : responseFor(url)
    )
    renderWithMessages(<ProgressPage />)
    expect(await screen.findByRole('alert')).toHaveTextContent(
      messages.common.errorMessage
    )
    expect(
      screen.queryByText(messages.progressActivity.empty)
    ).not.toBeInTheDocument()
    mockApiFetch.mockImplementation(async (url: string) => responseFor(url))
    fireEvent.click(screen.getByRole('button', { name: 'Retry' }))
    expect(
      await screen.findByRole('heading', { name: 'Your learning rhythm' })
    ).toBeInTheDocument()
  })

  it('reconciles a persisted switch with a failed refresh before loading progress', async () => {
    mockApiFetch.mockImplementation(async (url: string) => {
      if (url === '/api/languages/active') return json({})
      if (url === '/api/languages') return json({}, 503)
      return responseFor(url)
    })
    expect(await useLanguageStore.getState().switchLanguage('de-DE')).toBe(
      false
    )
    expect(useLanguageStore.getState().activeLanguage?.code).toBe('en-GB')
    expect(useLanguageStore.getState().needsRefresh).toBe(true)

    renderWithMessages(<ProgressPage />)
    expect(await screen.findByRole('alert')).toBeInTheDocument()
    expect(mockApiFetch).not.toHaveBeenCalledWith('/api/progress/summary')
    expect(mockApiFetch).not.toHaveBeenCalledWith(
      '/api/vocabulary?language=en-GB'
    )

    mockApiFetch.mockImplementation(async (url: string) => {
      if (url === '/api/languages') {
        return json({
          languages: [{ target_language: 'de-DE', is_active: true }],
          all_supported_languages: ['en-GB', 'de-DE'],
        })
      }
      return responseFor(url, 777)
    })
    fireEvent.click(screen.getByRole('button', { name: 'Retry' }))
    expect(await screen.findByText('777')).toBeInTheDocument()
    expect(mockApiFetch).toHaveBeenCalledWith('/api/vocabulary?language=de-DE')
    expect(mockApiFetch).toHaveBeenCalledWith('/api/curriculum/A1?language=de-DE')
    expect(mockApiFetch).not.toHaveBeenCalledWith(
      '/api/curriculum/A1?language=en-GB'
    )
  })

  it('discards pending data on invalidation even when the cached language stays the same', async () => {
    let resolveOld!: (data: unknown) => void
    const oldBody = new Promise((resolve) => {
      resolveOld = resolve
    })
    const oldJson = vi.fn(() => oldBody)
    mockApiFetch.mockImplementation(async (url: string) => {
      if (url === '/api/progress/summary') return { ok: true, json: oldJson }
      if (url === '/api/languages') return json({}, 503)
      return responseFor(url)
    })
    renderWithMessages(<ProgressPage />)
    await waitFor(() => expect(oldJson).toHaveBeenCalled())
    act(() => useLanguageStore.getState().invalidateLanguages())
    expect(await screen.findByRole('alert')).toBeInTheDocument()
    await act(async () =>
      resolveOld(await responseFor('/api/progress/summary', 999).json())
    )
    expect(screen.queryByText('999')).not.toBeInTheDocument()
    expect(mockApiFetch).not.toHaveBeenCalledWith(
      '/api/curriculum/A1?language=en-GB'
    )
  })

  it('pauses loaded progress during a switch before activeLanguage changes', async () => {
    renderWithMessages(<ProgressPage />)
    expect(await screen.findByText('125')).toBeInTheDocument()
    mockApiFetch.mockClear()
    act(() => useLanguageStore.setState({ isSwitching: true }))
    expect(screen.queryByText('125')).not.toBeInTheDocument()
    expect(screen.getByRole('status')).toBeInTheDocument()
    expect(mockApiFetch).not.toHaveBeenCalled()
    act(() => useLanguageStore.setState({ isSwitching: false }))
    expect(await screen.findByText('125')).toBeInTheDocument()
  })

  it('resolves missing language context instead of requesting English by default', async () => {
    useLanguageStore.setState({ activeLanguage: null })
    mockApiFetch.mockImplementation(async (url: string) => {
      if (url === '/api/languages') {
        return json({ languages: [{ target_language: 'ja-JP', is_active: true }] })
      }
      return responseFor(url)
    })
    renderWithMessages(<ProgressPage />)
    expect(await screen.findByText('125')).toBeInTheDocument()
    expect(mockApiFetch).toHaveBeenCalledWith('/api/vocabulary?language=ja-JP')
    expect(mockApiFetch).not.toHaveBeenCalledWith(
      '/api/vocabulary?language=en-GB'
    )
  })

  it.each([429, 503])(
    'offers retry on curriculum HTTP %s and renders recovered competencies',
    async (status) => {
      mockApiFetch.mockImplementation(async (url: string) =>
        url.startsWith('/api/curriculum/') ? json({}, status) : responseFor(url)
      )
      renderWithMessages(<ProgressPage />)
      expect(await screen.findByRole('alert')).toBeInTheDocument()
      expect(screen.queryByText('125')).not.toBeInTheDocument()

      mockApiFetch.mockImplementation(async (url: string) => {
        if (url.startsWith('/api/curriculum/')) {
          return json([
            {
              id: 'a1-unit-1',
              level: 'A1',
              unit_number: 1,
              title: 'Greetings',
              default_weeks: 1,
              grammar_points: [],
              vocabulary_set_ids: ['greetings'],
              lesson_types: ['grammar'],
              competency_checklist: ['Introduce yourself', 'Ask a name'],
            },
          ])
        }
        if (url === '/api/progress/competencies') {
          return json([
            {
              unit_id: 'a1-unit-1',
              score: 0.6,
              mastered_count: 1,
              total_count: 2,
            },
          ])
        }
        if (url.startsWith('/api/vocabulary?')) {
          return json({
            sets: [
              {
                id: 'greetings',
                level: 'A1',
                topic: 'Meeting people',
                unit_ref: 'a1-unit-1',
                words: ['hello', 'goodbye'].map((word) => ({
                  word,
                  pos: 'phrase',
                  definition: word,
                  example: word,
                })),
              },
            ],
          })
        }
        if (url === '/api/flashcards/all') {
          return json([{ id: 1, word: ' HELLO ', repetitions: 1 }])
        }
        return responseFor(url)
      })
      fireEvent.click(screen.getByRole('button', { name: 'Retry' }))
      expect(
        await screen.findByRole('heading', { name: 'Greetings' })
      ).toHaveAttribute('lang', 'en-GB')
      expect(
        screen.getByRole('progressbar', {
          name: `Greetings: ${messages.progress.mastered}`,
        })
      ).toHaveAttribute('aria-valuenow', '50')
      expect(
        screen.getByRole('progressbar', { name: 'Meeting people' })
      ).toHaveAttribute('aria-valuenow', '50')
      expect(screen.getByText('Introduce yourself')).toHaveAttribute(
        'lang',
        'en-GB'
      )
      expect(screen.getByText('Meeting people')).toHaveAttribute('lang', 'en-GB')
    }
  )
})

describe('activity history', () => {
  it('uses a fixed UTC window across a year boundary and excludes out-of-window entries', () => {
    renderWithMessages(
      <ActivityHistory
        endDate="2026-01-02"
        entries={[
          { date: '2025-12-05', xp_earned: 999 },
          { date: '2025-12-06', xp_earned: 20 },
          { date: '2025-12-31', xp_earned: 0 },
          { date: '2026-01-02', xp_earned: 5 },
          { date: '2026-01-03', xp_earned: 999 },
        ]}
      />
    )
    const days = within(screen.getByRole('list')).getAllByRole('listitem')
    expect(days).toHaveLength(28)
    expect(days[0]).toHaveAccessibleName('6 Dec 2025: Practised, 20 XP')
    expect(days[27]).toHaveAccessibleName('2 Jan 2026: Practised, 5 XP')
    expect(screen.getByText('25 XP · Active days: 3/28')).toBeInTheDocument()
    expect(
      screen.getByRole('listitem', {
        name: '1 Jan 2026: No activity recorded, 0 XP',
      })
    ).toBeInTheDocument()
  })
})
