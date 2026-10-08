import { createRequire } from 'node:module'
import { StrictMode } from 'react'
import { act, cleanup, renderHook, waitFor } from '@testing-library/react/pure'
import type { RealTimeVADOptions } from '@ricky0123/vad-web'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

// These packages use CommonJS internally. Load the same module instances so the
// model factory spy applies to the real hook and MicVAD, not an ESM wrapper.
const loadCjs = createRequire(import.meta.url)
const { useMicVAD } = loadCjs(
  '@ricky0123/vad-react'
) as typeof import('@ricky0123/vad-react')
const { MicVAD } = loadCjs(
  '@ricky0123/vad-web'
) as typeof import('@ricky0123/vad-web')
const { SileroV5 } = loadCjs(
  '@ricky0123/vad-web/dist/models/v5.js'
) as typeof import('@ricky0123/vad-web/dist/models/v5')

type VadInstance = Awaited<ReturnType<typeof MicVAD.new>>
type Model = Awaited<ReturnType<typeof SileroV5.new>>

function model() {
  return {
    process: vi.fn(async () => ({ isSpeech: 0, notSpeech: 1 })),
    reset_state: vi.fn(),
    release: vi.fn(async () => {}),
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

function microphone() {
  const stop = vi.fn()
  const stream = { getTracks: () => [{ stop }] } as unknown as MediaStream
  return { stream, stop }
}

function options(
  getStream: () => Promise<MediaStream>
): Partial<RealTimeVADOptions> {
  return {
    model: 'v5',
    startOnLoad: false,
    baseAssetPath: '/vad/',
    onnxWASMBasePath: '/vad/',
    getStream,
    resumeStream: getStream,
    ortConfig: (ort) => {
      ort.env.wasm.numThreads = 1
    },
  }
}

const instances: VadInstance[] = []
const closeAudio = vi.fn(async () => {})
const addWorkletModule = vi.fn(async () => {})
const connectSource = vi.fn()

beforeEach(() => {
  instances.length = 0
  closeAudio.mockReset().mockResolvedValue(undefined)
  addWorkletModule.mockReset().mockResolvedValue(undefined)
  connectSource.mockClear()
  vi.stubGlobal('IS_REACT_ACT_ENVIRONMENT', true)
  vi.stubGlobal('fetch', vi.fn(async () => {
    throw new Error('VAD lifecycle tests must not fetch model or WASM assets')
  }))
  vi.stubGlobal('AudioContext', class {
    audioWorklet = { addModule: addWorkletModule }
    close = closeAudio
  })
  vi.stubGlobal('AudioWorkletNode', class {
    port = { postMessage: vi.fn(), onmessage: null }
    disconnect = vi.fn()
  })
  vi.stubGlobal('MediaStreamAudioSourceNode', class {
    connect = connectSource
    disconnect = vi.fn()
  })

  vi.spyOn(SileroV5, 'new').mockImplementation(async () => model())
  const createVAD = MicVAD.new
  vi.spyOn(MicVAD, 'new').mockImplementation(async (config) => {
    const vad = await createVAD(config)
    instances.push(vad)
    return vad
  })
})

afterEach(async () => {
  await act(async () => {
    cleanup()
    // Failure-path tests explicitly assert rejection; teardown must not report it twice.
    await Promise.allSettled(instances.map((vad) => vad.destroy()))
  })
  vi.restoreAllMocks()
  vi.unstubAllGlobals()
})

describe('real MicVAD lifecycle with deferred microphone acquisition', () => {
  it('releases a loaded model when destroyed before the microphone is started', async () => {
    const loadedModel = model()
    vi.mocked(SileroV5.new).mockResolvedValueOnce(loadedModel)
    const getStream = vi.fn(async () => microphone().stream)
    const vad = await MicVAD.new(options(getStream))

    expect(getStream).not.toHaveBeenCalled()
    await expect(vad.destroy()).resolves.toBeUndefined()
    expect(loadedModel.release).toHaveBeenCalledTimes(1)
    expect(closeAudio).not.toHaveBeenCalled()
  })

  it('starts, pauses, resumes and releases an initialized session without StrictMode', async () => {
    const loadedModel = model()
    vi.mocked(SileroV5.new).mockResolvedValueOnce(loadedModel)
    const firstMic = microphone()
    const secondMic = microphone()
    const getStream = vi.fn()
      .mockResolvedValueOnce(firstMic.stream)
      .mockResolvedValueOnce(secondMic.stream)
    const { result, unmount } = renderHook(() => useMicVAD(options(getStream)))

    await waitFor(() => expect(result.current.loading).toBe(false))
    expect(result.current.errored).toBe(false)
    expect(getStream).not.toHaveBeenCalled()

    await act(async () => { await result.current.start() })
    expect(result.current.listening).toBe(true)
    expect(getStream).toHaveBeenCalledTimes(1)

    await act(async () => { await result.current.pause() })
    expect(result.current.listening).toBe(false)
    expect(firstMic.stop).toHaveBeenCalledTimes(1)
    expect(loadedModel.release).not.toHaveBeenCalled()

    await act(async () => { await result.current.start() })
    expect(result.current.listening).toBe(true)
    expect(getStream).toHaveBeenCalledTimes(2)

    await act(async () => { unmount() })
    expect(secondMic.stop).toHaveBeenCalledTimes(1)
    expect(loadedModel.release).toHaveBeenCalledTimes(1)
    expect(closeAudio).toHaveBeenCalledTimes(1)
  })

  it.each(['canceled-first', 'current-first'] as const)(
    'keeps the current StrictMode initialization usable when models load %s',
    async (order) => {
      const canceled = deferred<Model>()
      const current = deferred<Model>()
      const canceledModel = model()
      const currentModel = model()
      vi.mocked(SileroV5.new)
        .mockReturnValueOnce(canceled.promise)
        .mockReturnValueOnce(current.promise)
      const getStream = vi.fn(async () => microphone().stream)
      const { result } = renderHook(() => useMicVAD(options(getStream)), {
        wrapper: StrictMode,
      })

      expect(SileroV5.new).toHaveBeenCalledTimes(2)
      expect(result.current.loading).toBe(true)
      if (order === 'canceled-first') {
        await act(async () => { canceled.resolve(canceledModel) })
        await act(async () => { current.resolve(currentModel) })
      } else {
        await act(async () => { current.resolve(currentModel) })
        expect(result.current.loading).toBe(false)
        expect(result.current.errored).toBe(false)
        await act(async () => { canceled.resolve(canceledModel) })
      }

      expect(getStream).not.toHaveBeenCalled()
      expect(result.current.loading).toBe(false)
      expect(result.current.errored).toBe(false)
      expect(canceledModel.release).toHaveBeenCalledTimes(1)
      expect(currentModel.release).not.toHaveBeenCalled()

      await act(async () => { await result.current.start() })
      expect(result.current.listening).toBe(true)
      expect(getStream).toHaveBeenCalledTimes(1)
    }
  )

  it('shares one disposal promise and releases the model only once', async () => {
    const release = deferred<void>()
    const loadedModel = model()
    loadedModel.release.mockReturnValue(release.promise)
    vi.mocked(SileroV5.new).mockResolvedValueOnce(loadedModel)
    const vad = await MicVAD.new(options(async () => microphone().stream))

    const first = vad.destroy()
    const second = vad.destroy()
    expect(second).toBe(first)
    await waitFor(() => expect(loadedModel.release).toHaveBeenCalledTimes(1))
    release.resolve()
    await Promise.all([first, second])
    await vad.destroy()
    expect(loadedModel.release).toHaveBeenCalledTimes(1)
  })

  it.each(['loading', 'ready'] as const)(
    'releases an unstarted instance when leaving while %s',
    async (state) => {
      const pending = deferred<Model>()
      const loadedModel = model()
      vi.mocked(SileroV5.new).mockReturnValueOnce(pending.promise)
      const getStream = vi.fn(async () => microphone().stream)
      const { result, unmount } = renderHook(() => useMicVAD(options(getStream)))

      if (state === 'ready') {
        await act(async () => { pending.resolve(loadedModel) })
        expect(result.current.loading).toBe(false)
      }
      await act(async () => {
        unmount()
        if (state === 'loading') pending.resolve(loadedModel)
      })

      expect(loadedModel.release).toHaveBeenCalledTimes(1)
      expect(getStream).not.toHaveBeenCalled()
      expect(closeAudio).not.toHaveBeenCalled()
    }
  )

  it('discards a canceled model failure while the current initialization is still loading', async () => {
    vi.spyOn(console, 'error').mockImplementation(() => {})
    const canceled = deferred<Model>()
    const current = deferred<Model>()
    vi.mocked(SileroV5.new)
      .mockReturnValueOnce(canceled.promise)
      .mockReturnValueOnce(current.promise)
    const getStream = vi.fn(async () => microphone().stream)
    const { result } = renderHook(() => useMicVAD(options(getStream)), {
      wrapper: StrictMode,
    })

    await act(async () => { canceled.reject(new Error('Obsolete model failure')) })
    expect(result.current.loading).toBe(true)
    expect(result.current.errored).toBe(false)
    await act(async () => { current.resolve(model()) })
    expect(result.current.loading).toBe(false)
    expect(result.current.errored).toBe(false)
    expect(getStream).not.toHaveBeenCalled()
  })

  it.each(['model', 'cleanup'] as const)(
    'ignores a late canceled %s failure after the current instance is ready',
    async (failure) => {
      vi.spyOn(console, 'error').mockImplementation(() => {})
      const canceled = deferred<Model>()
      const current = deferred<Model>()
      vi.mocked(SileroV5.new)
        .mockReturnValueOnce(canceled.promise)
        .mockReturnValueOnce(current.promise)
      const getStream = vi.fn(async () => microphone().stream)
      const { result } = renderHook(() => useMicVAD(options(getStream)), {
        wrapper: StrictMode,
      })

      await act(async () => { current.resolve(model()) })
      expect(result.current.errored).toBe(false)
      await act(async () => {
        const error = new Error('Obsolete initialization failed')
        if (failure === 'model') {
          canceled.reject(error)
        } else {
          const canceledModel = model()
          canceledModel.release.mockRejectedValue(error)
          canceled.resolve(canceledModel)
        }
      })

      expect(result.current.loading).toBe(false)
      expect(result.current.errored).toBe(false)
      await act(async () => { await result.current.start() })
      expect(result.current.listening).toBe(true)
    }
  )

  it('still exposes a genuine failure of the current model', async () => {
    vi.spyOn(console, 'error').mockImplementation(() => {})
    vi.mocked(SileroV5.new).mockRejectedValueOnce(new Error('Current model failed'))
    const getStream = vi.fn(async () => microphone().stream)
    const { result } = renderHook(() => useMicVAD(options(getStream)))

    await waitFor(() => expect(result.current.loading).toBe(false))
    expect(result.current.errored).toBe('Current model failed')
    expect(getStream).not.toHaveBeenCalled()
  })

  it('handles and reports an asynchronous cleanup rejection on unmount', async () => {
    const error = new Error('Model release failed')
    const log = vi.spyOn(console, 'error').mockImplementation(() => {})
    const loadedModel = model()
    loadedModel.release.mockRejectedValue(error)
    vi.mocked(SileroV5.new).mockResolvedValueOnce(loadedModel)
    const { result, unmount } = renderHook(() =>
      useMicVAD(options(async () => microphone().stream))
    )

    await waitFor(() => expect(result.current.loading).toBe(false))
    await act(async () => { unmount() })
    expect(log).toHaveBeenCalledWith('Failed to destroy MicVAD', error)
    expect(loadedModel.release).toHaveBeenCalledTimes(1)
  })

  it('stops a microphone acquired after disposal was requested without starting audio', async () => {
    const pending = deferred<MediaStream>()
    const mic = microphone()
    const loadedModel = model()
    vi.mocked(SileroV5.new).mockResolvedValueOnce(loadedModel)
    const getStream = vi.fn(() => pending.promise)
    const vad = await MicVAD.new(options(getStream))

    const start = vad.start()
    const disposal = vad.destroy()
    expect(loadedModel.release).not.toHaveBeenCalled()
    pending.resolve(mic.stream)
    await Promise.all([start, disposal])

    expect(mic.stop).toHaveBeenCalledTimes(1)
    expect(loadedModel.release).toHaveBeenCalledTimes(1)
    expect(addWorkletModule).not.toHaveBeenCalled()
    expect(connectSource).not.toHaveBeenCalled()
    expect(vad.listening).toBe(false)
    await vad.start()
    expect(getStream).toHaveBeenCalledTimes(1)
  })

  it('waits for a pending worklet and releases partial audio initialization', async () => {
    const pending = deferred<void>()
    addWorkletModule.mockReturnValueOnce(pending.promise)
    const mic = microphone()
    const loadedModel = model()
    vi.mocked(SileroV5.new).mockResolvedValueOnce(loadedModel)
    const vad = await MicVAD.new(options(async () => mic.stream))

    const start = vad.start()
    await waitFor(() => expect(addWorkletModule).toHaveBeenCalledTimes(1))
    const disposal = vad.destroy()
    expect(closeAudio).not.toHaveBeenCalled()
    expect(loadedModel.release).not.toHaveBeenCalled()
    pending.resolve()
    await Promise.all([start, disposal])

    expect(mic.stop).toHaveBeenCalledTimes(1)
    expect(loadedModel.release).toHaveBeenCalledTimes(1)
    expect(closeAudio).toHaveBeenCalledTimes(1)
    expect(connectSource).not.toHaveBeenCalled()
    expect(vad.listening).toBe(false)
  })

  it('releases the replacement microphone when disposal overlaps a resume', async () => {
    const pending = deferred<MediaStream>()
    const firstMic = microphone()
    const secondMic = microphone()
    const loadedModel = model()
    vi.mocked(SileroV5.new).mockResolvedValueOnce(loadedModel)
    const getStream = vi.fn()
      .mockResolvedValueOnce(firstMic.stream)
      .mockReturnValueOnce(pending.promise)
    const vad = await MicVAD.new(options(getStream))
    await vad.start()
    await vad.pause()

    const resume = vad.start()
    const disposal = vad.destroy()
    pending.resolve(secondMic.stream)
    await Promise.all([resume, disposal])

    expect(firstMic.stop).toHaveBeenCalledTimes(1)
    expect(secondMic.stop).toHaveBeenCalledTimes(1)
    expect(loadedModel.release).toHaveBeenCalledTimes(1)
    expect(closeAudio).toHaveBeenCalledTimes(1)
    expect(connectSource).toHaveBeenCalledTimes(1)
    expect(vad.listening).toBe(false)
  })

  it('closes its audio context even when model release fails', async () => {
    const loadedModel = model()
    loadedModel.release.mockRejectedValue(new Error('Model release failed'))
    vi.mocked(SileroV5.new).mockResolvedValueOnce(loadedModel)
    const mic = microphone()
    const vad = await MicVAD.new(options(async () => mic.stream))
    await vad.start()

    await expect(vad.destroy()).rejects.toThrow('Model release failed')
    expect(mic.stop).toHaveBeenCalledTimes(1)
    expect(closeAudio).toHaveBeenCalledTimes(1)
  })

  it('preserves an audio context owned by the caller', async () => {
    const vad = await MicVAD.new({
      ...options(async () => microphone().stream),
      audioContext: new AudioContext(),
    })
    await vad.start()
    await vad.destroy()
    expect(closeAudio).not.toHaveBeenCalled()
  })
})
