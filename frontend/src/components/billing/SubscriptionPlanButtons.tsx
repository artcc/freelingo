'use client'

import { useEffect, useRef, useState } from 'react'
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
}

export function SubscriptionPlanButtons({
  className = '',
  preferredPlan,
}: SubscriptionPlanButtonsProps) {
  const tBilling = useTranslations('billing')
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
          <button
            key={plan}
            type="button"
            onClick={() => startCheckout(plan)}
            disabled={loading !== null}
            className={`flex-1 px-4 py-2.5 font-mono text-sm font-bold tracking-widest uppercase transition-colors disabled:opacity-50 ${
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
        ))}
      </div>
      <p className="text-fl-muted-3 font-mono text-xs leading-relaxed">
        {tBilling(
          trialEligible ? 'paywallNoCharge' : 'paywallNoChargeTrialUsed'
        )}
      </p>
      {error && <p className="text-fl-error font-mono text-xs">{error}</p>}
    </div>
  )
}
