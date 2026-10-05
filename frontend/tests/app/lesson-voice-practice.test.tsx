import { act, cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

const mocks = vi.hoisted(() => ({
  apiFetch: vi.fn(),
  push: vi.fn(),
  params: 'lesson=7',
  voice: vi.fn(),
}))

vi.mock('next/navigation', () => ({
  useRouter: () => ({ push: mocks.push }),
  useSearchParams: () => new URLSearchParams(mocks.params),
}))
vi.mock('next-intl', async (importOriginal) => {
  const { createTranslator } = await importOriginal<typeof import('next-intl')>()
  const { default: messages } = await import('../../../messages/es.json')
  const practice = createTranslator({ locale: 'es', messages, namespace: 'lessonPractice' })
  return {
    useLocale: () => 'es',
    useTranslations: (namespace: string) => Object.assign(
      (key: string) => `${namespace}.${key}`,
      { rich: practice.rich }
    ),
  }
})
vi.mock('next/dynamic', () => ({
  default: () => function Voice(props: Record<string, unknown>) {
    mocks.voice(props)
    return <div data-testid="voice" />
  },
}))
vi.mock('@/lib/api', () => ({ apiFetch: mocks.apiFetch }))
vi.mock('@/components/ui/page-loading', () => ({
  PageLoading: () => <div data-testid="loading" />,
}))
vi.mock('@/components/billing/PaywallBanner', () => ({
  PaywallBanner: () => <div data-testid="paywall" />,
}))
vi.mock('@/components/billing/FreemiumQuotaBanner', () => ({
  FreemiumQuotaBanner: () => null,
}))

import ConversationPage from '@/app/(app)/conversation/page'
import { LessonVoicePracticeButton } from '@/components/lesson/LessonVoicePracticeButton'
import { useAuthStore } from '@/store/auth'
import { useConfigStore } from '@/store/config'
import { useFreemiumStore } from '@/store/freemium'
import { useLanguageStore } from '@/store/language'
import { getLanguageByCode } from '@/lib/target-languages'

function detail(overrides: Record<string, unknown> = {}) {
  return {
    target_language: 'fr-FR',
    lesson: {
      id: 7,
      title: 'Raconter un voyage',
      cefr_level: 'B1',
      is_completed: true,
      ...overrides,
    },
  }
}

function response(data: unknown, status = 200) {
  return new Response(JSON.stringify(data), { status })
}

beforeEach(() => {
  vi.clearAllMocks()
  mocks.params = 'lesson=7'
  mocks.apiFetch.mockReset().mockImplementation((url: string) =>
    Promise.resolve(url === '/api/lessons/7' ? response(detail()) : response({}, 404))
  )
  sessionStorage.clear()
  useAuthStore.setState({
    accessToken: 'token',
    user: {
      id: 1,
      username: 'learner',
      displayName: 'Learner',
      role: 'user',
      conversation_max_duration: 30,
      conversation_inactivity_timeout: 3,
      subscription_status: 'none',
    },
  })
  useConfigStore.setState({ stripeEnabled: false, maintenanceMode: false })
  useLanguageStore.setState({ activeLanguage: getLanguageByCode('en-GB') ?? null })
  useFreemiumStore.setState({ status: null, loaded: false })
})

afterEach(() => cleanup())

describe('Lesson practice entry', () => {
  it('opens a summary and navigates only after confirmation', () => {
    render(<LessonVoicePracticeButton lessonId={7} title="Raconter un voyage" targetLanguage="fr-FR" />)
    expect(screen.queryByRole('alertdialog')).toBeNull()
    fireEvent.click(screen.getByRole('button', { name: 'lessonPractice.action' }))
    expect(screen.getByRole('alertdialog')).toHaveAccessibleName('Práctica: Raconter un voyage')
    const topic = screen.getByText('Raconter un voyage')
    expect(topic).toHaveAttribute('lang', 'fr-FR')
    expect(topic.parentElement).toHaveAttribute('lang', 'es')
    expect(topic.parentElement).toHaveTextContent('Práctica: Raconter un voyage')
    expect(screen.getByText('lessonPractice.description')).toBeInTheDocument()
    expect(mocks.push).not.toHaveBeenCalled()
    expect(mocks.apiFetch).not.toHaveBeenCalled()
    fireEvent.click(screen.getByRole('button', { name: 'lessonPractice.cancel' }))
    expect(screen.queryByRole('alertdialog')).toBeNull()
    expect(mocks.push).not.toHaveBeenCalled()
    fireEvent.click(screen.getByRole('button', { name: 'lessonPractice.action' }))
    fireEvent.click(screen.getByRole('button', { name: 'lessonPractice.start' }))
    expect(mocks.push).toHaveBeenCalledExactlyOnceWith('/conversation?lesson=7')
  })

  it('uses the persisted lesson language and ignores unrelated chat and demo context', async () => {
    sessionStorage.setItem('voice_context', JSON.stringify([{ role: 'user', content: 'Other chat' }]))
    sessionStorage.setItem('assessment_voice_trial', JSON.stringify({ token: 'old-demo' }))
    render(<ConversationPage />)
    await screen.findByTestId('voice')
    expect(mocks.voice).toHaveBeenLastCalledWith(expect.objectContaining({
      lessonId: 7,
      lessonTitle: 'Raconter un voyage',
      targetLanguage: 'fr-FR',
      cefrLevel: 'B1',
      autoStart: true,
      initialContext: undefined,
    }))
    expect(mocks.voice.mock.lastCall?.[0].voiceTrialToken).toBeUndefined()
    expect(mocks.apiFetch.mock.calls.map(([url]) => url)).toEqual(['/api/lessons/7'])
    act(() => useLanguageStore.setState({ activeLanguage: getLanguageByCode('de-DE') ?? null }))
    expect(mocks.voice.mock.lastCall?.[0].targetLanguage).toBe('fr-FR')
    expect(mocks.voice.mock.lastCall?.[0].lessonId).toBe(7)
  })

  it.each(['', '0', '-1', 'abc', '1.2', '2147483648', '9007199254740991', '9007199254740992', '9223372036854775808'])('rejects invalid lesson query %s without starting generic voice', async (id) => {
    mocks.params = `lesson=${id}`
    render(<ConversationPage />)
    await screen.findByRole('alert')
    expect(mocks.apiFetch).not.toHaveBeenCalled()
    expect(mocks.voice).not.toHaveBeenCalled()
  })

  it('accepts the largest lesson ID supported by the database', async () => {
    mocks.params = 'lesson=2147483647'
    mocks.apiFetch.mockResolvedValue(response(detail({ id: 2147483647 })))
    render(<ConversationPage />)
    await screen.findByTestId('voice')
    expect(mocks.apiFetch).toHaveBeenCalledWith('/api/lessons/2147483647', expect.any(Object))
    expect(mocks.voice.mock.lastCall?.[0].lessonId).toBe(2147483647)
  })

  it.each([
    response({}, 404),
    response(detail({ is_completed: false })),
    response(detail({ id: 8 })),
    response({ lesson: detail().lesson }),
  ])('does not fall back to a generic session when lesson context is unavailable', async (res) => {
    mocks.apiFetch.mockResolvedValue(res)
    render(<ConversationPage />)
    await screen.findByRole('alert')
    expect(mocks.voice).not.toHaveBeenCalled()
  })

  it('retries a failed lesson lookup', async () => {
    mocks.apiFetch.mockRejectedValueOnce(new Error('Network'))
    render(<ConversationPage />)
    await screen.findByRole('alert')
    fireEvent.click(screen.getByRole('button', { name: 'common.retry' }))
    await screen.findByTestId('voice')
    expect(mocks.apiFetch).toHaveBeenCalledTimes(2)
  })

  it('aborts loading on exit and ignores its late result', async () => {
    let resolve!: (value: Response) => void
    mocks.apiFetch.mockReturnValue(new Promise<Response>((done) => { resolve = done }))
    const view = render(<ConversationPage />)
    const signal = mocks.apiFetch.mock.calls[0][1].signal as AbortSignal
    view.unmount()
    expect(signal.aborted).toBe(true)
    await act(async () => { resolve(response(detail())) })
    expect(mocks.voice).not.toHaveBeenCalled()
  })

  it('keeps the existing voice paywall when the free quota is exhausted', async () => {
    useConfigStore.setState({ stripeEnabled: true })
    useFreemiumStore.setState({
      loaded: true,
      lastFetch: Date.now(),
      status: {
        trial_active: false,
        trial_ends_at: null,
        chat_remaining: 5,
        chat_limit: 5,
        lessons_remaining: 3,
        lessons_limit: 3,
        listening_remaining: 3,
        listening_limit: 3,
        reading_remaining: 3,
        reading_limit: 3,
        voice_remaining_seconds: 0,
        voice_limit_seconds: 300,
      },
    })
    render(<ConversationPage />)
    await screen.findByTestId('paywall')
    expect(mocks.voice).not.toHaveBeenCalled()
  })

  it('keeps maintenance gating', async () => {
    useConfigStore.setState({ maintenanceMode: true })
    render(<ConversationPage />)
    await screen.findByText('maintenance.title')
    expect(mocks.voice).not.toHaveBeenCalled()
  })

  it('preserves the ordinary voice entry from text chat', async () => {
    mocks.params = ''
    const messages = [{ role: 'user', content: 'Books' }]
    sessionStorage.setItem('voice_context', JSON.stringify({ messages }))
    mocks.apiFetch.mockResolvedValue(response({ cefr_level: 'A2' }))
    render(<ConversationPage />)
    await screen.findByTestId('voice')
    await waitFor(() => expect(mocks.voice).toHaveBeenLastCalledWith(expect.objectContaining({
      initialContext: messages,
      autoStart: true,
      lessonId: undefined,
      targetLanguage: 'en-GB',
    })))
    expect(mocks.apiFetch).toHaveBeenCalledWith('/api/study-plan/today')
  })
})
