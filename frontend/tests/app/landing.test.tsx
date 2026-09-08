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

vi.mock('@/components/billing/PricingSection', () => ({
  default: () => null,
}))

vi.mock('@/components/ui/landing-faq', () => ({
  LandingFAQ: () => null,
}))

vi.mock('@/components/ui/landing-nav', () => ({
  LandingNav: () => null,
}))

vi.mock('@/components/ui/scroll-reveal', () => ({
  ScrollReveal: ({ children }: { children: React.ReactNode }) => <>{children}</>,
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

beforeEach(() => {
  mockHas.mockReset().mockReturnValue(false)
  vi.stubGlobal(
    'fetch',
    vi.fn(async (url: string) => {
      const { pathname } = new URL(url)
      if (pathname === '/api/config') {
        return new Response(JSON.stringify({ stripe_enabled: false }))
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

  it('preserves the dashboard CTA for authenticated visitors', async () => {
    mockHas.mockImplementation((name: string) => name === 'refresh_token')

    render(await Home())

    expect(mockHas).toHaveBeenCalledWith('refresh_token')
    expect(screen.getByRole('link', { name: 'dashboard' })).toHaveAttribute(
      'href',
      '/dashboard'
    )
    expect(screen.queryByRole('link', { name: 'start' })).not.toBeInTheDocument()
    expect(screen.getByRole('link', { name: /howItWorks/ })).toHaveAttribute(
      'href',
      '#features'
    )
  })
})
