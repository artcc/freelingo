import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { act, cleanup, fireEvent, render, screen } from '@testing-library/react'
import React from 'react'

const { apiFetch } = vi.hoisted(() => ({ apiFetch: vi.fn() }))
vi.mock('@/lib/api', () => ({
  apiFetch,
  requestAccessToken: vi.fn(),
}))
vi.mock('next-intl', () => ({
  useTranslations: () => (key: string, values?: { days?: number }) =>
    values?.days === undefined ? key : `${key}:${values.days}`,
}))
vi.mock('next/link', () => ({
  default: ({ href, children, ...props }: React.AnchorHTMLAttributes<HTMLAnchorElement>) =>
    <a href={href} {...props}>{children}</a>,
}))
vi.mock('@/components/LanguageSwitcher', () => ({ default: () => null }))
vi.mock('@/components/ui/confirm-dialog', () => ({ ConfirmDialog: () => null }))
vi.mock('@/components/ui/contact-form-modal', () => ({ ContactFormModal: () => null }))
vi.mock('@/components/ui/loading-bar', () => ({ LoadingBar: () => null }))
vi.mock('@/components/ui/page-loading', () => ({ PageLoading: () => null }))
vi.mock('@/components/ui/page-loading-boundary', () => ({
  PageLoadingProvider: ({ children }: { children: React.ReactNode }) => children,
  PageLoadingViewport: ({ children }: { children: React.ReactNode }) => children,
}))

import AppLayout from '@/app/(app)/layout'
import { useAuthStore } from '@/store/auth'
import { useConfigStore } from '@/store/config'

beforeEach(() => {
  vi.useFakeTimers()
  vi.setSystemTime('2026-11-15T12:00:00Z')
  useAuthStore.getState().startSession('token')
  useConfigStore.setState({
    loaded: true,
    stripeEnabled: true,
    freemiumTrialEnabled: true,
  })
  apiFetch.mockReset()
  apiFetch.mockImplementation(async (url: string) => ({
    ok: true,
    json: async () => url === '/api/auth/me'
      ? {
          id: 1,
          username: 'learner',
          display_name: 'Learner',
          role: 'user',
          learning_goals: [],
          subscription_status: 'none',
          freemium_trial_ends_at: '2026-11-15T12:00:01Z',
        }
      : url === '/api/feedback/unread-summary'
        ? { unread_count: 0 }
        : { trial_active: false, trial_ends_at: null },
  }))
})

afterEach(() => {
  cleanup()
  vi.useRealTimers()
})

describe('layout trial presentation', () => {
  it('exposes plans in desktop and mobile navigation and makes trial days clickable', async () => {
    await act(async () => {
      render(<AppLayout><div>content</div></AppLayout>)
    })
    expect(screen.getAllByRole('link', { name: 'viewPremium' })).toHaveLength(2)
    for (const link of screen.getAllByRole('link', { name: 'viewPremium' })) {
      expect(link).toHaveAttribute('href', '/settings#plan')
    }
    expect(screen.getByRole('link', { name: '★ trialDays:1' })).toHaveAttribute(
      'href', '/settings#plan'
    )
    act(() => useConfigStore.setState({ stripeEnabled: false }))
    expect(screen.queryByRole('link', { name: 'viewPremium' })).not.toBeInTheDocument()
  })

  it('reacts to the runtime toggle in both desktop and mobile navigation', async () => {
    await act(async () => {
      render(<AppLayout><div>content</div></AppLayout>)
    })
    fireEvent.click(screen.getByRole('button', { name: 'openMenu' }))
    expect(screen.getAllByText('★ trialDays:1')).toHaveLength(2)
    act(() => useConfigStore.setState({ freemiumTrialEnabled: false }))
    expect(screen.queryByText('★ trialDays:1')).not.toBeInTheDocument()
    act(() => useConfigStore.setState({ freemiumTrialEnabled: true }))
    expect(screen.getAllByText('★ trialDays:1')).toHaveLength(2)
  })

  it('removes the countdown at expiration and refreshes quotas once', async () => {
    await act(async () => {
      render(<AppLayout><div>content</div></AppLayout>)
    })
    expect(screen.getByText('★ trialDays:1')).toBeInTheDocument()
    const initialReads = apiFetch.mock.calls.filter(
      ([url]) => url === '/api/freemium/status'
    ).length
    await act(() => vi.advanceTimersByTimeAsync(1_000))
    expect(screen.queryByText('★ trialDays:1')).not.toBeInTheDocument()
    expect(apiFetch.mock.calls.filter(
      ([url]) => url === '/api/freemium/status'
    )).toHaveLength(initialReads + 1)
    await act(() => vi.advanceTimersByTimeAsync(60_000))
    expect(apiFetch.mock.calls.filter(
      ([url]) => url === '/api/freemium/status'
    )).toHaveLength(initialReads + 1)
  })
})
