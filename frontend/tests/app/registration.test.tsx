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
import { useConfigStore } from '@/store/config'
import { useAuthStore } from '@/store/auth'

const { searchParams, push, apiFetch } = vi.hoisted(() => ({
  searchParams: new URLSearchParams(),
  push: vi.fn(),
  apiFetch: vi.fn(),
}))

vi.mock('next/navigation', () => ({
  useRouter: () => ({ push }),
  useSearchParams: () => searchParams,
}))

vi.mock('next-intl', () => ({
  useTranslations: (namespace: string) => (key: string) =>
    `${namespace}.${key}`,
}))

vi.mock('next/link', () => ({
  default: ({
    href,
    children,
    ...props
  }: React.AnchorHTMLAttributes<HTMLAnchorElement>) =>
    React.createElement('a', { href, ...props }, children),
}))

vi.mock('@/lib/api', () => ({ apiFetch }))

import RegisterPage from '@/app/(auth)/register/page'
import LoginPage from '@/app/(auth)/login/page'
import PrivacyPage from '@/app/(legal)/privacy/page'
import TermsPage from '@/app/(legal)/terms/page'

function configResponse(allowRegistration: boolean) {
  return new Response(JSON.stringify({ allow_registration: allowRegistration }))
}

beforeEach(() => {
  for (const key of Array.from(searchParams.keys())) searchParams.delete(key)
  push.mockReset()
  apiFetch.mockReset()
  useConfigStore.setState({ ...useConfigStore.getInitialState() }, true)
  useAuthStore.setState({ accessToken: null, user: null })
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(configResponse(false)))
})

afterEach(() => {
  cleanup()
  vi.unstubAllGlobals()
})

async function fillAndSubmit(container: HTMLElement) {
  const form = container.querySelector('form')!
  const inputs = form.querySelectorAll('input')
  // Existing form order: username, display name, email, passwords, legal acceptance.
  const values = [
    'learner',
    'Learner',
    'learner@example.com',
    'Test1234!@',
    'Test1234!@',
  ]
  values.forEach((value, index) =>
    fireEvent.change(inputs[index], { target: { value } })
  )
  fireEvent.click(screen.getByRole('checkbox'))
  await act(async () => fireEvent.submit(form))
}

describe('registration availability', () => {
  it('shows loading without flashing a form or closed message, then opens public signup', async () => {
    let resolveConfig!: (response: Response) => void
    vi.mocked(fetch).mockReturnValueOnce(
      new Promise((resolve) => {
        resolveConfig = resolve
      })
    )
    const { container } = render(<RegisterPage />)
    expect(
      screen.getByRole('status', { name: 'common.loading' })
    ).toBeInTheDocument()
    expect(container.querySelector('form')).toBeNull()
    expect(
      screen.queryByText('auth.register.registrationClosed')
    ).not.toBeInTheDocument()

    await act(async () => resolveConfig(configResponse(true)))
    expect(
      screen.getByRole('button', { name: 'auth.register.submit' })
    ).toBeInTheDocument()
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
    expect(fetch).toHaveBeenCalledWith('/api/config')
  })

  it.each(['', 'invite='])(
    'shows the closed state without a supplied invite (%s)',
    async (query) => {
      if (query) searchParams.set('invite', '')
      const { container } = render(<RegisterPage />)
      expect(
        await screen.findByText('auth.register.registrationClosed')
      ).toBeInTheDocument()
      expect(
        screen.getByRole('link', { name: 'auth.register.login' })
      ).toHaveAttribute('href', '/login')
      expect(container.querySelector('form')).toBeNull()
      expect(apiFetch).not.toHaveBeenCalled()
    }
  )

  it.each(['network', 'HTTP', 'missing flag'])(
    'keeps ordinary signup closed after a %s failure',
    async (failure) => {
      if (failure === 'network')
        vi.mocked(fetch).mockRejectedValueOnce(new Error('offline'))
      if (failure === 'HTTP')
        vi.mocked(fetch).mockResolvedValueOnce(
          new Response('', { status: 503 })
        )
      if (failure === 'missing flag')
        vi.mocked(fetch).mockResolvedValueOnce(new Response('{}'))
      const { container } = render(<RegisterPage />)
      expect(
        await screen.findByText('auth.register.registrationClosed')
      ).toBeInTheDocument()
      expect(container.querySelector('form')).toBeNull()
      expect(screen.queryByRole('status')).not.toBeInTheDocument()
    }
  )

  it('opens an unvalidated invite immediately even while config is unavailable', async () => {
    searchParams.set('invite', 'supplied-token')
    vi.mocked(fetch).mockReturnValueOnce(new Promise(() => {}))
    render(<RegisterPage />)
    expect(
      screen.getByRole('button', { name: 'auth.register.submit' })
    ).toBeInTheDocument()
    expect(
      screen.queryByText('auth.register.registrationClosed')
    ).not.toBeInTheDocument()
    expect(apiFetch).not.toHaveBeenCalled()
  })

  it.each([null, 'monthly', 'yearly'])(
    'preserves public registration and onboarding plan=%s',
    async (plan) => {
      vi.mocked(fetch).mockResolvedValueOnce(configResponse(true))
      if (plan) searchParams.set('plan', plan)
      apiFetch.mockResolvedValueOnce(
        new Response(JSON.stringify({ access_token: 'new-token' }))
      )
      const { container } = render(<RegisterPage />)
      await screen.findByRole('button', { name: 'auth.register.submit' })
      await fillAndSubmit(container)
      expect(apiFetch).toHaveBeenCalledWith(
        '/api/auth/register',
        expect.objectContaining({ method: 'POST' })
      )
      expect(JSON.parse(apiFetch.mock.calls[0][1].body)).not.toHaveProperty(
        'invite_token'
      )
      expect(useAuthStore.getState().accessToken).toBe('new-token')
      expect(push).toHaveBeenCalledWith(
        plan ? `/onboarding?plan=${plan}` : '/onboarding'
      )
    }
  )

  it.each([true, false])(
    'passes an invite to the backend and respects its decision (accepted=%s)',
    async (accepted) => {
      searchParams.set('invite', 'unvalidated-token')
      apiFetch.mockResolvedValueOnce(
        new Response(
          JSON.stringify(
            accepted
              ? { access_token: 'invited-token' }
              : { detail: 'Invalid or expired invite' }
          ),
          { status: accepted ? 200 : 403 }
        )
      )
      const { container } = render(<RegisterPage />)
      await waitFor(() => expect(useConfigStore.getState().loaded).toBe(true))
      expect(
        screen.queryByText('auth.register.registrationClosed')
      ).not.toBeInTheDocument()
      await fillAndSubmit(container)
      expect(JSON.parse(apiFetch.mock.calls[0][1].body).invite_token).toBe(
        'unvalidated-token'
      )
      if (accepted) {
        expect(push).toHaveBeenCalledWith('/onboarding')
      } else {
        expect(
          await screen.findByText(/auth.register.invalidInvite/)
        ).toBeInTheDocument()
        expect(push).not.toHaveBeenCalled()
        expect(useAuthStore.getState().accessToken).toBeNull()
      }
    }
  )

  it.each([true, false])(
    'shows the login signup link only for registration=%s',
    async (allowRegistration) => {
      vi.mocked(fetch).mockResolvedValueOnce(configResponse(allowRegistration))
      render(<LoginPage />)
      await waitFor(() => expect(useConfigStore.getState().loaded).toBe(true))
      if (allowRegistration) {
        expect(
          screen.getByRole('link', { name: 'auth.login.register' })
        ).toHaveAttribute('href', '/register')
      } else {
        expect(
          screen.queryByRole('link', { name: 'auth.login.register' })
        ).not.toBeInTheDocument()
        expect(
          screen.queryByText('auth.login.noAccount')
        ).not.toBeInTheDocument()
      }
      expect(
        screen.getByRole('button', { name: 'auth.login.submit' })
      ).toBeInTheDocument()
      expect(
        screen.getByRole('link', { name: 'auth.login.forgotPassword' })
      ).toHaveAttribute('href', '/forgot-password')
    }
  )

  it('preserves the supplied invite in registration legal links', async () => {
    searchParams.set('invite', 'token+with/symbols')
    render(<RegisterPage />)
    await waitFor(() => expect(useConfigStore.getState().loaded).toBe(true))
    for (const page of ['terms', 'privacy']) {
      expect(
        screen.getByRole('link', { name: `auth.register.${page}Link` })
      ).toHaveAttribute(
        'href',
        `/${page}?from=register&invite=token%2Bwith%2Fsymbols`
      )
    }
  })
})

describe.each([
  ['privacy', PrivacyPage, 'terms'],
  ['terms', TermsPage, 'privacy'],
] as const)('%s return navigation', (page, Page, other) => {
  it.each([true, false])(
    'returns ordinary visitors appropriately for registration=%s',
    async (allowRegistration) => {
      searchParams.set('from', 'register')
      vi.mocked(fetch).mockResolvedValueOnce(configResponse(allowRegistration))
      const { container } = render(<Page />)
      await waitFor(() => expect(useConfigStore.getState().loaded).toBe(true))
      if (allowRegistration) {
        expect(
          screen.getByRole('link', { name: `legal.${page}.linkBack` })
        ).toHaveAttribute('href', '/register')
      } else {
        expect(container.querySelector('a[href^="/register"]')).toBeNull()
        expect(
          screen.getByRole('link', { name: 'auth.register.login' })
        ).toHaveAttribute('href', '/login')
      }
    }
  )

  it('preserves invites between legal pages and back to the form when closed', async () => {
    searchParams.set('from', 'register')
    searchParams.set('invite', 'token+with/symbols')
    render(<Page />)
    await waitFor(() => expect(useConfigStore.getState().loaded).toBe(true))
    expect(
      screen.getByRole('link', { name: `legal.${page}.linkBack` })
    ).toHaveAttribute('href', '/register?invite=token%2Bwith%2Fsymbols')
    expect(
      screen.getByRole('link', {
        name: `legal.${page}.link${other === 'terms' ? 'Terms' : 'Privacy'}`,
      })
    ).toHaveAttribute(
      'href',
      `/${other}?from=register&invite=token%2Bwith%2Fsymbols`
    )
  })

  it('preserves the authenticated Settings return link', () => {
    searchParams.set('from', 'settings')
    render(<Page />)
    expect(
      screen.getByRole('link', { name: `legal.${page}.linkBackSettings` })
    ).toHaveAttribute('href', '/settings')
    expect(fetch).not.toHaveBeenCalled()
  })
})
