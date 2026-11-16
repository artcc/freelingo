import {
  act,
  fireEvent,
  render,
  screen,
  waitFor,
  within,
} from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { PracticeCatalog } from '@/components/grammar-practice/PracticeCatalog'
import { PracticeSession } from '@/components/grammar-practice/PracticeSession'
import { AddPracticeButton } from '@/components/grammar-practice/AddPracticeButton'
import { PracticeVoiceButton } from '@/components/grammar-practice/PracticeVoiceButton'
import { apiFetch } from '@/lib/api'
import {
  practiceRequest,
  PracticeRequestError,
  pendingPracticeKey,
  readPendingPractice,
  type PendingPractice,
  type PracticeHistory,
  type PracticeSession as Session,
} from '@/lib/grammar-practice'
import { useAuthStore } from '@/store/auth'
import { useLanguageStore } from '@/store/language'
import { useFreemiumStore } from '@/store/freemium'
import { useConfigStore } from '@/store/config'
import { getLanguageByCode } from '@/lib/target-languages'

const { push } = vi.hoisted(() => ({ push: vi.fn() }))
vi.mock('next/navigation', () => ({ useRouter: () => ({ push }) }))
vi.mock('next-intl', () => {
  const translate = Object.assign(
    (key: string, values?: Record<string, unknown>) =>
      values ? `${key}:${JSON.stringify(values)}` : key,
    { rich: (key: string) => key }
  )
  return { useTranslations: () => translate, useLocale: () => 'en' }
})
vi.mock('@/lib/api', () => ({ apiFetch: vi.fn() }))
vi.mock('@/lib/grammar-practice', async (original) => ({
  ...(await original<typeof import('@/lib/grammar-practice')>()),
  practiceRequest: vi.fn(),
}))
vi.mock('@/components/billing/FreemiumQuotaBanner', () => ({
  FreemiumQuotaBanner: () => null,
}))
vi.mock('@/components/billing/PaywallBanner', () => ({
  PaywallBanner: () => <div>paywall</div>,
}))

const id = 'c08ae315-59fb-41f6-b516-78206d09bbab'
const initial: Session = {
  id,
  topic_id: 7,
  title: 'Present simple',
  study_plan_id: 4,
  target_language: 'en-GB',
  native_language: 'es',
  topic_level: 'A1',
  learner_level: 'A2',
  status: 'ready',
  error: null,
  created_at: '2026-11-16T12:00:00Z',
  completed_at: null,
  remaining_seconds: null,
  answered: 0,
  correct: 0,
  challenges: [
    {
      index: 0,
      type: 'multiple_choice',
      question: 'She ___ home.',
      options: ['go', 'goes', 'going', 'gone'],
    },
    { index: 1, type: 'fill_blank', question: 'I ___ tea.' },
    {
      index: 2,
      type: 'multiple_choice',
      question: 'They ___ English.',
      options: ['study', 'studies', 'studying', 'studied'],
    },
    {
      index: 3,
      type: 'multiple_choice',
      question: 'He ___ coffee.',
      options: ['like', 'liking', 'likes', 'liked'],
    },
    { index: 4, type: 'fill_blank', question: 'We ___ tennis.' },
  ],
}
const history: PracticeHistory = {
  study_plan_id: 4,
  target_language: 'en-GB',
  quota: { remaining: 3, limit: 3 },
  limited: true,
  topic: {
    id: 7,
    slug: 'present-simple',
    title: 'Present simple',
    level: 'A1',
    answered: 10,
    correct: 8,
    completed_sessions: 2,
    last_practiced: '2026-11-16T12:00:00Z',
    active_session_id: null,
  },
  sessions: [initial],
  total: 11,
}

function deferred<T>() {
  let resolve!: (value: T) => void
  let reject!: (error: Error) => void
  const promise = new Promise<T>((res, rej) => {
    resolve = res
    reject = rej
  })
  return { promise, resolve, reject }
}

const fetchLanguages = useLanguageStore.getState().fetchLanguages

beforeEach(() => {
  vi.clearAllMocks()
  vi.mocked(practiceRequest).mockReset()
  vi.mocked(apiFetch).mockReset()
  sessionStorage.clear()
  useAuthStore.setState({ sessionVersion: 1 })
  useLanguageStore.setState({
    activeLanguage: getLanguageByCode('en-GB'),
    needsRefresh: false,
    isSwitching: false,
    invalidationVersion: 0,
    userLanguages: [],
    fetchLanguages,
  })
  useFreemiumStore.setState({
    status: null,
    loaded: false,
    lastFetch: 0,
    fetchStatus: vi.fn().mockResolvedValue(undefined),
  })
  useConfigStore.setState({ stripeEnabled: true })
})
afterEach(() => vi.useRealTimers())

describe('grammar library and captured resource context', () => {
  it.each(['study_context_changed', 'language_not_found', 'response_language'])(
    'reconciles a stale library read on explicit retry (%s) without generating',
    async (failure) => {
      const library = {
        study_plan_id: 9,
        target_language: 'ja-JP',
        quota: history.quota,
        limited: true,
        topics: [{ ...history.topic, title: 'Japanese topic' }],
        total: 1,
      }
      if (failure === 'response_language') {
        vi.mocked(practiceRequest).mockResolvedValueOnce(library)
      } else {
        vi.mocked(practiceRequest).mockRejectedValueOnce(
          new PracticeRequestError(
            failure === 'language_not_found' ? 404 : 409,
            failure
          )
        )
      }
      vi.mocked(practiceRequest).mockResolvedValue(library)
      vi.mocked(apiFetch).mockImplementation(
        async () =>
          new Response(
            JSON.stringify({
              languages: [
                { target_language: 'en-GB', is_active: false, plan: null },
                {
                  target_language: 'ja-JP',
                  is_active: true,
                  plan: { id: 9, cefr_level: 'A1' },
                },
              ],
            })
          )
      )
      render(<PracticeCatalog />)
      expect(await screen.findByRole('alert')).toHaveTextContent(
        'contextChanged'
      )
      expect(apiFetch).not.toHaveBeenCalled()
      expect(screen.queryByText('Japanese topic')).not.toBeInTheDocument()

      fireEvent.click(screen.getByRole('button', { name: 'retry' }))
      expect(await screen.findByText('Japanese topic')).toBeVisible()
      expect(apiFetch).toHaveBeenCalledWith('/api/languages', expect.anything())
      expect(useLanguageStore.getState().activeLanguage?.code).toBe('ja-JP')
      expect(
        vi.mocked(practiceRequest).mock.calls.map(([path]) => path)
      ).toEqual([
        '/topics?target_language=en-GB&skip=0&limit=20',
        '/topics?target_language=ja-JP&skip=0&limit=20',
      ])
      expect(
        vi
          .mocked(practiceRequest)
          .mock.calls.every(([, options]) => !options?.method)
      ).toBe(true)
    }
  )

  it.each([false, true])(
    'reconciles a current-plan language mismatch before allowing an explicit add (refresh failure: %s)',
    async (refreshFails) => {
      let languageReads = 0
      vi.mocked(apiFetch).mockImplementation(async (path) => {
        if (path === '/api/languages') {
          languageReads += 1
          if (refreshFails && languageReads === 1)
            return new Response('{}', { status: 503 })
          return new Response(
            JSON.stringify({
              languages: [
                {
                  target_language: 'ja-JP',
                  is_active: true,
                  plan: { id: 9, cefr_level: 'A1' },
                },
              ],
            })
          )
        }
        return new Response(JSON.stringify({ id: 9, target_language: 'ja-JP' }))
      })
      vi.mocked(practiceRequest).mockResolvedValue(history.topic)
      function Resource() {
        const language = useLanguageStore((state) => state.activeLanguage?.code)
        return (
          <AddPracticeButton slug="present-simple" targetLanguage={language!} />
        )
      }
      render(<Resource />)
      expect(await screen.findByRole('alert')).toHaveTextContent(
        'contextChanged'
      )
      expect(screen.getByRole('button', { name: 'add' })).toBeDisabled()
      expect(languageReads).toBe(0)
      fireEvent.click(screen.getByRole('button', { name: 'retry' }))
      if (refreshFails) {
        expect(await screen.findByRole('alert')).toHaveTextContent(
          'errorMessage'
        )
        expect(practiceRequest).not.toHaveBeenCalled()
        fireEvent.click(screen.getByRole('button', { name: 'retry' }))
      }
      await waitFor(() =>
        expect(screen.getByRole('button', { name: 'add' })).toBeEnabled()
      )
      expect(useLanguageStore.getState().activeLanguage?.code).toBe('ja-JP')
      expect(languageReads).toBe(refreshFails ? 2 : 1)
      expect(practiceRequest).not.toHaveBeenCalled()
      fireEvent.click(screen.getByRole('button', { name: 'add' }))
      await waitFor(() => expect(push).toHaveBeenCalled())
      expect(
        JSON.parse(String(vi.mocked(practiceRequest).mock.calls[0][1]?.body))
      ).toEqual({
        slug: 'present-simple',
        study_plan_id: 9,
        target_language: 'ja-JP',
      })
    }
  )

  it('retries an unrelated library error without invalidating the language context', async () => {
    vi.mocked(practiceRequest)
      .mockRejectedValueOnce(new PracticeRequestError(503, 'unavailable'))
      .mockResolvedValueOnce({
        study_plan_id: 4,
        target_language: 'en-GB',
        quota: history.quota,
        limited: true,
        topics: [history.topic],
        total: 1,
      })
    render(<PracticeCatalog />)
    expect(await screen.findByRole('alert')).toHaveTextContent('errorMessage')
    fireEvent.click(screen.getByRole('button', { name: 'retry' }))
    expect(await screen.findByText('Present simple')).toBeVisible()
    expect(apiFetch).not.toHaveBeenCalled()
    expect(useLanguageStore.getState().needsRefresh).toBe(false)
  })

  it('reconciles a cross-tab language change before allowing an explicit add in the new resource context', async () => {
    let changedInOtherTab = false
    vi.mocked(apiFetch).mockImplementation(
      async (path) =>
        new Response(
          JSON.stringify(
            path === '/api/languages'
              ? {
                  languages: [
                    {
                      target_language: 'ja-JP',
                      is_active: true,
                      plan: { id: 9, cefr_level: 'A1' },
                    },
                  ],
                }
              : {
                  id: changedInOtherTab ? 9 : 4,
                  target_language: changedInOtherTab ? 'ja-JP' : 'en-GB',
                }
          )
        )
    )
    vi.mocked(practiceRequest)
      .mockRejectedValueOnce(
        new PracticeRequestError(409, 'study_context_changed')
      )
      .mockResolvedValueOnce(history.topic)
    function Resource() {
      const language = useLanguageStore((state) => state.activeLanguage?.code)
      return (
        <AddPracticeButton slug="present-simple" targetLanguage={language!} />
      )
    }
    render(<Resource />)
    await waitFor(() =>
      expect(screen.getByRole('button', { name: 'add' })).toBeEnabled()
    )
    changedInOtherTab = true
    fireEvent.click(screen.getByRole('button', { name: 'add' }))
    await screen.findByRole('alert')
    fireEvent.click(screen.getByRole('button', { name: 'retry' }))
    await waitFor(() =>
      expect(useLanguageStore.getState().activeLanguage?.code).toBe('ja-JP')
    )
    await waitFor(() =>
      expect(screen.getByRole('button', { name: 'add' })).toBeEnabled()
    )
    expect(apiFetch).toHaveBeenCalledWith('/api/languages', expect.anything())
    expect(practiceRequest).toHaveBeenCalledTimes(1)
    fireEvent.click(screen.getByRole('button', { name: 'add' }))
    await waitFor(() => expect(push).toHaveBeenCalled())
    expect(
      JSON.parse(String(vi.mocked(practiceRequest).mock.calls[1][1]?.body))
    ).toEqual({
      slug: 'present-simple',
      study_plan_id: 9,
      target_language: 'ja-JP',
    })
  })

  it('reconciles a confirmed midnight quota refill after an initially exhausted GET without a 402', async () => {
    const quota = {
      trial_active: false,
      trial_ends_at: null,
      chat_remaining: 1,
      chat_limit: 1,
      lessons_remaining: 1,
      lessons_limit: 1,
      listening_remaining: 1,
      listening_limit: 1,
      reading_remaining: 1,
      reading_limit: 1,
      games_remaining: 3,
      games_limit: 3,
      voice_remaining_seconds: 60,
      voice_limit_seconds: 60,
      grammar_practice_remaining: 0,
      grammar_practice_limit: 3,
    }
    useFreemiumStore.setState({
      status: quota,
      lastFetch: Date.UTC(2026, 10, 16, 23, 59),
    })
    vi.mocked(practiceRequest)
      .mockResolvedValueOnce({ ...history, quota: { remaining: 0, limit: 3 } })
      .mockResolvedValue(history)
    render(<PracticeCatalog topicId="7" />)
    expect(await screen.findByText('paywall')).toBeVisible()
    expect(screen.getByRole('button', { name: 'generate' })).toBeDisabled()
    act(() =>
      useFreemiumStore.setState({
        status: { ...quota, grammar_practice_remaining: 3 },
        lastFetch: Date.UTC(2026, 10, 17),
      })
    )
    await waitFor(() =>
      expect(screen.getByRole('button', { name: 'generate' })).toBeEnabled()
    )
    expect(screen.queryByText('paywall')).not.toBeInTheDocument()
    expect(practiceRequest).toHaveBeenCalledTimes(2)
    act(() =>
      useFreemiumStore.setState({
        status: { ...quota, grammar_practice_remaining: 3 },
        lastFetch: Date.UTC(2026, 10, 17, 0, 1),
      })
    )
    expect(practiceRequest).toHaveBeenCalledTimes(2)
  })

  it('captures the plan before the click and opens an idempotently returned existing topic', async () => {
    vi.mocked(apiFetch).mockResolvedValue(
      new Response(JSON.stringify({ id: 4, target_language: 'en-GB' }))
    )
    vi.mocked(practiceRequest).mockResolvedValue(history.topic)
    render(<AddPracticeButton slug="present-simple" targetLanguage="en-GB" />)
    expect(screen.getByRole('button', { name: 'add' })).toBeDisabled()
    await waitFor(() =>
      expect(screen.getByRole('button', { name: 'add' })).toBeEnabled()
    )
    expect(apiFetch).toHaveBeenCalledTimes(1)
    fireEvent.click(screen.getByRole('button', { name: 'add' }))
    await waitFor(() =>
      expect(push).toHaveBeenCalledWith('/grammar-practice/7')
    )
    expect(apiFetch).toHaveBeenCalledTimes(1)
    expect(
      JSON.parse(String(vi.mocked(practiceRequest).mock.calls[0][1]?.body))
    ).toEqual({
      slug: 'present-simple',
      study_plan_id: 4,
      target_language: 'en-GB',
    })
  })

  it('requires refresh and a separate click after a same-language plan conflict', async () => {
    const reconcile = vi.fn(async () => {
      useLanguageStore.setState({ needsRefresh: false })
      return true
    })
    useLanguageStore.setState({ fetchLanguages: reconcile })
    vi.mocked(apiFetch)
      .mockResolvedValueOnce(
        new Response(JSON.stringify({ id: 4, target_language: 'en-GB' }))
      )
      .mockResolvedValueOnce(
        new Response(JSON.stringify({ id: 9, target_language: 'en-GB' }))
      )
    vi.mocked(practiceRequest)
      .mockRejectedValueOnce(
        new PracticeRequestError(409, 'study_context_changed')
      )
      .mockResolvedValueOnce(history.topic)
    render(<AddPracticeButton slug="present-simple" targetLanguage="en-GB" />)
    await waitFor(() =>
      expect(screen.getByRole('button', { name: 'add' })).toBeEnabled()
    )
    fireEvent.click(screen.getByRole('button', { name: 'add' }))
    expect(await screen.findByRole('alert')).toHaveTextContent('contextChanged')
    expect(screen.getByRole('button', { name: 'add' })).toBeDisabled()
    fireEvent.click(screen.getByRole('button', { name: 'retry' }))
    await waitFor(() =>
      expect(screen.getByRole('button', { name: 'add' })).toBeEnabled()
    )
    expect(reconcile).toHaveBeenCalledTimes(1)
    expect(practiceRequest).toHaveBeenCalledTimes(1)
    fireEvent.click(screen.getByRole('button', { name: 'add' }))
    await waitFor(() => expect(push).toHaveBeenCalled())
    expect(
      JSON.parse(String(vi.mocked(practiceRequest).mock.calls[1][1]?.body))
        .study_plan_id
    ).toBe(9)
  })

  it('keeps theory readable without a plan and prevents adding', async () => {
    vi.mocked(apiFetch).mockResolvedValue(new Response('null'))
    render(<AddPracticeButton slug="present-simple" targetLanguage="en-GB" />)
    expect(await screen.findByText('noPlan')).toBeVisible()
    expect(screen.getByRole('button', { name: 'add' })).toBeDisabled()
    expect(practiceRequest).not.toHaveBeenCalled()
  })

  it('discards a resource add callback after authentication changes', async () => {
    vi.mocked(apiFetch).mockImplementation(
      async () =>
        new Response(JSON.stringify({ id: 4, target_language: 'en-GB' }))
    )
    const pending = deferred<typeof history.topic>()
    vi.mocked(practiceRequest).mockReturnValue(pending.promise)
    render(<AddPracticeButton slug="present-simple" targetLanguage="en-GB" />)
    await waitFor(() =>
      expect(screen.getByRole('button', { name: 'add' })).toBeEnabled()
    )
    fireEvent.click(screen.getByRole('button', { name: 'add' }))
    await act(async () => {
      useAuthStore.setState({ sessionVersion: 2 })
      pending.resolve(history.topic)
    })
    expect(push).not.toHaveBeenCalled()
  })

  it('shows library statistics, pagination and resource discovery without generating', async () => {
    vi.mocked(practiceRequest).mockResolvedValue({
      study_plan_id: 4,
      target_language: 'en-GB',
      quota: history.quota,
      limited: true,
      topics: [history.topic],
      total: 21,
    })
    render(<PracticeCatalog />)
    expect(
      await screen.findByText('answered:{"count":10}', { exact: false })
    ).toBeVisible()
    expect(
      screen.getByText('accuracy:{"percent":80}', { exact: false })
    ).toBeVisible()
    expect(screen.getByText('2026-11-16')).toBeVisible()
    expect(screen.getByRole('link', { name: 'explore' })).toHaveAttribute(
      'href',
      '/grammar'
    )
    fireEvent.click(screen.getByRole('button', { name: 'next' }))
    await waitFor(() =>
      expect(practiceRequest).toHaveBeenCalledWith(
        '/topics?target_language=en-GB&skip=20&limit=20',
        expect.anything()
      )
    )
    expect(
      vi
        .mocked(practiceRequest)
        .mock.calls.every(([, options]) => !options?.method)
    ).toBe(true)
  })

  it('shows the shared no-plan state for an empty library and opens assessment', async () => {
    vi.mocked(practiceRequest).mockResolvedValue({
      study_plan_id: null,
      target_language: 'en-GB',
      quota: history.quota,
      limited: true,
      topics: [],
      total: 0,
    })
    render(<PracticeCatalog />)
    expect(
      await screen.findByRole('heading', { name: 'noPlanTitle' })
    ).toBeVisible()
    fireEvent.click(screen.getByRole('button', { name: 'startAssessment' }))
    expect(push).toHaveBeenCalledWith('/assessment')
    expect(screen.queryByText('empty')).not.toBeInTheDocument()
  })

  it('keeps saved library topics accessible without a plan', async () => {
    vi.mocked(practiceRequest).mockResolvedValue({
      study_plan_id: null,
      target_language: 'en-GB',
      quota: history.quota,
      limited: true,
      topics: [history.topic],
      total: 1,
    })
    render(<PracticeCatalog />)
    expect(
      await screen.findByRole('link', { name: /Present simple/ })
    ).toHaveAttribute('href', '/grammar-practice/7')
    expect(screen.getByRole('link', { name: 'assessment' })).toHaveAttribute(
      'href',
      '/assessment'
    )
    expect(
      screen.queryByRole('heading', { name: 'noPlanTitle' })
    ).not.toBeInTheDocument()
  })

  it('offers grammar resources when the library is empty but a plan exists', async () => {
    vi.mocked(practiceRequest).mockResolvedValue({
      study_plan_id: 4,
      target_language: 'en-GB',
      quota: history.quota,
      limited: true,
      topics: [],
      total: 0,
    })
    render(<PracticeCatalog />)
    expect(await screen.findByText('empty')).toBeVisible()
    expect(screen.getByRole('link', { name: 'explore' })).toHaveAttribute(
      'href',
      '/grammar'
    )
    expect(
      screen.queryByRole('heading', { name: 'noPlanTitle' })
    ).not.toBeInTheDocument()
  })

  it('keeps history and saved sessions usable with no plan and exhausted quota', async () => {
    vi.mocked(practiceRequest).mockResolvedValue({
      ...history,
      study_plan_id: null,
      quota: { remaining: 0, limit: 3 },
    })
    render(<PracticeCatalog topicId="7" />)
    expect(await screen.findByText('paywall')).toBeVisible()
    expect(screen.getByRole('button', { name: 'generate' })).toBeDisabled()
    expect(screen.getByRole('link', { name: /ready/ })).toHaveAttribute(
      'href',
      `/grammar-practice/sessions/${id}`
    )
    fireEvent.click(screen.getByRole('button', { name: 'next' }))
    await waitFor(() =>
      expect(practiceRequest).toHaveBeenCalledWith(
        '/topics/7?skip=10&limit=10',
        expect.anything()
      )
    )
  })

  it('does not open theory or generate in another active language while retaining saved sessions', async () => {
    useLanguageStore.setState({ activeLanguage: getLanguageByCode('ja-JP') })
    vi.mocked(practiceRequest).mockResolvedValue(history)
    render(<PracticeCatalog topicId="7" />)
    expect(await screen.findByRole('button', { name: 'theory' })).toBeDisabled()
    expect(
      screen.queryByRole('link', { name: 'theory' })
    ).not.toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'generate' })).toBeDisabled()
    expect(screen.getByRole('link', { name: /ready/ })).toHaveAttribute(
      'href',
      `/grammar-practice/sessions/${id}`
    )
  })

  it('discards plan lookup results invalidated within the same language', async () => {
    const stale = deferred<Response>()
    vi.mocked(apiFetch)
      .mockReturnValueOnce(stale.promise)
      .mockResolvedValueOnce(
        new Response(JSON.stringify({ id: 9, target_language: 'en-GB' }))
      )
    vi.mocked(practiceRequest).mockResolvedValue(history.topic)
    render(<AddPracticeButton slug="present-simple" targetLanguage="en-GB" />)
    await act(async () => {
      useLanguageStore.setState({ invalidationVersion: 1 })
      stale.resolve(
        new Response(JSON.stringify({ id: 4, target_language: 'en-GB' }))
      )
    })
    await waitFor(() =>
      expect(screen.getByRole('button', { name: 'add' })).toBeEnabled()
    )
    fireEvent.click(screen.getByRole('button', { name: 'add' }))
    await waitFor(() => expect(push).toHaveBeenCalled())
    expect(
      JSON.parse(String(vi.mocked(practiceRequest).mock.calls[0][1]?.body))
        .study_plan_id
    ).toBe(9)
  })
})

describe('grammar creation recovery', () => {
  it.each(['maintenance', 'network'])(
    'recovers an unaccepted %s request with the same stored payload after explicit retry',
    async (failure) => {
      vi.mocked(practiceRequest)
        .mockResolvedValueOnce(history)
        .mockRejectedValueOnce(
          failure === 'maintenance'
            ? new PracticeRequestError(503, 'maintenance')
            : new Error('offline')
        )
      const view = render(<PracticeCatalog topicId="7" />)
      fireEvent.click(await screen.findByRole('button', { name: 'generate' }))
      await waitFor(() => expect(push).toHaveBeenCalled())
      const original = readPendingPractice(7)!
      expect(original.payload.study_plan_id).toBe(4)
      view.unmount()
      vi.mocked(practiceRequest).mockRejectedValueOnce(
        new PracticeRequestError(404, 'not_found')
      )
      const sessionView = render(
        <PracticeSession sessionId={original.payload.request_id} />
      )
      expect(
        await screen.findByRole('link', { name: 'retryCreation' })
      ).toHaveAttribute('href', '/grammar-practice/7')
      expect(
        vi
          .mocked(practiceRequest)
          .mock.calls.filter(([, options]) => options?.method === 'POST')
      ).toHaveLength(1)
      sessionView.unmount()
      // A later plan change must not rewrite the uncertain request's captured context.
      vi.mocked(practiceRequest)
        .mockResolvedValueOnce({ ...history, study_plan_id: 99 })
        .mockRejectedValueOnce(new PracticeRequestError(404, 'not_found'))
        .mockResolvedValueOnce({ ...initial, id: original.payload.request_id })
      render(<PracticeCatalog topicId="7" />)
      await screen.findByRole('button', { name: 'retryCreation' })
      expect(
        vi
          .mocked(practiceRequest)
          .mock.calls.filter(([, options]) => options?.method === 'POST')
      ).toHaveLength(1)
      fireEvent.click(screen.getByRole('button', { name: 'retryCreation' }))
      await waitFor(() => expect(readPendingPractice(7)).toBeNull())
      const submissions = vi
        .mocked(practiceRequest)
        .mock.calls.filter(([, options]) => options?.method === 'POST')
      expect(submissions).toHaveLength(2)
      expect(submissions[1][0]).toBe('/topics/7/sessions')
      expect(submissions[1][1]?.body).toBe(submissions[0][1]?.body)
    }
  )

  it.each(['request_conflict', 'study_context_changed'])(
    'retires a definitively rejected recovery marker: %s',
    async (code) => {
      vi.mocked(apiFetch).mockResolvedValue(
        new Response(
          JSON.stringify({
            languages: [
              {
                target_language: 'en-GB',
                is_active: true,
                plan: { id: 4, cefr_level: 'A2' },
              },
            ],
          })
        )
      )
      const pending: PendingPractice = {
        topic_id: 7,
        payload: { request_id: id, study_plan_id: 4, target_language: 'en-GB' },
      }
      sessionStorage.setItem(pendingPracticeKey(7), JSON.stringify(pending))
      vi.mocked(practiceRequest)
        .mockResolvedValueOnce(history)
        .mockRejectedValueOnce(new PracticeRequestError(404, 'not_found'))
        .mockRejectedValueOnce(new PracticeRequestError(409, code))
        .mockResolvedValueOnce(history)
      render(<PracticeCatalog topicId="7" />)
      fireEvent.click(
        await screen.findByRole('button', { name: 'retryCreation' })
      )
      await waitFor(() => expect(readPendingPractice(7)).toBeNull())
      expect(await screen.findByRole('alert')).toHaveTextContent(
        'contextChanged'
      )
      expect(screen.getByRole('button', { name: 'generate' })).toBeDisabled()
      fireEvent.click(screen.getByRole('button', { name: 'retry' }))
      await waitFor(() =>
        expect(screen.getByRole('button', { name: 'generate' })).toBeEnabled()
      )
      expect(
        vi
          .mocked(practiceRequest)
          .mock.calls.filter(([, options]) => options?.method === 'POST')
      ).toHaveLength(1)
      expect(apiFetch).toHaveBeenCalledTimes(
        code === 'study_context_changed' ? 1 : 0
      )
    }
  )

  it.each(['success', 'refresh_failure', 'no_active_language'])(
    'reconciles a generation conflict while preserving the saved topic (%s)',
    async (scenario) => {
      let changed = false
      let languageReads = 0
      vi.mocked(practiceRequest).mockImplementation(async (_path, options) => {
        if (options?.method === 'POST') {
          changed = true
          throw new PracticeRequestError(409, 'study_context_changed')
        }
        return { ...history, study_plan_id: changed ? null : 4 }
      })
      vi.mocked(apiFetch).mockImplementation(async () => {
        languageReads += 1
        if (scenario === 'refresh_failure' && languageReads === 1)
          return new Response('{}', { status: 503 })
        return new Response(
          JSON.stringify({
            languages: [
              { target_language: 'en-GB', is_active: false, plan: null },
              ...(scenario === 'no_active_language'
                ? []
                : [
                    {
                      target_language: 'ja-JP',
                      is_active: true,
                      plan: { id: 9, cefr_level: 'A1' },
                    },
                  ]),
            ],
          })
        )
      })
      render(<PracticeCatalog topicId="7" />)
      fireEvent.click(await screen.findByRole('button', { name: 'generate' }))
      expect(await screen.findByRole('alert')).toHaveTextContent(
        'contextChanged'
      )
      expect(apiFetch).not.toHaveBeenCalled()
      fireEvent.click(screen.getByRole('button', { name: 'retry' }))
      if (scenario === 'refresh_failure') {
        expect(await screen.findByRole('alert')).toHaveTextContent(
          'errorMessage'
        )
        expect(useLanguageStore.getState().needsRefresh).toBe(true)
        expect(practiceRequest).toHaveBeenCalledTimes(2)
        fireEvent.click(screen.getByRole('button', { name: 'retry' }))
      }
      expect(
        await screen.findByRole('heading', { name: 'Present simple' })
      ).toBeVisible()
      expect(screen.getByRole('button', { name: 'generate' })).toBeDisabled()
      expect(screen.getByRole('link', { name: /ready/ })).toHaveAttribute(
        'href',
        `/grammar-practice/sessions/${id}`
      )
      expect(useLanguageStore.getState().needsRefresh).toBe(false)
      expect(useLanguageStore.getState().activeLanguage?.code ?? null).toBe(
        scenario === 'no_active_language' ? null : 'ja-JP'
      )
      expect(apiFetch).toHaveBeenCalledWith('/api/languages', expect.anything())
      expect(
        vi.mocked(practiceRequest).mock.calls.map(([path]) => path)
      ).toEqual([
        '/topics/7?skip=0&limit=10',
        '/topics/7/sessions',
        '/topics/7?skip=0&limit=10',
      ])
      expect(
        vi
          .mocked(practiceRequest)
          .mock.calls.filter(([, options]) => options?.method === 'POST')
      ).toHaveLength(1)
      expect(push).not.toHaveBeenCalled()
    }
  )

  it('continues a saved session discovered during explicit recovery without another POST', async () => {
    sessionStorage.setItem(
      pendingPracticeKey(7),
      JSON.stringify({
        topic_id: 7,
        payload: { request_id: id, study_plan_id: 4, target_language: 'en-GB' },
      })
    )
    vi.mocked(practiceRequest)
      .mockResolvedValueOnce(history)
      .mockResolvedValueOnce(initial)
    render(<PracticeCatalog topicId="7" />)
    fireEvent.click(
      await screen.findByRole('button', { name: 'retryCreation' })
    )
    await waitFor(() =>
      expect(push).toHaveBeenCalledWith(`/grammar-practice/sessions/${id}`)
    )
    expect(
      vi
        .mocked(practiceRequest)
        .mock.calls.every(([, options]) => !options?.method)
    ).toBe(true)
  })

  it('retains uncertain identity when its recovery GET is rate limited', async () => {
    const pending = {
      topic_id: 7,
      payload: { request_id: id, study_plan_id: 4, target_language: 'en-GB' },
    }
    sessionStorage.setItem(pendingPracticeKey(7), JSON.stringify(pending))
    vi.mocked(practiceRequest)
      .mockResolvedValueOnce(history)
      .mockRejectedValueOnce(new PracticeRequestError(429, 'unavailable', 10))
    render(<PracticeCatalog topicId="7" />)
    fireEvent.click(
      await screen.findByRole('button', { name: 'retryCreation' })
    )
    expect(await screen.findByRole('alert')).toHaveTextContent('recoveryError')
    expect(readPendingPractice(7)).toEqual(pending)
    expect(screen.getByRole('button', { name: 'retryCreation' })).toBeDisabled()
    expect(
      vi
        .mocked(practiceRequest)
        .mock.calls.every(([, options]) => !options?.method)
    ).toBe(true)
  })

  it('offers generation for the current plan alongside an older active session', async () => {
    vi.mocked(practiceRequest)
      .mockResolvedValueOnce({
        ...history,
        study_plan_id: 99,
        topic: { ...history.topic, active_session_id: id },
      })
      .mockResolvedValueOnce({
        ...initial,
        id: 'new-plan-session',
        study_plan_id: 99,
      })
    render(<PracticeCatalog topicId="7" />)
    expect(
      await screen.findByRole('link', { name: 'continue' })
    ).toHaveAttribute('href', `/grammar-practice/sessions/${id}`)
    expect(screen.getByRole('button', { name: 'generate' })).toBeEnabled()
    fireEvent.click(screen.getByRole('button', { name: 'generate' }))
    await waitFor(() =>
      expect(push).toHaveBeenCalledWith(
        '/grammar-practice/sessions/new-plan-session'
      )
    )
    expect(
      JSON.parse(String(vi.mocked(practiceRequest).mock.calls[1][1]?.body))
        .study_plan_id
    ).toBe(99)
  })

  it('persists the UUID before POST and uses it for uncertain recovery without a new POST', async () => {
    vi.mocked(practiceRequest)
      .mockResolvedValueOnce(history)
      .mockImplementationOnce(async (_path, options) => {
        const body = JSON.parse(String(options?.body))
        expect(readPendingPractice(7)).toEqual({ topic_id: 7, payload: body })
        expect(body).toMatchObject({
          study_plan_id: 4,
          target_language: 'en-GB',
        })
        throw new Error('lost response')
      })
    const view = render(<PracticeCatalog topicId="7" />)
    fireEvent.click(await screen.findByRole('button', { name: 'generate' }))
    const pendingId = readPendingPractice(7)?.payload.request_id
    await waitFor(() =>
      expect(push).toHaveBeenCalledWith(
        `/grammar-practice/sessions/${pendingId}`
      )
    )
    view.unmount()
    vi.mocked(practiceRequest).mockResolvedValue(history)
    render(<PracticeCatalog topicId="7" />)
    expect(
      await screen.findByRole('link', { name: 'recover' })
    ).toHaveAttribute('href', `/grammar-practice/sessions/${pendingId}`)
    expect(
      vi
        .mocked(practiceRequest)
        .mock.calls.filter(([, options]) => options?.method === 'POST')
    ).toHaveLength(1)
  })

  it('offers the conflicting active session instead of posting again', async () => {
    vi.mocked(practiceRequest)
      .mockResolvedValueOnce(history)
      .mockRejectedValueOnce(
        new PracticeRequestError(409, 'practice_in_progress', 0, id)
      )
    render(<PracticeCatalog topicId="7" />)
    fireEvent.click(await screen.findByRole('button', { name: 'generate' }))
    expect(
      await screen.findByRole('link', { name: 'continue' })
    ).toHaveAttribute('href', `/grammar-practice/sessions/${id}`)
    expect(sessionStorage.getItem(pendingPracticeKey(7))).toBeNull()
  })

  it.each(['freemium_exhausted', 'freemium_unavailable'])(
    'distinguishes quota denial from unavailability: %s',
    async (code) => {
      vi.mocked(practiceRequest)
        .mockResolvedValueOnce(history)
        .mockRejectedValueOnce(new PracticeRequestError(402, code))
      render(<PracticeCatalog topicId="7" />)
      fireEvent.click(await screen.findByRole('button', { name: 'generate' }))
      if (code === 'freemium_exhausted')
        expect(await screen.findByText('paywall')).toBeVisible()
      else {
        expect(await screen.findByRole('alert')).toHaveTextContent(
          'errorMessage'
        )
        expect(screen.queryByText('paywall')).not.toBeInTheDocument()
      }
      expect(screen.getByRole('link', { name: /ready/ })).toBeVisible()
    }
  )

  it('ignores late creation navigation after a language switch', async () => {
    const pending = deferred<Session>()
    vi.mocked(practiceRequest)
      .mockResolvedValueOnce(history)
      .mockReturnValueOnce(pending.promise)
      .mockResolvedValue(history)
    render(<PracticeCatalog topicId="7" />)
    fireEvent.click(await screen.findByRole('button', { name: 'generate' }))
    await waitFor(() => expect(practiceRequest).toHaveBeenCalledTimes(2))
    const signal = vi.mocked(practiceRequest).mock.calls[1][1]?.signal
    await act(async () => {
      useLanguageStore.setState({ activeLanguage: getLanguageByCode('ja-JP') })
      pending.resolve(initial)
    })
    expect(signal?.aborted).toBe(true)
    expect(push).not.toHaveBeenCalled()
  })
})

describe('grammar saved sessions', () => {
  it.each([422, 429])(
    'preserves a cloze draft after a provisional switch rejected with %s',
    async (status) => {
      vi.mocked(practiceRequest).mockResolvedValue({ ...initial, answered: 1 })
      const switching = deferred<Response>()
      vi.mocked(apiFetch).mockReturnValueOnce(switching.promise)
      render(<PracticeSession sessionId={id} />)
      const input = await screen.findByRole('textbox', { name: 'fillBlank' })
      fireEvent.change(input, { target: { value: 'drink' } })
      let switchResult!: Promise<boolean>
      act(() => {
        switchResult = useLanguageStore.getState().switchLanguage('ja-JP')
      })
      expect(input).not.toBeVisible()
      await act(async () => {
        switching.resolve(new Response(null, { status }))
        await switchResult
      })
      expect(screen.getByRole('textbox', { name: 'fillBlank' })).toBe(input)
      expect(input).toHaveValue('drink')
      expect(practiceRequest).toHaveBeenCalledTimes(1)
    }
  )

  it('holds an answer response until a rejected provisional switch settles', async () => {
    const answer = deferred<Session>()
    const switching = deferred<Response>()
    vi.mocked(practiceRequest)
      .mockResolvedValueOnce(initial)
      .mockReturnValueOnce(answer.promise)
    vi.mocked(apiFetch).mockReturnValueOnce(switching.promise)
    render(<PracticeSession sessionId={id} />)
    fireEvent.click(await screen.findByRole('radio', { name: 'goes' }))
    fireEvent.click(screen.getByRole('button', { name: 'check' }))
    let switchResult!: Promise<boolean>
    act(() => {
      switchResult = useLanguageStore.getState().switchLanguage('ja-JP')
    })
    await act(async () =>
      answer.resolve({
        ...initial,
        answered: 1,
        correct: 1,
        challenges: [
          {
            ...initial.challenges[0],
            answer: 1,
            correct: true,
            correct_answer: 'goes',
            explanation: 'Saved feedback',
          },
          ...initial.challenges.slice(1),
        ],
      })
    )
    expect(screen.queryByText('Saved feedback')).not.toBeInTheDocument()
    await act(async () => {
      switching.resolve(new Response(null, { status: 422 }))
      await switchResult
    })
    expect(await screen.findByText('Saved feedback')).toBeVisible()
    expect(practiceRequest).toHaveBeenCalledTimes(2)
    expect(screen.getByRole('textbox', { name: 'fillBlank' })).toBeEnabled()
  })

  it('completes all five persisted challenges, reveals only submitted solutions and enables voice at completion', async () => {
    let saved: Session = structuredClone(initial)
    const solutions = [1, 'drink', 0, 2, 'play']
    vi.mocked(practiceRequest).mockResolvedValueOnce(saved)
    for (const [index, value] of [1, 'drink', 1, 2, 'play'].entries()) {
      const correct = value === solutions[index]
      saved = {
        ...saved,
        answered: saved.answered + 1,
        correct: saved.correct + Number(correct),
        status: index === 4 ? 'completed' : 'ready',
        completed_at: index === 4 ? '2026-11-16T12:05:00Z' : null,
        challenges: saved.challenges.map((challenge) =>
          challenge.index === index
            ? {
                ...challenge,
                answer: value,
                correct,
                correct_answer:
                  typeof solutions[index] === 'number'
                    ? challenge.options![solutions[index] as number]
                    : String(solutions[index]),
                explanation: `Explanation ${index}`,
              }
            : challenge
        ),
      }
      vi.mocked(practiceRequest).mockResolvedValueOnce(saved)
    }
    render(<PracticeSession sessionId={id} />)
    for (const [index, value] of [1, 'drink', 1, 2, 'play'].entries()) {
      expect(
        screen.queryByRole('button', { name: 'voiceAction' })
      ).not.toBeInTheDocument()
      expect(screen.queryByText(`Explanation ${index}`)).not.toBeInTheDocument()
      if (typeof value === 'number')
        fireEvent.click(
          await screen.findByRole('radio', {
            name: initial.challenges[index].options![value],
          })
        )
      else
        fireEvent.change(
          await screen.findByRole('textbox', { name: 'fillBlank' }),
          { target: { value } }
        )
      fireEvent.click(screen.getByRole('button', { name: 'check' }))
      expect(await screen.findByText(`Explanation ${index}`)).toHaveAttribute(
        'lang',
        'es'
      )
    }
    expect(screen.getByRole('button', { name: 'voiceAction' })).toBeVisible()
    expect(screen.getByText('accuracy:{"percent":80}')).toBeVisible()
    expect(
      screen.queryByRole('button', { name: 'check' })
    ).not.toBeInTheDocument()
    expect(
      vi
        .mocked(practiceRequest)
        .mock.calls.filter(([, options]) => options?.method === 'POST')
        .map(([, options]) => JSON.parse(String(options?.body)))
    ).toEqual([
      { index: 0, value: 1 },
      { index: 1, value: 'drink' },
      { index: 2, value: 1 },
      { index: 3, value: 2 },
      { index: 4, value: 'play' },
    ])
  })

  it('recovers a lost answer via GET and only unlocks after known persisted state', async () => {
    const recovery = deferred<Session>()
    const saved = {
      ...initial,
      answered: 1,
      correct: 1,
      challenges: [
        {
          ...initial.challenges[0],
          answer: 1,
          correct: true,
          correct_answer: 'goes',
          explanation: 'Tercera persona.',
        },
        ...initial.challenges.slice(1),
      ],
    }
    vi.mocked(practiceRequest)
      .mockResolvedValueOnce(initial)
      .mockRejectedValueOnce(new Error('lost response'))
      .mockReturnValueOnce(recovery.promise)
    render(<PracticeSession sessionId={id} />)
    fireEvent.click(await screen.findByRole('radio', { name: 'goes' }))
    fireEvent.click(screen.getByRole('button', { name: 'check' }))
    await waitFor(() => expect(practiceRequest).toHaveBeenCalledTimes(3))
    expect(screen.getByRole('button', { name: 'check' })).toBeDisabled()
    await act(async () => recovery.resolve(saved))
    expect(await screen.findByText('Tercera persona.')).toHaveAttribute(
      'lang',
      'es'
    )
    expect(screen.getByRole('textbox', { name: 'fillBlank' })).toHaveAttribute(
      'lang',
      'en-GB'
    )
    expect(
      vi
        .mocked(practiceRequest)
        .mock.calls.filter(([, options]) => options?.method === 'POST')
    ).toHaveLength(1)
    expect(
      JSON.parse(String(vi.mocked(practiceRequest).mock.calls[1][1]?.body))
    ).toEqual({ index: 0, value: 1 })
  })

  it('resumes a saved-language cloze and submits through the form, with a 500-character limit', async () => {
    useLanguageStore.setState({ activeLanguage: getLanguageByCode('ja-JP') })
    vi.mocked(practiceRequest).mockResolvedValue({ ...initial, answered: 1 })
    render(<PracticeSession sessionId={id} />)
    const input = await screen.findByRole('textbox', { name: 'fillBlank' })
    expect(input).toHaveAttribute('lang', 'en-GB')
    expect(input).toHaveAttribute('maxlength', '500')
    fireEvent.change(input, { target: { value: 'drink' } })
    fireEvent.submit(input.closest('form')!)
    await waitFor(() => expect(practiceRequest).toHaveBeenCalledTimes(2))
    expect(vi.mocked(practiceRequest).mock.calls[1][0]).toBe(
      `/sessions/${id}/answers`
    )
    expect(
      JSON.parse(String(vi.mocked(practiceRequest).mock.calls[1][1]?.body))
    ).toEqual({ index: 1, value: 'drink' })
  })

  it('does not display future questions or solutions before answering', async () => {
    vi.mocked(practiceRequest).mockResolvedValue(initial)
    render(<PracticeSession sessionId={id} />)
    expect(await screen.findByText(/She ___ home\./)).toHaveAttribute(
      'lang',
      'en-GB'
    )
    expect(screen.queryByText(/I ___ tea\./)).not.toBeInTheDocument()
    expect(screen.queryByText('solution')).not.toBeInTheDocument()
  })

  it('requires confirmation to abandon and preserves feedback after abandonment', async () => {
    vi.mocked(practiceRequest)
      .mockResolvedValueOnce(initial)
      .mockResolvedValueOnce({ ...initial, status: 'abandoned' })
    render(<PracticeSession sessionId={id} />)
    fireEvent.click(await screen.findByRole('button', { name: 'abandon' }))
    expect(practiceRequest).toHaveBeenCalledTimes(1)
    const dialog = screen.getByRole('alertdialog')
    fireEvent.click(within(dialog).getByRole('button', { name: 'abandon' }))
    await waitFor(() =>
      expect(vi.mocked(practiceRequest).mock.calls[1][0]).toBe(
        `/sessions/${id}/abandon`
      )
    )
    expect(await screen.findByRole('link', { name: 'another' })).toBeVisible()
    expect(
      screen.queryByRole('button', { name: 'check' })
    ).not.toBeInTheDocument()
  })

  it('exposes voice only after completion and uses the exact session UUID after confirmation', async () => {
    vi.mocked(practiceRequest).mockResolvedValue({
      ...initial,
      status: 'completed',
      answered: 5,
      correct: 4,
    })
    render(<PracticeSession sessionId={id} />)
    fireEvent.click(await screen.findByRole('button', { name: 'voiceAction' }))
    expect(push).not.toHaveBeenCalled()
    fireEvent.click(
      within(screen.getByRole('alertdialog')).getByRole('button', {
        name: 'start',
      })
    )
    expect(push).toHaveBeenCalledWith(`/conversation?grammarPractice=${id}`)
  })

  it('does not navigate a stale voice confirmation after auth replacement', () => {
    render(
      <PracticeVoiceButton
        sessionId={id}
        title="Present simple"
        targetLanguage="en-GB"
      />
    )
    fireEvent.click(screen.getByRole('button', { name: 'voiceAction' }))
    act(() => useAuthStore.setState({ sessionVersion: 2 }))
    fireEvent.click(
      within(screen.getByRole('alertdialog')).getByRole('button', {
        name: 'start',
      })
    )
    expect(push).not.toHaveBeenCalled()
  })

  it('polls sequentially and cancels late polls when the context changes', async () => {
    vi.useFakeTimers()
    const poll = deferred<Session>()
    vi.mocked(practiceRequest)
      .mockResolvedValueOnce({
        ...initial,
        status: 'generating',
        challenges: [],
        remaining_seconds: 60,
      })
      .mockReturnValueOnce(poll.promise)
      .mockResolvedValue({ ...initial, title: 'New context read' })
    render(<PracticeSession sessionId={id} />)
    await act(async () => {
      await Promise.resolve()
    })
    await act(async () => {
      await vi.advanceTimersByTimeAsync(3000)
    })
    expect(practiceRequest).toHaveBeenCalledTimes(2)
    await act(async () => {
      await vi.advanceTimersByTimeAsync(12_000)
    })
    expect(practiceRequest).toHaveBeenCalledTimes(2)
    await act(async () => {
      useLanguageStore.setState({ invalidationVersion: 1 })
      poll.resolve({ ...initial, title: 'Stale poll' })
    })
    expect(screen.queryByText('Stale poll')).not.toBeInTheDocument()
    expect(screen.getByText('New context read')).toBeVisible()
  })

  it('honours Retry-After without overlapping recovery requests', async () => {
    vi.useFakeTimers()
    vi.mocked(practiceRequest)
      .mockRejectedValueOnce(new PracticeRequestError(429, 'unavailable', 8))
      .mockResolvedValue(initial)
    render(<PracticeSession sessionId={id} />)
    await act(async () => {
      await Promise.resolve()
    })
    await act(async () => {
      await vi.advanceTimersByTimeAsync(7999)
    })
    expect(practiceRequest).toHaveBeenCalledTimes(1)
    await act(async () => {
      await vi.advanceTimersByTimeAsync(1)
    })
    expect(practiceRequest).toHaveBeenCalledTimes(2)
    expect(screen.getByRole('radio', { name: 'goes' })).toBeEnabled()
  })

  it('stops after four read failures and retries only GET on explicit recovery', async () => {
    vi.useFakeTimers()
    vi.mocked(practiceRequest).mockRejectedValue(new Error('network'))
    render(<PracticeSession sessionId={id} />)
    await act(async () => {
      await vi.advanceTimersByTimeAsync(30_000)
    })
    expect(practiceRequest).toHaveBeenCalledTimes(4)
    expect(screen.getByRole('alert')).toHaveTextContent('recoveryError')
    await act(async () => {
      await vi.advanceTimersByTimeAsync(60_000)
    })
    expect(practiceRequest).toHaveBeenCalledTimes(4)
    vi.mocked(practiceRequest).mockResolvedValue(initial)
    await act(async () =>
      fireEvent.click(screen.getByRole('button', { name: 'retry' }))
    )
    expect(screen.getByRole('radio', { name: 'goes' })).toBeEnabled()
    expect(
      vi
        .mocked(practiceRequest)
        .mock.calls.every(([, options]) => !options?.method)
    ).toBe(true)
  })

  it('bounds generation observation even if the server keeps returning generating', async () => {
    vi.useFakeTimers()
    vi.mocked(practiceRequest).mockResolvedValue({
      ...initial,
      status: 'generating',
      challenges: [],
      remaining_seconds: 1,
    })
    render(<PracticeSession sessionId={id} />)
    await act(async () => {
      await vi.advanceTimersByTimeAsync(12_000)
    })
    expect(screen.getByRole('alert')).toHaveTextContent('recoveryError')
    const count = vi.mocked(practiceRequest).mock.calls.length
    await act(async () => {
      await vi.advanceTimersByTimeAsync(60_000)
    })
    expect(practiceRequest).toHaveBeenCalledTimes(count)
    expect(
      vi
        .mocked(practiceRequest)
        .mock.calls.every(([, options]) => !options?.method)
    ).toBe(true)
  })
})
