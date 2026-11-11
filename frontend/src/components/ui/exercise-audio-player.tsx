'use client'

import { useCallback, useLayoutEffect, useRef, useState } from 'react'
import { useTranslations } from 'next-intl'
import { apiFetch } from '@/lib/api'
import { useAuthStore } from '@/store/auth'

interface ExerciseAudioPlayerProps {
  exerciseId: number
  onFirstPlay?: () => void
  tts?: { text: string; studyPlanId: number }
}

interface Playback {
  controller: AbortController
  audio: HTMLAudioElement | null
  url: string | null
  detach: (() => void) | null
  pending: boolean
  timeout: ReturnType<typeof setTimeout> | null
}

function storedVoice() {
  try {
    return typeof window !== 'undefined'
      ? (localStorage.getItem('tts_voice') ?? undefined)
      : undefined
  } catch {
    return undefined
  }
}

export function ExerciseAudioPlayer({
  exerciseId,
  onFirstPlay,
  tts,
}: ExerciseAudioPlayerProps) {
  const t = useTranslations('listening')
  const tAudio = useTranslations('audioPlayer')
  const voice = tts ? storedVoice() : undefined
  const source = JSON.stringify([
    exerciseId,
    tts?.text,
    tts?.studyPlanId,
    voice,
  ])
  const [state, setState] = useState<
    'idle' | 'loading' | 'playing' | 'paused' | 'error'
  >('idle')
  const [progress, setProgress] = useState(0)
  const [duration, setDuration] = useState(0)
  const playbackRef = useRef<Playback | null>(null)
  const playedRef = useRef(false)
  const onFirstPlayRef = useRef(onFirstPlay)
  const sessionVersion = useAuthStore((auth) => auth.sessionVersion)
  const userId = useAuthStore((auth) => auth.user?.id)
  const contextRef = useRef<{
    source: string
    sessionVersion: number
    userId: number | undefined
  } | null>(null)

  const stopPlayback = useCallback(() => {
    const playback = playbackRef.current
    playbackRef.current = null
    if (!playback) return
    if (playback.timeout) clearTimeout(playback.timeout)
    playback.controller.abort()
    playback.detach?.()
    if (playback.audio) {
      playback.audio.pause()
      playback.audio.removeAttribute('src')
      playback.audio.load()
    }
    if (playback.url) URL.revokeObjectURL(playback.url)
  }, [])

  useLayoutEffect(() => {
    onFirstPlayRef.current = onFirstPlay
  }, [onFirstPlay])

  useLayoutEffect(() => {
    contextRef.current = { source, sessionVersion, userId }
    const reset = () => {
      stopPlayback()
      playedRef.current = false
      setState('idle')
      setProgress(0)
      setDuration(0)
    }
    reset()
    // Stop immediately on authentication changes, including before React commits.
    const unsubscribe = useAuthStore.subscribe((auth) => {
      if (auth.sessionVersion !== sessionVersion || auth.user?.id !== userId) {
        reset()
      }
    })
    return () => {
      unsubscribe()
      contextRef.current = null
      stopPlayback()
    }
  }, [source, sessionVersion, userId, stopPlayback])

  async function handlePlayPause() {
    const context = contextRef.current
    const sameContext = () => {
      const auth = useAuthStore.getState()
      return (
        context !== null &&
        contextRef.current === context &&
        context.source === source &&
        auth.sessionVersion === context.sessionVersion &&
        auth.user?.id === context.userId
      )
    }
    if (!sameContext() || playbackRef.current?.pending) return

    if (state === 'playing') {
      playbackRef.current?.audio?.pause()
      setState('paused')
      return
    }

    if (state !== 'paused' || !playbackRef.current?.audio) {
      stopPlayback()
      playbackRef.current = {
        controller: new AbortController(),
        audio: null,
        url: null,
        detach: null,
        pending: false,
        timeout: null,
      }
      setProgress(0)
      setDuration(0)
    }
    const playback = playbackRef.current
    if (!playback) return
    const current = () =>
      sameContext() &&
      playbackRef.current === playback &&
      !playback.controller.signal.aborted
    const fail = () => {
      if (!current()) return
      stopPlayback()
      setProgress(0)
      setDuration(0)
      setState('error')
    }

    playback.pending = true
    setState('loading')
    if (tts) playback.timeout = setTimeout(fail, 60_000)
    try {
      if (!playback.audio) {
        const res = await apiFetch(
          tts ? '/api/tts' : `/api/listening/audio/${exerciseId}`,
          {
            signal: playback.controller.signal,
            ...(tts
              ? {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({
                    text: tts.text,
                    study_plan_id: tts.studyPlanId,
                    voice,
                  }),
                }
              : {}),
          }
        )
        if (!current()) return
        if (!res.ok) throw new Error(`${res.status}`)
        const blob = await res.blob()
        if (!current()) return
        playback.url = URL.createObjectURL(blob)
        const audio = new Audio(playback.url)
        playback.audio = audio

        const metadata = () => {
          if (current()) setDuration(audio.duration)
        }
        const timeupdate = () => {
          if (current() && audio.duration > 0) {
            setProgress((audio.currentTime / audio.duration) * 100)
          }
        }
        const ended = () => {
          if (!current()) return
          if (tts) audio.currentTime = 0
          else stopPlayback()
          setProgress(100)
          setState(tts ? 'paused' : 'idle')
        }
        audio.addEventListener('loadedmetadata', metadata)
        audio.addEventListener('timeupdate', timeupdate)
        audio.addEventListener('ended', ended)
        audio.addEventListener('error', fail)
        playback.detach = () => {
          audio.removeEventListener('loadedmetadata', metadata)
          audio.removeEventListener('timeupdate', timeupdate)
          audio.removeEventListener('ended', ended)
          audio.removeEventListener('error', fail)
        }
      }

      const audio = playback.audio
      if (tts && audio.currentTime === 0) setProgress(0)
      await audio.play()
      if (!current()) {
        // A browser may settle play() after cleanup; stop only that old element.
        audio.pause()
        return
      }
      setState('playing')

      if (!playedRef.current) {
        playedRef.current = true
        onFirstPlayRef.current?.()
      }
    } catch {
      fail()
    } finally {
      if (playback.timeout) clearTimeout(playback.timeout)
      playback.timeout = null
      playback.pending = false
    }
  }

  function handleSeek(e: React.MouseEvent<HTMLDivElement>) {
    const rect = e.currentTarget.getBoundingClientRect()
    if (rect.width > 0) seek((e.clientX - rect.left) / rect.width)
  }

  function seek(position: number) {
    const audio = playbackRef.current?.audio
    if (!audio || !Number.isFinite(audio.duration) || audio.duration <= 0)
      return
    const ratio = Math.max(0, Math.min(1, position))
    audio.currentTime = ratio * audio.duration
    setProgress(ratio * 100)
  }

  const icon = state === 'loading' ? '◌' : state === 'playing' ? '▐▐' : '▶'
  const label = tts
    ? tAudio(state === 'playing' ? 'ariaPause' : 'listen')
    : state === 'playing'
      ? 'Pause'
      : 'Play'

  return (
    <div className="border-fl-border bg-fl-surface space-y-2 border p-4">
      <div className="flex items-center gap-4">
        <button
          onClick={handlePlayPause}
          disabled={state === 'loading'}
          aria-label={label}
          className="text-fl-fg hover:text-fl-fg-bright w-8 shrink-0 text-center font-mono text-base transition-colors disabled:opacity-40"
        >
          {icon}
        </button>

        <div
          className="bg-fl-border relative h-1.5 flex-1 cursor-pointer"
          onClick={handleSeek}
          role={tts ? 'slider' : 'progressbar'}
          tabIndex={tts ? 0 : undefined}
          aria-label={tts ? tAudio('ariaSeek') : undefined}
          onKeyDown={
            tts
              ? (event) => {
                  const positions: Record<string, number> = {
                    ArrowLeft: progress / 100 - 0.05,
                    ArrowDown: progress / 100 - 0.05,
                    ArrowRight: progress / 100 + 0.05,
                    ArrowUp: progress / 100 + 0.05,
                    Home: 0,
                    End: 1,
                  }
                  if (event.key in positions) {
                    event.preventDefault()
                    seek(positions[event.key])
                  }
                }
              : undefined
          }
          aria-valuenow={Math.round(progress)}
          aria-valuemin={0}
          aria-valuemax={100}
        >
          <div
            className="bg-fl-accent h-full transition-all"
            style={{ width: `${progress}%` }}
          />
        </div>

        {duration > 0 && (
          <span className="text-fl-label text-fl-muted-3 shrink-0 font-mono tabular-nums">
            {Math.ceil(duration)}s
          </span>
        )}
      </div>
      {state === 'error' && (
        <p className="text-fl-label font-mono text-red-500">
          {t('audioError')}
        </p>
      )}
    </div>
  )
}
