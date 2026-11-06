import React from 'react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import {
  act,
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from '@testing-library/react'
import { PaywallBanner } from '@/components/billing/PaywallBanner'
import { BillingSection } from '@/components/settings/BillingSection'
import PricingSection from '@/components/billing/PricingSection'
import OnboardingPage from '@/app/(auth)/onboarding/page'
import DashboardPage from '@/app/(app)/dashboard/page'
import { useAuthStore, type User } from '@/store/auth'
import { useConfigStore } from '@/store/config'
import { useLanguageStore } from '@/store/language'

const { apiFetch, landingState, push } = vi.hoisted(() => ({
  apiFetch: vi.fn(),
  landingState: vi.fn(),
  push: vi.fn(),
}))
vi.mock('@/lib/api', () => ({ apiFetch, restoreAccessToken: vi.fn() }))
vi.mock('@/lib/landing-subscription', () => ({
  getLandingSubscriptionState: landingState,
}))
vi.mock('next-intl', () => ({
  useLocale: () => 'es',
  useTranslations: () => (key: string) => key,
}))
vi.mock('next/navigation', () => ({
  useRouter: () => ({ push }),
  useSearchParams: () => new URLSearchParams(),
}))
vi.mock('@/components/tour/OnboardingTour', () => ({ default: () => null }))
vi.mock('@/components/whats-new/WhatsNew', () => ({ default: () => null }))

const profile: User = {
  id: 1,
  username: 'learner',
  displayName: 'Learner',
  role: 'user',
  subscription_status: 'none',
  trial_used: false,
  conversation_max_duration: 1800,
  conversation_inactivity_timeout: 180,
}
const json = (data: unknown, status = 200) =>
  new Response(JSON.stringify(data), { status })
const savedProfile = (status = 'none') => ({
  ...profile,
  display_name: profile.displayName,
  target_language: 'en-GB',
  freemium_trial_used: true,
  subscription_status: status,
})

beforeEach(() => {
  apiFetch.mockReset()
  landingState.mockReset()
  push.mockReset()
  useAuthStore.getState().startSession('token')
  useAuthStore.getState().setUser(profile)
  useConfigStore.setState({
    loaded: true,
    stripeEnabled: true,
    stripeTrialDays: 0,
    freemiumTrialEnabled: false,
    load: vi.fn().mockResolvedValue(undefined),
  })
  useLanguageStore.setState({
    activeLanguage: null,
    availableLanguageCodes: ['en-GB'],
    fetchLanguages: vi.fn().mockResolvedValue(undefined),
  })
  Object.defineProperty(window, 'location', {
    configurable: true,
    value: { assign: vi.fn() },
  })
})
afterEach(cleanup)

async function renderPortal(component: string) {
  useAuthStore
    .getState()
    .setUser({ ...profile, subscription_status: 'past_due' })
  if (component === 'dashboard') {
    apiFetch
      .mockResolvedValueOnce(json({}))
      .mockResolvedValueOnce(json({ lessons: [] }))
  }
  const view = render(
    component === 'paywall' ? (
      <PaywallBanner />
    ) : component === 'settings' ? (
      <BillingSection />
    ) : (
      <DashboardPage />
    )
  )
  await screen.findByText('updatePayment')
  return view
}

describe.each(['paywall', 'settings', 'dashboard'])(
  'billing portal in %s',
  (component) => {
    it.each(['session', 'unmount', 'body', 'error'])(
      'ignores a response after %s invalidation',
      async (invalidation) => {
        const view = await renderPortal(component)
        let resolveResponse!: (response: Response) => void
        let resolveBody!: (body: unknown) => void
        const body = new Promise((resolve) => {
          resolveBody = resolve
        })
        const decode = vi.fn(() => body)
        if (invalidation === 'body') {
          apiFetch.mockResolvedValueOnce({ ok: true, json: decode })
        } else {
          apiFetch.mockReturnValueOnce(
            new Promise<Response>((resolve) => {
              resolveResponse = resolve
            })
          )
        }
        fireEvent.click(screen.getByText('updatePayment'))
        const options = apiFetch.mock.lastCall![1]
        expect(options.signal.aborted).toBe(false)
        if (invalidation === 'body')
          await waitFor(() => expect(decode).toHaveBeenCalledOnce())
        if (invalidation === 'unmount') view.unmount()
        else
          act(() => {
            useAuthStore.getState().startSession('different-account')
            useAuthStore
              .getState()
              .setUser({ ...profile, id: 2, subscription_status: 'past_due' })
          })
        expect(options.signal.aborted).toBe(true)
        await act(async () => {
          const url = 'https://billing.stripe.com/session/previous-account'
          if (invalidation === 'body') resolveBody({ url })
          else
            resolveResponse(json({ url }, invalidation === 'error' ? 503 : 200))
        })
        expect(window.location.assign).not.toHaveBeenCalled()
        expect(screen.queryByText('portalError')).toBeNull()
        if (invalidation !== 'unmount') {
          expect(screen.getByText('updatePayment')).not.toBeDisabled()
          apiFetch.mockResolvedValueOnce(
            json({ url: 'https://billing.stripe.com/session/current-account' })
          )
          fireEvent.click(screen.getByText('updatePayment'))
          await waitFor(() =>
            expect(window.location.assign).toHaveBeenCalledWith(
              'https://billing.stripe.com/session/current-account'
            )
          )
        }
      }
    )

    it('allows retry after a provider failure', async () => {
      await renderPortal(component)
      apiFetch.mockResolvedValueOnce(json({}, 503))
      fireEvent.click(screen.getByText('updatePayment'))
      await screen.findByText('portalError')
      expect(screen.getByText('updatePayment')).not.toBeDisabled()
      apiFetch.mockResolvedValueOnce(
        json({ url: 'https://billing.stripe.com/session/retry' })
      )
      fireEvent.click(screen.getByText('updatePayment'))
      await waitFor(() =>
        expect(window.location.assign).toHaveBeenCalledWith(
          'https://billing.stripe.com/session/retry'
        )
      )
      expect(screen.queryByText('portalError')).toBeNull()
    })
  }
)

async function showCheckout(component: string) {
  if (component === 'onboarding') {
    apiFetch.mockResolvedValueOnce(json(savedProfile()))
    const view = render(<OnboardingPage />)
    fireEvent.click(screen.getByText('next'))
    fireEvent.click(screen.getByText('continue'))
    await screen.findByText('trialNoChargeTrialUsed')
    return { ...view, button: 'trialCtaMonthlyTrialUsed', error: 'trialError' }
  }
  landingState.mockResolvedValueOnce({ subscribed: false, trialUsed: false })
  const view = render(
    <PricingSection
      allowRegistration
      stripeEnabled
      hasSession
      trialDays={0}
      priceMonthly={10}
      priceYearly={100}
      totalPriceMonthly={120}
      totalPriceYearly={100}
    />
  )
  await screen.findAllByText('ctaRegisterTrialUsed')
  return { ...view, button: 'ctaRegisterTrialUsed', error: 'checkoutError' }
}

describe.each(['onboarding', 'landing'])(
  'Checkout recovery in %s',
  (component) => {
    it.each(['active', 'trialing'])(
      'recovers a confirmed %s subscription',
      async (status) => {
        const view = await showCheckout(component)
        apiFetch
          .mockResolvedValueOnce(
            json({ detail: 'subscription_already_active' }, 409)
          )
          .mockResolvedValueOnce(json(savedProfile(status)))
        fireEvent.click(screen.getAllByText(view.button)[0])
        await waitFor(() =>
          expect(useAuthStore.getState().user?.subscription_status).toBe(status)
        )
        expect(screen.queryByText(view.error)).toBeNull()
        expect(window.location.assign).not.toHaveBeenCalled()
        if (component === 'onboarding')
          expect(push).toHaveBeenCalledWith('/dashboard')
        else expect(screen.queryByText('pricingTitle')).toBeNull()
      }
    )

    it.each(['provider', 'profile', 'unsubscribed', 'pending'])(
      'allows retry after %s failure without claiming Premium',
      async (failure) => {
        const view = await showCheckout(component)
        const before = apiFetch.mock.calls.length
        apiFetch.mockResolvedValueOnce(
          json(
            {
              detail:
                failure === 'pending'
                  ? 'subscription_payment_pending'
                  : 'subscription_already_active',
            },
            failure === 'provider' ? 503 : 409
          )
        )
        if (failure === 'profile') apiFetch.mockResolvedValueOnce(json({}, 503))
        if (failure === 'unsubscribed')
          apiFetch.mockResolvedValueOnce(json(savedProfile()))
        fireEvent.click(screen.getAllByText(view.button)[0])
        await screen.findByText(view.error)
        expect(useAuthStore.getState().user?.subscription_status).toBe('none')
        expect(window.location.assign).not.toHaveBeenCalled()
        expect(push).not.toHaveBeenCalled()
        expect(apiFetch.mock.calls.length - before).toBe(
          ['profile', 'unsubscribed'].includes(failure) ? 2 : 1
        )
        expect(
          screen.getAllByText(view.button)[0].closest('button')
        ).not.toBeDisabled()
        apiFetch.mockResolvedValueOnce(
          json({ url: 'https://checkout.stripe.com/retry' })
        )
        fireEvent.click(screen.getAllByText(view.button)[0])
        await waitFor(() =>
          expect(window.location.assign).toHaveBeenCalledWith(
            'https://checkout.stripe.com/retry'
          )
        )
      }
    )

    it.each(['session', 'unmount'])(
      'ignores a recovered profile decoded after %s invalidation',
      async (invalidation) => {
        const view = await showCheckout(component)
        let finish!: (body: unknown) => void
        const body = new Promise((resolve) => {
          finish = resolve
        })
        const decode = vi.fn(() => body)
        apiFetch
          .mockResolvedValueOnce(
            json({ detail: 'subscription_already_active' }, 409)
          )
          .mockResolvedValueOnce({ ok: true, json: decode })
        fireEvent.click(screen.getAllByText(view.button)[0])
        await waitFor(() => expect(decode).toHaveBeenCalledOnce())
        if (invalidation === 'unmount') view.unmount()
        else
          act(() => {
            useAuthStore.getState().startSession('different-account')
            useAuthStore.getState().setUser({ ...profile, id: 2 })
          })
        await act(async () => finish(savedProfile('active')))
        expect(useAuthStore.getState().user?.subscription_status).toBe('none')
        if (invalidation === 'session')
          expect(useAuthStore.getState().user?.id).toBe(2)
        expect(push).not.toHaveBeenCalled()
        expect(window.location.assign).not.toHaveBeenCalled()
        expect(screen.queryByText(view.error)).toBeNull()
      }
    )
  }
)

describe.each(['onboarding', 'paywall', 'dashboard'])(
  'trial eligibility in %s',
  (component) => {
    it.each([
      [0, false],
      [7, false],
      [7, true],
      [0, true],
    ] as const)(
      'uses configured days=%s and previous use=%s',
      async (days, used) => {
        useConfigStore.setState({ stripeTrialDays: days })
        useAuthStore.getState().setUser({ ...profile, trial_used: used })
        const eligible = days > 0 && !used
        if (component === 'onboarding') {
          apiFetch.mockResolvedValueOnce(
            json({ ...savedProfile(), trial_used: used })
          )
          render(<OnboardingPage />)
          fireEvent.click(screen.getByText('next'))
          fireEvent.click(screen.getByText('continue'))
          await screen.findByText(
            eligible ? 'trialNoCharge' : 'trialNoChargeTrialUsed'
          )
          expect(
            screen.getByText(eligible ? 'trialTitle' : 'trialTitleTrialUsed')
          ).toBeInTheDocument()
        } else if (component === 'paywall') {
          render(<PaywallBanner />)
          expect(
            screen.getByText(
              eligible ? 'paywallNoCharge' : 'paywallNoChargeTrialUsed'
            )
          ).toBeInTheDocument()
        } else {
          apiFetch
            .mockResolvedValueOnce(json({}))
            .mockResolvedValueOnce(json({ lessons: [] }))
          render(<DashboardPage />)
          await screen.findByText(
            eligible ? 'premiumBannerDesc' : 'premiumBannerDescTrialUsed'
          )
          expect(
            screen.getByText(
              eligible ? 'premiumBannerCta' : 'premiumBannerCtaTrialUsed'
            )
          ).toBeInTheDocument()
        }
      }
    )
  }
)
