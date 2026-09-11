'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { Menu, X } from 'lucide-react'
import { hasActiveLandingSubscription } from '@/lib/landing-subscription'

interface LandingNavProps {
  hasSession: boolean
  stripeEnabled: boolean
  navFeatures: string
  navReviews: string
  navPricing: string
  navFAQ: string
  showReviews: boolean
  signIn: string
  dashboard: string
}

export function LandingNav({
  hasSession,
  stripeEnabled,
  navFeatures,
  navReviews,
  navPricing,
  navFAQ,
  showReviews,
  signIn,
  dashboard,
}: LandingNavProps) {
  const [open, setOpen] = useState(false)
  const [showPricing, setShowPricing] = useState(stripeEnabled && !hasSession)

  useEffect(() => {
    let canceled = false

    if (!stripeEnabled) {
      setShowPricing(false)
      return
    }

    if (!hasSession) {
      setShowPricing(true)
      return
    }

    setShowPricing(false)
    async function checkSubscription() {
      const subscribed = await hasActiveLandingSubscription()
      if (!canceled) setShowPricing(!subscribed)
    }
    checkSubscription()

    return () => {
      canceled = true
    }
  }, [hasSession, stripeEnabled])

  const links = (
    <>
      <a
        href="#features"
        onClick={() => setOpen(false)}
        className="text-fl-muted-2 hover:text-fl-fg font-mono text-xs tracking-widest uppercase transition-colors"
      >
        {navFeatures}
      </a>
      {showReviews && (
        <a
          href="#reviews"
          onClick={() => setOpen(false)}
          className="text-fl-muted-2 hover:text-fl-fg font-mono text-xs tracking-widest uppercase transition-colors"
        >
          {navReviews}
        </a>
      )}
      {showPricing && (
        <a
          href="#pricing"
          onClick={() => setOpen(false)}
          className="text-fl-muted-2 hover:text-fl-fg font-mono text-xs tracking-widest uppercase transition-colors"
        >
          {navPricing}
        </a>
      )}
      <a
        href="#faq"
        onClick={() => setOpen(false)}
        className="text-fl-muted-2 hover:text-fl-fg font-mono text-xs tracking-widest uppercase transition-colors"
      >
        {navFAQ}
      </a>
      <Link
        href={hasSession ? '/dashboard' : '/login'}
        onClick={() => setOpen(false)}
        className="text-fl-muted-2 hover:text-fl-fg font-mono text-xs tracking-widest uppercase transition-colors"
      >
        {hasSession ? dashboard : signIn}
      </Link>
    </>
  )

  return (
    <nav className="border-fl-border bg-fl-bg/80 sticky top-0 z-10 border-b backdrop-blur-sm">
      <div className="mx-auto flex h-14 max-w-5xl items-center justify-between px-6">
        <div className="flex items-center gap-3">
          <Image src="/logo.png" alt="FreeLingo" width={28} height={28} />
          <span className="text-fl-fg font-code text-sm font-bold tracking-widest uppercase">
            FreeLingo
          </span>
        </div>

        {/* Desktop links */}
        <div className="hidden items-center gap-6 md:flex">{links}</div>

        {/* Mobile hamburger */}
        <button
          onClick={() => setOpen(!open)}
          className="text-fl-muted-2 hover:text-fl-fg md:hidden"
          aria-label="Toggle menu"
        >
          {open ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
        </button>
      </div>

      {/* Mobile dropdown */}
      {open && (
        <div className="border-fl-border bg-fl-bg flex flex-col gap-4 border-b px-6 pb-5 md:hidden">
          {links}
        </div>
      )}
    </nav>
  )
}
