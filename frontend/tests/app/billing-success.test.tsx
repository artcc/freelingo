import { describe, expect, it, vi, beforeEach, afterEach } from 'vitest'
import { render, screen, waitFor, act } from '@testing-library/react'
import React from 'react'

const { mockApiFetch, mockPush } = vi.hoisted(() => ({
  mockApiFetch: vi.fn(),
  mockPush: vi.fn(),
}))

vi.mock('next-intl', () => ({
  useTranslations: () => (key: string, vars?: Record<string, unknown>) =>
    vars?.seconds ? `${key}:${vars.seconds}` : key,
}))

vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: mockPush,
  }),
}))

vi.mock('next/link', () => ({
  default: ({
    href,
    children,
    ...props
  }: React.AnchorHTMLAttributes<HTMLAnchorElement>) =>
    React.createElement('a', { href: String(href), ...props }, children),
}))

vi.mock('@/lib/api', async (importOriginal) => ({
  ...(await importOriginal<typeof import('@/lib/api')>()),
  apiFetch: mockApiFetch,
}))

import BillingSuccessPage from '@/app/(auth)/billing/success/page'
import { useAuthStore } from '@/store/auth'

function jsonResponse(data: unknown, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  })
}

function me(subscriptionStatus: string) {
  return {
    id: 1,
    username: 'learner',
    display_name: 'Learner',
    email: 'learner@example.com',
    native_language: 'es',
    ui_locale: 'en',
    role: 'user',
    conversation_max_duration: 30,
    conversation_inactivity_timeout: 10,
    subscription_status: subscriptionStatus,
    subscription_ends_at: null,
    trial_used: false,
  }
}

beforeEach(() => {
  mockApiFetch.mockReset()
  mockPush.mockReset()
  useAuthStore.setState({ accessToken: 'token', user: null })
})

afterEach(() => {
  vi.useRealTimers()
})

describe('BillingSuccessPage', () => {
  it('does not restore a token after the confirmation page unmounts', async () => {
    useAuthStore.setState({ accessToken: null })
    let finish!: (response: Response) => void
    const mock = vi.spyOn(globalThis, 'fetch').mockReturnValueOnce(
      new Promise((resolve) => {
        finish = resolve
      })
    )
    const { unmount } = render(<BillingSuccessPage />)
    unmount()
    await act(async () => finish(jsonResponse({ access_token: 'obsolete' })))
    expect(useAuthStore.getState().accessToken).toBeNull()
    expect(mockApiFetch).not.toHaveBeenCalled()
    mock.mockRestore()
  })

  it('does not publish a profile whose body finishes after session replacement', async () => {
    let finish!: (body: unknown) => void
    mockApiFetch.mockResolvedValue({
      ok: true,
      json: () =>
        new Promise((resolve) => {
          finish = resolve
        }),
    })
    render(<BillingSuccessPage />)
    await waitFor(() => expect(finish).toBeDefined())
    useAuthStore.getState().startSession('new-session')
    await act(async () => finish(me('active')))
    expect(useAuthStore.getState().user).toBeNull()
    expect(mockPush).not.toHaveBeenCalled()
  })
  it('shows confirmed Premium copy only after /me returns an active subscription', async () => {
    mockApiFetch.mockResolvedValueOnce(jsonResponse(me('active')))

    render(<BillingSuccessPage />)

    expect(screen.getByText('successCheckingTitle')).toBeDefined()
    expect(screen.queryByText('successTitle')).toBeNull()

    await waitFor(() => expect(screen.getByText('successTitle')).toBeDefined())
    expect(screen.getByText('successDesc')).toBeDefined()
    expect(screen.getByText('successRedirect:5')).toBeDefined()
    expect(useAuthStore.getState().user?.subscription_status).toBe('active')
  })

  it('refreshes the session before checking /me when the access token is missing', async () => {
    useAuthStore.setState({ accessToken: null, user: null })
    const fetchMock = vi
      .spyOn(globalThis, 'fetch')
      .mockResolvedValueOnce(jsonResponse({ access_token: 'new-token' }))
    mockApiFetch.mockResolvedValueOnce(jsonResponse(me('trialing')))

    render(<BillingSuccessPage />)

    await waitFor(() => expect(screen.getByText('successTitle')).toBeDefined())
    expect(fetchMock).toHaveBeenCalledWith('/api/auth/refresh', {
      method: 'POST',
      credentials: 'include',
    })
    expect(useAuthStore.getState().accessToken).toBe('new-token')
    expect(useAuthStore.getState().user?.subscription_status).toBe('trialing')
  })

  it('does not show active Premium copy when /me never confirms the subscription', async () => {
    vi.useFakeTimers()
    mockApiFetch.mockImplementation(() =>
      Promise.resolve(jsonResponse(me('none')))
    )

    render(<BillingSuccessPage />)

    expect(screen.getByText('successCheckingTitle')).toBeDefined()

    await act(async () => {
      await vi.advanceTimersByTimeAsync(6100)
    })

    expect(screen.getByText('successPendingTitle')).toBeDefined()
    expect(screen.queryByText('successTitle')).toBeNull()
    expect(screen.queryByText('successRedirect:5')).toBeNull()
  })
})
