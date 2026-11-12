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
import {
  defaultFrameProcessorOptions,
  FrameProcessor,
  type FrameProcessorEvent,
} from '@ricky0123/vad-web/dist/frame-processor'
import { Message } from '@ricky0123/vad-web/dist/messages'

const mocks = vi.hoisted(() => ({
  options: {} as Parameters<typeof useMicVAD>[0],
  start: vi.fn(),
  pause: vi.fn(),
  getUserMedia: vi.fn(),
  apiFetch: vi.fn(),
  enqueue: vi.fn(),
  cancel: vi.fn(),
  closeAudio: vi.fn(),
  onAudioIdle: null as (() => void) | null,
  starters: [] as string[],
  push: vi.fn(),
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
      Object.assign(
        (key: string, values?: { seconds?: number }) => {
          if (key === 'warningTimeout') return `${key}:${values?.seconds}`
          return key
        },
        {
          raw: () => mocks.starters,
          rich: practice.rich,
        }
      ),
  }
})
vi.mock('next/navigation', () => ({ useRouter: () => ({ push: mocks.push }) }))
vi.mock('@/lib/api', () => ({ apiFetch: mocks.apiFetch }))
vi.mock('@/lib/audio', async (importOriginal) => ({
  ...(await importOriginal<typeof import('@/lib/audio')>()),
  createAudioQueue: (_ctx: AudioContext, onIdle?: () => void) => {
    mocks.onAudioIdle = onIdle ?? null
    return { enqueue: mocks.enqueue, cancel: mocks.cancel }
  },
}))
vi.mock('@/components/reviews/ReviewPrompt', () => ({
  ReviewPrompt: () => null,
  getReviewPromptDismissal: () => null,
}))
vi.mock('@/lib/review-prompt-triggers', () => ({
  shouldShowVoiceReviewPrompt: () => false,
}))
vi.mock('@/components/conversation/StatusIndicator', async (importOriginal) => {
  const { default: StatusIndicator } =
    await importOriginal<
      typeof import('@/components/conversation/StatusIndicator')
    >()
  return {
    default: (props: Parameters<typeof StatusIndicator>[0]) => (
      <>
        <div data-testid="speaking">{String(props.userSpeaking)}</div>
        <StatusIndicator {...props} />
      </>
    ),
  }
})

import ConversationMode from '@/components/conversation/ConversationMode'
import { useAuthStore } from '@/store/auth'
import { useConfigStore } from '@/store/config'
import { mapUser } from '@/lib/mappers'
import { float32ToWav } from '@/lib/audio'

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

function deferred<T>() {
  let resolve!: (value: T) => void
  let reject!: (error: Error) => void
  const promise = new Promise<T>((done, fail) => {
    resolve = done
    reject = fail
  })
  return { promise, resolve, reject }
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

function speak(audio = new Float32Array(24000).fill(0.05)) {
  mocks.options.onFrameProcessed?.({ isSpeech: 0.99, notSpeech: 0.01 }, audio)
  mocks.options.onSpeechStart?.()
  mocks.options.onSpeechEnd?.(audio)
}

beforeEach(() => {
  useConfigStore.setState(
    { ...useConfigStore.getInitialState(), loaded: true },
    true
  )
  localStorage.clear()
  vi.clearAllMocks()
  MockWebSocket.instances = []
  mocks.starters = []
  mocks.onAudioIdle = null
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
  describe('authentication ownership', () => {
    const originalUser = mapUser({
      id: 1,
      username: 'voice-test',
      display_name: 'Voice Test',
      role: 'user',
    })

    beforeEach(() => useAuthStore.setState({ user: originalUser }))

    function replaceIdentity(change: 'session' | 'user' | 'logout') {
      if (change === 'session') {
        useAuthStore.getState().startSession('next-token')
        useAuthStore.getState().setUser(originalUser)
      } else if (change === 'user') {
        useAuthStore.getState().setUser({ ...originalUser, id: 2 })
      } else {
        useAuthStore.getState().logout()
      }
    }

    describe.each(['resume', 'microphone', 'vad', 'config', 'warmup'] as const)(
      'pending %s',
      (stage) => {
        it.each(['session', 'user'] as const)(
          'invalidates immediately on %s replacement without disturbing the next attempt',
          async (change) => {
            const oldMic = microphone()
            const nextMic = microphone()
            const pending = deferred<void>()
            const permission = deferred<MediaStream>()
            const response = deferred<Response>()
            const configFetch = vi.fn().mockReturnValue(response.promise)
            let warmupSignal: AbortSignal | undefined
            mocks.getUserMedia.mockResolvedValue(nextMic.stream)
            if (stage !== 'resume')
              mocks.getUserMedia.mockResolvedValueOnce(oldMic.stream)
            if (stage === 'resume') {
              const resume = vi.fn().mockResolvedValue(undefined)
              resume.mockReturnValueOnce(pending.promise)
              vi.stubGlobal(
                'AudioContext',
                class {
                  state = 'suspended'
                  close = mocks.closeAudio
                  resume = resume
                }
              )
            }
            if (stage === 'microphone') {
              mocks.getUserMedia
                .mockReset()
                .mockResolvedValue(nextMic.stream)
                .mockReturnValueOnce(permission.promise)
            }
            if (stage === 'vad')
              mocks.start.mockReturnValueOnce(pending.promise)
            if (stage === 'config') {
              useConfigStore.setState({ loaded: false })
              vi.stubGlobal('fetch', configFetch)
            }
            if (stage === 'warmup') {
              mocks.apiFetch.mockImplementation((url, options) => {
                if (url === '/api/conversation/warmup') {
                  warmupSignal = options.signal
                  return response.promise
                }
                return Promise.resolve({ ok: true, json: async () => null })
              })
            }
            render(<ConversationMode />)
            await act(async () => {
              fireEvent.click(screen.getByRole('button', { name: 'start' }))
            })
            expect(MockWebSocket.instances).toHaveLength(0)
            if (stage === 'config')
              expect(configFetch).toHaveBeenCalledTimes(1)
            if (stage === 'warmup') expect(warmupSignal).toBeDefined()
            if (stage === 'vad') expect(mocks.start).toHaveBeenCalledTimes(1)

            act(() => {
              replaceIdentity(change)
              // Resource invalidation is synchronous at the auth-store boundary.
              expect(mocks.closeAudio).toHaveBeenCalledTimes(1)
              if (stage === 'vad' || stage === 'config' || stage === 'warmup')
                expect(oldMic.stop).toHaveBeenCalledTimes(1)
              if (warmupSignal) expect(warmupSignal.aborted).toBe(true)
            })
            mocks.apiFetch.mockResolvedValue({
              ok: true,
              json: async () => null,
            })
            await act(async () => {
              fireEvent.click(screen.getByRole('button', { name: 'start' }))
            })
            // VAD operations remain serialized; both config consumers share one load.
            expect(MockWebSocket.instances).toHaveLength(
              stage === 'vad' || stage === 'config' ? 0 : 1
            )
            await act(async () => {
              pending.resolve()
              permission.resolve(oldMic.stream)
              response.resolve(
                new Response(JSON.stringify({ tts_provider: 'gemini' }))
              )
            })
            await waitFor(() =>
              expect(MockWebSocket.instances).toHaveLength(1)
            )
            const current = MockWebSocket.instances[0]
            act(() => current.onopen?.())
            expect(JSON.parse(current.send.mock.calls[0][0]).token).toBe(
              change === 'session' ? 'next-token' : 'token'
            )
            expect(mocks.closeAudio).toHaveBeenCalledTimes(1)
            expect(nextMic.stop).not.toHaveBeenCalled()
            expect(current.close).not.toHaveBeenCalled()
            expect(oldMic.stop).toHaveBeenCalledTimes(
              stage === 'resume' ? 0 : 1
            )
            expect(screen.queryByText(/errorConnection|errorMic/)).toBeNull()
            if (stage === 'config') {
              expect(configFetch).toHaveBeenCalledTimes(1)
              expect(configFetch.mock.calls[0][1].signal.aborted).toBe(false)
            }
            if (stage === 'vad') {
              expect(mocks.pause).toHaveBeenCalledTimes(1)
              expect(mocks.start).toHaveBeenCalledTimes(2)
              expect(mocks.pause.mock.invocationCallOrder[0]).toBeLessThan(
                mocks.start.mock.invocationCallOrder[1]
              )
            }
          }
        )
      }
    )

    it.each(['resume', 'microphone', 'vad', 'warmup'] as const)(
      'ignores an obsolete %s rejection after a replacement attempt starts',
      async (stage) => {
        const pending = deferred<void>()
        const nextMic = microphone()
        mocks.getUserMedia.mockResolvedValue(nextMic.stream)
        if (stage === 'vad' || stage === 'warmup')
          mocks.getUserMedia.mockResolvedValueOnce(microphone().stream)
        if (stage === 'resume') {
          const resume = vi.fn().mockResolvedValue(undefined)
          resume.mockReturnValueOnce(pending.promise)
          vi.stubGlobal(
            'AudioContext',
            class {
              state = 'suspended'
              close = mocks.closeAudio
              resume = resume
            }
          )
        }
        if (stage === 'microphone')
          mocks.getUserMedia.mockReturnValueOnce(pending.promise)
        if (stage === 'vad') mocks.start.mockReturnValueOnce(pending.promise)
        if (stage === 'warmup') {
          mocks.apiFetch.mockImplementation((url) =>
            url === '/api/conversation/warmup'
              ? pending.promise
              : Promise.resolve({ ok: true, json: async () => null })
          )
        }
        render(<ConversationMode />)
        await act(async () => {
          fireEvent.click(screen.getByRole('button', { name: 'start' }))
        })
        act(() => replaceIdentity('session'))
        mocks.apiFetch.mockResolvedValue({ ok: true, json: async () => null })
        await act(async () => {
          fireEvent.click(screen.getByRole('button', { name: 'start' }))
        })
        await act(async () => pending.reject(new Error('Obsolete failure')))
        await waitFor(() => expect(MockWebSocket.instances).toHaveLength(1))
        expect(MockWebSocket.instances[0].close).not.toHaveBeenCalled()
        expect(mocks.closeAudio).toHaveBeenCalledTimes(1)
        expect(nextMic.stop).not.toHaveBeenCalled()
        expect(screen.queryByText(/errorConnection|errorMic/)).toBeNull()
      }
    )

    describe.each(['connecting', 'live'] as const)('%s WebSocket', (stage) => {
      it.each(['session', 'user', 'logout'] as const)(
        'closes on %s replacement and ignores stale socket/audio callbacks',
        async (change) => {
          const mic = microphone()
          mocks.getUserMedia.mockResolvedValueOnce(mic.stream)
          render(<ConversationMode />)
          fireEvent.click(screen.getByRole('button', { name: 'start' }))
          await waitFor(() => expect(MockWebSocket.instances).toHaveLength(1))
          const old = MockWebSocket.instances[0]
          const oldOpen = old.onopen!
          const oldMessage = old.onmessage!
          const oldError = old.onerror!
          const oldClose = old.onclose!
          const oldIdle = mocks.onAudioIdle!
          const decoded = deferred<ArrayBuffer>()
          const playback = deferred<void>()
          if (stage === 'live') {
            act(() => oldOpen())
            const blob = new Blob()
            blob.arrayBuffer = vi.fn(() => decoded.promise)
            mocks.enqueue.mockReturnValueOnce(playback.promise)
            act(() => {
              old.message({
                type: 'transcript',
                role: 'assistant',
                final: true,
                text: 'Private previous transcript',
              })
              oldMessage({ data: blob })
              oldMessage({ data: new ArrayBuffer(8) })
            })
          } else {
            old.readyState = 0
          }
          act(() => {
            replaceIdentity(change)
            expect(old.close).toHaveBeenCalledTimes(1)
            expect(mic.stop).toHaveBeenCalledTimes(1)
            expect(mocks.cancel).toHaveBeenCalledTimes(1)
            expect(mocks.closeAudio).toHaveBeenCalledTimes(1)
          })
          expect(old.onopen).toBeNull()
          expect(old.onmessage).toBeNull()
          expect(old.onerror).toBeNull()
          expect(old.onclose).toBeNull()
          expect(screen.queryByText('Private previous transcript')).toBeNull()
          const oldSendCount = old.send.mock.calls.length
          act(() => {
            speak()
            mocks.options.onVADMisfire?.()
          })
          expect(old.send).toHaveBeenCalledTimes(oldSendCount)
          expect(screen.getByTestId('speaking')).toHaveTextContent('false')
          if (change === 'logout') {
            act(() => {
              useAuthStore.getState().startSession('next-token')
              useAuthStore.getState().setUser(originalUser)
            })
          }
          const current = await start()
          mocks.enqueue.mockClear()
          act(() => current.onmessage?.({ data: new ArrayBuffer(8) }))
          expect(screen.getByText('statusSpeaking')).toBeInTheDocument()
          await act(async () => {
            oldOpen()
            oldMessage({ data: new ArrayBuffer(8) })
            oldMessage({
              data: JSON.stringify({
                type: 'session_end',
                reason: 'inactivity',
              }),
            })
            oldError()
            oldClose({ code: 1006, reason: '' })
            oldIdle()
            if (stage === 'live') {
              decoded.resolve(new ArrayBuffer(8))
              playback.reject(new Error('Obsolete playback'))
            }
          })
          expect(old.send).toHaveBeenCalledTimes(oldSendCount)
          expect(mocks.enqueue).toHaveBeenCalledTimes(1)
          expect(current.close).not.toHaveBeenCalled()
          expect(mocks.closeAudio).toHaveBeenCalledTimes(1)
          expect(screen.getByText('statusSpeaking')).toBeInTheDocument()
          expect(screen.queryByText(/errorConnection|sessionEnded/)).toBeNull()
        }
      )
    })

    it('does not auto-start the previous chat context after authentication changes', async () => {
      const mic = microphone()
      const permission = deferred<MediaStream>()
      mocks.getUserMedia.mockReturnValueOnce(permission.promise)
      render(
        <ConversationMode
          autoStart
          initialContext={[{ role: 'user', content: 'Previous account context' }]}
        />
      )
      await waitFor(() => expect(mocks.getUserMedia).toHaveBeenCalledTimes(1))
      act(() => replaceIdentity('session'))
      await act(async () => permission.resolve(mic.stream))
      expect(mic.stop).toHaveBeenCalledTimes(1)
      expect(mocks.getUserMedia).toHaveBeenCalledTimes(1)
      expect(mocks.start).not.toHaveBeenCalled()
      expect(MockWebSocket.instances).toHaveLength(0)
      expect(screen.getByRole('button', { name: 'start' })).toBeEnabled()
    })

    it('preserves pending startup and live playback during token rotation and same-user updates', async () => {
      const mic = microphone()
      mocks.getUserMedia.mockResolvedValueOnce(mic.stream)
      const pending = deferWarmup()
      render(<ConversationMode />)
      await act(async () => {
        fireEvent.click(screen.getByRole('button', { name: 'start' }))
      })
      act(() => {
        useAuthStore.getState().setTokens('rotated-token')
        useAuthStore.getState().setUser({
          ...originalUser,
          displayName: 'Updated',
        })
      })
      expect(pending.signal.aborted).toBe(false)
      await act(async () => pending.resolve({ ok: true }))
      const ws = MockWebSocket.instances[0]
      act(() => ws.onopen?.())
      expect(JSON.parse(ws.send.mock.calls[0][0]).token).toBe('rotated-token')
      act(() => ws.onmessage?.({ data: new ArrayBuffer(8) }))
      act(() => {
        useAuthStore.getState().setTokens('rotated-again')
        useAuthStore.getState().setUser({
          ...originalUser,
          displayName: 'Again',
        })
      })
      expect(screen.getByText('statusSpeaking')).toBeInTheDocument()
      expect(ws.close).not.toHaveBeenCalled()
      expect(mic.stop).not.toHaveBeenCalled()
      expect(mocks.cancel).not.toHaveBeenCalled()
      expect(mocks.closeAudio).not.toHaveBeenCalled()
    })
  })

  it('resolves delayed provider configuration before opening the trial WebSocket', async () => {
    useConfigStore.setState({ loaded: false, ttsProvider: 'local' })
    localStorage.setItem('tts_voice', 'coral')
    localStorage.setItem('gemini_tts_voice', 'male')
    let finish!: (response: Response) => void
    vi.stubGlobal(
      'fetch',
      vi.fn().mockReturnValueOnce(
        new Promise((resolve) => {
          finish = resolve
        })
      )
    )
    render(<ConversationMode trialMode voiceTrialToken="trial-token" />)
    fireEvent.click(screen.getByRole('button', { name: 'start' }))
    await waitFor(() =>
      expect(fetch).toHaveBeenCalledWith('/api/config', {
        signal: expect.any(AbortSignal),
      })
    )
    expect(MockWebSocket.instances).toHaveLength(0)
    expect(
      mocks.apiFetch.mock.calls.some(
        ([url]) => url === '/api/conversation/warmup'
      )
    ).toBe(false)
    await act(async () =>
      finish(new Response(JSON.stringify({ tts_provider: 'gemini' })))
    )
    await waitFor(() => expect(MockWebSocket.instances).toHaveLength(1))
    const ws = MockWebSocket.instances[0]
    act(() => ws.onopen?.())
    expect(JSON.parse(ws.send.mock.calls[0][0])).toEqual({
      type: 'auth',
      token: 'token',
      voice: 'male',
      voice_trial_token: 'trial-token',
    })
  })

  it.each(['success', 'timeout'] as const)(
    'preserves the full warmup budget after delayed configuration (%s)',
    async (outcome) => {
      vi.useFakeTimers()
      useConfigStore.setState({ loaded: false })
      localStorage.setItem('gemini_tts_voice', 'male')
      const config = deferred<Response>()
      vi.stubGlobal('fetch', vi.fn().mockReturnValue(config.promise))
      const warmup = deferWarmup()
      render(<ConversationMode />)
      await act(async () =>
        fireEvent.click(screen.getByRole('button', { name: 'start' }))
      )
      expect(fetch).toHaveBeenCalledTimes(1)
      await act(async () => vi.advanceTimersByTimeAsync(18_000))
      await act(async () =>
        config.resolve(new Response(JSON.stringify({ tts_provider: 'gemini' })))
      )
      expect(warmup.signal).toBeDefined()
      await act(async () => vi.advanceTimersByTimeAsync(58_000))
      expect(warmup.signal.aborted).toBe(false)
      expect(screen.queryByText(/errorConnection/)).not.toBeInTheDocument()
      expect(MockWebSocket.instances).toHaveLength(0)

      if (outcome === 'success') {
        await act(async () => warmup.resolve({ ok: true }))
        expect(MockWebSocket.instances).toHaveLength(1)
        const ws = MockWebSocket.instances[0]
        act(() => ws.onopen?.())
        expect(JSON.parse(ws.send.mock.calls[0][0])).toMatchObject({
          voice: 'male',
        })
      } else {
        await act(async () => vi.advanceTimersByTimeAsync(17_000))
        expect(warmup.signal.aborted).toBe(true)
        expect(screen.getByText(/errorConnection/)).toBeVisible()
        expect(MockWebSocket.instances).toHaveLength(0)
      }
    }
  )

  it.each(['unmount', 'timeout', 'failure'])(
    'does not open a WebSocket after config %s',
    async (outcome) => {
      useConfigStore.setState({ loaded: false })
      if (outcome === 'timeout') vi.useFakeTimers()
      let finish!: (response: Response) => void
      vi.stubGlobal(
        'fetch',
        vi.fn().mockReturnValueOnce(
          new Promise((resolve) => {
            finish = resolve
          })
        )
      )
      const { unmount } = render(<ConversationMode />)
      await act(async () =>
        fireEvent.click(screen.getByRole('button', { name: 'start' }))
      )
      expect(fetch).toHaveBeenCalledTimes(1)
      if (outcome === 'unmount') unmount()
      if (outcome === 'timeout') {
        await act(async () => vi.advanceTimersByTimeAsync(75_000))
      }
      await act(async () =>
        finish(
          outcome === 'failure'
            ? new Response('', { status: 503 })
            : new Response(JSON.stringify({ tts_provider: 'gemini' }))
        )
      )
      expect(MockWebSocket.instances).toHaveLength(0)
      expect(
        mocks.apiFetch.mock.calls.some(
          ([url]) => url === '/api/conversation/warmup'
        )
      ).toBe(false)
      if (outcome !== 'unmount')
        expect(screen.getByText(/errorConnection/)).toBeVisible()
    }
  )
  it.each([
    ['gemini', 'male', false],
    ['gemini', 'male', true],
    ['openai', 'coral', false],
    ['openai', 'coral', true],
  ] as const)(
    'authenticates %s with voice %s (trial: %s) and accepts WAV frames',
    async (provider, voice, trial) => {
      useConfigStore.setState({ ttsProvider: provider })
      localStorage.setItem('tts_voice', 'coral')
      localStorage.setItem('gemini_tts_voice', 'male')
      render(
        <ConversationMode
          targetLanguage="fr-FR"
          voiceTrialToken={trial ? 'assessment-trial' : undefined}
          trialMode={trial}
        />
      )
      fireEvent.click(screen.getByRole('button', { name: 'start' }))
      await waitFor(() => expect(MockWebSocket.instances).toHaveLength(1))
      const ws = MockWebSocket.instances[0]
      act(() => ws.onopen?.())

      expect(JSON.parse(ws.send.mock.calls[0][0])).toEqual({
        type: 'auth',
        token: 'token',
        voice,
        target_language: 'fr-FR',
        ...(trial ? { voice_trial_token: 'assessment-trial' } : {}),
      })
      const wav = float32ToWav(new Float32Array([0.5]), 24000)
      act(() => ws.onmessage?.({ data: wav }))
      expect(mocks.enqueue).toHaveBeenCalledWith(wav)
    }
  )

  it.each(['current', 'replace-session', 'unmount'])(
    'handles a completed demo checkout conflict for %s',
    async (action) => {
      const profile = {
        id: 1,
        username: 'learner',
        display_name: 'Learner',
        role: 'user',
        subscription_status: 'none',
      }
      mocks.apiFetch.mockImplementation(async (url: string) => ({
        ok: true,
        json: async () => (url === '/api/auth/me' ? profile : null),
      }))
      const view = render(<ConversationMode trialMode />)
      await start()
      fireEvent.click(screen.getByRole('button', { name: 'stop' }))
      await waitFor(() =>
        expect(useAuthStore.getState().user?.username).toBe('learner')
      )
      let finish!: (body: unknown) => void
      const body = new Promise((resolve) => {
        finish = resolve
      })
      const decode = vi.fn(() => body)
      mocks.apiFetch
        .mockResolvedValueOnce({
          ok: false,
          status: 409,
          json: async () => ({ detail: 'subscription_already_active' }),
        })
        .mockResolvedValueOnce({ ok: true, json: decode })
      fireEvent.click(screen.getByText('planMonthly'))
      await waitFor(() => expect(decode).toHaveBeenCalledOnce())
      if (action === 'unmount') view.unmount()
      else if (action === 'replace-session')
        act(() => useAuthStore.getState().startSession('new-account'))
      await act(async () =>
        finish({ ...profile, subscription_status: 'active' })
      )
      if (action === 'current') {
        expect(useAuthStore.getState().user?.subscription_status).toBe('active')
        expect(mocks.push).toHaveBeenCalledWith('/dashboard')
      } else {
        expect(useAuthStore.getState().user?.subscription_status).not.toBe(
          'active'
        )
        expect(mocks.push).not.toHaveBeenCalled()
      }
      expect(screen.queryByText('checkoutError')).toBeNull()
    }
  )

  it.each([
    'automatic-start',
    'manual-start',
    'retry-after-error',
    'restart-after-stop',
  ])('preserves chat context in the voice handshake after %s', async (path) => {
    const context = [
      {
        role: 'user' as const,
        content: 'I would like to practise ordering food.',
      },
      {
        role: 'assistant' as const,
        content: 'What would you like to order?',
      },
    ]
    render(
      <ConversationMode
        initialContext={context}
        autoStart={path !== 'manual-start'}
      />
    )
    if (path === 'manual-start') {
      fireEvent.click(screen.getByRole('button', { name: 'start' }))
    }
    await waitFor(() => expect(MockWebSocket.instances).toHaveLength(1))
    let ws = MockWebSocket.instances[0]
    act(() => ws.onopen?.())
    expect(JSON.parse(ws.send.mock.calls[0][0]).context).toEqual(context)

    if (path === 'retry-after-error' || path === 'restart-after-stop') {
      if (path === 'retry-after-error') {
        act(() => ws.onerror?.())
        expect(screen.getByText('✕ errorConnection')).toBeInTheDocument()
      } else {
        fireEvent.click(screen.getByRole('button', { name: 'stop' }))
      }
      fireEvent.click(screen.getByRole('button', { name: 'startNew' }))
      await waitFor(() => expect(MockWebSocket.instances).toHaveLength(2))
      ws = MockWebSocket.instances[1]
      act(() => ws.onopen?.())
    }

    const authentication = JSON.parse(ws.send.mock.calls[0][0])
    expect(authentication.type).toBe('auth')
    expect(authentication.context).toEqual(context)
  })

  it.each([
    { speechPause: 1000, voiceFrames: 32, prependSilence: true },
    { speechPause: 2000, voiceFrames: 32, prependSilence: true },
    { speechPause: 3000, voiceFrames: 32, prependSilence: true },
    { speechPause: 3000, voiceFrames: 32, prependSilence: false },
    { speechPause: 3000, voiceFrames: 13, prependSilence: true },
  ])(
    'sends the same detected voice with pause=$speechPause frames=$voiceFrames padding=$prependSilence',
    async ({ speechPause, voiceFrames, prependSilence }) => {
      useAuthStore.setState({
        user: mapUser({
          id: 1,
          username: 'voice-test',
          display_name: 'Voice Test',
          role: 'user',
          native_language: 'es',
          target_language: 'en-GB',
          conversation_speech_pause: speechPause,
        }),
      })
      render(<ConversationMode />)
      const ws = await start()
      expect(mocks.options.redemptionMs).toBe(speechPause)
      vi.spyOn(performance, 'now').mockReturnValue(1000)

      const voiceFrame = Float32Array.from(
        { length: 512 },
        (_, index) => 0.032 * Math.sin((2 * Math.PI * 250 * index) / 16000)
      )
      const silenceFrame = new Float32Array(512)
      const segments: Float32Array[] = []
      // Only model inference is simulated; padding and segmentation use installed VAD code.
      const processor = new FrameProcessor(
        async (frame) => ({
          isSpeech: frame === voiceFrame ? 0.99 : 0.01,
          notSpeech: frame === voiceFrame ? 0.01 : 0.99,
        }),
        () => {},
        {
          ...defaultFrameProcessorOptions,
          positiveSpeechThreshold: mocks.options.positiveSpeechThreshold!,
          redemptionMs: mocks.options.redemptionMs!,
        },
        32
      )
      const handleEvent = (event: FrameProcessorEvent) => {
        if (event.msg === Message.FrameProcessed) {
          mocks.options.onFrameProcessed?.(event.probs, event.frame)
        }
        if (event.msg === Message.SpeechStart) mocks.options.onSpeechStart?.()
        if (event.msg === Message.VADMisfire) mocks.options.onVADMisfire?.()
        if (event.msg === Message.SpeechEnd) {
          segments.push(event.audio)
          mocks.options.onSpeechEnd?.(event.audio)
        }
      }

      processor.resume()
      await act(async () => {
        if (prependSilence) {
          for (let i = 0; i < processor.preSpeechPadFrames; i++) {
            await processor.process(silenceFrame, handleEvent)
          }
        }
        for (let i = 0; i < voiceFrames; i++) {
          await processor.process(voiceFrame, handleEvent)
        }
        for (let i = 0; i < processor.redemptionFrames; i++) {
          await processor.process(silenceFrame, handleEvent)
        }
      })

      expect(segments).toHaveLength(1)
      const segment = segments[0]
      const rms = Math.sqrt(
        segment.reduce((energy, sample) => energy + sample * sample, 0) /
          segment.length
      )
      expect(
        ws.send,
        JSON.stringify({
          speechPause,
          voicedMs: voiceFrames * 32,
          segmentMs: (segment.length / 16000) * 1000,
          rms,
        })
      ).toHaveBeenCalledTimes(1)
      const wav = ws.send.mock.calls[0][0] as ArrayBuffer
      expect(wav.byteLength).toBe(44 + segment.length * 2)
      const pcm = new DataView(wav)
      const firstVoicedSample = prependSilence
        ? processor.preSpeechPadFrames * 512
        : 0
      expect(pcm.getInt16(44 + (firstVoicedSample + 1) * 2, true)).toBe(
        Math.trunc(voiceFrame[1] * 0x7fff)
      )
    }
  )

  it.each([0, 0.005, NaN, Infinity])(
    'rejects a detected segment with quiet or invalid amplitude %s',
    async (amplitude) => {
      render(<ConversationMode />)
      const ws = await start()
      act(() => speak(new Float32Array(24000).fill(amplitude)))
      expect(ws.send).not.toHaveBeenCalled()
      act(() => speak())
      expect(ws.send).toHaveBeenCalledTimes(1)
    }
  )

  it.each(['misfire', 'too-short', 'assistant-active'])(
    'does not carry %s speech energy into the next utterance',
    async (discard) => {
      render(<ConversationMode />)
      const ws = await start()
      if (discard === 'assistant-active') {
        act(() => speak())
        act(() => speak())
        act(() => ws.message({ type: 'status', value: 'listening' }))
        ws.send.mockClear()
      } else if (discard === 'too-short') {
        act(() => speak(new Float32Array(512).fill(0.5)))
      } else {
        act(() => {
          mocks.options.onFrameProcessed?.(
            { isSpeech: 0.99, notSpeech: 0.01 },
            new Float32Array(24000).fill(0.5)
          )
          mocks.options.onSpeechStart?.()
          mocks.options.onVADMisfire?.()
        })
      }
      act(() => speak(new Float32Array(24000).fill(0.005)))
      expect(ws.send).not.toHaveBeenCalled()
      act(() => speak())
      expect(ws.send).toHaveBeenCalledTimes(1)
    }
  )

  it('clears unfinished speech energy when restarting the session', async () => {
    render(<ConversationMode />)
    await start()
    act(() => {
      mocks.options.onFrameProcessed?.(
        { isSpeech: 0.99, notSpeech: 0.01 },
        new Float32Array(24000).fill(0.5)
      )
      mocks.options.onSpeechStart?.()
    })
    fireEvent.click(screen.getByRole('button', { name: 'stop' }))
    const ws = await start('startNew')
    act(() => speak(new Float32Array(24000).fill(0.005)))
    expect(ws.send).not.toHaveBeenCalled()
    act(() => speak())
    expect(ws.send).toHaveBeenCalledTimes(1)
  })

  it.each(['transcribing', 'thinking'])(
    'does not advertise listening while %s blocks a new user turn',
    async (value) => {
      render(<ConversationMode />)
      const ws = await start()
      expect(screen.getByText('statusListening')).toBeInTheDocument()

      act(() => speak())
      expect(screen.getByText('statusThinking')).toBeInTheDocument()
      act(() => ws.message({ type: 'status', value, turn_id: 2 }))
      act(() => mocks.options.onSpeechStart?.())
      expect(screen.getByText('statusThinking')).toBeInTheDocument()
      act(() => speak())

      expect(ws.send).toHaveBeenCalledTimes(1)
      expect(ws.send.mock.calls[0][0]).toBeInstanceOf(ArrayBuffer)
      expect(screen.queryByText('statusListening')).not.toBeInTheDocument()
      expect(screen.getByText('statusThinking')).toBeInTheDocument()
    }
  )

  it('shows preparation between chunks and listens only after backend work and audio end', async () => {
    render(<ConversationMode />)
    const ws = await start()
    act(() => speak())
    act(() => ws.message({ type: 'status', value: 'thinking', turn_id: 2 }))
    act(() => ws.onmessage?.({ data: new ArrayBuffer(8) }))
    act(() => mocks.options.onSpeechStart?.())
    expect(screen.getByText('statusSpeaking')).toBeInTheDocument()
    act(() => mocks.options.onVADMisfire?.())

    act(() => mocks.onAudioIdle?.())
    expect(screen.getByText('statusThinking')).toBeInTheDocument()
    act(() => speak())
    expect(ws.send).toHaveBeenCalledTimes(1)

    act(() => ws.onmessage?.({ data: new ArrayBuffer(8) }))
    act(() => ws.message({ type: 'status', value: 'listening', turn_id: 2 }))
    act(() => ws.message({ type: 'turn_complete', turn_id: 2 }))
    expect(screen.getByText('statusSpeaking')).toBeInTheDocument()
    act(() => speak())
    expect(ws.send).toHaveBeenCalledTimes(1)

    act(() => mocks.onAudioIdle?.())
    expect(screen.getByText('statusListening')).toBeInTheDocument()
    act(() => speak())
    expect(ws.send).toHaveBeenCalledTimes(2)
  })

  it.each(['inactivity', 'max_duration'])(
    'keeps only an applicable %s warning after a new accepted utterance',
    async (reason) => {
      render(<ConversationMode />)
      const ws = await start()
      vi.useFakeTimers()
      act(() =>
        ws.message({
          type: 'session_warning',
          reason,
          remaining_seconds: 60,
        })
      )
      expect(screen.getByText('warningTimeout:60')).toBeInTheDocument()
      await act(async () => {
        await vi.advanceTimersByTimeAsync(10_000)
      })
      act(() => speak())
      act(() =>
        ws.message({ type: 'status', value: 'transcribing', turn_id: 2 })
      )
      expect(ws.send).toHaveBeenCalledTimes(1)
      await act(async () => {
        await vi.advanceTimersByTimeAsync(50_000)
      })

      expect(ws.close).not.toHaveBeenCalled()
      if (reason === 'inactivity') {
        expect(screen.queryByText(/warningTimeout:/)).not.toBeInTheDocument()
      } else {
        expect(screen.getByText('warningTimeout:0')).toBeInTheDocument()
      }
    }
  )

  it.each([
    ['max_duration', 'inactivity'],
    ['inactivity', 'max_duration'],
  ])(
    'keeps the maximum-duration deadline when warnings arrive as %s then %s',
    async (first, second) => {
      render(<ConversationMode />)
      const ws = await start()
      vi.useFakeTimers()
      act(() => {
        for (const reason of [first, second]) {
          ws.message({
            type: 'session_warning',
            reason,
            remaining_seconds: reason === 'inactivity' ? 20 : 60,
          })
        }
      })
      expect(screen.getByText('warningTimeout:20')).toBeInTheDocument()
      await act(async () => {
        await vi.advanceTimersByTimeAsync(10_000)
      })
      act(() => speak())
      act(() =>
        ws.message({ type: 'status', value: 'transcribing', turn_id: 2 })
      )
      expect(screen.getByText('warningTimeout:50')).toBeInTheDocument()
      await act(async () => {
        await vi.advanceTimersByTimeAsync(10_000)
      })
      expect(screen.getByText('warningTimeout:40')).toBeInTheDocument()
    }
  )

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
