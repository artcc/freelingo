import React from 'react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { act, cleanup, fireEvent, render, screen } from '@testing-library/react'
import { BillingSection } from '@/components/settings/BillingSection'
import { SubscriptionPlanButtons } from '@/components/billing/SubscriptionPlanButtons'
import { useAuthStore, type User } from '@/store/auth'
import { useConfigStore } from '@/store/config'

const { selection, createCheckout } = vi.hoisted(() => ({
  selection: { query: '' },
  createCheckout: vi.fn(),
}))

vi.mock('next/navigation', () => ({
  useSearchParams: () => new URLSearchParams(selection.query),
}))
vi.mock('@/lib/billing', () => ({ createCheckout }))
vi.mock('next-intl', () => ({
  useLocale: () => 'en-GB',
  useTranslations: () => (
    key: string,
    values?: Record<string, string | number>
  ) => {
    if (key === 'planYearly')
      return `Annual · €${values?.price}/year · 2 months free →`
    if (key === 'planMonthly') return `Monthly · €${values?.price}/month →`
    if (key === 'cardTrialTerms') return `cardTrialTerms ${values?.days}`
    if (key === 'noCardTrialDescription')
      return `noCardTrialDescription ${values?.date}`
    return key
  },
}))

const learner: User = {
  id: 1,
  username: 'learner',
  displayName: 'Learner',
  role: 'user',
  conversation_max_duration: 900,
  conversation_inactivity_timeout: 60,
  subscription_status: 'none',
  trial_used: false,
}

beforeEach(() => {
  vi.useFakeTimers()
  vi.setSystemTime(new Date('2026-11-15T12:00:00Z'))
  selection.query = ''
  createCheckout.mockReset()
  createCheckout.mockResolvedValue(null)
  useAuthStore.setState(
    { ...useAuthStore.getInitialState(), user: learner, accessToken: 'token' },
    true
  )
  useConfigStore.setState(
    {
      ...useConfigStore.getInitialState(),
      loaded: true,
      stripeEnabled: true,
      freemiumTrialEnabled: true,
      stripeTrialDays: 7,
      priceMonthly: 10,
      priceYearly: 100,
    },
    true
  )
})

afterEach(() => {
  cleanup()
  vi.useRealTimers()
})

describe('settings Premium offer', () => {
  it.each([
    ['', 'Monthly', 'monthly'],
    ['plan=invalid', 'Monthly', 'monthly'],
    ['plan=monthly', 'Monthly', 'monthly'],
    ['plan=yearly', 'Annual', 'yearly'],
  ])('honours purchase intent with monthly as the settings default: %s', async (
    query,
    label,
    interval
  ) => {
    selection.query = query
    render(<BillingSection />)
    const firstButton = screen.getAllByRole('button')[0]
    expect(firstButton).toHaveTextContent(label)
    expect(createCheckout).not.toHaveBeenCalled()
    await act(async () => fireEvent.click(firstButton))
    expect(createCheckout).toHaveBeenCalledWith(interval, expect.any(AbortSignal))
  })

  it('keeps annual first for shared consumers without settings details', () => {
    render(<SubscriptionPlanButtons />)
    expect(screen.getAllByRole('button')[0]).toHaveTextContent('Annual')
    expect(screen.queryByText('monthlyCommitment')).not.toBeInTheDocument()
    expect(screen.getByText('paywallNoCharge')).toBeInTheDocument()
  })

  it('explains included practice and the general limits beside both intervals', () => {
    render(<BillingSection />)
    expect(screen.getAllByRole('listitem')).toHaveLength(5)
    expect(screen.getByText('generalLimits')).toBeInTheDocument()
    expect(
      screen.getByRole('button', { name: /Monthly/ })
    ).toHaveAccessibleDescription('monthlyCommitment cardTrialTerms 7')
    expect(
      screen.getByRole('button', { name: /Annual/ })
    ).toHaveAccessibleDescription('yearlyCommitment cardTrialTerms 7')
  })

  it('shows the dated no-card trial and updates when it expires', () => {
    useAuthStore.setState({
      user: {
        ...learner,
        freemium_trial_ends_at: '2026-11-15T12:00:01Z',
      },
    })
    render(<BillingSection />)
    expect(screen.getByText('noCardTrialStatus')).toBeInTheDocument()
    expect(
      screen.getByText('noCardTrialDescription 15/11/2026')
    ).toBeInTheDocument()
    expect(screen.queryByText('statusNone')).not.toBeInTheDocument()
    expect(screen.getByRole('button', { name: /Monthly/ })).toBeEnabled()
    act(() => vi.advanceTimersByTime(1000))
    expect(screen.queryByText('noCardTrialStatus')).not.toBeInTheDocument()
    expect(screen.getByText('statusNone')).toBeInTheDocument()
  })

  it('respects the no-card trial runtime toggle without hiding plans', () => {
    useAuthStore.setState({
      user: {
        ...learner,
        freemium_trial_ends_at: '2026-11-20T12:00:00Z',
      },
    })
    render(<BillingSection />)
    expect(screen.getByText('noCardTrialStatus')).toBeInTheDocument()
    act(() => useConfigStore.setState({ freemiumTrialEnabled: false }))
    expect(screen.queryByText('noCardTrialStatus')).not.toBeInTheDocument()
    expect(screen.getByRole('button', { name: /Monthly/ })).toBeEnabled()
  })

  it.each(['active', 'trialing', 'past_due', 'unpaid', 'paused'] as const)(
    'preserves management or payment recovery for %s',
    (subscription_status) => {
      useAuthStore.setState({
        user: {
          ...learner,
          subscription_status,
          freemium_trial_ends_at: '2026-11-20T12:00:00Z',
        },
      })
      render(<BillingSection />)
      expect(screen.queryByText('noCardTrialStatus')).not.toBeInTheDocument()
      expect(
        screen.queryByRole('button', { name: /Monthly/ })
      ).not.toBeInTheDocument()
      expect(
        screen.getByRole('button', {
          name: ['active', 'trialing'].includes(subscription_status)
            ? 'manage'
            : 'updatePayment',
        })
      ).toBeEnabled()
    }
  )

  it.each([
    { days: 0, used: false, loaded: true },
    { days: -1, used: false, loaded: true },
    { days: 1.5, used: false, loaded: true },
    { days: NaN, used: false, loaded: true },
    { days: Infinity, used: false, loaded: true },
    { days: 7, used: true, loaded: true },
    { days: 7, used: undefined, loaded: true },
    { days: 7, used: false, loaded: false },
  ])('does not promise a subscription trial without known eligibility: %j', ({
    days,
    used,
    loaded,
  }) => {
    useConfigStore.setState({ stripeTrialDays: days, loaded })
    useAuthStore.setState({ user: { ...learner, trial_used: used } })
    render(<BillingSection />)
    const known = loaded && Number.isInteger(days) && days >= 0 &&
      typeof used === 'boolean'
    expect(screen.getByText(
      known ? 'paidTerms' : 'paywallNoChargeTrialUsed'
    )).toBeInTheDocument()
    expect(screen.queryByText(/^cardTrialTerms/)).not.toBeInTheDocument()
  })

  it('uses the configured card-trial duration and only claims exact annual savings', () => {
    useConfigStore.setState({ stripeTrialDays: 14, priceYearly: 110 })
    render(<BillingSection />)
    expect(screen.getByText('cardTrialTerms 14')).toBeInTheDocument()
    expect(screen.getByText('Annual · €110/year →')).toBeInTheDocument()
    expect(screen.queryByText('2 months free')).not.toBeInTheDocument()
    act(() => useConfigStore.setState({ priceYearly: 100 }))
    expect(screen.getByText('2 months free')).toBeInTheDocument()
  })
})
