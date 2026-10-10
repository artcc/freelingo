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
import { useLanguageStore } from '@/store/language'
import { useAuthStore } from '@/store/auth'
import { useConfigStore } from '@/store/config'
import { useLoadingStore } from '@/store/loading'
import { getLanguageByCode } from '@/lib/target-languages'

const { push } = vi.hoisted(() => ({ push: vi.fn() }))
vi.mock('next/navigation', () => ({ useRouter: () => ({ push }) }))
vi.mock('next-intl', () => {
  const translate = (key: string) => key
  return { useTranslations: () => translate, useLocale: () => 'en' }
})

function deferred<T>() {
  let resolve!: (value: T) => void
  let reject!: (reason: unknown) => void
  const promise = new Promise<T>((done, fail) => {
    resolve = done
    reject = fail
  })
  return { promise, resolve, reject }
}
const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status })
const bank = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'].flatMap((difficulty) =>
  Array.from({ length: 15 }, (_, i) => ({
    id: `${difficulty}-${i}`,
    skill: 'grammar',
    difficulty,
    question: `Placement question ${difficulty}-${i}`,
    options: [
      'Correct answer',
      'Second answer',
      'Third answer',
      'Fourth answer',
    ],
    correct: 'Correct answer',
  }))
)
const evaluation = {
  cefr_level: 'B1',
  score: 1,
  skill_profile: { grammar: 1 },
  strengths: ['grammar'],
  weaknesses: [],
}
const summary = (active = 'en-GB') => ({
  languages: ['en-GB', 'de-DE'].map((target_language, index) => ({
    target_language,
    is_active: target_language === active,
    plan: {
      id: 8 + index,
      cefr_level: 'A1',
      progress_day: 0,
      total_days: 48,
      completion_pct: 0,
    },
    progress: null,
  })),
})

beforeEach(() => {
  push.mockReset()
  sessionStorage.clear()
  vi.stubGlobal('fetch', vi.fn())
  useAuthStore.getState().startSession('token')
  useLanguageStore.setState({
    activeLanguage: getLanguageByCode('en-GB') ?? null,
    userLanguages: summary().languages,
    needsRefresh: false,
    isSwitching: false,
  })
  useConfigStore.setState({
    loaded: true,
    analyticsEnabled: true,
    stripeEnabled: false,
    maintenanceMode: false,
  })
  useLoadingStore.setState({ count: 0 })
})
afterEach(() => {
  cleanup()
  useConfigStore.setState({ analyticsEnabled: false })
  vi.unstubAllGlobals()
  vi.useRealTimers()
})

async function startQuiz() {
  fireEvent.click(
    await screen.findByRole('button', { name: /hasExperienceOption/ })
  )
  fireEvent.click(screen.getByRole('button', { name: 'startWarningConfirm' }))
  await screen.findByText(/^Placement question /)
}

async function answerQuestions(count: number, finish = true) {
  for (let i = 0; i < count; i += 1) {
    const previous = screen.getByText(/^Placement question /).textContent
    fireEvent.click(screen.getByRole('button', { name: /Correct answer/ }))
    if (i < count - 1 || !finish) {
      await waitFor(() =>
        expect(screen.getByText(/^Placement question /).textContent).not.toBe(
          previous
        )
      )
    }
  }
}

describe('Assessment evaluation recovery', () => {
  const shortBank = bank.filter((q) => q.difficulty === 'A2').slice(0, 2)
  const evaluations = () =>
    vi
      .mocked(fetch)
      .mock.calls.filter(([url]) => url === '/api/assessment/evaluate')

  async function finishQuiz(count: number) {
    const expected = []
    for (let i = 0; i < count; i += 1) {
      const question = bank.find(
        (q) =>
          q.question === screen.getByText(/^Placement question /).textContent
      )!
      const last = i === count - 1
      expected.push({
        question_id: question.id,
        skill: question.skill,
        difficulty: question.difficulty,
        correct: !last,
        dont_know: last,
      })
      if (last)
        fireEvent.click(screen.getByRole('button', { name: 'dontKnow' }))
      else await answerQuestions(1, false)
    }
    return expected
  }

  it.each(
    ['limit', 'exhaustion'].flatMap((trigger) =>
      ['503', '429', 'transport', 'json'].map((failure) => ({
        trigger,
        failure,
      }))
    )
  )(
    'recovers $failure at $trigger with the exact answers and a single retry in flight',
    async ({ trigger, failure }) => {
      const body = deferred<unknown>()
      const response = json({})
      const readBody = vi.spyOn(response, 'json').mockReturnValue(body.promise)
      let attempts = 0
      vi.mocked(fetch).mockImplementation(async (url) => {
        if (url === '/api/study-plan/current') return json(null)
        if (String(url).startsWith('/api/assessment/bank'))
          return json({ questions: trigger === 'limit' ? bank : shortBank })
        if (url === '/api/assessment/evaluate') {
          attempts += 1
          if (attempts > 2) return response
          if (failure === 'transport')
            throw new TypeError('Network unavailable')
          if (failure === 'json') return new Response('unreadable json')
          return json({}, Number(failure))
        }
        return json({}, 404)
      })
      render(<AssessmentPage />)
      await startQuiz()
      const expected = await finishQuiz(trigger === 'limit' ? 15 : 2)
      expect(await screen.findByRole('alert')).toHaveTextContent('errorMessage')
      expect(screen.queryByRole('status')).not.toBeInTheDocument()
      expect(evaluations()).toHaveLength(1)
      expect(JSON.parse(String(evaluations()[0][1]?.body))).toEqual({
        answers: expected,
      })

      fireEvent.click(screen.getByRole('button', { name: 'retry' }))
      expect(await screen.findByRole('alert')).toHaveTextContent('errorMessage')
      expect(evaluations()).toHaveLength(2)
      const retry = screen.getByRole('button', { name: 'retry' })
      act(() => {
        fireEvent.click(retry)
        fireEvent.click(retry)
      })
      await waitFor(() => expect(readBody).toHaveBeenCalledTimes(1))
      expect(evaluations()).toHaveLength(3)
      expect(
        screen.getByRole('status', { name: 'evaluating' })
      ).toBeInTheDocument()
      expect(screen.queryByRole('alert')).not.toBeInTheDocument()
      expect(
        screen.queryByRole('button', { name: 'retry' })
      ).not.toBeInTheDocument()
      await act(async () => body.resolve(evaluation))
      expect(await screen.findByText('resultStep')).toBeInTheDocument()
      expect(screen.queryByText('errorMessage')).not.toBeInTheDocument()
      expect(evaluations().map(([, options]) => options?.body)).toEqual(
        Array(3).fill(JSON.stringify({ answers: expected }))
      )
      const start = vi
        .mocked(fetch)
        .mock.calls.find(([url]) => url === '/api/assessment/started')!
      const attempt = new Headers(start[1]?.headers).get('X-Assessment-Attempt')
      expect(attempt).toMatch(/^[0-9a-f-]{36}$/)
      expect(
        evaluations().map(([, options]) =>
          new Headers(options?.headers).get('X-Assessment-Attempt')
        )
      ).toEqual(Array(3).fill(attempt))
      // Evaluation recovery cannot reload the bank, reconcile plans, or complete.
      expect(vi.mocked(fetch).mock.calls.map(([url]) => url)).toEqual([
        '/api/study-plan/current',
        '/api/assessment/bank?language=en-GB',
        '/api/assessment/started',
        ...Array(3).fill('/api/assessment/evaluate'),
      ])
      expect(push).not.toHaveBeenCalled()
    }
  )

  it.each(
    [422, 429].flatMap((status) =>
      ['error', 'initial-failure', 'retry-success', 'retry-failure'].map(
        (stage) => ({
          status,
          stage,
        })
      )
    )
  )(
    'preserves $stage through a rejected $status switch',
    async ({ status, stage }) => {
      const change = deferred<Response>()
      const body = deferred<unknown>()
      const response = json({})
      const readBody = vi.spyOn(response, 'json').mockReturnValue(body.promise)
      let attempts = 0
      vi.mocked(fetch).mockImplementation(async (url) => {
        if (url === '/api/languages/active') return change.promise
        if (url === '/api/study-plan/current') return json(null)
        if (String(url).startsWith('/api/assessment/bank'))
          return json({ questions: shortBank })
        if (url === '/api/assessment/evaluate') {
          attempts += 1
          if (attempts === 1)
            return stage === 'initial-failure' ? response : json({}, 503)
          if (attempts === 2 && stage.startsWith('retry-')) return response
          return json(evaluation)
        }
        return json({}, 404)
      })
      render(<AssessmentPage />)
      await startQuiz()
      const expected = await finishQuiz(2)
      if (stage !== 'initial-failure') {
        await screen.findByRole('alert')
        if (stage !== 'error')
          fireEvent.click(screen.getByRole('button', { name: 'retry' }))
      }
      if (stage !== 'error')
        await waitFor(() => expect(readBody).toHaveBeenCalledTimes(1))
      const signal = evaluations().at(-1)![1]!.signal!
      let switching!: Promise<boolean>
      act(() => {
        switching = useLanguageStore.getState().switchLanguage('de-DE')
      })
      if (stage !== 'error') {
        await act(async () => {
          if (stage === 'retry-success') body.resolve(evaluation)
          else body.reject(new SyntaxError('Unreadable delayed body'))
        })
      }
      expect(
        screen.getByRole('status', { name: 'loading' })
      ).toBeInTheDocument()
      expect(screen.queryByRole('alert')).not.toBeInTheDocument()
      expect(
        screen.queryByRole('button', { name: 'retry' })
      ).not.toBeInTheDocument()
      expect(screen.queryByText('resultStep')).not.toBeInTheDocument()
      expect(signal.aborted).toBe(false)
      await act(async () => {
        change.resolve(json({}, status))
        expect(await switching).toBe(false)
      })
      if (stage !== 'retry-success') {
        expect(await screen.findByRole('alert')).toHaveTextContent(
          'errorMessage'
        )
        fireEvent.click(screen.getByRole('button', { name: 'retry' }))
      }
      expect(await screen.findByText('resultStep')).toBeInTheDocument()
      expect(screen.queryByText('errorMessage')).not.toBeInTheDocument()
      const count = stage === 'retry-failure' ? 3 : 2
      expect(evaluations().map(([, options]) => options?.body)).toEqual(
        Array(count).fill(JSON.stringify({ answers: expected }))
      )
      expect(
        vi
          .mocked(fetch)
          .mock.calls.filter(([url]) => url === '/api/study-plan/current')
      ).toHaveLength(1)
      expect(
        vi
          .mocked(fetch)
          .mock.calls.some(([url]) => url === '/api/assessment/complete')
      ).toBe(false)
      expect(push).not.toHaveBeenCalled()
    }
  )

  it.each(
    ['language', 'roundtrip', 'invalidation', 'session', 'unmount'].flatMap(
      (change) =>
        ['error', 'retry-success', 'retry-failure'].map((stage) => ({
          change,
          stage,
        }))
    )
  )(
    'discards $stage after $change without reviving it or unlocking a new evaluation',
    async ({ change, stage }) => {
      const oldBody = deferred<unknown>()
      const oldResponse = json({})
      const readOldBody = vi
        .spyOn(oldResponse, 'json')
        .mockReturnValue(oldBody.promise)
      const newBody = deferred<unknown>()
      const newResponse = json({})
      const readNewBody = vi
        .spyOn(newResponse, 'json')
        .mockReturnValue(newBody.promise)
      let active = 'en-GB'
      let replaced = false
      let attempts = 0
      vi.mocked(fetch).mockImplementation(async (url, options) => {
        if (url === '/api/languages/active') {
          active = JSON.parse(String(options?.body)).target_language
          return json({})
        }
        if (url === '/api/languages') return json(summary(active))
        if (url === '/api/study-plan/current') return json(null)
        if (String(url).startsWith('/api/assessment/bank'))
          return json({ questions: shortBank.slice(0, 1) })
        if (url === '/api/assessment/evaluate') {
          attempts += 1
          if (replaced) return newResponse
          return attempts === 1 ? json({}, 503) : oldResponse
        }
        return json({}, 404)
      })
      const { unmount } = render(<AssessmentPage />)
      await startQuiz()
      await finishQuiz(1)
      await screen.findByRole('alert')
      if (stage !== 'error') {
        fireEvent.click(screen.getByRole('button', { name: 'retry' }))
        await waitFor(() => expect(readOldBody).toHaveBeenCalledTimes(1))
      }
      const oldSignal = evaluations().at(-1)![1]!.signal!
      const oldCount = evaluations().length
      replaced = true
      if (change === 'unmount') {
        unmount()
        render(<AssessmentPage />)
      } else {
        await act(async () => {
          if (change === 'session')
            useAuthStore.getState().startSession('replacement-session')
          else if (change === 'invalidation')
            useLanguageStore.getState().invalidateLanguages()
          else
            expect(
              await useLanguageStore.getState().switchLanguage('de-DE')
            ).toBe(true)
        })
      }
      await screen.findByRole('button', { name: /beginnerOption/ })
      if (change === 'roundtrip') {
        await act(async () =>
          expect(
            await useLanguageStore.getState().switchLanguage('en-GB')
          ).toBe(true)
        )
        await screen.findByRole('button', { name: /beginnerOption/ })
      }
      expect(oldSignal.aborted).toBe(true)
      expect(evaluations()).toHaveLength(oldCount)
      expect(screen.queryByRole('alert')).not.toBeInTheDocument()
      expect(
        screen.queryByRole('button', { name: 'retry' })
      ).not.toBeInTheDocument()

      await startQuiz()
      await answerQuestions(1)
      await waitFor(() => expect(readNewBody).toHaveBeenCalledTimes(1))
      expect(
        new Headers(evaluations().at(-1)![1]?.headers).get(
          'X-Assessment-Attempt'
        )
      ).not.toBe(
        new Headers(evaluations()[0][1]?.headers).get('X-Assessment-Attempt')
      )
      // Resolve an obsolete body while a replacement flow owns its own request.
      if (stage !== 'error') {
        await act(async () => {
          if (stage === 'retry-success')
            oldBody.resolve({ ...evaluation, cefr_level: 'C2' })
          else oldBody.reject(new SyntaxError('Obsolete body'))
        })
      }
      expect(
        screen.getByRole('status', { name: 'evaluating' })
      ).toBeInTheDocument()
      expect(screen.queryByText('resultStep')).not.toBeInTheDocument()
      expect(screen.queryByRole('alert')).not.toBeInTheDocument()
      expect(
        screen.queryByRole('button', { name: 'retry' })
      ).not.toBeInTheDocument()
      expect(evaluations()).toHaveLength(oldCount + 1)
      expect(
        JSON.parse(String(evaluations().at(-1)![1]?.body)).answers
      ).toEqual([
        {
          question_id: shortBank[0].id,
          skill: 'grammar',
          difficulty: 'A2',
          correct: true,
          dont_know: false,
        },
      ])
      await act(async () => newBody.resolve(evaluation))
      expect(await screen.findByText('resultStep')).toBeInTheDocument()
      expect(screen.getByRole('button', { name: 'B1' })).toHaveClass(
        'border-fl-accent'
      )
      expect(
        vi
          .mocked(fetch)
          .mock.calls.some(([url]) => url === '/api/assessment/complete')
      ).toBe(false)
      expect(push).not.toHaveBeenCalled()
    }
  )
})

describe('Assessment start analytics', () => {
  it.each(['disabled', 're-enabled', 'disabled-during-evaluation'])(
    'cancels pending telemetry without interrupting assessment when %s',
    async (state) => {
      const pendingEvaluation = deferred<Response>()
      vi.mocked(fetch).mockImplementation(async (url, options) => {
        if (url === '/api/study-plan/current') return json(null)
        if (String(url).startsWith('/api/assessment/bank'))
          return json({
            questions: bank.filter((q) => q.difficulty === 'A2').slice(0, 1),
          })
        if (url === '/api/assessment/started') {
          const signal = options!.signal!
          return new Promise<Response>((_resolve, reject) => {
            signal.throwIfAborted()
            signal.addEventListener('abort', () => reject(signal.reason), {
              once: true,
            })
          })
        }
        if (url === '/api/assessment/evaluate') return pendingEvaluation.promise
        return json({}, 404)
      })
      const evaluations = () =>
        vi
          .mocked(fetch)
          .mock.calls.filter(([url]) => url === '/api/assessment/evaluate')
      render(<AssessmentPage />)
      await startQuiz()
      const start = vi
        .mocked(fetch)
        .mock.calls.find(([url]) => url === '/api/assessment/started')!
      expect(start[1]?.signal?.aborted).toBe(false)

      if (state === 'disabled-during-evaluation') {
        await answerQuestions(1)
        await waitFor(() => expect(evaluations()).toHaveLength(1))
      }
      act(() => {
        useConfigStore.setState({ analyticsEnabled: false })
        // A quick reactivation must not resurrect the previous operation UUID.
        if (state === 're-enabled')
          useConfigStore.setState({ analyticsEnabled: true })
      })
      expect(start[1]?.signal?.aborted).toBe(true)
      if (state !== 'disabled-during-evaluation') await answerQuestions(1)
      await waitFor(() => expect(evaluations()).toHaveLength(1))
      const submission = evaluations()[0][1]!
      expect(submission.signal?.aborted).toBe(false)
      expect(new Headers(submission.headers).has('X-Assessment-Attempt')).toBe(
        state === 'disabled-during-evaluation'
      )
      expect(JSON.parse(String(submission.body)).answers).toHaveLength(1)
      await act(async () => pendingEvaluation.resolve(json(evaluation)))
      expect(await screen.findByText('resultStep')).toBeInTheDocument()
      expect(submission.signal?.aborted).toBe(false)
      expect(
        vi
          .mocked(fetch)
          .mock.calls.filter(([url]) => url === '/api/assessment/started')
      ).toHaveLength(1)
    }
  )

  it.each(['disabled', 'pending', 'invalid', 'disabled-after-start'])(
    'finishes assessment with no analytics header when config is %s',
    async (state) => {
      const active = state === 'disabled-after-start'
      useConfigStore.setState({
        loaded: state !== 'pending' && state !== 'invalid',
        analyticsEnabled: active,
      })
      const pending = deferred<Response>()
      vi.mocked(fetch).mockImplementation(async (url) => {
        if (url === '/api/config')
          return state === 'pending'
            ? pending.promise
            : new Response('invalid JSON')
        if (url === '/api/study-plan/current') return json(null)
        if (String(url).startsWith('/api/assessment/bank'))
          return json({
            questions: bank.filter((q) => q.difficulty === 'A2').slice(0, 1),
          })
        if (url === '/api/assessment/started')
          return new Response(null, { status: 204 })
        if (url === '/api/assessment/evaluate') return json(evaluation)
        return json({}, 404)
      })
      const uuid = vi.spyOn(crypto, 'randomUUID')
      render(<AssessmentPage />)
      await startQuiz()
      if (active)
        act(() => useConfigStore.setState({ analyticsEnabled: false }))
      await answerQuestions(1)
      expect(await screen.findByText('resultStep')).toBeInTheDocument()
      const starts = vi
        .mocked(fetch)
        .mock.calls.filter(([url]) => url === '/api/assessment/started')
      expect(starts).toHaveLength(active ? 1 : 0)
      if (!active) expect(uuid).not.toHaveBeenCalled()
      const submission = vi
        .mocked(fetch)
        .mock.calls.find(([url]) => url === '/api/assessment/evaluate')!
      expect(
        new Headers(submission[1]?.headers).has('X-Assessment-Attempt')
      ).toBe(false)
      expect(JSON.parse(String(submission[1]?.body)).answers).toHaveLength(1)
      await act(async () => pending.resolve(json({ analytics_enabled: false })))
    }
  )

  it.each(['401', '503', 'transport'])(
    'starts the quiz despite a %s analytics failure without refreshing auth',
    async (failure) => {
      vi.mocked(fetch).mockImplementation(async (url) => {
        if (url === '/api/study-plan/current') return json(null)
        if (String(url).startsWith('/api/assessment/bank'))
          return json({ questions: bank })
        if (url === '/api/assessment/started') {
          if (failure === 'transport') throw new TypeError('Unavailable')
          return json({}, Number(failure))
        }
        return json({}, 404)
      })
      render(<AssessmentPage />)
      await screen.findByRole('button', { name: /beginnerOption/ })
      expect(
        vi
          .mocked(fetch)
          .mock.calls.some(([url]) => url === '/api/assessment/started')
      ).toBe(false)
      await startQuiz()
      expect(screen.getByText(/^Placement question /)).toBeInTheDocument()
      const calls = vi.mocked(fetch).mock.calls
      const signals = calls.filter(([url]) => url === '/api/assessment/started')
      expect(signals).toHaveLength(1)
      expect(signals[0][1]?.body).toBeUndefined()
      expect(new Headers(signals[0][1]?.headers).get('Authorization')).toBe(
        'Bearer token'
      )
      expect(calls.some(([url]) => String(url).includes('/auth/refresh'))).toBe(
        false
      )
      expect(useAuthStore.getState().accessToken).toBe('token')
    }
  )

  it('does not count the beginner shortcut as a started quiz', async () => {
    vi.mocked(fetch).mockImplementation(async (url) => {
      if (url === '/api/study-plan/current') return json(null)
      if (String(url).startsWith('/api/assessment/bank'))
        return json({ questions: bank })
      return json({}, 404)
    })
    render(<AssessmentPage />)
    fireEvent.click(
      await screen.findByRole('button', { name: /beginnerOption/ })
    )
    expect(
      await screen.findByRole('button', { name: /startMyPlan/ })
    ).toBeInTheDocument()
    expect(
      vi
        .mocked(fetch)
        .mock.calls.some(([url]) => url === '/api/assessment/started')
    ).toBe(false)
  })
})

describe('Assessment provisional language switches', () => {
  it.each(['headers', 'body', 'summary'])(
    'does not reconcile a completion into a replacement session during %s',
    async (stage) => {
      const headers = deferred<Response>()
      const body = deferred<unknown>()
      const languages = deferred<Response>()
      const response = json({})
      const readBody = vi.spyOn(response, 'json').mockReturnValue(body.promise)
      let summaryCalls = 0
      vi.mocked(fetch).mockImplementation(async (url) => {
        if (url === '/api/study-plan/current') return json(null)
        if (String(url).startsWith('/api/assessment/bank'))
          return json({ questions: bank })
        if (url === '/api/assessment/complete') return headers.promise
        if (url === '/api/languages') {
          summaryCalls += 1
          return languages.promise
        }
        return json({}, 404)
      })
      const { unmount } = render(<AssessmentPage />)
      fireEvent.click(
        await screen.findByRole('button', { name: /beginnerOption/ })
      )
      fireEvent.click(screen.getByRole('button', { name: /startMyPlan/ }))
      await waitFor(() =>
        expect(
          vi
            .mocked(fetch)
            .mock.calls.some(([url]) => url === '/api/assessment/complete')
        ).toBe(true)
      )
      if (stage !== 'headers') {
        await act(async () => headers.resolve(response))
        await waitFor(() => expect(readBody).toHaveBeenCalled())
      }
      if (stage === 'summary')
        await act(async () => body.resolve({ plan_id: 99, cefr_level: 'A1' }))
      unmount()
      useAuthStore.getState().startSession('replacement-session')
      const replacement = summary('de-DE')
      replacement.languages[1].plan.id = 200
      useLanguageStore.setState({
        activeLanguage: getLanguageByCode('de-DE') ?? null,
        userLanguages: replacement.languages,
        needsRefresh: false,
      })
      const version = useLanguageStore.getState().invalidationVersion
      const old = summary()
      old.languages[0].plan.id = 99
      await act(async () => {
        headers.resolve(response)
        body.resolve({
          plan_id: 99,
          cefr_level: 'A1',
          voice_trial: { available: true, token: 'old-trial' },
        })
        languages.resolve(json(old))
      })
      expect(summaryCalls).toBe(stage === 'headers' ? 0 : 1)
      expect(useLanguageStore.getState()).toMatchObject({
        userLanguages: replacement.languages,
        needsRefresh: false,
        invalidationVersion: version,
      })
      expect(push).not.toHaveBeenCalled()
      expect(sessionStorage.getItem('assessment_voice_trial')).toBeNull()
    }
  )

  it('reconciles an abandoned completion after a confirmed language switch without restoring its offer', async () => {
    const completion = deferred<Response>()
    let active = 'en-GB'
    let planId = 8
    vi.mocked(fetch).mockImplementation(async (url) => {
      if (url === '/api/study-plan/current') return json(null)
      if (String(url).startsWith('/api/assessment/bank'))
        return json({ questions: bank })
      if (url === '/api/assessment/complete') return completion.promise
      if (url === '/api/languages/active') {
        active = 'de-DE'
        return json({})
      }
      if (url === '/api/languages') {
        const data = summary(active)
        data.languages[0].plan.id = planId
        return json(data)
      }
      return json({}, 404)
    })
    render(<AssessmentPage />)
    fireEvent.click(
      await screen.findByRole('button', { name: /beginnerOption/ })
    )
    fireEvent.click(screen.getByRole('button', { name: /startMyPlan/ }))
    await act(async () =>
      expect(await useLanguageStore.getState().switchLanguage('de-DE')).toBe(
        true
      )
    )
    await screen.findByRole('button', { name: /beginnerOption/ })
    await act(async () => {
      planId = 99
      completion.resolve(
        json({
          plan_id: 99,
          cefr_level: 'A1',
          voice_trial: { available: true, token: 'old-trial' },
        })
      )
    })
    await waitFor(() =>
      expect(useLanguageStore.getState().userLanguages[0].plan?.id).toBe(99)
    )
    expect(useLanguageStore.getState()).toMatchObject({
      activeLanguage: { code: 'de-DE' },
      needsRefresh: false,
    })
    expect(
      await screen.findByRole('button', { name: /beginnerOption/ })
    ).toBeInTheDocument()
    expect(screen.queryByText('voiceTrialTitle')).not.toBeInTheDocument()
    expect(push).not.toHaveBeenCalled()
  })

  it('recovers a committed plan with an unreadable completion body without another POST', async () => {
    let committed = false
    vi.mocked(fetch).mockImplementation(async (url) => {
      if (url === '/api/study-plan/current')
        return json(
          committed ? { cefr_level: 'B2', created_at: '2026-01-01' } : null
        )
      if (String(url).startsWith('/api/assessment/bank'))
        return json({ questions: bank })
      if (url === '/api/assessment/complete') {
        committed = true
        return new Response('invalid json')
      }
      if (url === '/api/languages') {
        const data = summary()
        data.languages[0].plan.id = 99
        data.languages[0].plan.cefr_level = 'B2'
        return json(data)
      }
      return json({}, 404)
    })
    render(<AssessmentPage />)
    fireEvent.click(
      await screen.findByRole('button', { name: /beginnerOption/ })
    )
    fireEvent.click(screen.getByRole('button', { name: /startMyPlan/ }))
    expect(
      await screen.findByRole('button', { name: 'retake' })
    ).toBeInTheDocument()
    expect(screen.getByText('B2')).toBeInTheDocument()
    expect(useLanguageStore.getState().userLanguages[0].plan?.id).toBe(99)
    expect(
      vi
        .mocked(fetch)
        .mock.calls.filter(([url]) => url === '/api/assessment/complete')
    ).toHaveLength(1)
    expect(push).not.toHaveBeenCalled()
  })

  it('keeps the current summary after a definite completion rejection', async () => {
    const rejection = deferred<Response>()
    vi.mocked(fetch).mockImplementation(async (url) => {
      if (url === '/api/study-plan/current') return json(null)
      if (String(url).startsWith('/api/assessment/bank'))
        return json({ questions: bank })
      if (url === '/api/assessment/complete') return rejection.promise
      return json({}, 422)
    })
    const version = useLanguageStore.getState().invalidationVersion
    render(<AssessmentPage />)
    fireEvent.click(
      await screen.findByRole('button', { name: /beginnerOption/ })
    )
    fireEvent.click(screen.getByRole('button', { name: /startMyPlan/ }))
    expect(screen.getByRole('button', { name: 'buildingPlan' })).toBeDisabled()
    await act(async () => rejection.resolve(json({}, 422)))
    expect(
      await screen.findByRole('button', { name: /startMyPlan/ })
    ).toBeEnabled()
    expect(useLanguageStore.getState()).toMatchObject({
      userLanguages: summary().languages,
      needsRefresh: false,
      invalidationVersion: version,
    })
    expect(
      vi
        .mocked(fetch)
        .mock.calls.filter(([url]) => url === '/api/assessment/complete')
    ).toHaveLength(1)
    expect(
      vi.mocked(fetch).mock.calls.some(([url]) => url === '/api/languages')
    ).toBe(false)
    expect(push).not.toHaveBeenCalled()
  })

  it.each([
    { stage: 'offer', voiceOffer: true, uncertain: false },
    { stage: 'offer', voiceOffer: true, uncertain: true },
    { stage: 'reconciling', voiceOffer: true, uncertain: false },
    { stage: 'reconciling', voiceOffer: false, uncertain: false },
  ])(
    'recovers an external invalidation without repeating completion ($stage, voice: $voiceOffer, uncertain: $uncertain)',
    async ({ stage, voiceOffer, uncertain }) => {
      let active = 'en-GB'
      let recover = false
      let summaryCalls = 0
      const oldSummary = deferred<Response>()
      vi.mocked(fetch).mockImplementation(async (url) => {
        if (url === '/api/languages/active') {
          active = 'de-DE'
          if (uncertain) throw new TypeError('Lost switch response')
          return json({})
        }
        if (url === '/api/languages') {
          summaryCalls += 1
          if (summaryCalls === 1)
            return stage === 'reconciling'
              ? oldSummary.promise
              : json(summary())
          return recover ? json(summary(active)) : json({}, 503)
        }
        if (url === '/api/study-plan/current')
          return json(
            active === 'en-GB'
              ? null
              : { cefr_level: 'B2', created_at: '2026-01-01' }
          )
        if (String(url).startsWith('/api/assessment/bank'))
          return json({ questions: bank })
        if (url === '/api/assessment/complete')
          return json({
            plan_id: 8,
            cefr_level: 'A1',
            voice_trial: {
              available: voiceOffer,
              token: voiceOffer ? 'old-trial' : null,
            },
          })
        return json({}, 404)
      })
      render(<AssessmentPage />)
      fireEvent.click(
        await screen.findByRole('button', { name: /beginnerOption/ })
      )
      fireEvent.click(screen.getByRole('button', { name: /startMyPlan/ }))
      await waitFor(() => expect(summaryCalls).toBe(1))
      if (stage === 'offer') await screen.findByText('voiceTrialTitle')
      const completionVersion = useLanguageStore.getState().invalidationVersion
      await act(async () =>
        expect(await useLanguageStore.getState().switchLanguage('de-DE')).toBe(
          false
        )
      )
      expect(useLanguageStore.getState()).toMatchObject({
        needsRefresh: true,
        activeLanguage: { code: 'en-GB' },
      })
      expect(useLanguageStore.getState().invalidationVersion).toBeGreaterThan(
        completionVersion
      )
      expect(await screen.findByRole('alert')).toHaveTextContent('errorMessage')
      if (stage === 'reconciling')
        await act(async () => oldSummary.resolve(json(summary())))
      expect(screen.queryByText('voiceTrialTitle')).not.toBeInTheDocument()
      expect(
        screen.queryByRole('button', { name: /voiceTrialStart/ })
      ).not.toBeInTheDocument()
      expect(push).not.toHaveBeenCalled()
      expect(sessionStorage.getItem('assessment_voice_trial')).toBeNull()
      recover = true
      fireEvent.click(screen.getByRole('button', { name: 'retry' }))
      expect(await screen.findByText('B2')).toBeInTheDocument()
      expect(useLanguageStore.getState()).toMatchObject({
        needsRefresh: false,
        activeLanguage: { code: 'de-DE' },
      })
      expect(screen.queryByText('voiceTrialTitle')).not.toBeInTheDocument()
      expect(
        vi
          .mocked(fetch)
          .mock.calls.filter(([url]) => url === '/api/assessment/complete')
      ).toHaveLength(1)
      expect(
        vi
          .mocked(fetch)
          .mock.calls.filter(([url]) => url === '/api/languages/active')
      ).toHaveLength(1)
    }
  )

  it('recovers its own failed summary before enabling the committed voice offer', async () => {
    let recover = false
    vi.mocked(fetch).mockImplementation(async (url) => {
      if (url === '/api/study-plan/current') return json(null)
      if (String(url).startsWith('/api/assessment/bank'))
        return json({ questions: bank })
      if (url === '/api/languages')
        return recover ? json(summary()) : json({}, 503)
      if (url === '/api/assessment/complete')
        return json({
          plan_id: 8,
          cefr_level: 'A1',
          voice_trial: {
            available: true,
            token: 'trial',
            duration_seconds: 300,
          },
        })
      return json({}, 404)
    })
    render(<AssessmentPage />)
    fireEvent.click(
      await screen.findByRole('button', { name: /beginnerOption/ })
    )
    fireEvent.click(screen.getByRole('button', { name: /startMyPlan/ }))
    expect(await screen.findByRole('alert')).toHaveTextContent('errorMessage')
    expect(
      screen.queryByRole('button', { name: /voiceTrialStart/ })
    ).not.toBeInTheDocument()
    recover = true
    fireEvent.click(screen.getByRole('button', { name: 'retry' }))
    fireEvent.click(
      await screen.findByRole('button', { name: /voiceTrialStart/ })
    )
    expect(push).toHaveBeenCalledWith('/conversation')
    expect(
      JSON.parse(sessionStorage.getItem('assessment_voice_trial')!)
    ).toMatchObject({ token: 'trial', planId: 8, targetLanguage: 'en-GB' })
    expect(
      vi
        .mocked(fetch)
        .mock.calls.filter(([url]) => url === '/api/assessment/complete')
    ).toHaveLength(1)
  })

  it('resumes the next-question timer after a rejected switch', async () => {
    const change = deferred<Response>()
    vi.mocked(fetch).mockImplementation(async (url) => {
      if (url === '/api/languages/active') return change.promise
      if (url === '/api/study-plan/current') return json(null)
      return json({ questions: bank })
    })
    render(<AssessmentPage />)
    await startQuiz()
    vi.useFakeTimers()
    const first = screen.getByText(/^Placement question /).textContent!
    fireEvent.click(screen.getByRole('button', { name: /Correct answer/ }))
    let switching!: Promise<boolean>
    act(() => {
      switching = useLanguageStore.getState().switchLanguage('de-DE')
    })
    await act(async () => {
      await vi.advanceTimersByTimeAsync(150)
    })
    expect(screen.queryByText(/^Placement question /)).not.toBeInTheDocument()
    await act(async () => {
      change.resolve(json({}, 422))
      expect(await switching).toBe(false)
    })
    expect(screen.getByText(/^Placement question /).textContent).not.toBe(first)
    expect(
      vi
        .mocked(fetch)
        .mock.calls.filter(([url]) => url === '/api/study-plan/current')
    ).toHaveLength(1)
  })

  it.each([
    { stage: 'quiz', status: 422 },
    { stage: 'quiz', status: 429 },
    { stage: 'result', status: 422 },
    { stage: 'result', status: 429 },
  ])(
    'preserves $stage through a rejected $status switch',
    async ({ stage, status }) => {
      const change = deferred<Response>()
      vi.mocked(fetch).mockImplementation(async (url) => {
        if (url === '/api/languages/active') return change.promise
        if (url === '/api/study-plan/current') return json(null)
        if (String(url).startsWith('/api/assessment/bank'))
          return json({ questions: bank })
        if (url === '/api/assessment/evaluate') return json(evaluation)
        if (url === '/api/assessment/complete')
          return json({ plan_id: 8, cefr_level: 'B2' })
        if (url === '/api/languages') return json(summary())
        return json({}, 404)
      })
      render(<AssessmentPage />)
      await startQuiz()
      const firstId = screen
        .getByText(/^Placement question /)
        .textContent!.replace('Placement question ', '')
      await answerQuestions(stage === 'quiz' ? 1 : 15, stage !== 'quiz')
      const question =
        stage === 'quiz'
          ? screen.getByText(/^Placement question /).textContent
          : null
      if (stage === 'result') {
        await screen.findByText('resultStep')
        fireEvent.click(screen.getByRole('button', { name: 'B2' }))
      }
      let switching!: Promise<boolean>
      act(() => {
        switching = useLanguageStore.getState().switchLanguage('de-DE')
      })
      expect(screen.queryByText(/^Placement question /)).not.toBeInTheDocument()
      expect(screen.queryByText('resultStep')).not.toBeInTheDocument()
      await act(async () => {
        change.resolve(json({ detail: 'Rejected' }, status))
        expect(await switching).toBe(false)
      })
      if (stage === 'quiz') {
        expect(await screen.findByText(question!)).toBeInTheDocument()
        await answerQuestions(14)
        await screen.findByText('resultStep')
        fireEvent.click(screen.getByRole('button', { name: 'B2' }))
      } else {
        expect(await screen.findByText('resultStep')).toBeInTheDocument()
        expect(screen.getByRole('button', { name: 'B2' })).toHaveClass(
          'border-fl-accent'
        )
      }
      const evaluations = vi
        .mocked(fetch)
        .mock.calls.filter(([url]) => url === '/api/assessment/evaluate')
      expect(evaluations).toHaveLength(1)
      const { answers } = JSON.parse(String(evaluations[0][1]?.body))
      expect(answers).toHaveLength(15)
      expect(answers[0]).toMatchObject({ question_id: firstId, correct: true })
      expect(
        vi
          .mocked(fetch)
          .mock.calls.filter(([url]) => url === '/api/study-plan/current')
      ).toHaveLength(1)
      fireEvent.click(screen.getByRole('button', { name: /createPlan/ }))
      fireEvent.click(screen.getByRole('button', { name: /startMyPlan/ }))
      await waitFor(() => expect(push).toHaveBeenCalledWith('/plan'))
      const complete = vi
        .mocked(fetch)
        .mock.calls.filter(([url]) => url === '/api/assessment/complete')
      expect(complete).toHaveLength(1)
      expect(JSON.parse(String(complete[0][1]?.body))).toMatchObject({
        cefr_level: 'B2',
        target_language: 'en-GB',
      })
    }
  )

  it.each(['evaluate', 'complete'])(
    'retains a /%s response received during a rejected switch',
    async (operation) => {
      const change = deferred<Response>()
      const body = deferred<unknown>()
      const response = json({})
      const readBody = vi.spyOn(response, 'json').mockReturnValue(body.promise)
      vi.mocked(fetch).mockImplementation(async (url) => {
        if (url === '/api/languages/active') return change.promise
        if (url === '/api/study-plan/current') return json(null)
        if (String(url).startsWith('/api/assessment/bank'))
          return json({ questions: bank })
        if (url === `/api/assessment/${operation}`) return response
        if (url === '/api/languages') return json(summary())
        return json({}, 404)
      })
      render(<AssessmentPage />)
      if (operation === 'evaluate') {
        await startQuiz()
        await answerQuestions(15)
      } else {
        fireEvent.click(
          await screen.findByRole('button', { name: /beginnerOption/ })
        )
        fireEvent.click(screen.getByRole('button', { name: /startMyPlan/ }))
      }
      await waitFor(() => expect(readBody).toHaveBeenCalledTimes(1))
      let switching!: Promise<boolean>
      act(() => {
        switching = useLanguageStore.getState().switchLanguage('de-DE')
      })
      await act(async () =>
        body.resolve(
          operation === 'evaluate'
            ? evaluation
            : {
                plan_id: 8,
                cefr_level: 'A1',
                voice_trial: {
                  available: true,
                  token: 'trial',
                  duration_seconds: 300,
                },
              }
        )
      )
      expect(screen.queryByText('resultStep')).not.toBeInTheDocument()
      expect(screen.queryByText('voiceTrialTitle')).not.toBeInTheDocument()
      await act(async () => {
        change.resolve(json({}, 429))
        expect(await switching).toBe(false)
      })
      expect(
        await screen.findByText(
          operation === 'evaluate' ? 'resultStep' : 'voiceTrialTitle'
        )
      ).toBeInTheDocument()
      expect(
        vi
          .mocked(fetch)
          .mock.calls.filter(([url]) => url === `/api/assessment/${operation}`)
      ).toHaveLength(1)
      expect(push).not.toHaveBeenCalled()
    }
  )

  it.each([false, true])(
    'discards old completion after A → B → A (voice offer: %s)',
    async (voiceOffer) => {
      const oldSummary = deferred<Response>()
      let summaryCalls = 0
      let active = 'en-GB'
      vi.mocked(fetch).mockImplementation(async (url, options) => {
        if (url === '/api/languages/active') {
          active = JSON.parse(String(options?.body)).target_language
          return json({})
        }
        if (url === '/api/languages')
          return ++summaryCalls === 1
            ? oldSummary.promise
            : json(summary(active))
        if (url === '/api/study-plan/current') return json(null)
        if (String(url).startsWith('/api/assessment/bank'))
          return json({ questions: bank })
        if (url === '/api/assessment/complete')
          return json({
            plan_id: 8,
            cefr_level: 'A1',
            voice_trial: {
              available: voiceOffer,
              token: voiceOffer ? 'old-trial' : null,
            },
          })
        return json({}, 404)
      })
      render(<AssessmentPage />)
      fireEvent.click(
        await screen.findByRole('button', { name: /beginnerOption/ })
      )
      fireEvent.click(screen.getByRole('button', { name: /startMyPlan/ }))
      await waitFor(() => expect(summaryCalls).toBe(1))
      await act(async () =>
        expect(await useLanguageStore.getState().switchLanguage('de-DE')).toBe(
          true
        )
      )
      await screen.findByRole('button', { name: /beginnerOption/ })
      await act(async () =>
        expect(await useLanguageStore.getState().switchLanguage('en-GB')).toBe(
          true
        )
      )
      fireEvent.click(
        await screen.findByRole('button', { name: /hasExperienceOption/ })
      )
      fireEvent.click(
        screen.getByRole('button', { name: 'startWarningConfirm' })
      )
      const question = screen.getByText(/^Placement question /).textContent!
      await act(async () => oldSummary.resolve(json(summary())))
      expect(screen.getByText(question)).toBeInTheDocument()
      expect(screen.queryByText('voiceTrialTitle')).not.toBeInTheDocument()
      expect(push).not.toHaveBeenCalled()
      expect(
        vi
          .mocked(fetch)
          .mock.calls.filter(([url]) => url === '/api/assessment/complete')
      ).toHaveLength(1)
    }
  )
})
