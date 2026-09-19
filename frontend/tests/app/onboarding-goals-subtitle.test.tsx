import { beforeEach, describe, expect, it, vi } from 'vitest'
import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import React from 'react'
import enMessages from '../../../messages/en.json'

const { mockApiFetch, mockPush } = vi.hoisted(() => ({
  mockApiFetch: vi.fn(),
  mockPush: vi.fn(),
}))

// Resolve real catalog strings with real {variable} interpolation; the
// repo's usual next-intl mock echoes keys and would hide this bug.
vi.mock('next-intl', async (importOriginal) => {
  const actual = await importOriginal<typeof import('next-intl')>()
  return {
    ...actual,
    useTranslations: (namespace: string) => {
      const messages = enMessages as Record<string, unknown>
      const scope = messages[namespace] as Record<string, unknown>
      return (key: string, values?: Record<string, string>) => {
        let raw: unknown = scope?.[key]
        if (raw === undefined && key.includes('.')) {
          raw = key
            .split('.')
            .reduce<
              Record<string, unknown> | undefined
            >((node, part) => (node && typeof node === 'object' ? (node[part] as Record<string, unknown>) : undefined), scope)
        }
        let text = typeof raw === 'string' ? raw : key
        for (const [name, value] of Object.entries(values ?? {})) {
          text = text.replaceAll(`{${name}}`, value)
        }
        return text
      }
    },
    // real useLocale needs a provider; pin the UI locale
    useLocale: () => 'en',
  }
})

vi.mock('next/navigation', () => ({
  useRouter: () => ({ push: mockPush }),
  useSearchParams: () => new URLSearchParams(),
  usePathname: () => '/onboarding',
}))

vi.mock('@/lib/api', () => ({
  apiFetch: mockApiFetch,
}))

vi.mock('@/store/auth', () => ({
  useAuthStore: (selector: (state: Record<string, unknown>) => unknown) =>
    selector({
      setUser: vi.fn(),
      user: {
        id: 1,
        username: 'tester',
        email: 'tester@example.com',
        role: 'admin',
        native_language: 'en',
        target_language: 'es-ES',
        is_active: true,
        is_verified: true,
      },
      isSubscribed: () => false,
      isFreemiumTrialActive: () => false,
    }),
  isSubscribed: () => false,
  isFreemiumTrialActive: () => false,
}))

vi.mock('@/store/config', () => ({
  useConfigStore: (selector: (state: Record<string, unknown>) => unknown) =>
    selector({
      stripeEnabled: false,
      stripeTrialDays: 7,
      priceMonthly: '14.95',
      priceYearly: '149.50',
      load: vi.fn(),
    }),
}))

const mockLanguageState = {
  fetchLanguages: vi.fn().mockResolvedValue(undefined),
  availableLanguageCodes: ['de-DE', 'en-GB', 'en-US', 'es-ES', 'fr-FR'],
}

vi.mock('@/store/language', () => {
  const useLanguageStore = (
    selector: (state: Record<string, unknown>) => unknown
  ) => selector(mockLanguageState)
  ;(useLanguageStore as unknown as Record<string, unknown>).getState = () =>
    mockLanguageState
  return { useLanguageStore }
})

import OnboardingPage from '@/app/(auth)/onboarding/page'

describe('onboarding goals subtitle', () => {
  beforeEach(() => {
    mockApiFetch.mockReset()
    mockPush.mockReset()
  })

  it('names the selected language on the goals step', async () => {
    render(React.createElement(OnboardingPage))

    // step 1: pick Spanish, continue
    await waitFor(() =>
      expect(screen.getAllByRole('button').length).toBeGreaterThan(0)
    )
    fireEvent.click(screen.getByRole('button', { name: /Spanish/i }))
    fireEvent.click(screen.getByRole('button', { name: /^next$/i }))

    // step 2: the subtitle must name the picked language, not English
    await waitFor(() => {
      expect(screen.getByText(/Select all that apply/)).toBeDefined()
    })
    const subtitle = screen.getByText(/Select all that apply/).textContent
    expect(subtitle).toBe(
      'What do you want to use Spanish for? Select all that apply.'
    )
    expect(subtitle).not.toContain('English')
  })
})
