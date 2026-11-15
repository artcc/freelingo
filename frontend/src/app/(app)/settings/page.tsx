'use client'

import { useEffect, useRef, useState } from 'react'
import { useTranslations } from 'next-intl'
import { apiFetch } from '@/lib/api'
import { useAuthStore } from '@/store/auth'
import { useConfigStore } from '@/store/config'
import { useRouter } from 'next/navigation'
import {
  Bot,
  CreditCard,
  Globe2,
  MessageSquareText,
  Palette,
  User,
  Volume2,
} from 'lucide-react'
import { ConfirmDialog } from '@/components/ui/confirm-dialog'
import { useLogout } from '@/hooks/useLogout'
import { useBillingPortal } from '@/hooks/useBillingPortal'
import { ProfileSection } from '@/components/settings/ProfileSection'
import { ConversationSection } from '@/components/settings/ConversationSection'
import { VoiceSection } from '@/components/settings/VoiceSection'
import { UsageLimitsSection } from '@/components/settings/UsageLimitsSection'
import { AppearanceSection } from '@/components/settings/AppearanceSection'
import { BillingSection } from '@/components/settings/BillingSection'
import { ReviewSection } from '@/components/settings/ReviewSection'
import {
  SettingsActionCard,
  SettingsNav,
  SettingsPageHeader,
  SettingsPanel,
} from '@/components/settings/SettingsShell'

export default function SettingsPage() {
  const t = useTranslations('settings')
  const tCommon = useTranslations('common')
  const tPremium = useTranslations('premiumOffer')
  const stripeEnabled = useConfigStore((s) => s.stripeEnabled)
  const planTitle = stripeEnabled
    ? tPremium('planSection')
    : t('sectionUsageLimits')
  const user = useAuthStore((s) => s.user)
  const logout = useAuthStore((s) => s.logout)
  const router = useRouter()
  const handleLogout = useLogout()

  const [logoutConfirm, setLogoutConfirm] = useState(false)
  const [deleteConfirm, setDeleteConfirm] = useState(false)
  const [deleting, setDeleting] = useState(false)
  const [deleteError, setDeleteError] = useState('')
  const deleteRequest = useRef<AbortController | null>(null)
  const cancellationRequired =
    stripeEnabled &&
    !user?.cancel_at_period_end &&
    [
      'active',
      'trialing',
      'past_due',
      'unpaid',
      'paused',
      'incomplete',
    ].includes(user?.subscription_status ?? '')

  useEffect(() => {
    const unsubscribe = useAuthStore.subscribe((state, previous) => {
      if (
        state.sessionVersion !== previous.sessionVersion ||
        state.user?.id !== previous.user?.id
      ) {
        deleteRequest.current?.abort()
        deleteRequest.current = null
        setDeleting(false)
        setDeleteConfirm(false)
        setDeleteError('')
      }
    })
    return () => {
      unsubscribe()
      deleteRequest.current?.abort()
      deleteRequest.current = null
    }
  }, [])

  const navItems = [
    { href: '#account', label: t('sectionAccount'), icon: User },
    { href: '#preferences', label: t('sectionAppearance'), icon: Palette },
    { href: '#voice', label: t('sectionConversation'), icon: Volume2 },
    { href: '#plan', label: planTitle, icon: CreditCard },
    { href: '#community', label: t('sectionReview'), icon: MessageSquareText },
    { href: '#legal', label: t('sectionLegal'), icon: Globe2 },
  ]

  async function handleDeleteAccount() {
    if (deleteRequest.current) return
    const controller = new AbortController()
    deleteRequest.current = controller
    const { sessionVersion, user: owner } = useAuthStore.getState()
    const isCurrent = () =>
      !controller.signal.aborted &&
      useAuthStore.getState().sessionVersion === sessionVersion &&
      useAuthStore.getState().user?.id === owner?.id
    setDeleting(true)
    setDeleteError('')
    try {
      const res = await apiFetch('/api/auth/me', {
        method: 'DELETE',
        signal: controller.signal,
      })
      if (!isCurrent()) return
      if (!res.ok) {
        const data = await res.json().catch(() => null)
        if (!isCurrent()) return
        setDeleteError(
          res.status === 409 &&
            data?.detail === 'subscription_cancellation_required'
            ? 'cancellationRequired'
            : res.status === 409 && data?.detail === 'billing_checkout_pending'
              ? 'checkoutPending'
              : res.status === 503 &&
                  data?.detail === 'billing_verification_unavailable'
                ? 'verificationUnavailable'
                : 'failed'
        )
        return
      }
      logout()
      router.push('/login')
    } catch {
      if (isCurrent()) setDeleteError('failed')
    } finally {
      if (isCurrent()) setDeleting(false)
      if (deleteRequest.current === controller) deleteRequest.current = null
    }
  }

  return (
    <div className="mx-auto max-w-6xl space-y-4 p-6">
      <SettingsPageHeader
        eyebrow={`${t('sectionAccount')} / ${t('title')}`}
        title={t('title')}
      />

      <SettingsNav items={navItems} />

      <div className="grid gap-3 md:grid-cols-2">
        <SettingsActionCard
          href="/settings/languages"
          label={t('languagesManage')}
          description={t('sectionLanguages')}
          icon={Globe2}
        />
        <SettingsActionCard
          href="/settings/memories"
          label={t('memoryManage')}
          description={t('sectionMemory')}
          icon={Bot}
        />
      </div>

      <div className="space-y-4">
        <SettingsPanel id="account" title={t('sectionAccount')}>
          <ProfileSection title={t('cardProfileAccess')} />

          <div className="border-fl-border bg-fl-surface border p-6">
            <div className="border-fl-border mb-4 flex items-center gap-2 border-b pb-4">
              <span className="text-fl-label text-fl-muted-2">●</span>
              <span className="text-fl-label text-fl-muted-2 font-mono tracking-widest uppercase">
                {t('cardSessionSecurity')}
              </span>
            </div>
            <div className="space-y-2">
              <button
                onClick={() => setLogoutConfirm(true)}
                className="text-fl-label text-fl-muted-2 border-fl-border hover:text-fl-error hover:border-fl-error/40 w-full border py-3 font-mono tracking-widest uppercase transition-colors"
              >
                {tCommon('logout')}
              </button>

              {user?.role !== 'admin' && (
                <button
                  onClick={() => {
                    setDeleteError('')
                    setDeleteConfirm(true)
                  }}
                  disabled={deleting}
                  className="text-fl-label text-fl-error border-fl-error/40 hover:border-fl-error/70 w-full border py-3 font-mono tracking-widest uppercase transition-colors disabled:opacity-40"
                >
                  {t('deleteAccount')}
                </button>
              )}
            </div>
          </div>
        </SettingsPanel>

        <SettingsPanel id="preferences" title={t('sectionAppearance')}>
          <AppearanceSection title={t('cardTheme')} />
        </SettingsPanel>

        <SettingsPanel id="voice" title={t('sectionConversation')}>
          <div className="grid gap-4 xl:grid-cols-2">
            <ConversationSection title={t('cardConversationTiming')} />
            <VoiceSection title={t('cardTutorVoice')} />
          </div>
        </SettingsPanel>

        <SettingsPanel id="plan" title={planTitle}>
          <div className="space-y-4">
            <BillingSection />
            <UsageLimitsSection title={t('cardCurrentUsage')} />
          </div>
        </SettingsPanel>

        <SettingsPanel id="community" title={t('sectionReview')}>
          <ReviewSection title={t('cardProductReview')} />
        </SettingsPanel>

        <SettingsPanel id="legal" title={t('sectionLegal')}>
          <div className="border-fl-border bg-fl-surface border p-6">
            <div className="border-fl-border mb-4 flex items-center gap-2 border-b pb-4">
              <span className="text-fl-label text-fl-muted-2">●</span>
              <span className="text-fl-label text-fl-muted-2 font-mono tracking-widest uppercase">
                {t('cardLegalDocuments')}
              </span>
            </div>
            <div className="flex flex-col gap-2">
              <a
                href="/terms?from=settings"
                className="text-fl-muted-2 hover:text-fl-fg font-mono text-xs tracking-widest uppercase transition-colors"
              >
                {t('termsOfService')}
              </a>
              <a
                href="/privacy?from=settings"
                className="text-fl-muted-2 hover:text-fl-fg font-mono text-xs tracking-widest uppercase transition-colors"
              >
                {t('privacyPolicy')}
              </a>
            </div>
          </div>
        </SettingsPanel>
      </div>

      <ConfirmDialog
        open={logoutConfirm}
        title={tCommon('logoutConfirmTitle')}
        message={tCommon('logoutConfirmMessage')}
        confirmLabel={tCommon('logout')}
        onConfirm={handleLogout}
        onCancel={() => setLogoutConfirm(false)}
      />

      {deleteConfirm && (
        <DeleteAccountDialog
          deleting={deleting}
          error={deleteError}
          cancellationRequired={cancellationRequired}
          onConfirm={handleDeleteAccount}
          onCancel={() => setDeleteConfirm(false)}
        />
      )}
    </div>
  )
}

// The dialog owns portal work so closing it also cancels pending navigation.
function DeleteAccountDialog({
  deleting,
  error,
  cancellationRequired,
  onConfirm,
  onCancel,
}: {
  deleting: boolean
  error: string
  cancellationRequired: boolean
  onConfirm: () => void
  onCancel: () => void
}) {
  const t = useTranslations('settings')
  const tDeletion = useTranslations('accountDeletion')
  const {
    openPortal,
    loading: portalLoading,
    error: portalError,
  } = useBillingPortal()
  const showCancellation =
    error === 'cancellationRequired' || (!error && cancellationRequired)

  return (
    <ConfirmDialog
      open
      title={t('deleteAccountTitle')}
      message={t('deleteAccountMessage')}
      confirmLabel={t('deleteAccountConfirm')}
      confirming={deleting || portalLoading}
      error={
        showCancellation ? (
          <>
            {tDeletion('cancellationRequired')}{' '}
            <button
              type="button"
              onClick={openPortal}
              disabled={deleting || portalLoading}
              aria-busy={portalLoading}
              className="underline underline-offset-4 disabled:opacity-50"
            >
              {tDeletion('manageSubscription')}
            </button>
            {portalError && <span className="mt-2 block">{portalError}</span>}
          </>
        ) : error ? (
          tDeletion(error)
        ) : undefined
      }
      danger
      onConfirm={onConfirm}
      onCancel={onCancel}
    />
  )
}
