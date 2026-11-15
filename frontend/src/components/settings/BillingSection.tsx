'use client'

import { Suspense } from 'react'
import { useSearchParams } from 'next/navigation'
import { useLocale, useTranslations } from 'next-intl'
import { Check } from 'lucide-react'
import { useBillingPortal } from '@/hooks/useBillingPortal'
import { useTrialStatus } from '@/hooks/useTrialStatus'
import { useAuthStore, isSubscribed, needsPaymentRecovery } from '@/store/auth'
import { useConfigStore } from '@/store/config'
import { SubscriptionPlanButtons } from '@/components/billing/SubscriptionPlanButtons'
import { getSelectedPlan } from '@/lib/checkout-navigation'

function SelectedPlanButtons() {
  const searchParams = useSearchParams()
  return (
    <SubscriptionPlanButtons
      preferredPlan={getSelectedPlan(searchParams.get('plan')) ?? 'monthly'}
      showPlanDetails
    />
  )
}

export function BillingSection() {
  const tBilling = useTranslations('billing')
  const tOffer = useTranslations('premiumOffer')
  const locale = useLocale()
  const user = useAuthStore((s) => s.user)
  const stripeEnabled = useConfigStore((s) => s.stripeEnabled)
  const {
    openPortal,
    loading: portalLoading,
    error: portalError,
  } = useBillingPortal()
  const paymentRecovery = needsPaymentRecovery(user)
  const canManageBilling = isSubscribed(user, stripeEnabled) || paymentRecovery
  const { freemiumTrialActive } = useTrialStatus()
  const noCardTrial = freemiumTrialActive && !canManageBilling

  if (!stripeEnabled) return null

  return (
    <div className="border-fl-border bg-fl-surface border p-6 font-sans">
      <div className="border-fl-border mb-4 flex items-center gap-2 border-b pb-4">
        <span className="text-fl-label text-fl-muted-2" aria-hidden="true">
          ●
        </span>
        <h2 className="text-fl-fg text-base font-semibold">
          {tBilling('section')}
        </h2>
      </div>
      <div className="space-y-4">
        {/* Status badge */}
        <div className="flex flex-wrap items-center justify-between gap-2">
          <span className="text-fl-muted-1 text-sm">{tBilling('status')}</span>
          <span
            className={`border px-2.5 py-1 text-sm font-semibold ${
              user?.subscription_status === 'active' &&
              !user?.cancel_at_period_end
                ? 'border-green-600/40 text-green-500'
                : user?.subscription_status === 'active' &&
                    user?.cancel_at_period_end
                  ? 'border-fl-accent/40 text-fl-accent'
                  : user?.subscription_status === 'trialing' || noCardTrial
                    ? 'border-fl-accent/40 text-fl-accent'
                    : paymentRecovery
                      ? 'border-yellow-500/40 text-yellow-500'
                      : 'border-fl-border text-fl-muted-3'
            }`}
          >
            {user?.subscription_status === 'active' &&
              !user?.cancel_at_period_end &&
              tBilling('statusActive')}
            {user?.subscription_status === 'active' &&
              user?.cancel_at_period_end &&
              tBilling('statusCanceling')}
            {user?.subscription_status === 'trialing' &&
              tBilling('statusTrialing')}
            {user?.subscription_status === 'past_due' &&
              tBilling('statusPastDue')}
            {user?.subscription_status === 'unpaid' && tBilling('statusUnpaid')}
            {user?.subscription_status === 'paused' && tBilling('statusPaused')}
            {noCardTrial && tOffer('noCardTrialStatus')}
            {!noCardTrial &&
              user?.subscription_status === 'incomplete' &&
              tBilling('statusIncomplete')}
            {!noCardTrial &&
              user?.subscription_status === 'incomplete_expired' &&
              tBilling('statusIncompleteExpired')}
            {!noCardTrial &&
              user?.subscription_status === 'canceled' &&
              tBilling('statusCanceled')}
            {!noCardTrial &&
              (!user?.subscription_status ||
                user?.subscription_status === 'none') &&
              tBilling('statusNone')}
          </span>
        </div>

        {noCardTrial && user?.freemium_trial_ends_at && (
          <p className="border-fl-accent/30 bg-fl-accent/5 text-fl-muted-1 border p-3 text-sm leading-relaxed">
            {tOffer('noCardTrialDescription', {
              date: new Date(user.freemium_trial_ends_at).toLocaleDateString(
                locale
              ),
            })}
          </p>
        )}

        {/* Next billing / end date */}
        {user?.subscription_ends_at &&
          (user.subscription_status === 'active' ||
            user.subscription_status === 'trialing' ||
            user.subscription_status === 'past_due' ||
            user.subscription_status === 'unpaid' ||
            user.subscription_status === 'paused' ||
            user.subscription_status === 'canceled' ||
            user.cancel_at_period_end) &&
          new Date(user.subscription_ends_at) > new Date() && (
            <div className="flex flex-wrap items-center justify-between gap-2">
              <span className="text-fl-muted-1 text-sm">
                {user.subscription_status === 'canceled' ||
                user.cancel_at_period_end
                  ? tBilling('accessUntil')
                  : tBilling('nextBilling')}
              </span>
              <span className="text-fl-muted-1 text-sm">
                {new Date(user.subscription_ends_at).toLocaleDateString(locale)}
              </span>
            </div>
          )}

        {paymentRecovery && (
          <div className="border border-yellow-500/30 bg-yellow-500/5 p-3">
            <p className="text-sm font-semibold text-yellow-500">
              {tBilling('pastDueTitle')}
            </p>
            <p className="text-fl-muted-1 mt-2 text-sm leading-relaxed">
              {tBilling('pastDueDesc')}
            </p>
          </div>
        )}

        {!canManageBilling && (
          <div className="border-fl-border space-y-3 border-t pt-4">
            <div>
              <h3 className="text-fl-fg text-lg font-semibold">
                {tOffer('benefitsTitle')}
              </h3>
              <p className="text-fl-muted-1 mt-1 text-sm leading-relaxed">
                {tOffer('benefitsDescription')}
              </p>
            </div>
            <ul className="grid gap-3 sm:grid-cols-2">
              {[
                'benefitsVoice',
                'benefitsChat',
                'benefitsComprehension',
                'benefitsLessonsGames',
                'benefitsLanguages',
              ].map((benefit) => (
                <li
                  key={benefit}
                  className="text-fl-muted-1 flex items-start gap-2 text-sm leading-relaxed"
                >
                  <Check
                    className="text-fl-accent mt-0.5 h-4 w-4 shrink-0"
                    aria-hidden="true"
                  />
                  <span>{tOffer(benefit)}</span>
                </li>
              ))}
            </ul>
            <p className="text-fl-muted-2 text-sm leading-relaxed">
              {tOffer('generalLimits')}
            </p>
          </div>
        )}

        {/* Manage or subscribe button */}
        {canManageBilling ? (
          <button
            onClick={openPortal}
            disabled={portalLoading}
            className="border-fl-border text-fl-muted-1 hover:text-fl-fg hover:border-fl-border-2 focus-visible:outline-fl-accent w-full border py-2.5 text-sm font-semibold transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 disabled:opacity-50"
          >
            {portalLoading
              ? '...'
              : tBilling(paymentRecovery ? 'updatePayment' : 'manage')}
          </button>
        ) : (
          <Suspense
            fallback={
              <SubscriptionPlanButtons
                preferredPlan="monthly"
                showPlanDetails
              />
            }
          >
            <SelectedPlanButtons />
          </Suspense>
        )}

        {portalError && (
          <p className="text-fl-error text-sm" role="alert">
            {portalError}
          </p>
        )}
      </div>
    </div>
  )
}
