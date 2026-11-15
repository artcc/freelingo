import { act, cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { GameCatalog } from '@/components/games/GameCatalog'
import { apiFetch } from '@/lib/api'
import { type DetectiveCatalog } from '@/lib/detective'
import { getLanguageByCode } from '@/lib/target-languages'
import { useAuthStore } from '@/store/auth'
import { useConfigStore } from '@/store/config'
import { useFreemiumStore } from '@/store/freemium'
import { useLanguageStore } from '@/store/language'

const { push } = vi.hoisted(() => ({ push: vi.fn() }))
vi.mock('next/navigation', () => ({ useRouter: () => ({ push }) }))
vi.mock('next-intl', () => {
  const translate = (key: string) => `translated:${key}`
  return { useTranslations: () => translate }
})
vi.mock('@/lib/api', () => ({ apiFetch: vi.fn() }))
vi.mock('@/components/billing/FreemiumQuotaBanner', () => ({ FreemiumQuotaBanner: () => null }))
vi.mock('@/components/billing/PaywallBanner', () => ({ PaywallBanner: () => <div>paywall</div> }))

const api = vi.mocked(apiFetch)
const json = (body: unknown, status = 200) => new Response(JSON.stringify(body), { status })
const quota = (remaining: number) => ({
  trial_active: false, trial_ends_at: null,
  chat_remaining: 3, chat_limit: 3, lessons_remaining: 3, lessons_limit: 3,
  listening_remaining: 3, listening_limit: 3, reading_remaining: 3, reading_limit: 3,
  games_remaining: remaining, games_limit: 3,
  voice_remaining_seconds: 300, voice_limit_seconds: 300,
})
const catalog = (remaining: number): DetectiveCatalog => ({
  study_plan_id: 1, target_language: 'en-GB', level: 'A1', limited: true,
  quota: { remaining, limit: 3 }, total: 0, history: [],
  modes: {
    review: { available: false, reason: 'noSources' },
    prepare: { available: false, reason: 'noUpcoming' },
    free: { available: true, reason: null },
  },
})

beforeEach(() => {
  api.mockReset()
  push.mockReset()
  useAuthStore.setState({ sessionVersion: 1, accessToken: 'token', user: {
    id: 1, username: 'learner', displayName: 'Learner', role: 'user',
    subscription_status: 'none', conversation_max_duration: 300, conversation_inactivity_timeout: 30,
  } })
  useLanguageStore.setState({
    activeLanguage: getLanguageByCode('en-GB'), needsRefresh: false, isSwitching: false,
    userLanguages: [{
      target_language: 'en-GB', is_active: true, progress: null,
      plan: { id: 1, cefr_level: 'A1', progress_day: 0, total_days: 48, completion_pct: 0 },
    }],
  })
  useConfigStore.setState({ stripeEnabled: true, loaded: true })
  useFreemiumStore.setState({
    status: quota(0), loaded: true, lastFetch: 1,
    fetchStatus: vi.fn().mockResolvedValue(undefined),
  })
})

afterEach(() => {
  cleanup()
  useAuthStore.setState(useAuthStore.getInitialState(), true)
  useConfigStore.setState(useConfigStore.getInitialState(), true)
  useFreemiumStore.setState(useFreemiumStore.getInitialState(), true)
  useLanguageStore.setState(useLanguageStore.getInitialState(), true)
})

describe('Games access through the real HTTP parser', () => {
  it.each(['subscription', 'billing-disabled', 'trial-enabled'])(
    'retains %s recovery while the exhausted catalog response is pending',
    async (change) => {
      useConfigStore.setState({ freemiumTrialEnabled: false })
      useAuthStore.getState().setUser({
        ...useAuthStore.getState().user!,
        freemium_trial_ends_at: new Date(Date.now() + 60_000).toISOString(),
      })
      let finish!: (response: Response) => void
      api.mockReturnValueOnce(new Promise((resolve) => { finish = resolve }))
        .mockResolvedValueOnce(json({ ...catalog(0), limited: false }))
      render(<GameCatalog gameType="detective" />)
      await waitFor(() => expect(api).toHaveBeenCalledTimes(1))
      act(() => {
        if (change === 'subscription') useAuthStore.getState().setUser({
          ...useAuthStore.getState().user!, subscription_status: 'active',
        })
        else if (change === 'billing-disabled') useConfigStore.setState({ stripeEnabled: false })
        else useConfigStore.setState({ freemiumTrialEnabled: true })
      })
      await act(async () => finish(json(catalog(0))))
      await waitFor(() => expect(screen.getAllByRole('button', { name: 'translated:start' })[2]).toBeEnabled())
      expect(api).toHaveBeenCalledTimes(2)
      expect(screen.queryByText('paywall')).not.toBeInTheDocument()
      expect(push).not.toHaveBeenCalled()
    }
  )

  it('rechecks an old creation denial when Premium was confirmed during the POST', async () => {
    let finish!: (response: Response) => void
    api.mockResolvedValueOnce(json(catalog(3)))
      .mockReturnValueOnce(new Promise((resolve) => { finish = resolve }))
      .mockResolvedValueOnce(json({ ...catalog(0), limited: false }))
    render(<GameCatalog gameType="detective" />)
    fireEvent.click((await screen.findAllByRole('button', { name: 'translated:start' }))[2])
    act(() => useAuthStore.getState().setUser({
      ...useAuthStore.getState().user!, subscription_status: 'active',
    }))
    await act(async () => finish(json({
      detail: { reason: 'freemium_exhausted', feature: 'games' },
    }, 402)))
    await waitFor(() => expect(screen.getAllByRole('button', { name: 'translated:start' })[2]).toBeEnabled())
    expect(api).toHaveBeenCalledTimes(3)
    expect(screen.queryByText('paywall')).not.toBeInTheDocument()
    expect(push).not.toHaveBeenCalled()
  })

  it.each([
    { detail: { reason: 'freemium_exhausted', feature: 'games', remaining: 0, limit: 3 }, paywall: true },
    { detail: { reason: 'freemium_unavailable', feature: 'games', remaining: 0, limit: 0 }, paywall: false },
    { detail: { reason: 'freemium_exhausted', feature: 'voice' }, paywall: false },
    { detail: 'subscription_required', paywall: true },
    { detail: 'freemium_exhausted', paywall: false },
    { detail: 'technical_internal_message', paywall: false },
    { detail: null, paywall: false },
  ])('classifies a real 402 body: $detail', async ({ detail, paywall }) => {
    api.mockResolvedValueOnce(json(catalog(3))).mockResolvedValueOnce(json({ detail }, 402))
    render(<GameCatalog gameType="detective" />)
    fireEvent.click((await screen.findAllByRole('button', { name: 'translated:start' }))[2])
    if (paywall) {
      expect(await screen.findByText('paywall')).toBeVisible()
      expect(screen.getAllByRole('button', { name: 'translated:start' })[2]).toBeDisabled()
    } else {
      expect(await screen.findByRole('alert')).toHaveTextContent('translated:errorMessage')
      expect(screen.queryByText('paywall')).not.toBeInTheDocument()
      expect(screen.getAllByRole('button', { name: 'translated:start' })[2]).toBeEnabled()
    }
    expect(screen.queryByText('technical_internal_message')).not.toBeInTheDocument()
    expect(screen.queryByText(/freemium_(exhausted|unavailable)/)).not.toBeInTheDocument()
    expect(api).toHaveBeenCalledTimes(2)
    expect(push).not.toHaveBeenCalled()
  })

  it('rechecks a stale exhausted catalog once after replenishment and still respects catalog authority', async () => {
    api.mockResolvedValueOnce(json(catalog(0))).mockResolvedValueOnce(json(catalog(0)))
    render(<GameCatalog gameType="detective" />)
    await screen.findByText('paywall')
    act(() => useFreemiumStore.setState({ status: quota(3), lastFetch: 2 }))
    await waitFor(() => expect(api).toHaveBeenCalledTimes(2))
    expect(await screen.findByText('paywall')).toBeVisible()
    expect(screen.getAllByRole('button', { name: 'translated:start' })[2]).toBeDisabled()
    await act(async () => {
      useFreemiumStore.setState({ lastFetch: 0 })
      useFreemiumStore.setState({ status: quota(3), lastFetch: 3 })
    })
    expect(api).toHaveBeenCalledTimes(2)
  })

  it('unblocks a replenished catalog and never loops through the forced global status refresh', async () => {
    api.mockResolvedValueOnce(json(catalog(0))).mockResolvedValueOnce(json(catalog(3)))
    render(<GameCatalog gameType="detective" />)
    await screen.findByText('paywall')
    act(() => useFreemiumStore.setState({ status: quota(3), lastFetch: 2 }))
    await waitFor(() => expect(screen.getAllByRole('button', { name: 'translated:start' })[2]).toBeEnabled())
    await act(async () => {
      useFreemiumStore.setState({ status: quota(3), lastFetch: 3 })
    })
    expect(api).toHaveBeenCalledTimes(2)
    expect(useFreemiumStore.getState().fetchStatus).toHaveBeenCalledTimes(2)
    expect(screen.queryByText('paywall')).not.toBeInTheDocument()
  })

  it.each([0, 3])(
    'reconciles stale positive quota after catalog exhaustion and a failed forced refresh (catalog retry=%s)',
    async (remaining) => {
      // Keep both the catalog parser and status store real for this ordering.
      useFreemiumStore.setState({
        status: quota(3),
        lastFetch: Date.now(),
        fetchStatus: useFreemiumStore.getInitialState().fetchStatus,
      })
      let catalogReads = 0
      let quotaReads = 0
      api.mockImplementation(async (url) => {
        if (url === '/api/freemium/status') {
          quotaReads += 1
          return quotaReads === 1 ? json({}, 503) : json(quota(3))
        }
        catalogReads += 1
        if (catalogReads > 2) throw new Error('Unexpected catalog retry loop')
        return json(catalog(catalogReads === 1 ? 0 : remaining))
      })
      render(<GameCatalog gameType="detective" />)
      await screen.findByText('paywall')
      await waitFor(() => expect(quotaReads).toBe(1))
      expect(useFreemiumStore.getState().lastFetch).toBe(0)
      expect(useFreemiumStore.getState().status?.games_remaining).toBe(3)
      expect(catalogReads).toBe(1)

      await act(async () => {
        await useFreemiumStore.getState().fetchStatus(true)
      })
      await waitFor(() => expect(quotaReads).toBe(3))
      expect(catalogReads).toBe(2)
      if (remaining === 0) {
        expect(screen.getByText('paywall')).toBeVisible()
        expect(screen.getAllByRole('button', { name: 'translated:start' })[2]).toBeDisabled()
      } else {
        expect(screen.queryByText('paywall')).not.toBeInTheDocument()
        expect(screen.getAllByRole('button', { name: 'translated:start' })[2]).toBeEnabled()
      }
      await act(async () => {
        await useFreemiumStore.getState().fetchStatus(true)
      })
      expect(catalogReads).toBe(2)
    }
  )

  it('rechecks a local POST denial after confirmed recovery even when the previous global quota was positive', async () => {
    useFreemiumStore.setState({ status: quota(3) })
    api.mockResolvedValueOnce(json(catalog(3)))
      .mockResolvedValueOnce(json({ detail: { reason: 'freemium_exhausted', feature: 'games', remaining: 0, limit: 3 } }, 402))
      .mockResolvedValueOnce(json(catalog(3)))
    render(<GameCatalog gameType="detective" />)
    fireEvent.click((await screen.findAllByRole('button', { name: 'translated:start' }))[2])
    await screen.findByText('paywall')
    act(() => useFreemiumStore.setState({ status: quota(3), lastFetch: 2 }))
    await waitFor(() => expect(screen.getAllByRole('button', { name: 'translated:start' })[2]).toBeEnabled())
    expect(api).toHaveBeenCalledTimes(3)
    expect(screen.queryByText('paywall')).not.toBeInTheDocument()
  })

  it.each(['subscription', 'billing-disabled', 'trial-enabled'])(
    'rechecks catalog authority after explicit %s recovery',
    async (change) => {
      useConfigStore.setState({ freemiumTrialEnabled: false })
      useAuthStore.getState().setUser({
        ...useAuthStore.getState().user!,
        freemium_trial_ends_at: new Date(Date.now() + 60_000).toISOString(),
      })
      api.mockResolvedValueOnce(json(catalog(0)))
        .mockResolvedValueOnce(json({ ...catalog(0), limited: false }))
      render(<GameCatalog gameType="detective" />)
      await screen.findByText('paywall')
      act(() => {
        if (change === 'subscription') useAuthStore.getState().setUser({
          ...useAuthStore.getState().user!, subscription_status: 'active',
        })
        else if (change === 'billing-disabled') useConfigStore.setState({ stripeEnabled: false })
        else useConfigStore.setState({ freemiumTrialEnabled: true })
      })
      await waitFor(() => expect(screen.getAllByRole('button', { name: 'translated:start' })[2]).toBeEnabled())
      expect(api).toHaveBeenCalledTimes(2)
      expect(screen.queryByText('paywall')).not.toBeInTheDocument()
    }
  )

  it('discards a replenishment catalog response after changing the owner language', async () => {
    let finish!: (response: Response) => void
    const pending = new Promise<Response>((resolve) => { finish = resolve })
    api.mockResolvedValueOnce(json(catalog(0))).mockReturnValueOnce(pending)
      .mockResolvedValueOnce(json({ ...catalog(3), study_plan_id: 2, target_language: 'fr-FR' }))
    render(<GameCatalog gameType="detective" />)
    await screen.findByText('paywall')
    act(() => useFreemiumStore.setState({ status: quota(3), lastFetch: 2 }))
    await waitFor(() => expect(api).toHaveBeenCalledTimes(2))
    act(() => useLanguageStore.setState({
      activeLanguage: getLanguageByCode('fr-FR'),
      userLanguages: [{
        target_language: 'fr-FR', is_active: true, progress: null,
        plan: { id: 2, cefr_level: 'A1', progress_day: 0, total_days: 48, completion_pct: 0 },
      }],
    }))
    await screen.findByText(/translated:fr-FR/)
    await act(async () => finish(json(catalog(0))))
    expect(screen.queryByText(/translated:en-GB/)).not.toBeInTheDocument()
    expect(screen.queryByText('paywall')).not.toBeInTheDocument()
    expect(useFreemiumStore.getState().fetchStatus).toHaveBeenCalledTimes(2)
  })
})
