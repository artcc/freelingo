import { act, cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react'
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
}))

vi.mock('@ricky0123/vad-react', () => ({
  useMicVAD: (options: Parameters<typeof useMicVAD>[0]) => {
    mocks.options = options
    return { loading: false, errored: false, start: mocks.start, pause: mocks.pause }
  },
}))
vi.mock('next-intl', () => ({
  useTranslations: () => Object.assign((key: string) => key, { raw: () => [] }),
}))
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
vi.mock('@/lib/review-prompt-triggers', () => ({ shouldShowVoiceReviewPrompt: () => false }))
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
  close = vi.fn(() => { this.readyState = 3 })

  constructor() { MockWebSocket.instances.push(this) }

  message(message: unknown) {
    this.onmessage?.({ data: JSON.stringify(message) })
  }
}

function microphone() {
  const stop = vi.fn()
  return { stream: { getTracks: () => [{ stop }] } as unknown as MediaStream, stop }
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
  mocks.getUserMedia.mockReset().mockResolvedValue(microphone().stream)
  mocks.start.mockImplementation(async () => { await mocks.options.getStream?.() })
  mocks.pause.mockResolvedValue(undefined)
  mocks.closeAudio.mockResolvedValue(undefined)
  mocks.enqueue.mockResolvedValue(undefined)
  mocks.apiFetch.mockResolvedValue({ ok: true, json: async () => null })
  vi.stubGlobal('WebSocket', MockWebSocket)
  vi.stubGlobal('AudioContext', class {
    state = 'running'
    close = mocks.closeAudio
  })
  vi.stubGlobal('navigator', { mediaDevices: { getUserMedia: mocks.getUserMedia } })
  Element.prototype.scrollIntoView = vi.fn()
  useAuthStore.setState({ accessToken: 'token', user: null })
})

afterEach(() => {
  cleanup()
  vi.unstubAllGlobals()
})

describe('ConversationMode session lifecycle', () => {
  it('retries denied permission without poisoning VAD', async () => {
    mocks.getUserMedia.mockRejectedValueOnce(new DOMException('Denied', 'NotAllowedError'))
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
    mocks.getUserMedia.mockReturnValue(new Promise<MediaStream>((resolve) => { grant = resolve }))
    const view = render(<ConversationMode />)
    fireEvent.click(screen.getByRole('button', { name: 'start' }))
    view.unmount()
    await act(async () => { grant(mic.stream) })
    expect(mic.stop).toHaveBeenCalledTimes(1)
    expect(mocks.start).not.toHaveBeenCalled()
    expect(MockWebSocket.instances).toHaveLength(0)
  })

  it.each(['json', 'onerror', 'onclose'])('cleans up %s once and ignores obsolete callbacks after restart', async (kind) => {
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
      oldMessage({ data: JSON.stringify({ type: 'session_end', reason: 'inactivity' }) })
      oldError()
      oldClose({ code: 1006, reason: '' })
    })
    expect(current.close).not.toHaveBeenCalled()
    expect(screen.getByRole('button', { name: 'stop' })).toBeDefined()
  })

  it.each([
    { type: 'status', value: 'listening' },
    { type: 'turn_complete' },
    ...['stt_failed', 'llm_failed', 'tts_failed'].map((code) => ({ type: 'error', code })),
  ])('blocks immediately and releases on $type $value $code', async (outcome) => {
    render(<ConversationMode />)
    const ws = await start()
    act(() => { speak(); speak() })
    expect(ws.send).toHaveBeenCalledTimes(1)
    act(() => ws.message({ type: 'status', value: 'transcribing' }))
    act(() => speak())
    expect(ws.send).toHaveBeenCalledTimes(1)
    act(() => ws.message(outcome))
    expect(screen.getByRole('button', { name: 'stop' })).toBeDefined()
    act(() => speak())
    expect(ws.send).toHaveBeenCalledTimes(2)
    expect(ws.close).not.toHaveBeenCalled()
  })

  it('clears visual speech and discards the unfinished segment on misfire', async () => {
    render(<ConversationMode />)
    const ws = await start()
    act(() => { mocks.options.onSpeechStart?.() })
    expect(screen.getByTestId('speaking').textContent).toBe('true')
    act(() => { mocks.options.onVADMisfire?.() })
    expect(screen.getByTestId('speaking').textContent).toBe('false')
    act(() => { mocks.options.onSpeechEnd?.(new Float32Array(24000).fill(0.05)) })
    expect(ws.send).not.toHaveBeenCalled()
  })

  it('ignores a Blob decoded after a new session has started', async () => {
    render(<ConversationMode />)
    const ws = await start()
    let decode!: (buffer: ArrayBuffer) => void
    const blob = new Blob()
    blob.arrayBuffer = vi.fn(() => new Promise<ArrayBuffer>((resolve) => { decode = resolve }))
    act(() => ws.onmessage?.({ data: blob }))
    act(() => ws.onerror?.())
    const current = await start('startNew')
    await act(async () => { decode(new ArrayBuffer(8)) })
    expect(mocks.enqueue).not.toHaveBeenCalled()
    expect(current.close).not.toHaveBeenCalled()
    act(() => speak())
    expect(current.send).toHaveBeenCalledTimes(1)
  })

  it('releases resources after a WAV send throws and allows restart', async () => {
    render(<ConversationMode />)
    const ws = await start()
    ws.send.mockImplementationOnce(() => { throw new Error('Transport closed') })
    act(() => speak())
    expect(ws.close).toHaveBeenCalledTimes(1)
    const current = await start('startNew')
    act(() => speak())
    expect(current.send).toHaveBeenCalledTimes(1)
  })
})
