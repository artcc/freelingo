import {
  act,
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import AssessmentPage from '@/app/(app)/assessment/page'
import ListeningPage from '@/app/(app)/listening/page'
import ReadingPage from '@/app/(app)/reading/page'
import LanguageSwitcher from '@/components/LanguageSwitcher'
import { getLanguageByCode } from '@/lib/target-languages'
import { useAuthStore } from '@/store/auth'
import { useConfigStore } from '@/store/config'
import { useFreemiumStore } from '@/store/freemium'
import { useLanguageStore } from '@/store/language'
import { useLoadingStore } from '@/store/loading'

const { push, refresh } = vi.hoisted(() => ({
  push: vi.fn(),
  refresh: vi.fn(),
}))

vi.mock('next/navigation', () => ({ useRouter: () => ({ push, refresh }) }))
vi.mock('next-intl', () => {
  const translate = (key: string) => key
  return { useTranslations: () => translate, useLocale: () => 'en' }
})

// Only HTTP and framework navigation/translation are substituted. Pages, stores,
// apiFetch, useExerciseGeneration and resolveExercise run together.
const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status })
const plan = (id: number, level = 'A1') => ({
  id,
  cefr_level: level,
  progress_day: 0,
  total_days: 48,
  completion_pct: 0,
})
const languages = (id = 8) => ({
  languages: [
    {
      target_language: 'en-GB',
      is_active: true,
      plan: plan(id),
      progress: null,
    },
  ],
  all_supported_languages: ['en-GB'],
})
const ready = () =>
  json({
    available: true,
    context: { study_plan_id: 8, target_language: 'en-GB', level: 'A1' },
    exercise: {
      id: 42,
      target_language: 'en-GB',
      level: 'A1',
      exercise_type: 'story',
      topic: 'Fresh exercise',
      text: 'A new passage.',
      questions: [],
      duration_seconds: 10,
    },
    generation_status: 'idle',
    generation_error: null,
    generation_deadline: null,
    generation_remaining_seconds: null,
  })

beforeEach(() => {
  push.mockReset()
  refresh.mockReset()
  vi.stubGlobal('fetch', vi.fn())
  useLanguageStore.setState({
    activeLanguage: null,
    userLanguages: [],
    needsRefresh: false,
    isSwitching: false,
  })
  useAuthStore.setState({ user: null, accessToken: 'token' })
  useConfigStore.setState({
    loaded: true,
    stripeEnabled: false,
    maintenanceMode: false,
  })
  useLoadingStore.setState({ count: 0 })
  useFreemiumStore.setState({ status: null, loaded: false, lastFetch: 0 })
})

afterEach(() => {
  cleanup()
  vi.unstubAllGlobals()
  vi.useRealTimers()
})

describe.each([
  { feature: 'reading', Page: ReadingPage },
  { feature: 'listening', Page: ListeningPage },
])('$feature context initialization', ({ feature, Page }) => {
  const lookups = () =>
    vi
      .mocked(fetch)
      .mock.calls.filter(([url]) =>
        String(url).startsWith(`/api/${feature}/next`)
      )
  const assertFreshLookup = () => {
    expect(lookups()).toHaveLength(1)
    const query = new URL(String(lookups()[0][0]), 'http://localhost')
      .searchParams
    expect(query.get('expected_study_plan_id')).toBe('8')
    expect(query.get('expected_level')).toBe('A1')
    expect(query.get('expected_target_language')).toBe('en-GB')
  }

  it.each(['502', 'network'])(
    'recovers an initial language failure (%s) with Retry',
    async (failure) => {
      vi.mocked(fetch)
        .mockImplementationOnce(async () => {
          if (failure === 'network') throw new TypeError('Offline')
          return json({}, 502)
        })
        .mockResolvedValueOnce(json(languages()))
        .mockResolvedValueOnce(ready())

      render(<Page />)
      expect(await screen.findByText('unavailable')).toBeInTheDocument()
      expect(screen.queryByRole('status')).not.toBeInTheDocument()
      expect(lookups()).toHaveLength(0)
      // DOM removal can precede PageLoading's passive-effect cleanup.
      await waitFor(() => expect(useLoadingStore.getState().count).toBe(0))

      fireEvent.click(screen.getByRole('button', { name: 'retry' }))
      await waitFor(assertFreshLookup)
      expect(await screen.findByText(/Fresh exercise/)).toBeInTheDocument()
      await waitFor(() => expect(useLoadingStore.getState().count).toBe(0))
      expect(screen.queryByText('unavailable')).not.toBeInTheDocument()
      expect(
        screen.queryByRole('button', { name: 'retry' })
      ).not.toBeInTheDocument()
      expect(
        vi
          .mocked(fetch)
          .mock.calls.some(([, options]) => options?.method === 'POST')
      ).toBe(false)
    }
  )

  it('recovers a persisted language switch and discards the switcher’s older response', async () => {
    const original = {
      ...languages(),
      languages: [
        ...languages().languages,
        {
          target_language: 'es-ES',
          is_active: false,
          plan: plan(9),
          progress: null,
        },
      ],
    }
    const updated = {
      ...original,
      languages: original.languages.map((language) => ({
        ...language,
        is_active: language.target_language === 'es-ES',
      })),
    }
    useLanguageStore.setState({
      activeLanguage: getLanguageByCode('en-GB') ?? null,
      userLanguages: original.languages,
    })
    let finishOld: (response: Response) => void = () => {}
    const oldSummary = new Promise<Response>((resolve) => {
      finishOld = resolve
    })
    let summaryCalls = 0
    vi.mocked(fetch).mockImplementation(async (url) => {
      if (url === '/api/languages/active') return json({})
      if (url === '/api/languages') {
        summaryCalls += 1
        if (summaryCalls === 1) return oldSummary
        return summaryCalls <= 3 ? json({}, 502) : json(updated)
      }
      const response = await ready().json()
      if (String(url).includes('expected_target_language=es-ES')) {
        response.context = {
          study_plan_id: 9,
          target_language: 'es-ES',
          level: 'A1',
        }
        response.exercise.target_language = 'es-ES'
      }
      return json(response)
    })
    render(
      <>
        <LanguageSwitcher />
        <Page />
      </>
    )
    expect(await screen.findByText(/Fresh exercise/)).toBeInTheDocument()
    fireEvent.click(screen.getByRole('button', { name: /en-GB/ }))
    fireEvent.click(screen.getByRole('button', { name: /es-ES/ }))
    expect(await screen.findByText('unavailable')).toBeInTheDocument()
    expect(screen.queryByText('switched')).not.toBeInTheDocument()
    expect(refresh).not.toHaveBeenCalled()
    expect(useLanguageStore.getState().needsRefresh).toBe(true)
    expect(lookups()).toHaveLength(1)
    await act(async () => {
      finishOld(json(original))
    })
    expect(useLanguageStore.getState().needsRefresh).toBe(true)
    // Recover from the switcher without repeating the server-side mutation.
    fireEvent.click(screen.getAllByRole('button', { name: 'retry' })[0])
    await waitFor(() =>
      expect(useLanguageStore.getState().activeLanguage?.code).toBe('es-ES')
    )
    expect(await screen.findByText(/Fresh exercise/)).toBeInTheDocument()
    expect(lookups()).toHaveLength(2)
    expect(String(lookups()[1][0])).toContain('expected_study_plan_id=9')
    expect(String(lookups()[1][0])).toContain('expected_target_language=es-ES')
    expect(
      vi
        .mocked(fetch)
        .mock.calls.filter(([, options]) => options?.method === 'PUT')
    ).toHaveLength(1)
  })

  it.each([
    { replay: false, rejected: false },
    { replay: false, rejected: true },
    { replay: true, rejected: false },
    { replay: true, rejected: true },
  ])(
    'submits the captured context (replay: $replay, rejected: $rejected)',
    async ({ replay, rejected }) => {
      const response = await ready().json()
      response.exercise.questions = Array.from({ length: 5 }, (_, index) => ({
        index,
        question: `Question ${index}`,
        options: { A: `Answer ${index}`, B: `Other ${index}` },
      }))
      const historyContext = {
        study_plan_id: 8,
        target_language: 'en-GB',
        level: 'B2',
      }
      useLanguageStore.setState({
        activeLanguage: getLanguageByCode('en-GB') ?? null,
        userLanguages: languages().languages,
      })
      vi.mocked(fetch).mockImplementation(async (url) => {
        if (String(url).startsWith(`/api/${feature}/history`))
          return json({
            context: historyContext,
            total: 1,
            items: [
              {
                id: 1,
                score: 5,
                xp_earned: 50,
                exercise: response.exercise,
                text: response.exercise.text,
                answers: {},
                correct_answers: [],
              },
            ],
          })
        if (url === `/api/${feature}/attempt`)
          return rejected
            ? json({ detail: 'study_context_changed' }, 409)
            : json({
                score: 5,
                xp_earned: replay ? 0 : 50,
                correct_answers: [],
                text: response.exercise.text,
              })
        if (String(url).startsWith('/api/reviews')) return json({})
        return json(response)
      })
      render(<Page />)
      expect(await screen.findByText(/Fresh exercise/)).toBeInTheDocument()
      if (replay) {
        fireEvent.click(screen.getByRole('button', { name: 'history' }))
        fireEvent.click(
          await screen.findByRole('button', { name: 'practiceAgain' })
        )
      }
      for (let index = 0; index < 5; index += 1) {
        fireEvent.click(
          screen.getByRole('button', { name: new RegExp(`Answer ${index}`) })
        )
      }
      fireEvent.click(screen.getByRole('button', { name: 'submit' }))
      expect(
        await screen.findByText(rejected ? 'contextChanged' : 'resultsLabel')
      ).toBeInTheDocument()
      const attempts = vi
        .mocked(fetch)
        .mock.calls.filter(([url]) => url === `/api/${feature}/attempt`)
      expect(attempts).toHaveLength(1)
      expect(JSON.parse(String(attempts[0][1]?.body))).toEqual({
        exercise_id: 42,
        replay,
        context: replay ? historyContext : response.context,
        answers: { 0: 'A', 1: 'A', 2: 'A', 3: 'A', 4: 'A' },
      })
      if (rejected)
        expect(screen.queryByText('resultsLabel')).not.toBeInTheDocument()
    }
  )

  it.each([false, true])(
    'preserves partial answers after a rejected switch (replay: %s)',
    async (replay) => {
      const response = await ready().json()
      response.exercise.questions = Array.from({ length: 5 }, (_, index) => ({
        index,
        question: `Question ${index}`,
        options: { A: `Answer ${index}`, B: `Other ${index}` },
      }))
      const historyExercise = {
        ...response.exercise,
        id: 77,
        topic: 'History exercise',
      }
      useLanguageStore.setState({
        activeLanguage: getLanguageByCode('en-GB') ?? null,
        userLanguages: languages().languages,
      })
      let rejectSwitch: (response: Response) => void = () => {}
      const pendingSwitch = new Promise<Response>((resolve) => {
        rejectSwitch = resolve
      })
      vi.mocked(fetch).mockImplementation(async (url) => {
        if (url === '/api/languages/active') return pendingSwitch
        if (String(url).startsWith(`/api/${feature}/history`))
          return json({
            context: response.context,
            total: 1,
            items: [
              {
                id: 1,
                score: 5,
                xp_earned: 50,
                exercise: historyExercise,
                text: historyExercise.text,
                answers: {},
                correct_answers: [],
              },
            ],
          })
        if (url === `/api/${feature}/attempt`)
          return json({
            score: 5,
            xp_earned: replay ? 0 : 50,
            correct_answers: [],
            text: response.exercise.text,
          })
        if (String(url).startsWith('/api/reviews')) return json({})
        return json(response)
      })
      render(<Page />)
      expect(await screen.findByText(/Fresh exercise/)).toBeInTheDocument()
      if (replay) {
        fireEvent.click(screen.getByRole('button', { name: 'history' }))
        fireEvent.click(
          await screen.findByRole('button', { name: 'practiceAgain' })
        )
      }
      fireEvent.click(screen.getByRole('button', { name: /Answer 0/ }))
      let switching: Promise<boolean> = Promise.resolve(true)
      act(() => {
        switching = useLanguageStore.getState().switchLanguage('es-ES')
      })
      expect(useLanguageStore.getState().isSwitching).toBe(true)
      expect(screen.getByRole('button', { name: /Answer 0/ })).toHaveClass(
        'border-fl-accent'
      )
      expect(screen.queryByRole('status')).not.toBeInTheDocument()
      await act(async () => {
        rejectSwitch(json({ detail: 'Language not available' }, 422))
        expect(await switching).toBe(false)
      })
      expect(useLanguageStore.getState().needsRefresh).toBe(false)
      expect(lookups()).toHaveLength(1)
      expect(screen.getByRole('button', { name: /Answer 0/ })).toHaveClass(
        'border-fl-accent'
      )
      for (let index = 1; index < 5; index += 1) {
        fireEvent.click(
          screen.getByRole('button', { name: new RegExp(`Answer ${index}`) })
        )
      }
      fireEvent.click(screen.getByRole('button', { name: 'submit' }))
      expect(await screen.findByText('resultsLabel')).toBeInTheDocument()
      const attempt = vi
        .mocked(fetch)
        .mock.calls.find(([url]) => url === `/api/${feature}/attempt`)
      expect(JSON.parse(String(attempt?.[1]?.body))).toEqual({
        exercise_id: replay ? 77 : 42,
        replay,
        context: response.context,
        answers: { 0: 'A', 1: 'A', 2: 'A', 3: 'A', 4: 'A' },
      })
    }
  )

  it.each(['PUT', 'auth refresh'])(
    'bounds a pending %s during a language switch and recovers through GET',
    async (pendingStage) => {
      vi.useFakeTimers()
      vi.spyOn(AbortSignal, 'timeout').mockImplementation((ms) => {
        const controller = new AbortController()
        setTimeout(
          () => controller.abort(new DOMException('Timed out', 'TimeoutError')),
          ms
        )
        return controller.signal
      })
      useLanguageStore.setState({
        activeLanguage: getLanguageByCode('en-GB') ?? null,
        userLanguages: languages().languages,
      })
      const updated = {
        ...languages(9),
        languages: [{ ...languages(9).languages[0], target_language: 'es-ES' }],
      }
      let finishRefresh: (response: Response) => void = () => {}
      const refreshResponse = new Promise<Response>((resolve) => {
        finishRefresh = resolve
      })
      let summaryCalls = 0
      vi.mocked(fetch).mockImplementation(async (url, options) => {
        if (url === '/api/auth/refresh') return refreshResponse
        if (url === '/api/languages/active') {
          if (pendingStage === 'auth refresh') return json({}, 401)
          return new Promise((_resolve, reject) => {
            options?.signal?.addEventListener(
              'abort',
              () => reject(options.signal?.reason),
              { once: true }
            )
          })
        }
        if (url === '/api/languages')
          return ++summaryCalls === 1 ? json({}, 502) : json(updated)
        const response = await ready().json()
        response.context = {
          study_plan_id: 9,
          target_language: 'es-ES',
          level: 'A1',
        }
        response.exercise.target_language = 'es-ES'
        return json(response)
      })
      const switching = useLanguageStore.getState().switchLanguage('es-ES')
      // Entering a page during the switch must also have a bounded wait.
      render(<Page />)
      await act(async () => {
        await vi.advanceTimersByTimeAsync(19_999)
      })
      expect(useLanguageStore.getState().isSwitching).toBe(true)
      expect(lookups()).toHaveLength(0)
      await act(async () => {
        await vi.advanceTimersByTimeAsync(1)
      })
      expect(await switching).toBe(false)
      expect(useLanguageStore.getState().isSwitching).toBe(false)
      expect(useLanguageStore.getState().needsRefresh).toBe(true)
      expect(screen.getByText('unavailable')).toBeInTheDocument()
      expect(screen.getByRole('button', { name: 'retry' })).toBeInTheDocument()
      expect(screen.queryByRole('status')).not.toBeInTheDocument()
      expect(useLoadingStore.getState().count).toBe(0)
      await act(async () => {
        finishRefresh(json({ access_token: 'new-token' }))
        await vi.advanceTimersByTimeAsync(0)
      })
      if (pendingStage === 'auth refresh')
        expect(useAuthStore.getState().accessToken).toBe('new-token')
      vi.useRealTimers()
      fireEvent.click(screen.getByRole('button', { name: 'retry' }))
      expect(await screen.findByText(/Fresh exercise/)).toBeInTheDocument()
      expect(lookups()).toHaveLength(1)
      expect(String(lookups()[0][0])).toContain('expected_study_plan_id=9')
      expect(String(lookups()[0][0])).toContain(
        'expected_target_language=es-ES'
      )
      expect(
        vi
          .mocked(fetch)
          .mock.calls.filter(([, options]) => options?.method === 'PUT')
      ).toHaveLength(1)
    }
  )

  it.each(['missing', 'invalidated'])(
    'recovers %s context with an exhausted quota without enabling generation',
    async (contextState) => {
      useConfigStore.setState({ stripeEnabled: true })
      useAuthStore.setState({
        user: {
          id: 1,
          username: 'learner',
          displayName: 'Learner',
          role: 'user',
          conversation_max_duration: 300,
          conversation_inactivity_timeout: 60,
          subscription_status: 'none',
        },
      })
      useFreemiumStore.setState({
        loaded: true,
        lastFetch: Date.now(),
        status: {
          trial_active: false,
          trial_ends_at: null,
          chat_remaining: 0,
          chat_limit: 5,
          lessons_remaining: 0,
          lessons_limit: 5,
          listening_remaining: 0,
          listening_limit: 5,
          reading_remaining: 0,
          reading_limit: 5,
          games_remaining: 3,
          games_limit: 3,
          voice_remaining_seconds: 0,
          voice_limit_seconds: 300,
        },
      })
      if (contextState === 'invalidated') {
        useLanguageStore.setState({
          activeLanguage: getLanguageByCode('en-GB') ?? null,
          userLanguages: languages(7).languages,
          needsRefresh: true,
        })
      }
      vi.mocked(fetch)
        .mockResolvedValueOnce(json({}, 502))
        .mockResolvedValueOnce(json(languages()))
        .mockResolvedValueOnce(
          json({
            available: false,
            exercise: null,
            context: {
              study_plan_id: 8,
              target_language: 'en-GB',
              level: 'A1',
            },
            generation_status: 'idle',
          })
        )

      render(<Page />)
      expect(await screen.findByText('unavailable')).toBeInTheDocument()
      expect(screen.getByText('paywallLabel')).toBeInTheDocument()
      expect(
        screen.queryByRole('button', { name: 'generate' })
      ).not.toBeInTheDocument()
      expect(lookups()).toHaveLength(0)

      fireEvent.click(screen.getByRole('button', { name: 'retry' }))
      await waitFor(assertFreshLookup)
      expect(await screen.findByText('paywallLabel')).toBeInTheDocument()
      expect(screen.queryByText('unavailable')).not.toBeInTheDocument()
      expect(
        screen.queryByRole('button', { name: 'retry' })
      ).not.toBeInTheDocument()
      expect(
        screen.queryByRole('button', { name: 'generate' })
      ).not.toBeInTheDocument()
      expect(
        vi
          .mocked(fetch)
          .mock.calls.some(([, options]) => options?.method === 'POST')
      ).toBe(false)
    }
  )

  it('bounds a pending language request and offers recovery', async () => {
    vi.useFakeTimers()
    vi.spyOn(AbortSignal, 'timeout').mockImplementation((ms) => {
      const controller = new AbortController()
      setTimeout(
        () => controller.abort(new DOMException('Timed out', 'TimeoutError')),
        ms
      )
      return controller.signal
    })
    vi.mocked(fetch).mockImplementationOnce(
      (_url, options) =>
        new Promise((_resolve, reject) => {
          options?.signal?.addEventListener(
            'abort',
            () => reject(options.signal?.reason),
            { once: true }
          )
        })
    )
    render(<Page />)
    await act(async () => {
      await vi.advanceTimersByTimeAsync(20_000)
    })
    expect(screen.getByText('unavailable')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'retry' })).toBeInTheDocument()
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
    expect(lookups()).toHaveLength(0)
    expect(useLoadingStore.getState().count).toBe(0)
  })

  it.each([200, 503])(
    'preserves shared context loading after unmount without starting exercises (HTTP %s)',
    async (status) => {
      let signal: AbortSignal | null | undefined
      let finish!: (response: Response) => void
      vi.mocked(fetch).mockImplementationOnce(
        (_url, options) =>
          new Promise((resolve, reject) => {
            finish = resolve
            signal = options?.signal
            signal?.addEventListener('abort', () => reject(signal?.reason), {
              once: true,
            })
          })
      )
      const { unmount } = render(<Page />)
      render(<LanguageSwitcher />)
      expect(fetch).toHaveBeenCalledTimes(1)
      expect(fetch).toHaveBeenCalledWith('/api/languages', expect.any(Object))

      unmount()
      // Only the shared HTTP request remains; the page's loading owner is gone.
      await waitFor(() => expect(useLoadingStore.getState().count).toBe(1))
      expect(signal?.aborted).toBe(false)
      expect(lookups()).toHaveLength(0)

      await act(async () =>
        finish(json(status === 200 ? languages() : {}, status))
      )
      await waitFor(() => expect(useLoadingStore.getState().count).toBe(0))
      if (status === 200) {
        expect(useLanguageStore.getState().activeLanguage?.code).toBe('en-GB')
        expect(
          screen.getByRole('button', { name: /en-GB/ })
        ).toBeInTheDocument()
      } else {
        expect(useLanguageStore.getState().activeLanguage).toBeNull()
      }
      expect(lookups()).toHaveLength(0)
      expect(fetch).toHaveBeenCalledTimes(1)
    }
  )

  it.each([false, true])(
    'uses the new plan after retaking Assessment (voice offer: %s)',
    async (voiceOffer) => {
      useLanguageStore.setState({
        activeLanguage: getLanguageByCode('en-GB') ?? null,
        userLanguages: [
          {
            target_language: 'en-GB',
            is_active: true,
            plan: plan(7, 'B1'),
            progress: null,
          },
        ],
      })
      let finishSummary: (response: Response) => void = () => {}
      const summary = new Promise<Response>((resolve) => {
        finishSummary = resolve
      })
      vi.mocked(fetch).mockImplementation(async (url) => {
        if (url === '/api/study-plan/current')
          return json({ cefr_level: 'B1', created_at: '2026-01-01' })
        if (String(url).startsWith('/api/assessment/bank'))
          return json({ questions: [] })
        if (url === '/api/assessment/complete')
          return json({
            plan_id: 8,
            cefr_level: 'A1',
            voice_trial: voiceOffer
              ? { available: true, token: 'trial', duration_seconds: 300 }
              : { available: false },
          })
        if (url === '/api/languages') return summary
        return ready()
      })

      const assessment = render(<AssessmentPage />)
      fireEvent.click(await screen.findByRole('button', { name: 'retake' }))
      fireEvent.click(screen.getByRole('button', { name: /beginnerOption/ }))
      fireEvent.click(screen.getByRole('button', { name: /startMyPlan/ }))
      await waitFor(() =>
        expect(useLanguageStore.getState().needsRefresh).toBe(true)
      )
      expect(push).not.toHaveBeenCalled()
      expect(screen.queryByText('voiceTrialTitle')).not.toBeInTheDocument()
      await act(async () => {
        finishSummary(json(languages()))
      })
      if (voiceOffer)
        expect(await screen.findByText('voiceTrialTitle')).toBeInTheDocument()
      else await waitFor(() => expect(push).toHaveBeenCalledWith('/plan'))
      expect(useLanguageStore.getState().userLanguages[0].plan?.id).toBe(8)
      assessment.unmount()

      // Navigation preserves the same Zustand store, as the app layout does.
      render(<Page />)
      await waitFor(assertFreshLookup)
      expect(await screen.findByText(/Fresh exercise/)).toBeInTheDocument()
      await waitFor(() =>
        expect(screen.queryByRole('status')).not.toBeInTheDocument()
      )
      expect(screen.queryByText('contextChanged')).not.toBeInTheDocument()
    }
  )

  it('recovers a failed summary refresh after Assessment without re-creating the plan', async () => {
    useLanguageStore.setState({
      activeLanguage: getLanguageByCode('en-GB') ?? null,
      userLanguages: [
        {
          target_language: 'en-GB',
          is_active: true,
          plan: plan(7, 'B1'),
          progress: null,
        },
      ],
    })
    let summaryCalls = 0
    vi.mocked(fetch).mockImplementation(async (url) => {
      if (url === '/api/study-plan/current')
        return json({ cefr_level: 'B1', created_at: '2026-01-01' })
      if (String(url).startsWith('/api/assessment/bank'))
        return json({ questions: [] })
      if (url === '/api/assessment/complete')
        return json({ plan_id: 8, cefr_level: 'A1' })
      if (url === '/api/languages')
        return ++summaryCalls <= 2 ? json({}, 502) : json(languages())
      return ready()
    })
    const assessment = render(<AssessmentPage />)
    fireEvent.click(await screen.findByRole('button', { name: 'retake' }))
    fireEvent.click(screen.getByRole('button', { name: /beginnerOption/ }))
    fireEvent.click(screen.getByRole('button', { name: /startMyPlan/ }))
    await waitFor(() => expect(push).toHaveBeenCalledWith('/plan'))
    expect(useLanguageStore.getState().needsRefresh).toBe(true)
    assessment.unmount()

    render(<Page />)
    expect(await screen.findByText('unavailable')).toBeInTheDocument()
    expect(lookups()).toHaveLength(0)
    fireEvent.click(screen.getByRole('button', { name: 'retry' }))
    await waitFor(assertFreshLookup)
    expect(await screen.findByText(/Fresh exercise/)).toBeInTheDocument()
    await waitFor(() =>
      expect(screen.queryByRole('status')).not.toBeInTheDocument()
    )
    expect(
      vi
        .mocked(fetch)
        .mock.calls.filter(([url]) => url === '/api/assessment/complete')
    ).toHaveLength(1)
  })
})
