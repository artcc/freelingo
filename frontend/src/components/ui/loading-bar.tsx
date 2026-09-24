'use client'

import { useEffect, useRef, useState } from 'react'
import { useTranslations } from 'next-intl'
import { useLoadingStore } from '@/store/loading'

const MIN_VISIBLE_MS = 600
const COMPLETE_DURATION_MS = 400

type Phase = 'hidden' | 'loading' | 'completing'

export function LoadingBar() {
  const tCommon = useTranslations('common')
  const count = useLoadingStore((s) => s.count)
  const complete = useLoadingStore((s) => s.complete)
  const finishComplete = useLoadingStore((s) => s.finishComplete)

  const [phase, setPhase] = useState<Phase>('hidden')
  const visibleSince = useRef(0)
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null)

  useEffect(() => {
    if (count > 0) {
      // New request started — show loading immediately, cancel any pending complete
      if (timerRef.current) clearTimeout(timerRef.current)
      visibleSince.current = Date.now()
      setPhase('loading')
      return
    }

    if (complete && phase === 'loading') {
      // All requests finished — wait minimum visible time, then exit
      const elapsed = Date.now() - visibleSince.current
      const remaining = Math.max(0, MIN_VISIBLE_MS - elapsed)
      timerRef.current = setTimeout(() => {
        setPhase('completing')
      }, remaining)
    }

    return () => {
      if (timerRef.current) clearTimeout(timerRef.current)
    }
  }, [count, complete, phase])

  if (phase === 'hidden') return null

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
        onAnimationEnd={(e) => {
          if (
            phase === 'completing' &&
            e.nativeEvent.animationName === 'loading-bar-complete'
          ) {
            setPhase('hidden')
            finishComplete()
          }
        }}
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
      `}</style>
    </div>
  )
}
