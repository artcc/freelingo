'use client'

import { useState, useEffect, useRef, useCallback } from 'react'
import { useTranslations } from 'next-intl'
import { apiFetch } from '@/lib/api'
import { useConfigStore } from '@/store/config'
import { trackBrowserEvent } from '@/lib/analytics'
import { useAuthStore } from '@/store/auth'
import { getLogger } from '@/lib/logger'
import {
  GEMINI_VOICES,
  OPENAI_VOICES,
  resolveTtsVoice,
  ttsVoiceStorageKey,
} from '@/lib/tts-voice'

const logger = getLogger('voice-preview')

export function VoiceSection({ title }: { title?: string } = {}) {
  const t = useTranslations('settings')
  const ttsProvider = useConfigStore((s) => s.ttsProvider)
  const openaiTtsVoice = useConfigStore((s) => s.openaiTtsVoice)
  const geminiTtsVoice = useConfigStore((s) => s.geminiTtsVoice)
  const configLoaded = useConfigStore((s) => s.loaded)
  const sessionVersion = useAuthStore((s) => s.sessionVersion)
  const voices: readonly string[] =
    ttsProvider === 'gemini' ? GEMINI_VOICES : OPENAI_VOICES

  const [selectedVoice, setSelectedVoice] = useState<string>('')
  const [playingVoice, setPlayingVoice] = useState<string | null>(null)
  const [loadingVoice, setLoadingVoice] = useState<string | null>(null)
  const audioRef = useRef<HTMLAudioElement | null>(null)
  const urlRef = useRef<string | null>(null)
  const controllerRef = useRef<AbortController | null>(null)

  const cleanupPreview = useCallback(() => {
    controllerRef.current?.abort()
    controllerRef.current = null
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
    const defaultVoice =
      ttsProvider === 'gemini' ? geminiTtsVoice : openaiTtsVoice
    setSelectedVoice(
      resolveTtsVoice(ttsProvider) ??
        (voices.includes(defaultVoice)
          ? defaultVoice
          : ttsProvider === 'gemini'
            ? 'female'
            : 'nova')
    )
    setPlayingVoice(null)
    setLoadingVoice(null)
    return cleanupPreview
  }, [
    ttsProvider,
    openaiTtsVoice,
    geminiTtsVoice,
    configLoaded,
    voices,
    cleanupPreview,
  ])

  useEffect(() => {
    const reset = () => {
      cleanupPreview()
      setPlayingVoice(null)
      setLoadingVoice(null)
    }
    reset()
    const unsubscribe = useAuthStore.subscribe((auth) => {
      if (auth.sessionVersion !== sessionVersion) reset()
    })
    return () => {
      unsubscribe()
      cleanupPreview()
    }
  }, [sessionVersion, cleanupPreview])

  function selectVoice(voice: string) {
    cleanupPreview()
    setPlayingVoice(null)
    setLoadingVoice(null)
    setSelectedVoice(voice)
    try {
      localStorage.setItem(ttsVoiceStorageKey(ttsProvider), voice)
    } catch (error) {
      logger.warn('Could not persist voice preference', error)
    }
    if (selectedVoice !== voice) trackBrowserEvent('voice_changed')
  }

  async function togglePreview(voice: string) {
    cleanupPreview()
    setPlayingVoice(null)
    setLoadingVoice(null)
    if (playingVoice === voice) {
      return
    }
    const controller = new AbortController()
    controllerRef.current = controller
    const analyticsSession = useAuthStore.getState().sessionVersion
    const current = () =>
      controllerRef.current === controller &&
      !controller.signal.aborted &&
      useAuthStore.getState().sessionVersion === analyticsSession
    setLoadingVoice(voice)
    try {
      const res = await apiFetch(`/api/tts/preview/${voice}`, {
        cache: 'no-store',
        signal: controller.signal,
      })
      if (!current()) return
      if (!res.ok) throw new Error(`Voice preview error ${res.status}`)
      const blob = await res.blob()
      if (!current()) return
      const url = URL.createObjectURL(blob)
      urlRef.current = url
      const audio = new Audio(url)
      audioRef.current = audio
      setPlayingVoice(voice)
      const finish = () => {
        if (!current()) return
        cleanupPreview()
        setPlayingVoice(null)
        setLoadingVoice(null)
      }
      audio.onended = finish
      audio.onerror = finish
      await audio.play()
      if (!current()) {
        audio.pause()
        return
      }
      if (audioRef.current === audio)
        trackBrowserEvent('voice_preview_played', {
          sessionVersion: analyticsSession,
        })
    } catch (error) {
      if (current()) {
        logger.warn('Voice preview failed', error)
        cleanupPreview()
        setPlayingVoice(null)
        setLoadingVoice(null)
      }
    } finally {
      if (current()) setLoadingVoice(null)
    }
  }

  if (!configLoaded || (ttsProvider !== 'openai' && ttsProvider !== 'gemini'))
    return null

  return (
    <div className="border-fl-border bg-fl-surface border p-6">
      <div className="border-fl-border mb-5 flex items-center gap-2 border-b pb-4">
        <span className="text-fl-label text-fl-muted-2">●</span>
        <span className="text-fl-label text-fl-muted-2 font-mono tracking-widest uppercase">
          {title ?? t('sectionVoice')}
        </span>
      </div>
      <p className="text-fl-hint text-fl-muted-3 mb-4 font-mono">
        {t('voiceHint')}
      </p>
      <div className="flex items-center gap-3">
        <select
          aria-label={title ?? t('sectionVoice')}
          value={selectedVoice}
          onChange={(e) => selectVoice(e.target.value)}
          className="bg-fl-bg border-fl-border text-fl-fg focus:border-fl-border-2 flex-1 appearance-none border px-4 py-3 font-mono text-sm tracking-widest uppercase transition-colors focus:outline-none"
        >
          {voices.map((voice) => (
            <option key={voice} value={voice}>
              {ttsProvider === 'gemini'
                ? t(voice === 'female' ? 'voiceFemale' : 'voiceMale')
                : voice}
            </option>
          ))}
        </select>
        <button
          type="button"
          onClick={() => void togglePreview(selectedVoice)}
          disabled={loadingVoice === selectedVoice}
          className="text-fl-muted-3 hover:text-fl-fg border-fl-border hover:border-fl-border-2 border px-4 py-3 font-mono text-xs tracking-widest whitespace-nowrap uppercase transition-colors disabled:opacity-40"
        >
          {loadingVoice === selectedVoice
            ? '...'
            : playingVoice === selectedVoice
              ? t('voiceStop')
              : t('voicePlay')}
        </button>
      </div>
    </div>
  )
}
