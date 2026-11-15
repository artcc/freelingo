import React from 'react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { cleanup, render, screen, within } from '@testing-library/react'
import type { ReviewPublic, ReviewPublicSummary } from '@/types/api'
import { SUPPORTED_TARGET_LANGUAGES } from '@/lib/target-languages'

const { mockHas, mockLandingNav, mockReviewsCarousel } = vi.hoisted(() => ({
  mockHas: vi.fn(),
  mockLandingNav: vi.fn(() => null),
  mockReviewsCarousel: vi.fn(() => null),
}))

vi.mock('next/headers', () => ({
  cookies: async () => ({ has: mockHas }),
}))

vi.mock('next-intl/server', () => ({
  getLocale: async () => 'en',
  getTranslations: async () => (key: string) => key,
}))

vi.mock('next/link', () => ({
  default: ({
    href,
    children,
    ...props
  }: React.AnchorHTMLAttributes<HTMLAnchorElement>) =>
    React.createElement('a', { href, ...props }, children),
}))

vi.mock('next-intl', () => ({
  useLocale: () => 'en',
  useTranslations: () => (key: string) => key,
}))

vi.mock('@/lib/landing-subscription', () => ({
  getLandingSubscriptionState: async () => ({
    subscribed: true,
    trialUsed: false,
  }),
}))

vi.mock('@/components/ui/landing-faq', () => ({
  LandingFAQ: () => null,
}))

vi.mock('@/components/ui/landing-nav', () => ({
  LandingNav: mockLandingNav,
}))

vi.mock('@/components/ui/scroll-reveal', () => ({
  ScrollReveal: ({ children }: { children: React.ReactNode }) => (
    <>{children}</>
  ),
}))

vi.mock('@/components/ui/contact-button', () => ({
  ContactButton: () => null,
}))

vi.mock('@/components/LanguageBubbles', () => ({
  LanguageBubbles: () => null,
}))

vi.mock('@/components/reviews/LandingReviewsCarousel', () => ({
  LandingReviewsCarousel: mockReviewsCarousel,
}))

import Home from '@/app/page'

let config: Record<string, unknown>
let configStatus: number
let reviews: ReviewPublic[]
let reviewSummary: ReviewPublicSummary

beforeEach(() => {
  config = {
    allow_registration: true,
    stripe_enabled: false,
    stripe_trial_days: 7,
  }
  configStatus = 200
  reviews = []
  reviewSummary = { total: 0, average_rating: null }
  mockLandingNav.mockClear()
  mockReviewsCarousel.mockClear()
  mockHas.mockReset().mockReturnValue(false)
  vi.stubGlobal(
    'fetch',
    vi.fn(async (url: string) => {
      const { pathname } = new URL(url)
      if (pathname === '/api/config') {
        return new Response(JSON.stringify(config), { status: configStatus })
      }
      if (pathname === '/api/reviews/public') {
        return new Response(JSON.stringify(reviews))
      }
      if (pathname === '/api/reviews/public/summary') {
        return new Response(JSON.stringify(reviewSummary))
      }
      throw new Error(`Unexpected fetch: ${url}`)
    })
  )
})

afterEach(() => {
  cleanup()
  vi.unstubAllGlobals()
})

describe('Landing Home', () => {
  it('shows reviews navigation and the full summary even without comments', async () => {
    reviewSummary = { total: 128, average_rating: 4.9 }

    render(await Home())

    expect(mockLandingNav).toHaveBeenCalledWith(
      expect.objectContaining({ showReviews: true }),
      undefined
    )
    expect(mockReviewsCarousel).toHaveBeenCalledWith(
      { reviews: [], summary: reviewSummary },
      undefined
    )
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining('/api/reviews/public/summary'),
      { next: { revalidate: 300 } }
    )
  })

  it('hides reviews navigation when there are no approved ratings or comments', async () => {
    render(await Home())

    expect(mockLandingNav).toHaveBeenCalledWith(
      expect.objectContaining({ showReviews: false }),
      undefined
    )
  })

  it.each(['network', 'HTTP', 'JSON'])(
    'keeps comments when the summary has a %s failure',
    async (failure) => {
      reviews = [
        {
          id: 1,
          user_display_name: 'Ada',
          target_language: 'en-GB',
          rating: 5,
          comment: 'Excellent practice',
          created_at: '2026-10-20',
        },
      ]
      const originalFetch = vi.mocked(fetch).getMockImplementation()!
      vi.mocked(fetch).mockImplementation(async (...args) => {
        if (String(args[0]).endsWith('/api/reviews/public/summary')) {
          if (failure === 'network') throw new Error('summary unavailable')
          if (failure === 'HTTP') return new Response(null, { status: 503 })
          return new Response('invalid JSON')
        }
        return originalFetch(...args)
      })

      render(await Home())

      expect(mockReviewsCarousel).toHaveBeenCalledWith(
        { reviews, summary: null },
        undefined
      )
      expect(mockLandingNav).toHaveBeenCalledWith(
        expect.objectContaining({ showReviews: true }),
        undefined
      )
    }
  )

  it('keeps the summary visible when comments cannot be fetched', async () => {
    reviewSummary = { total: 128, average_rating: 4.9 }
    const originalFetch = vi.mocked(fetch).getMockImplementation()!
    vi.mocked(fetch).mockImplementation(async (...args) => {
      if (String(args[0]).includes('/api/reviews/public?')) {
        throw new Error('comments unavailable')
      }
      return originalFetch(...args)
    })

    render(await Home())

    expect(mockReviewsCarousel).toHaveBeenCalledWith(
      { reviews: [], summary: reviewSummary },
      undefined
    )
    expect(mockLandingNav).toHaveBeenCalledWith(
      expect.objectContaining({ showReviews: true }),
      undefined
    )
  })

  it('renders the main learning content and one H1 in the server response', async () => {
    render(await Home())
    const main = screen.getByRole('main')
    expect(screen.getAllByRole('heading', { level: 1 })).toHaveLength(1)
    expect(within(main).getByRole('heading', { level: 1 })).toHaveTextContent(
      'hero'
    )
    expect(within(main).getByText('journey.learnDesc')).toBeInTheDocument()
    expect(within(main).getByText('journey.practiceDesc')).toBeInTheDocument()
    expect(within(main).getByText('journey.speakDesc')).toBeInTheDocument()
    expect(main.querySelector('.reveal h1')).toBeNull()
    const languages = within(main).getByRole('region', { name: 'subtitle' })
    expect(within(languages).getAllByRole('listitem')).toHaveLength(
      SUPPORTED_TARGET_LANGUAGES.length
    )
    for (const language of SUPPORTED_TARGET_LANGUAGES) {
      expect(within(languages).getByText(language.code)).toBeVisible()
    }
  })

  it.each([
    { registration: true, session: false, offer: true },
    { registration: false, session: false, offer: false },
    { registration: true, session: true, offer: false },
  ])(
    'only marks up a free offer when signup is visible: %j',
    async ({ registration, session, offer }) => {
      config.allow_registration = registration
      mockHas.mockReturnValue(session)
      const { container } = render(await Home())
      const scripts = container.querySelectorAll(
        'script[type="application/ld+json"]'
      )
      expect(scripts).toHaveLength(1)
      const data = JSON.parse(scripts[0].textContent ?? '')
      const app = data['@graph'].find(
        (node: { '@type': string }) => node['@type'] === 'WebApplication'
      )
      const website = data['@graph'].find(
        (node: { '@type': string }) => node['@type'] === 'WebSite'
      )
      expect(app.applicationCategory).toBe('EducationalApplication')
      expect(website.about['@id']).toBe(app['@id'])
      expect(app.url).toBe('https://freelingo.app/')
      expect(app.inLanguage).toBe('en')
      expect(app.aggregateRating).toBeUndefined()
      expect(app.review).toBeUndefined()
      if (offer) {
        expect(app.offers.price).toBe(0)
        expect(app.offers.priceCurrency).toBeUndefined()
        expect(
          screen.getAllByRole('link', { name: app.offers.name })
        ).toHaveLength(2)
      } else {
        expect(app.offers).toBeUndefined()
      }
    }
  )

  it('keeps signup available when optional reviews cannot be fetched', async () => {
    vi.mocked(fetch).mockImplementation(async (url) => {
      if (String(url).endsWith('/api/config')) {
        return new Response(JSON.stringify(config))
      }
      throw new Error('reviews unavailable')
    })
    render(await Home())
    const links = screen.getAllByRole('link', { name: 'startFree' })
    expect(links).toHaveLength(2)
    links.forEach((link) => expect(link).toHaveAttribute('href', '/register'))
  })

  it('preserves all public pricing signup links and plan selection when enabled', async () => {
    config.stripe_enabled = true
    render(await Home())
    const links = screen.getAllByRole('link', { name: 'startFree' })
    expect(links).toHaveLength(2)
    links.forEach((link) => expect(link).toHaveAttribute('href', '/register'))
    expect(screen.getByRole('link', { name: 'planFreeCta' })).toHaveAttribute(
      'href',
      '/register'
    )
    expect(
      screen
        .getAllByRole('link', { name: 'ctaRegister' })
        .map((link) => link.getAttribute('href'))
    ).toEqual([
      '/register?plan=monthly',
      '/register?plan=yearly',
      '/register?plan=yearly',
    ])
  })

  it('distinguishes the study plan from limited lessons and games', async () => {
    config.stripe_enabled = true
    render(await Home())

    const table = screen.getByRole('table')
    expect(screen.getByText('pricingContext')).toBeInTheDocument()
    for (const label of ['freeFeature.lessons', 'freeFeature.games']) {
      const row = within(table).getByRole('row', {
        name: `${label} limitedLabel`,
      })
      expect(within(row).getAllByRole('cell')[1]).toHaveTextContent(
        'limitedLabel'
      )
    }
    const studyPlan = within(table).getByRole('row', { name: 'freeFeature.f2' })
    expect(within(studyPlan).queryByText('limitedLabel')).toBeNull()
    expect(within(table).queryByText('freeFeature.l5')).toBeNull()
  })

  it.each([0, 7])(
    'shows card-trial terms only when configured trial days are positive: %s',
    async (days) => {
      config.stripe_enabled = true
      config.stripe_trial_days = days
      render(await Home())

      expect(screen.queryAllByText('paywallNoCharge')).toHaveLength(
        days > 0 ? 2 : 0
      )
      expect(screen.queryAllByText('paywallNoChargeTrialUsed')).toHaveLength(
        days > 0 ? 0 : 2
      )
      expect(screen.queryAllByText('ctaRegister')).toHaveLength(
        days > 0 ? 3 : 0
      )
    }
  )

  it.each([true, false])(
    'describes the no-card signup period independently of Stripe trial days: %s',
    async (freemiumTrialEnabled) => {
      config.stripe_enabled = true
      config.stripe_trial_days = 0
      config.freemium_trial_enabled = freemiumTrialEnabled
      render(await Home())

      expect(screen.queryAllByText('freeTrialNote')).toHaveLength(
        freemiumTrialEnabled ? 2 : 0
      )
      expect(screen.queryAllByText('freeNote')).toHaveLength(
        freemiumTrialEnabled ? 0 : 2
      )
      expect(
        screen.getByText(
          freemiumTrialEnabled ? 'planFreeTrialDesc' : 'planFreeDesc'
        )
      ).toBeInTheDocument()
      expect(screen.getByText('pricingDescTrialUsed')).toBeInTheDocument()
      expect(screen.queryByText('trialBadge')).toBeNull()
      expect(screen.queryByText('ctaRegister')).toBeNull()
      expect(screen.queryByText('paywallNoCharge')).toBeNull()
    }
  )

  it('does not advertise a signup trial when billing is disabled', async () => {
    config.freemium_trial_enabled = true
    render(await Home())

    expect(screen.queryByText('freeTrialNote')).toBeNull()
    expect(screen.queryByText('planFreeTrialDesc')).toBeNull()
    expect(screen.queryByText('pricingTitle')).toBeNull()
  })

  it('does not invent a Stripe trial when its duration is missing', async () => {
    config.stripe_enabled = true
    delete config.stripe_trial_days
    render(await Home())

    expect(screen.queryByText('trialBadge')).toBeNull()
    expect(screen.getAllByText('ctaRegisterTrialUsed')).toHaveLength(3)
  })

  it('keeps Cloud access distinct from closed registration on the current instance', async () => {
    config.allow_registration = false
    const { container } = render(await Home())

    const modes = screen.getByRole('region', { name: 'modes.title' })
    expect(within(modes).getByText('modes.accounts')).toBeInTheDocument()
    expect(screen.queryByText('pricingTitle')).toBeNull()
    expect(
      within(modes).getByRole('link', { name: 'modes.cloud.cta' })
    ).toHaveAttribute('href', 'https://freelingo.app/login')
    expect(
      within(modes).getByRole('link', { name: 'modes.selfHosted.cta' })
    ).toHaveAttribute('href', 'https://github.com/artcc/freelingo#quick-start')
    expect(container.querySelector('a[href^="/register"]')).toBeNull()
  })

  it('preserves pricing plan selection when closed signup CTAs become Sign in', async () => {
    config = { allow_registration: false, stripe_enabled: true }
    const { container } = render(await Home())
    expect(container.querySelector('a[href^="/register"]')).toBeNull()
    const links = screen.getAllByRole('link', { name: 'signIn' })
    expect(links).toHaveLength(6)
    const pricing = container.querySelector<HTMLElement>('#pricing')!
    const pricingLinks = within(pricing).getAllByRole('link', {
      name: 'signIn',
    })
    expect(pricingLinks).toHaveLength(4)
    const [freePlan, monthlyPlan, yearlyPlan, pricingCta] = pricingLinks
    expect(freePlan).toHaveAttribute('href', '/login')
    expect(monthlyPlan).toHaveAttribute('href', '/login?plan=monthly')
    expect(yearlyPlan).toHaveAttribute('href', '/login?plan=yearly')
    expect(pricingCta).toHaveAttribute('href', '/login?plan=yearly')
    const genericLinks = links.filter((link) => !pricing.contains(link))
    expect(genericLinks).toHaveLength(2)
    genericLinks.forEach((link) =>
      expect(link).toHaveAttribute('href', '/login')
    )
    expect(screen.queryByText('startFree')).not.toBeInTheDocument()
    expect(screen.queryByText('freeNote')).not.toBeInTheDocument()
    expect(screen.queryByText('ctaRegister')).not.toBeInTheDocument()
  })

  it.each(['missing flag', 'HTTP error', 'network error'])(
    'does not advertise signup on %s',
    async (failure) => {
      config = {}
      if (failure === 'HTTP error') configStatus = 503
      if (failure === 'network error')
        vi.mocked(fetch).mockRejectedValue(new Error('offline'))
      const { container } = render(await Home())
      expect(container.querySelector('a[href^="/register"]')).toBeNull()
      const links = screen.getAllByRole('link', { name: 'signIn' })
      expect(links).toHaveLength(2)
      links.forEach((link) => expect(link).toHaveAttribute('href', '/login'))
    }
  )

  it('shows the static microdemo and preserves anonymous CTAs', async () => {
    render(await Home())

    expect(mockHas).toHaveBeenCalledWith('refresh_token')
    const demo = screen.getByRole('region', { name: 'microDemo.title' })
    expect(
      within(demo).getByRole('heading', { name: 'microDemo.title', level: 3 })
    ).toBeInTheDocument()

    const phrases = demo.querySelectorAll('p[lang]')
    expect(phrases).toHaveLength(3)
    phrases.forEach((phrase) => {
      expect(phrase).toHaveAttribute('lang', 'en-GB')
    })
    expect(
      Array.from(phrases, (phrase) =>
        phrase.textContent?.replace(/\s+/g, ' ').trim()
      )
    ).toEqual([
      'What did you do yesterday?',
      'Yesterday I go to the park.',
      'Yesterday I went to the park.',
    ])
    expect(within(demo).queryByRole('button')).not.toBeInTheDocument()
    expect(demo.querySelector('button, input')).toBeNull()
    const links = screen.getAllByRole('link', { name: 'startFree' })
    expect(links).toHaveLength(2)
    links.forEach((link) => expect(link).toHaveAttribute('href', '/register'))
    expect(screen.getByRole('link', { name: /howItWorks/ })).toHaveAttribute(
      'href',
      '#features'
    )
  })

  it.each([true, false])(
    'preserves the dashboard CTA with registration=%s',
    async (allowRegistration) => {
      config.allow_registration = allowRegistration
      mockHas.mockImplementation((name: string) => name === 'refresh_token')

      render(await Home())

      expect(mockHas).toHaveBeenCalledWith('refresh_token')
      const links = screen.getAllByRole('link', { name: 'dashboard' })
      expect(links).toHaveLength(2)
      links.forEach((link) =>
        expect(link).toHaveAttribute('href', '/dashboard')
      )
      expect(
        screen.queryByRole('link', { name: 'startFree' })
      ).not.toBeInTheDocument()
      expect(screen.queryByText('freeNote')).not.toBeInTheDocument()
      expect(screen.getByRole('link', { name: /howItWorks/ })).toHaveAttribute(
        'href',
        '#features'
      )
    }
  )

  it.each([true, false])(
    'shows free-access limits beside both CTAs only with Stripe enabled=%s',
    async (stripeEnabled) => {
      config.stripe_enabled = stripeEnabled
      render(await Home())
      expect(screen.queryAllByText('freeNote')).toHaveLength(
        stripeEnabled ? 2 : 0
      )
    }
  )
})
