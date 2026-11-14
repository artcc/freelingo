import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import React from 'react'
import TargetLanguageSelector from '@/components/TargetLanguageSelector'
import { TARGET_LANGUAGE_CATALOG } from '@/lib/target-languages'

vi.mock('next-intl', () => ({
  useTranslations: () => (key: string) => key,
}))

vi.mock('next/image', () => ({
  default: function MockImage({
    src,
    alt,
    width,
    height,
    className,
  }: {
    src: string
    alt: string
    width: number
    height: number
    className?: string
  }) {
    return React.createElement('img', { src, alt, width, height, className })
  },
}))

describe('TargetLanguageSelector', () => {
  const allCodes = [
    'en-US',
    'en-GB',
    'es-ES',
    'it-IT',
    'pt-PT',
    'fr-FR',
    'de-DE',
  ]
  const catalogCodes = TARGET_LANGUAGE_CATALOG.map((lang) => lang.code)

  it('renders only languages matching availableCodes', () => {
    render(
      <TargetLanguageSelector
        value="en-GB"
        onChange={() => {}}
        availableCodes={['en-US', 'en-GB']}
      />
    )

    const buttons = screen.getAllByRole('button')
    expect(buttons).toHaveLength(2)
  })

  it('renders all languages when all codes are available', () => {
    render(
      <TargetLanguageSelector
        value="en-GB"
        onChange={() => {}}
        availableCodes={catalogCodes}
      />
    )

    const buttons = screen.getAllByRole('button')
    expect(buttons).toHaveLength(17)
  })

  it('renders nothing when availableCodes is empty', () => {
    const { container } = render(
      <TargetLanguageSelector
        value="en-GB"
        onChange={() => {}}
        availableCodes={[]}
      />
    )

    expect(screen.queryByRole('button')).toBeNull()
    const div = container.firstChild as HTMLElement
    expect(div.children).toHaveLength(0)
  })

  it('renders CJK catalog languages when availableCodes includes them', () => {
    render(
      <TargetLanguageSelector
        value="en-GB"
        onChange={() => {}}
        availableCodes={['ja-JP', 'ko-KR']}
      />
    )

    const buttons = screen.getAllByRole('button')
    expect(buttons).toHaveLength(2)
    expect(buttons.map((button) => button.textContent).join(' ')).toContain(
      'ja-JP'
    )
    expect(buttons.map((button) => button.textContent).join(' ')).toContain(
      'ko-KR'
    )
  })

  it('renders the Polish catalog entry when availableCodes includes it', () => {
    render(
      <TargetLanguageSelector
        value="en-GB"
        onChange={() => {}}
        availableCodes={['pl-PL']}
      />
    )

    const buttons = screen.getAllByRole('button')
    expect(buttons).toHaveLength(1)
    expect(buttons[0].textContent).toContain('pl-PL')
    expect(screen.getByRole('img').getAttribute('src')).toBe(
      '/flags/poland.jpg'
    )
  })

  it('selects Brazil independently and excludes it when disabled', () => {
    const onChange = vi.fn()
    const { rerender } = render(
      <TargetLanguageSelector
        value="pt-PT"
        onChange={onChange}
        availableCodes={['pt-BR', 'pt-PT']}
      />
    )
    expect(screen.getAllByRole('img').map((img) => img.getAttribute('src'))).toEqual([
      '/flags/brazil.jpg',
      '/flags/portugal.jpg',
    ])
    fireEvent.click(screen.getByRole('button', { name: /pt-BR/ }))
    expect(onChange).toHaveBeenCalledWith('pt-BR')
    rerender(
      <TargetLanguageSelector
        value="pt-PT"
        onChange={onChange}
        availableCodes={['pt-PT']}
      />
    )
    expect(screen.queryByRole('button', { name: /pt-BR/ })).toBeNull()
    expect(screen.getAllByRole('button')).toHaveLength(1)
  })

  it('selects Dutch only when enabled by the backend', () => {
    const onChange = vi.fn()
    const { rerender } = render(
      <TargetLanguageSelector
        value="en-GB"
        onChange={onChange}
        availableCodes={['en-GB', 'nl-NL']}
      />
    )
    fireEvent.click(screen.getByRole('button', { name: /nl-NL/ }))
    expect(onChange).toHaveBeenCalledWith('nl-NL')
    rerender(
      <TargetLanguageSelector
        value="en-GB"
        onChange={onChange}
        availableCodes={['en-GB']}
      />
    )
    expect(screen.queryByRole('button', { name: /nl-NL/ })).toBeNull()
  })

  it.each([
    ['ru-RU', '/flags/russia.jpg'],
    ['sv-SE', '/flags/sweden.jpg'],
    ['da-DK', '/flags/denmark.jpg'],
    ['cs-CZ', '/flags/czech_republic.jpg'],
  ])('selects %s with its flag only while enabled by the backend', (code, flag) => {
    const onChange = vi.fn()
    const { rerender } = render(
      <TargetLanguageSelector
        value="en-GB"
        onChange={onChange}
        availableCodes={['en-GB', code, 'xx-XX']}
      />
    )
    expect(screen.getAllByRole('button')).toHaveLength(2)
    expect(screen.getByAltText(code)).toHaveAttribute('src', flag)
    fireEvent.click(screen.getByRole('button', { name: new RegExp(code) }))
    expect(onChange).toHaveBeenCalledWith(code)
    rerender(
      <TargetLanguageSelector
        value="en-GB"
        onChange={onChange}
        availableCodes={['en-GB']}
      />
    )
    expect(screen.queryByRole('button', { name: new RegExp(code) })).toBeNull()
    expect(screen.getAllByRole('button')).toHaveLength(1)
  })

  it('shows active state for the selected language', () => {
    render(
      <TargetLanguageSelector
        value="es-ES"
        onChange={() => {}}
        availableCodes={allCodes}
      />
    )

    const buttons = screen.getAllByRole('button')
    const activeButton = buttons.find((btn) =>
      btn.className.includes('bg-fl-accent')
    )

    expect(activeButton).toBeDefined()
    expect(activeButton!.textContent).toContain('es-ES')
  })

  it('calls onChange with the clicked code', () => {
    const onChange = vi.fn()

    render(
      <TargetLanguageSelector
        value="en-GB"
        onChange={onChange}
        availableCodes={allCodes}
      />
    )

    const buttons = screen.getAllByRole('button')
    const italianButton = buttons.find((btn) =>
      btn.textContent?.includes('it-IT')
    )

    expect(italianButton).toBeDefined()
    fireEvent.click(italianButton!)

    expect(onChange).toHaveBeenCalledWith('it-IT')
  })

  it('calls onChange when clicking already-selected language', () => {
    const onChange = vi.fn()

    render(
      <TargetLanguageSelector
        value="en-GB"
        onChange={onChange}
        availableCodes={['en-GB', 'en-US']}
      />
    )

    const buttons = screen.getAllByRole('button')
    const activeButton = buttons.find((btn) =>
      btn.className.includes('bg-fl-accent')
    )

    fireEvent.click(activeButton!)

    expect(onChange).toHaveBeenCalledWith('en-GB')
  })

  it('renders flag images with correct src', () => {
    render(
      <TargetLanguageSelector
        value="en-US"
        onChange={() => {}}
        availableCodes={catalogCodes}
      />
    )

    const images = screen.getAllByRole('img')
    const srcs = images.map((img) => img.getAttribute('src'))

    expect(srcs).toContain('/flags/usa.jpg')
    expect(srcs).toContain('/flags/uk.jpg')
    expect(srcs).toContain('/flags/spain.jpg')
    expect(srcs).toContain('/flags/italy.jpg')
    expect(srcs).toContain('/flags/portugal.jpg')
    expect(srcs).toContain('/flags/france.jpg')
    expect(srcs).toContain('/flags/germany.jpg')
    expect(srcs).toContain('/flags/netherlands.jpg')
    expect(srcs).toContain('/flags/russia.jpg')
    expect(srcs).toContain('/flags/denmark.jpg')
    expect(srcs).toContain('/flags/czech_republic.jpg')
    expect(srcs).toContain('/flags/japan.jpg')
    expect(srcs).toContain('/flags/south_korea.jpg')
    expect(srcs).toContain('/flags/china.jpg')
  })

  it('displays translated names from targetLanguages namespace', () => {
    render(
      <TargetLanguageSelector
        value="en-GB"
        onChange={() => {}}
        availableCodes={allCodes}
      />
    )

    const buttons = screen.getAllByRole('button')
    const textContent = buttons.map((b) => b.textContent).join(' ')

    expect(textContent).toContain('en-US')
    expect(textContent).toContain('en-GB')
    expect(textContent).toContain('es-ES')
    expect(textContent).toContain('it-IT')
    expect(textContent).toContain('pt-PT')
    expect(textContent).toContain('fr-FR')
    expect(textContent).toContain('de-DE')
  })

  it('does not re-render filtered languages when onChange does not change', () => {
    const { rerender } = render(
      <TargetLanguageSelector
        value="en-GB"
        onChange={() => {}}
        availableCodes={['en-GB', 'en-US']}
      />
    )

    rerender(
      <TargetLanguageSelector
        value="en-GB"
        onChange={() => {}}
        availableCodes={['en-GB', 'en-US']}
      />
    )

    expect(screen.getAllByRole('button')).toHaveLength(2)
  })
})
