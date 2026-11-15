import {
  act,
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
  within,
} from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import React from 'react'

const { apiFetch, push } = vi.hoisted(() => ({
  apiFetch: vi.fn(),
  push: vi.fn(),
}))

vi.mock('@/lib/api', () => ({ apiFetch }))
vi.mock('next-intl', () => {
  const translate = (key: string) => key
  return { useTranslations: () => translate, useLocale: () => 'en' }
})
vi.mock('next/navigation', () => ({
  useRouter: () => ({ push }),
  useSearchParams: () => new URLSearchParams(),
}))
vi.mock('next/link', () => ({
  default: (props: React.AnchorHTMLAttributes<HTMLAnchorElement>) => (
    <a {...props} />
  ),
}))
vi.mock('@/hooks/useLogout', () => ({ useLogout: () => vi.fn() }))
vi.mock('@/components/settings/ProfileSection', () => ({
  ProfileSection: () => null,
}))
vi.mock('@/components/settings/ConversationSection', () => ({
  ConversationSection: () => null,
}))
vi.mock('@/components/settings/VoiceSection', () => ({
  VoiceSection: () => null,
}))
vi.mock('@/components/settings/UsageLimitsSection', () => ({
  UsageLimitsSection: () => null,
}))
vi.mock('@/components/settings/AppearanceSection', () => ({
  AppearanceSection: () => null,
}))
vi.mock('@/components/settings/ReviewSection', () => ({
  ReviewSection: () => null,
}))
vi.mock('@/components/admin/AdminNav', () => ({ AdminNav: () => null }))
vi.mock('@/components/ui/page-loading', () => ({
  PageLoading: () => <div>loading</div>,
}))

import SettingsPage from '@/app/(app)/settings/page'
import AdminUsersPage from '@/app/(app)/admin/users/page'
import { useAuthStore, type User } from '@/store/auth'
import { useConfigStore } from '@/store/config'

const user: User = {
  id: 1,
  username: 'learner',
  displayName: 'Learner',
  role: 'user',
  subscription_status: 'none',
  conversation_max_duration: 900,
  conversation_inactivity_timeout: 60,
}
const listedUser = {
  id: 2,
  username: 'other',
  display_name: 'Other learner',
  email: null,
  role: 'user',
  native_language: 'en',
  is_active: true,
  subscription_status: 'active',
}

function response(detail: string, status: number) {
  return new Response(JSON.stringify({ detail }), { status })
}

function deferred<T>() {
  let resolve!: (value: T) => void
  const promise = new Promise<T>((done) => {
    resolve = done
  })
  return { promise, resolve }
}

beforeEach(() => {
  apiFetch.mockReset()
  push.mockReset()
  useAuthStore.getState().startSession('original-token')
  useAuthStore.getState().setUser(user)
  useConfigStore.setState({ stripeEnabled: true, loaded: true })
  Object.defineProperty(window, 'location', {
    configurable: true,
    value: { assign: vi.fn(), search: '' },
  })
})
afterEach(cleanup)

function openSettingsDeletion() {
  fireEvent.click(screen.getByRole('button', { name: 'deleteAccount' }))
  return within(screen.getByRole('alertdialog'))
}

const rejections = [
  [409, 'subscription_cancellation_required', 'cancellationRequired'],
  [409, 'billing_checkout_pending', 'checkoutPending'],
  [503, 'billing_verification_unavailable', 'verificationUnavailable'],
  [500, 'private provider error', 'failed'],
] as const

describe('settings account deletion', () => {
  it.each(rejections)(
    'preserves authentication and the modal after %s %s',
    async (status, detail, key) => {
      apiFetch.mockResolvedValueOnce(response(detail, status))
      render(<SettingsPage />)
      const dialog = openSettingsDeletion()
      fireEvent.click(
        dialog.getByRole('button', { name: 'deleteAccountConfirm' })
      )
      await waitFor(() =>
        expect(dialog.getByRole('alert')).toHaveTextContent(key)
      )
      expect(useAuthStore.getState().accessToken).toBe('original-token')
      expect(useAuthStore.getState().user).toEqual(user)
      expect(push).not.toHaveBeenCalled()
      expect(
        dialog.getByRole('button', { name: 'deleteAccountConfirm' })
      ).toBeEnabled()
      if (key === 'cancellationRequired') {
        expect(
          dialog.getByRole('button', { name: 'manageSubscription' })
        ).toBeEnabled()
      }
    }
  )

  it.each([
    'active',
    'trialing',
    'past_due',
    'unpaid',
    'paused',
    'incomplete',
  ] as const)(
    'warns before sending a request for an uncancelled %s subscription',
    (subscription_status) => {
      useAuthStore.getState().setUser({ ...user, subscription_status })
      render(<SettingsPage />)
      const dialog = openSettingsDeletion()
      expect(dialog.getByRole('alert')).toHaveTextContent(
        'cancellationRequired'
      )
      expect(
        dialog.getByRole('button', { name: 'manageSubscription' })
      ).toBeEnabled()
      expect(apiFetch).not.toHaveBeenCalled()
    }
  )

  it.each(['none', 'incomplete', 'canceled'] as const)(
    'opens the portal after a deletion denial despite a stale %s profile offering checkout',
    async (subscription_status) => {
      useAuthStore.getState().setUser({ ...user, subscription_status })
      apiFetch
        .mockResolvedValueOnce(
          response('subscription_cancellation_required', 409)
        )
        .mockResolvedValueOnce(
          new Response(
            JSON.stringify({ url: 'https://billing.stripe.com/session/manage' })
          )
        )
      render(<SettingsPage />)
      expect(screen.getByRole('button', { name: 'planMonthly' })).toBeEnabled()
      expect(
        screen.queryByRole('button', { name: 'manage' })
      ).not.toBeInTheDocument()
      const dialog = openSettingsDeletion()
      fireEvent.click(
        dialog.getByRole('button', { name: 'deleteAccountConfirm' })
      )
      await waitFor(() =>
        expect(dialog.getByRole('alert')).toHaveTextContent(
          'cancellationRequired'
        )
      )
      fireEvent.click(
        dialog.getByRole('button', { name: 'manageSubscription' })
      )
      await waitFor(() =>
        expect(window.location.assign).toHaveBeenCalledExactlyOnceWith(
          'https://billing.stripe.com/session/manage'
        )
      )
      expect(apiFetch.mock.calls.map(([url]) => url)).toEqual([
        '/api/auth/me',
        '/api/billing/portal',
      ])
      expect(apiFetch.mock.calls[1][1]).toMatchObject({ method: 'POST' })
      expect(useAuthStore.getState().user?.subscription_status).toBe(
        subscription_status
      )
      expect(useAuthStore.getState().accessToken).toBe('original-token')
      expect(push).not.toHaveBeenCalled()
    }
  )

  it('opens the portal from the informative warning without trying deletion', async () => {
    useAuthStore.getState().setUser({ ...user, subscription_status: 'active' })
    apiFetch.mockResolvedValueOnce(
      new Response(
        JSON.stringify({ url: 'https://billing.stripe.com/session/manage' })
      )
    )
    render(<SettingsPage />)
    const dialog = openSettingsDeletion()
    expect(
      dialog.getByRole('button', { name: 'deleteAccountConfirm' })
    ).toBeEnabled()
    fireEvent.click(dialog.getByRole('button', { name: 'manageSubscription' }))
    await waitFor(() => expect(window.location.assign).toHaveBeenCalledOnce())
    expect(apiFetch.mock.calls.map(([url]) => url)).toEqual([
      '/api/billing/portal',
    ])
  })

  it('keeps the profile warning advisory when the backend permits deletion', async () => {
    useAuthStore.getState().setUser({ ...user, subscription_status: 'active' })
    apiFetch.mockResolvedValueOnce(new Response(null, { status: 204 }))
    render(<SettingsPage />)
    const dialog = openSettingsDeletion()
    expect(dialog.getByRole('alert')).toHaveTextContent('cancellationRequired')
    fireEvent.click(
      dialog.getByRole('button', { name: 'deleteAccountConfirm' })
    )
    await waitFor(() => expect(push).toHaveBeenCalledExactlyOnceWith('/login'))
    expect(apiFetch.mock.calls.map(([url]) => url)).toEqual(['/api/auth/me'])
    expect(useAuthStore.getState().accessToken).toBeNull()
  })

  it('clears a previous portal error when reopening the deletion dialog', async () => {
    useAuthStore.getState().setUser({ ...user, subscription_status: 'active' })
    apiFetch.mockResolvedValueOnce(response('private error', 503))
    render(<SettingsPage />)
    const dialog = openSettingsDeletion()
    fireEvent.click(dialog.getByRole('button', { name: 'manageSubscription' }))
    await waitFor(() =>
      expect(dialog.getByRole('alert')).toHaveTextContent('portalError')
    )
    fireEvent.click(dialog.getByRole('button', { name: 'cancel' }))
    const reopened = openSettingsDeletion()
    expect(reopened.getByRole('alert')).toHaveTextContent(
      'cancellationRequired'
    )
    expect(reopened.queryByText('portalError')).not.toBeInTheDocument()
  })

  it.each(['http', 'network'] as const)(
    'retains the cancellation warning and permits a portal retry after %s failure',
    async (failure) => {
      apiFetch.mockResolvedValueOnce(
        response('subscription_cancellation_required', 409)
      )
      if (failure === 'http')
        apiFetch.mockResolvedValueOnce(response('private error', 503))
      else apiFetch.mockRejectedValueOnce(new Error('private error'))
      render(<SettingsPage />)
      const dialog = openSettingsDeletion()
      fireEvent.click(
        dialog.getByRole('button', { name: 'deleteAccountConfirm' })
      )
      await waitFor(() =>
        expect(dialog.getByRole('alert')).toHaveTextContent(
          'cancellationRequired'
        )
      )
      fireEvent.click(
        dialog.getByRole('button', { name: 'manageSubscription' })
      )
      await waitFor(() =>
        expect(dialog.getByRole('alert')).toHaveTextContent('portalError')
      )
      expect(dialog.getByRole('alert')).toHaveTextContent(
        'cancellationRequired'
      )
      expect(dialog.getByRole('alert')).not.toHaveTextContent('private error')
      expect(useAuthStore.getState().accessToken).toBe('original-token')
      expect(window.location.assign).not.toHaveBeenCalled()
      const portal = deferred<Response>()
      apiFetch.mockReturnValueOnce(portal.promise)
      const manage = dialog.getByRole('button', { name: 'manageSubscription' })
      fireEvent.click(manage)
      fireEvent.click(manage)
      expect(manage).toBeDisabled()
      expect(
        dialog.getByRole('button', { name: 'deleteAccountConfirm' })
      ).toBeDisabled()
      expect(dialog.getByRole('button', { name: 'cancel' })).toBeDisabled()
      expect(dialog.queryByText('portalError')).not.toBeInTheDocument()
      act(() => useAuthStore.getState().setTokens('rotated-token'))
      await act(async () =>
        portal.resolve(
          new Response(
            JSON.stringify({
              url: 'https://billing.stripe.com/session/retry',
            })
          )
        )
      )
      expect(window.location.assign).toHaveBeenCalledExactlyOnceWith(
        'https://billing.stripe.com/session/retry'
      )
      expect(apiFetch).toHaveBeenCalledTimes(3)
    }
  )

  it.each(['session', 'unmount', 'body'] as const)(
    'ignores late portal navigation after %s invalidation',
    async (invalidation) => {
      apiFetch.mockResolvedValueOnce(
        response('subscription_cancellation_required', 409)
      )
      const view = render(<SettingsPage />)
      const dialog = openSettingsDeletion()
      fireEvent.click(
        dialog.getByRole('button', { name: 'deleteAccountConfirm' })
      )
      await waitFor(() =>
        expect(dialog.getByRole('alert')).toHaveTextContent(
          'cancellationRequired'
        )
      )
      const portal = deferred<Response>()
      const body = deferred<{ url: string }>()
      const json = vi.fn(() => body.promise)
      if (invalidation === 'body')
        apiFetch.mockResolvedValueOnce({ ok: true, json })
      else apiFetch.mockReturnValueOnce(portal.promise)
      fireEvent.click(
        dialog.getByRole('button', { name: 'manageSubscription' })
      )
      if (invalidation === 'body')
        await waitFor(() => expect(json).toHaveBeenCalledOnce())
      const signal = apiFetch.mock.lastCall![1].signal
      if (invalidation === 'unmount') view.unmount()
      else
        act(() => {
          useAuthStore.getState().startSession('replacement-token')
          useAuthStore.getState().setUser({ ...user, id: 3 })
        })
      expect(signal.aborted).toBe(true)
      await act(async () => {
        const destination = {
          url: 'https://billing.stripe.com/session/obsolete',
        }
        if (invalidation === 'body') body.resolve(destination)
        else portal.resolve(new Response(JSON.stringify(destination)))
      })
      expect(window.location.assign).not.toHaveBeenCalled()
      expect(screen.queryByRole('alertdialog')).not.toBeInTheDocument()
      expect(screen.queryByText('portalError')).not.toBeInTheDocument()
    }
  )

  it('allows server-verified deletion with scheduled cancellation and logs out only on success', async () => {
    useAuthStore.getState().setUser({
      ...user,
      subscription_status: 'active',
      cancel_at_period_end: true,
    })
    const pending = deferred<Response>()
    apiFetch.mockReturnValueOnce(pending.promise)
    render(<SettingsPage />)
    const dialog = openSettingsDeletion()
    expect(dialog.queryByRole('alert')).not.toBeInTheDocument()
    const confirm = dialog.getByRole('button', { name: 'deleteAccountConfirm' })
    fireEvent.click(confirm)
    fireEvent.click(confirm)
    expect(apiFetch).toHaveBeenCalledTimes(1)
    expect(confirm).toBeDisabled()
    expect(dialog.getByRole('button', { name: 'cancel' })).toBeDisabled()
    expect(useAuthStore.getState().accessToken).toBe('original-token')
    act(() => useAuthStore.getState().setTokens('rotated-token'))
    await act(async () => pending.resolve(new Response(null, { status: 204 })))
    expect(useAuthStore.getState().accessToken).toBeNull()
    expect(push).toHaveBeenCalledExactlyOnceWith('/login')
  })

  it('shows a safe error after transport or invalid JSON failures and permits retry', async () => {
    apiFetch
      .mockRejectedValueOnce(new Error('private network error'))
      .mockResolvedValueOnce(new Response('not JSON', { status: 503 }))
    render(<SettingsPage />)
    const dialog = openSettingsDeletion()
    const confirm = dialog.getByRole('button', { name: 'deleteAccountConfirm' })
    fireEvent.click(confirm)
    await waitFor(() =>
      expect(dialog.getByRole('alert')).toHaveTextContent('failed')
    )
    fireEvent.click(confirm)
    await waitFor(() => expect(confirm).toBeEnabled())
    expect(apiFetch).toHaveBeenCalledTimes(2)
    expect(dialog.getByRole('alert')).toHaveTextContent('failed')
    expect(useAuthStore.getState().accessToken).toBe('original-token')
  })

  it.each(['session', 'unmount'] as const)(
    'ignores a successful late deletion after %s',
    async (change) => {
      const pending = deferred<Response>()
      apiFetch.mockReturnValueOnce(pending.promise)
      const { unmount } = render(<SettingsPage />)
      fireEvent.click(
        openSettingsDeletion().getByRole('button', {
          name: 'deleteAccountConfirm',
        })
      )
      if (change === 'unmount') unmount()
      else
        act(() => {
          useAuthStore.getState().startSession('replacement-token')
          useAuthStore.getState().setUser({ ...user, id: 3 })
        })
      expect(apiFetch.mock.calls[0][1].signal.aborted).toBe(true)
      await act(async () =>
        pending.resolve(new Response(null, { status: 204 }))
      )
      expect(useAuthStore.getState().accessToken).toBe(
        change === 'session' ? 'replacement-token' : 'original-token'
      )
      expect(push).not.toHaveBeenCalled()
    }
  )

  it('ignores delayed error body decoding after session replacement', async () => {
    const body = deferred<{ detail: string }>()
    const json = vi.fn(() => body.promise)
    apiFetch.mockResolvedValueOnce({ ok: false, status: 409, json })
    render(<SettingsPage />)
    fireEvent.click(
      openSettingsDeletion().getByRole('button', {
        name: 'deleteAccountConfirm',
      })
    )
    await waitFor(() => expect(json).toHaveBeenCalled())
    act(() => {
      useAuthStore.getState().startSession('replacement-token')
      useAuthStore.getState().setUser({ ...user, id: 3 })
    })
    await act(async () =>
      body.resolve({ detail: 'subscription_cancellation_required' })
    )
    expect(screen.queryByRole('alertdialog')).not.toBeInTheDocument()
    expect(openSettingsDeletion().queryByRole('alert')).not.toBeInTheDocument()
    expect(push).not.toHaveBeenCalled()
  })
})

describe('admin account deletion', () => {
  const remove = vi.fn()
  beforeEach(() => {
    remove.mockReset()
    useAuthStore.getState().setUser({ ...user, role: 'admin' })
    apiFetch.mockImplementation((url: string, options?: RequestInit) => {
      if (options?.method === 'DELETE') return remove()
      return Promise.resolve(
        new Response(JSON.stringify({ items: [listedUser], total: 1 }))
      )
    })
  })

  async function openAdminDeletion() {
    const buttons = await screen.findAllByRole('button', { name: 'delete' })
    fireEvent.click(buttons[0])
    return within(screen.getByRole('alertdialog'))
  }

  it.each(rejections)(
    'keeps the user and modal after %s %s',
    async (status, detail, key) => {
      remove.mockResolvedValueOnce(response(detail, status))
      render(<AdminUsersPage />)
      const dialog = await openAdminDeletion()
      const callsBeforeDelete = apiFetch.mock.calls.length
      fireEvent.click(dialog.getByRole('button', { name: 'deleteConfirm' }))
      await waitFor(() =>
        expect(dialog.getByRole('alert')).toHaveTextContent(key)
      )
      expect(apiFetch).toHaveBeenCalledTimes(callsBeforeDelete + 1)
      expect(screen.getAllByText('Other learner').length).toBeGreaterThan(0)
      expect(
        dialog.getByRole('button', { name: 'deleteConfirm' })
      ).toBeEnabled()
    }
  )

  it('keeps transport failure retryable and refreshes the list only on success', async () => {
    remove
      .mockRejectedValueOnce(new Error('offline'))
      .mockResolvedValueOnce(new Response(null, { status: 204 }))
    render(<AdminUsersPage />)
    const dialog = await openAdminDeletion()
    const callsBeforeDelete = apiFetch.mock.calls.length
    fireEvent.click(dialog.getByRole('button', { name: 'deleteConfirm' }))
    await waitFor(() =>
      expect(dialog.getByRole('alert')).toHaveTextContent('failed')
    )
    fireEvent.click(dialog.getByRole('button', { name: 'deleteConfirm' }))
    await waitFor(() =>
      expect(screen.queryByRole('alertdialog')).not.toBeInTheDocument()
    )
    expect(apiFetch).toHaveBeenCalledTimes(callsBeforeDelete + 3)
    expect(useAuthStore.getState().accessToken).toBe('original-token')
  })

  it.each(['session', 'unmount'] as const)(
    'ignores a late success after %s',
    async (change) => {
      const pending = deferred<Response>()
      remove.mockReturnValueOnce(pending.promise)
      const { unmount } = render(<AdminUsersPage />)
      const dialog = await openAdminDeletion()
      fireEvent.click(dialog.getByRole('button', { name: 'deleteConfirm' }))
      const calls = apiFetch.mock.calls.length
      const signal = apiFetch.mock.calls[calls - 1][1].signal
      if (change === 'unmount') unmount()
      else act(() => useAuthStore.getState().startSession('replacement-token'))
      expect(signal.aborted).toBe(true)
      await act(async () =>
        pending.resolve(new Response(null, { status: 204 }))
      )
      expect(apiFetch).toHaveBeenCalledTimes(calls)
      expect(screen.queryByRole('alertdialog')).not.toBeInTheDocument()
    }
  )
})
