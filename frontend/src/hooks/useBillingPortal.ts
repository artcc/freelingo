'use client'

import { useEffect, useRef, useState } from 'react'
import { useTranslations } from 'next-intl'
import { apiFetch } from '@/lib/api'
import { useAuthStore } from '@/store/auth'

export function useBillingPortal() {
  const t = useTranslations('billing')
  const sessionVersion = useAuthStore((s) => s.sessionVersion)
  const request = useRef<AbortController | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    setLoading(false)
    setError(null)
    return () => request.current?.abort()
  }, [sessionVersion])

  async function openPortal() {
    if (request.current && !request.current.signal.aborted) return
    const controller = new AbortController()
    request.current = controller
    const version = useAuthStore.getState().sessionVersion
    const obsolete = () =>
      controller.signal.aborted ||
      useAuthStore.getState().sessionVersion !== version
    setLoading(true)
    setError(null)
    try {
      const response = await apiFetch('/api/billing/portal', {
        method: 'POST',
        signal: controller.signal,
      })
      if (obsolete()) return
      if (!response.ok) throw new Error('Billing portal unavailable')
      const { url } = await response.json()
      if (obsolete()) return
      window.location.assign(url)
    } catch {
      if (!obsolete()) setError(t('portalError'))
    } finally {
      if (!obsolete()) setLoading(false)
      if (request.current === controller) request.current = null
    }
  }

  return { openPortal, loading, error }
}
