import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { TargetLanguageText } from '@/components/TargetLanguageText'

describe('TargetLanguageText — Russian', () => {
  it('preserves Cyrillic, ё, and stress marks without adding romanization', () => {
    const text = 'Привет! Всё хорошо́.'
    const { container } = render(
      <TargetLanguageText languageCode="ru-RU">{text}</TargetLanguageText>
    )

    const content = screen.getByText(text)
    expect(content).toHaveAttribute('lang', 'ru-RU')
    expect(content).toHaveClass('font-target-cyrillic')
    expect(content.children).toHaveLength(0)
    expect(container.textContent).toBe(text)
  })

  it('renders optional support only when explicitly supplied', () => {
    render(
      <TargetLanguageText languageCode="ru-RU" translation="Hello!">
        Привет!
      </TargetLanguageText>
    )

    expect(screen.getByText('Привет!')).toHaveAttribute('lang', 'ru-RU')
    expect(screen.getByText('Hello!')).toBeInTheDocument()
  })
})
