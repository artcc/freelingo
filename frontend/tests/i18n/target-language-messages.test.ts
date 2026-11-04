import { describe, expect, it } from 'vitest'
import { SUPPORTED_LOCALES } from '@/lib/locales'
import { TARGET_LANGUAGE_CATALOG } from '@/lib/target-languages'
import { WHATS_NEW_VERSION } from '@/components/whats-new/WhatsNew'

describe.each(SUPPORTED_LOCALES)('target language messages in %s', (locale) => {
  it('provides regional labels, descriptions, greetings, and matching announcements', async () => {
    const messages = (await import(`../../../messages/${locale}.json`)).default
    for (const language of TARGET_LANGUAGE_CATALOG) {
      expect(messages.targetLanguages[language.code]?.trim()).toBeTruthy()
      expect(messages.targetLanguages[`${language.code}-description`]?.trim()).toBeTruthy()
      expect(messages.landing.languageGreetings[language.code]?.trim()).toBeTruthy()
    }
    expect(messages.targetLanguages['pt-BR']).not.toBe(messages.targetLanguages['pt-PT'])
    expect(messages.landing.languageGreetings['pt-BR']).toBe('Oi!')
    expect(messages.whatsNew.version).toBe(WHATS_NEW_VERSION)
    expect(Object.keys(messages.whatsNew).filter((key) => /^entry\d+$/.test(key))).toEqual([
      'entry1',
      'entry2',
      'entry3',
      'entry4',
    ])
  })
})
