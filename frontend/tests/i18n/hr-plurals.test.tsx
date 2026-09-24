import { render, screen } from '@testing-library/react'
import { NextIntlClientProvider, useTranslations } from 'next-intl'
import { describe, expect, it } from 'vitest'

import hr from '../../../messages/hr.json'

function PluralExamples({ count }: { count: number }) {
  const grammar = useTranslations('grammar')
  const billing = useTranslations('billing')
  const vocabulary = useTranslations('vocabulary')
  const common = useTranslations('common')

  return (
    <>
      <p>{grammar('topicsFound', { count })}</p>
      <p>{billing('trialDays', { days: count })}</p>
      <p>{vocabulary('sets', { count })}</p>
      <p>{common('errorMessage')}</p>
    </>
  )
}

describe('Croatian plural messages', () => {
  it.each([
    [1, 'Pronađena 1 tema', '1 dan probnog razdoblja', '1 zbirka'],
    [2, 'Pronađene 2 teme', '2 dana probnog razdoblja', '2 zbirke'],
    [5, 'Pronađeno 5 tema', '5 dana probnog razdoblja', '5 zbirki'],
    [21, 'Pronađena 21 tema', '21 dan probnog razdoblja', '21 zbirka'],
    [22, 'Pronađene 22 teme', '22 dana probnog razdoblja', '22 zbirke'],
    [25, 'Pronađeno 25 tema', '25 dana probnog razdoblja', '25 zbirki'],
  ])('formats %i with the correct Croatian forms', (count, topics, days, sets) => {
    render(
      <NextIntlClientProvider locale="hr" messages={hr} timeZone="UTC">
        <PluralExamples count={count} />
      </NextIntlClientProvider>
    )

    expect(screen.getByText(topics)).toBeInTheDocument()
    expect(screen.getByText(days)).toBeInTheDocument()
    expect(screen.getByText(sets)).toBeInTheDocument()
    expect(screen.getByText(hr.common.errorMessage)).toBeInTheDocument()
  })
})
