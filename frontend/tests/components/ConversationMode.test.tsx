import {
  act,
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import type { useMicVAD } from '@ricky0123/vad-react'

const mocks = vi.hoisted(() => ({
  options: {} as Parameters<typeof useMicVAD>[0],
  start: vi.fn(),
  pause: vi.fn(),
  getUserMedia: vi.fn(),
  apiFetch: vi.fn(),
  enqueue: vi.fn(),
  cancel: vi.fn(),
  closeAudio: vi.fn(),
  starters: [] as string[],
}))

vi.mock('@ricky0123/vad-react', () => ({
  useMicVAD: (options: Parameters<typeof useMicVAD>[0]) => {
    mocks.options = options
    return {
      loading: false,
      errored: false,
      start: mocks.start,
      pause: mocks.pause,
    }
  },
}))
vi.mock('next-intl', async (importOriginal) => {
  const { createTranslator } =
    await importOriginal<typeof import('next-intl')>()
  const { default: messages } = await import('../../../messages/en.json')
  const practice = createTranslator({
    locale: 'en',
    messages,
    namespace: 'lessonPractice',
  })
  return {
    useLocale: () => 'en',
    useTranslations: () =>
      Object.assign((key: string) => key, {
        raw: () => mocks.starters,
        rich: practice.rich,
      }),
  }
})
vi.mock('next/navigation', () => ({ useRouter: () => ({ push: vi.fn() }) }))
vi.mock('@/lib/api', () => ({ apiFetch: mocks.apiFetch }))
vi.mock('@/lib/audio', async (importOriginal) => ({
  ...(await importOriginal<typeof import('@/lib/audio')>()),
  createAudioQueue: () => ({ enqueue: mocks.enqueue, cancel: mocks.cancel }),
}))
vi.mock('@/components/reviews/ReviewPrompt', () => ({
  ReviewPrompt: () => null,
  getReviewPromptDismissal: () => null,
}))
vi.mock('@/lib/review-prompt-triggers', () => ({
  shouldShowVoiceReviewPrompt: () => false,
}))
vi.mock('@/components/conversation/StatusIndicator', () => ({
  default: ({ userSpeaking }: { userSpeaking: boolean }) => (
    <div data-testid="speaking">{String(userSpeaking)}</div>
  ),
}))

import ConversationMode from '@/components/conversation/ConversationMode'
import { useAuthStore } from '@/store/auth'

class MockWebSocket {
  static OPEN = 1
  static instances: MockWebSocket[] = []
  readyState = 1
  binaryType = ''
  onopen: (() => void) | null = null
  onmessage: ((event: { data: unknown }) => void) | null = null
  onerror: (() => void) | null = null
  onclose: ((event: { code: number; reason: string }) => void) | null = null
  send = vi.fn()
  close = vi.fn(() => {
    this.readyState = 3
  })

  constructor() {
    MockWebSocket.instances.push(this)
  }

  message(message: unknown) {
    this.onmessage?.({ data: JSON.stringify(message) })
  }
}

function microphone() {
  const stop = vi.fn()
  return {
    stream: { getTracks: () => [{ stop }] } as unknown as MediaStream,
    stop,
  }
}

function deferWarmup(ignoreAbort = false) {
  let resolve!: (response: { ok: boolean; status?: number }) => void
  let reject!: (error: Error) => void
  let signal!: AbortSignal
  const response = new Promise((res, rej) => {
    resolve = res
    reject = rej
  })
  mocks.apiFetch.mockImplementation((url: string, options?: RequestInit) => {
    if (url !== '/api/conversation/warmup') {
      return Promise.resolve({ ok: true, json: async () => null })
    }
    signal = options!.signal as AbortSignal
    if (!ignoreAbort) {
      signal.addEventListener('abort', () => reject(signal.reason), {
        once: true,
      })
    }
    return response
  })
  return {
    resolve,
    reject,
    get signal() {
      return signal
    },
  }
}

async function start(label = 'start') {
  const count = MockWebSocket.instances.length
  fireEvent.click(screen.getByRole('button', { name: label }))
  await waitFor(() => expect(MockWebSocket.instances).toHaveLength(count + 1))
  const ws = MockWebSocket.instances[count]
  act(() => ws.onopen?.())
  ws.send.mockClear()
  return ws
}

function speak() {
  mocks.options.onSpeechStart?.()
  mocks.options.onSpeechEnd?.(new Float32Array(24000).fill(0.05))
}

beforeEach(() => {
  vi.clearAllMocks()
  MockWebSocket.instances = []
  mocks.starters = []
  mocks.getUserMedia.mockReset().mockResolvedValue(microphone().stream)
  mocks.start.mockImplementation(async () => {
    await mocks.options.getStream?.()
  })
  mocks.pause.mockResolvedValue(undefined)
  mocks.closeAudio.mockResolvedValue(undefined)
  mocks.enqueue.mockResolvedValue(undefined)
  mocks.apiFetch.mockResolvedValue({ ok: true, json: async () => null })
  vi.stubGlobal('WebSocket', MockWebSocket)
  vi.stubGlobal(
    'AudioContext',
    class {
      state = 'running'
      close = mocks.closeAudio
    }
  )
  vi.stubGlobal('navigator', {
    mediaDevices: { getUserMedia: mocks.getUserMedia },
  })
  Element.prototype.scrollIntoView = vi.fn()
  useAuthStore.setState({ accessToken: 'token', user: null })
})

afterEach(() => {
  cleanup()
  vi.useRealTimers()
  vi.restoreAllMocks()
  vi.unstubAllGlobals()
})

describe('ConversationMode session lifecycle', () => {
  it.each(['replace-session', 'unmount'])(
    'ignores a delayed trial profile after %s',
    async (action) => {
      let finish!: (body: unknown) => void
      mocks.apiFetch.mockImplementation(async (url: string) =>
        url === '/api/auth/me'
          ? {
              ok: true,
              json: () =>
                new Promise((resolve) => {
                  finish = resolve
                }),
            }
          : { ok: true, json: async () => null }
      )
      const { unmount } = render(<ConversationMode trialMode />)
      await start()
      fireEvent.click(screen.getByRole('button', { name: 'stop' }))
      await waitFor(() => expect(finish).toBeDefined())
      if (action === 'unmount') unmount()
      else act(() => useAuthStore.getState().startSession('new-session'))
      await act(async () =>
        finish({ id: 1, username: 'old-user', role: 'user' })
      )
      expect(useAuthStore.getState().user).toBeNull()
      if (action === 'unmount') {
        const options = mocks.apiFetch.mock.calls.find(
          ([url]) => url === '/api/auth/me'
        )![1]
        expect(options.signal.aborted).toBe(true)
      }
    }
  )

  it.each(['de-DE', 'ja-JP'])(
    'starts a suggested topic without overriding %s with English',
    async (targetLanguage) => {
      mocks.starters = ['Travel']
      render(<ConversationMode targetLanguage={targetLanguage} />)
      fireEvent.click(screen.getByRole('button', { name: 'Travel' }))
      await waitFor(() => expect(MockWebSocket.instances).toHaveLength(1))
      const ws = MockWebSocket.instances[0]
      act(() => ws.onopen?.())
      expect(JSON.parse(ws.send.mock.calls[0][0])).toEqual({
        type: 'auth',
        token: 'token',
        target_language: targetLanguage,
        context: [
          {
            role: 'user',
            content: "I'd like to practise by talking about Travel.",
          },
        ],
      })
    }
  )

  it.each([undefined, 7])(
    'waits through a 30-second cold start for lesson %s',
    async (lessonId) => {
      vi.useFakeTimers()
      const pending = deferWarmup()
      render(<ConversationMode lessonId={lessonId} />)
      await act(async () => {
        fireEvent.click(screen.getByRole('button', { name: 'start' }))
      })
      await act(async () => {
        await vi.advanceTimersByTimeAsync(30_000)
      })
      expect(pending.signal.aborted).toBe(false)
      expect(screen.queryByText(/errorConnection/)).toBeNull()
      expect(MockWebSocket.instances).toHaveLength(0)

      await act(async () => {
        pending.resolve({ ok: true })
      })
      expect(MockWebSocket.instances).toHaveLength(1)
      await act(async () => {
        await vi.advanceTimersByTimeAsync(80_000)
      })
      expect(pending.signal.aborted).toBe(false)
      expect(screen.queryByText(/errorConnection/)).toBeNull()
      expect(MockWebSocket.instances[0].close).not.toHaveBeenCalled()
    }
  )

  it('aborts at 75 seconds, releases the microphone, and allows a fresh attempt', async () => {
    vi.useFakeTimers()
    const log = vi.spyOn(console, 'error').mockImplementation(() => {})
    const mic = microphone()
    mocks.getUserMedia.mockResolvedValueOnce(mic.stream)
    const pending = deferWarmup()
    render(<ConversationMode />)
    await act(async () => {
      fireEvent.click(screen.getByRole('button', { name: 'start' }))
    })
    await act(async () => {
      await vi.advanceTimersByTimeAsync(74_999)
    })
    expect(pending.signal.aborted).toBe(false)
    await act(async () => {
      await vi.advanceTimersByTimeAsync(1)
    })
    expect(pending.signal.aborted).toBe(true)
    expect(mic.stop).toHaveBeenCalledTimes(1)
    expect(mocks.closeAudio).toHaveBeenCalledTimes(1)
    expect(screen.getByText('✕ errorConnection')).toBeInTheDocument()
    expect(log).toHaveBeenCalledWith(expect.stringContaining('warmup timeout'))
    expect(MockWebSocket.instances).toHaveLength(0)

    mocks.apiFetch.mockResolvedValue({ ok: true, json: async () => null })
    await act(async () => {
      fireEvent.click(screen.getByRole('button', { name: 'startNew' }))
    })
    expect(MockWebSocket.instances).toHaveLength(1)
    expect(screen.queryByText(/errorConnection/)).toBeNull()
  })

  it.each(['stop', 'unmount'])(
    'cancels warming on %s and ignores a late response',
    async (action) => {
      vi.useFakeTimers()
      const log = vi.spyOn(console, 'error').mockImplementation(() => {})
      const mic = microphone()
      mocks.getUserMedia.mockResolvedValueOnce(mic.stream)
      // Simulate a transport that delivers a response despite cancellation.
      const pending = deferWarmup(true)
      const view = render(<ConversationMode />)
      await act(async () => {
        fireEvent.click(screen.getByRole('button', { name: 'start' }))
      })
      const abort = vi.spyOn(AbortController.prototype, 'abort')
      if (action === 'stop') {
        await act(async () => {
          fireEvent.click(screen.getByRole('button', { name: 'stop' }))
        })
        mocks.apiFetch.mockResolvedValue({ ok: true, json: async () => null })
        await act(async () => {
          fireEvent.click(screen.getByRole('button', { name: 'startNew' }))
        })
      } else {
        view.unmount()
      }
      expect(pending.signal.aborted).toBe(true)
      expect(mic.stop).toHaveBeenCalledTimes(1)
      await act(async () => {
        await vi.advanceTimersByTimeAsync(80_000)
      })
      expect(abort).toHaveBeenCalledTimes(1)
      await act(async () => {
        pending.resolve({ ok: true })
      })
      expect(MockWebSocket.instances).toHaveLength(action === 'stop' ? 1 : 0)
      if (action === 'stop') {
        expect(MockWebSocket.instances[0].close).not.toHaveBeenCalled()
      }
      expect(log).not.toHaveBeenCalled()
    }
  )

  it.each(['network', 402, 503])(
    'reports %s warmup failures without opening a WebSocket',
    async (failure) => {
      vi.useFakeTimers()
      const log = vi.spyOn(console, 'error').mockImplementation(() => {})
      const pending = deferWarmup()
      render(<ConversationMode />)
      await act(async () => {
        fireEvent.click(screen.getByRole('button', { name: 'start' }))
      })
      await act(async () => {
        if (failure === 'network')
          pending.reject(new TypeError('Failed to fetch'))
        else pending.resolve({ ok: false, status: failure as number })
      })
      expect(screen.getByText('✕ errorConnection')).toBeInTheDocument()
      expect(log).toHaveBeenCalledWith(
        expect.stringContaining(
          failure === 'network' ? 'Failed to fetch' : `"status":${failure}`
        )
      )
      await act(async () => {
        await vi.advanceTimersByTimeAsync(80_000)
      })
      expect(log).toHaveBeenCalledTimes(1)
      expect(MockWebSocket.instances).toHaveLength(0)
    }
  )

  it('sends the lesson reference through the existing handshake and lets the user end practice', async () => {
    render(
      <ConversationMode
        lessonId={7}
        lessonTitle="Past experiences"
        targetLanguage="fr-FR"
      />
    )
    const topic = screen.getByText('Past experiences')
    expect(topic).toHaveAttribute('lang', 'fr-FR')
    expect(topic.parentElement).toHaveAttribute('lang', 'en')
    expect(topic.parentElement).toHaveTextContent('Practice: Past experiences')
    fireEvent.click(screen.getByRole('button', { name: 'start' }))
    await waitFor(() => expect(MockWebSocket.instances).toHaveLength(1))
    const ws = MockWebSocket.instances[0]
    act(() => ws.onopen?.())
    expect(JSON.parse(ws.send.mock.calls[0][0])).toEqual({
      type: 'auth',
      token: 'token',
      lesson_id: 7,
      target_language: 'fr-FR',
    })
    expect(mocks.apiFetch).toHaveBeenCalledWith(
      '/api/conversation/warmup',
      expect.any(Object)
    )
    expect(screen.queryByText('startersHint')).toBeNull()
    act(() =>
      ws.message({
        type: 'transcript',
        role: 'assistant',
        final: true,
        text: 'We have practised the main points. You can finish or keep practising.',
      })
    )
    expect(ws.close).not.toHaveBeenCalled()
    expect(screen.getByRole('button', { name: 'stop' })).toBeInTheDocument()
    fireEvent.click(screen.getByRole('button', { name: 'stop' }))
    await waitFor(() => expect(ws.close).toHaveBeenCalledTimes(1))
  })

  it('does not add lesson context to ordinary voice sessions', async () => {
    render(<ConversationMode />)
    fireEvent.click(screen.getByRole('button', { name: 'start' }))
    await waitFor(() => expect(MockWebSocket.instances).toHaveLength(1))
    const ws = MockWebSocket.instances[0]
    act(() => ws.onopen?.())
    expect(JSON.parse(ws.send.mock.calls[0][0])).toEqual({
      type: 'auth',
      token: 'token',
    })
  })

  it('retries denied permission without poisoning VAD', async () => {
    mocks.getUserMedia.mockRejectedValueOnce(
      new DOMException('Denied', 'NotAllowedError')
    )
    render(<ConversationMode />)
    fireEvent.click(screen.getByRole('button', { name: 'start' }))
    await screen.findByText(/errorMic/)
    expect(mocks.start).not.toHaveBeenCalled()
    await start('startNew')
    expect(mocks.start).toHaveBeenCalledTimes(1)
  })

  it('stops a microphone granted after unmount without starting VAD or WS', async () => {
    const mic = microphone()
    let grant!: (stream: MediaStream) => void
    mocks.getUserMedia.mockReturnValue(
      new Promise<MediaStream>((resolve) => {
        grant = resolve
      })
    )
    const view = render(<ConversationMode />)
    fireEvent.click(screen.getByRole('button', { name: 'start' }))
    view.unmount()
    await act(async () => {
      grant(mic.stream)
    })
    expect(mic.stop).toHaveBeenCalledTimes(1)
    expect(mocks.start).not.toHaveBeenCalled()
    expect(MockWebSocket.instances).toHaveLength(0)
  })

  it.each(['json', 'onerror', 'onclose'])(
    'cleans up %s once and ignores obsolete callbacks after restart',
    async (kind) => {
      const mic = microphone()
      mocks.getUserMedia.mockResolvedValueOnce(mic.stream)
      render(<ConversationMode />)
      const ws = await start()
      const oldOpen = ws.onopen!
      const oldMessage = ws.onmessage!
      const oldError = ws.onerror!
      const oldClose = ws.onclose!
      act(() => {
        if (kind === 'json') ws.message({ type: 'error', code: 'unauthorized' })
        else if (kind === 'onerror') oldError()
        else oldClose({ code: 1006, reason: '' })
        oldError()
        oldClose({ code: 1006, reason: '' })
      })
      await waitFor(() => expect(mocks.pause).toHaveBeenCalledTimes(1))
      expect(mic.stop).toHaveBeenCalledTimes(1)
      expect(mocks.closeAudio).toHaveBeenCalledTimes(1)
      expect(ws.close).toHaveBeenCalledTimes(1)
      const current = await start('startNew')
      act(() => {
        oldOpen()
        oldMessage({
          data: JSON.stringify({ type: 'session_end', reason: 'inactivity' }),
        })
        oldError()
        oldClose({ code: 1006, reason: '' })
      })
      expect(current.close).not.toHaveBeenCalled()
      expect(screen.getByRole('button', { name: 'stop' })).toBeDefined()
    }
  )

  it.each([
    { type: 'status', value: 'listening' },
    { type: 'turn_complete' },
    ...['stt_failed', 'llm_failed', 'tts_failed'].map((code) => ({
      type: 'error',
      code,
    })),
  ])(
    'blocks immediately and releases on $type $value $code',
    async (outcome) => {
      render(<ConversationMode />)
      const ws = await start()
      act(() => {
        speak()
        speak()
      })
      expect(ws.send).toHaveBeenCalledTimes(1)
      act(() => ws.message({ type: 'status', value: 'transcribing' }))
      act(() => speak())
      expect(ws.send).toHaveBeenCalledTimes(1)
      act(() => ws.message(outcome))
      expect(screen.getByRole('button', { name: 'stop' })).toBeDefined()
      act(() => speak())
      expect(ws.send).toHaveBeenCalledTimes(2)
      expect(ws.close).not.toHaveBeenCalled()
    }
  )

  it.each([
    ['stt_failed', 'errorTranscription'],
    ['llm_failed', 'errorResponse'],
    ['tts_failed', 'errorSpeech'],
    ['auth_failed', 'errorUnauthorized'],
    ['services_disabled', 'errorServicesDisabled'],
    ['quota_exceeded_sessions', 'quotaExceededSessions'],
    ['quota_exceeded_time', 'quotaExceededTime'],
    ['quota_exceeded_tokens', 'quotaExceededTokens'],
    ['no_active_plan', 'noActivePlan'],
    ['lesson_practice_unavailable', 'unavailable'],
    ['unknown_server_error', 'errorMessage'],
  ])(
    'localizes %s without displaying the backend message',
    async (code, key) => {
      render(<ConversationMode />)
      const ws = await start()

      act(() =>
        ws.message({
          type: 'error',
          code,
          message: 'Untranslated backend failure',
        })
      )

      expect(screen.getByText(new RegExp(key))).toBeInTheDocument()
      expect(screen.queryByText(/Untranslated backend failure/)).toBeNull()
    }
  )

  it.each(['onerror', 'onclose'])(
    'localizes %s without displaying transport diagnostics',
    async (event) => {
      render(<ConversationMode />)
      const ws = await start()

      act(() => {
        if (event === 'onerror') ws.onerror?.()
        else ws.onclose?.({ code: 1011, reason: 'Untranslated close reason' })
      })

      expect(screen.getByText('✕ errorConnection')).toBeInTheDocument()
      expect(
        screen.queryByText(/Untranslated close reason|\[onerror|\[code/)
      ).toBeNull()
    }
  )

  it('clears visual speech and discards the unfinished segment on misfire', async () => {
    render(<ConversationMode />)
    const ws = await start()
    act(() => {
      mocks.options.onSpeechStart?.()
    })
    expect(screen.getByTestId('speaking').textContent).toBe('true')
    act(() => {
      mocks.options.onVADMisfire?.()
    })
    expect(screen.getByTestId('speaking').textContent).toBe('false')
    act(() => {
      mocks.options.onSpeechEnd?.(new Float32Array(24000).fill(0.05))
    })
    expect(ws.send).not.toHaveBeenCalled()
  })

  it('ignores a Blob decoded after a new session has started', async () => {
    render(<ConversationMode />)
    const ws = await start()
    let decode!: (buffer: ArrayBuffer) => void
    const blob = new Blob()
    blob.arrayBuffer = vi.fn(
      () =>
        new Promise<ArrayBuffer>((resolve) => {
          decode = resolve
        })
    )
    act(() => ws.onmessage?.({ data: blob }))
    act(() => ws.onerror?.())
    const current = await start('startNew')
    await act(async () => {
      decode(new ArrayBuffer(8))
    })
    expect(mocks.enqueue).not.toHaveBeenCalled()
    expect(current.close).not.toHaveBeenCalled()
    act(() => speak())
    expect(current.send).toHaveBeenCalledTimes(1)
  })

  it('releases resources after a WAV send throws and allows restart', async () => {
    render(<ConversationMode />)
    const ws = await start()
    ws.send.mockImplementationOnce(() => {
      throw new Error('Transport closed')
    })
    act(() => speak())
    expect(ws.close).toHaveBeenCalledTimes(1)
    const current = await start('startNew')
    act(() => speak())
    expect(current.send).toHaveBeenCalledTimes(1)
  })
})
