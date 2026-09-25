import { createTranslator } from 'next-intl'
import { describe, expect, it } from 'vitest'

import { SUPPORTED_LOCALES } from '@/lib/locales'
import en from '../../../messages/en.json'

const messageKeys = [
  'assessment.voiceTrialLabel',
  'assessment.voiceTrialTitle',
  'assessment.voiceTrialDesc',
  'assessment.voiceTrialStart',
  'assessment.voiceTrialSkip',
  'conversation.trialBanner',
  'conversation.trialCtaLabel',
  'conversation.trialCtaTitle',
  'conversation.trialCtaDesc',
  'conversation.errorTranscription',
  'conversation.errorResponse',
  'conversation.errorSpeech',
] as const

const english = createTranslator({ locale: 'en', messages: en })

describe.each(SUPPORTED_LOCALES)('voice messages in %s', (locale) => {
  it('renders translated trial and error messages without English fallback', async () => {
    const messages = (await import(`../../../messages/${locale}.json`)).default
    const t = createTranslator({
      locale,
      messages,
      onError: (error) => {
        throw error
      },
    })

    for (const key of messageKeys) {
      const rendered = t(key, { minutes: 5 })
      expect(rendered.trim()).not.toBe('')
      expect(rendered).not.toBe(key)
      expect(rendered).not.toContain('{minutes}')
      if (locale !== 'en') {
        expect(rendered).not.toBe(english(key, { minutes: 5 }))
      }
    }
  })
})
