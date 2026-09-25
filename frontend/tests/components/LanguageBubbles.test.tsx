import { describe, expect, it, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import React from 'react'
import { LanguageBubbles } from '@/components/LanguageBubbles'
import { SUPPORTED_TARGET_LANGUAGES } from '@/lib/target-languages'

vi.mock('next-intl', () => ({
  useTranslations: (namespace: string) => (key: string) =>
    namespace === 'targetLanguages' ? `Localized ${key}` : key,
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
  it('renders one bubble per supported target language', () => {
    render(<LanguageBubbles />)

    expect(screen.getAllByRole('img')).toHaveLength(
      SUPPORTED_TARGET_LANGUAGES.length
    )
    expect(screen.getByAltText('Localized de-DE')).toBeInTheDocument()
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
