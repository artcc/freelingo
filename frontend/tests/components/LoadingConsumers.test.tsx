import { act, cleanup, fireEvent, render, screen } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { UsageLimitsSection } from '@/components/settings/UsageLimitsSection'
import MyLanguagesPage from '@/app/(app)/settings/languages/page'
import PricingSection from '@/components/billing/PricingSection'
import { useAuthStore } from '@/store/auth'
import { useLanguageStore } from '@/store/language'

const mocks = vi.hoisted(() => ({ apiFetch: vi.fn(), subscription: vi.fn() }))
vi.mock('@/lib/api', () => ({
  apiFetch: mocks.apiFetch,
  restoreAccessToken: vi.fn(),
}))
vi.mock('@/lib/landing-subscription', () => ({
  getLandingSubscriptionState: mocks.subscription,
}))
vi.mock('next-intl', () => ({
  useLocale: () => 'es',
  useTranslations: () => (key: string) => key,
}))

function deferred<T>() {
  let resolve!: (value: T) => void
  const promise = new Promise<T>((done) => {
    resolve = done
  })
  return { promise, resolve }
}

const quota = {
  sessions_this_week: 2,
  sessions_limit: 5,
  sessions_unlimited: false,
  minutes_today: 10,
  minutes_limit: 30,
  time_unlimited: false,
  minutes_this_week: 20,
  weekly_minutes_limit: 60,
  weekly_minutes_unlimited: false,
  tokens_this_month: 1000,
  tokens_monthly_limit: 5000,
  tokens_unlimited: false,
}
const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status })
const pricingProps = {
  allowRegistration: true,
  stripeEnabled: true,
  hasSession: true,
  trialDays: 0,
  priceMonthly: 10,
  priceYearly: 100,
  totalPriceMonthly: 120,
  totalPriceYearly: 100,
}

beforeEach(() => {
  vi.resetAllMocks()
  useAuthStore.getState().startSession('token')
  useLanguageStore.setState({
    activeLanguage: null,
    userLanguages: [],
    availableLanguageCodes: [],
    needsRefresh: false,
    isSwitching: false,
    fetchLanguages: vi.fn().mockResolvedValue(true),
  })
})
afterEach(() => {
  cleanup()
  vi.useRealTimers()
})

describe('Usage limits loading', () => {
  it.each(['http', 'network', 'empty'])(
    'shows a local error and retries after %s failure',
    async (failure) => {
      if (failure === 'http')
        mocks.apiFetch.mockResolvedValueOnce(
          json({ detail: 'unavailable' }, 503)
        )
      else if (failure === 'empty')
        mocks.apiFetch.mockResolvedValueOnce(json(null))
      else mocks.apiFetch.mockRejectedValueOnce(new Error('offline'))
      mocks.apiFetch.mockResolvedValueOnce(json(quota))
      render(<UsageLimitsSection />)
      expect(screen.getByRole('status')).toHaveTextContent('loading')
      expect(screen.getByText('sectionUsageLimits')).toBeInTheDocument()
      expect(await screen.findByRole('alert')).toHaveTextContent('errorMessage')
      expect(screen.queryByRole('status')).toBeNull()
      expect(screen.queryByText('quotaHint')).toBeNull()
      fireEvent.click(screen.getByRole('button', { name: 'retry' }))
      expect(await screen.findByText('quotaHint')).toBeInTheDocument()
      expect(screen.queryByRole('alert')).toBeNull()
    }
  )

  it('bounds the read, ignores a late body and permits retry', async () => {
    vi.useFakeTimers()
    const body = deferred<unknown>()
    mocks.apiFetch.mockResolvedValueOnce({ ok: true, json: () => body.promise })
    render(<UsageLimitsSection />)
    await act(async () => {
      await Promise.resolve()
    })
    const signal = mocks.apiFetch.mock.calls[0][1].signal as AbortSignal
    await act(async () => {
      vi.advanceTimersByTime(20_000)
    })
    expect(signal.aborted).toBe(true)
    expect(screen.getByRole('alert')).toBeInTheDocument()
    mocks.apiFetch.mockResolvedValueOnce(json(quota))
    await act(async () => {
      fireEvent.click(screen.getByRole('button', { name: 'retry' }))
    })
    await act(async () => {
      body.resolve({ ...quota, sessions_this_week: 99 })
    })
    expect(screen.queryByRole('alert')).toBeNull()
    expect(screen.getByText('quotaHint')).toBeInTheDocument()
    expect(screen.queryByText(/99/)).toBeNull()
  })

  it('cancels on unmount and clears the read deadline', async () => {
    vi.useFakeTimers()
    const response = deferred<Response>()
    mocks.apiFetch.mockReturnValueOnce(response.promise)
    const view = render(<UsageLimitsSection />)
    const signal = mocks.apiFetch.mock.calls[0][1].signal as AbortSignal
    view.unmount()
    expect(signal.aborted).toBe(true)
    expect(vi.getTimerCount()).toBe(0)
    await act(async () => {
      response.resolve(json(quota))
    })
    expect(screen.queryByText('quotaHint')).toBeNull()
  })
})

describe('Language settings loading', () => {
  it('keeps the heading and navigation visible and distinguishes a failed read from an empty account', async () => {
    const fetchLanguages = vi
      .fn()
      .mockResolvedValueOnce(false)
      .mockResolvedValueOnce(true)
    useLanguageStore.setState({ fetchLanguages })
    const { container } = render(<MyLanguagesPage />)
    expect(screen.getByRole('heading', { name: 'myLanguages' })).toBeVisible()
    expect(screen.getByRole('link', { name: 'title' })).toHaveAttribute(
      'href',
      '/settings'
    )
    expect(screen.getByRole('status')).toBeInTheDocument()
    expect(container.querySelector('.h-dvh')).toBeNull()
    await screen.findByRole('alert')
    expect(screen.queryByText('noLanguages')).toBeNull()
    fireEvent.click(screen.getByRole('button', { name: 'retry' }))
    expect(await screen.findByText('noLanguages')).toBeInTheDocument()
    expect(screen.queryByRole('alert')).toBeNull()
  })

  it('discards a previous session completion while the current read remains pending', async () => {
    const oldRead = deferred<boolean>()
    const currentRead = deferred<boolean>()
    const fetchLanguages = vi
      .fn()
      .mockReturnValueOnce(oldRead.promise)
      .mockReturnValueOnce(currentRead.promise)
    useLanguageStore.setState({ fetchLanguages })
    const view = render(<MyLanguagesPage />)
    const oldSignal = fetchLanguages.mock.calls[0][0] as AbortSignal
    act(() => useAuthStore.getState().startSession('new-account'))
    expect(oldSignal.aborted).toBe(true)
    await act(async () => {
      oldRead.resolve(false)
    })
    expect(screen.getByRole('status')).toBeInTheDocument()
    expect(screen.queryByRole('alert')).toBeNull()
    await act(async () => {
      currentRead.resolve(true)
    })
    expect(screen.getByText('noLanguages')).toBeInTheDocument()
    view.unmount()
    expect((fetchLanguages.mock.calls[1][0] as AbortSignal).aborted).toBe(true)
  })
})

describe('Landing pricing lookup', () => {
  it('reserves only its section while the session lookup is pending', async () => {
    const lookup = deferred<{ subscribed: boolean; trialUsed: boolean }>()
    mocks.subscription.mockReturnValueOnce(lookup.promise)
    const { container } = render(
      <>
        <a href="/about">About</a>
        <PricingSection {...pricingProps} />
      </>
    )
    expect(screen.getByRole('link', { name: 'About' })).toBeVisible()
    expect(screen.getByRole('status').closest('section')).toHaveClass(
      'min-h-80'
    )
    expect(container.querySelector('.fixed, .h-dvh, [inert]')).toBeNull()
    expect(screen.queryByText('pricingTitle')).toBeNull()
    await act(async () => {
      lookup.resolve({ subscribed: true, trialUsed: true })
    })
    expect(screen.queryByRole('status')).toBeNull()
    expect(screen.queryByText('pricingTitle')).toBeNull()
  })

  it('ignores an obsolete subscribed response and waits for the current session', async () => {
    const oldLookup = deferred<{ subscribed: boolean; trialUsed: boolean }>()
    const newLookup = deferred<{ subscribed: boolean; trialUsed: boolean }>()
    mocks.subscription
      .mockReturnValueOnce(oldLookup.promise)
      .mockReturnValueOnce(newLookup.promise)
    render(<PricingSection {...pricingProps} />)
    act(() => useAuthStore.getState().startSession('new-account'))
    await act(async () => {
      oldLookup.resolve({ subscribed: true, trialUsed: true })
    })
    expect(screen.getByRole('status')).toBeInTheDocument()
    await act(async () => {
      newLookup.resolve({ subscribed: false, trialUsed: false })
    })
    expect(screen.getByText('pricingTitle')).toBeInTheDocument()
    expect(screen.queryByRole('status')).toBeNull()
  })

  it('ignores a session lookup after unmount', async () => {
    const lookup = deferred<{ subscribed: boolean; trialUsed: boolean }>()
    mocks.subscription.mockReturnValueOnce(lookup.promise)
    const view = render(<PricingSection {...pricingProps} />)
    view.unmount()
    await act(async () => {
      lookup.resolve({ subscribed: false, trialUsed: false })
    })
    expect(screen.queryByText('pricingTitle')).toBeNull()
  })
})
