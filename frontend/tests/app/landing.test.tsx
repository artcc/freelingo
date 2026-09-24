import React from 'react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { cleanup, render, screen, within } from '@testing-library/react'

const { mockHas } = vi.hoisted(() => ({
  mockHas: vi.fn(),
}))

vi.mock('next/headers', () => ({
  cookies: async () => ({ has: mockHas }),
}))

vi.mock('next-intl/server', () => ({
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
  LandingNav: () => null,
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
  LandingReviewsCarousel: () => null,
}))

import Home from '@/app/page'

let config: Record<string, unknown>
let configStatus: number

beforeEach(() => {
  config = { allow_registration: true, stripe_enabled: false }
  configStatus = 200
  mockHas.mockReset().mockReturnValue(false)
  vi.stubGlobal(
    'fetch',
    vi.fn(async (url: string) => {
      const { pathname } = new URL(url)
      if (pathname === '/api/config') {
        return new Response(JSON.stringify(config), { status: configStatus })
      }
      if (pathname === '/api/reviews/public') {
        return new Response(JSON.stringify([]))
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
  it('keeps signup available when optional reviews cannot be fetched', async () => {
    vi.mocked(fetch).mockImplementation(async (url) => {
      if (String(url).endsWith('/api/config')) {
        return new Response(JSON.stringify(config))
      }
      throw new Error('reviews unavailable')
    })
    render(await Home())
    expect(screen.getByRole('link', { name: 'start' })).toHaveAttribute(
      'href',
      '/register'
    )
  })

  it('preserves all public pricing signup links and plan selection when enabled', async () => {
    config.stripe_enabled = true
    render(await Home())
    expect(screen.getByRole('link', { name: 'start' })).toHaveAttribute(
      'href',
      '/register'
    )
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

  it('replaces the hero and every pricing signup CTA with Sign in when closed', async () => {
    config = { allow_registration: false, stripe_enabled: true }
    const { container } = render(await Home())
    expect(container.querySelector('a[href^="/register"]')).toBeNull()
    const links = screen.getAllByRole('link', { name: 'signIn' })
    expect(links).toHaveLength(5)
    links.forEach((link) => expect(link).toHaveAttribute('href', '/login'))
    expect(screen.queryByText('start')).not.toBeInTheDocument()
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
      expect(screen.getByRole('link', { name: 'signIn' })).toHaveAttribute(
        'href',
        '/login'
      )
    }
  )

  it('shows the static microdemo and preserves anonymous CTAs', async () => {
    render(await Home())

    expect(mockHas).toHaveBeenCalledWith('refresh_token')
    const demo = screen.getByRole('region', { name: 'microDemo.title' })
    expect(
      within(demo).getByRole('heading', { name: 'microDemo.title', level: 2 })
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
    expect(screen.getByRole('link', { name: 'start' })).toHaveAttribute(
      'href',
      '/register'
    )
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
      expect(screen.getByRole('link', { name: 'dashboard' })).toHaveAttribute(
        'href',
        '/dashboard'
      )
      expect(
        screen.queryByRole('link', { name: 'start' })
      ).not.toBeInTheDocument()
      expect(screen.getByRole('link', { name: /howItWorks/ })).toHaveAttribute(
        'href',
        '#features'
      )
    }
  )
})
