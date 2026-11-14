import { describe, expect, it, vi } from 'vitest'
import { fireEvent, render, screen } from '@testing-library/react'
import React from 'react'
import { renderToString } from 'react-dom/server'
import { LanguageBubbles } from '@/components/LanguageBubbles'
import { SUPPORTED_TARGET_LANGUAGES } from '@/lib/target-languages'

vi.mock('next-intl', () => ({
  useTranslations: (namespace: string) => (key: string) =>
    namespace === 'targetLanguages'
      ? `Localized ${key}`
      : key === 'languageGreetings.ru-RU'
        ? 'Привет!'
        : key === 'languageGreetings.sv-SE' ||
            key === 'languageGreetings.da-DK'
          ? 'Hej!'
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
      SUPPORTED_TARGET_LANGUAGES.length
    )
  })

  it('renders one bubble per supported target language', () => {
    render(<LanguageBubbles />)
    fireEvent.click(screen.getByTestId('lingu-ready'))

    expect(screen.getAllByRole('img', { name: /^Localized / })).toHaveLength(
      SUPPORTED_TARGET_LANGUAGES.length
    )
    expect(screen.getByAltText('Localized de-DE')).toBeInTheDocument()
    expect(screen.getByAltText('Localized nl-NL')).toHaveAttribute(
      'src',
      '/flags/netherlands.jpg'
    )
    expect(screen.getByAltText('Localized pt-BR')).toHaveAttribute(
      'src',
      '/flags/brazil.jpg'
    )
    expect(screen.getByAltText('Localized ru-RU')).toHaveAttribute(
      'src',
      '/flags/russia.jpg'
    )
    expect(screen.getByText('Привет!')).toHaveAttribute('lang', 'ru-RU')
    expect(screen.getByText('Привет!')).toHaveClass('font-target-cyrillic')
    expect(screen.getByAltText('Localized sv-SE')).toHaveAttribute(
      'src',
      '/flags/sweden.jpg'
    )
    expect(screen.getByAltText('Localized da-DK')).toHaveAttribute(
      'src',
      '/flags/denmark.jpg'
    )
    const greetings = screen.getAllByText('Hej!')
    expect(greetings).toHaveLength(2)
    expect(greetings.map((greeting) => greeting.getAttribute('lang'))).toEqual([
      'sv-SE',
      'da-DK',
    ])
    for (const greeting of greetings) {
      expect(greeting).toHaveClass('font-target-latin')
    }
    expect(screen.getByRole('img', { name: 'FreeLingo' })).toBeInTheDocument()
  })

  it('uses a wider desktop orbit and wrapping mobile layout for all languages', () => {
    const { container } = render(<LanguageBubbles />)
    const wrappers = Array.from(
      container.querySelectorAll<HTMLDivElement>('div[style]')
    ).filter((el) => el.style.getPropertyValue('--bubble-x'))

    expect(container.querySelector('.flex-wrap')).toHaveClass('gap-y-4')
    expect(wrappers).toHaveLength(SUPPORTED_TARGET_LANGUAGES.length)
    const xPositions = wrappers.map((el) =>
      Number.parseFloat(el.style.getPropertyValue('--bubble-x'))
    )
    expect(Math.max(...xPositions) - Math.min(...xPositions)).toBeGreaterThan(
      420
    )
    for (const wrapper of wrappers) {
      expect(wrapper).toHaveClass('relative', 'sm:absolute')
      const x = Number.parseFloat(wrapper.style.getPropertyValue('--bubble-x'))
      const y = Number.parseFloat(wrapper.style.getPropertyValue('--bubble-y'))
      expect(Math.hypot(x / 215, y / 140)).toBeCloseTo(1, 2)
    }
  })

  it('hydrates server markup despite tiny differences in trigonometric precision', () => {
    const cos = Math.cos
    const sin = Math.sin
    const serverCos = vi
      .spyOn(Math, 'cos')
      .mockImplementation((angle) => cos(angle) + 1e-15)
    const serverSin = vi
      .spyOn(Math, 'sin')
      .mockImplementation((angle) => sin(angle) - 1e-15)
    const container = document.createElement('div')
    try {
      container.innerHTML = renderToString(<LanguageBubbles />)
    } finally {
      serverCos.mockRestore()
      serverSin.mockRestore()
    }

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
