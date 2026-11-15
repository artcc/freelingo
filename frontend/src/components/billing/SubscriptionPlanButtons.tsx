'use client'

import { useEffect, useId, useRef, useState } from 'react'
import { useLocale, useTranslations } from 'next-intl'
import { createCheckout } from '@/lib/billing'
import {
  hasTwoMonthsFree,
  splitYearlyCta,
  type BillingInterval,
} from '@/lib/billing-copy'
import { useConfigStore } from '@/store/config'
import { useAuthStore } from '@/store/auth'

interface SubscriptionPlanButtonsProps {
  className?: string
  preferredPlan?: BillingInterval | null
  showPlanDetails?: boolean
}

export function SubscriptionPlanButtons({
  className = '',
  preferredPlan,
  showPlanDetails = false,
}: SubscriptionPlanButtonsProps) {
  const tBilling = useTranslations('billing')
  const tOffer = useTranslations('premiumOffer')
  const descriptionId = useId()
  const locale = useLocale()
  const priceMonthly = useConfigStore((s) => s.priceMonthly)
  const priceYearly = useConfigStore((s) => s.priceYearly)
  const trialDays = useConfigStore((s) => s.stripeTrialDays)
  const configLoaded = useConfigStore((s) => s.loaded)
  const user = useAuthStore((s) => s.user)
  const trialEligible =
    configLoaded &&
    Number.isInteger(trialDays) &&
    trialDays > 0 &&
    user?.trial_used === false
  const trialEligibilityKnown =
    configLoaded &&
    Number.isInteger(trialDays) &&
    trialDays >= 0 &&
    typeof user?.trial_used === 'boolean'
  const [loading, setLoading] = useState<BillingInterval | null>(null)
  const [error, setError] = useState<string | null>(null)
  const checkoutRequest = useRef<AbortController | null>(null)
  useEffect(() => () => checkoutRequest.current?.abort(), [])
  const yearlyCta = splitYearlyCta(
    tBilling('planYearly', {
      price: new Intl.NumberFormat(locale).format(priceYearly),
    }),
    hasTwoMonthsFree(priceMonthly, priceYearly)
  )
  const plans: BillingInterval[] =
    preferredPlan === 'monthly' ? ['monthly', 'yearly'] : ['yearly', 'monthly']

  async function startCheckout(plan: BillingInterval) {
    if (loading) return
    const controller = new AbortController()
    checkoutRequest.current = controller
    const { sessionVersion } = useAuthStore.getState()
    const obsolete = () =>
      controller.signal.aborted ||
      useAuthStore.getState().sessionVersion !== sessionVersion
    setLoading(plan)
    setError(null)
    try {
      const url = await createCheckout(plan, controller.signal)
      if (obsolete()) return
      if (url) window.location.assign(url)
    } catch {
      if (obsolete()) return
      setError(tBilling('checkoutError'))
    } finally {
      if (!obsolete()) setLoading(null)
    }
  }

  return (
    <div className={`space-y-3 ${className}`}>
      <div className="flex flex-col gap-3 sm:flex-row">
        {plans.map((plan, index) => (
          <div key={plan} className="flex flex-1 flex-col gap-2">
            <button
              type="button"
              onClick={() => startCheckout(plan)}
              disabled={loading !== null}
              aria-describedby={
                showPlanDetails
                  ? `${descriptionId}-${plan} ${descriptionId}-terms`
                  : undefined
              }
              className={`focus-visible:outline-fl-accent w-full flex-1 px-4 py-2.5 text-sm font-bold transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 disabled:opacity-50 ${
                showPlanDetails
                  ? 'font-sans'
                  : 'font-mono tracking-widest uppercase'
              } ${
                index === 0
                  ? 'bg-fl-accent text-fl-accent-fg hover:bg-fl-accent/90'
                  : 'border-fl-border text-fl-muted-1 hover:text-fl-fg hover:border-fl-border-2 border'
              }`}
            >
              {loading === plan ? (
                '...'
              ) : plan === 'yearly' ? (
                <span className="flex flex-col items-center gap-0.5 leading-relaxed">
                  <span>{yearlyCta.main}</span>
                  {yearlyCta.savings && (
                    <span className="text-xs">{yearlyCta.savings}</span>
                  )}
                </span>
              ) : (
                tBilling('planMonthly', {
                  price: new Intl.NumberFormat(locale).format(priceMonthly),
                })
              )}
            </button>
            {showPlanDetails && (
              <p
                id={`${descriptionId}-${plan}`}
                className="text-fl-muted-2 text-center font-sans text-sm leading-relaxed"
              >
                {tOffer(
                  plan === 'monthly' ? 'monthlyCommitment' : 'yearlyCommitment'
                )}
              </p>
            )}
          </div>
        ))}
      </div>
      <p
        id={`${descriptionId}-terms`}
        className={
          showPlanDetails
            ? 'text-fl-muted-2 font-sans text-sm leading-relaxed'
            : 'text-fl-muted-3 font-mono text-xs leading-relaxed'
        }
      >
        {showPlanDetails
          ? trialEligible
            ? tOffer('cardTrialTerms', { days: trialDays })
            : trialEligibilityKnown
              ? tOffer('paidTerms')
              : tBilling('paywallNoChargeTrialUsed')
          : tBilling(
              trialEligible ? 'paywallNoCharge' : 'paywallNoChargeTrialUsed'
            )}
      </p>
      {error && (
        <p className="text-fl-error font-sans text-sm" role="alert">
          {error}
        </p>
      )}
    </div>
  )
}
