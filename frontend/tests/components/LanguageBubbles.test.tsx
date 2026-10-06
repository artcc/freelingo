import { describe, expect, it, vi } from 'vitest'
import { fireEvent, render, screen } from '@testing-library/react'
import React from 'react'
import { LanguageBubbles } from '@/components/LanguageBubbles'
import { SUPPORTED_TARGET_LANGUAGES } from '@/lib/target-languages'

vi.mock('next-intl', () => ({
  useTranslations: (namespace: string) => (key: string) =>
    namespace === 'targetLanguages' ? `Localized ${key}` : key,
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
  it('reveals Lingu and the language circle together when the avatar is ready', () => {
    const { container } = render(<LanguageBubbles />)
    const group = container.firstElementChild

    expect(group).toHaveAttribute('aria-hidden', 'true')
    expect(group).toHaveClass('opacity-0')
    expect(screen.queryByRole('img', { name: 'FreeLingo' })).toBeNull()
    expect(screen.queryAllByRole('img', { name: /^Localized / })).toHaveLength(0)

    fireEvent.click(screen.getByTestId('lingu-ready'))

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
    expect(screen.getByRole('img', { name: 'FreeLingo' })).toBeInTheDocument()
  })

  it('positions bubbles dynamically from the supported language count', () => {
    const { container } = render(<LanguageBubbles />)
    const wrappers = Array.from(
      container.querySelectorAll<HTMLDivElement>('div[style]')
    ).filter((el) => el.style.left.includes('calc(50%'))

    expect(wrappers).toHaveLength(SUPPORTED_TARGET_LANGUAGES.length)
    expect(new Set(wrappers.map((el) => el.style.left)).size).toBeGreaterThan(1)
    expect(new Set(wrappers.map((el) => el.style.top)).size).toBeGreaterThan(1)
  })
})
