'use client'

import { useState } from 'react'
import { useTranslations } from 'next-intl'
import { apiFetch } from '@/lib/api'
import { splitYearlyCta, type BillingInterval } from '@/lib/billing-copy'
import { useConfigStore } from '@/store/config'

interface SubscriptionPlanButtonsProps {
  className?: string
}

export function SubscriptionPlanButtons({
  className = '',
}: SubscriptionPlanButtonsProps) {
  const tBilling = useTranslations('billing')
  const priceMonthly = useConfigStore((s) => s.priceMonthly)
  const priceYearly = useConfigStore((s) => s.priceYearly)
  const [loading, setLoading] = useState<BillingInterval | null>(null)
  const [error, setError] = useState<string | null>(null)
  const yearlyCta = splitYearlyCta(
    tBilling('planYearly', { price: String(priceYearly) })
  )

  async function startCheckout(plan: BillingInterval) {
    if (loading) return
    setLoading(plan)
    setError(null)
    try {
      const res = await apiFetch('/api/billing/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ plan }),
      })
      if (!res.ok) {
        const data = await res.json().catch(() => ({}))
        throw new Error(data.detail ?? tBilling('checkoutError'))
      }
      const { url } = await res.json()
      window.location.assign(url)
    } catch (err) {
      setError(err instanceof Error ? err.message : tBilling('checkoutError'))
      setLoading(null)
    }
  }

  return (
    <div className={`space-y-3 ${className}`}>
      <div className="flex flex-col gap-3 sm:flex-row">
        <button
          type="button"
          onClick={() => startCheckout('yearly')}
          disabled={loading !== null}
          className="bg-fl-accent text-fl-accent-fg hover:bg-fl-accent/90 flex-1 px-4 py-2.5 font-mono text-sm font-bold tracking-widest uppercase transition-colors disabled:opacity-50"
        >
          {loading === 'yearly' ? (
            '...'
          ) : (
            <span className="flex flex-col items-center gap-0.5 leading-relaxed">
              <span>{yearlyCta.main}</span>
              {yearlyCta.savings && (
                <span className="text-fl-accent-fg text-xs">
                  {yearlyCta.savings}
                </span>
              )}
            </span>
          )}
        </button>
        <button
          type="button"
          onClick={() => startCheckout('monthly')}
          disabled={loading !== null}
          className="border-fl-border text-fl-muted-1 hover:text-fl-fg hover:border-fl-border-2 flex-1 border px-4 py-2.5 font-mono text-sm font-bold tracking-widest uppercase transition-colors disabled:opacity-50"
        >
          {loading === 'monthly'
            ? '...'
            : tBilling('planMonthly', { price: String(priceMonthly) })}
        </button>
      </div>
      {error && <p className="text-fl-error font-mono text-xs">{error}</p>}
    </div>
  )
}
