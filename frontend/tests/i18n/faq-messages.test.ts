import { createTranslator } from 'next-intl'
import { describe, expect, it } from 'vitest'
import { SUPPORTED_LOCALES } from '@/lib/locales'
import en from '../../../messages/en.json'

const passthrough = (chunks: string) => chunks
const richValues = {
  languages: 'English, Spanish',
  strong: passthrough,
  code: passthrough,
  adminLink: passthrough,
  settingsLink: passthrough,
  feedbackLink: passthrough,
  languagesLink: passthrough,
  grammarLink: passthrough,
  gamesLink: passthrough,
  memoriesLink: passthrough,
  billingLink: passthrough,
}

describe.each(SUPPORTED_LOCALES)(
  'Authenticated FAQ messages in %s',
  (locale) => {
    it('includes all questions and sections with the same rich-text contracts', async () => {
      const messages = (await import(`../../../messages/${locale}.json`))
        .default
      expect(Object.keys(messages.faq).sort()).toEqual(
        Object.keys(en.faq).sort()
      )
      const t = createTranslator({
        locale,
        messages,
        namespace: 'faq',
        onError: (error) => {
          throw error
        },
      })

      for (const [key, source] of Object.entries(en.faq)) {
        const translated = messages.faq[key] as string
        expect((translated.match(/<\/?\w+>/g) ?? []).sort()).toEqual(
          (source.match(/<\/?\w+>/g) ?? []).sort()
        )
        const text = t.markup(key, richValues)
        expect(text.trim()).not.toBe('')
        expect(text).not.toBe(key)
        expect(text).not.toMatch(/[{}]|<\/?\w+>/)
      }
    })
  }
)
