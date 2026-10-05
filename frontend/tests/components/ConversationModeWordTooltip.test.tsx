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
import ConversationMode from '@/components/conversation/ConversationMode'
import { useAuthStore } from '@/store/auth'
import { useLanguageStore } from '@/store/language'
import { getLanguageByCode } from '@/lib/target-languages'

vi.mock('next-intl', () => ({
  useTranslations: () => {
    const t = ((key: string) => key) as ((key: string) => string) & {
      raw: (key: string) => string[]
    }
    t.raw = (key: string) =>
      key === 'starters' ? ['a', 'b', 'c', 'd', 'e', 'f'] : []
    return t
  },
  useLocale: () => 'en',
}))

const mockApiFetch = vi.hoisted(() => vi.fn())
vi.mock('@/lib/api', () => ({ apiFetch: mockApiFetch }))

vi.mock('@/lib/conversation-ws', () => ({
  buildConversationWsUrl: () => 'ws://test',
}))

vi.mock('@/lib/audio', () => ({
  createAudioQueue: () => ({
    enqueue: vi.fn().mockResolvedValue(undefined),
    cancel: vi.fn(),
  }),
  float32ToWav: vi.fn(),
}))

const vadMocks = vi.hoisted(() => ({
  options: {} as Parameters<typeof useMicVAD>[0],
}))

vi.mock('@ricky0123/vad-react', () => ({
  useMicVAD: (options: Parameters<typeof useMicVAD>[0]) => {
    vadMocks.options = options
    return {
      loading: false,
      errored: false,
      start: vi.fn(async () => {
        await vadMocks.options.getStream?.()
      }),
      pause: vi.fn().mockResolvedValue(undefined),
      listening: false,
      userSpeaking: false,
    }
  },
}))

vi.mock('next/navigation', () => ({ useRouter: () => ({ push: vi.fn() }) }))

vi.mock('@/components/reviews/ReviewPrompt', () => ({
  ReviewPrompt: () => null,
  getReviewPromptDismissal: () => null,
}))

vi.mock('@/lib/review-prompt-triggers', () => ({
  shouldShowVoiceReviewPrompt: () => false,
}))

class MockAudioContext {
  state = 'running'
  resume = vi.fn().mockResolvedValue(undefined)
  close = vi.fn().mockResolvedValue(undefined)
}

function microphoneStream() {
  return {
    getTracks: () => [{ stop: vi.fn() }],
  } as unknown as MediaStream
}

class MockWebSocket {
  static OPEN = 1
  static instances: MockWebSocket[] = []
  static get last(): MockWebSocket | undefined {
    return MockWebSocket.instances[MockWebSocket.instances.length - 1]
  }

  readyState = 1
  binaryType = ''
  onopen: ((ev: Event) => void) | null = null
  onmessage: ((ev: MessageEvent) => void) | null = null
  onclose: ((ev: CloseEvent) => void) | null = null
  onerror: ((ev: Event) => void) | null = null
  send = vi.fn()
  close = vi.fn()

  constructor(public url: string) {
    MockWebSocket.instances.push(this)
  }
}

function mockSelection(word: string) {
  const rect = { left: 10, top: 20, width: 30, height: 10 }
  const selection = {
    isCollapsed: false,
    rangeCount: 1,
    toString: () => word,
    getRangeAt: () => ({ getBoundingClientRect: () => rect }),
    removeAllRanges: vi.fn(),
  }
  vi.spyOn(window, 'getSelection').mockReturnValue(
    selection as unknown as Selection
  )
}

async function selectWordInBubble(bubbleText: string, word: string) {
  mockSelection(word)
  fireEvent.pointerUp(screen.getByText(bubbleText))
  await act(async () => {
    await new Promise((resolve) => setTimeout(resolve, 0))
  })
}

async function startSession() {
  fireEvent.click(screen.getByText('start'))
  await waitFor(() => expect(MockWebSocket.instances.length).toBeGreaterThan(0))
  act(() => {
    MockWebSocket.last?.onopen?.(new Event('open'))
  })
  await waitFor(() =>
    expect(screen.getByRole('button', { name: 'stop' })).toBeInTheDocument()
  )
}

function deliverTranscript(payload: Record<string, unknown>) {
  act(() => {
    MockWebSocket.last?.onmessage?.({
      data: JSON.stringify({ type: 'transcript', final: true, ...payload }),
    } as MessageEvent)
  })
}

const baseUser = {
  id: 1,
  username: 'u',
  displayName: 'U',
  role: 'user' as const,
  conversation_max_duration: 1800,
  conversation_inactivity_timeout: 180,
}

describe('ConversationMode word tooltip dismissal', () => {
  beforeEach(() => {
    mockApiFetch.mockReset()
    mockApiFetch.mockImplementation(async (url: string) => {
      if (url === '/api/auth/quota') {
        return { ok: true, json: async () => null }
      }
      return { ok: true, json: async () => ({}) }
    })
    useAuthStore.setState({ accessToken: 'tok', user: { ...baseUser } })
    MockWebSocket.instances = []
    Element.prototype.scrollIntoView = vi.fn()
    vi.stubGlobal('AudioContext', MockAudioContext)
    vi.stubGlobal('WebSocket', MockWebSocket)
    vi.stubGlobal('navigator', {
      mediaDevices: { getUserMedia: vi.fn(async () => microphoneStream()) },
    })
  })

  afterEach(() => {
    cleanup()
    vi.unstubAllGlobals()
  })

  it.each([undefined, 7])('saves words with the lesson owner only in practice mode (%s)', async (lessonId) => {
    useLanguageStore.setState({ activeLanguage: getLanguageByCode('fr-FR') ?? null })
    render(<ConversationMode lessonId={lessonId} targetLanguage="fr-FR" cefrLevel="B1" />)
    await startSession()
    deliverTranscript({ role: 'assistant', text: 'Bon voyage', turn_id: 1 })
    await selectWordInBubble('Bon voyage', 'voyage')
    act(() => useLanguageStore.setState({ activeLanguage: getLanguageByCode('de-DE') ?? null }))
    fireEvent.click(screen.getByText('saveWord'))
    await waitFor(() => expect(mockApiFetch).toHaveBeenCalledWith('/api/flashcards/from-word', expect.any(Object)))
    const call = mockApiFetch.mock.calls.find(([url]) => url === '/api/flashcards/from-word')!
    expect(JSON.parse(call[1].body)).toEqual({
      word: 'voyage', context: 'Bon voyage', cefr_level: 'B1',
      ...(lessonId !== undefined ? { lesson_id: lessonId } : {}),
    })
  })

  it('dismisses the word tooltip when a new transcript turn arrives', async () => {
    render(<ConversationMode targetLanguage="es" />)
    await startSession()

    deliverTranscript({
      role: 'assistant',
      text: 'El perro corre',
      turn_id: 1,
    })
    await selectWordInBubble('El perro corre', 'perro')
    expect(screen.getByText('saveWord')).toBeInTheDocument()
    expect(screen.getByText('perro')).toBeInTheDocument()

    deliverTranscript({ role: 'user', text: 'Ya veo', turn_id: 2 })

    expect(screen.queryByText('saveWord')).not.toBeInTheDocument()
  })

  it('dismisses the word tooltip when the session is stopped', async () => {
    render(<ConversationMode targetLanguage="es" />)
    await startSession()

    deliverTranscript({
      role: 'assistant',
      text: 'El perro corre',
      turn_id: 1,
    })
    await selectWordInBubble('El perro corre', 'perro')
    expect(screen.getByText('saveWord')).toBeInTheDocument()

    fireEvent.click(screen.getByRole('button', { name: 'stop' }))

    expect(screen.queryByText('saveWord')).not.toBeInTheDocument()
  })

  it('dismisses the word tooltip and clears the transcript when a new session is started', async () => {
    render(<ConversationMode targetLanguage="es" />)
    await startSession()

    deliverTranscript({
      role: 'assistant',
      text: 'El perro corre',
      turn_id: 1,
    })
    await selectWordInBubble('El perro corre', 'perro')
    expect(screen.getByText('saveWord')).toBeInTheDocument()

    fireEvent.click(screen.getByRole('button', { name: 'stop' }))
    expect(screen.getByText('El perro corre')).toBeInTheDocument()

    await selectWordInBubble('El perro corre', 'perro')
    expect(screen.getByText('saveWord')).toBeInTheDocument()

    fireEvent.click(screen.getByText('startNew'))

    expect(screen.queryByText('saveWord')).not.toBeInTheDocument()
    expect(screen.queryByText('El perro corre')).not.toBeInTheDocument()
  })
})
