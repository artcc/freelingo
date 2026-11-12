import React from 'react'
import { act, cleanup, fireEvent, render, screen } from '@testing-library/react'
import { NextIntlClientProvider } from 'next-intl'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { VoiceSection } from '@/components/settings/VoiceSection'
import { useConfigStore } from '@/store/config'
import { useAuthStore } from '@/store/auth'
import es from '../../../messages/es.json'

const apiFetch = vi.hoisted(() => vi.fn())
vi.mock('@/lib/api', () => ({ apiFetch }))
vi.mock('@/lib/analytics', () => ({ trackBrowserEvent: vi.fn() }))

function deferred<T>() {
  let resolve!: (value: T) => void
  let reject!: (reason: Error) => void
  const promise = new Promise<T>((done, fail) => {
    resolve = done
    reject = fail
  })
  return { promise, resolve, reject }
}

let audios: FakeAudio[]
let playResult: Promise<void>

class FakeAudio {
  onended: (() => void) | null = null
  onerror: (() => void) | null = null
  play = vi.fn(() => playResult)
  pause = vi.fn()
  constructor() {
    audios.push(this)
  }
}

const response = () =>
  new Response('RIFFaudio', { headers: { 'Content-Type': 'audio/wav' } })

function show() {
  return render(
    <NextIntlClientProvider locale="es" messages={es}>
      <VoiceSection />
    </NextIntlClientProvider>
  )
}

async function clickPreview() {
  await act(async () => {
    fireEvent.click(screen.getByRole('button'))
  })
}

beforeEach(() => {
  useConfigStore.setState({
    ...useConfigStore.getInitialState(),
    ttsProvider: 'gemini',
    loaded: true,
  })
  localStorage.clear()
  audios = []
  playResult = Promise.resolve()
  apiFetch.mockReset().mockImplementation(async () => response())
  vi.stubGlobal('Audio', FakeAudio)
  vi.spyOn(URL, 'createObjectURL').mockReturnValue('blob:preview')
  vi.spyOn(URL, 'revokeObjectURL').mockImplementation(() => {})
})

afterEach(() => {
  cleanup()
  useConfigStore.setState(useConfigStore.getInitialState(), true)
  vi.unstubAllGlobals()
})

describe('VoiceSection', () => {
  it('does not offer previews before provider configuration is loaded', () => {
    useConfigStore.setState({ loaded: false })
    show()
    expect(screen.queryByRole('combobox')).not.toBeInTheDocument()
    expect(apiFetch).not.toHaveBeenCalled()
  })
  it('offers only translated female and male options for Gemini', () => {
    localStorage.setItem('tts_voice', 'coral')
    show()
    expect(
      screen.getAllByRole('option').map((option) => option.textContent)
    ).toEqual([es.settings.voiceFemale, es.settings.voiceMale])
    expect(
      screen.getByRole('combobox', { name: es.settings.sectionVoice })
    ).toHaveValue('female')
    expect(localStorage.getItem('tts_voice')).toBe('coral')
  })

  it('uses the configured Gemini default when storage contains an incompatible voice', () => {
    useConfigStore.setState({ geminiTtsVoice: 'male' })
    localStorage.setItem('gemini_tts_voice', 'nova')
    show()
    expect(screen.getByRole('combobox')).toHaveValue('male')
  })

  it('preserves independent preferences through provider switches', () => {
    localStorage.setItem('tts_voice', 'coral')
    show()
    fireEvent.change(screen.getByRole('combobox'), {
      target: { value: 'male' },
    })
    expect(localStorage.getItem('gemini_tts_voice')).toBe('male')
    expect(localStorage.getItem('tts_voice')).toBe('coral')

    act(() => useConfigStore.setState({ ttsProvider: 'openai' }))
    expect(screen.getByRole('combobox')).toHaveValue('coral')
    expect(screen.getAllByRole('option')).toHaveLength(9)
    fireEvent.change(screen.getByRole('combobox'), {
      target: { value: 'nova' },
    })
    expect(localStorage.getItem('tts_voice')).toBe('nova')

    act(() => useConfigStore.setState({ ttsProvider: 'local' }))
    expect(screen.queryByRole('combobox')).not.toBeInTheDocument()
    act(() => useConfigStore.setState({ ttsProvider: 'gemini' }))
    expect(screen.getByRole('combobox')).toHaveValue('male')
    act(() => useConfigStore.setState({ ttsProvider: 'openai' }))
    expect(screen.getByRole('combobox')).toHaveValue('nova')
  })

  it.each(['female', 'male'])(
    'previews %s using the existing endpoint',
    async (voice) => {
      show()
      fireEvent.change(screen.getByRole('combobox'), {
        target: { value: voice },
      })
      await clickPreview()

      expect(apiFetch).toHaveBeenCalledWith(`/api/tts/preview/${voice}`, {
        cache: 'no-store',
        signal: expect.any(AbortSignal),
      })
      expect(URL.createObjectURL).toHaveBeenCalledWith(
        expect.objectContaining({ type: 'audio/wav' })
      )
      expect(audios[0].play).toHaveBeenCalledTimes(1)
      expect(
        screen.getByRole('button', { name: es.settings.voiceStop })
      ).toBeEnabled()
      act(() => audios[0].onended?.())
      expect(URL.revokeObjectURL).toHaveBeenCalledWith('blob:preview')
      expect(
        screen.getByRole('button', { name: es.settings.voicePlay })
      ).toBeEnabled()
    }
  )

  it.each(['unmount', 'provider', 'voice', 'stop', 'session'])(
    'releases active preview resources on %s',
    async (change) => {
      const { unmount } = show()
      await clickPreview()
      const signal = apiFetch.mock.calls[0][1].signal as AbortSignal
      if (change === 'unmount') unmount()
      if (change === 'session')
        act(() => useAuthStore.getState().startSession('next-account'))
      if (change === 'provider')
        act(() => useConfigStore.setState({ ttsProvider: 'openai' }))
      if (change === 'voice')
        fireEvent.change(screen.getByRole('combobox'), {
          target: { value: 'male' },
        })
      if (change === 'stop') await clickPreview()

      expect(signal.aborted).toBe(true)
      expect(audios[0].pause).toHaveBeenCalled()
      expect(audios[0].onended).toBeNull()
      expect(audios[0].onerror).toBeNull()
      expect(URL.revokeObjectURL).toHaveBeenCalledTimes(1)
    }
  )

  describe.each(['fetch', 'blob', 'play'])('pending %s', (stage) => {
    it.each(['unmount', 'provider', 'session'])(
      'ignores a late completion after %s',
      async (change) => {
        const fetchResult = deferred<Response>()
        const blobResult = deferred<Blob>()
        const playing = deferred<void>()
        if (stage === 'fetch') apiFetch.mockReturnValueOnce(fetchResult.promise)
        if (stage === 'blob') {
          const res = response()
          vi.spyOn(res, 'blob').mockReturnValueOnce(blobResult.promise)
          apiFetch.mockResolvedValueOnce(res)
        }
        if (stage === 'play') playResult = playing.promise
        const { unmount } = show()
        await clickPreview()
        const signal = apiFetch.mock.calls[0][1].signal as AbortSignal
        if (change === 'unmount') unmount()
        if (change === 'provider')
          act(() => useConfigStore.setState({ ttsProvider: 'openai' }))
        if (change === 'session')
          act(() => useAuthStore.getState().startSession('next-account'))

        await act(async () => {
          fetchResult.resolve(response())
          blobResult.resolve(new Blob(['audio'], { type: 'audio/wav' }))
          playing.resolve()
        })

        expect(signal.aborted).toBe(true)
        if (stage === 'play') {
          expect(audios[0].pause).toHaveBeenCalled()
          expect(URL.revokeObjectURL).toHaveBeenCalledTimes(1)
        } else {
          expect(URL.createObjectURL).not.toHaveBeenCalled()
          expect(audios).toHaveLength(0)
        }
        if (change === 'provider') {
          expect(screen.getByRole('combobox')).toHaveValue('nova')
          expect(
            screen.getByRole('button', { name: es.settings.voicePlay })
          ).toBeEnabled()
        }
      }
    )
  })

  it('does not let an obsolete response clear the next preview loading state', async () => {
    const first = deferred<Response>()
    const second = deferred<Response>()
    apiFetch
      .mockReturnValueOnce(first.promise)
      .mockReturnValueOnce(second.promise)
    show()
    await clickPreview()
    fireEvent.change(screen.getByRole('combobox'), {
      target: { value: 'male' },
    })
    await clickPreview()
    await act(async () => first.resolve(response()))
    expect(screen.getByRole('button')).toBeDisabled()
    expect(audios).toHaveLength(0)
    await act(async () => second.resolve(response()))
    expect(audios).toHaveLength(1)
    expect(
      screen.getByRole('button', { name: es.settings.voiceStop })
    ).toBeEnabled()
  })

  it('releases the URL when play fails and permits retry', async () => {
    vi.spyOn(console, 'warn').mockImplementation(() => {})
    const playing = deferred<void>()
    playResult = playing.promise
    show()
    await clickPreview()
    await act(async () => playing.reject(new Error('Playback blocked')))
    expect(URL.revokeObjectURL).toHaveBeenCalledTimes(1)
    expect(
      screen.getByRole('button', { name: es.settings.voicePlay })
    ).toBeEnabled()
    playResult = Promise.resolve()
    await clickPreview()
    expect(audios).toHaveLength(2)
  })
})
