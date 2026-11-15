import {
  act,
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import ChatPage from '@/app/(app)/chat/page'
import { useAuthStore } from '@/store/auth'
import { useConfigStore } from '@/store/config'
import { useFreemiumStore } from '@/store/freemium'

vi.mock('next-intl', () => {
  const translate = (key: string) => key
  return { useTranslations: () => translate, useLocale: () => 'en' }
})

// Keep the page, paywall, quota banner, stores and apiFetch real.
const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status })
const quota = (remaining: number) => ({
  trial_active: false,
  trial_ends_at: null,
  chat_remaining: remaining,
  chat_limit: 3,
  lessons_remaining: 2,
  lessons_limit: 3,
  listening_remaining: 2,
  listening_limit: 2,
  reading_remaining: 2,
  reading_limit: 2,
  games_remaining: 3,
  games_limit: 3,
  voice_remaining_seconds: 900,
  voice_limit_seconds: 900,
})
function startAccount(id: number) {
  useAuthStore.getState().startSession(`token-${id}`)
  useAuthStore.getState().setUser({
    id,
    username: `account-${id}`,
    displayName: `Account ${id}`,
    role: 'user',
    subscription_status: 'none',
    conversation_max_duration: 300,
    conversation_inactivity_timeout: 30,
  })
}

beforeEach(() => {
  vi.stubGlobal('fetch', vi.fn())
  Element.prototype.scrollIntoView = vi.fn()
  startAccount(1)
  useConfigStore.setState({
    loaded: true,
    stripeEnabled: true,
    maintenanceMode: false,
  })
})

afterEach(() => {
  cleanup()
  vi.useRealTimers()
  vi.unstubAllGlobals()
})

describe('Chat freemium session ownership', () => {
  it.each(['http', 'transport'])('localizes %s failures without exposing technical text', async (failure) => {
    vi.mocked(fetch).mockImplementation(async (url) => {
      if (url === '/api/freemium/status') return json(quota(2))
      if (url === '/api/chat') {
        if (failure === 'transport') throw new Error('technical_internal_message')
        return json({ detail: 'technical_internal_message' }, 402)
      }
      return json([])
    })
    render(<ChatPage />)
    await waitFor(() => expect(screen.getByPlaceholderText('placeholder')).toBeEnabled())
    fireEvent.change(screen.getByPlaceholderText('placeholder'), { target: { value: 'Hello' } })
    fireEvent.click(screen.getByRole('button', { name: 'send' }))
    expect(await screen.findByText(/errorMessage/)).toBeVisible()
    expect(screen.queryByText('technical_internal_message')).not.toBeInTheDocument()
    expect(screen.queryByText('paywallChatTitle')).not.toBeInTheDocument()
  })

  it.each(['expiry', 'toggle'])(
    'updates the consuming controls at a trial %s without another user action',
    async (change) => {
      vi.useFakeTimers()
      vi.setSystemTime(new Date('2026-11-15T12:00:00Z'))
      useConfigStore.setState({ freemiumTrialEnabled: true })
      useAuthStore.getState().setUser({
        ...useAuthStore.getState().user!,
        freemium_trial_ends_at: new Date(Date.now() + 1_000).toISOString(),
      })
      vi.mocked(fetch).mockImplementation(async (url) =>
        url === '/api/freemium/status' ? json(quota(0)) : json([])
      )
      await act(async () => { render(<ChatPage />) })
      expect(screen.getByPlaceholderText('placeholder')).toBeEnabled()
      expect(screen.queryByText('paywallChatTitle')).not.toBeInTheDocument()
      if (change === 'expiry') {
        await act(async () => { await vi.advanceTimersByTimeAsync(1_000) })
      } else {
        act(() => useConfigStore.setState({ freemiumTrialEnabled: false }))
      }
      expect(screen.getByText('paywallChatTitle')).toBeVisible()
      expect(screen.queryByPlaceholderText('placeholder')).not.toBeInTheDocument()
    }
  )

  it.each(['freemium_exhausted', 'freemium_unavailable'])(
    'handles %s without losing the draft or inventing a saved message',
    async (reason) => {
      let quotaReads = 0
      vi.mocked(fetch).mockImplementation(async (url) => {
        if (url === '/api/freemium/status') {
          quotaReads += 1
          return quotaReads === 1 ? json(quota(2)) : json({}, 503)
        }
        if (url === '/api/chat')
          return json({ detail: { reason, feature: 'chat', remaining: 0, limit: 3 } }, 402)
        return json([])
      })
      render(<ChatPage />)
      await screen.findByText('2/3')
      await waitFor(() => expect(screen.getByPlaceholderText('placeholder')).toBeEnabled())
      fireEvent.change(screen.getByPlaceholderText('placeholder'), {
        target: { value: 'Keep this draft' },
      })
      fireEvent.click(screen.getByRole('button', { name: 'send' }))
      if (reason === 'freemium_exhausted') {
        expect(await screen.findByText('paywallChatTitle')).toBeVisible()
        expect(quotaReads).toBe(2)
        act(() => useFreemiumStore.setState({ status: quota(2), lastFetch: Date.now() }))
      } else {
        expect(await screen.findByText(/errorMessage/)).toBeVisible()
        expect(screen.queryByText('paywallChatTitle')).not.toBeInTheDocument()
        expect(quotaReads).toBe(1)
      }
      expect(screen.getByPlaceholderText('placeholder')).toHaveValue('Keep this draft')
      expect(screen.queryByText('Keep this draft')).not.toBeInTheDocument()
      if (reason === 'freemium_exhausted')
        expect(screen.queryByText(/errorMessage/)).not.toBeInTheDocument()
      expect(vi.mocked(fetch).mock.calls.filter(([url]) => url === '/api/chat')).toHaveLength(1)
    }
  )

  it('ignores a late quota denial decoded after session replacement', async () => {
    let finish!: (body: unknown) => void
    const body = new Promise((resolve) => { finish = resolve })
    const denied = json({}, 402)
    vi.spyOn(denied, 'json').mockReturnValue(body)
    let quotaReads = 0
    vi.mocked(fetch).mockImplementation(async (url) => {
      if (url === '/api/freemium/status') {
        quotaReads += 1
        return json(quota(2))
      }
      if (url === '/api/chat') return denied
      return json([])
    })
    render(<ChatPage />)
    await waitFor(() => expect(screen.getByPlaceholderText('placeholder')).toBeEnabled())
    fireEvent.change(screen.getByPlaceholderText('placeholder'), { target: { value: 'Hello' } })
    fireEvent.click(screen.getByRole('button', { name: 'send' }))
    await waitFor(() => expect(denied.json).toHaveBeenCalled())
    act(() => startAccount(2))
    await screen.findByText('2/3')
    const readsBefore = quotaReads
    await act(async () => finish({ detail: { reason: 'freemium_exhausted', feature: 'chat' } }))
    expect(quotaReads).toBe(readsBefore)
    expect(screen.queryByText('paywallChatTitle')).not.toBeInTheDocument()
  })

  it.each([
    { a: 0, b: 2, fails: false },
    { a: 2, b: 0, fails: false },
    { a: 0, b: 2, fails: true },
  ])(
    'uses only B quota for the real banner/paywall ($a → $b, failure=$fails)',
    async ({ a, b, fails }) => {
      let finish!: (response: Response) => void
      const pending = new Promise<Response>((resolve) => {
        finish = resolve
      })
      const tokens: unknown[] = []
      vi.mocked(fetch).mockImplementation(async (url, options) => {
        if (url === '/api/freemium/status') {
          const token = (options?.headers as Record<string, string>)
            .Authorization
          tokens.push(token)
          return token === 'Bearer token-1' ? json(quota(a)) : pending
        }
        return json([])
      })
      const first = render(<ChatPage />)
      expect(await screen.findByText(`${a}/3`)).toBeInTheDocument()
      expect(!!screen.queryByText('paywallChatTitle')).toBe(a === 0)
      first.unmount()

      act(() => {
        useAuthStore.getState().logout()
        startAccount(2)
      })
      render(<ChatPage />)
      await waitFor(() =>
        expect(tokens).toEqual(['Bearer token-1', 'Bearer token-2'])
      )
      expect(screen.queryByText(`${a}/3`)).not.toBeInTheDocument()
      expect(screen.queryByText('paywallChatTitle')).not.toBeInTheDocument()
      expect(useFreemiumStore.getState().status).toBeNull()

      await act(async () => {
        finish(fails ? json({}, 503) : json(quota(b)))
      })
      if (fails) {
        expect(screen.queryByText(`${a}/3`)).not.toBeInTheDocument()
        expect(screen.queryByText('paywallChatTitle')).not.toBeInTheDocument()
        expect(useFreemiumStore.getState().status).toBeNull()
      } else {
        expect(await screen.findByText(`${b}/3`)).toBeInTheDocument()
        expect(!!screen.queryByText('paywallChatTitle')).toBe(b === 0)
        expect(!!screen.queryByPlaceholderText('placeholder')).toBe(b > 0)
      }
    }
  )

  it.each([false, true])(
    'scopes delayed stream consumption to its session (replacement=%s)',
    async (replace) => {
      let controller!: ReadableStreamDefaultController<Uint8Array>
      const stream = new ReadableStream<Uint8Array>({
        start(value) {
          controller = value
        },
      })
      vi.mocked(fetch).mockImplementation(async (url) => {
        if (url === '/api/freemium/status') return json(quota(2))
        if (url === '/api/chat') return new Response(stream)
        return json([])
      })
      const view = render(<ChatPage />)
      await screen.findByText('2/3')
      fireEvent.change(screen.getByPlaceholderText('placeholder'), {
        target: { value: 'Hello' },
      })
      fireEvent.click(screen.getByRole('button', { name: 'send' }))
      await waitFor(() =>
        expect(fetch).toHaveBeenCalledWith('/api/chat', expect.anything())
      )
      if (replace) {
        view.unmount()
        useAuthStore.getState().logout()
        startAccount(2)
        await useFreemiumStore.getState().fetchStatus()
      } else {
        act(() => useAuthStore.getState().setTokens('rotated-token'))
      }
      await act(async () => {
        controller.enqueue(new TextEncoder().encode('data: {"done":true}\n\n'))
        controller.close()
      })
      expect(useFreemiumStore.getState().status?.chat_remaining).toBe(
        replace ? 2 : 1
      )
    }
  )
})
