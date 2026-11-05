'use client'

import { useLocale, useTranslations } from 'next-intl'
import { SUPPORTED_TARGET_LANGUAGES } from '@/lib/target-languages'

export function useTargetLanguageList() {
  const locale = useLocale()
  const t = useTranslations('targetLanguages')
  const collator = new Intl.Collator(locale)
  const names = SUPPORTED_TARGET_LANGUAGES.map(({ code }) => t(code)).sort(
    collator.compare
  )

  return new Intl.ListFormat(locale, { type: 'conjunction' }).format(names)
}
