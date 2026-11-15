'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useTranslations } from 'next-intl'
import { ConfirmDialog } from '@/components/ui/confirm-dialog'
import { usePageLoadingActive } from '@/components/ui/page-loading-boundary'
import { WHATS_NEW_VERSION } from '@/components/whats-new/WhatsNew'
import { TOUR_STORAGE_KEY } from '@/lib/onboarding-tour'
import {
  acknowledgeTrialExpiry,
  hasSeenTrialExpiry,
} from '@/lib/premium-prompts'
import { useAuthStore, isSubscribed, needsPaymentRecovery } from '@/store/auth'
import { useConfigStore } from '@/store/config'

/** Dashboard entry only: never interrupt an exercise when a trial expires. */
export function TrialExpiredNotice() {
  const user = useAuthStore((s) => s.user)
  const sessionVersion = useAuthStore((s) => s.sessionVersion)
  const loaded = useConfigStore((s) => s.loaded)
  const stripeEnabled = useConfigStore((s) => s.stripeEnabled)
  const trialEnabled = useConfigStore((s) => s.freemiumTrialEnabled)
  const pageLoading = usePageLoadingActive()
  const end = Date.parse(user?.freemium_trial_ends_at ?? '')
  if (
    !loaded ||
    !stripeEnabled ||
    !trialEnabled ||
    pageLoading ||
    !user ||
    !Number.isFinite(end) ||
    isSubscribed(user, stripeEnabled) ||
    needsPaymentRecovery(user)
  ) {
    return null
  }
  return (
    <ExpiredNotice
      key={`${sessionVersion}:${user.id}:${end}`}
      userId={user.id}
      trialEnd={end}
    />
  )
}

function ExpiredNotice({
  userId,
  trialEnd,
}: {
  userId: number
  trialEnd: number
}) {
  const t = useTranslations('premiumOffer')
  const router = useRouter()
  const [open, setOpen] = useState(false)

  useEffect(() => {
    if (trialEnd > Date.now()) return
    // Leave tour/news visits to their existing dialogs. Retry on a later entry.
    try {
      if (
        !localStorage.getItem(TOUR_STORAGE_KEY) ||
        !localStorage.getItem(`fl_whats_new_seen_${WHATS_NEW_VERSION}`)
      ) {
        return
      }
    } catch {
      return
    }
    function showWhenVisible() {
      if (
        document.visibilityState === 'visible' &&
        !hasSeenTrialExpiry(userId, trialEnd)
      ) {
        acknowledgeTrialExpiry(userId, trialEnd)
        setOpen(true)
      }
    }
    showWhenVisible()
    document.addEventListener('visibilitychange', showWhenVisible)
    return () =>
      document.removeEventListener('visibilitychange', showWhenVisible)
  }, [userId, trialEnd])

  return (
    <ConfirmDialog
      open={open}
      title={t('expiredTitle')}
      message={t('expiredDescription')}
      confirmLabel={t('viewPlans')}
      cancelLabel={t('stayFree')}
      onCancel={() => setOpen(false)}
      onConfirm={() => {
        setOpen(false)
        router.push('/settings#plan')
      }}
    />
  )
}
