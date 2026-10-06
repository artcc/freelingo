import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react'
import React from 'react'
import { AudioPlayer } from '@/components/ui/AudioPlayer'
import { useAuthStore } from '@/store/auth'

vi.mock('next-intl', () => ({
  useTranslations: () => (key: string) => key,
}))

function makeOkResponse(blob?: Blob) {
  return {
    ok: true,
    status: 200,
    blob: () =>
      Promise.resolve(blob ?? new Blob(['audio'], { type: 'audio/mpeg' })),
    headers: new Headers(),
  }
}

const PLAY = '▶'
const PAUSE = '■'
const ERROR = '✕'
const LOADING = '...'

// Stores the latest mock Audio instance so tests can inspect it
let currentAudioMock: ReturnType<typeof makeAudioMock> | null = null

function makeAudioMock() {
  return {
    play: vi.fn().mockResolvedValue(undefined),
    pause: vi.fn(),
    onended: null as (() => void) | null,
    onerror: null as (() => void) | null,
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
  }
}

describe('AudioPlayer', () => {
  let fetchMock: ReturnType<typeof vi.fn>
  let localStorageStore: Record<string, string>
  let revokeCalls: string[]
  let urlCounter: number

  beforeEach(() => {
    urlCounter = 0
    revokeCalls = []
    currentAudioMock = makeAudioMock()

    // Replace Audio constructor directly on globalThis (not via stubGlobal)
    // A plain function assignment survives vi.restoreAllMocks()
    ;(globalThis as any).Audio = function () {
      currentAudioMock = makeAudioMock()
      return currentAudioMock
    }

    // Replace fetch directly
    fetchMock = vi.fn()
    ;(globalThis as any).fetch = fetchMock

    // Spy on URL static methods — these get restored by setup.ts afterEach,
    // but we re-create them in every beforeEach so it's fine.
    vi.spyOn(URL, 'createObjectURL').mockImplementation(() => {
      urlCounter++
      return `blob:fake-url-${urlCounter}`
    })
    vi.spyOn(URL, 'revokeObjectURL').mockImplementation((url: string) => {
      revokeCalls.push(url)
    })

    // Fresh localStorage
    localStorageStore = {}
    ;(globalThis as any).localStorage = {
      getItem: vi.fn((key: string) => localStorageStore[key] ?? null),
      setItem: vi.fn((key: string, value: string) => {
        localStorageStore[key] = value
      }),
      removeItem: vi.fn((key: string) => {
        delete localStorageStore[key]
      }),
      clear: vi.fn(() => {
        localStorageStore = {}
      }),
      get length() {
        return Object.keys(localStorageStore).length
      },
      key: vi.fn((i: number) => Object.keys(localStorageStore)[i] ?? null),
    }

    useAuthStore.setState({ accessToken: null, user: null })
  })

  afterEach(() => {
    // beforeEach overwrites all globals, so no manual cleanup needed here.
    // vi.restoreAllMocks() (called in setup.ts) already handles spies and vi.fn mocks.
  })

  // ───────────── RENDERING ─────────────

  it('renders in idle state with the play symbol', () => {
    render(<AudioPlayer text="Hello" />)
    expect(screen.getByText(PLAY)).toBeDefined()
  })

  it('renders idle aria-label', () => {
    render(<AudioPlayer text="Hello" />)
    expect(screen.getByLabelText('ariaListen')).toBeDefined()
  })

  it('renders idle title', () => {
    render(<AudioPlayer text="Hello" />)
    expect(screen.getByTitle('listen')).toBeDefined()
  })

  it('applies sm size class by default', () => {
    render(<AudioPlayer text="Hello" />)
    expect(screen.getByRole('button').className).toContain('px-2 py-1')
  })

  it('applies md size class when size=md', () => {
    render(<AudioPlayer text="Hello" size="md" />)
    expect(screen.getByRole('button').className).toContain('px-3 py-2')
  })

  it('applies custom className', () => {
    render(<AudioPlayer text="Hello" className="custom-audio" />)
    expect(screen.getByRole('button').className).toContain('custom-audio')
  })

  it('has idle-only color classes (no active/animation/error)', () => {
    render(<AudioPlayer text="Hello" />)
    const c = screen.getByRole('button').className.split(/\s+/).filter(Boolean)
    expect(c).toContain('text-fl-muted-2')
    expect(c).not.toContain('text-fl-fg')
    expect(c).not.toContain('animate-pulse')
    expect(c).not.toContain('text-fl-error-fg')
  })

  // ───────────── PLAY FLOW ─────────────

  it('calls POST /api/tts with correct body and headers on click', async () => {
    fetchMock.mockResolvedValueOnce(makeOkResponse())

    render(<AudioPlayer text="Hello world" />)

    await act(async () => {
      fireEvent.click(screen.getByRole('button'))
    })

    expect(fetchMock).toHaveBeenCalledWith(
      '/api/tts',
      expect.objectContaining({
        method: 'POST',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
        }),
        body: JSON.stringify({ text: 'Hello world', voice: undefined }),
      })
    )
  })

  it('keeps custom audio URLs as GET requests by default', async () => {
    fetchMock.mockResolvedValueOnce(makeOkResponse())
    const audioUrl = '/api/phrasebook/audio/greetings/0?language=es'
    render(<AudioPlayer text="Hola" audioUrl={audioUrl} />)

    await act(async () => {
      fireEvent.click(screen.getByRole('button'))
    })

    expect(fetchMock).toHaveBeenCalledWith(
      audioUrl,
      expect.objectContaining({ credentials: 'include' })
    )
    expect(fetchMock.mock.calls[0][1].method).toBeUndefined()
    expect(fetchMock.mock.calls[0][1].body).toBeUndefined()
    expect(screen.getByText(PAUSE)).toBeDefined()
  })

  it('sends X-TTS-Trace-ID header', async () => {
    fetchMock.mockResolvedValueOnce(makeOkResponse())

    render(<AudioPlayer text="Hello" />)
    fireEvent.click(screen.getByRole('button'))

    await waitFor(() => {
      expect(fetchMock.mock.calls[0][1].headers['X-TTS-Trace-ID']).toMatch(
        /^tts-/
      )
    })
  })

  it('sends Authorization header when access token is available', async () => {
    useAuthStore.setState({ accessToken: 'tok-abc123' })
    fetchMock.mockResolvedValueOnce(makeOkResponse())

    render(<AudioPlayer text="Hello" />)
    fireEvent.click(screen.getByRole('button'))

    await waitFor(() => {
      expect(fetchMock.mock.calls[0][1].headers.Authorization).toBe(
        'Bearer tok-abc123'
      )
    })
  })

  it('does not send Authorization header when no access token', async () => {
    fetchMock.mockResolvedValueOnce(makeOkResponse())

    render(<AudioPlayer text="Hello" />)
    fireEvent.click(screen.getByRole('button'))

    await waitFor(() => {
      expect(fetchMock.mock.calls[0][1].headers.Authorization).toBeUndefined()
    })
  })

  it('creates Audio, calls play, transitions to playing', async () => {
    fetchMock.mockResolvedValueOnce(makeOkResponse())

    render(<AudioPlayer text="Hello" />)

    await act(async () => {
      fireEvent.click(screen.getByRole('button'))
    })

    await waitFor(() => {
      expect(currentAudioMock!.play).toHaveBeenCalled()
      expect(screen.getByText(PAUSE)).toBeDefined()
    })
  })

  it('renders playing aria-label and title', async () => {
    fetchMock.mockResolvedValueOnce(makeOkResponse())

    render(<AudioPlayer text="Hello" />)
    fireEvent.click(screen.getByRole('button'))

    await waitFor(() => {
      expect(screen.getByLabelText('ariaStop')).toBeDefined()
      expect(screen.getByTitle('stop')).toBeDefined()
    })
  })

  it('has playing-specific color class', async () => {
    fetchMock.mockResolvedValueOnce(makeOkResponse())

    render(<AudioPlayer text="Hello" />)

    await act(async () => {
      fireEvent.click(screen.getByRole('button'))
    })

    await waitFor(() => {
      const c = screen
        .getByRole('button')
        .className.split(/\s+/)
        .filter(Boolean)
      expect(c).toContain('text-fl-fg')
    })
  })

  // ───────────── LOADING ─────────────

  it('shows loading ellipsis while fetching', async () => {
    fetchMock.mockImplementationOnce(() => new Promise<Response>(() => {}))

    render(<AudioPlayer text="Hello" />)
    fireEvent.click(screen.getByRole('button'))

    await waitFor(() => {
      expect(screen.getByText(LOADING)).toBeDefined()
    })
  })

  it('shows loading color class with pulse animation', async () => {
    fetchMock.mockImplementationOnce(() => new Promise<Response>(() => {}))

    render(<AudioPlayer text="Hello" />)
    fireEvent.click(screen.getByRole('button'))

    await waitFor(() => {
      const c = screen
        .getByRole('button')
        .className.split(/\s+/)
        .filter(Boolean)
      expect(c).toContain('animate-pulse')
      expect(c).toContain('text-fl-muted-3')
    })
  })

  it('is idempotent — does nothing when clicked during loading', async () => {
    fetchMock.mockImplementationOnce(() => new Promise<Response>(() => {}))

    render(<AudioPlayer text="Hello" />)
    const btn = screen.getByRole('button')

    fireEvent.click(btn)
    await waitFor(() => {
      expect(screen.getByText(LOADING)).toBeDefined()
    })

    fireEvent.click(btn)
    fireEvent.click(btn)
    expect(fetchMock).toHaveBeenCalledTimes(1)
  })

  // ───────────── STOP ─────────────

  it('pauses audio and returns to idle when clicked while playing', async () => {
    fetchMock.mockResolvedValueOnce(makeOkResponse())

    render(<AudioPlayer text="Hello" />)
    const btn = screen.getByRole('button')

    await act(async () => {
      fireEvent.click(btn)
    })

    await waitFor(() => {
      expect(screen.getByText(PAUSE)).toBeDefined()
    })

    await act(async () => {
      fireEvent.click(btn)
    })

    expect(currentAudioMock!.pause).toHaveBeenCalled()
    expect(screen.getByText(PLAY)).toBeDefined()
  })

  // ───────────── VOICE RESOLUTION ─────────────

  it('sends explicit voice prop in request body', async () => {
    fetchMock.mockResolvedValueOnce(makeOkResponse())

    render(<AudioPlayer text="Hello" voice="nova" />)
    fireEvent.click(screen.getByRole('button'))

    await waitFor(() => {
      expect(fetchMock).toHaveBeenCalledWith(
        '/api/tts',
        expect.objectContaining({
          body: JSON.stringify({ text: 'Hello', voice: 'nova' }),
        })
      )
    })
  })

  it('resolves voice from localStorage when no voice prop', async () => {
    localStorage.setItem('tts_voice', 'alloy')
    fetchMock.mockResolvedValueOnce(makeOkResponse())

    render(<AudioPlayer text="Hello" />)
    fireEvent.click(screen.getByRole('button'))

    await waitFor(() => {
      expect(fetchMock).toHaveBeenCalledWith(
        '/api/tts',
        expect.objectContaining({
          body: JSON.stringify({ text: 'Hello', voice: 'alloy' }),
        })
      )
    })
  })

  it('prioritizes voice prop over localStorage', async () => {
    localStorage.setItem('tts_voice', 'alloy')
    fetchMock.mockResolvedValueOnce(makeOkResponse())

    render(<AudioPlayer text="Hello" voice="nova" />)
    fireEvent.click(screen.getByRole('button'))

    await waitFor(() => {
      expect(fetchMock).toHaveBeenCalledWith(
        '/api/tts',
        expect.objectContaining({
          body: JSON.stringify({ text: 'Hello', voice: 'nova' }),
        })
      )
    })
  })

  it('sends no voice when neither prop nor localStorage is set', async () => {
    fetchMock.mockResolvedValueOnce(makeOkResponse())

    render(<AudioPlayer text="Hello" />)
    fireEvent.click(screen.getByRole('button'))

    await waitFor(() => {
      const body = JSON.parse(fetchMock.mock.calls[0][1].body)
      expect(body.voice).toBeUndefined()
    })
  })

  // ───────────── AUDIO ENDED ─────────────

  it('revokes object URL and returns to idle when audio ends', async () => {
    fetchMock.mockResolvedValueOnce(makeOkResponse())

    render(<AudioPlayer text="Hello" />)

    await act(async () => {
      fireEvent.click(screen.getByRole('button'))
    })

    await waitFor(() => {
      expect(screen.getByText(PAUSE)).toBeDefined()
    })

    await act(async () => {
      currentAudioMock!.onended!()
    })

    expect(revokeCalls).toContain('blob:fake-url-1')
    expect(screen.getByText(PLAY)).toBeDefined()
  })

  // ───────────── ERROR: HTTP ─────────────

  it('shows error on non-ok HTTP response then recovers after 2s', async () => {
    vi.useFakeTimers()
    fetchMock.mockResolvedValueOnce({ ok: false, status: 500 })

    render(<AudioPlayer text="Hello" />)

    await act(async () => {
      fireEvent.click(screen.getByRole('button'))
    })

    expect(screen.getByText(ERROR)).toBeDefined()
    const c = screen.getByRole('button').className.split(/\s+/).filter(Boolean)
    expect(c).toContain('text-fl-error-fg')

    act(() => {
      vi.advanceTimersByTime(2000)
    })

    expect(screen.getByText(PLAY)).toBeDefined()
    vi.useRealTimers()
  })

  it('shows error on network failure then recovers after 2s', async () => {
    vi.useFakeTimers()
    fetchMock.mockRejectedValueOnce(new Error('Network error'))

    render(<AudioPlayer text="Hello" />)

    await act(async () => {
      fireEvent.click(screen.getByRole('button'))
    })

    expect(screen.getByText(ERROR)).toBeDefined()
    const c = screen.getByRole('button').className.split(/\s+/).filter(Boolean)
    expect(c).toContain('text-fl-error-fg')

    act(() => {
      vi.advanceTimersByTime(2000)
    })

    expect(screen.getByText(PLAY)).toBeDefined()
    vi.useRealTimers()
  })

  // ───────────── ERROR: AUDIO PLAYBACK ─────────────

  it('shows error when audio onerror fires then recovers after 2s', async () => {
    // Phase 1: real timers for click→fetch→play transition
    fetchMock.mockResolvedValueOnce(makeOkResponse())

    render(<AudioPlayer text="Hello" />)

    await act(async () => {
      fireEvent.click(screen.getByRole('button'))
    })

    await waitFor(() => {
      expect(screen.getByText(PAUSE)).toBeDefined()
    })

    // Phase 2: fake timers for onerror + 2s recovery timeout
    vi.useFakeTimers()

    act(() => {
      currentAudioMock!.onerror!()
    })

    expect(screen.getByText(ERROR)).toBeDefined()

    act(() => {
      vi.advanceTimersByTime(2000)
    })

    expect(screen.getByText(PLAY)).toBeDefined()
    vi.useRealTimers()
  })

  // ───────────── UNMOUNT ─────────────

  it.each(['before retry', 'after retry'] as const)(
    'keeps a retry playing when onerror is followed by play rejection %s',
    async (rejectionTiming) => {
      vi.useFakeTimers()
      try {
        const failedAudio = makeAudioMock()
        const retryAudio = makeAudioMock()
        let rejectPlay!: (error: Error) => void
        failedAudio.play.mockImplementation(
          () =>
            new Promise<void>((_, reject) => {
              rejectPlay = reject
            })
        )
        const audioConstructor = vi.fn(function () {
          return retryAudio
        })
        audioConstructor.mockImplementationOnce(function () {
          return failedAudio
        })
        globalThis.Audio = audioConstructor as unknown as typeof Audio
        fetchMock.mockResolvedValue(makeOkResponse())
        const { unmount } = render(<AudioPlayer text="Hello" />)

        await act(async () => {
          fireEvent.click(screen.getByRole('button'))
        })
        act(() => {
          failedAudio.onerror!()
        })
        expect(screen.getByText(ERROR)).toBeDefined()
        if (rejectionTiming === 'before retry') {
          await act(async () => {
            rejectPlay(new Error('Playback failed'))
          })
        }
        expect(vi.getTimerCount()).toBe(1)

        await act(async () => {
          fireEvent.click(screen.getByRole('button'))
        })
        expect(screen.getByText(PAUSE)).toBeDefined()
        if (rejectionTiming === 'after retry') {
          await act(async () => {
            rejectPlay(new Error('Playback failed'))
          })
        }
        act(() => {
          vi.advanceTimersByTime(2500)
        })
        expect(screen.getByText(PAUSE)).toBeDefined()
        expect(retryAudio.pause).not.toHaveBeenCalled()

        // The next click stops the retry instead of starting overlapping audio.
        fireEvent.click(screen.getByRole('button'))
        expect(screen.getByText(PLAY)).toBeDefined()
        expect(retryAudio.pause).toHaveBeenCalledTimes(1)
        expect(audioConstructor).toHaveBeenCalledTimes(2)
        expect(fetchMock).toHaveBeenCalledTimes(2)
        expect(revokeCalls).toEqual(['blob:fake-url-1', 'blob:fake-url-2'])
        unmount()
        expect(vi.getTimerCount()).toBe(0)
      } finally {
        vi.useRealTimers()
      }
    }
  )

  it('clears recovery after both playback error paths when unmounted', async () => {
    vi.useFakeTimers()
    try {
      const audio = makeAudioMock()
      audio.play.mockImplementation(() => {
        audio.onerror!()
        return Promise.reject(new Error('Playback failed'))
      })
      globalThis.Audio = function () {
        return audio
      } as unknown as typeof Audio
      fetchMock.mockResolvedValue(makeOkResponse())
      const { unmount } = render(<AudioPlayer text="Hello" />)
      await act(async () => {
        fireEvent.click(screen.getByRole('button'))
      })
      expect(screen.getByText(ERROR)).toBeDefined()
      expect(audio.pause).toHaveBeenCalledTimes(1)
      expect(revokeCalls).toEqual(['blob:fake-url-1'])
      unmount()
      expect(vi.getTimerCount()).toBe(0)
    } finally {
      vi.useRealTimers()
    }
  })

  it('still reports a request timeout and recovers', async () => {
    vi.useFakeTimers()
    try {
      fetchMock.mockImplementation(
        (_, { signal }: RequestInit) =>
          new Promise((_, reject) => {
            signal!.addEventListener('abort', () =>
              reject(new DOMException('Aborted', 'AbortError'))
            )
          })
      )
      const { unmount } = render(<AudioPlayer text="Hello" timeoutMs={100} />)
      await act(async () => {
        fireEvent.click(screen.getByRole('button'))
      })
      await act(async () => {
        await vi.advanceTimersByTimeAsync(100)
      })
      expect(screen.getByText(ERROR)).toBeDefined()
      act(() => {
        vi.advanceTimersByTime(2000)
      })
      expect(screen.getByText(PLAY)).toBeDefined()
      unmount()
    } finally {
      vi.useRealTimers()
    }
  })

  it('unmounts without throwing while idle', () => {
    const { unmount } = render(<AudioPlayer text="Hello" />)
    expect(() => unmount()).not.toThrow()
  })

  it('unmounts without throwing while loading', () => {
    // Use a promise that never settles so the component stays in loading state
    fetchMock.mockImplementationOnce(() => new Promise<Response>(() => {}))

    const { unmount } = render(<AudioPlayer text="Hello" />)

    act(() => {
      fireEvent.click(screen.getByRole('button'))
    })

    // After act flushes, React has committed the 'loading' state
    expect(screen.getByText(LOADING)).toBeDefined()
    expect(() => unmount()).not.toThrow()
  })

  it('unmounts without throwing while playing', async () => {
    fetchMock.mockResolvedValueOnce(makeOkResponse())

    const { unmount } = render(<AudioPlayer text="Hello" />)

    await act(async () => {
      fireEvent.click(screen.getByRole('button'))
    })

    await waitFor(() => {
      expect(screen.getByText(PAUSE)).toBeDefined()
    })

    expect(() => unmount()).not.toThrow()
  })

  it('unmounts without throwing while in error state', async () => {
    vi.useFakeTimers()
    fetchMock.mockRejectedValueOnce(new Error('fail'))

    const { unmount } = render(<AudioPlayer text="Hello" />)

    await act(async () => {
      fireEvent.click(screen.getByRole('button'))
    })

    expect(screen.getByText(ERROR)).toBeDefined()
    expect(() => unmount()).not.toThrow()

    vi.useRealTimers()
  })

  // ───────────── MULTIPLE INSTANCES ─────────────

  it('two instances work independently', async () => {
    fetchMock.mockResolvedValueOnce(makeOkResponse())
    fetchMock.mockResolvedValueOnce(makeOkResponse())

    render(
      <>
        <AudioPlayer text="Item A" />
        <AudioPlayer text="Item B" />
      </>
    )

    const buttons = screen.getAllByRole('button')
    expect(buttons).toHaveLength(2)

    // Start A
    await act(async () => {
      fireEvent.click(buttons[0])
    })
    await waitFor(() => {
      expect(buttons[0].textContent).toBe(PAUSE)
    })

    // Start B
    await act(async () => {
      fireEvent.click(buttons[1])
    })
    await waitFor(() => {
      expect(buttons[1].textContent).toBe(PAUSE)
    })

    // Stop A — B should keep playing
    await act(async () => {
      fireEvent.click(buttons[0])
    })
    // Note: each click creates a fresh Audio(), so after pausing A,
    // its audioRef is set to null. The next click on A would create a new audio.
    // currentAudioMock here points to the LAST-created Audio (B's), but
    // A's pause was called on the previous Audio instance. We can't assert
    // on currentAudioMock.pause because it got overwritten when B started.
    // Instead verify via UI state.
    expect(buttons[0].textContent).toBe(PLAY)
    expect(buttons[1].textContent).toBe(PAUSE)
  })

  it('two instances send independent requests with correct text', async () => {
    fetchMock.mockResolvedValueOnce(makeOkResponse())
    fetchMock.mockResolvedValueOnce(makeOkResponse())

    render(
      <>
        <AudioPlayer text="First text" />
        <AudioPlayer text="Second text" />
      </>
    )

    const buttons = screen.getAllByRole('button')

    await act(async () => {
      fireEvent.click(buttons[0])
    })
    await act(async () => {
      fireEvent.click(buttons[1])
    })

    await waitFor(() => {
      expect(fetchMock).toHaveBeenCalledTimes(2)
    })

    const bodies = fetchMock.mock.calls.map((call: any[]) =>
      JSON.parse(call[1].body)
    )
    expect(bodies[0].text).toBe('First text')
    expect(bodies[1].text).toBe('Second text')
  })

  // ───────────── RE-PLAY ─────────────

  it('can re-play after audio ends', async () => {
    fetchMock.mockResolvedValue(makeOkResponse())

    render(<AudioPlayer text="Hello" />)
    const btn = screen.getByRole('button')

    // First play
    await act(async () => {
      fireEvent.click(btn)
    })
    await waitFor(() => {
      expect(screen.getByText(PAUSE)).toBeDefined()
    })

    // Audio ends
    await act(async () => {
      currentAudioMock!.onended!()
    })
    await waitFor(() => {
      expect(screen.getByText(PLAY)).toBeDefined()
    })
    expect(revokeCalls).toContain('blob:fake-url-1')

    // Second play
    await act(async () => {
      fireEvent.click(btn)
    })
    await waitFor(() => {
      expect(screen.getByText(PAUSE)).toBeDefined()
    })
    expect(fetchMock).toHaveBeenCalledTimes(2)
  })

  it('can re-play after error recovery', async () => {
    vi.useFakeTimers()

    fetchMock.mockRejectedValueOnce(new Error('fail'))

    render(<AudioPlayer text="Hello" />)
    const btn = screen.getByRole('button')

    await act(async () => {
      fireEvent.click(btn)
    })
    expect(screen.getByText(ERROR)).toBeDefined()

    act(() => {
      vi.advanceTimersByTime(2000)
    })
    expect(screen.getByText(PLAY)).toBeDefined()

    vi.useRealTimers()
    fetchMock.mockResolvedValueOnce(makeOkResponse())

    await act(async () => {
      fireEvent.click(btn)
    })
    await waitFor(() => {
      expect(screen.getByText(PAUSE)).toBeDefined()
    })
    expect(fetchMock).toHaveBeenCalledTimes(2)
  })

  // ───────────── EDGE CASES ─────────────

  it('handles long text without crashing', async () => {
    fetchMock.mockResolvedValueOnce(makeOkResponse())

    const longText = 'A'.repeat(5000)
    render(<AudioPlayer text={longText} />)

    await act(async () => {
      fireEvent.click(screen.getByRole('button'))
    })

    await waitFor(() => {
      expect(screen.getByText(PAUSE)).toBeDefined()
    })

    expect(fetchMock).toHaveBeenCalledWith(
      '/api/tts',
      expect.objectContaining({
        body: expect.stringContaining('A'.repeat(5000)),
      })
    )
  })

  it('clears audioRef on pause so a fresh Audio is created next play', async () => {
    fetchMock.mockResolvedValue(makeOkResponse())

    render(<AudioPlayer text="Hello" />)
    const btn = screen.getByRole('button')

    // Play
    await act(async () => {
      fireEvent.click(btn)
    })
    await waitFor(() => {
      expect(screen.getByText(PAUSE)).toBeDefined()
    })

    // Pause
    await act(async () => {
      fireEvent.click(btn)
    })
    expect(screen.getByText(PLAY)).toBeDefined()

    // Play again — should trigger a new fetch
    await act(async () => {
      fireEvent.click(btn)
    })
    await waitFor(() => {
      expect(screen.getByText(PAUSE)).toBeDefined()
    })
    expect(fetchMock).toHaveBeenCalledTimes(2)
  })
})
