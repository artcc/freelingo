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
  it.each(['replace-session', 'unmount'])(
    'ignores a late login profile after %s',
    async (action) => {
      searchParams.set('plan', 'yearly')
      let finish!: (body: unknown) => void
      apiFetch
        .mockResolvedValueOnce(
          new Response(JSON.stringify({ access_token: 'first-token' }))
        )
        .mockResolvedValueOnce({
          ok: true,
          json: () =>
            new Promise((resolve) => {
              finish = resolve
            }),
        })
      const { container, unmount } = render(<LoginPage />)
      fireEvent.change(
        container.querySelector('input[autocomplete="username"]')!,
        {
          target: { value: 'user@example.com' },
        }
      )
      fireEvent.change(container.querySelector('input[type="password"]')!, {
        target: { value: 'password' },
      })
      fireEvent.submit(container.querySelector('form')!)
      await waitFor(() => expect(finish).toBeDefined())
      if (action === 'unmount') unmount()
      else useAuthStore.getState().startSession('second-token')
      await act(async () =>
        finish({ id: 1, username: 'old-user', role: 'user' })
      )
      expect(useAuthStore.getState().user).toBeNull()
      expect(push).not.toHaveBeenCalled()
      if (action === 'unmount')
        expect(apiFetch.mock.calls[1][1].signal.aborted).toBe(true)
      else expect(useAuthStore.getState().accessToken).toBe('second-token')
    }
  )

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
    expect(fetch).toHaveBeenCalledWith('/api/config', {
      signal: expect.any(AbortSignal),
    })
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
    let resolveConfig!: (response: Response) => void
    vi.mocked(fetch).mockReturnValueOnce(
      new Promise((resolve) => {
        resolveConfig = resolve
      })
    )
    const { unmount } = render(<RegisterPage />)
    expect(
      screen.getByRole('button', { name: 'auth.register.submit' })
    ).toBeInTheDocument()
    expect(
      screen.queryByText('auth.register.registrationClosed')
    ).not.toBeInTheDocument()
    expect(apiFetch).not.toHaveBeenCalled()
    unmount()
    await act(async () => {
      resolveConfig(configResponse(false))
      await useConfigStore.getState().load()
    })
  })

  it.each([null, 'monthly', 'yearly', 'https://example.com', 'unknown'])(
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
        plan === 'monthly' || plan === 'yearly'
          ? `/onboarding?plan=${plan}`
          : '/onboarding'
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

  it.each(['monthly', 'yearly'])(
    'preserves plan=%s and the invite across signup links without copying other parameters',
    async (plan) => {
      searchParams.set('plan', plan)
      searchParams.set('invite', 'token+with/symbols')
      searchParams.set('token', 'must-not-propagate')
      searchParams.set('next', 'https://example.com')
      render(<RegisterPage />)
      await waitFor(() => expect(useConfigStore.getState().loaded).toBe(true))
      expect(
        screen.getByRole('link', { name: 'auth.register.login' })
      ).toHaveAttribute('href', `/login?plan=${plan}&invite=token%2Bwith%2Fsymbols`)
      for (const page of ['terms', 'privacy']) {
        expect(
          screen.getByRole('link', { name: `auth.register.${page}Link` })
        ).toHaveAttribute(
          'href',
          `/${page}?from=register&plan=${plan}&invite=token%2Bwith%2Fsymbols`
        )
      }
    }
  )

  it('keeps the selected plan when closed signup sends visitors to login', async () => {
    searchParams.set('plan', 'yearly')
    render(<RegisterPage />)
    expect(
      await screen.findByRole('link', { name: 'auth.register.login' })
    ).toHaveAttribute('href', '/login?plan=yearly')
  })

  it('keeps invited signup accessible from login with its selected plan', async () => {
    searchParams.set('invite', 'invite-token')
    searchParams.set('plan', 'monthly')
    render(<LoginPage />)
    await waitFor(() => expect(useConfigStore.getState().loaded).toBe(true))
    expect(
      screen.getByRole('link', { name: 'auth.login.register' })
    ).toHaveAttribute('href', '/register?plan=monthly&invite=invite-token')
  })

  it.each([
    ['monthly', [], '/settings?plan=monthly#plan'],
    ['yearly', null, '/onboarding?plan=yearly'],
    ['https://example.com', [], '/dashboard'],
  ])(
    'continues login plan=%s without starting checkout',
    async (plan, goals, destination) => {
      searchParams.set('plan', String(plan))
      apiFetch
        .mockResolvedValueOnce(
          new Response(JSON.stringify({ access_token: 'login-token' }))
        )
        .mockResolvedValueOnce(
          new Response(
            JSON.stringify({
              id: 1,
              username: 'learner',
              learning_goals: goals,
            })
          )
        )
      const { container } = render(<LoginPage />)
      fireEvent.change(
        container.querySelector('input[autocomplete="username"]')!,
        { target: { value: 'learner@example.com' } }
      )
      fireEvent.change(container.querySelector('input[type="password"]')!, {
        target: { value: 'Test1234!@' },
      })
      await act(async () => fireEvent.submit(container.querySelector('form')!))
      expect(push).toHaveBeenCalledWith(destination)
      expect(apiFetch).toHaveBeenCalledTimes(2)
    }
  )

  it.each(['replace-session', 'unmount'])(
    'ignores a late registration body after %s',
    async (action) => {
      searchParams.set('invite', 'invite-token')
      searchParams.set('plan', 'yearly')
      let finish!: (body: unknown) => void
      apiFetch.mockResolvedValueOnce({
        ok: true,
        json: () =>
          new Promise((resolve) => {
            finish = resolve
          }),
      })
      const { container, unmount } = render(<RegisterPage />)
      await fillAndSubmit(container)
      await waitFor(() => expect(finish).toBeDefined())
      if (action === 'unmount') unmount()
      else useAuthStore.getState().startSession('replacement-token')
      await act(async () => finish({ access_token: 'obsolete-token' }))
      expect(push).not.toHaveBeenCalled()
      expect(useAuthStore.getState().accessToken).toBe(
        action === 'unmount' ? null : 'replacement-token'
      )
    }
  )

  it.each([
    [[], '/settings?plan=monthly#plan'],
    [null, '/onboarding?plan=monthly'],
  ])(
    'waits for a successful profile retry before routing with goals=%s',
    async (goals, destination) => {
      searchParams.set('plan', 'monthly')
      apiFetch
        .mockResolvedValueOnce(
          new Response(JSON.stringify({ access_token: 'login-token' }))
        )
        .mockResolvedValueOnce(new Response('', { status: 503 }))
      const { container } = render(<LoginPage />)
      fireEvent.change(
        container.querySelector('input[autocomplete="username"]')!,
        { target: { value: 'learner@example.com' } }
      )
      fireEvent.change(container.querySelector('input[type="password"]')!, {
        target: { value: 'Test1234!@' },
      })
      await act(async () => fireEvent.submit(container.querySelector('form')!))
      expect(push).not.toHaveBeenCalled()
      expect(useAuthStore.getState().user).toBeNull()
      expect(screen.getByText(/auth.login.loginFailed/)).toBeInTheDocument()
      expect(
        screen.getByRole('button', { name: 'auth.login.submit' })
      ).toBeEnabled()
      expect(searchParams.get('plan')).toBe('monthly')

      apiFetch
        .mockResolvedValueOnce(
          new Response(JSON.stringify({ access_token: 'retry-token' }))
        )
        .mockResolvedValueOnce(
          new Response(
            JSON.stringify({
              id: 1,
              username: 'learner',
              learning_goals: goals,
            })
          )
        )
      await act(async () => fireEvent.submit(container.querySelector('form')!))
      expect(push).toHaveBeenCalledTimes(1)
      expect(push).toHaveBeenCalledWith(destination)
      expect(useAuthStore.getState().user?.learning_goals).toEqual(goals)
      expect(useAuthStore.getState().accessToken).toBe('retry-token')
      expect(
        screen.queryByText(/auth.login.loginFailed/)
      ).not.toBeInTheDocument()
      expect(apiFetch).toHaveBeenCalledTimes(4)
      expect(apiFetch.mock.calls.map(([path]) => path)).toEqual([
        '/api/auth/login',
        '/api/auth/me',
        '/api/auth/login',
        '/api/auth/me',
      ])
    }
  )

  it.each(
    [
      null,
      {},
      [],
      { id: 1, username: 'learner' },
      { id: 1, username: 'learner', learning_goals: 'travel' },
      { id: 1, username: 'learner', learning_goals: [null] },
      { learning_goals: null },
    ].map((profile) => ({ profile }))
  )(
    'rejects malformed successful profiles without inferring onboarding ($profile)',
    async ({ profile }) => {
      searchParams.set('plan', 'yearly')
      apiFetch
        .mockResolvedValueOnce(
          new Response(JSON.stringify({ access_token: 'login-token' }))
        )
        .mockResolvedValueOnce(new Response(JSON.stringify(profile)))
      const { container } = render(<LoginPage />)
      fireEvent.change(
        container.querySelector('input[autocomplete="username"]')!,
        { target: { value: 'learner@example.com' } }
      )
      fireEvent.change(container.querySelector('input[type="password"]')!, {
        target: { value: 'Test1234!@' },
      })
      await act(async () => fireEvent.submit(container.querySelector('form')!))
      expect(push).not.toHaveBeenCalled()
      expect(useAuthStore.getState().user).toBeNull()
      expect(screen.getByText(/auth.login.loginFailed/)).toBeInTheDocument()
      expect(
        screen.getByRole('button', { name: 'auth.login.submit' })
      ).toBeEnabled()
      expect(searchParams.get('plan')).toBe('yearly')
      expect(apiFetch).toHaveBeenCalledTimes(2)
    }
  )
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

  it.each(['monthly', 'yearly', 'https://example.com'])(
    'preserves only a whitelisted plan=%s with the invite in legal navigation',
    async (plan) => {
      searchParams.set('from', 'register')
      searchParams.set('plan', plan)
      searchParams.set('invite', 'token+with/symbols')
      searchParams.set('next', 'https://example.com')
      searchParams.set('token', 'must-not-propagate')
      render(<Page />)
      await waitFor(() => expect(useConfigStore.getState().loaded).toBe(true))
      const planQuery =
        plan === 'monthly' || plan === 'yearly' ? `plan=${plan}&` : ''
      expect(
        screen.getByRole('link', { name: `legal.${page}.linkBack` })
      ).toHaveAttribute(
        'href',
        `/register?${planQuery}invite=token%2Bwith%2Fsymbols`
      )
      expect(
        screen.getByRole('link', {
          name: `legal.${page}.link${other === 'terms' ? 'Terms' : 'Privacy'}`,
        })
      ).toHaveAttribute(
        'href',
        `/${other}?from=register&${planQuery}invite=token%2Bwith%2Fsymbols`
      )
    }
  )

  it('preserves the selected plan when returning to closed registration via login', async () => {
    searchParams.set('from', 'register')
    searchParams.set('plan', 'yearly')
    render(<Page />)
    await waitFor(() => expect(useConfigStore.getState().loaded).toBe(true))
    expect(
      screen.getByRole('link', { name: 'auth.register.login' })
    ).toHaveAttribute('href', '/login?plan=yearly')
  })
})
