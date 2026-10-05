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
import { getLanguageByCode } from '@/lib/target-languages'
import { useAuthStore } from '@/store/auth'
import { useConfigStore } from '@/store/config'
import { useLanguageStore } from '@/store/language'
import { useLoadingStore } from '@/store/loading'

const { push } = vi.hoisted(() => ({ push: vi.fn() }))

vi.mock('next/navigation', () => ({ useRouter: () => ({ push }) }))
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
      expect(useLoadingStore.getState().count).toBe(0)

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

  it('aborts context loading on unmount', async () => {
    let signal: AbortSignal | null | undefined
    vi.mocked(fetch).mockImplementationOnce(
      (_url, options) =>
        new Promise((_resolve, reject) => {
          signal = options?.signal
          signal?.addEventListener('abort', () => reject(signal?.reason), {
            once: true,
          })
        })
    )
    const { unmount } = render(<Page />)
    unmount()
    await waitFor(() => expect(useLoadingStore.getState().count).toBe(0))
    expect(signal?.aborted).toBe(true)
    expect(lookups()).toHaveLength(0)
  })

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
