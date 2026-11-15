import React from 'react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import {
  act,
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from '@testing-library/react'
import { useAuthStore, type User } from '@/store/auth'
import { useConfigStore } from '@/store/config'
import { useLanguageStore } from '@/store/language'

const { searchParams, push, apiFetch, createCheckout, restoreAccessToken } =
  vi.hoisted(() => ({
    searchParams: new URLSearchParams(),
    push: vi.fn(),
    apiFetch: vi.fn(),
    createCheckout: vi.fn(),
    restoreAccessToken: vi.fn(),
  }))

vi.mock('next/navigation', () => ({
  useRouter: () => ({ push }),
  useSearchParams: () => searchParams,
}))

vi.mock('next-intl', () => ({
  useLocale: () => 'en',
  useTranslations: () => (key: string) => key,
}))

vi.mock('@/lib/api', () => ({ apiFetch, restoreAccessToken }))
vi.mock('@/lib/billing', () => ({ createCheckout }))

import OnboardingPage from '@/app/(auth)/onboarding/page'

const learner: User = {
  id: 1,
  username: 'learner',
  displayName: 'Learner',
  role: 'user',
  conversation_max_duration: 900,
  conversation_inactivity_timeout: 60,
  learning_goals: null,
  subscription_status: 'none',
  trial_used: false,
  freemium_trial_ends_at: '2099-01-01T00:00:00Z',
}

beforeEach(() => {
  for (const key of Array.from(searchParams.keys())) searchParams.delete(key)
  push.mockReset()
  apiFetch.mockReset()
  createCheckout.mockReset()
  restoreAccessToken.mockReset()
  createCheckout.mockResolvedValue(null)
  apiFetch.mockImplementation(async () =>
    new Response(
      JSON.stringify({
        ...learner,
        ...useAuthStore.getState().user,
        display_name: 'Learner',
        learning_goals: [],
      })
    )
  )
  useAuthStore.setState(
    { ...useAuthStore.getInitialState(), accessToken: 'token', user: learner },
    true
  )
  useConfigStore.setState(
    {
      ...useConfigStore.getInitialState(),
      loaded: true,
      stripeEnabled: true,
      stripeTrialDays: 0,
      freemiumTrialEnabled: true,
    },
    true
  )
  useLanguageStore.setState(
    {
      ...useLanguageStore.getInitialState(),
      availableLanguageCodes: ['en-GB'],
      fetchLanguages: vi.fn().mockResolvedValue(true),
    },
    true
  )
})

afterEach(() => {
  cleanup()
  vi.useRealTimers()
})

async function completeGoals() {
  await act(async () => {
    await Promise.resolve()
  })
  await act(async () =>
    fireEvent.click(screen.getByRole('button', { name: 'next' }))
  )
  await act(async () =>
    fireEvent.click(screen.getByRole('button', { name: 'continue' }))
  )
}

describe('onboarding purchase intent', () => {
  it('restores a fresh page session before loading languages and completing the selected plan', async () => {
    searchParams.set('plan', 'monthly')
    useAuthStore.setState({ accessToken: null, user: null })
    let finishRestore!: () => void
    restoreAccessToken.mockImplementationOnce(
      () =>
        new Promise<void>((resolve) => {
          finishRestore = () => {
            useAuthStore.getState().setTokens('restored-token')
            resolve()
          }
        })
    )
    const fetchLanguages = vi.mocked(useLanguageStore.getState().fetchLanguages)
    render(<OnboardingPage />)
    expect(restoreAccessToken).toHaveBeenCalledWith(expect.any(AbortSignal))
    expect(fetchLanguages).not.toHaveBeenCalled()
    expect(apiFetch).not.toHaveBeenCalled()

    await act(async () => finishRestore())
    expect(fetchLanguages).toHaveBeenCalledWith(expect.any(AbortSignal))
    expect(screen.getByRole('button', { name: /en-GB/ })).toBeInTheDocument()
    await completeGoals()
    expect(apiFetch).toHaveBeenCalledWith(
      '/api/auth/me',
      expect.objectContaining({ method: 'PATCH' })
    )
    expect(
      screen.getByRole('button', { name: 'trialCtaMonthlyTrialUsed' })
    ).toBeInTheDocument()
    expect(push).not.toHaveBeenCalled()
    expect(createCheckout).not.toHaveBeenCalled()
  })

  it('restores a missing token before saving onboarding preferences', async () => {
    render(<OnboardingPage />)
    await screen.findByRole('button', { name: /en-GB/ })
    useAuthStore.setState({ accessToken: null })
    restoreAccessToken.mockImplementationOnce(async () => {
      expect(apiFetch).not.toHaveBeenCalled()
      useAuthStore.getState().setTokens('restored-token')
    })

    await completeGoals()
    expect(restoreAccessToken).toHaveBeenCalledWith(expect.any(AbortSignal))
    expect(apiFetch).toHaveBeenCalledTimes(1)
    expect(screen.getByRole('button', { name: 'goToDashboard' })).toBeEnabled()
  })

  it.each(['replace-session', 'unmount'])(
    'does not load languages after an obsolete restoration (%s)',
    async (action) => {
      useAuthStore.setState({ accessToken: null })
      let finishRestore!: () => void
      restoreAccessToken.mockReturnValueOnce(
        new Promise<void>((resolve) => {
          finishRestore = resolve
        })
      )
      const fetchLanguages = vi.mocked(
        useLanguageStore.getState().fetchLanguages
      )
      const { unmount } = render(<OnboardingPage />)
      if (action === 'unmount') unmount()
      else act(() => useAuthStore.getState().startSession('replacement-token'))
      await act(async () => finishRestore())

      expect(fetchLanguages).not.toHaveBeenCalled()
      expect(apiFetch).not.toHaveBeenCalled()
      expect(push).not.toHaveBeenCalled()
      if (action === 'unmount') {
        expect(restoreAccessToken.mock.calls[0][0].aborted).toBe(true)
      }
    }
  )

  it('allows retrying an authentication restoration failure before loading languages', async () => {
    useAuthStore.setState({ accessToken: null })
    restoreAccessToken.mockRejectedValueOnce(new Error('network'))
    const fetchLanguages = vi.mocked(useLanguageStore.getState().fetchLanguages)
    render(<OnboardingPage />)
    const retry = await screen.findByRole('button', { name: 'retry' })
    expect(fetchLanguages).not.toHaveBeenCalled()
    restoreAccessToken.mockImplementationOnce(async () => {
      useAuthStore.getState().setTokens('restored-token')
    })

    await act(async () => fireEvent.click(retry))
    expect(screen.queryByRole('button', { name: 'retry' })).toBeNull()
    expect(screen.getByRole('button', { name: /en-GB/ })).toBeInTheDocument()
  })

  it('finishes a successful language retry and replaces an unavailable default language', async () => {
    useLanguageStore.setState({ availableLanguageCodes: [] })
    const fetchLanguages = vi.mocked(useLanguageStore.getState().fetchLanguages)
    fetchLanguages.mockResolvedValueOnce(false)
    render(<OnboardingPage />)
    const retry = await screen.findByRole('button', { name: 'retry' })
    fetchLanguages.mockImplementationOnce(async () => {
      useLanguageStore.setState({ availableLanguageCodes: ['fr-FR'] })
      return true
    })

    await act(async () => fireEvent.click(retry))
    expect(screen.queryByRole('button', { name: 'retry' })).toBeNull()
    expect(screen.getByRole('button', { name: /fr-FR/ })).toBeInTheDocument()
    await completeGoals()
    expect(JSON.parse(apiFetch.mock.calls[0][1].body)).toEqual({
      target_language: 'fr-FR',
      learning_goals: [],
    })
  })

  it('blocks step one while languages are pending or failed and advances only after a valid retry', async () => {
    const fetchLanguages = vi.mocked(useLanguageStore.getState().fetchLanguages)
    let finishLanguages!: (success: boolean) => void
    fetchLanguages.mockReturnValueOnce(
      new Promise<boolean>((resolve) => {
        finishLanguages = resolve
      })
    )
    const { container } = render(<OnboardingPage />)
    const next = screen.getByRole('button', { name: 'next' })
    expect(next).toBeDisabled()
    fireEvent.click(next)
    fireEvent.submit(container.querySelector('form')!)
    expect(screen.queryByRole('button', { name: 'continue' })).toBeNull()

    await act(async () => finishLanguages(false))
    expect(next).toBeDisabled()
    fireEvent.click(next)
    fireEvent.submit(container.querySelector('form')!)
    expect(screen.queryByRole('button', { name: 'continue' })).toBeNull()
    expect(apiFetch).not.toHaveBeenCalled()

    fetchLanguages.mockReturnValueOnce(
      new Promise<boolean>((resolve) => {
        finishLanguages = resolve
      })
    )
    fireEvent.click(screen.getByRole('button', { name: 'retry' }))
    expect(next).toBeDisabled()
    fireEvent.submit(container.querySelector('form')!)
    expect(screen.queryByRole('button', { name: 'continue' })).toBeNull()

    await act(async () => {
      useLanguageStore.setState({ availableLanguageCodes: ['fr-FR'] })
      finishLanguages(true)
    })
    expect(next).toBeEnabled()
    expect(screen.getByRole('button', { name: /fr-FR/ })).toBeInTheDocument()
    await completeGoals()
    expect(JSON.parse(apiFetch.mock.calls[0][1].body).target_language).toBe(
      'fr-FR'
    )
  })

  it('keeps step one blocked when a successful lookup has no available selection', async () => {
    useLanguageStore.setState({ availableLanguageCodes: [] })
    const { container } = render(<OnboardingPage />)
    await screen.findByRole('button', { name: 'retry' })
    expect(screen.getByRole('button', { name: 'next' })).toBeDisabled()
    fireEvent.submit(container.querySelector('form')!)
    expect(screen.queryByRole('button', { name: 'continue' })).toBeNull()
    expect(apiFetch).not.toHaveBeenCalled()
  })

  it('keeps another language retry available if recovery also fails', async () => {
    useLanguageStore.setState({ availableLanguageCodes: [] })
    vi.mocked(useLanguageStore.getState().fetchLanguages).mockResolvedValue(false)
    render(<OnboardingPage />)
    const retry = await screen.findByRole('button', { name: 'retry' })
    await act(async () => fireEvent.click(retry))
    expect(screen.getByRole('button', { name: 'retry' })).toBeEnabled()
    expect(apiFetch).not.toHaveBeenCalled()
  })

  it('waits for pending billing configuration before saving and retains the selected plan', async () => {
    searchParams.set('plan', 'yearly')
    let finishConfig!: () => void
    const pendingConfig = new Promise<void>((resolve) => {
      finishConfig = resolve
    })
    useConfigStore.setState({
      loaded: false,
      stripeEnabled: false,
      load: vi.fn(() => pendingConfig),
    })
    render(<OnboardingPage />)
    await completeGoals()
    expect(apiFetch).not.toHaveBeenCalled()
    expect(push).not.toHaveBeenCalled()
    expect(screen.getByRole('button', { name: 'saving' })).toBeDisabled()

    await act(async () => {
      useConfigStore.setState({ loaded: true, stripeEnabled: true })
      finishConfig()
    })
    expect(apiFetch).toHaveBeenCalledTimes(1)
    expect(screen.getAllByRole('button')[0]).toHaveTextContent(
      'trialCtaYearlyTrialUsed'
    )
    expect(push).not.toHaveBeenCalled()
    expect(createCheckout).not.toHaveBeenCalled()
  })

  it('offers recovery after failed configuration without discarding the selected plan', async () => {
    searchParams.set('plan', 'monthly')
    const loadConfig = vi.fn().mockResolvedValue(undefined)
    useConfigStore.setState({
      loaded: false,
      stripeEnabled: false,
      load: loadConfig,
    })
    render(<OnboardingPage />)
    await completeGoals()
    expect(screen.getByText('✕ saveFailed')).toBeInTheDocument()
    expect(apiFetch).not.toHaveBeenCalled()
    expect(push).not.toHaveBeenCalled()
    expect(searchParams.get('plan')).toBe('monthly')

    loadConfig.mockImplementationOnce(async () => {
      useConfigStore.setState({ loaded: true, stripeEnabled: true })
    })
    await act(async () =>
      fireEvent.click(screen.getByRole('button', { name: 'retry' }))
    )
    expect(apiFetch).toHaveBeenCalledTimes(1)
    expect(screen.getAllByRole('button')[0]).toHaveTextContent(
      'trialCtaMonthlyTrialUsed'
    )
    expect(push).not.toHaveBeenCalled()
    expect(createCheckout).not.toHaveBeenCalled()
  })

  it('replaces no-card trial confirmation when it expires while the page is open', async () => {
    vi.useFakeTimers()
    vi.setSystemTime(new Date('2030-01-01T00:00:00Z'))
    useAuthStore.setState({
      user: {
        ...learner,
        freemium_trial_ends_at: '2030-01-01T00:00:01Z',
      },
    })
    render(<OnboardingPage />)
    await completeGoals()
    expect(
      screen.getByRole('heading', { name: 'freemiumTrialTitle' })
    ).toBeInTheDocument()

    await act(async () => {
      await vi.advanceTimersByTimeAsync(1001)
    })

    expect(
      screen.queryByRole('heading', { name: 'freemiumTrialTitle' })
    ).not.toBeInTheDocument()
    expect(
      screen.getByRole('button', { name: 'trialCtaMonthlyTrialUsed' })
    ).toBeInTheDocument()
    expect(createCheckout).not.toHaveBeenCalled()
    expect(push).not.toHaveBeenCalled()
  })

  it('updates trial confirmation after runtime flag changes and keeps a usable completion action', async () => {
    render(<OnboardingPage />)
    await completeGoals()
    expect(
      screen.getByRole('heading', { name: 'freemiumTrialTitle' })
    ).toBeInTheDocument()

    act(() => useConfigStore.setState({ freemiumTrialEnabled: false }))
    expect(
      screen.queryByRole('heading', { name: 'freemiumTrialTitle' })
    ).not.toBeInTheDocument()
    expect(
      screen.getByRole('button', { name: 'trialCtaMonthlyTrialUsed' })
    ).toBeInTheDocument()

    act(() => useConfigStore.setState({ stripeEnabled: false }))
    expect(
      screen.queryByRole('button', { name: 'trialCtaMonthlyTrialUsed' })
    ).not.toBeInTheDocument()
    expect(screen.getByText('3/3')).toBeInTheDocument()
    fireEvent.click(screen.getByRole('button', { name: 'goToDashboard' }))
    expect(push).toHaveBeenCalledWith('/dashboard')
    expect(createCheckout).not.toHaveBeenCalled()
  })

  it.each(['monthly', 'yearly'])(
    'offers the selected %s plan during a no-card trial and waits for a click',
    async (plan) => {
      searchParams.set('plan', plan)
      render(<OnboardingPage />)
      await completeGoals()

      expect(screen.getByText('trialTitleTrialUsed')).toBeInTheDocument()
      expect(screen.getByText('trialNoChargeTrialUsed')).toBeInTheDocument()
      expect(createCheckout).not.toHaveBeenCalled()
      expect(push).not.toHaveBeenCalled()
      const buttons = screen.getAllByRole('button')
      expect(buttons[0]).toHaveTextContent(
        plan === 'monthly'
          ? 'trialCtaMonthlyTrialUsed'
          : 'trialCtaYearlyTrialUsed'
      )
      expect(screen.getByRole('button', { name: 'trialSkip' })).toBeEnabled()

      await act(async () => fireEvent.click(buttons[0]))
      expect(createCheckout).toHaveBeenCalledWith(plan, expect.any(AbortSignal))
      expect(push).toHaveBeenCalledWith('/dashboard')
    }
  )

  it('allows continuing free with an explicitly selected paid plan', async () => {
    searchParams.set('plan', 'yearly')
    render(<OnboardingPage />)
    await completeGoals()
    fireEvent.click(screen.getByRole('button', { name: 'trialSkip' }))
    expect(push).toHaveBeenCalledWith('/dashboard')
    expect(createCheckout).not.toHaveBeenCalled()
  })

  it.each([null, 'unknown', 'https://example.com'])(
    'keeps no-card confirmation for plan=%s without offering checkout',
    async (plan) => {
      if (plan) searchParams.set('plan', plan)
      render(<OnboardingPage />)
      await completeGoals()
      expect(
        screen.getByRole('heading', { name: 'freemiumTrialTitle' })
      ).toBeInTheDocument()
      expect(
        screen.queryByText('trialCtaMonthlyTrialUsed')
      ).not.toBeInTheDocument()
      fireEvent.click(screen.getByRole('button', { name: 'goToDashboard' }))
      expect(push).toHaveBeenCalledWith('/dashboard')
      expect(createCheckout).not.toHaveBeenCalled()
    }
  )

  it.each([true, false, undefined])(
    'offers a card trial only when configured and unused (used=%s)',
    async (used) => {
      searchParams.set('plan', 'monthly')
      useAuthStore.setState({ user: { ...learner, trial_used: used } })
      useConfigStore.setState({ stripeTrialDays: 3 })
      render(<OnboardingPage />)
      await completeGoals()
      expect(
        screen.getByRole('button', {
          name: used === false ? 'trialCtaMonthly' : 'trialCtaMonthlyTrialUsed',
        })
      ).toBeInTheDocument()
      expect(
        screen.getByText(
          used === false ? 'trialNoCharge' : 'trialNoChargeTrialUsed'
        )
      ).toBeInTheDocument()
    }
  )

  it('keeps checkout available without promising a trial for a null eligibility response', async () => {
    searchParams.set('plan', 'monthly')
    useAuthStore.setState({ user: { ...learner, trial_used: undefined } })
    useConfigStore.setState({ stripeTrialDays: 3 })
    apiFetch.mockResolvedValueOnce(
      new Response(
        JSON.stringify({ ...learner, trial_used: null, learning_goals: [] })
      )
    )
    render(<OnboardingPage />)
    await completeGoals()
    expect(
      screen.getByRole('button', { name: 'trialCtaMonthlyTrialUsed' })
    ).toBeInTheDocument()
    expect(screen.queryByText('trialNoCharge')).not.toBeInTheDocument()
    expect(createCheckout).not.toHaveBeenCalled()
    await act(async () =>
      fireEvent.click(
        screen.getByRole('button', { name: 'trialCtaMonthlyTrialUsed' })
      )
    )
    expect(createCheckout).toHaveBeenCalledWith(
      'monthly',
      expect.any(AbortSignal)
    )
  })

  it.each(['stripe-disabled', 'subscribed'])(
    'does not offer a purchase when %s',
    async (condition) => {
      searchParams.set('plan', 'monthly')
      if (condition === 'stripe-disabled')
        useConfigStore.setState({ stripeEnabled: false })
      else {
        useAuthStore.setState({
          user: {
            ...learner,
            subscription_status: 'active',
            freemium_trial_ends_at: null,
          },
        })
      }
      render(<OnboardingPage />)
      await completeGoals()
      expect(push).toHaveBeenCalledWith('/dashboard')
      expect(createCheckout).not.toHaveBeenCalled()
    }
  )

  it('preserves the clicked plan when authentication restoration fails', async () => {
    searchParams.set('plan', 'yearly')
    render(<OnboardingPage />)
    await completeGoals()
    useAuthStore.setState({ accessToken: null })
    restoreAccessToken.mockRejectedValueOnce(new Error('expired'))
    await act(async () =>
      fireEvent.click(
        screen.getByRole('button', { name: 'trialCtaMonthlyTrialUsed' })
      )
    )
    expect(push).toHaveBeenCalledWith('/login?plan=monthly')
    expect(createCheckout).not.toHaveBeenCalled()
  })

  it.each(['replace-session', 'unmount'])(
    'does not redirect after an obsolete checkout finishes (%s)',
    async (action) => {
      searchParams.set('plan', 'yearly')
      let finish!: (url: null) => void
      createCheckout.mockReturnValueOnce(
        new Promise((resolve) => {
          finish = resolve
        })
      )
      const { unmount } = render(<OnboardingPage />)
      await completeGoals()
      fireEvent.click(
        screen.getByRole('button', { name: 'trialCtaYearlyTrialUsed' })
      )
      expect(createCheckout).toHaveBeenCalledTimes(1)
      if (action === 'unmount') unmount()
      else act(() => useAuthStore.getState().startSession('replacement-token'))
      await act(async () => finish(null))
      expect(push).not.toHaveBeenCalled()
      if (action === 'unmount')
        expect(createCheckout.mock.calls[0][1].aborted).toBe(true)
    }
  )

  it.each(['replace-session', 'unmount'])(
    'does not publish an obsolete onboarding profile (%s)',
    async (action) => {
      searchParams.set('plan', 'monthly')
      let finish!: (body: unknown) => void
      apiFetch.mockResolvedValueOnce({
        ok: true,
        json: () =>
          new Promise((resolve) => {
            finish = resolve
          }),
      })
      const { unmount } = render(<OnboardingPage />)
      await completeGoals()
      await waitFor(() => expect(finish).toBeDefined())
      if (action === 'unmount') unmount()
      else act(() => useAuthStore.getState().startSession('replacement-token'))
      await act(async () => finish({ ...learner, learning_goals: [] }))
      expect(useAuthStore.getState().user?.learning_goals).not.toEqual([])
      expect(push).not.toHaveBeenCalled()
      expect(createCheckout).not.toHaveBeenCalled()
    }
  )
})
