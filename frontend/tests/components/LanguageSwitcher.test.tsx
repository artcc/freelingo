import { describe, it, expect, vi, beforeEach } from 'vitest'
import { act, render, screen, fireEvent, waitFor } from '@testing-library/react'
import React from 'react'
import LanguageSwitcher from '@/components/LanguageSwitcher'
import { useLanguageStore } from '@/store/language'
import { SUPPORTED_TARGET_LANGUAGES } from '@/lib/target-languages'

vi.mock('next-intl', () => ({
  useTranslations: () => (key: string) => key,
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

const mockRefresh = vi.fn()
vi.mock('next/navigation', () => ({
  useRouter: () => ({ refresh: mockRefresh }),
}))

vi.mock('@/lib/api', () => ({
  apiFetch: vi.fn(),
}))

function seedStore(
  overrides: Partial<ReturnType<typeof useLanguageStore.getState>> = {}
) {
  useLanguageStore.setState({
    activeLanguage: SUPPORTED_TARGET_LANGUAGES[0],
    userLanguages: [
      {
        target_language: 'en-US',
        is_active: true,
        plan: {
          id: 1,
          cefr_level: 'B1',
          progress_day: 42,
          total_days: 48,
          completion_pct: 87.5,
        },
        progress: {
          total_xp: 12500,
          current_streak: 23,
          lessons_completed: 38,
        },
      },
    ],
    supportedLanguages: SUPPORTED_TARGET_LANGUAGES,
    availableLanguageCodes: ['en-US', 'en-GB', 'es-ES', 'it-IT', 'pt-PT'],
    isSwitching: false,
    fetchLanguages: vi.fn().mockResolvedValue(undefined),
    switchLanguage: vi.fn().mockResolvedValue(true),
    addLanguage: vi.fn().mockResolvedValue(true),
    removeLanguage: vi.fn().mockResolvedValue(true),
    ...overrides,
  })
}

describe('LanguageSwitcher', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    seedStore()
  })

  it('renders the active language name', () => {
    render(<LanguageSwitcher />)
    expect(screen.getByText('en-US')).toBeDefined()
  })

  it('disables both the selector and open choices during a global switch', () => {
    useLanguageStore.setState({
      userLanguages: [
        {
          target_language: 'en-US',
          is_active: true,
          plan: null,
          progress: null,
        },
        {
          target_language: 'de-DE',
          is_active: false,
          plan: null,
          progress: null,
        },
      ],
    })
    render(<LanguageSwitcher />)
    fireEvent.click(screen.getByRole('button'))
    act(() => useLanguageStore.setState({ isSwitching: true }))
    for (const button of screen.getAllByRole('button')) {
      expect(button).toBeDisabled()
      fireEvent.click(button)
    }
    expect(useLanguageStore.getState().switchLanguage).not.toHaveBeenCalled()
  })

  it('renders a loading skeleton when no active language', () => {
    useLanguageStore.setState({ activeLanguage: null })
    const { container } = render(<LanguageSwitcher />)
    expect(container.querySelector('.animate-pulse')).toBeTruthy()
  })

  it('does not open dropdown when only one language', () => {
    render(<LanguageSwitcher />)
    const button = screen.getByRole('button')
    fireEvent.click(button)
    // Dropdown shouldn't appear — only 1 language
    expect(screen.queryByText('en-GB')).toBeNull()
  })

  it('opens dropdown when multiple languages exist', () => {
    useLanguageStore.setState({
      userLanguages: [
        {
          target_language: 'en-US',
          is_active: true,
          plan: {
            id: 1,
            cefr_level: 'B1',
            progress_day: 42,
            total_days: 48,
            completion_pct: 87.5,
          },
          progress: {
            total_xp: 12500,
            current_streak: 23,
            lessons_completed: 38,
          },
        },
        {
          target_language: 'es-ES',
          is_active: false,
          plan: {
            id: 2,
            cefr_level: 'A1',
            progress_day: 3,
            total_days: 40,
            completion_pct: 7.5,
          },
          progress: { total_xp: 850, current_streak: 3, lessons_completed: 3 },
        },
      ],
    })

    render(<LanguageSwitcher />)
    const button = screen.getByRole('button')
    fireEvent.click(button)

    expect(screen.getByText('es-ES')).toBeDefined()
  })

  it('shows CEFR level in dropdown items', () => {
    useLanguageStore.setState({
      userLanguages: [
        {
          target_language: 'en-US',
          is_active: true,
          plan: {
            id: 1,
            cefr_level: 'B1',
            progress_day: 42,
            total_days: 48,
            completion_pct: 87.5,
          },
          progress: {
            total_xp: 12500,
            current_streak: 23,
            lessons_completed: 38,
          },
        },
        {
          target_language: 'es-ES',
          is_active: false,
          plan: {
            id: 2,
            cefr_level: 'A1',
            progress_day: 3,
            total_days: 40,
            completion_pct: 7.5,
          },
          progress: { total_xp: 850, current_streak: 3, lessons_completed: 3 },
        },
      ],
    })

    render(<LanguageSwitcher />)
    const button = screen.getByRole('button')
    fireEvent.click(button)

    expect(screen.getByText('A1')).toBeDefined()
  })

  it('shows checkmark on active language in dropdown', () => {
    useLanguageStore.setState({
      userLanguages: [
        {
          target_language: 'en-US',
          is_active: true,
          plan: {
            id: 1,
            cefr_level: 'B1',
            progress_day: 42,
            total_days: 48,
            completion_pct: 87.5,
          },
          progress: {
            total_xp: 12500,
            current_streak: 23,
            lessons_completed: 38,
          },
        },
        {
          target_language: 'es-ES',
          is_active: false,
          plan: {
            id: 2,
            cefr_level: 'A1',
            progress_day: 3,
            total_days: 40,
            completion_pct: 7.5,
          },
          progress: { total_xp: 850, current_streak: 3, lessons_completed: 3 },
        },
      ],
    })

    render(<LanguageSwitcher />)
    const button = screen.getByRole('button')
    fireEvent.click(button)

    expect(screen.getByText('✓')).toBeDefined()
  })

  it('calls switchLanguage and shows toast on switch', async () => {
    const mockSwitch = vi.fn().mockResolvedValue(true)
    useLanguageStore.setState({
      userLanguages: [
        {
          target_language: 'en-US',
          is_active: true,
          plan: {
            id: 1,
            cefr_level: 'B1',
            progress_day: 42,
            total_days: 48,
            completion_pct: 87.5,
          },
          progress: {
            total_xp: 12500,
            current_streak: 23,
            lessons_completed: 38,
          },
        },
        {
          target_language: 'es-ES',
          is_active: false,
          plan: {
            id: 2,
            cefr_level: 'A1',
            progress_day: 3,
            total_days: 40,
            completion_pct: 7.5,
          },
          progress: { total_xp: 850, current_streak: 3, lessons_completed: 3 },
        },
      ],
      switchLanguage: mockSwitch,
    })

    render(<LanguageSwitcher />)
    const button = screen.getByRole('button')
    fireEvent.click(button)

    const spanishBtn = screen.getByText('es-ES')
    fireEvent.click(spanishBtn)

    await waitFor(() => {
      expect(mockSwitch).toHaveBeenCalledWith('es-ES')
    })
  })

  it('calls router.refresh after successful language switch', async () => {
    const mockSwitch = vi.fn().mockResolvedValue(true)
    useLanguageStore.setState({
      userLanguages: [
        {
          target_language: 'en-US',
          is_active: true,
          plan: {
            id: 1,
            cefr_level: 'B1',
            progress_day: 42,
            total_days: 48,
            completion_pct: 87.5,
          },
          progress: {
            total_xp: 12500,
            current_streak: 23,
            lessons_completed: 38,
          },
        },
        {
          target_language: 'es-ES',
          is_active: false,
          plan: {
            id: 2,
            cefr_level: 'A1',
            progress_day: 3,
            total_days: 40,
            completion_pct: 7.5,
          },
          progress: { total_xp: 850, current_streak: 3, lessons_completed: 3 },
        },
      ],
      switchLanguage: mockSwitch,
    })

    mockRefresh.mockClear()
    render(<LanguageSwitcher />)
    const button = screen.getByRole('button')
    fireEvent.click(button)

    const spanishBtn = screen.getByText('es-ES')
    fireEvent.click(spanishBtn)

    await waitFor(() => {
      expect(mockRefresh).toHaveBeenCalled()
    })
  })

  it('shows ellipsis while switching', () => {
    useLanguageStore.setState({
      isSwitching: true,
      userLanguages: [
        {
          target_language: 'en-US',
          is_active: true,
          plan: {
            id: 1,
            cefr_level: 'B1',
            progress_day: 42,
            total_days: 48,
            completion_pct: 87.5,
          },
          progress: {
            total_xp: 12500,
            current_streak: 23,
            lessons_completed: 38,
          },
        },
        {
          target_language: 'es-ES',
          is_active: false,
          plan: {
            id: 2,
            cefr_level: 'A1',
            progress_day: 3,
            total_days: 40,
            completion_pct: 7.5,
          },
          progress: { total_xp: 850, current_streak: 3, lessons_completed: 3 },
        },
      ],
    })

    render(<LanguageSwitcher />)
    expect(screen.getByText('...')).toBeDefined()
  })

  it('calls fetchLanguages on mount', () => {
    const mockFetch = vi.fn().mockResolvedValue(undefined)
    seedStore({ fetchLanguages: mockFetch })

    render(<LanguageSwitcher />)
    expect(mockFetch).toHaveBeenCalled()
  })
})
