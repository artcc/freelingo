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
  vi.unstubAllGlobals()
})

describe('Chat freemium session ownership', () => {
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
