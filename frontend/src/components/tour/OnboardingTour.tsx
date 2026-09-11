'use client'

import { useState, useEffect, useCallback } from 'react'
import { useTranslations } from 'next-intl'
import { useConfigStore } from '@/store/config'
import {
  Sparkles,
  MessageSquare,
  Mic,
  Layers,
  BookOpen,
  Headphones,
  Zap,
} from 'lucide-react'

const STORAGE_KEY = 'fl_tour_done'

const STEP_ICONS = [
  Sparkles,
  MessageSquare,
  Mic,
  Layers,
  BookOpen,
  Headphones,
  Zap,
]
const PREMIUM_STEPS = new Set([1, 2, 5])

export default function OnboardingTour() {
  const t = useTranslations('tour')
  const stripeEnabled = useConfigStore((s) => s.stripeEnabled)
  const [visible, setVisible] = useState(false)
  const [step, setStep] = useState(0)
  const [leaving, setLeaving] = useState(false)
  const [dir, setDir] = useState<'next' | 'prev'>('next')

  const totalSteps = 7

  useEffect(() => {
    if (typeof window !== 'undefined' && !localStorage.getItem(STORAGE_KEY)) {
      setVisible(true)
    }
  }, [])

  const dismiss = useCallback(() => {
    localStorage.setItem(STORAGE_KEY, '1')
    setVisible(false)
  }, [])

  const goTo = useCallback((next: number, direction: 'next' | 'prev') => {
    setDir(direction)
    setLeaving(true)
    setTimeout(() => {
      setStep(next)
      setLeaving(false)
    }, 150)
  }, [])

  if (!visible) return null

  const isFirst = step === 0
  const isLast = step === totalSteps - 1

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* Backdrop */}
      <div
        className="bg-fl-bg/80 absolute inset-0 backdrop-blur-sm"
        onClick={dismiss}
      />

      {/* Modal */}
      <div className="border-fl-border bg-fl-surface relative z-10 w-full max-w-md border shadow-2xl">
        {/* Top bar */}
        <div className="border-fl-border flex items-center justify-between border-b px-5 pt-5 pb-4">
          {/* Progress dots */}
          <div className="flex gap-1.5">
            {Array.from({ length: totalSteps }).map((_, i) => (
              <span
                key={i}
                className={`block h-1.5 w-1.5 rounded-full transition-colors ${
                  i === step ? 'bg-fl-accent' : 'bg-fl-border'
                }`}
              />
            ))}
          </div>
          <button
            onClick={dismiss}
            className="text-fl-hint text-fl-muted-3 hover:text-fl-fg font-mono tracking-widest uppercase transition-colors"
          >
            {t('skip')}
          </button>
        </div>

        {/* Step content */}
        <div
          className={`px-6 py-7 transition-all duration-150 ${
            leaving
              ? dir === 'next'
                ? '-translate-x-3 opacity-0'
                : 'translate-x-3 opacity-0'
              : 'translate-x-0 opacity-100'
          }`}
        >
          <div className="mb-4 flex items-center gap-3">
            {(() => {
              const Icon = STEP_ICONS[step]
              return <Icon className="text-fl-muted-2 h-5 w-5" />
            })()}
            <span className="text-fl-label text-fl-muted-2 font-mono tracking-widest uppercase">
              {t(`step${step + 1}.label`)}
              {stripeEnabled && PREMIUM_STEPS.has(step) && (
                <span className="text-fl-accent ml-1">★</span>
              )}
            </span>
          </div>
          <h2 className="text-fl-fg mb-2 font-mono text-base font-bold">
            {t(`step${step + 1}.title`)}
          </h2>
          <p className="text-fl-muted-1 font-mono text-sm leading-relaxed">
            {t(`step${step + 1}.desc`)}
          </p>
        </div>

        {/* Navigation */}
        <div className="flex items-center justify-between px-6 pb-6">
          <button
            onClick={() => goTo(step - 1, 'prev')}
            disabled={isFirst}
            className="text-fl-muted-2 hover:text-fl-fg font-mono text-xs tracking-widest uppercase transition-colors disabled:opacity-0"
          >
            ← {t('prev')}
          </button>
          {isLast ? (
            <button
              onClick={dismiss}
              className="bg-fl-accent text-fl-accent-fg hover:bg-fl-accent/90 px-5 py-2 font-mono text-sm tracking-widest uppercase transition-colors"
            >
              {t('done')}
            </button>
          ) : (
            <button
              onClick={() => goTo(step + 1, 'next')}
              className="text-fl-muted-1 hover:text-fl-fg font-mono text-sm tracking-widest uppercase transition-colors"
            >
              {t('next')} →
            </button>
          )}
        </div>
      </div>
    </div>
  )
}
