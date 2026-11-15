import { describe, expect, it } from 'vitest'
import { hasTwoMonthsFree, splitYearlyCta } from '@/lib/billing-copy'

describe('annual savings claims', () => {
  it.each([
    [4.99, 49.9],
    [9.99, 99.9],
    [10, 100],
  ])('recognizes exactly two free months for %s / %s', (monthly, yearly) => {
    expect(hasTwoMonthsFree(monthly, yearly)).toBe(true)
  })

  it.each([
    [0, 0],
    [-10, -100],
    [10, 120],
    [10, 90],
    [10, 99.99],
    [10, 100.01],
    [4.999, 49.99],
    [Number.NaN, 100],
    [10, Number.POSITIVE_INFINITY],
    [Number.MAX_VALUE, Number.MAX_VALUE],
  ])('omits an unsupported claim for %s / %s', (monthly, yearly) => {
    expect(hasTwoMonthsFree(monthly, yearly)).toBe(false)
  })

  it('preserves the annual price while omitting an unsupported savings label', () => {
    expect(
      splitYearlyCta('Best value · €120/year · 2 months free →', false)
    ).toEqual({ main: 'Best value · €120/year →', savings: null })
    expect(
      splitYearlyCta('Free trial, then €120/year · 2 months free', false)
    ).toEqual({ main: 'Free trial, then €120/year →', savings: null })
  })

  it('retains a supported savings label and handles an unsplit label', () => {
    expect(splitYearlyCta('Best value · €100/year · 2 months free →')).toEqual({
      main: 'Best value · €100/year →',
      savings: '2 months free',
    })
    expect(splitYearlyCta('Annual plan', false)).toEqual({
      main: 'Annual plan',
      savings: null,
    })
  })
})
