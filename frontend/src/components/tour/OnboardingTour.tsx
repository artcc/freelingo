'use client'

import { useState, useEffect, useCallback, useId, useRef } from 'react'
import { useLocale, useTranslations } from 'next-intl'
import {
  ArrowLeft,
  ArrowRight,
  BookOpen,
  Check,
  Gamepad2,
  Headphones,
  Layers,
  MessageSquare,
  Mic,
  Search,
  Shuffle,
  Sparkles,
} from 'lucide-react'
import LinguAvatar, {
  type LinguAnimation,
} from '@/components/lingu/LinguAvatar'
import { AudioPlayer, type PlayerState } from '@/components/ui/AudioPlayer'
import { useConfigStore } from '@/store/config'

const STORAGE_KEY = 'fl_tour_done'
const STEPS = [
  { id: 'step1', icon: Sparkles, gesture: 'saludo' },
  { id: 'step2', icon: BookOpen },
  { id: 'step3', icon: MessageSquare, premium: true },
  { id: 'step4', icon: Layers },
  { id: 'step5', icon: Headphones, premium: true },
  { id: 'step6', icon: Gamepad2, gesture: 'animando' },
  { id: 'step7', icon: Check, gesture: 'celebracion' },
] as const

export default function OnboardingTour() {
  const t = useTranslations('tour')
  const tNav = useTranslations('nav')
  const tGames = useTranslations('games')
  const locale = useLocale()
  const stripeEnabled = useConfigStore((s) => s.stripeEnabled)
  const [visible, setVisible] = useState(false)
  const [step, setStep] = useState(0)
  const [animation, setAnimation] = useState<LinguAnimation>('saludo')
  const [audioState, setAudioState] = useState<PlayerState>('idle')
  const [voice, setVoice] = useState<string | null>(null)
  const visited = useRef(new Set([0]))
  const dialogRef = useRef<HTMLDialogElement>(null)
  const titleRef = useRef<HTMLHeadingElement>(null)
  const titleId = useId()
  const descriptionId = useId()

  useEffect(() => {
    try {
      setVisible(!localStorage.getItem(STORAGE_KEY))
      setVoice(localStorage.getItem('tts_voice'))
    } catch {
      setVisible(true)
    }
  }, [])

  const dismiss = useCallback(() => {
    try {
      localStorage.setItem(STORAGE_KEY, '1')
    } catch {
      // The tour must remain dismissible when browser storage is unavailable.
    }
    setVisible(false)
  }, [])

  useEffect(() => {
    if (!visible) return
    const dialog = dialogRef.current
    const opener = document.activeElement as HTMLElement | null
    const previousOverflow = document.body.style.overflow
    dialog?.showModal()
    document.body.style.overflow = 'hidden'
    titleRef.current?.focus()
    return () => {
      dialog?.close()
      document.body.style.overflow = previousOverflow
      opener?.focus()
    }
  }, [visible])

  useEffect(() => {
    if (visible) titleRef.current?.focus()
  }, [step, visible])

  const onAudioState = useCallback((state: PlayerState) => {
    setAudioState(state)
    setAnimation((current) =>
      state === 'playing'
        ? 'hablando'
        : current === 'hablando'
          ? 'reposo'
          : current
    )
  }, [])
  const onGestureFinished = useCallback(() => setAnimation('reposo'), [])

  function goTo(next: number) {
    if (next < 0 || next >= STEPS.length) return
    const destination = STEPS[next]
    const gesture = 'gesture' in destination ? destination.gesture : 'reposo'
    setAnimation(visited.current.has(next) ? 'reposo' : gesture)
    visited.current.add(next)
    setAudioState('idle')
    setStep(next)
  }

  if (!visible) return null

  const current = STEPS[step]
  const Icon = current.icon
  const audioUrl = `/api/tts/tour/${locale}/${current.id}`
  const examples =
    step === 2
      ? [
          { icon: MessageSquare, label: tNav('tutor') },
          { icon: Mic, label: tNav('conversation') },
        ]
      : step === 4
        ? [
            { icon: Headphones, label: tNav('listening') },
            { icon: BookOpen, label: tNav('reading') },
          ]
        : step === 5
          ? [
              { icon: Search, label: tGames('detectiveTitle') },
              { icon: Shuffle, label: tGames('sentenceOrderTitle') },
              { icon: Layers, label: tGames('vocabularyPairsTitle') },
            ]
          : []

  return (
    <dialog
      ref={dialogRef}
      aria-labelledby={titleId}
      aria-describedby={descriptionId}
      className="border-fl-border bg-fl-surface text-fl-fg backdrop:bg-fl-bg/80 m-auto max-h-[calc(100dvh-2rem)] w-[calc(100%-2rem)] max-w-3xl overflow-y-auto border p-0 shadow-2xl backdrop:backdrop-blur-sm"
      onCancel={(event) => {
        event.preventDefault()
        dismiss()
      }}
      onClick={(event) => {
        if (event.target === event.currentTarget) dismiss()
      }}
    >
      <div>
        <div className="border-fl-border flex items-center justify-between gap-4 border-b px-5 py-4 md:px-8">
          <span className="font-code text-sm font-bold tracking-widest uppercase">
            FreeLingo
          </span>
          <div className="flex items-center gap-4">
            <span
              className="text-fl-muted-2 font-code text-xs tabular-nums"
              aria-live="polite"
            >
              {t('progress', { current: step + 1, total: STEPS.length })}
            </span>
            <button
              type="button"
              onClick={dismiss}
              className="text-fl-muted-2 hover:text-fl-fg min-h-10 text-sm underline-offset-4 hover:underline"
            >
              {t('skip')}
            </button>
          </div>
        </div>

        <div className="grid items-center gap-3 px-6 py-5 md:min-h-[390px] md:grid-cols-[240px_1fr] md:gap-8 md:px-8 md:py-8">
          <LinguAvatar animation={animation} onFinished={onGestureFinished} />
          <div className="min-w-0 space-y-4">
            <p className="text-fl-accent flex items-center gap-2 text-xs font-semibold tracking-widest uppercase">
              <Icon className="h-4 w-4 shrink-0" aria-hidden="true" />
              {t(`${current.id}.label`)}
              {stripeEnabled && 'premium' in current && (
                <span aria-label="Premium">★</span>
              )}
            </p>
            <h2
              id={titleId}
              ref={titleRef}
              tabIndex={-1}
              className="text-xl font-semibold tracking-tight outline-none md:text-2xl"
            >
              {t(`${current.id}.title`)}
            </h2>
            <div className="flex items-start gap-3">
              <p
                id={descriptionId}
                className="text-fl-muted-1 flex-1 text-base leading-relaxed"
              >
                {t(`${current.id}.desc`)}
              </p>
              <AudioPlayer
                key={`${locale}:${current.id}:${voice ?? ''}`}
                text={t(`${current.id}.desc`)}
                voice={voice ?? undefined}
                audioUrl={audioUrl}
                audioMethod="POST"
                timeoutMs={75_000}
                onStateChange={onAudioState}
                listenLabel={t('listen')}
                icon
                className="flex min-h-10 min-w-10 shrink-0 items-center justify-center"
              />
            </div>
            {audioState === 'error' && (
              <p role="status" className="text-fl-muted-2 text-sm">
                {t('audioError')}
              </p>
            )}
            {examples.length > 0 && (
              <ul className="grid gap-2 pt-1">
                {examples.map(({ icon: ExampleIcon, label }) => (
                  <li
                    key={label}
                    className="border-fl-border bg-fl-bg text-fl-muted-1 flex items-center gap-3 border px-3 py-2.5 text-sm"
                  >
                    <ExampleIcon
                      className="h-4 w-4 shrink-0"
                      aria-hidden="true"
                    />
                    {label}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>

        <div className="border-fl-border flex items-center justify-between gap-3 border-t px-6 py-4 md:px-8">
          <button
            type="button"
            onClick={() => goTo(step - 1)}
            disabled={step === 0}
            className="text-fl-muted-2 hover:text-fl-fg flex min-h-11 items-center gap-2 text-sm disabled:invisible"
          >
            <ArrowLeft className="h-4 w-4" aria-hidden="true" />
            {t('prev')}
          </button>
          <button
            type="button"
            onClick={() =>
              step === STEPS.length - 1 ? dismiss() : goTo(step + 1)
            }
            className="bg-fl-accent text-fl-accent-fg hover:bg-fl-accent/90 flex min-h-11 items-center justify-center gap-2 px-4 py-2 text-sm font-semibold transition-colors"
          >
            {t(step === STEPS.length - 1 ? 'done' : 'next')}
            <ArrowRight className="h-4 w-4 shrink-0" aria-hidden="true" />
          </button>
        </div>
      </div>
    </dialog>
  )
}
