import {
  act,
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { SituationsCatalog } from '@/components/situations/SituationsCatalog'
import ConversationPage from '@/app/(app)/conversation/page'
import { apiFetch } from '@/lib/api'
import { situationCategories } from '@/lib/situations'
import { getLanguageByCode } from '@/lib/target-languages'
import { mapUser } from '@/lib/mappers'
import { useAuthStore } from '@/store/auth'
import { useLanguageStore } from '@/store/language'
import { useConfigStore } from '@/store/config'
import { useFreemiumStore } from '@/store/freemium'

const mocks = vi.hoisted(() => ({
  query: '',
  push: vi.fn(),
  voice: vi.fn(),
}))

vi.mock('next/navigation', () => ({
  useRouter: () => ({ push: mocks.push }),
  useSearchParams: () => new URLSearchParams(mocks.query),
}))
vi.mock('next/dynamic', () => ({ default: () => mocks.voice }))
vi.mock('next-intl', () => {
  const labels: Record<string, string> = {
    'categories.daily_life': 'Daily life',
    'categories.travel': 'Travel',
    'categories.shopping_services': 'Shopping',
    'categories.social': 'Social',
    'categories.work': 'Work',
    'items.hotel_problem.title': 'A hotel problem',
    'items.ask_directions.title': 'Finding your way',
    'items.hotel_problem.description': 'Explain a noisy room',
  }
  const translate = (key: string) => labels[key] ?? key
  return { useTranslations: () => translate, useLocale: () => 'en' }
})
vi.mock('@/lib/api', () => ({ apiFetch: vi.fn() }))
vi.mock('@/components/billing/MaintenanceBanner', () => ({
  MaintenanceGate: ({ children }: { children: React.ReactNode }) => children,
}))
vi.mock('@/components/billing/FreemiumQuotaBanner', () => ({
  FreemiumQuotaBanner: () => null,
}))
vi.mock('@/components/billing/PaywallBanner', () => ({
  PaywallBanner: ({ feature }: { feature: string }) => (
    <div data-testid="paywall">{feature}</div>
  ),
}))
vi.mock('@/components/plan/NoPlanBanner', () => ({
  default: () => <a href="/assessment">no-plan</a>,
}))
vi.mock('@/components/ui/page-loading', () => ({
  PageLoading: () => <div>loading</div>,
}))

const plan = {
  id: 7,
  cefr_level: 'B1',
  progress_day: 1,
  total_days: 30,
  completion_pct: 0,
}
const language = {
  target_language: 'fr-FR',
  is_active: true,
  plan,
  progress: null,
}
const catalog = {
  study_plan_id: 7,
  target_language: 'fr-FR',
  cefr_level: 'B1',
  situations: Object.entries(situationCategories).flatMap(([category, ids]) =>
    ids.map((id) => ({ id, category }))
  ),
}
const quota = {
  trial_active: false,
  trial_ends_at: null,
  chat_remaining: 5,
  chat_limit: 5,
  lessons_remaining: 3,
  lessons_limit: 3,
  reading_remaining: 3,
  reading_limit: 3,
  listening_remaining: 3,
  listening_limit: 3,
  games_remaining: 3,
  games_limit: 3,
  voice_remaining_seconds: 300,
  voice_limit_seconds: 300,
  situations_remaining: 3,
  situations_limit: 3,
}

function deferred<T>() {
  let resolve!: (value: T) => void
  const promise = new Promise<T>((done) => {
    resolve = done
  })
  return { promise, resolve }
}

beforeEach(() => {
  vi.clearAllMocks()
  vi.mocked(apiFetch).mockReset()
  mocks.query = ''
  mocks.voice.mockImplementation(() => <div>voice-mode</div>)
  useAuthStore.setState({
    sessionVersion: 1,
    accessToken: 'token',
    user: mapUser({
      id: 1,
      username: 'learner',
      role: 'user',
      subscription_status: 'none',
    }),
  })
  useLanguageStore.setState({
    activeLanguage: getLanguageByCode('fr-FR'),
    userLanguages: [language],
    isSwitching: false,
    needsRefresh: false,
    invalidationVersion: 0,
    fetchLanguages: vi.fn().mockResolvedValue(false),
  })
  useConfigStore.setState({
    stripeEnabled: true,
    freemiumTrialEnabled: true,
  })
  useFreemiumStore.setState({
    status: quota,
    loaded: true,
    lastFetch: Date.now(),
    fetchStatus: vi.fn().mockResolvedValue(undefined),
  })
  vi.mocked(apiFetch).mockImplementation(
    async () => new Response(JSON.stringify(catalog))
  )
})

afterEach(cleanup)

describe('Situations catalog', () => {
  it('lists 50 cards in translated category/title order and searches descriptions', async () => {
    render(<SituationsCatalog />)
    await waitFor(() =>
      expect(screen.getAllByRole('button', { name: /^start:/ })).toHaveLength(
        50
      )
    )
    expect(
      screen.getAllByRole('heading', { level: 2 }).map((el) => el.textContent)
    ).toEqual(['Daily life', 'Shopping', 'Social', 'Travel', 'Work'])
    fireEvent.change(screen.getByRole('combobox'), {
      target: { value: 'travel' },
    })
    const titles = screen
      .getAllByRole('heading', { level: 3 })
      .map((el) => el.textContent)
    expect(titles[0]).toBe('A hotel problem')
    expect(titles[1]).toBe('Finding your way')
    expect(screen.getAllByRole('button', { name: /^start:/ })).toHaveLength(10)
    fireEvent.change(screen.getByRole('searchbox'), {
      target: { value: 'NOISY' },
    })
    expect(screen.getAllByRole('button', { name: /^start:/ })).toHaveLength(1)
    fireEvent.click(
      screen.getByRole('button', { name: 'start: A hotel problem' })
    )
    expect(mocks.push).toHaveBeenCalledWith(
      '/conversation?situation=hotel_problem&plan=7'
    )
    fireEvent.change(screen.getByRole('searchbox'), {
      target: { value: 'no match' },
    })
    expect(screen.getByText('noResults')).toBeInTheDocument()
  })

  it('shows the existing assessment entry for a confirmed missing plan', () => {
    useLanguageStore.setState({ userLanguages: [{ ...language, plan: null }] })
    render(<SituationsCatalog />)
    expect(screen.getByRole('link', { name: 'no-plan' })).toHaveAttribute(
      'href',
      '/assessment'
    )
    expect(apiFetch).not.toHaveBeenCalled()
  })

  it('recovers unknown language context before deciding whether there is a plan', async () => {
    useLanguageStore.setState({ needsRefresh: true })
    render(<SituationsCatalog />)
    expect(await screen.findByRole('alert')).toHaveTextContent('loadError')
    expect(screen.queryByText('no-plan')).toBeNull()
    useLanguageStore.setState({
      fetchLanguages: vi.fn().mockImplementation(async () => {
        useLanguageStore.setState({
          needsRefresh: false,
          userLanguages: [{ ...language, plan: null }],
        })
        return true
      }),
    })
    fireEvent.click(screen.getByRole('button', { name: 'retry' }))
    expect(
      await screen.findByRole('link', { name: 'no-plan' })
    ).toBeInTheDocument()
    expect(apiFetch).not.toHaveBeenCalled()
  })

  it('offers retry on transport failure without fabricating an empty catalog', async () => {
    vi.mocked(apiFetch).mockRejectedValueOnce(new Error('network'))
    render(<SituationsCatalog />)
    expect(await screen.findByRole('alert')).toHaveTextContent('loadError')
    expect(screen.queryByText('noResults')).toBeNull()
    fireEvent.click(screen.getByRole('button', { name: 'retry' }))
    expect(
      await screen.findByRole('button', {
        name: 'start: A hotel problem',
      })
    ).toBeEnabled()
  })

  it('reconciles a stale server plan only on retry', async () => {
    vi.mocked(apiFetch).mockResolvedValueOnce(
      new Response(null, { status: 409 })
    )
    render(<SituationsCatalog />)
    expect(await screen.findByRole('alert')).toHaveTextContent('contextChanged')
    expect(useLanguageStore.getState().fetchLanguages).not.toHaveBeenCalled()
    fireEvent.click(screen.getByRole('button', { name: 'retry' }))
    await waitFor(() =>
      expect(useLanguageStore.getState().fetchLanguages).toHaveBeenCalled()
    )
  })

  it.each(['language', 'owner'] as const)(
    'ignores stale catalog JSON after %s replacement',
    async (change) => {
      const old = deferred<typeof catalog>()
      let signal: AbortSignal | undefined
      vi.mocked(apiFetch).mockImplementationOnce(async (_url, options) => {
        signal = options?.signal as AbortSignal
        return { ok: true, json: () => old.promise } as Response
      })
      const view = render(<SituationsCatalog />)
      await waitFor(() => expect(apiFetch).toHaveBeenCalledOnce())
      const nextCatalog = {
        ...catalog,
        study_plan_id: 9,
        target_language: 'de-DE',
        situations: [{ id: 'make_plans', category: 'social' }],
      }
      vi.mocked(apiFetch).mockImplementation(
        async () => new Response(JSON.stringify(nextCatalog))
      )
      act(() => {
        if (change === 'owner') useAuthStore.setState({ sessionVersion: 2 })
        useLanguageStore.setState({
          activeLanguage: getLanguageByCode('de-DE'),
          userLanguages: [
            {
              ...language,
              target_language: 'de-DE',
              plan: { ...plan, id: 9 },
            },
          ],
        })
      })
      expect(
        await screen.findByRole('button', {
          name: 'start: items.make_plans.title',
        })
      ).toBeEnabled()
      expect(signal?.aborted).toBe(true)
      await act(async () => old.resolve(catalog))
      expect(screen.queryByText('A hotel problem')).toBeNull()
      view.unmount()
    }
  )

  it('rejects an earlier generation even when the language returns to the same plan', async () => {
    const old = deferred<Response>()
    vi.mocked(apiFetch).mockReturnValueOnce(old.promise)
    render(<SituationsCatalog />)
    await waitFor(() => expect(apiFetch).toHaveBeenCalledOnce())
    vi.mocked(apiFetch).mockResolvedValueOnce(
      new Response(
        JSON.stringify({
          ...catalog,
          situations: [{ id: 'make_plans', category: 'social' }],
        })
      )
    )
    act(() => {
      useLanguageStore.setState({
        activeLanguage: getLanguageByCode('de-DE'),
        invalidationVersion: 1,
      })
      useLanguageStore.setState({
        activeLanguage: getLanguageByCode('fr-FR'),
        invalidationVersion: 2,
      })
    })
    expect(
      await screen.findByRole('button', {
        name: 'start: items.make_plans.title',
      })
    ).toBeEnabled()
    await act(async () => {
      old.resolve(new Response(JSON.stringify(catalog)))
    })
    expect(screen.queryByText('A hotel problem')).toBeNull()
  })

  it('blocks catalog actions during a language switch and reconciles uncertain context', async () => {
    render(<SituationsCatalog />)
    await screen.findByRole('button', { name: 'start: A hotel problem' })
    act(() => useLanguageStore.setState({ isSwitching: true }))
    expect(screen.queryByRole('button', { name: /^start:/ })).toBeNull()
    act(() => {
      useLanguageStore.setState({
        isSwitching: false,
        needsRefresh: true,
        userLanguages: [{ ...language, plan: null }],
      })
    })
    expect(await screen.findByRole('alert')).toHaveTextContent('loadError')
    expect(screen.queryByText('no-plan')).toBeNull()
  })

  it.each(['situations', 'voice'] as const)(
    'respects the independent %s allowance',
    async (feature) => {
      useFreemiumStore.setState({
        status: {
          ...quota,
          ...(feature === 'situations'
            ? { situations_remaining: 0 }
            : { voice_remaining_seconds: 0 }),
        },
      })
      render(<SituationsCatalog />)
      expect(await screen.findByTestId('paywall')).toHaveTextContent(feature)
      expect(
        screen.getByRole('button', {
          name: 'start: A hotel problem',
        })
      ).toBeDisabled()
      expect(mocks.push).not.toHaveBeenCalled()
    }
  )

  it.each(['subscription', 'trial', 'self-hosted'] as const)(
    'retains the %s feature exemption',
    async (access) => {
      useFreemiumStore.setState({
        status: {
          ...quota,
          situations_remaining: 0,
          voice_remaining_seconds: 0,
        },
      })
      if (access === 'self-hosted')
        useConfigStore.setState({ stripeEnabled: false })
      else
        useAuthStore.setState({
          user: {
            ...useAuthStore.getState().user!,
            ...(access === 'subscription'
              ? { subscription_status: 'active' as const }
              : {
                  freemium_trial_ends_at: new Date(
                    Date.now() + 86_400_000
                  ).toISOString(),
                }),
          },
        })
      render(<SituationsCatalog />)
      expect(
        await screen.findByRole('button', {
          name: 'start: A hotel problem',
        })
      ).toBeEnabled()
      expect(screen.queryByTestId('paywall')).toBeNull()
    }
  )
})

describe('Situations voice entry', () => {
  beforeEach(() => {
    mocks.query = 'situation=hotel_problem&plan=7'
  })

  it('loads source metadata before voice starts and uses its localized title and plan', async () => {
    const pending = deferred<Response>()
    vi.mocked(apiFetch).mockReturnValueOnce(pending.promise)
    render(<ConversationPage />)
    expect(mocks.voice).not.toHaveBeenCalled()
    act(() => {
      useLanguageStore.setState({
        activeLanguage: getLanguageByCode('de-DE'),
        userLanguages: [
          { ...language, target_language: 'de-DE', plan: { ...plan, id: 9 } },
        ],
      })
    })
    await act(async () => {
      pending.resolve(new Response(JSON.stringify(catalog)))
    })
    expect(await screen.findByText('voice-mode')).toBeInTheDocument()
    expect(mocks.voice.mock.lastCall?.[0]).toMatchObject({
      situationId: 'hotel_problem',
      situationStudyPlanId: 7,
      lessonTitle: 'A hotel problem',
      targetLanguage: 'fr-FR',
      cefrLevel: 'B1',
      autoStart: true,
    })
    expect(apiFetch).toHaveBeenCalledTimes(1)
  })

  it.each([
    'plan=7',
    'situation=hotel_problem',
    'situation=hotel_problem&plan=0',
    'situation=hotel_problem&plan=7&lesson=1',
    'situation=hotel_problem&plan=7&grammarPractice=abc',
    'situation=hotel_problem&plan=7&plan=8',
    'situation=unknown&plan=7',
  ])('never falls back to free conversation for %s', async (query) => {
    mocks.query = query
    render(<ConversationPage />)
    expect(await screen.findByRole('alert')).toHaveTextContent('unavailable')
    expect(apiFetch).not.toHaveBeenCalled()
    expect(mocks.voice).not.toHaveBeenCalled()
  })

  it('rejects a catalog missing the requested situation and supports retry', async () => {
    vi.mocked(apiFetch).mockResolvedValueOnce(
      new Response(JSON.stringify({ ...catalog, situations: [] }))
    )
    render(<ConversationPage />)
    expect(await screen.findByRole('alert')).toHaveTextContent('unavailable')
    expect(mocks.voice).not.toHaveBeenCalled()
    fireEvent.click(screen.getByRole('button', { name: 'retry' }))
    expect(await screen.findByText('voice-mode')).toBeInTheDocument()
  })

  it.each(['situations', 'voice'] as const)(
    'requires a fresh start action after the exhausted %s allowance recovers',
    async (feature) => {
      useFreemiumStore.setState({
        status: {
          ...quota,
          ...(feature === 'situations'
            ? { situations_remaining: 0 }
            : { voice_remaining_seconds: 0 }),
        },
      })
      render(<ConversationPage />)
      expect(await screen.findByTestId('paywall')).toHaveTextContent(feature)
      expect(mocks.voice).not.toHaveBeenCalled()
      act(() => useFreemiumStore.setState({ status: quota }))
      expect(await screen.findByText('voice-mode')).toBeInTheDocument()
      expect(mocks.voice.mock.lastCall?.[0]).toMatchObject({
        situationId: 'hotel_problem',
        situationStudyPlanId: 7,
        autoStart: false,
      })
    }
  )

  it('cannot start from an old owner response after logout', async () => {
    const pending = deferred<Response>()
    vi.mocked(apiFetch).mockReturnValueOnce(pending.promise)
    vi.mocked(apiFetch).mockResolvedValueOnce(
      new Response(null, { status: 403 })
    )
    render(<ConversationPage />)
    act(() => useAuthStore.setState({ sessionVersion: 2, user: null }))
    expect(await screen.findByRole('alert')).toHaveTextContent('unavailable')
    await act(async () => {
      pending.resolve(new Response(JSON.stringify(catalog)))
    })
    expect(mocks.voice).not.toHaveBeenCalled()
  })

  it('ignores stale route metadata when a different situation is selected', async () => {
    const pending = deferred<Response>()
    vi.mocked(apiFetch).mockReturnValueOnce(pending.promise)
    const view = render(<ConversationPage />)
    mocks.query = 'situation=make_plans&plan=7'
    view.rerender(<ConversationPage />)
    await screen.findByText('voice-mode')
    await act(async () => {
      pending.resolve(new Response(JSON.stringify(catalog)))
    })
    expect(mocks.voice.mock.lastCall?.[0]).toMatchObject({
      situationId: 'make_plans',
      lessonTitle: 'items.make_plans.title',
    })
  })
})
