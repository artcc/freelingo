'use client'

import { useCallback, useState } from 'react'
import { useTranslations } from 'next-intl'
import Image from 'next/image'
import { Loader2 } from 'lucide-react'
import { SUPPORTED_TARGET_LANGUAGES } from '@/lib/target-languages'
import LinguAvatar from '@/components/lingu/LinguAvatar'
import { TargetLanguageText } from '@/components/TargetLanguageText'

const HERO_GREETINGS = [
  { code: 'en-GB', position: 'top-5 left-0 sm:top-8' },
  { code: 'ja-JP', position: 'top-12 -right-3 sm:top-16 sm:-right-6' },
  { code: 'de-DE', position: 'top-1/2 left-0 -translate-y-1/2' },
  { code: 'it-IT', position: 'top-1/2 right-0 -translate-y-1/2' },
  { code: 'es-ES', position: 'bottom-12 left-0 sm:bottom-16' },
  { code: 'fr-FR', position: 'right-0 bottom-5 sm:bottom-8' },
]

export function LanguageBubbles() {
  const t = useTranslations('landing')
  const tCommon = useTranslations('common')
  const tTarget = useTranslations('targetLanguages')
  const [ready, setReady] = useState(false)
  const onReady = useCallback(() => setReady(true), [])

  return (
    <div className="relative mx-auto h-[260px] w-full max-w-[360px] sm:h-[360px] sm:max-w-[420px]">
      {!ready && (
        <div
          role="status"
          aria-label={tCommon('loading')}
          className="pointer-events-none absolute inset-0 flex items-center justify-center"
        >
          <Loader2
            aria-hidden="true"
            className="text-fl-muted-2 size-6 motion-safe:animate-spin"
          />
        </div>
      )}
      <div
        aria-hidden={!ready}
        className={`relative flex h-full items-center justify-center transition-opacity duration-300 motion-reduce:transition-none ${ready ? 'opacity-100' : 'pointer-events-none opacity-0'}`}
      >
        <div className="flex justify-center" role="img" aria-label="FreeLingo">
          <LinguAvatar
            animation="saludo"
            loop
            onReady={onReady}
            className="h-[220px] w-[220px] sm:h-[300px] sm:w-[300px]"
          />
        </div>

        {HERO_GREETINGS.map(({ code, position }) => {
          const lang = SUPPORTED_TARGET_LANGUAGES.find(
            (language) => language.code === code
          )
          if (!lang) return null

          return (
            <div
              key={lang.code}
              className={`border-fl-border bg-fl-surface absolute flex items-center gap-2 rounded-2xl border px-3 py-2 shadow-sm sm:px-4 sm:py-2.5 ${position}`}
            >
              <Image
                src={lang.flagPath}
                alt={tTarget(lang.code)}
                width={18}
                height={13}
                className="h-[13px] w-[18px] shrink-0 rounded-[2px] object-cover"
              />
              <TargetLanguageText
                languageCode={lang.code}
                className="text-fl-fg text-sm font-medium whitespace-nowrap sm:text-base"
              >
                {t(`languageGreetings.${lang.code}`)}
              </TargetLanguageText>
            </div>
          )
        })}
      </div>
    </div>
  )
}
