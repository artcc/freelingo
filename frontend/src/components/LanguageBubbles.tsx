'use client'

import { useCallback, useMemo, useState } from 'react'
import { useTranslations } from 'next-intl'
import Image from 'next/image'
import { SUPPORTED_TARGET_LANGUAGES } from '@/lib/target-languages'
import LinguAvatar from '@/components/lingu/LinguAvatar'

function circlePosition(index: number, total: number, radius: number) {
  const angle = (index / total) * 2 * Math.PI - Math.PI / 2
  const x = Math.cos(angle) * radius
  const y = Math.sin(angle) * radius
  return { x, y }
}

export function LanguageBubbles() {
  const t = useTranslations('landing')
  const tTarget = useTranslations('targetLanguages')
  const [ready, setReady] = useState(false)
  const onReady = useCallback(() => setReady(true), [])
  const positions = useMemo(
    () =>
      SUPPORTED_TARGET_LANGUAGES.map((_, i) =>
        circlePosition(i, SUPPORTED_TARGET_LANGUAGES.length, 135)
      ),
    []
  )

  return (
    <div
      aria-hidden={!ready}
      className={`relative h-[360px] w-full transition-opacity duration-300 motion-reduce:transition-none sm:h-[380px] ${ready ? 'opacity-100' : 'pointer-events-none opacity-0'}`}
    >
      <div
        className="absolute top-1/2 left-1/2 z-[1] h-[140px] w-[140px] -translate-x-1/2 -translate-y-1/2"
        role="img"
        aria-label="FreeLingo"
      >
        <LinguAvatar
          animation="saludo"
          loop
          onReady={onReady}
          className="h-full w-full"
        />
      </div>

      {SUPPORTED_TARGET_LANGUAGES.map((lang, i) => {
        const { x, y } = positions[i]
        const greeting = t(`languageGreetings.${lang.code}`) ?? lang.name
        const delay = i * 0.35
        return (
          <div
            key={lang.code}
            className="absolute z-0 w-max"
            style={{
              left: `calc(50% + ${x}px)`,
              top: `calc(50% + ${y}px)`,
              transform: 'translate(-50%, -50%)',
            }}
          >
            <div
              className="animate-float w-max motion-reduce:animate-none"
              style={{
                animationDelay: `${delay}s`,
                animationDuration: '3.4s',
                animationPlayState: ready ? 'running' : 'paused',
              }}
            >
              <div className="border-fl-border bg-fl-surface flex items-center gap-1.5 rounded-full border px-2.5 py-1 shadow-sm transition-shadow hover:shadow-md">
                <Image
                  src={lang.flagPath}
                  alt={tTarget(lang.code)}
                  width={14}
                  height={10}
                  className="rounded-[2px]"
                />
                <span className="text-fl-fg font-sans text-[11px] font-medium whitespace-nowrap">
                  {greeting}
                </span>
              </div>
            </div>
          </div>
        )
      })}
    </div>
  )
}
