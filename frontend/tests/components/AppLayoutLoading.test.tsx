import { act, cleanup, render, screen } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import AppLayout from '@/app/(app)/layout'
import { PageLoading } from '@/components/ui/page-loading'
import { useAuthStore } from '@/store/auth'
import { useConfigStore } from '@/store/config'
import { useLoadingStore } from '@/store/loading'

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

let finishProfile: (response: Response) => void

beforeEach(() => {
  vi.clearAllMocks()
  vi.useFakeTimers({ toFake: ['setTimeout', 'clearTimeout', 'performance'] })
  useAuthStore.setState({ accessToken: 'test-token', user: null })
  useConfigStore.setState({ loaded: true, stripeEnabled: false })
  useLoadingStore.setState({ count: 0, complete: false })
  const pendingProfile = new Promise<Response>((resolve) => {
    finishProfile = resolve
  })
  vi.stubGlobal(
    'fetch',
    vi.fn(async (url) => {
      if (url === '/api/auth/me') return pendingProfile
      if (url === '/api/feedback/unread-summary')
        return Response.json({ unread_count: 0 })
      throw new Error(`Unexpected request: ${String(url)}`)
    })
  )
})

afterEach(() => {
  cleanup()
  vi.useRealTimers()
  vi.unstubAllGlobals()
})

function page(loading: boolean) {
  return (
    <AppLayout>
      {loading ? (
        <PageLoading label="Loading page data" />
      ) : (
        <button>Ready action</button>
      )}
    </AppLayout>
  )
}

const advance = (ms: number) => act(() => vi.advanceTimersByTime(ms))
const restoreProfile = () =>
  act(async () => {
    finishProfile(Response.json(profile))
  })

describe('loading across the real application shell', () => {
  it('does not show either indicator when initialization and page loading finish within 200 ms', async () => {
    const { rerender } = render(page(true))
    advance(100)
    await restoreProfile()
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
    expect(screen.queryByRole('progressbar')).not.toBeInTheDocument()

    advance(50)
    rerender(page(false))
    advance(0)
    expect(screen.getByRole('button', { name: 'Ready action' })).toBeVisible()
    advance(1000)
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
    expect(screen.queryByRole('progressbar')).not.toBeInTheDocument()
    expect(useLoadingStore.getState().count).toBe(0)
  })

  it('shares appearance and retention deadlines when initialization replaces its viewport', async () => {
    const { rerender } = render(page(true))
    advance(200)
    expect(screen.getByRole('status')).toHaveTextContent('initializing')

    advance(50)
    await restoreProfile()
    expect(screen.getByRole('status')).toHaveTextContent('Loading page data')
    expect(screen.queryByRole('progressbar')).not.toBeInTheDocument()

    advance(100)
    rerender(page(false))
    expect(
      screen.queryByRole('button', { name: 'Ready action' })
    ).not.toBeInTheDocument()
    advance(149)
    expect(screen.getByRole('status')).toBeInTheDocument()
    advance(1)
    expect(screen.getByRole('button', { name: 'Ready action' })).toBeVisible()
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
    advance(1000)
    expect(screen.queryByRole('progressbar')).not.toBeInTheDocument()
    expect(navigation.push).not.toHaveBeenCalled()
  })
})
