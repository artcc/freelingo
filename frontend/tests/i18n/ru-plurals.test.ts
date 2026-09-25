import { createTranslator } from 'next-intl'
import { describe, expect, it } from 'vitest'

import ru from '../../../messages/ru.json'

describe('Russian plural messages', () => {
  const t = createTranslator({ locale: 'ru', messages: ru })

  it.each([
    [1, 'день', 'Найдена 1 тема', 'Показана 1 ситуация', '1 набор'],
    [2, 'дня', 'Найдены 2 темы', 'Показаны 2 ситуации', '2 набора'],
    [5, 'дней', 'Найдено 5 тем', 'Показано 5 ситуаций', '5 наборов'],
    [21, 'день', 'Найдена 21 тема', 'Показана 21 ситуация', '21 набор'],
    [22, 'дня', 'Найдены 22 темы', 'Показаны 22 ситуации', '22 набора'],
    [25, 'дней', 'Найдено 25 тем', 'Показано 25 ситуаций', '25 наборов'],
  ])('formats %i with the correct forms', (count, day, topics, situations, sets) => {
    expect(t('dashboard.freemiumTrialTitle', { days: count })).toBe(
      `${count} ${day} пробного периода`
    )
    expect(t('freemium.trialDaysLeft', { days: count })).toBe(
      `${count} ${day} бесплатного пробного периода`
    )
    expect(t('grammar.topicsFound', { count })).toBe(topics)
    expect(t('phrasebook.situationsShown', { count })).toBe(situations)
    expect(t('vocabulary.sets', { count })).toBe(sets)
  })
})
