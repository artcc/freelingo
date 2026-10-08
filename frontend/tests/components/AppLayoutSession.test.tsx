import { StrictMode } from 'react'
import { act, cleanup, render, screen } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

const navigation = vi.hoisted(() => ({ push: vi.fn(), replace: vi.fn() }))

vi.mock('next/navigation', () => ({
  useRouter: () => navigation,
  usePathname: () => '/dashboard',
}))
vi.mock('next-intl', () => ({ useTranslations: () => (key: string) => key }))
vi.mock('@/components/LanguageSwitcher', () => ({ default: () => null }))
vi.mock('@/components/AuthAvatarImage', () => ({ AuthAvatarImage: () => null }))
vi.mock('@/components/ui/confirm-dialog', () => ({ ConfirmDialog: () => null }))
vi.mock('@/components/ui/contact-form-modal', () => ({
  ContactFormModal: () => null,
}))
vi.mock('@/components/ui/loading-bar', () => ({ LoadingBar: () => null }))
vi.mock('@/components/ui/page-loading', () => ({
  PageLoading: () => <div>Restoring session</div>,
}))

import AppLayout from '@/app/(app)/layout'
import { TOUR_STORAGE_KEY } from '@/lib/onboarding-tour'
import { useAuthStore } from '@/store/auth'
import { useConfigStore } from '@/store/config'
import { useLoadingStore } from '@/store/loading'

const profile = {
  id: 7,
  username: 'learner',
  display_name: 'Learner',
  role: 'user',
  is_verified: true,
  learning_goals: [],
  conversation_max_duration: 1800,
  conversation_inactivity_timeout: 180,
}

function json(value: unknown, status = 200) {
  return new Response(JSON.stringify(value), {
    status,
    headers: { 'Content-Type': 'application/json' },
  })
}

beforeEach(() => {
  vi.clearAllMocks()
  useAuthStore.setState({ accessToken: null, user: null })
  useConfigStore.setState({ loaded: true, stripeEnabled: false })
  useLoadingStore.setState({ count: 0 })
  localStorage.setItem(TOUR_STORAGE_KEY, '1')
  localStorage.setItem('fl_cookie_consent', 'accepted')
  vi.stubGlobal('fetch', vi.fn())
})

afterEach(() => {
  cleanup()
  vi.unstubAllGlobals()
})

describe('AppLayout session restoration after a full reload', () => {
  it.each([false, true])(
    'restores one rotated session and preserves the completed tour with StrictMode=%s',
    async (strict) => {
      let completeRefresh!: (response: Response) => void
      const pendingRefresh = new Promise<Response>((resolve) => {
        completeRefresh = resolve
      })
      let refreshRequests = 0
      vi.mocked(fetch).mockImplementation(async (url, options) => {
        if (url === '/api/auth/refresh') {
          refreshRequests++
          // The server consumes the old cookie before the browser receives its
          // replacement. A concurrent reuse can therefore legitimately get 401.
          if (refreshRequests === 1) return pendingRefresh
          return json({ detail: 'Invalid or expired refresh token' }, 401)
        }
        if (url === '/api/auth/me') {
          const headers = new Headers(options?.headers)
          return headers.get('Authorization') === 'Bearer restored-token'
            ? json(profile)
            : json({ detail: 'Unauthorized' }, 401)
        }
        if (url === '/api/feedback/unread-summary')
          return json({ unread_count: 0 })
        throw new Error(`Unexpected request: ${String(url)}`)
      })

      const layout = (
        <AppLayout>
          <div>Authenticated content</div>
        </AppLayout>
      )
      render(strict ? <StrictMode>{layout}</StrictMode> : layout)
      await act(async () => {
        completeRefresh(json({ access_token: 'restored-token' }))
      })

      expect.soft(refreshRequests).toBe(1)
      expect.soft(navigation.push).not.toHaveBeenCalled()
      expect.soft(useAuthStore.getState().accessToken).toBe('restored-token')
      expect.soft(useAuthStore.getState().user?.id).toBe(profile.id)
      expect.soft(localStorage.getItem(TOUR_STORAGE_KEY)).toBe('1')
      expect.soft(localStorage.getItem('fl_cookie_consent')).toBe('accepted')
      expect(screen.getByText('Authenticated content')).toBeInTheDocument()
      expect(fetch).toHaveBeenCalledWith(
        '/api/auth/refresh',
        expect.objectContaining({
          method: 'POST',
          credentials: 'include',
        })
      )
    }
  )

  it('still clears client authentication when the refresh cookie is genuinely invalid', async () => {
    vi.mocked(fetch).mockImplementation(async (url) => {
      if (url === '/api/auth/refresh') {
        return json({ detail: 'Invalid or expired refresh token' }, 401)
      }
      if (url === '/api/feedback/unread-summary')
        return json({ unread_count: 0 })
      throw new Error(`Unexpected request: ${String(url)}`)
    })

    await act(async () => {
      render(
        <AppLayout>
          <div>Authenticated content</div>
        </AppLayout>
      )
    })

    expect(navigation.push).toHaveBeenCalledWith('/login')
    expect(useAuthStore.getState().accessToken).toBeNull()
    expect(useAuthStore.getState().user).toBeNull()
    expect(localStorage.getItem(TOUR_STORAGE_KEY)).toBeNull()
    expect(localStorage.getItem('fl_cookie_consent')).toBe('accepted')
  })

  it.each([200, 401])(
    'ignores a refresh response with status %s after unmount',
    async (status) => {
      let complete!: (response: Response) => void
      vi.mocked(fetch).mockReturnValue(
        new Promise<Response>((resolve) => {
          complete = resolve
        })
      )
      const { unmount } = render(
        <AppLayout>
          <div>Authenticated content</div>
        </AppLayout>
      )
      unmount()

      await act(async () => {
        complete(
          status === 200
            ? json({ access_token: 'obsolete-token' })
            : json({ detail: 'Invalid refresh token' }, status)
        )
      })

      expect(fetch).toHaveBeenCalledTimes(1)
      expect(useAuthStore.getState().accessToken).toBeNull()
      expect(useAuthStore.getState().user).toBeNull()
      expect(navigation.push).not.toHaveBeenCalled()
      expect(localStorage.getItem(TOUR_STORAGE_KEY)).toBe('1')
    }
  )

  it('shares a pending rotation across an actual unmount and remount', async () => {
    let complete!: (response: Response) => void
    const pending = new Promise<Response>((resolve) => {
      complete = resolve
    })
    vi.mocked(fetch).mockImplementation(async (url) => {
      if (url === '/api/auth/refresh') return pending
      if (url === '/api/auth/me') return json(profile)
      if (url === '/api/feedback/unread-summary')
        return json({ unread_count: 0 })
      throw new Error(`Unexpected request: ${String(url)}`)
    })
    const first = render(
      <AppLayout>
        <div>Previous page</div>
      </AppLayout>
    )
    first.unmount()
    render(
      <AppLayout>
        <div>Current page</div>
      </AppLayout>
    )

    await act(async () => {
      complete(json({ access_token: 'restored-token' }))
    })

    expect(
      vi.mocked(fetch).mock.calls.filter(([url]) => url === '/api/auth/refresh')
    ).toHaveLength(1)
    expect(
      vi.mocked(fetch).mock.calls.filter(([url]) => url === '/api/auth/me')
    ).toHaveLength(1)
    expect(useAuthStore.getState().accessToken).toBe('restored-token')
    expect(screen.getByText('Current page')).toBeInTheDocument()
    expect(navigation.push).not.toHaveBeenCalled()
    expect(localStorage.getItem(TOUR_STORAGE_KEY)).toBe('1')
  })

  it.each([200, 401, 503])(
    'ignores an obsolete profile response with status %s',
    async (status) => {
      useAuthStore.setState({ accessToken: 'previous-token' })
      let complete!: (response: Response) => void
      vi.mocked(fetch).mockReturnValue(
        new Promise<Response>((resolve) => {
          complete = resolve
        })
      )
      const { unmount } = render(
        <AppLayout>
          <div>Previous page</div>
        </AppLayout>
      )
      unmount()
      expect(vi.mocked(fetch).mock.calls[0][1]?.signal?.aborted).toBe(true)
      useAuthStore.setState({ accessToken: 'current-token' })

      await act(async () => {
        complete(json(profile, status))
      })

      expect(useAuthStore.getState().accessToken).toBe('current-token')
      expect(useAuthStore.getState().user).toBeNull()
      expect(navigation.push).not.toHaveBeenCalled()
      expect(navigation.replace).not.toHaveBeenCalled()
      expect(localStorage.getItem(TOUR_STORAGE_KEY)).toBe('1')
      expect(fetch).toHaveBeenCalledTimes(1)
    }
  )

  it.each([200, 401])(
    'preserves a newer session when an initializer refresh finishes with %s',
    async (status) => {
      let complete!: (response: Response) => void
      vi.mocked(fetch).mockReturnValue(
        new Promise<Response>((resolve) => {
          complete = resolve
        })
      )
      const { unmount } = render(
        <AppLayout>
          <div>Previous page</div>
        </AppLayout>
      )
      unmount()
      useAuthStore.getState().startSession('current-token')
      await act(async () =>
        complete(
          status === 200
            ? json({ access_token: 'obsolete-token' })
            : json({}, status)
        )
      )
      expect(useAuthStore.getState().accessToken).toBe('current-token')
      expect(navigation.push).not.toHaveBeenCalled()
      expect(localStorage.getItem(TOUR_STORAGE_KEY)).toBe('1')
      expect(fetch).toHaveBeenCalledTimes(1)
    }
  )
})
