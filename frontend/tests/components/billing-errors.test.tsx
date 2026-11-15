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
import { NextIntlClientProvider } from 'next-intl'
import { useAuthStore, type User } from '@/store/auth'
import { useConfigStore } from '@/store/config'
import { useLanguageStore } from '@/store/language'
import en from '../../../messages/en.json'
import es from '../../../messages/es.json'

const { apiFetch, push } = vi.hoisted(() => ({
  apiFetch: vi.fn(),
  push: vi.fn(),
}))

vi.mock('@/lib/api', () => ({ apiFetch, restoreAccessToken: vi.fn() }))
vi.mock('@/lib/landing-subscription', () => ({
  getLandingSubscriptionState: async () => ({
    subscribed: false,
    trialUsed: true,
  }),
}))
vi.mock('next/navigation', () => ({
  useRouter: () => ({ push }),
  useSearchParams: () => new URLSearchParams('plan=monthly'),
}))
vi.mock('next/link', () => ({
  default: ({
    href,
    children,
    ...props
  }: React.AnchorHTMLAttributes<HTMLAnchorElement>) =>
    React.createElement('a', { href, ...props }, children),
}))

import { SubscriptionPlanButtons } from '@/components/billing/SubscriptionPlanButtons'
import { PaywallBanner } from '@/components/billing/PaywallBanner'
import { BillingSection } from '@/components/settings/BillingSection'
import PricingSection from '@/components/billing/PricingSection'
import OnboardingPage from '@/app/(auth)/onboarding/page'
import BillingSuccessPage from '@/app/(auth)/billing/success/page'

const catalogs = { en, es }
const technicalDetail = 'StripeAPIError: internal request req_private failed'
const learner: User = {
  id: 1,
  username: 'learner',
  displayName: 'Learner',
  role: 'user',
  conversation_max_duration: 900,
  conversation_inactivity_timeout: 60,
  learning_goals: [],
  subscription_status: 'none',
  trial_used: true,
}

beforeEach(() => {
  apiFetch.mockReset()
  push.mockReset()
  useAuthStore.setState(
    { ...useAuthStore.getInitialState(), accessToken: 'token', user: learner },
    true
  )
  useConfigStore.setState(
    {
      ...useConfigStore.getInitialState(),
      loaded: true,
      stripeEnabled: true,
      stripeTrialDays: 0,
    },
    true
  )
  useLanguageStore.setState(
    {
      ...useLanguageStore.getInitialState(),
      availableLanguageCodes: ['en-GB'],
      fetchLanguages: vi.fn().mockResolvedValue(true),
    },
    true
  )
})

afterEach(() => cleanup())

function renderLocalized(
  content: React.ReactNode,
  locale: keyof typeof catalogs
) {
  return render(
    <NextIntlClientProvider
      locale={locale}
      messages={catalogs[locale]}
      timeZone="UTC"
    >
      {content}
    </NextIntlClientProvider>
  )
}

function failRequest(mode: 'http' | 'network') {
  if (mode === 'network') {
    apiFetch.mockRejectedValueOnce(new Error(technicalDetail))
  } else {
    apiFetch.mockResolvedValueOnce(
      new Response(JSON.stringify({ detail: technicalDetail }), { status: 503 })
    )
  }
}

describe.each(['es', 'en'] as const)('localized billing errors (%s)', (locale) => {
  it.each(['plans', 'paywall', 'settings', 'pricing'] as const)(
    'discards backend details in %s checkout',
    async (component) => {
      failRequest('http')
      const components = {
        plans: <SubscriptionPlanButtons />,
        paywall: <PaywallBanner />,
        settings: <BillingSection />,
        pricing: (
          <PricingSection
            allowRegistration
            stripeEnabled
            hasSession
            trialDays={0}
            priceMonthly={10}
            priceYearly={100}
            totalPriceMonthly={10}
            totalPriceYearly={100}
          />
        ),
      }
      renderLocalized(components[component], locale)
      const buttons = await screen.findAllByRole('button')
      await act(async () => fireEvent.click(buttons[0]))
      expect(
        screen.getByText(catalogs[locale].billing.checkoutError)
      ).toBeInTheDocument()
      expect(
        screen.queryByText(technicalDetail, { exact: false })
      ).not.toBeInTheDocument()
      expect(screen.getAllByRole('button')[0]).toBeEnabled()
      expect(apiFetch).toHaveBeenCalledWith(
        '/api/billing/checkout',
        expect.any(Object)
      )
      expect(push).not.toHaveBeenCalled()
    }
  )

  it.each(['http', 'network'] as const)(
    'shows a translated portal error after %s failure',
    async (mode) => {
      useAuthStore.setState({
        user: { ...learner, subscription_status: 'active' },
      })
      failRequest(mode)
      renderLocalized(<BillingSection />, locale)
      const button = screen.getByRole('button', {
        name: catalogs[locale].billing.manage,
      })
      await act(async () => fireEvent.click(button))
      expect(
        screen.getByText(catalogs[locale].billing.portalError)
      ).toBeInTheDocument()
      expect(
        screen.queryByText(technicalDetail, { exact: false })
      ).not.toBeInTheDocument()
      expect(button).toBeEnabled()
      expect(apiFetch).toHaveBeenCalledWith(
        '/api/billing/portal',
        expect.any(Object)
      )
    }
  )

  it('discards exceptions during onboarding checkout', async () => {
    apiFetch.mockResolvedValueOnce(
      new Response(JSON.stringify({ ...learner, display_name: 'Learner' }))
    )
    renderLocalized(<OnboardingPage />, locale)
    await waitFor(() =>
      expect(
        screen.getByRole('button', { name: catalogs[locale].common.next })
      ).toBeEnabled()
    )
    await act(async () =>
      fireEvent.click(
        screen.getByRole('button', { name: catalogs[locale].common.next })
      )
    )
    await act(async () =>
      fireEvent.click(
        screen.getByRole('button', {
          name: catalogs[locale].onboarding.continue,
        })
      )
    )
    failRequest('network')
    await act(async () => fireEvent.click(screen.getAllByRole('button')[0]))
    expect(
      screen.getByText(catalogs[locale].onboarding.trialError)
    ).toBeInTheDocument()
    expect(
      screen.queryByText(technicalDetail, { exact: false })
    ).not.toBeInTheDocument()
    expect(push).not.toHaveBeenCalled()
  })

  it('discards backend details when saving onboarding preferences', async () => {
    failRequest('http')
    renderLocalized(<OnboardingPage />, locale)
    await waitFor(() =>
      expect(
        screen.getByRole('button', { name: catalogs[locale].common.next })
      ).toBeEnabled()
    )
    await act(async () =>
      fireEvent.click(
        screen.getByRole('button', { name: catalogs[locale].common.next })
      )
    )
    await act(async () =>
      fireEvent.click(
        screen.getByRole('button', {
          name: catalogs[locale].onboarding.continue,
        })
      )
    )
    expect(
      screen.getByText(`✕ ${catalogs[locale].onboarding.saveFailed}`)
    ).toBeInTheDocument()
    expect(
      screen.queryByText(technicalDetail, { exact: false })
    ).not.toBeInTheDocument()
    expect(push).not.toHaveBeenCalled()
  })

  it('shows a translated confirmation error without publishing technical details', async () => {
    failRequest('network')
    renderLocalized(<BillingSuccessPage />, locale)
    expect(
      await screen.findByText(catalogs[locale].billing.successErrorTitle)
    ).toBeInTheDocument()
    expect(
      screen.getByText(catalogs[locale].billing.successErrorDesc)
    ).toBeInTheDocument()
    expect(
      screen.queryByText(technicalDetail, { exact: false })
    ).not.toBeInTheDocument()
    expect(push).not.toHaveBeenCalled()
  })
})
