import { createTranslator } from 'next-intl'
import { describe, expect, it } from 'vitest'
import { WHATS_NEW_VERSION } from '@/components/whats-new/WhatsNew'
import { SUPPORTED_LOCALES } from '@/lib/locales'
import en from '../../../messages/en.json'

describe.each(SUPPORTED_LOCALES)('progress messages in %s', (locale) => {
  it('renders progress metrics and games guidance', async () => {
    const messages = (await import(`../../../messages/${locale}.json`)).default
    const t = createTranslator({
      locale,
      messages,
      onError: (error) => {
        throw error
      },
    })
    for (const key of Object.keys(en.dashboardProgress)) {
      for (const count of [0, 1, 2, 5, 21]) {
        const text = t(`dashboardProgress.${key}`, {
          count,
          xp: '35',
          correct: '3',
          total: '4',
        })
        expect(text.trim()).not.toBe('')
        expect(text).not.toContain('dashboardProgress.')
        expect(text).not.toMatch(/[{}]/)
      }
    }
    for (const key of [
      'nav.games',
      ...Object.keys(en.games).map((key) => `games.${key}`),
    ]) {
      const text = t(key)
      expect(text.trim()).not.toBe('')
      expect(text).not.toBe(key)
    }
  })

  it('keeps announcement versions and entry keys consistent and translations renderable', async () => {
    const messages = (await import(`../../../messages/${locale}.json`)).default
    const t = createTranslator({
      locale,
      messages,
      onError: (error) => {
        throw error
      },
    })
    const expectedEntries = Object.keys(en.whatsNew)
      .filter((key) => /^entry\d+$/.test(key))
      .sort()
    const entries = Object.keys(messages.whatsNew)
      .filter((key) => /^entry\d+$/.test(key))
      .sort()

    expect(WHATS_NEW_VERSION.trim()).not.toBe('')
    expect(messages.whatsNew.version).toBe(WHATS_NEW_VERSION)
    expect(expectedEntries.length).toBeGreaterThan(0)
    expect(entries).toEqual(expectedEntries)

    for (const key of [
      'whatsNew.title',
      'whatsNew.cta',
      ...entries.flatMap((entry) => [
        `whatsNew.${entry}.label`,
        `whatsNew.${entry}.desc`,
      ]),
    ]) {
      const text = t.markup(key, { bold: (chunks) => chunks })
      expect(text.trim()).not.toBe('')
      expect(text).not.toBe(key)
    }
  })
})
