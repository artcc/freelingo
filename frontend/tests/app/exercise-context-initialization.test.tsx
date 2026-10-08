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
      questions: Array.from({ length: 5 }, (_, index) => ({
        index,
        question: `Question ${index}`,
        options: {
          A: `Answer ${index}`,
          B: `Other ${index}`,
          C: `Third ${index}`,
          D: `Fourth ${index}`,
        },
      })),
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

function deferred<T>() {
  let resolve!: (value: T) => void
  const promise = new Promise<T>((done) => {
    resolve = done
  })
  return { promise, resolve }
}

function answerExercise() {
  for (let index = 0; index < 5; index += 1) {
    fireEvent.click(
      screen.getByRole('button', { name: new RegExp(`Answer ${index}`) })
    )
  }
}

describe('Assessment context recovery', () => {
  it('recovers a committed language addition using GET and completes only the resolved language', async () => {
    useLanguageStore.setState({
      activeLanguage: getLanguageByCode('en-GB') ?? null,
      userLanguages: languages().languages,
    })
    let recover = false
    vi.mocked(fetch).mockImplementation(async (url, options) => {
      if (url === '/api/languages' && options?.method === 'POST')
        return json({})
      if (url === '/api/languages')
        return recover
          ? json({
              languages: [
                {
                  target_language: 'de-DE',
                  is_active: true,
                  plan: null,
                  progress: null,
                },
              ],
            })
          : json({}, 503)
      if (url === '/api/study-plan/current') return json(null)
      if (url === '/api/assessment/bank?language=de-DE')
        return json({ questions: [] })
      if (url === '/api/assessment/complete')
        return json({ plan_id: 9, cefr_level: 'A1' })
      return json({}, 404)
    })
    expect(await useLanguageStore.getState().addLanguage('de-DE')).toBe(true)
    expect(useLanguageStore.getState().needsRefresh).toBe(true)
    render(<AssessmentPage />)
    expect(await screen.findByRole('alert')).toHaveTextContent('errorMessage')
    expect(
      vi.mocked(fetch).mock.calls.every(([url]) => url === '/api/languages')
    ).toBe(true)
    recover = true
    fireEvent.click(screen.getByRole('button', { name: 'retry' }))
    fireEvent.click(
      await screen.findByRole('button', { name: /beginnerOption/ })
    )
    fireEvent.click(screen.getByRole('button', { name: /startMyPlan/ }))
    await waitFor(() => expect(push).toHaveBeenCalledWith('/plan'))
    const completed = vi
      .mocked(fetch)
      .mock.calls.filter(([url]) => url === '/api/assessment/complete')
    expect(completed).toHaveLength(1)
    expect(JSON.parse(completed[0][1]!.body as string).target_language).toBe(
      'de-DE'
    )
    expect(
      vi
        .mocked(fetch)
        .mock.calls.filter(
          ([url, options]) =>
            url === '/api/languages' && options?.method === 'POST'
        )
    ).toHaveLength(1)
    expect(
      vi
        .mocked(fetch)
        .mock.calls.some(([url]) => String(url).includes('bank?language=en-GB'))
    ).toBe(false)
  })

  it('discards an earlier plan check after the assessment language changes', async () => {
    useLanguageStore.setState({
      activeLanguage: getLanguageByCode('en-GB') ?? null,
      userLanguages: languages().languages,
    })
    let finish!: (response: Response) => void
    const old = new Promise<Response>((resolve) => {
      finish = resolve
    })
    vi.mocked(fetch).mockImplementation(async (url) => {
      if (url === '/api/study-plan/current')
        return useLanguageStore.getState().activeLanguage?.code === 'en-GB'
          ? old
          : json(null)
      return json({ questions: [] })
    })
    render(<AssessmentPage />)
    const oldSignal = vi.mocked(fetch).mock.calls[0][1]!.signal!
    act(() =>
      useLanguageStore.setState({
        activeLanguage: getLanguageByCode('de-DE') ?? null,
      })
    )
    await screen.findByRole('button', { name: /beginnerOption/ })
    await act(async () =>
      finish(json({ cefr_level: 'C1', created_at: '2026-01-01' }))
    )
    expect(oldSignal.aborted).toBe(true)
    expect(
      screen.queryByRole('button', { name: 'retake' })
    ).not.toBeInTheDocument()
    expect(
      screen.getByRole('button', { name: /beginnerOption/ })
    ).toBeInTheDocument()
  })
})

describe.each([
  { feature: 'reading', Page: ReadingPage },
  { feature: 'listening', Page: ListeningPage },
])('$feature context initialization', ({ feature, Page }) => {
  it.each([
    'during-switch',
    'after-switch',
    'unmount',
    'new-session',
    'new-session-failure',
    'network',
    'server-error',
    'invalid-body',
    'overlapping-refresh',
  ])(
    'settles global quota independently of the exercise presentation (%s)',
    async (scenario) => {
      useLanguageStore.setState({
        activeLanguage: getLanguageByCode('en-GB') ?? null,
        userLanguages: languages().languages,
      })
      useConfigStore.setState({ stripeEnabled: true })
      const initialRemaining = [
        'after-switch',
        'invalid-body',
        'overlapping-refresh',
      ].includes(scenario)
        ? 2
        : 1
      const quota = {
        trial_active: false,
        trial_ends_at: null,
        chat_remaining: 5,
        chat_limit: 5,
        lessons_remaining: 5,
        lessons_limit: 5,
        listening_remaining: initialRemaining,
        listening_limit: 5,
        reading_remaining: initialRemaining,
        reading_limit: 5,
        games_remaining: 3,
        games_limit: 3,
        voice_remaining_seconds: 300,
        voice_limit_seconds: 300,
      }
      useFreemiumStore.setState({
        status: quota,
        loaded: true,
        lastFetch: Date.now(),
      })
      const quotaKey =
        feature === 'reading' ? 'reading_remaining' : 'listening_remaining'
      const transport = deferred<Response>()
      const switchResponse = deferred<Response>()
      const result = {
        score: 5,
        xp_earned: 50,
        text: 'Transcript',
        correct_answers: Array.from({ length: 5 }, (_, index) => ({
          index,
          correct: 'A',
        })),
      }
      const attempts: RequestInit[] = []
      vi.mocked(fetch).mockImplementation(async (url, options) => {
        if (url === `/api/${feature}/attempt`) {
          attempts.push(options!)
          const response = await transport.promise
          if (scenario === 'network' || scenario === 'new-session-failure')
            throw new TypeError('Lost response')
          return response
        }
        if (url === '/api/languages/active') return switchResponse.promise
        if (url === '/api/languages')
          return json({
            languages: [
              { ...languages(9).languages[0], target_language: 'de-DE' },
            ],
          })
        if (url === '/api/freemium/status')
          return json({ ...quota, [quotaKey]: initialRemaining - 1 })
        if (String(url).startsWith('/api/reviews')) return json({})
        const body = await ready().json()
        if (useLanguageStore.getState().activeLanguage?.code === 'de-DE') {
          body.context = {
            study_plan_id: 9,
            target_language: 'de-DE',
            level: 'A1',
          }
          body.exercise = {
            ...body.exercise,
            id: 43,
            topic: 'Replacement exercise',
            target_language: 'de-DE',
          }
        }
        return json(body)
      })
      const { unmount } = render(<Page />)
      await screen.findByText(/Fresh exercise/)
      answerExercise()
      fireEvent.click(screen.getByRole('button', { name: 'submit' }))
      await waitFor(() => expect(attempts).toHaveLength(1))
      if (scenario === 'unmount') unmount()
      else if (scenario.startsWith('new-session')) {
        act(() => {
          useAuthStore.getState().startSession('another-user')
          useFreemiumStore.setState({
            status: { ...quota, [quotaKey]: 5 },
            loaded: true,
            lastFetch: Date.now(),
          })
        })
      } else {
        let switching!: Promise<boolean>
        act(() => {
          switching = useLanguageStore.getState().switchLanguage('de-DE')
        })
        if (scenario === 'during-switch') {
          await act(async () => transport.resolve(json(result)))
          expect(useFreemiumStore.getState().status?.[quotaKey]).toBe(0)
          expect(screen.queryByText('resultsLabel')).not.toBeInTheDocument()
        }
        await act(async () => {
          switchResponse.resolve(json({}))
          expect(await switching).toBe(true)
        })
        expect(useLanguageStore.getState().activeLanguage?.code).toBe('de-DE')
        if (feature === 'listening' && scenario === 'during-switch') {
          expect(
            await screen.findByText('paywallListeningTitle')
          ).toBeInTheDocument()
          expect(
            screen.queryByRole('button', { name: 'submit' })
          ).not.toBeInTheDocument()
        } else {
          await screen.findByText(/Replacement exercise/)
        }
      }
      expect(attempts[0].signal?.aborted).not.toBe(true)
      if (scenario === 'overlapping-refresh') {
        await act(async () => useFreemiumStore.getState().fetchStatus(true))
        expect(useFreemiumStore.getState().status?.[quotaKey]).toBe(1)
      }
      if (scenario !== 'during-switch')
        await act(async () =>
          transport.resolve(
            scenario === 'invalid-body'
              ? new Response('invalid json')
              : json(result, scenario === 'server-error' ? 503 : 200)
          )
        )
      const expectedQuota = scenario.startsWith('new-session')
        ? 5
        : initialRemaining - 1
      await waitFor(() =>
        expect(useFreemiumStore.getState().status?.[quotaKey]).toBe(
          expectedQuota
        )
      )
      expect(screen.queryByText('resultsLabel')).not.toBeInTheDocument()
      expect(screen.queryByText('errorSubmit')).not.toBeInTheDocument()
      expect(attempts).toHaveLength(1)
      expect(JSON.parse(String(attempts[0].body)).answers).toEqual({
        0: 'A',
        1: 'A',
        2: 'A',
        3: 'A',
        4: 'A',
      })
      expect(
        vi
          .mocked(fetch)
          .mock.calls.filter(([url]) => url === '/api/freemium/status')
      ).toHaveLength(
        scenario === 'overlapping-refresh'
          ? 2
          : scenario === 'network' || scenario === 'server-error'
            ? 1
            : 0
      )
    }
  )

  it.each([
    { replay: false, status: 422, timing: 'during' },
    { replay: false, status: 422, timing: 'after' },
    { replay: false, status: 429, timing: 'during' },
    { replay: false, status: 429, timing: 'after' },
    { replay: true, status: 422, timing: 'during' },
    { replay: true, status: 422, timing: 'after' },
    { replay: true, status: 429, timing: 'during' },
    { replay: true, status: 429, timing: 'after' },
  ])(
    'keeps a persisted attempt through a rejected $status switch (replay: $replay, body: $timing)',
    async ({ replay, status, timing }) => {
      useLanguageStore.setState({
        activeLanguage: getLanguageByCode('en-GB') ?? null,
        userLanguages: languages().languages,
      })
      useConfigStore.setState({ stripeEnabled: true })
      useFreemiumStore.setState({
        loaded: true,
        lastFetch: Date.now(),
        status: {
          trial_active: false,
          trial_ends_at: null,
          chat_remaining: 5,
          chat_limit: 5,
          lessons_remaining: 5,
          lessons_limit: 5,
          listening_remaining: 5,
          listening_limit: 5,
          reading_remaining: 5,
          reading_limit: 5,
          games_remaining: 3,
          games_limit: 3,
          voice_remaining_seconds: 300,
          voice_limit_seconds: 300,
        },
      })
      const exercise = await ready().json()
      const switchResponse = deferred<Response>()
      const attemptBody = deferred<unknown>()
      const result = {
        score: 5,
        xp_earned: replay ? 0 : 50,
        correct_answers: Array.from({ length: 5 }, (_, index) => ({
          index,
          correct: 'A',
        })),
        text: exercise.exercise.text,
      }
      let attemptSignal: AbortSignal | undefined
      let persisted = 0
      vi.mocked(fetch).mockImplementation(async (url, options) => {
        if (url === '/api/languages/active') return switchResponse.promise
        if (String(url).startsWith(`/api/${feature}/history`))
          return json({
            context: exercise.context,
            total: 1,
            items: [
              {
                id: 1,
                ...result,
                exercise: exercise.exercise,
                answers: {},
                completed_at: '2026-01-01',
              },
            ],
          })
        if (url === `/api/${feature}/attempt`) {
          persisted += 1
          attemptSignal = options!.signal as AbortSignal
          const response = json(result)
          vi.spyOn(response, 'json').mockReturnValue(attemptBody.promise)
          return response
        }
        if (String(url).startsWith('/api/reviews')) return json({})
        return json(exercise)
      })
      render(<Page />)
      await screen.findByText(/Fresh exercise/)
      if (replay) {
        fireEvent.click(screen.getByRole('button', { name: 'history' }))
        fireEvent.click(
          await screen.findByRole('button', { name: 'practiceAgain' })
        )
      }
      answerExercise()
      fireEvent.click(screen.getByRole('button', { name: 'submit' }))
      await waitFor(() => expect(persisted).toBe(1))
      let switching!: Promise<boolean>
      act(() => {
        switching = useLanguageStore.getState().switchLanguage('es-ES')
      })
      const submittingLabel = feature === 'reading' ? '...' : 'checking'
      expect(
        screen.getByRole('button', { name: submittingLabel })
      ).toBeDisabled()
      expect(attemptSignal?.aborted).not.toBe(true)
      if (timing === 'during') {
        await act(async () => attemptBody.resolve(result))
        expect(screen.queryByText('resultsLabel')).not.toBeInTheDocument()
        expect(
          screen.getByRole('button', { name: submittingLabel })
        ).toBeDisabled()
      }
      await act(async () => {
        switchResponse.resolve(json({ detail: 'Rejected' }, status))
        expect(await switching).toBe(false)
      })
      if (timing === 'after') {
        expect(
          screen.getByRole('button', { name: submittingLabel })
        ).toBeDisabled()
        fireEvent.click(screen.getByRole('button', { name: submittingLabel }))
        expect(persisted).toBe(1)
        await act(async () => attemptBody.resolve(result))
      }
      expect(await screen.findByText('resultsLabel')).toBeInTheDocument()
      expect(screen.getByText('5/5')).toBeInTheDocument()
      expect(screen.queryByText('alreadyAttempted')).not.toBeInTheDocument()
      expect(attemptSignal?.aborted).not.toBe(true)
      expect(persisted).toBe(1)
      const attempt = vi
        .mocked(fetch)
        .mock.calls.find(([url]) => url === `/api/${feature}/attempt`)!
      expect(JSON.parse(String(attempt[1]?.body))).toEqual({
        exercise_id: 42,
        replay,
        context: exercise.context,
        answers: { 0: 'A', 1: 'A', 2: 'A', 3: 'A', 4: 'A' },
      })
      expect(
        useFreemiumStore.getState().status?.[
          feature === 'reading' ? 'reading_remaining' : 'listening_remaining'
        ]
      ).toBe(4)
      expect(lookups()).toHaveLength(1)
      await waitFor(() => expect(useLoadingStore.getState().count).toBe(0))
    }
  )

  it.each([
    { status: 200, timing: 'during' },
    { status: 503, timing: 'during' },
    { status: 200, timing: 'after' },
    { status: 503, timing: 'after' },
  ])(
    'ignores an old attempt (HTTP $status, response $timing switch) without unlocking the replacement submission',
    async ({ status, timing }) => {
      useLanguageStore.setState({
        activeLanguage: getLanguageByCode('en-GB') ?? null,
        userLanguages: languages().languages,
      })
      let targetLanguage = 'en-GB'
      let planId = 8
      const attempts: {
        resolve: (response: Response) => void
        signal?: AbortSignal
      }[] = []
      vi.mocked(fetch).mockImplementation(async (url, options) => {
        if (url === `/api/${feature}/attempt`)
          return new Promise<Response>((resolve) => {
            attempts.push({ resolve, signal: options!.signal as AbortSignal })
          })
        const body = await ready().json()
        return json({
          ...body,
          context: {
            ...body.context,
            study_plan_id: planId,
            target_language: targetLanguage,
          },
          exercise: {
            ...body.exercise,
            id: planId,
            target_language: targetLanguage,
            topic:
              targetLanguage === 'en-GB'
                ? 'Fresh exercise'
                : 'Replacement exercise',
          },
        })
      })
      render(<Page />)
      await screen.findByText(/Fresh exercise/)
      answerExercise()
      fireEvent.click(screen.getByRole('button', { name: 'submit' }))
      await waitFor(() => expect(attempts).toHaveLength(1))
      act(() => useLanguageStore.setState({ isSwitching: true }))
      const result = {
        score: 0,
        xp_earned: 0,
        correct_answers: Array.from({ length: 5 }, (_, index) => ({
          index,
          correct: 'B',
        })),
        text: 'Transcript',
      }
      if (timing === 'during') {
        await act(async () => attempts[0].resolve(json(result, status)))
        expect(screen.queryByText('resultsLabel')).not.toBeInTheDocument()
        expect(screen.queryByText('errorSubmit')).not.toBeInTheDocument()
      }
      targetLanguage = 'de-DE'
      planId = 9
      act(() =>
        useLanguageStore.setState({
          isSwitching: false,
          activeLanguage: getLanguageByCode('de-DE') ?? null,
          userLanguages: [
            {
              target_language: 'de-DE',
              is_active: true,
              plan: plan(9),
              progress: null,
            },
          ],
        })
      )
      await screen.findByText(/Replacement exercise/)
      // Local presentation is cancelled, but the POST remains observed for quota.
      expect(attempts[0].signal?.aborted).not.toBe(true)
      answerExercise()
      fireEvent.click(screen.getByRole('button', { name: 'submit' }))
      await waitFor(() => expect(attempts).toHaveLength(2))
      if (timing === 'after')
        await act(async () => attempts[0].resolve(json(result, status)))
      expect(screen.queryByText('resultsLabel')).not.toBeInTheDocument()
      expect(screen.queryByText('errorSubmit')).not.toBeInTheDocument()
      expect(
        screen.getByRole('button', {
          name: feature === 'reading' ? '...' : 'checking',
        })
      ).toBeDisabled()
      await act(async () => attempts[1].resolve(json(result)))
      expect(await screen.findByText('resultsLabel')).toBeInTheDocument()
    }
  )
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
