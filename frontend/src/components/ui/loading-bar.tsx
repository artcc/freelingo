'use client'

import { useLayoutEffect, useRef, useState } from 'react'
import { useTranslations } from 'next-intl'
import { useLoadingStore } from '@/store/loading'
import { usePageLoadingActive } from './page-loading-boundary'

const APPEAR_DELAY_MS = 200
const MIN_VISIBLE_MS = 300
const COMPLETE_DURATION_MS = 150

type Phase = 'hidden' | 'loading' | 'completing'

export function LoadingBar() {
  const tCommon = useTranslations('common')
  const count = useLoadingStore((s) => s.count)
  const complete = useLoadingStore((s) => s.complete)
  const finishComplete = useLoadingStore((s) => s.finishComplete)
  const fullPageActive = usePageLoadingActive()
  const pending = count > 0

  const [phase, setPhase] = useState<Phase>('hidden')
  const startedAt = useRef<number | null>(null)
  const visibleSince = useRef<number | null>(null)

  useLayoutEffect(() => {
    if (phase === 'loading' && pending && !fullPageActive) {
      visibleSince.current ??= performance.now()
    }
  }, [phase, pending, fullPageActive])

  useLayoutEffect(() => {
    if (fullPageActive) {
      startedAt.current = null
      visibleSince.current = null
      setPhase('hidden')
      if (!pending && complete) finishComplete()
      return
    }

    let timer: ReturnType<typeof setTimeout> | undefined
    if (pending) {
      if (phase === 'hidden') {
        startedAt.current ??= performance.now()
        timer = setTimeout(
          () => {
            setPhase('loading')
          },
          Math.max(0, APPEAR_DELAY_MS - (performance.now() - startedAt.current))
        )
      } else if (phase === 'completing') {
        // A handoff during exit belongs to the already-visible cycle.
        setPhase('loading')
      }
    } else if (phase === 'loading') {
      if (visibleSince.current === null) {
        // Activity can finish after the reveal timer but before its first commit.
        startedAt.current = null
        setPhase('hidden')
        if (complete) finishComplete()
        return
      }
      const remaining = Math.max(
        0,
        MIN_VISIBLE_MS - (performance.now() - visibleSince.current)
      )
      timer = setTimeout(() => setPhase('completing'), remaining)
    } else if (phase === 'completing') {
      // Completion also works when reduced motion disables CSS animations.
      timer = setTimeout(() => {
        startedAt.current = null
        visibleSince.current = null
        setPhase('hidden')
        finishComplete()
      }, COMPLETE_DURATION_MS)
    } else {
      startedAt.current = null
      visibleSince.current = null
      if (complete) finishComplete()
    }

    return () => clearTimeout(timer)
  }, [pending, complete, phase, fullPageActive, finishComplete])

  if (fullPageActive || phase === 'hidden') return null

  return (
    <div
      className="fixed top-0 right-0 left-0 z-[300] h-px overflow-hidden"
      role="progressbar"
      aria-label={tCommon('loading')}
    >
      <div
        className={`bg-fl-fg h-full ${
          phase === 'completing'
            ? 'animate-loading-bar-complete'
            : 'animate-loading-bar'
        }`}
        style={{ width: '100%' }}
      />
      <style>{`
        @keyframes loading-bar {
          0%   { transform: translateX(-100%); }
          50%  { transform: translateX(-20%); }
          100% { transform: translateX(0%); }
        }
        @keyframes loading-bar-complete {
          0%   { transform: translateX(0%); opacity: 1; }
          100% { transform: translateX(0%); opacity: 0; }
        }
        .animate-loading-bar {
          animation: loading-bar 1.4s ease-in-out infinite;
        }
        .animate-loading-bar-complete {
          animation: loading-bar-complete ${COMPLETE_DURATION_MS}ms ease-out forwards;
        }
        @media (prefers-reduced-motion: reduce) {
          .animate-loading-bar,
          .animate-loading-bar-complete {
            animation: none;
          }
        }
      `}</style>
    </div>
  )
}
