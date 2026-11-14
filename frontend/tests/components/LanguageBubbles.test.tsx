import { describe, expect, it, vi } from 'vitest'
import { fireEvent, render, screen } from '@testing-library/react'
import React from 'react'
import { renderToString } from 'react-dom/server'
import { LanguageBubbles } from '@/components/LanguageBubbles'

vi.mock('next-intl', () => ({
  useTranslations: (namespace: string) => (key: string) =>
    namespace === 'targetLanguages'
      ? `Localized ${key}`
      : key === 'languageGreetings.ja-JP'
        ? 'こんにちは！'
        : key,
}))

vi.mock('@/components/lingu/LinguAvatar', () => ({
  default: ({ onReady }: { onReady?: () => void }) => (
    <button data-testid="lingu-ready" onClick={onReady} />
  ),
}))

vi.mock('next/image', () => ({
  default: function MockImage(
    props: React.ImgHTMLAttributes<HTMLImageElement> & {
      unoptimized?: boolean
      priority?: boolean
    }
  ) {
    const { unoptimized, priority, ...imgProps } = props
    void unoptimized
    void priority
    return React.createElement('img', imgProps)
  },
}))

describe('LanguageBubbles', () => {
  it('reveals Lingu and the language bubbles together when the avatar is ready', () => {
    const { container } = render(<LanguageBubbles />)
    const group = container.querySelector('[aria-hidden="true"].opacity-0')
    const loading = screen.getByRole('status', { name: 'loading' })

    expect(loading).toBeVisible()
    expect(loading.textContent).toBe('')
    expect(loading.querySelector('svg')).toHaveClass('motion-safe:animate-spin')
    expect(group).toHaveAttribute('aria-hidden', 'true')
    expect(group).toHaveClass('opacity-0')
    expect(screen.queryByRole('img', { name: 'FreeLingo' })).toBeNull()
    expect(screen.queryAllByRole('img', { name: /^Localized / })).toHaveLength(
      0
    )

    fireEvent.click(screen.getByTestId('lingu-ready'))

    expect(screen.queryByRole('status')).not.toBeInTheDocument()
    expect(group).toHaveAttribute('aria-hidden', 'false')
    expect(group).toHaveClass('opacity-100')
    expect(screen.getByRole('img', { name: 'FreeLingo' })).toBeInTheDocument()
    expect(screen.getAllByRole('img', { name: /^Localized / })).toHaveLength(
      6
    )
  })

  it('shows a small greeting sample with localized labels and target-language typography', () => {
    render(<LanguageBubbles />)
    fireEvent.click(screen.getByTestId('lingu-ready'))

    expect(screen.getAllByRole('img', { name: /^Localized / })).toHaveLength(
      6
    )
    expect(screen.getByAltText('Localized en-GB')).toHaveAttribute(
      'src',
      '/flags/uk.jpg'
    )
    expect(screen.getByAltText('Localized es-ES')).toHaveAttribute(
      'src',
      '/flags/spain.jpg'
    )
    expect(screen.getByAltText('Localized fr-FR')).toHaveAttribute(
      'src',
      '/flags/france.jpg'
    )
    expect(screen.getByAltText('Localized ja-JP')).toHaveAttribute(
      'src',
      '/flags/japan.jpg'
    )
    expect(screen.getByAltText('Localized de-DE')).toHaveAttribute(
      'src',
      '/flags/germany.jpg'
    )
    expect(screen.getByAltText('Localized it-IT')).toHaveAttribute(
      'src',
      '/flags/italy.jpg'
    )
    expect(screen.getByText('こんにちは！')).toHaveAttribute('lang', 'ja-JP')
    expect(screen.getByText('こんにちは！')).toHaveClass('font-target-ja')
    expect(screen.getByText('languageGreetings.en-GB')).toHaveAttribute(
      'lang',
      'en-GB'
    )
    expect(screen.getByText('languageGreetings.en-GB')).toHaveClass(
      'font-target-latin'
    )
    expect(screen.getByRole('img', { name: 'FreeLingo' })).toBeInTheDocument()
  })

  it('hydrates server markup without changing the initial loading presentation', () => {
    const container = document.createElement('div')
    container.innerHTML = renderToString(<LanguageBubbles />)
    const serverMarkup = container.innerHTML
    const consoleError = vi.spyOn(console, 'error').mockImplementation(() => {})
    try {
      render(<LanguageBubbles />, { container, hydrate: true })
      expect(consoleError).not.toHaveBeenCalled()
      expect(container.innerHTML).toBe(serverMarkup)
    } finally {
      consoleError.mockRestore()
    }
  })
})
