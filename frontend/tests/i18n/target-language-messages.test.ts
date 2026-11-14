import { describe, expect, it } from 'vitest'
import { SUPPORTED_LOCALES } from '@/lib/locales'
import { TARGET_LANGUAGE_CATALOG } from '@/lib/target-languages'

describe.each(SUPPORTED_LOCALES)('target language messages in %s', (locale) => {
  it('provides regional labels, descriptions, greetings, and language FAQ placeholders', async () => {
    const messages = (await import(`../../../messages/${locale}.json`)).default
    for (const language of TARGET_LANGUAGE_CATALOG) {
      expect(messages.targetLanguages[language.code]?.trim()).toBeTruthy()
      expect(messages.targetLanguages[language.iso639]?.trim()).toBeTruthy()
      expect(messages.targetLanguages[`${language.code}-description`]?.trim()).toBeTruthy()
      expect(messages.landing.languageGreetings[language.code]?.trim()).toBeTruthy()
    }
    expect(messages.targetLanguages['pt-BR']).not.toBe(messages.targetLanguages['pt-PT'])
    expect(messages.landing.languageGreetings['pt-BR']).toBe('Oi!')
    expect(messages.landing.languageGreetings['nl-NL']).toBe('Hallo!')
    expect(messages.landing.languageGreetings['ru-RU']).toBe('Привет!')
    expect(messages.landing.languageGreetings['sv-SE']).toBe('Hej!')
    expect(messages.landing.languageGreetings['da-DK']).toBe('Hej!')
    expect(messages.faq.a_language).toContain('{languages}')
    expect(messages.landing.faq.languages.answer).toContain('{languages}')
    expect(messages.targetLanguages.nl?.trim()).toBeTruthy()
  })
})
