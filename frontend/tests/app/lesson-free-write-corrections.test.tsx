import { act, fireEvent, render, screen, waitFor } from '@testing-library/react'
import type { ElementType, HTMLAttributes, ReactNode } from 'react'
import { beforeEach, describe, expect, it, vi } from 'vitest'

const mocks = vi.hoisted(() => ({
  apiFetch: vi.fn(),
}))

vi.mock('next/navigation', () => ({
  useParams: () => ({ id: '1' }),
  useRouter: () => ({ push: vi.fn(), replace: vi.fn() }),
  usePathname: () => '/lesson/1',
  useSearchParams: () => new URLSearchParams(),
}))
vi.mock('next/link', () => ({
  default: ({ children, href }: { children: ReactNode; href: string }) => (
    <a href={href}>{children}</a>
  ),
}))
vi.mock('next-intl', () => ({
  useTranslations: () => Object.assign((key: string) => key, { rich: (key: string) => key }),
  useLocale: () => 'en',
}))
vi.mock('@/lib/api', () => ({ apiFetch: mocks.apiFetch }))
vi.mock('@/store/auth', () => ({
  useAuthStore: (selector: (state: object) => unknown) =>
    selector({ user: { username: 'learner', native_language: 'en' } }),
  isSubscribed: () => true,
  isFreemiumTrialActive: () => false,
}))
vi.mock('@/store/language', () => ({
  useLanguageStore: (selector: (state: object) => unknown) =>
    selector({ activeLanguage: { code: 'de-DE' } }),
}))
vi.mock('@/store/config', () => ({
  useConfigStore: (selector: (state: object) => unknown) =>
    selector({ stripeEnabled: false }),
}))
vi.mock('@/store/freemium', () => ({
  useFreemiumStore: (selector: (state: object) => unknown) =>
    selector({ status: null, fetchStatus: vi.fn() }),
}))
vi.mock('@/store/progress', () => ({
  useProgressStore: (selector: (state: object) => unknown) =>
    selector({ completeLesson: vi.fn() }),
}))
vi.mock('@/data/grammar', () => ({
  getGrammarTopics: () => Promise.resolve([]),
}))
vi.mock('@/components/billing/PaywallBanner', () => ({
  PaywallBanner: () => null,
}))
vi.mock('@/components/billing/FreemiumQuotaBanner', () => ({
  FreemiumQuotaBanner: () => null,
}))
vi.mock('@/components/ui/AudioPlayer', () => ({ AudioPlayer: () => null }))
vi.mock('@/components/ui/VoiceRecorder', () => ({
  VoiceRecorder: () => null,
}))
vi.mock('@/components/ui/confirm-dialog', () => ({
  ConfirmDialog: () => null,
}))
vi.mock('@/components/ui/WordTooltip', () => ({
  WordTooltip: () => null,
  useWordSave: () => ({
    selectedWord: null,
    tooltipPos: null,
    saveState: 'idle',
    handleTextSelection: vi.fn(),
    handleSaveWord: vi.fn(),
    dismissTooltip: vi.fn(),
  }),
}))
vi.mock('@/components/ui/page-loading', () => ({ PageLoading: () => null }))
vi.mock('@/components/reviews/ReviewPrompt', () => ({
  ReviewPrompt: () => null,
  getReviewPromptDismissal: () => ({ count: 0, lastDismissedAt: null }),
}))
vi.mock('@/components/TargetLanguageText', () => ({
  TargetLanguageText: ({
    children,
    as: Component = 'div',
    languageCode,
    reading,
    translation,
    ...props
  }: {
    children: ReactNode
    as?: ElementType
    languageCode?: string | null
    reading?: string | null
    translation?: string | null
  } & HTMLAttributes<HTMLElement>) => {
    void languageCode
    void reading
    void translation
    return <Component {...props}>{children}</Component>
  },
}))

import LessonPage from '@/app/(app)/lesson/[id]/page'

const ANSWER = 'Ich habe viele abenteuer gehabt. Ich bin mit auto gefahren.'

const CORRECTIONS = [
  {
    original: 'abenteuer',
    corrected: 'Abenteuer',
    explanation: 'Nouns are capitalized in German.',
  },
  {
    original: 'mit auto',
    corrected: 'mit dem Auto',
    explanation: "Dative article after 'mit'.",
  },
  {
    original: 'Deutschalnd',
    corrected: 'Deutschland',
    explanation: 'Spelling of the country name.',
  },
]

function jsonResponse(data: unknown) {
  return new Response(JSON.stringify(data), {
    status: 200,
    headers: { 'Content-Type': 'application/json' },
  })
}

function lessonDetail(overrides: {
  isCompleted?: boolean
  exercise?: Record<string, unknown>
}) {
  return {
    lesson: {
      id: 1,
      study_plan_id: 1,
      title: 'Meine letzte Reise',
      lesson_type: 'writing',
      cefr_level: 'A2',
      content: {},
      is_completed: overrides.isCompleted ?? false,
    },
    exercises: [
      {
        id: 10,
        exercise_type: 'free_write',
        question: 'Describe your last trip.',
        options: ['grammar'],
        correct_answer: 'Sample answer.',
        explanation: null,
        native_explanation: null,
        user_answer: null,
        score: null,
        feedback: null,
        corrections: null,
        native_hint: null,
        ...overrides.exercise,
      },
    ],
  }
}

function mockApi(
  detail: ReturnType<typeof lessonDetail>,
  answerResult?: Record<string, unknown>
) {
  mocks.apiFetch.mockImplementation((url: string) => {
    if (url === '/api/lessons/1') return Promise.resolve(jsonResponse(detail))
    if (url === '/api/lessons/exercises/10/answer') {
      return Promise.resolve(jsonResponse(answerResult ?? {}))
    }
    return Promise.resolve(new Response(null, { status: 404 }))
  })
}

async function renderLesson() {
  let result!: ReturnType<typeof render>
  // Finish the mocked load and answer-restoration effect before interacting.
  // Finding the textarea alone can observe the DOM before that effect runs.
  await act(async () => {
    result = render(<LessonPage />)
  })
  return result
}

async function submitFreeWriteAnswer() {
  const textarea = screen.getByPlaceholderText('yourAnswer')
  fireEvent.change(textarea, { target: { value: ANSWER } })
  expect(textarea).toHaveValue(ANSWER)
  const submitButton = screen.getByRole('button', { name: 'submitAnswer' })
  expect(submitButton).toBeEnabled()
  fireEvent.click(submitButton)
  await waitFor(() =>
    expect(mocks.apiFetch).toHaveBeenCalledWith(
      '/api/lessons/exercises/10/answer',
      expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({ answer: ANSWER }),
      })
    )
  )
}

function annotatedBlock(container: HTMLElement): HTMLElement {
  const del = container.querySelector('del') as HTMLElement
  return del.closest('.whitespace-pre-wrap') as HTMLElement
}

// The score badge is the labelled icon rendered next to the answer field.
function scoreBadge(label: string): HTMLElement {
  return screen.getByRole('img', { name: label })
}

describe('LessonPage free-write corrections', () => {
  beforeEach(() => {
    mocks.apiFetch.mockReset()
  })

  it('offers voice practice when reviewing a completed lesson', async () => {
    mockApi(lessonDetail({ isCompleted: true }))
    await renderLesson()
    expect(await screen.findByRole('button', { name: 'action' })).toBeInTheDocument()
  })

  it('does not offer lesson practice before completion', async () => {
    mockApi(lessonDetail({}))
    await renderLesson()
    await screen.findByPlaceholderText('yourAnswer')
    expect(screen.queryByRole('button', { name: 'action' })).toBeNull()
  })

  it('offers practice immediately after successful lesson completion', async () => {
    const detail = lessonDetail({ exercise: { user_answer: ANSWER, score: 1 } })
    mocks.apiFetch.mockImplementation((url: string) => {
      if (url === '/api/lessons/1') return Promise.resolve(jsonResponse(detail))
      if (url === '/api/lessons/1/complete') {
        return Promise.resolve(jsonResponse({ ...detail.lesson, is_completed: true }))
      }
      return Promise.resolve(new Response(null, { status: 404 }))
    })
    await renderLesson()
    fireEvent.click(await screen.findByRole('button', { name: 'completeLesson' }))
    await screen.findByText('lessonDone')
    expect(screen.getByRole('button', { name: 'action' })).toBeInTheDocument()
  })

  it('renders inline annotations, the corrections list and the amber state after evaluation', async () => {
    mockApi(lessonDetail({}), {
      id: 10,
      score: 0.8,
      feedback: 'Great job!',
      correct_answer: 'Sample answer.',
      corrections: CORRECTIONS,
    })
    const { container } = await renderLesson()

    await submitFreeWriteAnswer()

    await waitFor(() =>
      expect(screen.queryByPlaceholderText('yourAnswer')).toBeNull()
    )
    const block = annotatedBlock(container)
    expect(block.textContent).toBe(
      'Ich habe viele abenteuer Abenteuer gehabt. Ich bin mit auto mit dem Auto gefahren.'
    )
    expect(block.className).toContain('border-fl-warning/50')
    const inlineDeletions = Array.from(block.querySelectorAll('del')).map(
      (el) => el.textContent
    )
    const inlineInsertions = Array.from(block.querySelectorAll('ins')).map(
      (el) => el.textContent
    )
    expect(inlineDeletions).toEqual(['abenteuer', 'mit auto'])
    expect(inlineInsertions).toEqual(['Abenteuer', 'mit dem Auto'])

    expect(scoreBadge('corrections')).toHaveClass('text-fl-warning')

    // Corrections list shows every correction, including the one whose
    // fragment does not occur in the answer.
    const list = screen.getByText('corrections').closest('div') as HTMLElement
    const items = list.querySelectorAll('li')
    expect(items).toHaveLength(3)
    expect(items[2].querySelector('del')?.textContent).toBe('Deutschalnd')
    expect(items[2].querySelector('ins')?.textContent).toBe('Deutschland')
    expect(items[2].textContent).toContain('Spelling of the country name.')
    for (const item of items) {
      expect(item.querySelector('del')).toHaveClass('text-fl-error-fg')
      expect(item.querySelector('ins')).toHaveClass('text-fl-success')
      expect(item.querySelector('p')).toHaveClass('text-base')
      expect(item.querySelector('p')).not.toHaveClass('text-sm')
      expect(item.querySelector('p:last-child')).toHaveClass('text-sm')
    }
    expect(screen.getByText('Great job!')).toBeInTheDocument()
  })

  it('renders persisted corrections when reviewing a completed lesson', async () => {
    mockApi(
      lessonDetail({
        isCompleted: true,
        exercise: {
          user_answer: ANSWER,
          score: 0.8,
          feedback: 'Great job!',
          corrections: CORRECTIONS,
        },
      })
    )
    const { container } = await renderLesson()

    await screen.findByText('corrections')

    expect(screen.queryByPlaceholderText('yourAnswer')).toBeNull()
    const block = annotatedBlock(container)
    expect(block.className).toContain('border-fl-warning/50')
    expect(
      Array.from(block.querySelectorAll('ins')).map((el) => el.textContent)
    ).toEqual(['Abenteuer', 'mit dem Auto'])
    expect(scoreBadge('corrections')).toHaveClass('text-fl-warning')
    expect(
      screen.getByText('corrections').closest('div')?.querySelectorAll('li')
    ).toHaveLength(3)
  })

  it('keeps the red state and no corrections list for the unevaluated fallback', async () => {
    mockApi(lessonDetail({}), {
      id: 10,
      score: 0.5,
      feedback: 'Could not evaluate the answer.',
      correct_answer: 'Sample answer.',
      corrections: null,
    })
    const { container } = await renderLesson()

    await submitFreeWriteAnswer()

    await screen.findByText('Could not evaluate the answer.')
    const textarea = screen.getByPlaceholderText('yourAnswer')
    expect(textarea).toBeDisabled()
    expect(textarea.className).toContain('border-fl-error-fg/50')
    expect(scoreBadge('incorrect')).toHaveClass('text-fl-error-fg')
    expect(screen.queryByRole('img', { name: 'corrections' })).toBeNull()
    expect(screen.queryByText('corrections')).toBeNull()
    expect(container.querySelector('del')).toBeNull()
  })

  it('shows a partial score without corrections as red', async () => {
    mockApi(lessonDetail({}), {
      id: 10,
      score: 0.8,
      feedback: 'Good.',
      correct_answer: 'Sample answer.',
      corrections: [],
    })
    await renderLesson()

    await submitFreeWriteAnswer()

    await screen.findByText('Good.')
    expect(scoreBadge('incorrect')).toHaveClass('text-fl-error-fg')
    expect(screen.queryByText('corrections')).toBeNull()
  })
})
