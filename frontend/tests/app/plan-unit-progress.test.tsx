import { beforeEach, describe, expect, it, vi } from 'vitest'
import { act, fireEvent, render, screen, within } from '@testing-library/react'
import React from 'react'
import { useLanguageStore } from '@/store/language'
import { getLanguageByCode } from '@/lib/target-languages'

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
  default: ({ href, children, ...props }: React.AnchorHTMLAttributes<HTMLAnchorElement>) =>
    React.createElement('a', { href: String(href), ...props }, children),
}))
vi.mock('@/lib/api', () => ({ apiFetch: mockApiFetch }))

import PlanPage from '@/app/(app)/plan/page'

function response(data: unknown, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  })
}

function scenario(language = 'it-IT') {
  const units = Array.from({ length: 8 }, (_, index) => ({
    id: `a1-unit-${index + 1}`,
    level: 'A1',
    unit_number: index + 1,
    title: `Unit ${index + 1}`,
    grammar_points: [],
    vocabulary_set_ids: [],
    lesson_types: ['grammar', 'vocabulary'],
    competency_checklist: ['Introduce yourself'],
    prerequisite_unit: index ? `a1-unit-${index}` : undefined,
  }))
  const slots = Array.from({ length: 48 }, (_, index) => ({
    week: Math.floor(index / 4) + 1,
    day: index % 4 + 1,
    title: `Lesson ${index + 1}`,
    lesson_type: 'grammar',
    unit_id: index === 47 ? 'completion-test' : `a1-unit-${Math.floor(index / 6) + 1}`,
  }))
  const lessons = slots.slice(0, 8).map((slot, index) => ({
    id: index + 1,
    title: slot.title,
    week_number: slot.week,
    day_number: slot.day,
    lesson_type: slot.lesson_type,
    unit_id: slot.unit_id,
    is_completed: index < 7,
  }))
  const plan = {
    id: 7,
    target_language: language,
    cefr_level: 'A1',
    duration_weeks: 12,
    days_per_week: 4,
    current_unit: units[0].id,
    progress_day: 7,
    completion_test_taken: false,
    completion_test_score: null,
    completion_test_recommendation: null,
    generated_plan: {
      weekly_plan: Array.from({ length: 12 }, (_, index) => ({
        week: index + 1,
        days: slots.filter((slot) => slot.week === index + 1),
      })),
    },
  }
  const today = {
    plan_id: plan.id,
    progress_day: 7,
    lessons: [{ ...slots[7], id: 8, is_completed: false }],
    completion: { state: 'in_progress', score: null, recommendation: null, next_level: null },
  }
  const data = { plan, units, lessons, today, pending: [] as typeof lessons }
  useLanguageStore.setState({
    activeLanguage: getLanguageByCode(language) ?? null,
    userLanguages: [],
    needsRefresh: false,
    isSwitching: false,
  })
  mockApiFetch.mockImplementation(async (url: string) => {
    switch (url) {
      case '/api/study-plan/current': return response(data.plan)
      case '/api/study-plan/lessons': return response(data.lessons)
      case '/api/study-plan/pending-lessons': return response(data.pending)
      case '/api/study-plan/today': return response(data.today)
      case `/api/curriculum/A1?language=${language}`: return response(data.units)
      case '/api/progress/competencies':
        return response(data.units.map((unit) => ({ unit_id: unit.id, score: 0.49 })))
      default: throw new Error(`Unexpected request: ${url}`)
    }
  })
  return data
}

function card(index: number) {
  return screen.getByText(`Unit ${index}`).closest('button')!.parentElement!
}

function button(index: number) {
  return screen.getByText(`Unit ${index}`).closest('button')!
}

async function loaded() {
  await screen.findByText('Unit 1')
}

describe('My Plan unit progression', () => {
  beforeEach(() => {
    mockApiFetch.mockReset()
    mockPush.mockReset()
  })

  it.each([
    'cs-CZ',
    'da-DK', 'de-DE', 'en-GB', 'en-US', 'es-ES', 'fr-FR', 'it-IT', 'ja-JP', 'ko-KR',
    'nl-NL', 'pl-PL', 'pt-BR', 'pt-PT', 'ru-RU', 'sv-SE', 'zh-CN',
  ])('moves the active card and review access to unit 2 in %s', async (language) => {
    scenario(language)
    render(<PlanPage />)
    await loaded()

    expect(within(card(1)).getByRole('img', { name: 'completed' })).toBeInTheDocument()
    expect(within(card(1)).getByText('100%')).toBeInTheDocument()
    expect(within(card(1)).queryByText('currentUnit')).not.toBeInTheDocument()
    expect(within(card(1)).queryByRole('button', { name: 'start →' })).not.toBeInTheDocument()
    expect(button(2)).not.toBeDisabled()
    expect(within(card(2)).getByText('currentUnit')).toBeInTheDocument()
    expect(within(card(2)).getByText('17%')).toBeInTheDocument()
    expect(button(3)).toBeDisabled()
    fireEvent.click(within(card(2)).getByRole('button', { name: 'start →' }))
    expect(mockPush).toHaveBeenLastCalledWith('/lesson/8')
    fireEvent.click(button(2))
    expect(screen.getByText('Lesson 7')).toBeInTheDocument()
    expect(screen.queryByText('Lesson 1')).not.toBeInTheDocument()
    fireEvent.click(screen.getByRole('button', { name: 'reviewLesson' }))
    expect(mockPush).toHaveBeenLastCalledWith('/lesson/7')
    expect(mockApiFetch).not.toHaveBeenCalledWith('/api/progress/competencies', expect.anything())
  })

  it('does not let mastery complete a unit or unlock the next one', async () => {
    const data = scenario()
    const normal = mockApiFetch.getMockImplementation()!
    mockApiFetch.mockImplementation((url: string, options?: RequestInit) =>
      url === '/api/progress/competencies'
        ? Promise.resolve(response(data.units.map((unit) => ({ unit_id: unit.id, score: 1 }))))
        : normal(url, options)
    )
    render(<PlanPage />)
    await loaded()
    expect(within(card(2)).queryByRole('img', { name: 'completed' })).not.toBeInTheDocument()
    expect(within(card(2)).getByText('17%')).toBeInTheDocument()
    expect(button(3)).toBeDisabled()
  })

  it('uses the persisted grid rather than curriculum order to identify the active unit', async () => {
    const data = scenario()
    data.units.reverse()
    render(<PlanPage />)
    await loaded()
    expect(within(card(2)).getByText('currentUnit')).toBeInTheDocument()
    fireEvent.click(within(card(2)).getByRole('button', { name: 'start →' }))
    expect(mockPush).toHaveBeenCalledWith('/lesson/8')
  })

  it('keeps skipped units accessible without counting ungenerated slots as complete', async () => {
    const data = scenario()
    data.plan.progress_day = data.today.progress_day = 13
    data.today.lessons = []
    data.lessons[0].is_completed = false
    data.pending = [data.lessons[0], data.lessons[7]]
    render(<PlanPage />)
    await loaded()
    expect(button(1)).not.toBeDisabled()
    expect(button(2)).not.toBeDisabled()
    expect(within(card(1)).getByText('83%')).toBeInTheDocument()
    expect(within(card(2)).getByText('17%')).toBeInTheDocument()
    expect(within(card(3)).getByText('currentUnit')).toBeInTheDocument()
    expect(within(card(3)).getByText('0%')).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'start →' })).not.toBeInTheDocument()
    fireEvent.click(button(2))
    expect(screen.getAllByRole('button', { name: 'resume' }).length).toBeGreaterThan(0)
    expect(screen.getByRole('button', { name: 'reviewLesson' })).toBeInTheDocument()
    expect(screen.getByText('Lesson 12')).toBeInTheDocument()
  })

  it.each(['completion-test', 'level-test'])('has no active teaching unit at the %s slot', async (unitId) => {
    const data = scenario()
    data.plan.generated_plan.weekly_plan[11].days[3].unit_id = unitId
    data.plan.progress_day = data.today.progress_day = 47
    data.today.lessons = []
    data.today.completion.state = 'ready'
    render(<PlanPage />)
    await loaded()
    expect(screen.queryByText('currentUnit')).not.toBeInTheDocument()
    expect(button(8)).not.toBeDisabled()
    expect(screen.getByText('completionTestTitle').closest('button')).not.toBeDisabled()
  })

  it('keeps unfinished units accessible after exhaustion without unlocking a pending assessment', async () => {
    const data = scenario()
    data.plan.progress_day = data.today.progress_day = 48
    data.today.lessons = []
    data.pending = [data.lessons[7]]
    render(<PlanPage />)
    await loaded()
    expect(screen.queryByText('currentUnit')).not.toBeInTheDocument()
    for (let index = 1; index <= 8; index++) expect(button(index)).not.toBeDisabled()
    expect(within(card(2)).getByText('17%')).toBeInTheDocument()
    expect(screen.getByText('completionTestTitle').closest('button')).toBeDisabled()
    expect(screen.getByRole('button', { name: 'resume' })).toBeInTheDocument()
  })

  it('uses a late auto-advance without waiting for it to display the plan', async () => {
    const data = scenario()
    data.plan.progress_day = 5
    const normal = mockApiFetch.getMockImplementation()!
    let finish!: (value: Response) => void
    mockApiFetch.mockImplementation((url: string) => url === '/api/study-plan/today'
      ? new Promise<Response>((resolve) => { finish = resolve })
      : normal(url))
    render(<PlanPage />)
    await loaded()
    expect(screen.queryByText('currentUnit')).not.toBeInTheDocument()
    await act(async () => finish(response(data.today)))
    expect(within(card(2)).getByText('currentUnit')).toBeInTheDocument()
    fireEvent.click(within(card(2)).getByRole('button', { name: 'start →' }))
    expect(mockPush).toHaveBeenCalledWith('/lesson/8')
  })

  it.each(['other-plan', 'older-position'])('ignores /today with %s', async (kind) => {
    const data = scenario()
    if (kind === 'other-plan') data.today.plan_id = 99
    else data.today.progress_day = 6
    data.today.completion.state = 'ready'
    data.today.lessons = [{ ...data.today.lessons[0], id: 99 }]
    render(<PlanPage />)
    await loaded()
    expect(within(card(2)).getByText('currentUnit')).toBeInTheDocument()
    fireEvent.click(within(card(2)).getByRole('button', { name: 'start →' }))
    expect(mockPush).toHaveBeenCalledWith('/lesson/8')
    expect(screen.queryByText('levelComplete')).not.toBeInTheDocument()
  })

  it('does not offer an older lesson from the same unit as the current CTA', async () => {
    const data = scenario()
    const previous = data.lessons[6]
    data.today.lessons = [{
      ...data.today.lessons[0], id: previous.id, title: previous.title,
      day: previous.day_number, week: previous.week_number,
    }]
    render(<PlanPage />)
    await loaded()
    fireEvent.click(within(card(2)).getByRole('button', { name: 'start →' }))
    expect(mockPush).toHaveBeenCalledWith('/lesson/8')
    fireEvent.click(button(2))
    fireEvent.click(screen.getByRole('button', { name: 'reviewLesson' }))
    expect(mockPush).toHaveBeenLastCalledWith('/lesson/7')
  })

  it('does not reopen completed lessons from stale pending and today snapshots', async () => {
    const data = scenario()
    data.lessons[7].is_completed = true
    data.pending = [{ ...data.lessons[6], is_completed: false }]
    render(<PlanPage />)
    await loaded()
    expect(within(card(2)).getByText('33%')).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'start →' })).not.toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'resume' })).not.toBeInTheDocument()
    fireEvent.click(button(2))
    expect(screen.getAllByRole('button', { name: 'reviewLesson' })).toHaveLength(2)
  })

  it('retains current and review actions when /today and pending metadata are unavailable', async () => {
    scenario()
    const normal = mockApiFetch.getMockImplementation()!
    mockApiFetch.mockImplementation((url: string) =>
      ['/api/study-plan/today', '/api/study-plan/pending-lessons'].includes(url)
        ? Promise.resolve(response({}, 503)) : normal(url))
    render(<PlanPage />)
    await loaded()
    expect(within(card(2)).getByText('currentUnit')).toBeInTheDocument()
    fireEvent.click(button(2))
    expect(screen.getByRole('button', { name: 'reviewLesson' })).toBeInTheDocument()
    fireEvent.click(screen.getAllByRole('button', { name: 'start →' }).at(-1)!)
    expect(mockPush).toHaveBeenCalledWith('/lesson/8')
  })

  it('offers retry rather than inventing zero completion when persisted lessons fail', async () => {
    scenario()
    const normal = mockApiFetch.getMockImplementation()!
    let failed = true
    mockApiFetch.mockImplementation((url: string) =>
      url === '/api/study-plan/lessons' && failed
        ? Promise.resolve(response({}, 503)) : normal(url))
    render(<PlanPage />)
    await screen.findByRole('alert')
    expect(screen.queryByText('Unit 1')).not.toBeInTheDocument()
    failed = false
    fireEvent.click(screen.getByRole('button', { name: 'retry' }))
    await loaded()
    expect(within(card(1)).getByText('100%')).toBeInTheDocument()
    expect(within(card(2)).getByText('currentUnit')).toBeInTheDocument()
  })
})
