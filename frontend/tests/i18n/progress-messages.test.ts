import { createTranslator } from 'next-intl'
import { describe, expect, it } from 'vitest'
import { SUPPORTED_LOCALES } from '@/lib/locales'
import en from '../../../messages/en.json'

describe.each(SUPPORTED_LOCALES)('progress messages in %s', (locale) => {
  it('renders progress metrics and the three ordered release entries', async () => {
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
    expect(
      Object.keys(messages.whatsNew).filter((key) => /^entry\d+$/.test(key))
    ).toEqual(['entry1', 'entry2', 'entry3'])
    expect(
      t.markup('whatsNew.entry2.desc', { bold: (chunks) => chunks })
    ).toContain('XP')
    expect(messages.whatsNew.version).toBe('v1.9.30')
  })
})
