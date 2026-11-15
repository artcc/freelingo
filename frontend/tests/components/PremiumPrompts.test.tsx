import React from 'react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { act, cleanup, fireEvent, render, screen } from '@testing-library/react'
import { PremiumResultOffer } from '@/components/billing/PremiumResultOffer'
import { TrialExpiredNotice } from '@/components/billing/TrialExpiredNotice'
import WhatsNew, { WHATS_NEW_VERSION } from '@/components/whats-new/WhatsNew'
import { TOUR_STORAGE_KEY } from '@/lib/onboarding-tour'
import { claimPremiumResultOffer } from '@/lib/premium-prompts'
import { useAuthStore, type User } from '@/store/auth'
import { useConfigStore } from '@/store/config'
import { useFreemiumStore } from '@/store/freemium'
import {
  PageLoadingProvider,
  usePageLoadingPresentation,
} from '@/components/ui/page-loading-boundary'

const { push } = vi.hoisted(() => ({ push: vi.fn() }))
vi.mock('next/navigation', () => ({ useRouter: () => ({ push }) }))
vi.mock('next-intl', () => ({
  useLocale: () => 'en',
  useTranslations: () => (key: string) => key,
  useMessages: () => ({}),
}))
vi.mock('next/link', () => ({
  default: (props: React.AnchorHTMLAttributes<HTMLAnchorElement>) => <a {...props} />,
}))

const learner: User = {
  id: 1,
  username: 'learner',
  displayName: 'Learner',
  role: 'user',
  conversation_max_duration: 900,
  conversation_inactivity_timeout: 60,
  subscription_status: 'none',
  freemium_trial_ends_at: '2026-11-14T12:00:00Z',
}
const whatsNewKey = `fl_whats_new_seen_${WHATS_NEW_VERSION}`
const balance = {
  trial_active: false,
  trial_ends_at: null,
  chat_remaining: 5,
  chat_limit: 5,
  lessons_remaining: 3,
  lessons_limit: 3,
  listening_remaining: 3,
  listening_limit: 3,
  reading_remaining: 3,
  reading_limit: 3,
  games_remaining: 3,
  games_limit: 3,
  voice_remaining_seconds: 300,
  voice_limit_seconds: 300,
}

function DashboardLoad({ loading }: { loading: boolean }) {
  usePageLoadingPresentation(loading ? <span>Loading</span> : null)
  return loading ? null : <TrialExpiredNotice />
}

function DashboardInvitations() {
  return (
    <>
      <WhatsNew />
      <TrialExpiredNotice />
    </>
  )
}

beforeEach(() => {
  vi.useFakeTimers()
  vi.setSystemTime('2026-11-15T12:00:00Z')
  push.mockReset()
  localStorage.clear()
  localStorage.setItem(TOUR_STORAGE_KEY, '1')
  localStorage.setItem(whatsNewKey, '1')
  useAuthStore.getState().startSession('token')
  useAuthStore.getState().setUser(learner)
  useConfigStore.setState({
    loaded: true,
    stripeEnabled: true,
    freemiumTrialEnabled: true,
  })
  useFreemiumStore.setState({ status: balance, loaded: true, lastFetch: Date.now() })
  vi.stubGlobal('IntersectionObserver', undefined)
})

afterEach(() => {
  cleanup()
  vi.useRealTimers()
  vi.unstubAllGlobals()
})

describe('trial expiry invitation', () => {
  it('shows once per account and trial in this browser and explicitly opens plans', () => {
    const first = render(<TrialExpiredNotice />)
    expect(screen.getByRole('alertdialog')).toHaveTextContent('expiredTitle')
    fireEvent.click(screen.getByRole('button', { name: 'viewPlans' }))
    expect(push).toHaveBeenCalledWith('/settings#plan')
    first.unmount()
    useAuthStore.getState().startSession('new-session')
    useAuthStore.getState().setUser(learner)
    const second = render(<TrialExpiredNotice />)
    expect(screen.queryByRole('alertdialog')).not.toBeInTheDocument()
    second.unmount()
    useAuthStore.getState().setUser({ ...learner, id: 2 })
    render(<TrialExpiredNotice />)
    expect(screen.getByRole('alertdialog')).toBeInTheDocument()
  })

  it('supports Escape without navigation and respects the dismissal on return', () => {
    const first = render(<TrialExpiredNotice />)
    fireEvent.keyDown(window, { key: 'Escape' })
    expect(screen.queryByRole('alertdialog')).not.toBeInTheDocument()
    expect(push).not.toHaveBeenCalled()
    first.unmount()
    render(<TrialExpiredNotice />)
    expect(screen.queryByRole('alertdialog')).not.toBeInTheDocument()
  })

  it.each([TOUR_STORAGE_KEY, whatsNewKey])(
    'leaves a visit with pending %s to its existing dialog',
    (key) => {
      localStorage.removeItem(key)
      const first = render(<TrialExpiredNotice />)
      expect(screen.queryByRole('alertdialog')).not.toBeInTheDocument()
      localStorage.setItem(key, '1')
      first.unmount()
      render(<TrialExpiredNotice />)
      expect(screen.getByRole('alertdialog')).toBeInTheDocument()
    }
  )

  it('reserves the news visit when configuration arrives after news dismissal', () => {
    localStorage.removeItem(whatsNewKey)
    useConfigStore.setState({ loaded: false })
    const visit = render(<DashboardInvitations />)
    fireEvent.click(screen.getByRole('button', { name: 'cta →' }))
    expect(localStorage.getItem(whatsNewKey)).toBe('1')

    act(() => {
      useAuthStore.getState().setTokens('rotated-token')
      useAuthStore.getState().setUser({ ...learner, displayName: 'Updated' })
    })
    act(() => useConfigStore.setState({ loaded: true }))
    expect(screen.queryByRole('alertdialog')).not.toBeInTheDocument()
    expect(localStorage.getItem('fl_premium_prompts_1')).toBeNull()

    visit.unmount()
    render(<DashboardInvitations />)
    expect(screen.getByRole('alertdialog')).toHaveTextContent('expiredTitle')
  })

  it('reserves the tour visit even if it finishes before configuration loads', () => {
    localStorage.removeItem(TOUR_STORAGE_KEY)
    useConfigStore.setState({ loaded: false })
    const visit = render(<TrialExpiredNotice />)
    localStorage.setItem(TOUR_STORAGE_KEY, '1')

    act(() => useConfigStore.setState({ loaded: true }))
    expect(screen.queryByRole('alertdialog')).not.toBeInTheDocument()
    expect(localStorage.getItem('fl_premium_prompts_1')).toBeNull()

    visit.unmount()
    render(<TrialExpiredNotice />)
    expect(screen.getByRole('alertdialog')).toHaveTextContent('expiredTitle')
  })

  it.each(['session', 'account'] as const)(
    'does not carry a deferred visit into a replacement %s',
    (replacement) => {
      localStorage.removeItem(whatsNewKey)
      useConfigStore.setState({ loaded: false })
      render(<DashboardInvitations />)
      fireEvent.click(screen.getByRole('button', { name: 'cta →' }))
      act(() => {
        if (replacement === 'session') {
          useAuthStore.getState().startSession('replacement-token')
          useAuthStore.getState().setUser(learner)
        } else {
          useAuthStore.getState().setUser({ ...learner, id: 2 })
        }
      })
      expect(localStorage.getItem('fl_premium_prompts_1')).toBeNull()
      expect(localStorage.getItem('fl_premium_prompts_2')).toBeNull()

      act(() => useConfigStore.setState({ loaded: true }))
      expect(screen.getByRole('alertdialog')).toHaveTextContent('expiredTitle')
      const owner = replacement === 'session' ? 1 : 2
      expect(localStorage.getItem(`fl_premium_prompts_${owner}`)).not.toBeNull()
      if (replacement === 'account') {
        expect(localStorage.getItem('fl_premium_prompts_1')).toBeNull()
      }
    }
  )

  it('rechecks visit priority for a replacement account before delayed configuration', () => {
    useConfigStore.setState({ loaded: false })
    const visit = render(<TrialExpiredNotice />)
    localStorage.removeItem(TOUR_STORAGE_KEY)
    act(() => useAuthStore.getState().setUser({ ...learner, id: 2 }))
    localStorage.setItem(TOUR_STORAGE_KEY, '1')
    act(() => useConfigStore.setState({ loaded: true }))

    expect(screen.queryByRole('alertdialog')).not.toBeInTheDocument()
    expect(localStorage.getItem('fl_premium_prompts_1')).toBeNull()
    expect(localStorage.getItem('fl_premium_prompts_2')).toBeNull()
    visit.unmount()
    render(<TrialExpiredNotice />)
    expect(screen.getByRole('alertdialog')).toHaveTextContent('expiredTitle')
    expect(localStorage.getItem('fl_premium_prompts_1')).toBeNull()
    expect(localStorage.getItem('fl_premium_prompts_2')).not.toBeNull()
  })

  it.each(['active', 'trialing', 'past_due', 'unpaid', 'paused'] as const)(
    'does not turn %s into an expired free-trial offer',
    (subscription_status) => {
      useAuthStore.getState().setUser({ ...learner, subscription_status })
      render(<TrialExpiredNotice />)
      expect(screen.queryByRole('alertdialog')).not.toBeInTheDocument()
    }
  )

  it.each([null, 'invalid', '2026-11-20T12:00:00Z'])(
    'requires a known expired trial: %s',
    (freemium_trial_ends_at) => {
      useAuthStore.getState().setUser({ ...learner, freemium_trial_ends_at })
      render(<TrialExpiredNotice />)
      expect(screen.queryByRole('alertdialog')).not.toBeInTheDocument()
    }
  )

  it('removes the open dialog when access or configuration changes', () => {
    render(<TrialExpiredNotice />)
    expect(screen.getByRole('alertdialog')).toBeInTheDocument()
    act(() => useConfigStore.setState({ stripeEnabled: false }))
    expect(screen.queryByRole('alertdialog')).not.toBeInTheDocument()
  })

  it('does not treat disabling the trial flag as an expiry', () => {
    useConfigStore.setState({ freemiumTrialEnabled: false })
    render(<TrialExpiredNotice />)
    expect(screen.queryByRole('alertdialog')).not.toBeInTheDocument()
  })

  it('does not consume the reminder before configuration is ready', () => {
    useConfigStore.setState({ loaded: false })
    render(<TrialExpiredNotice />)
    expect(screen.queryByRole('alertdialog')).not.toBeInTheDocument()
    act(() => useConfigStore.setState({ loaded: true }))
    expect(screen.getByRole('alertdialog')).toBeInTheDocument()
  })

  it('waits for a visible tab before consuming the reminder', () => {
    const visibility = vi.spyOn(document, 'visibilityState', 'get')
    visibility.mockReturnValue('hidden')
    render(<TrialExpiredNotice />)
    expect(screen.queryByRole('alertdialog')).not.toBeInTheDocument()
    expect(localStorage.getItem('fl_premium_prompts_1')).toBeNull()
    visibility.mockReturnValue('visible')
    fireEvent(document, new Event('visibilitychange'))
    expect(screen.getByRole('alertdialog')).toBeInTheDocument()
  })

  it('waits for the dashboard loading boundary before opening the reminder', async () => {
    const view = render(
      <PageLoadingProvider><DashboardLoad loading /></PageLoadingProvider>
    )
    view.rerender(
      <PageLoadingProvider><DashboardLoad loading={false} /></PageLoadingProvider>
    )
    expect(localStorage.getItem('fl_premium_prompts_1')).toBeNull()
    expect(screen.queryByRole('alertdialog')).not.toBeInTheDocument()
    await act(() => vi.advanceTimersByTimeAsync(1))
    expect(screen.getByRole('alertdialog')).toBeInTheDocument()
  })

  it('remembers an expiry in memory when only the storage write fails', () => {
    useAuthStore.getState().setUser({ ...learner, id: 98 })
    localStorage.setItem('fl_premium_prompts_98', JSON.stringify({
      lastOfferedAt: 1, expiredTrialSeen: 1,
    }))
    vi.stubGlobal('localStorage', {
      ...localStorage,
      setItem: vi.fn(() => { throw new Error('full') }),
    })
    const first = render(<TrialExpiredNotice />)
    expect(screen.getByRole('alertdialog')).toBeInTheDocument()
    first.unmount()
    render(<TrialExpiredNotice />)
    expect(screen.queryByRole('alertdialog')).not.toBeInTheDocument()
    expect(claimPremiumResultOffer(98)).toBe(false)
  })
})

describe('post-success Premium invitations', () => {
  it('shares a three-day cooldown across activities but isolates accounts', () => {
    const first = render(<PremiumResultOffer feature="lessons" />)
    expect(screen.getByRole('link', { name: 'viewPremium' })).toHaveAttribute(
      'href', '/settings#plan'
    )
    fireEvent.click(screen.getByRole('button', { name: 'close' }))
    first.unmount()
    const second = render(<PremiumResultOffer feature="reading" />)
    expect(screen.queryByRole('complementary')).not.toBeInTheDocument()
    expect(screen.queryByRole('link')).not.toBeInTheDocument()
    second.unmount()
    vi.setSystemTime(Date.now() + 3 * 86_400_000)
    const third = render(<PremiumResultOffer feature="reading" />)
    expect(screen.getByRole('link', { name: 'viewPremium' })).toBeInTheDocument()
    third.unmount()
    useAuthStore.getState().setUser({ ...learner, id: 2 })
    render(<PremiumResultOffer feature="flashcards" />)
    expect(screen.getByText('result.flashcards')).toBeInTheDocument()
  })

  it('claims only a visible result, not a blocked review or an offscreen placeholder', () => {
    let callback: IntersectionObserverCallback = () => {}
    const disconnect = vi.fn()
    vi.stubGlobal('IntersectionObserver', class {
      constructor(cb: IntersectionObserverCallback) { callback = cb }
      observe = vi.fn()
      disconnect = disconnect
    })
    const view = render(<PremiumResultOffer feature="reading" blocked />)
    expect(localStorage.getItem('fl_premium_prompts_1')).toBeNull()
    view.rerender(<PremiumResultOffer feature="reading" />)
    expect(localStorage.getItem('fl_premium_prompts_1')).toBeNull()
    act(() => callback(
      [{ isIntersecting: true } as IntersectionObserverEntry],
      {} as IntersectionObserver
    ))
    expect(screen.getByText('result.reading')).toBeInTheDocument()
    expect(localStorage.getItem('fl_premium_prompts_1')).not.toBeNull()
    expect(disconnect).toHaveBeenCalled()
  })

  it('offers exhausted-quota continuity despite cooldown and explains renewal', () => {
    claimPremiumResultOffer(learner.id)
    useFreemiumStore.setState({
      status: { ...balance, listening_remaining: 0 },
    })
    render(<PremiumResultOffer feature="listening" />)
    expect(screen.getByText('exhaustedTitle')).toBeInTheDocument()
    expect(screen.getByText('weeklyReset')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'continuePremium' })).toBeInTheDocument()
  })

  it('does not promise renewal for a Premium-only feature', () => {
    useFreemiumStore.setState({
      status: { ...balance, lessons_remaining: 0, lessons_limit: 0 },
    })
    render(<PremiumResultOffer feature="lessons" />)
    expect(screen.getByText('exhaustedTitle')).toBeInTheDocument()
    expect(screen.queryByText('dailyReset')).not.toBeInTheDocument()
  })

  it('uses payment recovery when a completed activity has exhausted access', () => {
    useAuthStore.getState().setUser({ ...learner, subscription_status: 'past_due' })
    render(<PremiumResultOffer feature="reading" accessExhausted />)
    expect(screen.getByText('pastDueTitle')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'updatePayment' })).toBeInTheDocument()
    expect(screen.queryByText('planMonthly')).not.toBeInTheDocument()
  })

  it('does not infer exhaustion from an unknown quota', () => {
    useFreemiumStore.setState({ status: null })
    render(<PremiumResultOffer feature="voice" />)
    expect(screen.queryByText('exhaustedTitle')).not.toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'viewPremium' })).toBeInTheDocument()
  })

  it('explains the still-active trial instead of claiming a quota restriction', () => {
    useAuthStore.getState().setUser({
      ...learner, freemium_trial_ends_at: '2026-11-20T12:00:00Z',
    })
    useFreemiumStore.setState({ status: { ...balance, reading_remaining: 0 } })
    render(<PremiumResultOffer feature="reading" />)
    expect(screen.getByText('trialResultNote')).toBeInTheDocument()
    expect(screen.queryByText('exhaustedTitle')).not.toBeInTheDocument()
  })

  it.each(['active', 'trialing', 'past_due', 'unpaid', 'paused'] as const)(
    'does not invite %s accounts to purchase',
    (subscription_status) => {
      useAuthStore.getState().setUser({ ...learner, subscription_status })
      render(<PremiumResultOffer feature="lessons" />)
      expect(screen.queryByRole('link')).not.toBeInTheDocument()
      expect(localStorage.getItem('fl_premium_prompts_1')).toBeNull()
    }
  )

  it('survives blocked storage with a session-local cooldown', () => {
    useAuthStore.getState().setUser({ ...learner, id: 99 })
    vi.stubGlobal('localStorage', {
      ...localStorage,
      getItem: vi.fn(() => { throw new Error('blocked') }),
      setItem: vi.fn(() => { throw new Error('blocked') }),
    })
    const first = render(<PremiumResultOffer feature="lessons" />)
    expect(screen.getByRole('link', { name: 'viewPremium' })).toBeInTheDocument()
    first.unmount()
    render(<PremiumResultOffer feature="voice" />)
    expect(screen.queryByRole('link')).not.toBeInTheDocument()
  })
})
