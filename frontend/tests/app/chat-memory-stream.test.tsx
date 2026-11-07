import {
  act,
  fireEvent,
  render,
  screen,
  waitFor,
  within,
} from '@testing-library/react'
import type { ElementType, HTMLAttributes, ReactNode } from 'react'
import { beforeEach, describe, expect, it, vi } from 'vitest'

const mocks = vi.hoisted(() => ({
  apiFetch: vi.fn(),
  fetchFreemium: vi.fn(),
  decrementFreemium: vi.fn(),
  dismissTooltip: vi.fn(),
  handleTextSelection: vi.fn(),
  audioPlayer: vi.fn(),
  sessionVersion: 0,
  languageCode: 'en-GB',
}))

vi.mock('next-intl', () => ({
  useTranslations: () => (key: string) => key,
}))
vi.mock('@/lib/api', () => ({ apiFetch: mocks.apiFetch }))
vi.mock('@/store/auth', () => ({
  useAuthStore: (selector: (state: object) => unknown) =>
    selector({
      sessionVersion: mocks.sessionVersion,
      user: {
        username: 'learner',
        displayName: 'Learner',
        avatarUrl: null,
        subscription_status: 'active',
      },
    }),
  isSubscribed: () => true,
  isFreemiumTrialActive: () => false,
}))
vi.mock('@/store/language', () => ({
  useLanguageStore: (selector: (state: object) => unknown) =>
    selector({ activeLanguage: { code: mocks.languageCode } }),
}))
vi.mock('@/store/config', () => ({
  useConfigStore: (selector: (state: object) => unknown) =>
    selector({ stripeEnabled: false }),
}))
vi.mock('@/store/freemium', () => ({
  useFreemiumStore: (selector: (state: object) => unknown) =>
    selector({
      status: null,
      fetchStatus: mocks.fetchFreemium,
      decrement: mocks.decrementFreemium,
    }),
}))
vi.mock('@/components/billing/MaintenanceBanner', () => ({
  MaintenanceGate: ({ children }: { children: ReactNode }) => children,
}))
vi.mock('@/components/billing/PaywallBanner', () => ({
  PaywallBanner: () => null,
}))
vi.mock('@/components/billing/FreemiumQuotaBanner', () => ({
  FreemiumQuotaBanner: () => null,
}))
vi.mock('@/components/ui/AudioPlayer', () => ({
  AudioPlayer: (props: object) => {
    mocks.audioPlayer(props)
    return null
  },
}))
vi.mock('@/components/ui/WordTooltip', () => ({
  WordTooltip: () => null,
  useWordSave: () => ({
    selectedWord: null,
    tooltipPos: null,
    saveState: 'idle',
    handleTextSelection: mocks.handleTextSelection,
    handleSaveWord: vi.fn(),
    dismissTooltip: mocks.dismissTooltip,
  }),
}))
vi.mock('@/components/ui/page-loading', () => ({
  PageLoading: () => <div role="status">loading</div>,
}))
vi.mock('@/components/TargetLanguageText', () => ({
  TargetLanguageText: ({
    children,
    as: Component = 'div',
    languageCode,
    reading,
    translation,
    ...props
  }: {
    children: ReactNode
    as?: ElementType
    languageCode?: string | null
    reading?: string | null
    translation?: string | null
  } & HTMLAttributes<HTMLElement>) => (
    <Component
      data-language-code={languageCode ?? undefined}
      data-reading={reading ?? undefined}
      data-translation={translation ?? undefined}
      {...props}
    >
      {children}
    </Component>
  ),
}))
vi.mock('@/components/AuthAvatarImage', () => ({
  AuthAvatarImage: () => null,
}))

import ChatPage from '@/app/(app)/chat/page'

function jsonResponse(data: unknown) {
  return new Response(JSON.stringify(data), {
    status: 200,
    headers: { 'Content-Type': 'application/json' },
  })
}

function deferred<T>() {
  let resolve!: (value: T) => void
  let reject!: (error: unknown) => void
  const promise = new Promise<T>((yes, no) => {
    resolve = yes
    reject = no
  })
  return { promise, resolve, reject }
}

const conversations = [
  { id: 7, title: 'Conversation A', source: 'chat' },
  { id: 8, title: 'Conversation B', source: 'chat' },
]

const historyResponse = (content: string) =>
  jsonResponse({
    messages: [{ role: 'assistant', content }],
  })

function chatStreamResponse(events: Array<Record<string, unknown>>) {
  const encoder = new TextEncoder()
  return new Response(
    new ReadableStream<Uint8Array>({
      start(controller) {
        for (const event of events) {
          controller.enqueue(
            encoder.encode(`data: ${JSON.stringify(event)}\n\n`)
          )
        }
        controller.close()
      },
    }),
    { status: 200 }
  )
}

function controlledChatStreamResponse() {
  const encoder = new TextEncoder()
  let controller: ReadableStreamDefaultController<Uint8Array> | null = null
  const response = new Response(
    new ReadableStream<Uint8Array>({
      start(streamController) {
        controller = streamController
      },
    }),
    { status: 200 }
  )

  return {
    response,
    enqueue(event: Record<string, unknown>) {
      if (!controller) throw new Error('Chat stream is not initialized')
      controller.enqueue(encoder.encode(`data: ${JSON.stringify(event)}\n\n`))
    },
    close() {
      if (!controller) throw new Error('Chat stream is not initialized')
      controller.close()
    },
  }
}

describe('chat memory stream', () => {
  let chatEvents: Array<Record<string, unknown>>

  beforeEach(() => {
    mocks.sessionVersion = 0
    mocks.languageCode = 'en-GB'
    mocks.apiFetch.mockReset()
    mocks.fetchFreemium.mockReset()
    mocks.decrementFreemium.mockReset()
    mocks.dismissTooltip.mockReset()
    mocks.handleTextSelection.mockReset()
    mocks.audioPlayer.mockReset()
    Element.prototype.scrollIntoView = vi.fn()
    chatEvents = [
      { conversation_id: 7 },
      { token: 'Partial response.' },
      { response_reset: true },
      { token: 'Complete normal response.' },
      { done: true },
    ]
    mocks.apiFetch.mockImplementation((path: string) => {
      if (path === '/api/chat') {
        return Promise.resolve(chatStreamResponse(chatEvents))
      }
      return Promise.resolve(jsonResponse([]))
    })
  })

  it.each(['http', 'network'])(
    'keeps failed %s history distinct from an empty chat and retries it',
    async (failure) => {
      let attempts = 0
      mocks.apiFetch.mockImplementation((path: string) => {
        if (path === '/api/chat/conversations')
          return Promise.resolve(jsonResponse(conversations))
        if (++attempts === 1)
          return failure === 'http'
            ? Promise.resolve(new Response(null, { status: 503 }))
            : Promise.reject(new Error('Network'))
        return Promise.resolve(historyResponse('Recovered history'))
      })
      render(<ChatPage />)
      const retry = await screen.findByRole('button', { name: 'retry' })
      expect(screen.getByPlaceholderText('placeholder')).toBeDisabled()
      expect(screen.queryByText('subtitle')).not.toBeInTheDocument()
      fireEvent.click(retry)
      expect(await screen.findByText('Recovered history')).toBeInTheDocument()
      expect(screen.getByPlaceholderText('placeholder')).not.toBeDisabled()
      expect(attempts).toBe(2)
    }
  )

  it('renders a list failure with retry instead of an empty chat', async () => {
    mocks.apiFetch.mockRejectedValue(new Error('Offline'))
    render(<ChatPage />)
    const retries = await screen.findAllByRole('button', { name: 'retry' })
    expect(screen.getByPlaceholderText('placeholder')).toBeDisabled()
    expect(screen.queryByText('subtitle')).not.toBeInTheDocument()
    mocks.apiFetch.mockImplementation((path: string) =>
      Promise.resolve(
        path === '/api/chat/conversations'
          ? jsonResponse(conversations)
          : historyResponse('Recovered list')
      )
    )
    fireEvent.click(retries[0])
    expect(await screen.findByText('Recovered list')).toBeInTheDocument()
  })

  it.each(['list', 'history'])(
    'a %s timeout releases loading into a retryable error',
    async (target) => {
      const deadline = new AbortController()
      vi.spyOn(AbortSignal, 'timeout').mockReturnValue(deadline.signal)
      mocks.apiFetch.mockImplementation(
        (path: string, options: RequestInit) => {
          if (target === 'history' && path === '/api/chat/conversations')
            return Promise.resolve(jsonResponse(conversations))
          return new Promise((_resolve, reject) => {
            options.signal?.addEventListener(
              'abort',
              () => reject(options.signal?.reason),
              { once: true }
            )
          })
        }
      )
      render(<ChatPage />)
      if (target === 'history') await screen.findByText('Conversation B')
      expect(AbortSignal.timeout).toHaveBeenCalledWith(20_000)
      await act(async () => {
        deadline.abort(new DOMException('Timed out', 'TimeoutError'))
      })
      expect(screen.queryByRole('status')).not.toBeInTheDocument()
      expect(
        screen.getAllByRole('button', { name: 'retry' }).length
      ).toBeGreaterThan(0)
      expect(screen.getByPlaceholderText('placeholder')).toBeDisabled()
    }
  )

  it.each(['success', 'failure'])(
    'ignores obsolete A %s/finally while B history is pending',
    async (outcome) => {
      const a = deferred<Response>()
      const b = deferred<Response>()
      mocks.apiFetch.mockImplementation((path: string) => {
        if (path === '/api/chat/conversations')
          return Promise.resolve(jsonResponse(conversations))
        return path.includes('/7/') ? a.promise : b.promise
      })
      render(<ChatPage />)
      fireEvent.click(await screen.findByText('Conversation B'))
      const aSignal = mocks.apiFetch.mock.calls.find(([path]) =>
        path.includes('/7/')
      )![1].signal as AbortSignal
      expect(aSignal.aborted).toBe(true)
      await act(async () => {
        if (outcome === 'success') a.resolve(historyResponse('Obsolete A'))
        else a.reject(new Error('Old failure'))
      })
      expect(screen.getByPlaceholderText('placeholder')).toBeDisabled()
      expect(screen.queryByText('Obsolete A')).not.toBeInTheDocument()
      expect(screen.queryByRole('alert')).not.toBeInTheDocument()
      expect(screen.getByRole('status')).toBeInTheDocument()
      await act(async () => {
        b.resolve(historyResponse('Newest B'))
      })
      expect(screen.getByText('Newest B')).toBeInTheDocument()
      expect(screen.getByPlaceholderText('placeholder')).not.toBeDisabled()
    }
  )

  it('does not replace B when A finishes last, including delayed JSON decoding', async () => {
    const body = deferred<unknown>()
    mocks.apiFetch.mockImplementation((path: string) => {
      if (path === '/api/chat/conversations')
        return Promise.resolve(jsonResponse(conversations))
      if (path.includes('/7/'))
        return Promise.resolve({ ok: true, json: () => body.promise })
      return Promise.resolve(historyResponse('Newest B'))
    })
    render(<ChatPage />)
    fireEvent.click(await screen.findByText('Conversation B'))
    await screen.findByText('Newest B')
    await act(async () => {
      body.resolve({ messages: [{ role: 'assistant', content: 'Obsolete A' }] })
    })
    expect(screen.queryByText('Obsolete A')).not.toBeInTheDocument()
    expect(screen.getByText('Newest B')).toBeInTheDocument()
  })

  it('does not auto-select from a slow initial list after the user starts a new chat', async () => {
    const list = deferred<Response>()
    mocks.apiFetch.mockReturnValue(list.promise)
    render(<ChatPage />)
    expect(screen.getByPlaceholderText('placeholder')).toBeDisabled()
    fireEvent.click(screen.getByRole('button', { name: '+ newConversation' }))
    expect(screen.getByPlaceholderText('placeholder')).not.toBeDisabled()
    await act(async () => {
      list.resolve(jsonResponse(conversations))
    })
    expect(mocks.apiFetch).toHaveBeenCalledTimes(1)
    expect(screen.getByText('subtitle')).toBeInTheDocument()
  })

  it('cancels selected history when starting a new chat without publishing its late failure', async () => {
    const history = deferred<Response>()
    mocks.apiFetch.mockImplementation((path: string) =>
      path === '/api/chat/conversations'
        ? Promise.resolve(jsonResponse(conversations))
        : history.promise
    )
    render(<ChatPage />)
    await screen.findByText('Conversation B')
    fireEvent.click(screen.getByRole('button', { name: '+ newConversation' }))
    const signal = mocks.apiFetch.mock.calls.find(([path]) =>
      path.includes('/7/')
    )![1].signal as AbortSignal
    expect(signal.aborted).toBe(true)
    await act(async () => {
      history.reject(new Error('Late error'))
    })
    expect(screen.queryByRole('alert')).not.toBeInTheDocument()
    expect(screen.getByPlaceholderText('placeholder')).not.toBeDisabled()
    expect(screen.getByText('subtitle')).toBeInTheDocument()
  })

  it.each(['language', 'session'])(
    'discards old history across a %s change without presenting it as current',
    async (scope) => {
      const old = deferred<Response>()
      mocks.apiFetch.mockImplementation((path: string) =>
        path === '/api/chat/conversations'
          ? Promise.resolve(jsonResponse(conversations))
          : old.promise
      )
      const view = render(<ChatPage />)
      await screen.findByText('Conversation B')
      const oldSignal = mocks.apiFetch.mock.calls.find(([path]) =>
        path.includes('/7/')
      )![1].signal as AbortSignal
      const current = deferred<Response>()
      mocks.apiFetch.mockReturnValue(current.promise)
      if (scope === 'language') mocks.languageCode = 'de-DE'
      else mocks.sessionVersion += 1
      view.rerender(<ChatPage />)
      expect(oldSignal.aborted).toBe(true)
      expect(screen.queryByText('Conversation B')).not.toBeInTheDocument()
      await act(async () => {
        old.resolve(historyResponse('Old scope message'))
      })
      expect(screen.queryByText('Old scope message')).not.toBeInTheDocument()
      expect(screen.getByPlaceholderText('placeholder')).toBeDisabled()
      await act(async () => {
        current.resolve(jsonResponse([]))
      })
      expect(screen.getByPlaceholderText('placeholder')).not.toBeDisabled()
    }
  )

  it('deleting A cancels its history and cannot override a newer B selection', async () => {
    const a = deferred<Response>()
    const deletion = deferred<Response>()
    let deleted = false
    mocks.apiFetch.mockImplementation((path: string, options?: RequestInit) => {
      if (options?.method === 'DELETE') return deletion.promise
      if (path === '/api/chat/conversations')
        return Promise.resolve(
          jsonResponse(deleted ? [conversations[1]] : conversations)
        )
      if (path.includes('/7/')) return a.promise
      return Promise.resolve(historyResponse('Keep B'))
    })
    render(<ChatPage />)
    await screen.findByText('Conversation B')
    fireEvent.click(screen.getAllByRole('button', { name: 'deleteConfirm' })[0])
    fireEvent.click(
      within(screen.getByRole('alertdialog')).getByRole('button', {
        name: 'deleteConfirm',
      })
    )
    fireEvent.click(screen.getByText('Conversation B'))
    await screen.findByText('Keep B')
    await act(async () => {
      deleted = true
      deletion.resolve(new Response(null, { status: 204 }))
      a.resolve(historyResponse('Deleted A'))
    })
    expect(screen.queryByText('Deleted A')).not.toBeInTheDocument()
    expect(screen.getByText('Keep B')).toBeInTheDocument()
    expect(
      mocks.apiFetch.mock.calls.filter(([path]) => path.includes('/8/'))
    ).toHaveLength(1)
  })

  it('aborts pending reads on unmount', async () => {
    const pending = deferred<Response>()
    mocks.apiFetch.mockReturnValue(pending.promise)
    const view = render(<ChatPage />)
    const signal = mocks.apiFetch.mock.calls[0][1].signal as AbortSignal
    view.unmount()
    expect(signal.aborted).toBe(true)
    await act(async () => {
      pending.resolve(jsonResponse(conversations))
    })
    expect(mocks.apiFetch).toHaveBeenCalledTimes(1)
  })

  it('does not publish an old stream or memory toast into a replacement session', async () => {
    const stream = controlledChatStreamResponse()
    mocks.apiFetch.mockImplementation((path: string) =>
      Promise.resolve(path === '/api/chat' ? stream.response : jsonResponse([]))
    )
    const view = render(<ChatPage />)
    const input = screen.getByPlaceholderText('placeholder')
    await waitFor(() => expect(input).not.toBeDisabled())
    fireEvent.change(input, { target: { value: 'Hello' } })
    fireEvent.click(screen.getByRole('button', { name: 'send' }))
    await waitFor(() =>
      expect(mocks.apiFetch).toHaveBeenCalledWith(
        '/api/chat',
        expect.anything()
      )
    )
    const signal = mocks.apiFetch.mock.calls.find(
      ([path]) => path === '/api/chat'
    )![1].signal as AbortSignal
    mocks.sessionVersion += 1
    view.rerender(<ChatPage />)
    expect(signal.aborted).toBe(true)
    await act(async () => {
      stream.enqueue({
        token: 'Obsolete stream',
        memory_updated: true,
        done: true,
      })
      stream.close()
    })
    expect(screen.queryByText('Obsolete stream')).not.toBeInTheDocument()
    expect(screen.queryByText('memorySavedToast')).not.toBeInTheDocument()
    expect(screen.queryByText(/errorMessage/)).not.toBeInTheDocument()
    expect(screen.getByPlaceholderText('placeholder')).not.toBeDisabled()
  })

  it('replaces a partial incompatible-tools response with the complete fallback', async () => {
    const stream = controlledChatStreamResponse()
    mocks.apiFetch.mockImplementation((path: string) => {
      if (path === '/api/chat') return Promise.resolve(stream.response)
      return Promise.resolve(jsonResponse([]))
    })
    render(<ChatPage />)

    const input = await screen.findByPlaceholderText('placeholder')
    await waitFor(() => expect(input).not.toBeDisabled())
    fireEvent.change(input, { target: { value: 'Hello' } })
    fireEvent.click(screen.getByRole('button', { name: 'send' }))

    await act(async () => {
      stream.enqueue({ conversation_id: 7 })
      stream.enqueue({ token: '**Partial response.**' })
    })
    expect(await screen.findByText('Partial response.')).toBeInTheDocument()

    await act(async () => {
      stream.enqueue({ response_reset: true })
    })
    await waitFor(() =>
      expect(screen.queryByText('Partial response.')).not.toBeInTheDocument()
    )

    await act(async () => {
      stream.enqueue({ token: '*Complete normal response.*' })
      stream.enqueue({ done: true })
      stream.close()
    })
    expect(
      await screen.findByText('Complete normal response.')
    ).toBeInTheDocument()
    expect(screen.queryByText('Partial response.')).not.toBeInTheDocument()
    expect(screen.queryByText('memorySavedToast')).not.toBeInTheDocument()
    expect(mocks.dismissTooltip).toHaveBeenCalled()
    await waitFor(() =>
      expect(mocks.apiFetch).toHaveBeenCalledWith(
        '/api/chat',
        expect.anything()
      )
    )
  })

  it('enables assistant word selection only after streaming completes', async () => {
    const stream = controlledChatStreamResponse()
    mocks.apiFetch.mockImplementation((path: string) => {
      if (path === '/api/chat') return Promise.resolve(stream.response)
      return Promise.resolve(jsonResponse([]))
    })
    render(<ChatPage />)

    const input = await screen.findByPlaceholderText('placeholder')
    await waitFor(() => expect(input).not.toBeDisabled())
    fireEvent.change(input, { target: { value: 'Hello' } })
    fireEvent.click(screen.getByRole('button', { name: 'send' }))

    await act(async () => {
      stream.enqueue({ conversation_id: 7 })
      stream.enqueue({ token: '- **Streaming** response.' })
    })
    const response = await screen.findByText('Streaming')
    expect(response.tagName).toBe('STRONG')
    expect(response.closest('li')).not.toBeNull()
    fireEvent.pointerUp(response)
    expect(mocks.handleTextSelection).not.toHaveBeenCalled()

    await act(async () => {
      stream.enqueue({ done: true })
      stream.close()
    })
    await waitFor(() => expect(input).not.toBeDisabled())
    fireEvent.pointerUp(response)
    expect(mocks.handleTextSelection).toHaveBeenCalledWith(
      '- **Streaming** response.'
    )
    expect(mocks.audioPlayer).toHaveBeenCalledWith(
      expect.objectContaining({
        text: '- **Streaming** response.',
        conversationId: 7,
      })
    )
  })

  it('renders mixed voice/chat history while keeping learner text literal', async () => {
    mocks.apiFetch.mockImplementation((path: string) => {
      if (path === '/api/chat/conversations') {
        return Promise.resolve(
          jsonResponse([{ id: 7, title: 'Practice', source: 'voice' }])
        )
      }
      if (path === '/api/chat/conversations/7/messages') {
        return Promise.resolve(
          jsonResponse({
            messages: [
              { role: 'assistant', content: 'Hello from voice.' },
              { role: 'user', content: '**Keep my text literal**' },
              { role: 'assistant', content: 'Try **went**.\n\n- I went home.' },
            ],
          })
        )
      }
      return Promise.resolve(jsonResponse([]))
    })
    render(<ChatPage />)

    expect(await screen.findByText('Hello from voice.')).toBeInTheDocument()
    const learner = screen.getByText('**Keep my text literal**')
    expect(learner.querySelector('strong')).toBeNull()
    const word = screen.getByText('went')
    expect(word.tagName).toBe('STRONG')
    fireEvent.pointerUp(word)
    expect(mocks.handleTextSelection).toHaveBeenCalledWith(
      'Try **went**.\n\n- I went home.'
    )
    expect(mocks.audioPlayer).toHaveBeenCalledWith(
      expect.objectContaining({ text: 'Hello from voice.', conversationId: 7 })
    )
  })

  it('shows the toast only after the backend confirms a saved memory', async () => {
    chatEvents = [
      { conversation_id: 7 },
      { token: 'Normal response.' },
      { memory_updated: true },
      { done: true },
    ]
    render(<ChatPage />)

    const input = await screen.findByPlaceholderText('placeholder')
    await waitFor(() => expect(input).not.toBeDisabled())
    fireEvent.change(input, { target: { value: 'Remember this' } })
    fireEvent.click(screen.getByRole('button', { name: 'send' }))

    expect(await screen.findByText('Normal response.')).toBeInTheDocument()
    expect(await screen.findByText('memorySavedToast')).toBeInTheDocument()
  })

  it('keeps the confirmed memory toast when a later stream error arrives', async () => {
    chatEvents = [
      { conversation_id: 7 },
      { memory_updated: true },
      { error: 'Something went wrong.' },
    ]
    render(<ChatPage />)

    const input = await screen.findByPlaceholderText('placeholder')
    await waitFor(() => expect(input).not.toBeDisabled())
    fireEvent.change(input, { target: { value: 'Remember this' } })
    fireEvent.click(screen.getByRole('button', { name: 'send' }))

    expect(await screen.findByText('memorySavedToast')).toBeInTheDocument()
    expect(await screen.findByText(/errorMessage/)).toBeInTheDocument()
  })

  it.each([
    [429, 'Monthly token limit reached (10/10 tokens).', 'quotaExceededTokens'],
    [429, 'Rate limit exceeded: 30 per 1 minute', 'errorMessage'],
    [502, 'Provider unavailable', 'errorMessage'],
  ])(
    'localizes HTTP %i errors instead of showing backend details',
    async (status, detail, label) => {
      mocks.apiFetch.mockImplementation((path: string) =>
        Promise.resolve(
          path === '/api/chat'
            ? new Response(JSON.stringify({ detail }), {
                status,
                headers: { 'Content-Type': 'application/json' },
              })
            : jsonResponse([])
        )
      )
      render(<ChatPage />)

      const input = await screen.findByPlaceholderText('placeholder')
      await waitFor(() => expect(input).not.toBeDisabled())
      fireEvent.change(input, { target: { value: 'Hello' } })
      fireEvent.click(screen.getByRole('button', { name: 'send' }))

      expect(await screen.findByText(new RegExp(label))).toBeInTheDocument()
      expect(screen.queryByText(detail)).toBeNull()
    }
  )
})
