'use client'

import { useCallback, useMemo, useState, type CSSProperties } from 'react'
import { useTranslations } from 'next-intl'
import Image from 'next/image'
import { SUPPORTED_TARGET_LANGUAGES } from '@/lib/target-languages'
import LinguAvatar from '@/components/lingu/LinguAvatar'
import { TargetLanguageText } from '@/components/TargetLanguageText'

function orbitPosition(index: number, total: number) {
  const angle = (index / total) * 2 * Math.PI - Math.PI / 2
  // Bound precision so server and browser math produce identical CSS values.
  const x = Number((Math.cos(angle) * 215).toFixed(3))
  const y = Number((Math.sin(angle) * 140).toFixed(3))
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
        orbitPosition(i, SUPPORTED_TARGET_LANGUAGES.length)
      ),
    []
  )

  return (
    <div
      aria-hidden={!ready}
      className={`relative flex w-full flex-wrap justify-center gap-x-3 gap-y-4 pt-3 pb-8 transition-opacity duration-300 motion-reduce:transition-none sm:block sm:h-[380px] sm:p-0 ${ready ? 'opacity-100' : 'pointer-events-none opacity-0'}`}
    >
      <div
        className="relative z-[1] flex h-[140px] w-full justify-center sm:absolute sm:top-1/2 sm:left-1/2 sm:w-[140px] sm:-translate-x-1/2 sm:-translate-y-1/2"
        role="img"
        aria-label="FreeLingo"
      >
        <LinguAvatar
          animation="saludo"
          loop
          onReady={onReady}
          className="h-[140px] w-[140px]"
        />
      </div>

      {SUPPORTED_TARGET_LANGUAGES.map((lang, i) => {
        const { x, y } = positions[i]
        const greeting = t(`languageGreetings.${lang.code}`) ?? lang.name
        const delay = Number((i * 0.35).toFixed(2))
        return (
          <div
            key={lang.code}
            className="relative z-0 w-max sm:absolute sm:top-1/2 sm:left-1/2 sm:mt-[var(--bubble-y)] sm:ml-[var(--bubble-x)] sm:-translate-x-1/2 sm:-translate-y-1/2"
            style={
              {
                '--bubble-x': `${x}px`,
                '--bubble-y': `${y}px`,
              } as CSSProperties
            }
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
                  className="h-[10px] w-[14px] shrink-0 rounded-[2px] object-cover"
                />
                <TargetLanguageText
                  languageCode={lang.code}
                  className="text-fl-fg text-[11px] font-medium whitespace-nowrap"
                >
                  {greeting}
                </TargetLanguageText>
              </div>
            </div>
          </div>
        )
      })}
    </div>
  )
}
