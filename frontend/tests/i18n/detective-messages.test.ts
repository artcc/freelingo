import { createTranslator } from 'next-intl'
import { describe, expect, it } from 'vitest'
import { SUPPORTED_LOCALES } from '@/lib/locales'
import en from '../../../messages/en.json'

describe.each(SUPPORTED_LOCALES)('Game messages in %s', (locale) => {
  it('renders every game state, reward and billing message', async () => {
    const messages = (await import(`../../../messages/${locale}.json`)).default
    const t = createTranslator({ locale, messages, onError: (error) => { throw error } })
    expect(Object.keys(messages.detective).sort()).toEqual(Object.keys(en.detective).sort())
    expect(Object.keys(messages.sentenceOrder).sort()).toEqual(Object.keys(en.sentenceOrder).sort())
    expect(Object.keys(messages.vocabularyPairs).sort()).toEqual(Object.keys(en.vocabularyPairs).sort())
    for (const key of [...Object.keys(en.vocabularyPairs).map((k) => `vocabularyPairs.${k}`), 'games.vocabularyPairsTitle', 'games.vocabularyPairsDescription']) {
      const text = t(key, { count: 3, correct: 4, xp: 13 })
      expect(text.trim()).not.toBe('')
      expect(text).not.toBe(key)
      expect(text).not.toMatch(/[{}]/)
    }
    for (const key of [...Object.keys(en.detective).map((k) => `detective.${k}`), ...Object.keys(en.sentenceOrder).map((k) => `sentenceOrder.${k}`), 'games.sentenceOrderTitle', 'games.sentenceOrderDescription', 'games.detectiveTitle', 'games.detectiveDescription', 'freemium.gamesLabel', 'billing.paywallGamesTitle', 'billing.paywallGamesDesc']) {
      const text = t(key, { current: 1, total: 5, detected: 3, corrected: 4, correct: 4, xp: 11, fragment: '学生', position: 2 })
      expect(text.trim()).not.toBe('')
      expect(text).not.toBe(key)
      expect(text).not.toMatch(/[{}]/)
    }
  })
})
