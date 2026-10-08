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
  const promise = new Promise<T>((done) => {
    resolve = done
  })
  return { promise, resolve }
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
    stripeEnabled: false,
    maintenanceMode: false,
  })
  useLoadingStore.setState({ count: 0 })
})
afterEach(() => {
  cleanup()
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

describe('Assessment provisional language switches', () => {
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
