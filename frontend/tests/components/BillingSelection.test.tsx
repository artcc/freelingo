import { beforeEach, describe, expect, it, vi } from 'vitest'
import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import React from 'react'

const { selection, createCheckout } = vi.hoisted(() => ({
  selection: { value: '' },
  createCheckout: vi.fn(),
}))
vi.mock('next/navigation', () => ({
  useSearchParams: () => new URLSearchParams(selection.value),
}))
vi.mock('next-intl', () => ({
  useLocale: () => 'en',
  useTranslations: () => (key: string) => key,
}))
vi.mock('@/lib/billing', () => ({ createCheckout }))

import { BillingSection } from '@/components/settings/BillingSection'
import { useAuthStore } from '@/store/auth'
import { useConfigStore } from '@/store/config'

beforeEach(() => {
  createCheckout.mockReset()
  createCheckout.mockResolvedValue(null)
  useAuthStore.getState().startSession('token')
  useAuthStore.getState().setUser({
    id: 1,
    username: 'learner',
    displayName: 'Learner',
    role: 'user',
    conversation_max_duration: 900,
    conversation_inactivity_timeout: 60,
    subscription_status: 'none',
    trial_used: false,
  })
  useConfigStore.setState({
    stripeEnabled: true,
    loaded: true,
    stripeTrialDays: 0,
    priceMonthly: 10,
    priceYearly: 100,
  })
})

describe('settings plan selection', () => {
  it.each([
    ['plan=monthly', 'monthly'],
    ['plan=yearly', 'yearly'],
    ['', 'monthly'],
    ['plan=invalid', 'monthly'],
    ['plan=https%3A%2F%2Fexample.com', 'monthly'],
  ])('preserves a whitelisted selection from %s without automatic checkout', async (
    query,
    selected
  ) => {
    selection.value = query
    render(<BillingSection />)
    const buttons = screen.getAllByRole('button')
    expect(buttons[0]).toHaveTextContent(
      selected === 'monthly' ? 'planMonthly' : 'planYearly'
    )
    expect(buttons[1]).toHaveTextContent(
      selected === 'monthly' ? 'planYearly' : 'planMonthly'
    )
    expect(createCheckout).not.toHaveBeenCalled()
    fireEvent.click(buttons[0])
    await waitFor(() => {
      expect(createCheckout).toHaveBeenCalledWith(
        selected, expect.any(AbortSignal)
      )
    })
  })
})
