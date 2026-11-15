import React from 'react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { act, cleanup, fireEvent, render, screen } from '@testing-library/react'
import { NextIntlClientProvider } from 'next-intl'
import { useAuthStore } from '@/store/auth'
import { useConfigStore } from '@/store/config'
import en from '../../../messages/en.json'
import es from '../../../messages/es.json'

const { apiFetch, push } = vi.hoisted(() => ({
  apiFetch: vi.fn(),
  push: vi.fn(),
}))

vi.mock('@/lib/api', () => ({ apiFetch }))
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

import LoginPage from '@/app/(auth)/login/page'
import RegisterPage from '@/app/(auth)/register/page'

const catalogs = { en, es }
const technicalDetail = 'DatabaseError: internal host db-private failed'

beforeEach(() => {
  apiFetch.mockReset()
  push.mockReset()
  useAuthStore.setState({ ...useAuthStore.getInitialState() }, true)
  useConfigStore.setState(
    {
      ...useConfigStore.getInitialState(),
      loaded: true,
      allowRegistration: true,
    },
    true
  )
})

afterEach(() => cleanup())

function renderForm(page: 'login' | 'register', locale: keyof typeof catalogs) {
  const result = render(
    <NextIntlClientProvider
      locale={locale}
      messages={catalogs[locale]}
      timeZone="UTC"
    >
      {page === 'login' ? <LoginPage /> : <RegisterPage />}
    </NextIntlClientProvider>
  )
  const form = result.container.querySelector('form')!
  const values =
    page === 'login'
      ? ['learner@example.com', 'Test1234!@']
      : ['learner', 'Learner', 'learner@example.com', 'Test1234!@', 'Test1234!@']
  const inputs = form.querySelectorAll('input')
  values.forEach((value, index) =>
    fireEvent.change(inputs[index], { target: { value } })
  )
  if (page === 'register') fireEvent.click(screen.getByRole('checkbox'))
  return form
}

describe.each(['es', 'en'] as const)('localized auth errors (%s)', (locale) => {
  it.each([
    { detail: 'Invalid credentials', status: 401, key: 'error' },
    { detail: technicalDetail, status: 503, key: 'loginFailed' },
    { detail: technicalDetail, status: 401, key: 'loginFailed' },
    {
      detail: [{ msg: 'Internal email database failure' }],
      status: 503,
      key: 'loginFailed',
    },
    {
      detail: [{ loc: ['body', 'email'], msg: technicalDetail }],
      status: 422,
      key: 'invalidEmail',
    },
  ] as const)('maps login responses to a safe message: $key / $status', async ({
    detail,
    status,
    key,
  }) => {
    apiFetch.mockResolvedValueOnce(
      new Response(JSON.stringify({ detail }), { status })
    )
    const form = renderForm('login', locale)
    await act(async () => fireEvent.submit(form))
    expect(
      screen.getByText(`✕ ${catalogs[locale].auth.login[key]}`)
    ).toBeInTheDocument()
    expect(
      screen.queryByText(technicalDetail, { exact: false })
    ).not.toBeInTheDocument()
    expect(push).not.toHaveBeenCalled()
  })

  it.each([
    { detail: 'Email already taken', key: 'emailTaken' },
    { detail: 'Invalid or expired invite', key: 'invalidInvite' },
    { detail: technicalDetail, key: 'error' },
    { detail: [{ msg: 'Internal email database failure' }], key: 'error' },
    {
      detail: [{ loc: ['body', 'password'], msg: technicalDetail }],
      key: 'invalidPassword',
    },
  ] as const)('maps registration responses to a safe message: $key', async ({
    detail,
    key,
  }) => {
    apiFetch.mockResolvedValueOnce(
      new Response(JSON.stringify({ detail }), { status: 422 })
    )
    const form = renderForm('register', locale)
    await act(async () => fireEvent.submit(form))
    expect(
      screen.getByText(`✕ ${catalogs[locale].auth.register[key]}`)
    ).toBeInTheDocument()
    expect(
      screen.queryByText(technicalDetail, { exact: false })
    ).not.toBeInTheDocument()
    expect(push).not.toHaveBeenCalled()
  })

  it.each(['login', 'register'] as const)(
    'discards exception messages in %s and keeps retry available',
    async (page) => {
      apiFetch.mockRejectedValueOnce(new Error(technicalDetail))
      const form = renderForm(page, locale)
      await act(async () => fireEvent.submit(form))
      const messages = catalogs[locale].auth
      const expected =
        page === 'login' ? messages.login.loginFailed : messages.register.error
      expect(screen.getByText(`✕ ${expected}`)).toBeInTheDocument()
      expect(
        screen.queryByText(technicalDetail, { exact: false })
      ).not.toBeInTheDocument()
      expect(
        screen.getByRole('button', { name: messages[page].submit })
      ).toBeEnabled()
      expect(push).not.toHaveBeenCalled()
    }
  )
})
