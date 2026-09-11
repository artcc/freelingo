'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { useTranslations } from 'next-intl'
import { apiFetch } from '@/lib/api'
import { mapUser } from '@/lib/mappers'
import { useAuthStore } from '@/store/auth'

type ConfirmationStatus = 'checking' | 'confirmed' | 'pending' | 'error'

const CONFIRMATION_ATTEMPTS = 5
const CONFIRMATION_DELAY_MS = 1500

function isPremiumStatus(status: string | undefined): boolean {
  return status === 'active' || status === 'trialing'
}

function wait(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

export default function BillingSuccessPage() {
  const t = useTranslations('billing')
  const router = useRouter()
  const setUser = useAuthStore((s) => s.setUser)
  const [countdown, setCountdown] = useState(5)
  const [status, setStatus] = useState<ConfirmationStatus>('checking')

  // Confirm the subscription from /me before claiming Premium is active.
  useEffect(() => {
    let cancelled = false

    async function confirmSubscription() {
      try {
        if (!useAuthStore.getState().accessToken) {
          const refreshRes = await fetch('/api/auth/refresh', {
            method: 'POST',
            credentials: 'include',
          })
          if (!refreshRes.ok) {
            if (!cancelled) setStatus('error')
            return
          }
          const { access_token } = await refreshRes.json()
          useAuthStore.getState().setTokens(access_token)
        }

        for (let attempt = 0; attempt < CONFIRMATION_ATTEMPTS; attempt += 1) {
          const res = await apiFetch('/api/auth/me')
          if (!res.ok) throw new Error('me failed')
          const me = await res.json()
          const mappedUser = mapUser(me)
          if (!cancelled) setUser(mappedUser)

          if (isPremiumStatus(mappedUser.subscription_status)) {
            if (!cancelled) setStatus('confirmed')
            return
          }

          if (attempt < CONFIRMATION_ATTEMPTS - 1) {
            await wait(CONFIRMATION_DELAY_MS)
          }
        }

        if (!cancelled) setStatus('pending')
      } catch {
        if (!cancelled) setStatus('error')
      }
    }

    void confirmSubscription()

    return () => {
      cancelled = true
    }
  }, [setUser])

  // Auto-redirect countdown
  useEffect(() => {
    if (status !== 'confirmed') return
    if (countdown <= 0) {
      router.push('/dashboard')
      return
    }
    const id = setTimeout(() => setCountdown((n) => n - 1), 1000)
    return () => clearTimeout(id)
  }, [countdown, router, status])

  const content = {
    checking: {
      label: t('successCheckingLabel'),
      title: t('successCheckingTitle'),
      desc: t('successCheckingDesc'),
      icon: '◌',
    },
    confirmed: {
      label: t('successLabel'),
      title: t('successTitle'),
      desc: t('successDesc'),
      icon: '◎',
    },
    pending: {
      label: t('successPendingLabel'),
      title: t('successPendingTitle'),
      desc: t('successPendingDesc'),
      icon: '◌',
    },
    error: {
      label: t('successErrorLabel'),
      title: t('successErrorTitle'),
      desc: t('successErrorDesc'),
      icon: '△',
    },
  }[status]

  return (
    <div className="bg-fl-bg flex min-h-screen items-center justify-center px-4">
      <div className="border-fl-border bg-fl-surface w-full max-w-sm space-y-5 border p-8 text-center">
        <div className="text-fl-accent text-2xl">{content.icon}</div>
        <p className="text-fl-label text-fl-muted-2 font-mono tracking-widest uppercase">
          {content.label}
        </p>
        <h1 className="text-fl-fg font-mono text-base font-bold">
          {content.title}
        </h1>
        <p className="text-fl-muted-1 font-mono text-xs leading-relaxed">
          {content.desc}
        </p>
        {status === 'confirmed' && (
          <p className="text-fl-hint text-fl-muted-3 font-mono tracking-widest uppercase">
            {t('successRedirect', { seconds: countdown })}
          </p>
        )}
        <Link
          href="/dashboard"
          className="bg-fl-accent text-fl-accent-fg hover:bg-fl-accent/90 block py-3 font-mono text-xs font-bold tracking-widest uppercase transition-colors"
        >
          {t('successCta')}
        </Link>
      </div>
    </div>
  )
}
