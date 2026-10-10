'use client'

import { useCallback, useEffect, useRef, useState } from 'react'
import { Loader2, Square, Volume2, RotateCcw } from 'lucide-react'
import { useTranslations } from 'next-intl'
import { useAuthStore } from '@/store/auth'
import { getLogger } from '@/lib/logger'
import { trackBrowserEvent } from '@/lib/analytics'

const TTS_TIMEOUT_MS = 15_000
const ttsLogger = getLogger('tts')

interface AudioPlayerProps {
  text: string
  voice?: string
  studyPlanId?: number
  conversationId?: number
  size?: 'sm' | 'md'
  className?: string
  /** Custom audio endpoint; uses GET unless audioMethod is overridden. */
  audioUrl?: string
  audioMethod?: 'GET' | 'POST'
  onStateChange?: (state: PlayerState) => void
  timeoutMs?: number
  icon?: boolean
  listenLabel?: string
}

export type PlayerState = 'idle' | 'loading' | 'playing' | 'error'

function storedVoice() {
  try {
    return typeof window !== 'undefined'
      ? (localStorage.getItem('tts_voice') ?? undefined)
      : undefined
  } catch {
    return undefined
  }
}

export function AudioPlayer({
  text,
  voice,
  studyPlanId,
  conversationId,
  size = 'sm',
  className = '',
  audioUrl,
  audioMethod = audioUrl ? 'GET' : 'POST',
  onStateChange,
  timeoutMs = TTS_TIMEOUT_MS,
  icon = false,
  listenLabel,
}: AudioPlayerProps) {
  const [state, setState] = useState<PlayerState>('idle')
  const audioRef = useRef<HTMLAudioElement | null>(null)
  const controllerRef = useRef<AbortController | null>(null)
  const urlRef = useRef<string | null>(null)
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null)
  const recoveryRef = useRef<ReturnType<typeof setTimeout> | null>(null)
  const accessToken = useAuthStore((s) => s.accessToken)
  const t = useTranslations('audioPlayer')

  // Resolve voice: explicit prop > user localStorage preference > backend default
  const resolvedVoice = voice ?? storedVoice()

  const releaseAudio = useCallback(() => {
    if (audioRef.current) {
      audioRef.current.onended = null
      audioRef.current.onerror = null
      audioRef.current.pause()
      audioRef.current = null
    }
    if (urlRef.current) URL.revokeObjectURL(urlRef.current)
    urlRef.current = null
  }, [])

  useEffect(() => {
    setState('idle')
    return () => {
      controllerRef.current?.abort()
      controllerRef.current = null
      if (timeoutRef.current) clearTimeout(timeoutRef.current)
      if (recoveryRef.current) clearTimeout(recoveryRef.current)
      releaseAudio()
    }
  }, [
    text,
    audioUrl,
    audioMethod,
    resolvedVoice,
    studyPlanId,
    conversationId,
    releaseAudio,
  ])

  useEffect(() => {
    onStateChange?.(state)
  }, [state, onStateChange])

  async function handleClick() {
    if (state === 'loading') return

    if (state === 'playing') {
      controllerRef.current?.abort()
      releaseAudio()
      setState('idle')
      return
    }

    setState('loading')
    if (recoveryRef.current) clearTimeout(recoveryRef.current)
    recoveryRef.current = null
    controllerRef.current?.abort()
    const controller = new AbortController()
    const analyticsSession = useAuthStore.getState().sessionVersion
    const analyticsPath = window.location.pathname
    controllerRef.current = controller
    const timeoutId = setTimeout(() => controller.abort(), timeoutMs)
    timeoutRef.current = timeoutId
    let failed = false
    const showError = () => {
      if (failed || controllerRef.current !== controller) return
      failed = true
      clearTimeout(timeoutId)
      releaseAudio()
      setState('error')
      recoveryRef.current = setTimeout(() => {
        if (controllerRef.current !== controller) return
        recoveryRef.current = null
        setState('idle')
      }, 2000)
    }
    try {
      const traceId = `tts-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`
      const t0 = performance.now()

      const fetchStart = performance.now()
      const res = await fetch(
        audioUrl ?? '/api/tts',
        audioMethod === 'GET'
          ? {
              headers: {
                ...(accessToken
                  ? { Authorization: `Bearer ${accessToken}` }
                  : {}),
              },
              credentials: 'include' as RequestCredentials,
              cache: 'no-store',
              signal: controller.signal,
            }
          : {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'X-TTS-Trace-ID': traceId,
                ...(accessToken
                  ? { Authorization: `Bearer ${accessToken}` }
                  : {}),
              },
              body: JSON.stringify({
                text,
                voice: resolvedVoice,
                study_plan_id: studyPlanId,
                conversation_id: conversationId,
              }),
              signal: controller.signal,
            }
      )
      const fetchMs = performance.now() - fetchStart
      if (!res.ok) throw new Error(`TTS error ${res.status}`)

      const blobStart = performance.now()
      const blob = await res.blob()
      clearTimeout(timeoutId)
      if (controller.signal.aborted || controllerRef.current !== controller)
        return
      const blobMs = performance.now() - blobStart

      const url = URL.createObjectURL(blob)
      urlRef.current = url
      const audio = new Audio(url)
      audioRef.current = audio

      audio.onended = () => {
        if (controllerRef.current !== controller || controller.signal.aborted)
          return
        releaseAudio()
        setState('idle')
      }
      audio.onerror = showError

      const playStart = performance.now()
      await audio.play()
      if (controller.signal.aborted || controllerRef.current !== controller)
        return
      if (audioRef.current !== audio) return
      setState('playing')
      if (analyticsPath === '/phrasebook')
        trackBrowserEvent('phrasebook_audio_played', {
          sessionVersion: analyticsSession,
        })
      else if (
        analyticsPath === '/flashcards' ||
        analyticsPath === '/flashcards/vocabulary'
      )
        trackBrowserEvent('vocabulary_audio_played', {
          sessionVersion: analyticsSession,
        })
      const playMs = performance.now() - playStart
      const totalMs = performance.now() - t0

      const backendSynthMs = res.headers.get('X-TTS-Backend-Synth-Ms')
      const backendTotalMs = res.headers.get('X-TTS-Backend-Total-Ms')
      const proxyFetchMs = res.headers.get('X-TTS-Proxy-Fetch-Ms')
      const proxyBufferMs = res.headers.get('X-TTS-Proxy-Buffer-Ms')
      const proxyTotalMs = res.headers.get('X-TTS-Proxy-Total-Ms')
      const responseTraceId = res.headers.get('X-TTS-Trace-ID') || traceId

      // TTS latency metrics — only logged in development
      if (process.env.NODE_ENV === 'development') {
        ttsLogger.info('tts-metrics', {
          traceId: responseTraceId,
          textLength: text.length,
          blobBytes: blob.size,
          client: {
            fetchMs: Number(fetchMs.toFixed(1)),
            blobMs: Number(blobMs.toFixed(1)),
            playMs: Number(playMs.toFixed(1)),
            totalMs: Number(totalMs.toFixed(1)),
          },
          proxy: {
            fetchMs: proxyFetchMs ? Number(proxyFetchMs) : null,
            bufferMs: proxyBufferMs ? Number(proxyBufferMs) : null,
            totalMs: proxyTotalMs ? Number(proxyTotalMs) : null,
          },
          backend: {
            synthMs: backendSynthMs ? Number(backendSynthMs) : null,
            totalMs: backendTotalMs ? Number(backendTotalMs) : null,
          },
        })
      }
    } catch {
      clearTimeout(timeoutId)
      showError()
    }
  }

  const sizeClass =
    size === 'sm' ? 'px-2 py-1 text-fl-hint' : 'px-3 py-2 text-xs'

  const label =
    state === 'loading'
      ? '...'
      : state === 'playing'
        ? '■'
        : state === 'error'
          ? '✕'
          : '▶'

  const colorClass =
    state === 'playing'
      ? 'border-fl-border-2 text-fl-fg'
      : state === 'loading'
        ? 'border-fl-border text-fl-muted-3 animate-pulse'
        : state === 'error'
          ? 'border-fl-error/40 text-fl-error-fg'
          : 'border-fl-border text-fl-muted-2 hover:border-fl-border-2 hover:text-fl-fg'

  return (
    <button
      type="button"
      onClick={handleClick}
      title={state === 'playing' ? t('stop') : (listenLabel ?? t('listen'))}
      aria-label={
        state === 'playing' ? t('ariaStop') : (listenLabel ?? t('ariaListen'))
      }
      aria-busy={state === 'loading'}
      className={`border font-mono tracking-widest uppercase transition-colors ${colorClass} ${sizeClass} ${className}`}
    >
      {icon ? (
        state === 'loading' ? (
          <Loader2
            className="h-4 w-4 motion-safe:animate-spin"
            aria-hidden="true"
          />
        ) : state === 'playing' ? (
          <Square className="h-4 w-4" aria-hidden="true" />
        ) : state === 'error' ? (
          <RotateCcw className="h-4 w-4" aria-hidden="true" />
        ) : (
          <Volume2 className="h-4 w-4" aria-hidden="true" />
        )
      ) : (
        label
      )}
    </button>
  )
}
