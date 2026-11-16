import { createTranslator } from 'next-intl'
import { describe, expect, it } from 'vitest'
import { SUPPORTED_LOCALES } from '@/lib/locales'
import en from '../../../messages/en.json'

describe.each(SUPPORTED_LOCALES)(
  'grammar practice messages in %s',
  (locale) => {
    it('renders every practice state, navigation and quota message', async () => {
      const messages = (await import(`../../../messages/${locale}.json`))
        .default
      const t = createTranslator({
        locale,
        messages,
        onError: (error) => {
          throw error
        },
      })
      expect(Object.keys(messages.grammarPractice).sort()).toEqual(
        Object.keys(en.grammarPractice).sort()
      )
      for (const key of [
        ...Object.keys(en.grammarPractice).map(
          (key) => `grammarPractice.${key}`
        ),
        'nav.practiceGrammar',
        'freemium.grammarPracticeLabel',
        'billing.paywallGrammarPracticeTitle',
        'billing.paywallGrammarPracticeDesc',
      ]) {
        const text = t(key, { count: 10, percent: 80, correct: 4, answered: 5 })
        expect(text.trim()).not.toBe('')
        expect(text).not.toBe(key)
        expect(text).not.toMatch(/[{}]/)
      }
    })
  }
)
