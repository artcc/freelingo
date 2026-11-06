import React from 'react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from '@testing-library/react'
import { renderToStaticMarkup } from 'react-dom/server'
import { NextIntlClientProvider } from 'next-intl'
import { LandingFAQ } from '@/components/ui/landing-faq'
import FAQPage from '@/app/(app)/faq/page'
import { SUPPORTED_LOCALES } from '@/lib/locales'
import { SUPPORTED_TARGET_LANGUAGES } from '@/lib/target-languages'
import { useAuthStore } from '@/store/auth'
import { useConfigStore } from '@/store/config'
import messages from '../../../messages/en.json'

beforeEach(() => {
  useConfigStore.setState(useConfigStore.getInitialState(), true)
  useAuthStore.setState({ accessToken: null })
  vi.stubGlobal(
    'fetch',
    vi.fn(async (url: RequestInfo | URL) => {
      if (url === '/api/config') {
        return new Response(JSON.stringify({ analytics_enabled: true }))
      }
      if (url === '/api/analytics/public') {
        return new Response(null, { status: 204 })
      }
      throw new Error(`Unexpected request: ${url}`)
    })
  )
})

function FAQ() {
  return (
    <NextIntlClientProvider locale="en" messages={messages}>
      <LandingFAQ />
    </NextIntlClientProvider>
  )
}

afterEach(() => {
  cleanup()
  useConfigStore.setState(useConfigStore.getInitialState(), true)
  vi.unstubAllGlobals()
})

describe('Landing FAQ', () => {
  it.each(SUPPORTED_LOCALES)(
    'lists every language in localized alphabetical order in both FAQs (%s)',
    async (locale) => {
      const catalog = (await import(`../../../messages/${locale}.json`)).default
      const names = SUPPORTED_TARGET_LANGUAGES.map(
        ({ code }) => catalog.targetLanguages[code] as string
      ).sort(new Intl.Collator(locale).compare)
      const list = new Intl.ListFormat(locale, { type: 'conjunction' }).format(names)
      const { container } = render(
        <NextIntlClientProvider locale={locale} messages={catalog}>
          <LandingFAQ />
          <FAQPage />
        </NextIntlClientProvider>
      )

      const publicAnswer = container.querySelector('[id$="-languages-answer"]')
      expect(publicAnswer).toHaveTextContent(
        catalog.landing.faq.languages.answer.replace('{languages}', list)
      )
      fireEvent.click(
        screen.getByRole('button', {
          name: (name) =>
            name.replace(/\s*\+$/, '').replace(/\s+/g, ' ') ===
            catalog.faq.q_language.replace(/\s+/g, ' '),
        })
      )
      expect(container.lastElementChild).toHaveTextContent(
        catalog.faq.a_language.replace('{languages}', list).replace(/\s+/g, ' ')
      )
      expect(container.textContent).not.toContain('{languages}')
      await waitFor(() => expect(useConfigStore.getState().loaded).toBe(true))
    }
  )

  it('changes the list order when the page language changes', async () => {
    const spanish = (await import('../../../messages/es.json')).default
    const { container, rerender } = render(<FAQ />)
    const answer = () => container.querySelector('[id$="-languages-answer"]')

    expect(answer()?.textContent).toMatch(/^American English, British English, Chinese/)
    rerender(
      <NextIntlClientProvider locale="es" messages={spanish}>
        <LandingFAQ />
      </NextIntlClientProvider>
    )
    expect(answer()?.textContent).toMatch(/^Alemán/)
    await waitFor(() => expect(useConfigStore.getState().loaded).toBe(true))
  })

  it('includes answers in the initial HTML without requiring interaction', () => {
    const html = renderToStaticMarkup(<FAQ />)
    const document = new DOMParser().parseFromString(html, 'text/html')
    const answer = document.querySelector('[role="region"]')

    expect(answer?.textContent).toContain(messages.landing.faq.modes.answer)
    expect(answer?.hasAttribute('hidden')).toBe(true)
    expect(document.body.textContent).toContain(
      messages.landing.faq.data.answer
    )
  })

  it('loads public configuration and sends anonymous events for opens, not closes', async () => {
    render(<FAQ />)
    await waitFor(() => expect(useConfigStore.getState().loaded).toBe(true))
    const modes = screen.getByRole('button', {
      name: messages.landing.faq.modes.question,
    })
    const free = screen.getByRole('button', {
      name: messages.landing.faq.free.question,
    })

    expect(screen.queryByRole('region')).toBeNull()
    fireEvent.click(modes)
    const firstAnswer = screen.getByRole('region', {
      name: messages.landing.faq.modes.question,
    })
    expect(modes).toHaveAttribute('aria-expanded', 'true')
    expect(modes).toHaveAttribute('aria-controls', firstAnswer.id)
    expect(firstAnswer).toBeVisible()

    fireEvent.click(free)
    expect(modes).toHaveAttribute('aria-expanded', 'false')
    expect(firstAnswer).not.toBeVisible()
    expect(free).toHaveAttribute('aria-expanded', 'true')
    expect(screen.getByRole('region')).toHaveTextContent(
      messages.landing.faq.free.answer
    )

    fireEvent.click(free)
    expect(free).toHaveAttribute('aria-expanded', 'false')
    expect(screen.queryByRole('region')).toBeNull()
    const events = vi.mocked(fetch).mock.calls.filter(
      ([url]) => url === '/api/analytics/public'
    )
    expect(events).toHaveLength(2)
    for (const [, options] of events) {
      expect(options).toMatchObject({ method: 'POST', credentials: 'omit' })
      expect(new Headers(options?.headers).has('Authorization')).toBe(false)
      expect(JSON.parse(String(options?.body))).toEqual({
        event: 'faq_viewed',
        operation_id: expect.any(String),
      })
    }
  })

  it('keeps answers usable without sending events when analytics is disabled', async () => {
    vi.mocked(fetch).mockResolvedValueOnce(
      new Response(JSON.stringify({ analytics_enabled: false }))
    )
    render(<FAQ />)
    await waitFor(() => expect(useConfigStore.getState().loaded).toBe(true))

    fireEvent.click(
      screen.getByRole('button', {
        name: messages.landing.faq.modes.question,
      })
    )

    expect(screen.getByRole('region')).toHaveTextContent(
      messages.landing.faq.modes.answer
    )
    expect(fetch).toHaveBeenCalledTimes(1)
    expect(fetch).toHaveBeenCalledWith('/api/config')
  })
})
