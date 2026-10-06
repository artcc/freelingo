'use client'

import { useState, useSyncExternalStore } from 'react'
import dynamic from 'next/dynamic'
import Image from 'next/image'
import type { LinguAnimation } from '@/lib/lingu'

export type { LinguAnimation } from '@/lib/lingu'

export interface LinguSceneProps {
  animation: LinguAnimation
  loop?: boolean
  onFinished?: () => void
  onError: () => void
}

function Placeholder() {
  return (
    <Image
      src="/logo.png"
      alt=""
      fill
      sizes="(min-width: 768px) 280px, 180px"
      className="object-contain p-2"
    />
  )
}

const Scene = dynamic<LinguSceneProps>(
  () => import('./LinguScene').catch(() => ({ default: Placeholder })),
  { ssr: false, loading: Placeholder }
)

function subscribe(callback: () => void) {
  const query = window.matchMedia('(prefers-reduced-motion: reduce)')
  query.addEventListener('change', callback)
  return () => query.removeEventListener('change', callback)
}

export default function LinguAvatar({
  animation,
  loop,
  onFinished,
  className = 'h-44 w-44 sm:h-52 sm:w-52 md:h-80 md:w-full',
}: Omit<LinguSceneProps, 'onError'> & { className?: string }) {
  const [failed, setFailed] = useState(false)
  const reducedMotion = useSyncExternalStore(
    subscribe,
    () => window.matchMedia('(prefers-reduced-motion: reduce)').matches,
    () => true
  )

  return (
    <div aria-hidden="true" className={`relative mx-auto ${className}`}>
      {reducedMotion || failed ? (
        <Placeholder />
      ) : (
        <Scene
          animation={animation}
          loop={loop}
          onFinished={onFinished}
          onError={() => setFailed(true)}
        />
      )}
    </div>
  )
}
