import {
  act,
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import type { ReactNode } from 'react'

const mocks = vi.hoisted(() => ({
  apiFetch: vi.fn(),
  push: vi.fn(),
  params: 'lesson=7',
  voice: vi.fn(),
  moduleReady: true,
}))

vi.mock('next/navigation', () => ({
  useRouter: () => ({ push: mocks.push }),
  useSearchParams: () => new URLSearchParams(mocks.params),
}))
vi.mock('next-intl', async (importOriginal) => {
  const { createTranslator } =
    await importOriginal<typeof import('next-intl')>()
  const { default: messages } = await import('../../../messages/es.json')
  const practice = createTranslator({
    locale: 'es',
    messages,
    namespace: 'lessonPractice',
  })
  return {
    useLocale: () => 'es',
    useTranslations: (namespace: string) =>
      Object.assign((key: string) => `${namespace}.${key}`, {
        rich: practice.rich,
      }),
  }
})
vi.mock('next/dynamic', () => ({
  default: (_loader: unknown, options: { loading: () => ReactNode }) =>
    function Voice(props: Record<string, unknown>) {
      if (!mocks.moduleReady) {
        const Loading = options.loading
        return <Loading />
      }
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

function setVoiceQuota(remaining: number) {
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
      games_remaining: 3,
      games_limit: 3,
      voice_remaining_seconds: remaining,
      voice_limit_seconds: 300,
    },
  })
}

beforeEach(() => {
  vi.clearAllMocks()
  mocks.params = 'lesson=7'
  mocks.moduleReady = true
  mocks.apiFetch
    .mockReset()
    .mockImplementation((url: string) =>
      Promise.resolve(
        url === '/api/lessons/7' ? response(detail()) : response({}, 404)
      )
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
  useLanguageStore.setState({
    activeLanguage: getLanguageByCode('en-GB') ?? null,
    userLanguages: [],
  })
  useFreemiumStore.setState({ status: null, loaded: false })
})

afterEach(() => cleanup())

describe('Lesson practice entry', () => {
  it('opens a summary and navigates only after confirmation', () => {
    render(
      <LessonVoicePracticeButton
        lessonId={7}
        title="Raconter un voyage"
        targetLanguage="fr-FR"
      />
    )
    expect(screen.queryByRole('alertdialog')).toBeNull()
    fireEvent.click(
      screen.getByRole('button', { name: 'lessonPractice.action' })
    )
    expect(screen.getByRole('alertdialog')).toHaveAccessibleName(
      'Práctica: Raconter un voyage'
    )
    const topic = screen.getByText('Raconter un voyage')
    expect(topic).toHaveAttribute('lang', 'fr-FR')
    expect(topic.parentElement).toHaveAttribute('lang', 'es')
    expect(topic.parentElement).toHaveTextContent(
      'Práctica: Raconter un voyage'
    )
    expect(screen.getByText('lessonPractice.description')).toBeInTheDocument()
    expect(mocks.push).not.toHaveBeenCalled()
    expect(mocks.apiFetch).not.toHaveBeenCalled()
    fireEvent.click(
      screen.getByRole('button', { name: 'lessonPractice.cancel' })
    )
    expect(screen.queryByRole('alertdialog')).toBeNull()
    expect(mocks.push).not.toHaveBeenCalled()
    fireEvent.click(
      screen.getByRole('button', { name: 'lessonPractice.action' })
    )
    fireEvent.click(
      screen.getByRole('button', { name: 'lessonPractice.start' })
    )
    expect(mocks.push).toHaveBeenCalledExactlyOnceWith('/conversation?lesson=7')
  })

  it('uses the persisted lesson language and ignores unrelated chat and demo context', async () => {
    sessionStorage.setItem(
      'voice_context',
      JSON.stringify([{ role: 'user', content: 'Other chat' }])
    )
    sessionStorage.setItem(
      'assessment_voice_trial',
      JSON.stringify({ token: 'old-demo' })
    )
    render(<ConversationPage />)
    await screen.findByTestId('voice')
    expect(mocks.voice).toHaveBeenLastCalledWith(
      expect.objectContaining({
        lessonId: 7,
        lessonTitle: 'Raconter un voyage',
        targetLanguage: 'fr-FR',
        cefrLevel: 'B1',
        autoStart: true,
        initialContext: undefined,
      })
    )
    expect(mocks.voice.mock.lastCall?.[0].voiceTrialToken).toBeUndefined()
    expect(mocks.apiFetch.mock.calls.map(([url]) => url)).toEqual([
      '/api/lessons/7',
    ])
    act(() =>
      useLanguageStore.setState({
        activeLanguage: getLanguageByCode('de-DE') ?? null,
      })
    )
    expect(mocks.voice.mock.lastCall?.[0].targetLanguage).toBe('fr-FR')
    expect(mocks.voice.mock.lastCall?.[0].lessonId).toBe(7)
  })

  it.each([
    '',
    '0',
    '-1',
    'abc',
    '1.2',
    '2147483648',
    '9007199254740991',
    '9007199254740992',
    '9223372036854775808',
  ])(
    'rejects invalid lesson query %s without starting generic voice',
    async (id) => {
      mocks.params = `lesson=${id}`
      render(<ConversationPage />)
      await screen.findByRole('alert')
      expect(mocks.apiFetch).not.toHaveBeenCalled()
      expect(mocks.voice).not.toHaveBeenCalled()
    }
  )

  it('accepts the largest lesson ID supported by the database', async () => {
    mocks.params = 'lesson=2147483647'
    mocks.apiFetch.mockResolvedValue(response(detail({ id: 2147483647 })))
    render(<ConversationPage />)
    await screen.findByTestId('voice')
    expect(mocks.apiFetch).toHaveBeenCalledWith(
      '/api/lessons/2147483647',
      expect.any(Object)
    )
    expect(mocks.voice.mock.lastCall?.[0].lessonId).toBe(2147483647)
  })

  it.each([
    response({}, 404),
    response(detail({ is_completed: false })),
    response(detail({ id: 8 })),
    response({ lesson: detail().lesson }),
  ])(
    'does not fall back to a generic session when lesson context is unavailable',
    async (res) => {
      mocks.apiFetch.mockResolvedValue(res)
      render(<ConversationPage />)
      await screen.findByRole('alert')
      expect(mocks.voice).not.toHaveBeenCalled()
    }
  )

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
    mocks.apiFetch.mockReturnValue(
      new Promise<Response>((done) => {
        resolve = done
      })
    )
    const view = render(<ConversationPage />)
    const signal = mocks.apiFetch.mock.calls[0][1].signal as AbortSignal
    view.unmount()
    expect(signal.aborted).toBe(true)
    await act(async () => {
      resolve(response(detail()))
    })
    expect(mocks.voice).not.toHaveBeenCalled()
  })

  it('keeps the existing voice paywall when the free quota is exhausted', async () => {
    useConfigStore.setState({ stripeEnabled: true })
    setVoiceQuota(0)
    render(<ConversationPage />)
    await screen.findByTestId('paywall')
    expect(mocks.voice).not.toHaveBeenCalled()
  })

  it.each(['ordinary', 'lesson', 'demo'] as const)(
    'uses refreshed voice balance for %s without discarding the independent demo credential',
    async (mode) => {
      mocks.params = mode === 'lesson' ? 'lesson=7' : ''
      useConfigStore.setState({ stripeEnabled: true })
      setVoiceQuota(120)
      if (mode === 'demo') {
        sessionStorage.setItem(
          'assessment_voice_trial',
          JSON.stringify({ token: 'demo-token' })
        )
      }
      render(<ConversationPage />)
      await screen.findByTestId('voice')
      act(() => setVoiceQuota(0))
      if (mode === 'demo') {
        expect(screen.getByTestId('voice')).toBeInTheDocument()
        expect(screen.queryByTestId('paywall')).toBeNull()
        expect(mocks.voice.mock.lastCall?.[0].voiceTrialToken).toBe('demo-token')
      } else {
        expect(screen.getByTestId('paywall')).toBeInTheDocument()
        expect(screen.queryByTestId('voice')).toBeNull()
      }
      expect(
        mocks.apiFetch.mock.calls.filter(
          ([url]) => url === '/api/freemium/status'
        )
      ).toHaveLength(1)
    }
  )

  it('discards lesson metadata from a replaced authentication session', async () => {
    let oldBody!: (value: unknown) => void
    mocks.apiFetch
      .mockResolvedValueOnce({
        ok: true,
        json: () =>
          new Promise((resolve) => {
            oldBody = resolve
          }),
      })
      .mockResolvedValueOnce(response({}, 404))
    render(<ConversationPage />)
    await act(async () => Promise.resolve())
    const signal = mocks.apiFetch.mock.calls[0][1].signal as AbortSignal
    act(() => useAuthStore.getState().startSession('new-session'))
    await screen.findByRole('alert')
    expect(signal.aborted).toBe(true)
    await act(async () => oldBody(detail()))
    expect(mocks.voice).not.toHaveBeenCalled()
    expect(screen.getByRole('alert')).toBeInTheDocument()
  })

  it.each([
    [false, 'expiry'],
    [true, 'expiry'],
    [false, 'toggle'],
    [true, 'toggle'],
  ] as const)(
    'preserves admitted voice sessions (active: %s) when trial access changes by %s',
    async (active, boundary) => {
      vi.useFakeTimers()
      try {
        useConfigStore.setState({
          stripeEnabled: true,
          freemiumTrialEnabled: true,
        })
        useAuthStore.setState({
          user: {
            ...useAuthStore.getState().user!,
            freemium_trial_ends_at: new Date(Date.now() + 1000).toISOString(),
          },
        })
        setVoiceQuota(0)
        await act(async () => {
          render(<ConversationPage />)
        })
        expect(screen.getByTestId('voice')).toBeInTheDocument()
        if (active) {
          act(() => mocks.voice.mock.lastCall?.[0].onSessionActiveChange(true))
        }
        if (boundary === 'expiry') {
          await act(async () => vi.advanceTimersByTimeAsync(1000))
        } else {
          act(() => useConfigStore.setState({ freemiumTrialEnabled: false }))
        }
        if (active) {
          expect(screen.getByTestId('voice')).toBeInTheDocument()
          expect(screen.queryByTestId('paywall')).toBeNull()
          act(() =>
            mocks.voice.mock.lastCall?.[0].onSessionActiveChange(false)
          )
          expect(screen.getByTestId('voice')).toBeInTheDocument()
          expect(screen.queryByTestId('paywall')).toBeNull()
        } else {
          expect(screen.getByTestId('paywall')).toBeInTheDocument()
          expect(screen.queryByTestId('voice')).toBeNull()
        }
      } finally {
        vi.useRealTimers()
      }
    }
  )

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
    await waitFor(() =>
      expect(mocks.voice).toHaveBeenLastCalledWith(
        expect.objectContaining({
          initialContext: messages,
          autoStart: true,
          lessonId: undefined,
          targetLanguage: 'en-GB',
        })
      )
    )
    expect(mocks.apiFetch).toHaveBeenCalledWith(
      '/api/study-plan/today',
      expect.objectContaining({ signal: expect.any(AbortSignal) })
    )
  })
})

describe('Ordinary conversation loading', () => {
  it('reloads ordinary voice context when the plan changes in the same language', async () => {
    mocks.params = ''
    mocks.apiFetch
      .mockResolvedValueOnce(response({ cefr_level: 'A1' }))
      .mockResolvedValueOnce(response({ cefr_level: 'B2' }))
    render(<ConversationPage />)
    await screen.findByTestId('voice')
    expect(mocks.voice.mock.lastCall?.[0].cefrLevel).toBe('A1')
    act(() =>
      useLanguageStore.setState({
        userLanguages: [
          {
            target_language: 'en-GB',
            is_active: true,
            progress: null,
            plan: {
              id: 99,
              cefr_level: 'B2',
              progress_day: 1,
              total_days: 30,
              completion_pct: 0,
            },
          },
        ],
      })
    )
    expect(screen.queryByTestId('voice')).toBeNull()
    await screen.findByTestId('voice')
    expect(mocks.voice.mock.lastCall?.[0].cefrLevel).toBe('B2')
    expect(mocks.apiFetch).toHaveBeenCalledTimes(2)
  })

  it('hands shared loading from the plan lookup to the dynamic voice module', async () => {
    mocks.params = ''
    mocks.moduleReady = false
    const view = render(<ConversationPage />)
    expect(screen.getByTestId('loading')).toBeInTheDocument()
    await act(async () => {
      await Promise.resolve()
    })
    expect(screen.getByTestId('loading')).toBeInTheDocument()
    expect(mocks.voice).not.toHaveBeenCalled()
    mocks.moduleReady = true
    view.rerender(<ConversationPage />)
    expect(screen.getByTestId('voice')).toBeInTheDocument()
    expect(screen.queryByTestId('loading')).toBeNull()
  })

  it('shows shared loading until the plan resolves and rejects obsolete language responses', async () => {
    mocks.params = ''
    let oldBody!: (value: unknown) => void
    let currentResponse!: (value: Response) => void
    mocks.apiFetch
      .mockResolvedValueOnce({
        ok: true,
        json: () =>
          new Promise((resolve) => {
            oldBody = resolve
          }),
      })
      .mockReturnValueOnce(
        new Promise<Response>((resolve) => {
          currentResponse = resolve
        })
      )
    render(<ConversationPage />)
    expect(screen.getByTestId('loading')).toBeInTheDocument()
    expect(mocks.voice).not.toHaveBeenCalled()
    await act(async () => {
      await Promise.resolve()
    })
    const oldSignal = mocks.apiFetch.mock.calls[0][1].signal as AbortSignal
    act(() =>
      useLanguageStore.setState({
        activeLanguage: getLanguageByCode('de-DE') ?? null,
      })
    )
    expect(oldSignal.aborted).toBe(true)
    await act(async () => {
      oldBody({ cefr_level: 'C2' })
    })
    expect(screen.getByTestId('loading')).toBeInTheDocument()
    expect(mocks.voice).not.toHaveBeenCalled()
    await act(async () => {
      currentResponse(response({ cefr_level: 'A1' }))
    })
    expect(mocks.voice).toHaveBeenLastCalledWith(
      expect.objectContaining({ targetLanguage: 'de-DE', cefrLevel: 'A1' })
    )
  })

  it('retains planless entry after a failed lookup without reusing the previous language level', async () => {
    mocks.params = ''
    mocks.apiFetch
      .mockResolvedValueOnce(response({ cefr_level: 'C1' }))
      .mockRejectedValueOnce(new Error('no plan'))
    render(<ConversationPage />)
    await screen.findByTestId('voice')
    act(() =>
      useLanguageStore.setState({
        activeLanguage: getLanguageByCode('de-DE') ?? null,
      })
    )
    await screen.findByTestId('voice')
    expect(mocks.voice).toHaveBeenLastCalledWith(
      expect.objectContaining({ targetLanguage: 'de-DE', cefrLevel: null })
    )
  })

  it('does not impose a read-only timeout on today, and aborts on unmount', async () => {
    vi.useFakeTimers()
    try {
      mocks.params = ''
      let resolve!: (value: Response) => void
      mocks.apiFetch.mockReturnValueOnce(
        new Promise<Response>((done) => {
          resolve = done
        })
      )
      const view = render(<ConversationPage />)
      const signal = mocks.apiFetch.mock.calls[0][1].signal as AbortSignal
      await act(async () => {
        vi.advanceTimersByTime(60_000)
      })
      expect(signal.aborted).toBe(false)
      expect(screen.getByTestId('loading')).toBeInTheDocument()
      view.unmount()
      expect(signal.aborted).toBe(true)
      await act(async () => {
        resolve(response({ cefr_level: 'A2' }))
      })
      expect(mocks.voice).not.toHaveBeenCalled()
    } finally {
      vi.useRealTimers()
    }
  })

  it('preserves the assessment trial context after plan loading', async () => {
    mocks.params = ''
    sessionStorage.setItem(
      'assessment_voice_trial',
      JSON.stringify({
        token: 'trial-token',
        durationSeconds: 120,
        cefrLevel: 'B1',
        targetLanguage: 'fr-FR',
      })
    )
    render(<ConversationPage />)
    await screen.findByTestId('voice')
    expect(mocks.voice).toHaveBeenLastCalledWith(
      expect.objectContaining({
        trialMode: true,
        voiceTrialToken: 'trial-token',
        voiceTrialDurationSeconds: 120,
        autoStart: true,
        cefrLevel: 'B1',
        targetLanguage: 'fr-FR',
      })
    )
  })
})
