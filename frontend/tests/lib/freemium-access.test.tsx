import { act, cleanup, renderHook } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import {
  getFreemiumAccessFailure,
  useFreemiumAccessRecovery,
} from '@/lib/freemium-access'
import { useAuthStore } from '@/store/auth'
import { useFreemiumStore } from '@/store/freemium'
import { useConfigStore } from '@/store/config'

beforeEach(() => {
  useConfigStore.setState({ stripeEnabled: true })
})

afterEach(() => {
  cleanup()
  useFreemiumStore.setState(useFreemiumStore.getInitialState(), true)
  useAuthStore.setState(useAuthStore.getInitialState(), true)
  useConfigStore.setState(useConfigStore.getInitialState(), true)
})

describe('HTTP freemium recovery', () => {
  it.each([
    [402, { detail: { reason: 'freemium_exhausted', feature: 'reading' } }, 'exhausted'],
    [402, { detail: { reason: 'freemium_unavailable', feature: 'reading', remaining: 0, limit: 0 } }, 'unavailable'],
    [402, { detail: 'subscription_required' }, 'exhausted'],
    [402, { detail: { reason: 'freemium_exhausted', feature: 'chat' } }, null],
    [503, { detail: { reason: 'freemium_exhausted', feature: 'reading' } }, null],
    [402, null, null],
    [402, { detail: 'unknown' }, null],
  ])('classifies only explicit backend denials (%s, %j)', (status, body, expected) => {
    expect(getFreemiumAccessFailure(status as number, body, 'reading')).toBe(expected)
  })

  it('retains a confirmed denial after a failed refresh and clears it for a new session', async () => {
    const fetchStatus = vi.fn().mockResolvedValue(undefined)
    useFreemiumStore.setState({ status: null, fetchStatus })
    const { result, rerender } = renderHook(() => useFreemiumAccessRecovery('reading'))
    await act(async () => result.current.reportAccessDenied())
    expect(result.current.accessDenied).toBe(true)
    rerender()
    expect(fetchStatus).toHaveBeenCalledExactlyOnceWith(true)
    act(() => useAuthStore.getState().startSession('replacement'))
    expect(result.current.accessDenied).toBe(false)
    expect(fetchStatus).toHaveBeenCalledTimes(1)
  })

  it('does not mistake another feature optimistic update for restored access', async () => {
    const quota = {
      trial_active: false,
      trial_ends_at: null,
      chat_remaining: 3,
      chat_limit: 3,
      lessons_remaining: 3,
      lessons_limit: 3,
      listening_remaining: 3,
      listening_limit: 3,
      reading_remaining: 3,
      reading_limit: 3,
      games_remaining: 3,
      games_limit: 3,
      voice_remaining_seconds: 300,
      voice_limit_seconds: 300,
    }
    useFreemiumStore.setState({
      status: quota,
      lastFetch: 1,
      fetchStatus: vi.fn(async () => {
        useFreemiumStore.setState({ lastFetch: 0 })
      }),
    })
    const { result } = renderHook(() => useFreemiumAccessRecovery('reading'))
    await act(async () => result.current.reportAccessDenied())
    act(() => useFreemiumStore.getState().decrement('chat_remaining'))
    expect(result.current.accessDenied).toBe(true)
    act(() => {
      useFreemiumStore.setState({ status: { ...quota }, lastFetch: 2 })
      // A subsequent forced read may fail before React renders the positive GET.
      useFreemiumStore.setState({ lastFetch: 0 })
    })
    expect(result.current.accessDenied).toBe(false)
    await act(async () => useFreemiumStore.getState().fetchStatus(true))
    expect(result.current.accessDenied).toBe(false)
  })

  it('retires denial when billing is disabled, without trusting an already stale Premium profile', async () => {
    const user = {
      id: 1, username: 'learner', displayName: 'Learner', role: 'user' as const,
      subscription_status: 'active' as const,
      conversation_max_duration: 300, conversation_inactivity_timeout: 30,
    }
    useAuthStore.setState({ user })
    useFreemiumStore.setState({ status: null, fetchStatus: vi.fn().mockResolvedValue(undefined) })
    const { result } = renderHook(() => useFreemiumAccessRecovery('voice'))
    await act(async () => result.current.reportAccessDenied())
    act(() => useAuthStore.getState().setUser({ ...user, displayName: 'Updated' }))
    expect(result.current.accessDenied).toBe(true)
    act(() => useConfigStore.setState({ stripeEnabled: false }))
    expect(result.current.accessDenied).toBe(false)
    act(() => useConfigStore.setState({ stripeEnabled: true }))
    expect(result.current.accessDenied).toBe(false)
  })

  it.each([false, true])('retires denial after explicitly re-enabling a future trial (initial=%s)', async (enabled) => {
    useConfigStore.setState({ freemiumTrialEnabled: enabled })
    useAuthStore.setState({ user: {
      id: 1, username: 'learner', displayName: 'Learner', role: 'user',
      subscription_status: 'none',
      freemium_trial_ends_at: new Date(Date.now() + 60_000).toISOString(),
      conversation_max_duration: 300, conversation_inactivity_timeout: 30,
    } })
    useFreemiumStore.setState({ status: null, fetchStatus: vi.fn().mockResolvedValue(undefined) })
    const { result } = renderHook(() => useFreemiumAccessRecovery('voice'))
    await act(async () => result.current.reportAccessDenied())
    expect(result.current.accessDenied).toBe(true)
    if (enabled) act(() => useConfigStore.setState({ freemiumTrialEnabled: false }))
    act(() => useConfigStore.setState({ freemiumTrialEnabled: true }))
    expect(result.current.accessDenied).toBe(false)
    await act(async () => useFreemiumStore.getState().fetchStatus(true))
    expect(result.current.accessDenied).toBe(false)
  })
})
