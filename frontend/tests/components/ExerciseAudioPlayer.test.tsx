import { act, cleanup, fireEvent, render, screen } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

import { ExerciseAudioPlayer } from '@/components/ui/exercise-audio-player'
import { useAuthStore, type User } from '@/store/auth'

const apiFetch = vi.hoisted(() => vi.fn())
vi.mock('@/lib/api', () => ({ apiFetch }))
vi.mock('next-intl', () => ({
  useTranslations: () => (key: string) => key,
}))

const user = {
  id: 1,
  username: 'learner',
  displayName: 'Learner',
  role: 'user',
  conversation_max_duration: 300,
  conversation_inactivity_timeout: 30,
} satisfies User

function deferred<T>() {
  let resolve!: (value: T) => void
  let reject!: (error: Error) => void
  const promise = new Promise<T>((done, fail) => {
    resolve = done
    reject = fail
  })
  return { promise, resolve, reject }
}

const blob = () => new Blob(['audio'], { type: 'audio/mpeg' })
const response = () => new Response(blob())
let audios: FakeAudio[]
let playResults: Array<() => Promise<void>>

class FakeAudio extends EventTarget {
  duration = 100
  currentTime = 0
  play = vi.fn(() => playResults.shift()?.() ?? Promise.resolve())
  pause = vi.fn()
  load = vi.fn()
  removeAttribute = vi.fn()
}

async function play() {
  await act(async () => {
    fireEvent.click(screen.getByRole('button', { name: 'Play' }))
  })
}

function expectReleased(audio: FakeAudio, url: string) {
  expect(audio.pause).toHaveBeenCalled()
  expect(audio.removeAttribute).toHaveBeenCalledWith('src')
  expect(audio.load).toHaveBeenCalledTimes(1)
  expect(URL.revokeObjectURL).toHaveBeenCalledWith(url)
}

beforeEach(() => {
  audios = []
  playResults = []
  apiFetch.mockReset().mockImplementation(async () => response())
  useAuthStore.setState({ user, sessionVersion: 1, accessToken: 'first' })
  vi.stubGlobal(
    'Audio',
    vi.fn(function () {
      const audio = new FakeAudio()
      audios.push(audio)
      return audio
    })
  )
  let urlId = 0
  vi.spyOn(URL, 'createObjectURL').mockImplementation(() => `blob:${++urlId}`)
  vi.spyOn(URL, 'revokeObjectURL').mockImplementation(() => {})
})

afterEach(() => {
  cleanup()
  useAuthStore.setState(useAuthStore.getInitialState(), true)
  vi.unstubAllGlobals()
})

describe('ExerciseAudioPlayer lifecycle', () => {
  describe.each(['fetch', 'blob', 'play'] as const)('pending %s', (stage) => {
    it.each(['unmount', 'exercise', 'session', 'logout'])(
      'cancels on %s and ignores completion after cancellation',
      async (change) => {
        const fetchResult = deferred<Response>()
        const blobResult = deferred<Blob>()
        const playResult = deferred<void>()
        const firstResponse = response()
        const readBlob = vi.spyOn(firstResponse, 'blob')
        if (stage === 'fetch') apiFetch.mockReturnValueOnce(fetchResult.promise)
        if (stage === 'blob') {
          readBlob.mockReturnValueOnce(blobResult.promise)
          apiFetch.mockResolvedValueOnce(firstResponse)
        }
        if (stage === 'play') playResults.push(() => playResult.promise)
        const onFirstPlay = vi.fn()
        const { unmount, rerender } = render(
          <ExerciseAudioPlayer exerciseId={42} onFirstPlay={onFirstPlay} />
        )
        await play()
        expect(screen.getByRole('button')).toBeDisabled()
        const signal = apiFetch.mock.calls[0][1].signal as AbortSignal
        if (change === 'unmount') unmount()
        if (change === 'exercise')
          rerender(
            <ExerciseAudioPlayer exerciseId={43} onFirstPlay={onFirstPlay} />
          )
        if (change === 'session')
          act(() => useAuthStore.getState().startSession('second'))
        if (change === 'logout') act(() => useAuthStore.getState().logout())
        expect(signal.aborted).toBe(true)
        if (stage === 'play') expectReleased(audios[0], 'blob:1')

        await act(async () => {
          if (stage === 'fetch') fetchResult.resolve(firstResponse)
          if (stage === 'blob') blobResult.resolve(blob())
          if (stage === 'play') playResult.resolve()
        })
        expect(onFirstPlay).not.toHaveBeenCalled()
        if (stage === 'fetch') expect(readBlob).not.toHaveBeenCalled()
        if (stage !== 'play') {
          expect(Audio).not.toHaveBeenCalled()
          expect(URL.createObjectURL).not.toHaveBeenCalled()
        } else {
          expect(audios[0].play).toHaveBeenCalledTimes(1)
          expect(audios[0].pause).toHaveBeenCalledTimes(2)
        }
        expect(screen.queryByText('audioError')).not.toBeInTheDocument()
        if (change !== 'unmount') {
          expect(screen.getByRole('button', { name: 'Play' })).toBeEnabled()
          expect(screen.getByRole('progressbar')).toHaveAttribute(
            'aria-valuenow',
            '0'
          )
        }
      }
    )
  })

  it('preserves pause, resume, seek and replay without repeating the first-play signal', async () => {
    const onFirstPlay = vi.fn()
    const { unmount } = render(
      <ExerciseAudioPlayer exerciseId={42} onFirstPlay={onFirstPlay} />
    )
    await play()
    expect(apiFetch).toHaveBeenCalledExactlyOnceWith('/api/listening/audio/42', {
      signal: expect.any(AbortSignal),
    })
    expect(onFirstPlay).toHaveBeenCalledTimes(1)
    const audio = audios[0]
    act(() => {
      audio.dispatchEvent(new Event('loadedmetadata'))
      audio.currentTime = 30
      audio.dispatchEvent(new Event('timeupdate'))
    })
    expect(screen.getByText('100s')).toBeVisible()
    const progress = screen.getByRole('progressbar')
    expect(progress).toHaveAttribute('aria-valuenow', '30')
    vi.spyOn(progress, 'getBoundingClientRect').mockReturnValue({
      left: 10,
      width: 100,
    } as DOMRect)
    fireEvent.click(progress, { clientX: 60 })
    expect(audio.currentTime).toBe(50)
    expect(progress).toHaveAttribute('aria-valuenow', '50')

    fireEvent.click(screen.getByRole('button', { name: 'Pause' }))
    expect(audio.pause).toHaveBeenCalledTimes(1)
    expect(URL.revokeObjectURL).not.toHaveBeenCalled()
    await play()
    expect(audio.play).toHaveBeenCalledTimes(2)
    expect(apiFetch).toHaveBeenCalledTimes(1)
    expect(onFirstPlay).toHaveBeenCalledTimes(1)
    act(() => audio.dispatchEvent(new Event('ended')))
    expectReleased(audio, 'blob:1')
    expect(progress).toHaveAttribute('aria-valuenow', '100')

    await play()
    expect(apiFetch).toHaveBeenCalledTimes(2)
    expect(audios).toHaveLength(2)
    expect(onFirstPlay).toHaveBeenCalledTimes(1)
    expect(progress).toHaveAttribute('aria-valuenow', '0')
    expect(screen.queryByText('100s')).not.toBeInTheDocument()
    unmount()
    expectReleased(audios[1], 'blob:2')
    expect(URL.revokeObjectURL).toHaveBeenCalledTimes(2)
  })

  it('resets playback, progress and first-play tracking for a different exercise', async () => {
    const firstCallback = vi.fn()
    const nextCallback = vi.fn()
    const { rerender } = render(
      <ExerciseAudioPlayer exerciseId={42} onFirstPlay={firstCallback} />
    )
    await play()
    const oldAudio = audios[0]
    act(() => {
      oldAudio.dispatchEvent(new Event('loadedmetadata'))
      oldAudio.currentTime = 60
      oldAudio.dispatchEvent(new Event('timeupdate'))
    })
    rerender(
      <ExerciseAudioPlayer exerciseId={43} onFirstPlay={nextCallback} />
    )
    expectReleased(oldAudio, 'blob:1')
    expect(screen.getByRole('button', { name: 'Play' })).toBeEnabled()
    expect(screen.queryByText('100s')).not.toBeInTheDocument()
    expect(screen.getByRole('progressbar')).toHaveAttribute('aria-valuenow', '0')
    await play()
    expect(apiFetch.mock.calls[1][0]).toBe('/api/listening/audio/43')
    expect(firstCallback).toHaveBeenCalledTimes(1)
    expect(nextCallback).toHaveBeenCalledTimes(1)
    act(() => {
      oldAudio.dispatchEvent(new Event('error'))
      oldAudio.dispatchEvent(new Event('ended'))
      oldAudio.dispatchEvent(new Event('loadedmetadata'))
      oldAudio.dispatchEvent(new Event('timeupdate'))
    })
    expect(screen.getByRole('button', { name: 'Pause' })).toBeEnabled()
    expect(screen.queryByText('audioError')).not.toBeInTheDocument()
    expect(screen.getByRole('progressbar')).toHaveAttribute('aria-valuenow', '0')
    expect(audios[1].pause).not.toHaveBeenCalled()
  })

  it.each(['resolve', 'reject'])(
    'does not interrupt newer playback when an obsolete play promise %ss',
    async (settlement) => {
      const oldPlay = deferred<void>()
      playResults.push(() => oldPlay.promise)
      const onFirstPlay = vi.fn()
      const { rerender } = render(
        <ExerciseAudioPlayer exerciseId={42} onFirstPlay={onFirstPlay} />
      )
      await play()
      rerender(
        <ExerciseAudioPlayer exerciseId={43} onFirstPlay={onFirstPlay} />
      )
      await play()
      await act(async () => {
        if (settlement === 'resolve') oldPlay.resolve()
        else oldPlay.reject(new Error('Old playback failed'))
      })
      expect(screen.getByRole('button', { name: 'Pause' })).toBeEnabled()
      expect(screen.queryByText('audioError')).not.toBeInTheDocument()
      expect(audios[1].pause).not.toHaveBeenCalled()
      expect(onFirstPlay).toHaveBeenCalledTimes(1)
      expect(URL.revokeObjectURL).toHaveBeenCalledTimes(1)
    }
  )

  it.each(['http', 'network', 'play', 'resume', 'event'])(
    'releases failed %s resources and allows retry',
    async (failure) => {
      const onFirstPlay = vi.fn()
      if (failure === 'http')
        apiFetch.mockResolvedValueOnce(new Response(null, { status: 503 }))
      if (failure === 'network')
        apiFetch.mockRejectedValueOnce(new TypeError('Network failed'))
      if (failure === 'play') {
        playResults.push(() => Promise.reject(new Error('Playback failed')))
      }
      render(<ExerciseAudioPlayer exerciseId={42} onFirstPlay={onFirstPlay} />)
      await play()
      if (failure === 'resume') {
        fireEvent.click(screen.getByRole('button', { name: 'Pause' }))
        audios[0].play.mockRejectedValueOnce(new Error('Resume failed'))
        await play()
      }
      if (failure === 'event')
        act(() => audios[0].dispatchEvent(new Event('error')))
      expect(screen.getByText('audioError')).toBeVisible()
      if (audios.length) expectReleased(audios[0], 'blob:1')
      await play()
      expect(screen.getByRole('button', { name: 'Pause' })).toBeEnabled()
      expect(screen.queryByText('audioError')).not.toBeInTheDocument()
      expect(onFirstPlay).toHaveBeenCalledTimes(1)
    }
  )

  it('ignores a pending play rejection after a media error and successful retry', async () => {
    const failedPlay = deferred<void>()
    playResults.push(() => failedPlay.promise)
    const onFirstPlay = vi.fn()
    render(<ExerciseAudioPlayer exerciseId={42} onFirstPlay={onFirstPlay} />)
    await play()
    act(() => audios[0].dispatchEvent(new Event('error')))
    expectReleased(audios[0], 'blob:1')
    await play()
    await act(async () => failedPlay.reject(new Error('Late rejection')))
    expect(screen.getByRole('button', { name: 'Pause' })).toBeEnabled()
    expect(audios[1].pause).not.toHaveBeenCalled()
    expect(onFirstPlay).toHaveBeenCalledTimes(1)
  })

  it('does not restart audio on token rotation or callback changes', async () => {
    const pending = deferred<void>()
    playResults.push(() => pending.promise)
    const firstCallback = vi.fn()
    const latestCallback = vi.fn()
    const { rerender } = render(
      <ExerciseAudioPlayer exerciseId={42} onFirstPlay={firstCallback} />
    )
    await play()
    act(() => useAuthStore.getState().setTokens('rotated'))
    rerender(
      <ExerciseAudioPlayer exerciseId={42} onFirstPlay={latestCallback} />
    )
    expect(apiFetch.mock.calls[0][1].signal.aborted).toBe(false)
    await act(async () => pending.resolve())
    expect(firstCallback).not.toHaveBeenCalled()
    expect(latestCallback).toHaveBeenCalledTimes(1)
    expect(audios[0].pause).not.toHaveBeenCalled()
    expect(screen.getByRole('button', { name: 'Pause' })).toBeEnabled()
  })

  it.each(['playing', 'paused'])(
    'releases %s audio immediately when the account changes',
    async (state) => {
      const onFirstPlay = vi.fn()
      render(<ExerciseAudioPlayer exerciseId={42} onFirstPlay={onFirstPlay} />)
      await play()
      const oldAudio = audios[0]
      if (state === 'paused')
        fireEvent.click(screen.getByRole('button', { name: 'Pause' }))
      act(() => {
        useAuthStore.getState().startSession('other-account')
        // Cleanup happens at the store boundary, not in a later React effect.
        expectReleased(oldAudio, 'blob:1')
        useAuthStore.getState().setUser({ ...user, id: 2 })
      })
      expect(screen.getByRole('button', { name: 'Play' })).toBeEnabled()
      await play()
      expect(onFirstPlay).toHaveBeenCalledTimes(2)
      expect(audios[1].play).toHaveBeenCalledTimes(1)
      expect(audios[1].pause).not.toHaveBeenCalled()
    }
  )

  it('prevents overlapping resume calls and cancels a pending resume on unmount', async () => {
    const { unmount } = render(<ExerciseAudioPlayer exerciseId={42} />)
    await play()
    fireEvent.click(screen.getByRole('button', { name: 'Pause' }))
    const pending = deferred<void>()
    audios[0].play.mockReturnValueOnce(pending.promise)
    const button = screen.getByRole('button', { name: 'Play' })
    act(() => {
      fireEvent.click(button)
      fireEvent.click(button)
    })
    expect(button).toBeDisabled()
    expect(audios[0].play).toHaveBeenCalledTimes(2)
    expect(apiFetch).toHaveBeenCalledTimes(1)
    unmount()
    expectReleased(audios[0], 'blob:1')
    await act(async () => pending.resolve())
    expect(audios[0].pause).toHaveBeenCalledTimes(3)
  })
})
