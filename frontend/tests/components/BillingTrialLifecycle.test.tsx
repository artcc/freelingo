import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { act, cleanup, render, renderHook, screen } from '@testing-library/react'
import React from 'react'

vi.mock('next-intl', () => ({
  useTranslations: () => (key: string, values?: { days?: number }) =>
    values?.days === undefined ? key : `${key}:${values.days}`,
}))

vi.mock('next/link', () => ({
  default: ({ href, children, ...props }: React.AnchorHTMLAttributes<HTMLAnchorElement>) =>
    <a href={href} {...props}>{children}</a>,
}))

const { mockApiFetch } = vi.hoisted(() => ({ mockApiFetch: vi.fn() }))
vi.mock('@/lib/api', () => ({ apiFetch: mockApiFetch }))

import { FreemiumQuotaBanner } from '@/components/billing/FreemiumQuotaBanner'
import { useTrialStatus } from '@/hooks/useTrialStatus'
import { useFreemiumStatusRefresh } from '@/hooks/useFreemiumStatusRefresh'
import { isSubscribed, useAuthStore, type User } from '@/store/auth'
import { useConfigStore } from '@/store/config'
import { useFreemiumStore } from '@/store/freemium'

const DAY_MS = 86_400_000
const user: User = {
  id: 1,
  username: 'learner',
  displayName: 'Learner',
  role: 'user',
  conversation_max_duration: 900,
  conversation_inactivity_timeout: 60,
  subscription_status: 'none',
}
const status = {
  trial_active: false,
  trial_ends_at: null,
  chat_remaining: 0,
  chat_limit: 5,
  lessons_remaining: 0,
  lessons_limit: 3,
  listening_remaining: 0,
  listening_limit: 3,
  reading_remaining: 0,
  reading_limit: 3,
  games_remaining: 0,
  games_limit: 3,
  voice_remaining_seconds: 0,
  voice_limit_seconds: 300,
}

beforeEach(() => {
  vi.useFakeTimers()
  vi.setSystemTime('2026-11-15T12:00:00Z')
  mockApiFetch.mockReset()
  mockApiFetch.mockResolvedValue({ ok: true, json: async () => status })
  useAuthStore.getState().startSession('token')
  useAuthStore.getState().setUser(user)
  useConfigStore.setState({
    stripeEnabled: true,
    freemiumTrialEnabled: true,
    loaded: true,
  })
  useFreemiumStore.setState({ status, loaded: true, lastFetch: Date.now() })
})

afterEach(() => {
  cleanup()
  vi.useRealTimers()
})

describe('billing trial lifecycle', () => {
  it('links the low-quota upgrade action directly to the settings plan', () => {
    render(<FreemiumQuotaBanner feature="chat" />)
    expect(screen.getByRole('link', { name: 'freeLimit' })).toHaveAttribute(
      'href', '/settings#plan'
    )
  })

  it('warns on the last of three free uses, before exhaustion', () => {
    useFreemiumStore.setState({
      status: { ...status, lessons_remaining: 1, lessons_limit: 3 },
    })
    render(<FreemiumQuotaBanner feature="lessons" />)
    expect(screen.getByRole('link', { name: 'freeLimit' })).toHaveAttribute(
      'href', '/settings#plan'
    )
    expect(screen.getByText('dailyReset')).toBeInTheDocument()
    act(() => useFreemiumStore.setState({
      status: { ...status, lessons_remaining: 2, lessons_limit: 3 },
    }))
    expect(screen.queryByRole('link', { name: 'freeLimit' })).not.toBeInTheDocument()
  })

  it('makes trial and Premium-only labels actionable without inventing a reset', () => {
    useFreemiumStore.setState({
      status: { ...status, lessons_limit: 0 },
    })
    render(<FreemiumQuotaBanner feature="lessons" />)
    expect(screen.getByRole('link', { name: 'requiresSubscription' })).toHaveAttribute(
      'href', '/settings#plan'
    )
    expect(screen.queryByText('dailyReset')).not.toBeInTheDocument()
    act(() => useAuthStore.getState().setUser({
      ...user, freemium_trial_ends_at: '2026-11-20T12:00:00Z',
    }))
    expect(screen.getByRole('link', { name: 'trialUnlimited' })).toHaveAttribute(
      'href', '/settings#plan'
    )
  })

  it('updates remaining days and removes trial access exactly at expiry', () => {
    useAuthStore.getState().setUser({
      ...user,
      freemium_trial_ends_at: new Date(Date.now() + DAY_MS + 1_000).toISOString(),
    })
    render(<FreemiumQuotaBanner feature="chat" />)
    expect(screen.getByText('★ trialDaysLeft:2')).toBeInTheDocument()
    act(() => vi.advanceTimersByTime(1_000))
    expect(screen.getByText('★ trialDaysLeft:1')).toBeInTheDocument()
    act(() => vi.advanceTimersByTime(DAY_MS))
    expect(screen.queryByText('trialUnlimited')).not.toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'freeLimit' })).toBeInTheDocument()
  })

  it('reacts immediately to the trial runtime toggle', () => {
    useAuthStore.getState().setUser({
      ...user,
      freemium_trial_ends_at: new Date(Date.now() + DAY_MS).toISOString(),
    })
    const { result } = renderHook(() => useTrialStatus())
    expect(result.current).toMatchObject({
      freemiumTrialActive: true, trialDaysLeft: 1,
    })
    act(() => useConfigStore.setState({ freemiumTrialEnabled: false }))
    expect(result.current).toMatchObject({
      freemiumTrialActive: false, trialDaysLeft: 0,
    })
    act(() => useConfigStore.setState({ freemiumTrialEnabled: true }))
    expect(result.current.freemiumTrialActive).toBe(true)
  })

  it('ends the Stripe countdown without revoking persisted subscription access', () => {
    useAuthStore.getState().setUser({
      ...user,
      subscription_status: 'trialing',
      subscription_ends_at: new Date(Date.now() + 1_000).toISOString(),
    })
    const { result } = renderHook(() => useTrialStatus())
    expect(result.current.trialDaysLeft).toBe(1)
    act(() => vi.advanceTimersByTime(1_000))
    expect(result.current.trialDaysLeft).toBe(0)
    expect(isSubscribed(useAuthStore.getState().user, true)).toBe(true)
  })

  it.each(['invalid', '2026-11-14T00:00:00Z'])(
    'hides an invalid or expired countdown (%s)', (end) => {
      useAuthStore.getState().setUser({
        ...user,
        freemium_trial_ends_at: end,
        subscription_status: 'trialing',
        subscription_ends_at: end,
      })
      const { result } = renderHook(() => useTrialStatus())
      expect(result.current).toMatchObject({
        freemiumTrialActive: false, trialDaysLeft: 0,
      })
    }
  )

  it.each(['2026-11-15T23:59:59.500Z', '2026-11-17T23:59:59.500Z'])(
    'refreshes at UTC replenishment without minute polling (%s)', async (time) => {
      vi.setSystemTime(time)
      useFreemiumStore.setState({ lastFetch: Date.now() })
      renderHook(() => useFreemiumStatusRefresh(true))
      expect(mockApiFetch).not.toHaveBeenCalled()
      await act(() => vi.advanceTimersByTimeAsync(500))
      expect(mockApiFetch).toHaveBeenCalledTimes(1)
      await act(() => vi.advanceTimersByTimeAsync(60_000))
      expect(mockApiFetch).toHaveBeenCalledTimes(1)
    }
  )

  it('refreshes the expired trial snapshot inside the cache window', async () => {
    const end = new Date(Date.now() + 1_000).toISOString()
    useAuthStore.getState().setUser({ ...user, freemium_trial_ends_at: end })
    useFreemiumStore.setState({
      status: { ...status, trial_active: true, trial_ends_at: end },
    })
    renderHook(() => useFreemiumStatusRefresh(true))
    expect(mockApiFetch).not.toHaveBeenCalled()
    await act(() => vi.advanceTimersByTimeAsync(1_000))
    expect(mockApiFetch).toHaveBeenCalledTimes(1)
    expect(useFreemiumStore.getState().status?.trial_active).toBe(false)
  })

  it('refreshes on a runtime toggle and only stale focus events', async () => {
    renderHook(() => useFreemiumStatusRefresh(true))
    await act(async () => {
      window.dispatchEvent(new Event('focus'))
    })
    expect(mockApiFetch).not.toHaveBeenCalled()
    await act(async () => {
      useConfigStore.setState({ freemiumTrialEnabled: false })
    })
    expect(mockApiFetch).toHaveBeenCalledTimes(1)
    await act(() => vi.advanceTimersByTimeAsync(60_001))
    await act(async () => {
      window.dispatchEvent(new Event('focus'))
      document.dispatchEvent(new Event('visibilitychange'))
    })
    expect(mockApiFetch).toHaveBeenCalledTimes(2)
  })

  it('defers a hidden-tab boundary request until the tab is visible', async () => {
    const visibility = vi.spyOn(document, 'visibilityState', 'get')
    const end = new Date(Date.now() + 1_000).toISOString()
    useAuthStore.getState().setUser({ ...user, freemium_trial_ends_at: end })
    renderHook(() => useFreemiumStatusRefresh(true))
    visibility.mockReturnValue('hidden')
    await act(() => vi.advanceTimersByTimeAsync(1_000))
    expect(mockApiFetch).not.toHaveBeenCalled()
    visibility.mockReturnValue('visible')
    await act(async () => {
      document.dispatchEvent(new Event('visibilitychange'))
    })
    expect(mockApiFetch).toHaveBeenCalledTimes(1)
  })

  it('removes scheduled refreshes on logout and does not fetch for subscribers', async () => {
    const { unmount } = renderHook(() => useFreemiumStatusRefresh(true))
    act(() => useAuthStore.getState().logout())
    await act(() => vi.advanceTimersByTimeAsync(DAY_MS))
    window.dispatchEvent(new Event('focus'))
    expect(mockApiFetch).not.toHaveBeenCalled()
    unmount()
    useAuthStore.getState().startSession('other')
    useAuthStore.getState().setUser({ ...user, subscription_status: 'active' })
    renderHook(() => useFreemiumStatusRefresh(true))
    await act(() => vi.advanceTimersByTimeAsync(DAY_MS))
    expect(mockApiFetch).not.toHaveBeenCalled()
  })
})
