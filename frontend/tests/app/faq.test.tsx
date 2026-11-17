import {
  act,
  cleanup,
  fireEvent,
  render,
  screen,
  within,
} from '@testing-library/react'
import { NextIntlClientProvider } from 'next-intl'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import FAQPage from '@/app/(app)/faq/page'
import { trackBrowserEvent } from '@/lib/analytics'
import { useAuthStore, type User } from '@/store/auth'
import { useConfigStore } from '@/store/config'
import messages from '../../../messages/en.json'

vi.mock('@/lib/analytics', () => ({ trackBrowserEvent: vi.fn() }))

const user: User = {
  id: 1,
  username: 'learner',
  displayName: 'Learner',
  role: 'user',
  conversation_max_duration: 30,
  conversation_inactivity_timeout: 3,
}

function showFAQ() {
  return render(
    <NextIntlClientProvider
      locale="en"
      messages={messages}
      timeZone="UTC"
      onError={(error) => {
        throw error
      }}
    >
      <FAQPage />
    </NextIntlClientProvider>
  )
}

beforeEach(() => {
  useAuthStore.setState({ user })
  useConfigStore.setState(useConfigStore.getInitialState(), true)
  vi.mocked(trackBrowserEvent).mockClear()
})

afterEach(() => {
  cleanup()
  useAuthStore.setState({ user: null })
  useConfigStore.setState(useConfigStore.getInitialState(), true)
})

describe('Authenticated FAQ', () => {
  it('groups every question once and links the new activities to their pages', () => {
    useAuthStore.setState({ user: { ...user, role: 'admin' } })
    useConfigStore.setState({ loaded: true, stripeEnabled: true })
    showFAQ()

    expect(
      screen
        .getAllByRole('heading', { level: 2 })
        .map((node) => node.textContent)
    ).toEqual([
      messages.faq.sectionGettingStarted,
      messages.faq.sectionPractice,
      messages.faq.sectionLingu,
      messages.faq.sectionSubscription,
      messages.faq.sectionAccount,
      messages.faq.sectionAdmin,
    ])
    expect(
      screen
        .getAllByRole('button')
        .map((node) => node.textContent?.replace(/\+$/, '').trim())
        .sort()
    ).toEqual(
      Object.entries(messages.faq)
        .filter(([key]) => key.startsWith('q_'))
        .map(([, question]) => question)
        .sort()
    )

    const practice = within(
      screen.getByRole('region', { name: messages.faq.sectionPractice })
    )
    expect(
      practice.getByRole('button', { name: messages.faq.q_grammarPractice })
    ).toBeVisible()
    expect(
      practice.getByRole('button', { name: messages.faq.q_games })
    ).toBeVisible()
    const lingu = within(
      screen.getByRole('region', { name: messages.faq.sectionLingu })
    )
    expect(
      lingu.getByRole('button', { name: messages.faq.q_memories })
    ).toBeVisible()

    for (const [question, href] of [
      [messages.faq.q_multiLanguage, '/settings/languages'],
      [messages.faq.q_grammarPractice, '/grammar'],
      [messages.faq.q_games, '/games'],
      [messages.faq.q_memories, '/settings/memories'],
      [messages.faq.q_cancelSubscription, '/settings#plan'],
    ]) {
      fireEvent.click(screen.getByRole('button', { name: question }))
      expect(
        within(screen.getByRole('region', { name: question })).getByRole('link')
      ).toHaveAttribute('href', href)
    }
  })

  it('waits for enabled billing configuration without moving the open answer', () => {
    useConfigStore.setState({ stripeEnabled: true, loaded: false })
    showFAQ()
    expect(
      screen.queryByRole('heading', { name: messages.faq.sectionSubscription })
    ).toBeNull()
    expect(
      screen.queryByRole('button', { name: messages.faq.q_plans })
    ).toBeNull()

    const profile = screen.getByRole('button', {
      name: messages.faq.q_password,
    })
    fireEvent.click(profile)
    const answer = screen.getByRole('region', { name: messages.faq.q_password })
    act(() => useConfigStore.setState({ loaded: true }))
    expect(
      screen.getByRole('heading', { name: messages.faq.sectionSubscription })
    ).toBeVisible()
    expect(profile).toHaveAttribute('aria-expanded', 'true')
    expect(answer).toBeVisible()

    act(() => useConfigStore.setState({ stripeEnabled: false }))
    expect(
      screen.queryByRole('heading', { name: messages.faq.sectionSubscription })
    ).toBeNull()
    for (const name of [
      messages.faq.q_plans,
      messages.faq.q_quotas,
      messages.faq.q_cancelSubscription,
    ]) {
      expect(screen.queryByRole('button', { name })).toBeNull()
    }
    expect(answer).toBeVisible()
  })

  it('shows administration questions only to administrators', () => {
    showFAQ()
    expect(
      screen.queryByRole('heading', { name: messages.faq.sectionAdmin })
    ).toBeNull()
    expect(
      screen.queryByRole('button', { name: messages.faq.q_invite })
    ).toBeNull()

    act(() => useAuthStore.setState({ user: { ...user, role: 'admin' } }))
    expect(
      screen.getByRole('heading', { name: messages.faq.sectionAdmin })
    ).toBeVisible()
    fireEvent.click(screen.getByRole('button', { name: messages.faq.q_invite }))
    expect(screen.getByRole('link', { name: 'Admin → Users' })).toHaveAttribute(
      'href',
      '/admin/users'
    )

    act(() => useAuthStore.setState({ user }))
    expect(
      screen.queryByRole('button', { name: messages.faq.q_providers })
    ).toBeNull()
    expect(screen.queryByRole('link', { name: 'Admin → Users' })).toBeNull()
  })

  it('opens one answer across sections and tracks opens but not closes', () => {
    showFAQ()
    const start = screen.getByRole('button', { name: messages.faq.q_start })
    const voice = screen.getByRole('button', { name: messages.faq.q_voice })
    expect(start).toHaveAttribute('aria-expanded', 'false')
    expect(
      screen.queryByRole('region', { name: messages.faq.q_start })
    ).toBeNull()

    fireEvent.click(start)
    const firstAnswer = screen.getByRole('region', {
      name: messages.faq.q_start,
    })
    expect(start).toHaveAttribute('aria-controls', firstAnswer.id)
    expect(firstAnswer).toHaveAttribute('aria-labelledby', start.id)
    fireEvent.click(voice)
    expect(start).toHaveAttribute('aria-expanded', 'false')
    expect(firstAnswer).not.toBeVisible()
    expect(
      screen.getByRole('region', { name: messages.faq.q_voice })
    ).toBeVisible()
    fireEvent.click(voice)
    expect(voice).toHaveAttribute('aria-expanded', 'false')
    expect(
      screen.queryByRole('region', { name: messages.faq.q_voice })
    ).toBeNull()
    expect(trackBrowserEvent).toHaveBeenCalledTimes(2)
    expect(trackBrowserEvent).toHaveBeenCalledWith('faq_viewed')
  })
})
