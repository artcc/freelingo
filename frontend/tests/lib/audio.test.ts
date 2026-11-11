import { afterEach, describe, it, expect, vi } from 'vitest'
import { createAudioQueue, float32ToWav } from '@/lib/audio'

describe('float32ToWav', () => {
  it('produces a valid WAV header', () => {
    const samples = new Float32Array(100)
    const buffer = float32ToWav(samples, 16000)
    const view = new DataView(buffer)

    expect(
      String.fromCharCode(
        view.getUint8(0),
        view.getUint8(1),
        view.getUint8(2),
        view.getUint8(3)
      )
    ).toBe('RIFF')
    expect(
      String.fromCharCode(
        view.getUint8(8),
        view.getUint8(9),
        view.getUint8(10),
        view.getUint8(11)
      )
    ).toBe('WAVE')
    expect(
      String.fromCharCode(
        view.getUint8(12),
        view.getUint8(13),
        view.getUint8(14),
        view.getUint8(15)
      )
    ).toBe('fmt ')
    expect(
      String.fromCharCode(
        view.getUint8(36),
        view.getUint8(37),
        view.getUint8(38),
        view.getUint8(39)
      )
    ).toBe('data')
  })

  it('writes correct PCM format chunk', () => {
    const samples = new Float32Array(100)
    const buffer = float32ToWav(samples, 16000)
    const view = new DataView(buffer)

    expect(view.getUint32(16, true)).toBe(16)
    expect(view.getUint16(20, true)).toBe(1)
    expect(view.getUint16(22, true)).toBe(1)
    expect(view.getUint32(24, true)).toBe(16000)
    expect(view.getUint32(28, true)).toBe(32000)
    expect(view.getUint16(32, true)).toBe(2)
    expect(view.getUint16(34, true)).toBe(16)
  })

  it('calculates correct buffer size (44 byte header + data)', () => {
    const samples = new Float32Array(1000)
    const buffer = float32ToWav(samples, 16000)

    expect(buffer.byteLength).toBe(44 + 1000 * 2)
  })

  it('writes correct RIFF chunk size', () => {
    const samples = new Float32Array(100)
    const buffer = float32ToWav(samples, 16000)
    const view = new DataView(buffer)
    const dataSize = 100 * 2

    expect(view.getUint32(4, true)).toBe(36 + dataSize)
    expect(view.getUint32(40, true)).toBe(dataSize)
  })

  it('clamps samples to [-1, 1] range', () => {
    const samples = new Float32Array([2.0, -2.0, 0.5, -0.5])
    const buffer = float32ToWav(samples, 16000)
    const view = new DataView(buffer)

    const sample0 = view.getInt16(44, true)
    const sample1 = view.getInt16(46, true)
    const sample2 = view.getInt16(48, true)
    const sample3 = view.getInt16(50, true)

    expect(sample0).toBe(0x7fff)
    expect(sample1).toBe(-0x8000)
    expect(sample2).toBeGreaterThan(0)
    expect(sample3).toBeLessThan(0)
  })

  it('encodes silence as zeros', () => {
    const samples = new Float32Array(10)
    const buffer = float32ToWav(samples, 16000)
    const view = new DataView(buffer)

    for (let i = 0; i < 10; i++) {
      expect(view.getInt16(44 + i * 2, true)).toBe(0)
    }
  })

  it('handles empty sample array', () => {
    const samples = new Float32Array(0)
    const buffer = float32ToWav(samples, 16000)

    expect(buffer.byteLength).toBe(44)
  })

  it('works with different sample rates', () => {
    const samples = new Float32Array(100)
    const buffer = float32ToWav(samples, 44100)
    const view = new DataView(buffer)

    expect(view.getUint32(24, true)).toBe(44100)
    expect(view.getUint32(28, true)).toBe(88200)
  })
})

describe('createAudioQueue playback order', () => {
  afterEach(() => {
    vi.unstubAllGlobals()
  })

  function audioContext(events: string[]) {
    const sources: Array<{
      buffer: AudioBuffer | null
      connect: ReturnType<typeof vi.fn>
      start: ReturnType<typeof vi.fn>
      stop: ReturnType<typeof vi.fn>
      onended: (() => void) | null
    }> = []
    const ctx = {
      state: 'running',
      currentTime: 0,
      destination: {},
      decodeAudioData: vi.fn().mockResolvedValue({ duration: 2 }),
      createBufferSource: vi.fn(() => {
        const source = {
          buffer: null,
          connect: vi.fn(),
          start: vi.fn(() => events.push('web-start')),
          stop: vi.fn(),
          onended: null,
        }
        sources.push(source)
        return source
      }),
    }
    return { ctx, sources }
  }

  function htmlAudio(events: string[]) {
    const fallback = new EventTarget()
    const play = vi.fn(async () => {
      events.push('html-play')
    })
    const pause = vi.fn()
    vi.stubGlobal(
      'Audio',
      class {
        play = play
        pause = pause
        src = ''
        addEventListener = fallback.addEventListener.bind(fallback)
        removeEventListener = fallback.removeEventListener.bind(fallback)
      }
    )
    const createUrl = vi
      .spyOn(URL, 'createObjectURL')
      .mockReturnValue('blob:voice-test')
    const revokeUrl = vi
      .spyOn(URL, 'revokeObjectURL')
      .mockImplementation(() => {})
    return { fallback, play, pause, createUrl, revokeUrl }
  }

  it('schedules decoded chunks contiguously and stays busy until both end', async () => {
    const { ctx, sources } = audioContext([])
    const onIdle = vi.fn()
    const queue = createAudioQueue(ctx as unknown as AudioContext, onIdle)
    try {
      await queue.enqueue(new ArrayBuffer(8))
      await queue.enqueue(new ArrayBuffer(8))

      expect(sources).toHaveLength(2)
      expect(sources[0].start).toHaveBeenCalledWith(0.005)
      expect(sources[1].start).toHaveBeenCalledWith(2.005)
      expect(onIdle).not.toHaveBeenCalled()
      sources[0].onended?.()
      expect(onIdle).not.toHaveBeenCalled()
      sources[1].onended?.()
      expect(onIdle).toHaveBeenCalledTimes(1)
    } finally {
      queue.cancel()
    }
  })

  it('starts HTML fallback only after the preceding Web Audio chunk ends', async () => {
    const events: string[] = []
    const { ctx, sources } = audioContext(events)
    const { fallback, play } = htmlAudio(events)
    const queue = createAudioQueue(ctx as unknown as AudioContext)
    try {
      await queue.enqueue(new ArrayBuffer(8))
      expect(sources[0].start).toHaveBeenCalledTimes(1)
      ctx.currentTime = 0.5
      ctx.decodeAudioData.mockRejectedValueOnce(
        new DOMException('Cannot decode this chunk', 'EncodingError')
      )
      const secondChunk = queue.enqueue(new ArrayBuffer(8))
      await vi.waitFor(() =>
        expect(ctx.decodeAudioData).toHaveBeenCalledTimes(2)
      )

      ctx.currentTime = 2.005
      events.push('web-end')
      sources[0].onended?.()
      await vi.waitFor(() => expect(play).toHaveBeenCalledTimes(1))
      fallback.dispatchEvent(new Event('ended'))
      await secondChunk

      expect(events).toEqual(['web-start', 'web-end', 'html-play'])
    } finally {
      queue.cancel()
    }
  })

  it.each([
    ['WAV', float32ToWav(new Float32Array([0.5]), 24000), 'audio/wav'],
    ['MP3', new TextEncoder().encode('ID3audio').buffer, 'audio/mpeg'],
    ['short input', new ArrayBuffer(3), 'audio/mpeg'],
    [
      'non-WAVE RIFF',
      new TextEncoder().encode('RIFF0000WEBP').buffer,
      'audio/mpeg',
    ],
  ] as const)(
    'uses the correct MIME type for %s fallback',
    async (_name, bytes, type) => {
      const { ctx } = audioContext([])
      const { fallback, play, createUrl, revokeUrl } = htmlAudio([])
      ctx.decodeAudioData.mockRejectedValueOnce(new Error('Decode failed'))
      const queue = createAudioQueue(ctx as unknown as AudioContext)
      try {
        const playback = queue.enqueue(bytes)
        await vi.waitFor(() => expect(play).toHaveBeenCalledTimes(1))
        expect(createUrl.mock.calls[0][0]).toBeInstanceOf(Blob)
        expect((createUrl.mock.calls[0][0] as Blob).type).toBe(type)
        fallback.dispatchEvent(new Event('ended'))
        await playback
        expect(revokeUrl).toHaveBeenCalledWith('blob:voice-test')
      } finally {
        queue.cancel()
      }
    }
  )

  it('waits for every preceding source and finishes fallback before the next chunk', async () => {
    const events: string[] = []
    const { ctx, sources } = audioContext(events)
    const { fallback, play } = htmlAudio(events)
    const onIdle = vi.fn()
    const queue = createAudioQueue(ctx as unknown as AudioContext, onIdle)
    try {
      await queue.enqueue(new ArrayBuffer(8))
      await queue.enqueue(new ArrayBuffer(8))
      ctx.decodeAudioData.mockRejectedValueOnce(new Error('Decode failed'))
      const thirdChunk = queue.enqueue(new ArrayBuffer(8))
      const fourthChunk = queue.enqueue(new ArrayBuffer(8))
      await vi.waitFor(() =>
        expect(ctx.decodeAudioData).toHaveBeenCalledTimes(3)
      )

      sources[0].onended?.()
      await Promise.resolve()
      expect(play).not.toHaveBeenCalled()
      expect(onIdle).not.toHaveBeenCalled()
      ctx.currentTime = 4.005
      sources[1].onended?.()
      await vi.waitFor(() => expect(play).toHaveBeenCalledTimes(1))
      expect(ctx.decodeAudioData).toHaveBeenCalledTimes(3)
      expect(onIdle).not.toHaveBeenCalled()

      ctx.currentTime = 6
      fallback.dispatchEvent(new Event('ended'))
      await Promise.all([thirdChunk, fourthChunk])
      expect(sources).toHaveLength(3)
      expect(sources[2].start).toHaveBeenCalledWith(6.005)
      expect(onIdle).not.toHaveBeenCalled()
      sources[2].onended?.()
      expect(onIdle).toHaveBeenCalledTimes(1)
    } finally {
      queue.cancel()
    }
  })

  it('cancels a waiting fallback and ignores old source completion after reuse', async () => {
    const { ctx, sources } = audioContext([])
    const { play, createUrl } = htmlAudio([])
    const onIdle = vi.fn()
    const queue = createAudioQueue(ctx as unknown as AudioContext, onIdle)
    try {
      await queue.enqueue(new ArrayBuffer(8))
      ctx.decodeAudioData.mockRejectedValueOnce(new Error('Decode failed'))
      const waitingChunk = queue.enqueue(new ArrayBuffer(8))
      await vi.waitFor(() =>
        expect(ctx.decodeAudioData).toHaveBeenCalledTimes(2)
      )

      queue.cancel()
      await waitingChunk
      expect(play).not.toHaveBeenCalled()
      expect(createUrl).not.toHaveBeenCalled()
      expect(onIdle).toHaveBeenCalledTimes(1)

      await queue.enqueue(new ArrayBuffer(8))
      sources[0].onended?.()
      expect(onIdle).toHaveBeenCalledTimes(1)
      sources[1].onended?.()
      expect(onIdle).toHaveBeenCalledTimes(2)
    } finally {
      queue.cancel()
    }
  })

  it('settles cancelled HTML playback and releases its URL and event handlers', async () => {
    const { ctx, sources } = audioContext([])
    const { fallback, play, pause, revokeUrl } = htmlAudio([])
    const onIdle = vi.fn()
    const queue = createAudioQueue(ctx as unknown as AudioContext, onIdle)
    try {
      ctx.decodeAudioData.mockRejectedValueOnce(new Error('Decode failed'))
      const playingChunk = queue.enqueue(new ArrayBuffer(8))
      await vi.waitFor(() => expect(play).toHaveBeenCalledTimes(1))

      queue.cancel()
      await playingChunk
      expect(pause).toHaveBeenCalledTimes(1)
      expect(revokeUrl).toHaveBeenCalledExactlyOnceWith('blob:voice-test')
      expect(onIdle).toHaveBeenCalledTimes(1)

      await queue.enqueue(new ArrayBuffer(8))
      fallback.dispatchEvent(new Event('ended'))
      fallback.dispatchEvent(new Event('error'))
      expect(revokeUrl).toHaveBeenCalledTimes(1)
      expect(onIdle).toHaveBeenCalledTimes(1)
      sources[0].onended?.()
      expect(onIdle).toHaveBeenCalledTimes(2)
    } finally {
      queue.cancel()
    }
  })
})
