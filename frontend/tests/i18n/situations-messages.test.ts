import { createTranslator } from 'next-intl'
import { describe, expect, it } from 'vitest'
import { SUPPORTED_LOCALES } from '@/lib/locales'
import { situationCategories } from '@/lib/situations'
import en from '../../../messages/en.json'

function leaves(value: unknown, prefix = ''): string[] {
  if (typeof value === 'string') return [prefix]
  if (!value || typeof value !== 'object') return []
  return Object.entries(value).flatMap(([key, child]) =>
    leaves(child, prefix ? `${prefix}.${key}` : key)
  )
}

describe.each(SUPPORTED_LOCALES)('situation messages in %s', (locale) => {
  it('renders every nested catalog, navigation and quota message', async () => {
    const messages = (await import(`../../../messages/${locale}.json`)).default
    const t = createTranslator({
      locale,
      messages,
      onError: (error) => {
        throw error
      },
    })
    expect(leaves(messages.situations).sort()).toEqual(
      leaves(en.situations).sort()
    )
    const requiredKeys = [
      ...leaves(en.situations, 'situations'),
      ...Object.entries(situationCategories).flatMap(([category, ids]) => [
        `situations.categories.${category}`,
        ...ids.flatMap((id) => [
          `situations.items.${id}.title`,
          `situations.items.${id}.description`,
        ]),
      ]),
      'nav.situations',
      'freemium.situationsLabel',
      'billing.paywallSituationsTitle',
      'billing.paywallSituationsDesc',
    ]
    for (const key of requiredKeys) {
      const text = t(key)
      expect(text.trim()).not.toBe('')
      expect(text).not.toBe(key)
      expect(text).not.toMatch(/[{}]/)
    }
  })
})
