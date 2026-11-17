import { describe, it, expect, vi, beforeEach } from 'vitest'
import {
  render,
  screen,
  fireEvent,
  within,
  waitFor,
} from '@testing-library/react'
import React from 'react'
import UnitCard from '@/components/plan/UnitCard'
import UnitDrawer from '@/components/plan/UnitDrawer'
import type { CurriculumUnit } from '@/data/curriculum'

// ── Mocks ──────────────────────────────────────────────────────────────────

vi.mock('next-intl', () => ({
  useTranslations: () => (key: string) => key,
}))

vi.mock('next/image', () => ({
  default: function MockImage(
    props: React.ImgHTMLAttributes<HTMLImageElement> & {
      unoptimized?: boolean
      priority?: boolean
    }
  ) {
    const { unoptimized, priority, ...imgProps } = props
    void unoptimized
    void priority
    return React.createElement('img', imgProps)
  },
}))

// next/navigation is already mocked in tests/setup.ts

// ── Helpers ────────────────────────────────────────────────────────────────

type UnitStatus = {
  completed: boolean
  active: boolean
  locked: boolean
  isLevelTest: boolean
}

const defaultStatus: UnitStatus = {
  completed: false,
  active: false,
  locked: false,
  isLevelTest: false,
}

function renderUnitCard(
  overrides: Partial<{
    title: string
    index: number
    lessonCount: number
    grammarCount: number
    progress: number
    status: Partial<UnitStatus>
    onClick: () => void
    onStartLesson: () => void
  }> = {}
) {
  const props = {
    title: overrides.title ?? 'Basic Greetings',
    index: overrides.index ?? 0,
    lessonCount: overrides.lessonCount ?? 5,
    grammarCount: overrides.grammarCount ?? 2,
    progress: overrides.progress ?? 0.6,
    status: { ...defaultStatus, ...overrides.status },
    onClick: overrides.onClick ?? vi.fn(),
    onStartLesson: overrides.onStartLesson,
  }
  const result = render(<UnitCard {...props} />)
  return { ...result, props }
}

// ── UnitCard tests ─────────────────────────────────────────────────────────

describe('UnitCard', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  // ── Status states ──────────────────────────────────────────────────────

  it('renders completed unit with checkmark icon', () => {
    renderUnitCard({ status: { completed: true }, progress: 1 })
    expect(screen.getByRole('img', { name: 'completed' })).toBeInTheDocument()
    expect(screen.queryByText('currentUnit')).not.toBeInTheDocument()
  })

  it('renders active unit with pulsing dot icon', () => {
    renderUnitCard({ status: { active: true } })
    const dot = screen.getByRole('img', { name: 'currentUnit' })
    expect(dot).toBeInTheDocument()
    expect(dot.querySelector('svg')).toHaveClass('animate-pulse')
    expect(dot.querySelector('svg')).toHaveClass('motion-reduce:animate-none')
    expect(dot.querySelector('svg')).toHaveAttribute('aria-hidden', 'true')
    expect(
      screen.getByRole('button', { name: 'unitAriaLabel' })
    ).toHaveAttribute('aria-describedby', dot.id)
    expect(screen.getByText('currentUnit')).toBeInTheDocument()
  })

  it('keeps locked unit titles readable while disabling access', () => {
    renderUnitCard({ status: { locked: true } })
    expect(screen.getByRole('img', { name: 'unitLocked' })).toBeInTheDocument()
    expect(screen.getByText('Basic Greetings')).toBeVisible()
    expect(screen.getByRole('button', { name: 'unitAriaLabel' })).toBeDisabled()
  })

  it('renders level-test unit with special icon and badge', () => {
    renderUnitCard({ status: { isLevelTest: true, active: true } })
    expect(
      screen.getByRole('img', { name: 'levelTestLabel' })
    ).toBeInTheDocument()
    expect(screen.getByText('levelTestLabel')).toBeInTheDocument()
    expect(screen.queryByText('currentUnit')).not.toBeInTheDocument()
  })

  it('renders default state (none of the flags) with hollow dot', () => {
    renderUnitCard()
    expect(
      screen.getByRole('img', { name: 'unitAvailable' })
    ).toBeInTheDocument()
  })

  // ── Card content ───────────────────────────────────────────────────────

  it('renders padded unit index', () => {
    renderUnitCard({ index: 3 })
    expect(screen.getByText('04')).toBeInTheDocument()
  })

  it('renders the unit title', () => {
    renderUnitCard({ title: 'Past Tenses' })
    expect(screen.getByText('Past Tenses')).toBeInTheDocument()
  })

  it('renders lesson count translation key', () => {
    renderUnitCard({ lessonCount: 5 })
    expect(screen.getByText('nLessons')).toBeInTheDocument()
  })

  it('renders grammar count when grammarCount > 0', () => {
    renderUnitCard({ grammarCount: 3 })
    expect(screen.getByText('nGrammar')).toBeInTheDocument()
  })

  it('does not render grammar count when grammarCount is 0', () => {
    renderUnitCard({ grammarCount: 0 })
    expect(screen.queryByText('nGrammar')).toBeNull()
  })

  // ── Progress bar ───────────────────────────────────────────────────────

  it('renders progress bar for non-locked units', () => {
    const { container } = renderUnitCard({ progress: 0.42 })
    expect(screen.getByText('42%')).toBeInTheDocument()
    const bar = container.querySelector('.bg-fl-fg.h-full') as HTMLElement
    expect(bar).toBeInTheDocument()
    expect(bar.style.width).toBe('42%')
  })

  it('renders 0% progress bar when progress is 0', () => {
    const { container } = renderUnitCard({ progress: 0 })
    expect(screen.getByText('0%')).toBeInTheDocument()
    const bar = container.querySelector('.bg-fl-fg.h-full') as HTMLElement
    expect(bar.style.width).toBe('0%')
  })

  it('shows completed progress compactly without a redundant bar', () => {
    const { container } = renderUnitCard({
      progress: 1,
      status: { completed: true },
    })
    expect(screen.getByText('100%')).toBeInTheDocument()
    expect(container.querySelector('.bg-fl-fg.h-full')).toBeNull()
  })

  it('does not render progress bar for locked units', () => {
    const { container } = renderUnitCard({ status: { locked: true } })
    expect(container.querySelector('.bg-fl-fg.h-full')).toBeNull()
    expect(screen.queryByText(/%$/)).toBeNull()
  })

  // ── Click interaction ──────────────────────────────────────────────────

  it('calls onClick when card header is clicked', () => {
    const onClick = vi.fn()
    renderUnitCard({ onClick })
    const button = screen.getByLabelText('unitAriaLabel')
    fireEvent.click(button)
    expect(onClick).toHaveBeenCalledTimes(1)
  })

  it('does not call onClick when locked unit is clicked (button disabled)', () => {
    const onClick = vi.fn()
    renderUnitCard({ onClick, status: { locked: true } })
    const button = screen.getByLabelText('unitAriaLabel')
    expect(button).toBeDisabled()
    fireEvent.click(button)
    expect(onClick).not.toHaveBeenCalled()
  })

  // ── Start lesson button ────────────────────────────────────────────────

  it('shows start button when active and onStartLesson is provided', () => {
    const onStartLesson = vi.fn()
    renderUnitCard({ status: { active: true }, onStartLesson })
    expect(screen.getByText(/start/)).toBeInTheDocument()
  })

  it('calls onStartLesson when start button is clicked', () => {
    const onStartLesson = vi.fn()
    renderUnitCard({ status: { active: true }, onStartLesson })
    fireEvent.click(screen.getByText(/start/))
    expect(onStartLesson).toHaveBeenCalledTimes(1)
  })

  it('does not show start button when active but onStartLesson is not provided', () => {
    renderUnitCard({ status: { active: true } })
    expect(screen.queryByText(/start/)).toBeNull()
  })

  it('does not show start button when not active (even with onStartLesson)', () => {
    renderUnitCard({ onStartLesson: vi.fn() })
    expect(screen.queryByText(/start/)).toBeNull()
  })

  it('does not show start button when locked (even with onStartLesson)', () => {
    renderUnitCard({ status: { locked: true }, onStartLesson: vi.fn() })
    expect(screen.queryByText(/start/)).toBeNull()
  })
})

// ── UnitDrawer tests ───────────────────────────────────────────────────────

const mockUnit: CurriculumUnit = {
  id: 'unit-a1-1',
  level: 'A1',
  unit_number: 1,
  title: 'Greetings & Introductions',
  default_weeks: 2,
  grammar_points: ['presente de indicativo', 'verbos ser/estar'],
  vocabulary_set_ids: ['v1', 'v2'],
  lesson_types: ['grammar', 'vocabulary', 'reading'],
  prerequisite_unit: undefined,
  competency_checklist: ['Can greet people', 'Can introduce oneself'],
}

const mockUnitNoGrammar: CurriculumUnit = {
  ...mockUnit,
  grammar_points: [],
}

const mockLessons = [
  {
    id: 1,
    title: 'Verb Conjugation',
    lesson_type: 'grammar',
    week: 1,
    day: 1,
    completed: true,
    action: 'review' as const,
  },
  {
    id: 2,
    title: 'Common Phrases',
    lesson_type: 'vocabulary',
    week: 1,
    day: 2,
    completed: false,
    action: 'continue' as const,
  },
  {
    id: 3,
    title: 'Reading Comprehension',
    lesson_type: 'reading',
    week: 2,
    day: 1,
    completed: false,
    action: 'start' as const,
  },
]

const mockLessonsWithNullId = [
  {
    id: null,
    title: 'Pending Content',
    lesson_type: 'review',
    week: 3,
    day: 1,
    completed: false,
  },
  {
    id: 4,
    title: 'Final Test',
    lesson_type: 'review',
    week: 3,
    day: 2,
    completed: false,
    action: 'start' as const,
  },
]

function renderUnitDrawer(
  overrides: Partial<{
    unit: CurriculumUnit
    lessons: Array<{
      id: number | null
      title: string
      lesson_type: string
      week: number
      day: number
      completed: boolean
      action?: 'start' | 'continue' | 'review'
    }>
    onClose: () => void
    onStartLesson: (lessonId: number) => void
  }> = {}
) {
  const props = {
    unit: overrides.unit ?? mockUnit,
    lessons: overrides.lessons ?? mockLessons,
    onClose: overrides.onClose ?? vi.fn(),
    onStartLesson: overrides.onStartLesson ?? vi.fn(),
  }
  const result = render(<UnitDrawer {...props} />)
  return { ...result, props }
}

describe('UnitDrawer', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  // ── Header ─────────────────────────────────────────────────────────────

  it('renders unit level and label in header', () => {
    renderUnitDrawer()
    expect(screen.getByText(/A1/)).toBeInTheDocument()
    expect(screen.getByText(/unitLabel/)).toBeInTheDocument()
  })

  it('renders unit title in header', () => {
    renderUnitDrawer()
    expect(screen.getByText('Greetings & Introductions')).toBeInTheDocument()
  })

  it('opens a labelled modal with its real lesson progress', async () => {
    renderUnitDrawer()
    const dialog = screen.getByRole('dialog', { name: mockUnit.title })
    const heading = within(dialog).getByRole('heading', {
      name: mockUnit.title,
    })
    await waitFor(() => expect(heading).toHaveFocus())
    expect(dialog).toHaveAttribute('aria-describedby')
    expect(within(dialog).getByRole('progressbar')).toHaveAttribute(
      'aria-valuenow',
      '1'
    )
    expect(within(dialog).getByRole('progressbar')).toHaveAttribute(
      'aria-valuemax',
      '3'
    )
  })

  // ── Grammar points ─────────────────────────────────────────────────────

  it('renders grammar points section when grammar_points is non-empty', () => {
    renderUnitDrawer()
    expect(screen.getByText('grammarCovered')).toBeInTheDocument()
    fireEvent.click(screen.getByText('grammarCovered'))
    expect(screen.getByText('presente de indicativo')).toBeInTheDocument()
    expect(screen.getByText('verbos ser/estar')).toBeInTheDocument()
  })

  it('does not render grammar section when grammar_points is empty', () => {
    renderUnitDrawer({ unit: mockUnitNoGrammar })
    expect(screen.queryByText('grammarCovered')).toBeNull()
  })

  // ── Lessons list ───────────────────────────────────────────────────────

  it('renders all lesson titles', () => {
    renderUnitDrawer()
    expect(screen.getByText('lessonsHeader')).toBeInTheDocument()
    expect(screen.getByText('Verb Conjugation')).toBeInTheDocument()
    expect(screen.getByText('Common Phrases')).toBeInTheDocument()
    expect(screen.getByText('Reading Comprehension')).toBeInTheDocument()
  })

  it('marks completed lessons while keeping their titles readable for review', () => {
    renderUnitDrawer()
    const row = screen.getByText('Verb Conjugation').closest('li')!
    expect(
      within(row).getByRole('img', { name: 'completed' })
    ).toBeInTheDocument()
    expect(
      within(row).getByRole('button', { name: 'reviewLesson' })
    ).toBeInTheDocument()
  })

  it('distinguishes the current lesson from other incomplete lessons', () => {
    renderUnitDrawer()
    const circles = screen.getAllByRole('img', { name: 'lessonPending' })
    expect(circles.length).toBe(1)
    const current = screen.getByRole('img', { name: 'currentLesson' })
    expect(current.closest('li')).toHaveAttribute('aria-current', 'step')
  })

  it('renders lesson type label for each lesson', () => {
    renderUnitDrawer()
    expect(screen.getByText(/lessonTypes\.grammar/)).toBeInTheDocument()
    expect(screen.getByText(/lessonTypes\.vocabulary/)).toBeInTheDocument()
    expect(screen.getByText(/lessonTypes\.reading/)).toBeInTheDocument()
  })

  it('renders week/day info for each lesson', () => {
    renderUnitDrawer()
    const weekDayEls = screen.getAllByText(/weekDay/)
    expect(weekDayEls.length).toBe(3)
  })

  it('shows empty state when lessons array is empty', () => {
    renderUnitDrawer({ lessons: [] })
    expect(screen.getByText('noLessons')).toBeInTheDocument()
  })

  // ── Lesson action buttons ──────────────────────────────────────────────

  it('renders the action matching each available lesson state', () => {
    renderUnitDrawer()
    expect(screen.getByText('reviewLesson')).toBeInTheDocument()
    expect(screen.getByText('resume')).toBeInTheDocument()
    expect(screen.getByText('start →')).toBeInTheDocument()
  })

  it('does not render start button when lesson id is null', () => {
    renderUnitDrawer({ lessons: mockLessonsWithNullId })
    expect(screen.getAllByText('start →')).toHaveLength(1)
  })

  it('keeps scheduled lesson identities stable when numeric IDs collide with list positions', () => {
    const consoleError = vi.spyOn(console, 'error').mockImplementation(() => {})
    const lessons = [
      mockLessons[0],
      { ...mockLessonsWithNullId[0], week: 1, day: 2 },
    ]
    const { rerender, props } = renderUnitDrawer({ lessons })
    const scheduledRow = screen.getByText('Pending Content').closest('li')
    expect(screen.getAllByText('Verb Conjugation')).toHaveLength(1)
    expect(screen.getAllByText('Pending Content')).toHaveLength(1)
    expect(consoleError).not.toHaveBeenCalled()

    rerender(
      <UnitDrawer
        {...props}
        lessons={[lessons[0], { ...lessons[1], id: 9, action: 'start' }]}
      />
    )
    expect(screen.getByText('Pending Content').closest('li')).toBe(scheduledRow)
    fireEvent.click(screen.getByRole('button', { name: 'start →' }))
    expect(props.onStartLesson).toHaveBeenCalledWith(9)
    expect(consoleError).not.toHaveBeenCalled()
  })

  it('calls onStartLesson with correct lesson id when start is clicked', () => {
    const onStartLesson = vi.fn()
    renderUnitDrawer({ onStartLesson })
    fireEvent.click(screen.getByText('resume'))
    expect(onStartLesson).toHaveBeenCalledTimes(1)
    expect(onStartLesson).toHaveBeenCalledWith(2)
  })

  it('opens a completed lesson for review', () => {
    const onStartLesson = vi.fn()
    renderUnitDrawer({ onStartLesson })
    fireEvent.click(screen.getByText('reviewLesson'))
    expect(onStartLesson).toHaveBeenCalledWith(1)
  })

  // ── Close interactions ─────────────────────────────────────────────────

  it('closes on X button click', () => {
    const onClose = vi.fn()
    renderUnitDrawer({ onClose })
    fireEvent.click(screen.getAllByRole('button', { name: 'close' })[0])
    expect(onClose).toHaveBeenCalledTimes(1)
  })

  it('closes on bottom close button click', () => {
    const onClose = vi.fn()
    renderUnitDrawer({ onClose })
    const closeButtons = screen.getAllByText('close')
    const bottomButton = closeButtons.find((btn) => btn.tagName === 'BUTTON')
    fireEvent.click(bottomButton!)
    expect(onClose).toHaveBeenCalledTimes(1)
  })

  it('closes on Escape key press', () => {
    const onClose = vi.fn()
    renderUnitDrawer({ onClose })
    fireEvent.keyDown(document, { key: 'Escape' })
    expect(onClose).toHaveBeenCalledTimes(1)
  })

  it('does not close on non-Escape key press', () => {
    const onClose = vi.fn()
    renderUnitDrawer({ onClose })
    fireEvent.keyDown(document, { key: 'Enter' })
    expect(onClose).not.toHaveBeenCalled()
  })

  it('closes on an outside click on the portal backdrop', () => {
    const onClose = vi.fn()
    renderUnitDrawer({ onClose })
    const backdrop = document.querySelector(
      '[data-slot="unit-dialog-backdrop"]'
    )!
    fireEvent.mouseDown(backdrop)
    fireEvent.mouseUp(backdrop)
    fireEvent.click(backdrop)
    expect(onClose).toHaveBeenCalledTimes(1)
  })

  it('does not close when clicking inside drawer content', () => {
    const onClose = vi.fn()
    renderUnitDrawer({ onClose })
    // Click inside the drawer (e.g., on a lesson title)
    fireEvent.mouseDown(screen.getByText('Verb Conjugation'))
    expect(onClose).not.toHaveBeenCalled()
  })

  it('restores focus to the opener after closing', async () => {
    function Harness() {
      const [open, setOpen] = React.useState(false)
      return (
        <>
          <button onClick={() => setOpen(true)}>Open unit</button>
          {open && (
            <UnitDrawer
              unit={mockUnit}
              lessons={mockLessons}
              onClose={() => setOpen(false)}
              onStartLesson={vi.fn()}
            />
          )}
        </>
      )
    }
    render(<Harness />)
    const opener = screen.getByRole('button', { name: 'Open unit' })
    opener.focus()
    fireEvent.click(opener)
    const heading = screen.getByRole('heading', { name: mockUnit.title })
    await waitFor(() => expect(heading).toHaveFocus())
    fireEvent.click(screen.getAllByRole('button', { name: 'close' })[0])
    await waitFor(() => expect(opener).toHaveFocus())
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
  })
})
