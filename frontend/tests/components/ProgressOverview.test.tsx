import { render, screen, within } from '@testing-library/react'
import { NextIntlClientProvider } from 'next-intl'
import { describe, expect, it } from 'vitest'
import { ProgressOverview } from '@/components/dashboard/ProgressOverview'
import es from '../../../messages/es.json'

describe('dashboard progress', () => {
  it('presents zero-XP activity as practice and uses UTC dates with explicit accessible labels', () => {
    render(
      <NextIntlClientProvider locale="es" messages={es}>
        <ProgressOverview
          xp={1234}
          todayXp={0}
          streak={2}
          lessons={8}
          correct={3}
          total={4}
          activity={[
            { date: '2026-10-04', active: true, xp: 20 },
            { date: '2026-10-05', active: true, xp: 0 },
          ]}
        />
      </NextIntlClientProvider>
    )
    expect(screen.getByText('Hoy has practicado')).toBeInTheDocument()
    expect(screen.getByText('+0 XP hoy')).toBeInTheDocument()
    expect(screen.getByText('75%')).toBeInTheDocument()
    expect(screen.getByText('3 de 4 respuestas correctas')).toBeInTheDocument()
    const days = within(screen.getByRole('list')).getAllByRole('listitem')
    expect(days[1]).toHaveAccessibleName('5 oct 2026: Has practicado')
    expect(screen.getByRole('link', { name: 'Ver progreso' })).toHaveAttribute(
      'href',
      '/progress'
    )
  })

  it('does not present missing exercise evidence as zero accuracy or missed activity as active', () => {
    render(
      <NextIntlClientProvider locale="es" messages={es}>
        <ProgressOverview
          xp={0}
          todayXp={0}
          streak={0}
          lessons={0}
          correct={0}
          total={0}
          activity={[{ date: '2026-10-05', active: false, xp: 0 }]}
        />
      </NextIntlClientProvider>
    )
    expect(screen.getByText('—')).toBeInTheDocument()
    expect(screen.queryByText('0%')).not.toBeInTheDocument()
    expect(screen.queryByText('Hoy has practicado')).not.toBeInTheDocument()
    expect(screen.getByRole('listitem')).toHaveAccessibleName(
      '5 oct 2026: Sin actividad registrada'
    )
  })
})
