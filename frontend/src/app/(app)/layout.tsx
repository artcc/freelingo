'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { usePathname, useRouter } from 'next/navigation'
import { useLocale, useTranslations } from 'next-intl'
import { ChevronDown } from 'lucide-react'
import { useAuthStore, isSubscribed } from '@/store/auth'
import { useConfigStore } from '@/store/config'
import { apiFetch, requestAccessToken } from '@/lib/api'
import { mapUser } from '@/lib/mappers'
import { useLogout } from '@/hooks/useLogout'
import { useTrialStatus } from '@/hooks/useTrialStatus'
import { useFreemiumStatusRefresh } from '@/hooks/useFreemiumStatusRefresh'
import { ConfirmDialog } from '@/components/ui/confirm-dialog'
import { ContactFormModal } from '@/components/ui/contact-form-modal'
import { LoadingBar } from '@/components/ui/loading-bar'
import { PageLoading } from '@/components/ui/page-loading'
import {
  PageLoadingProvider,
  PageLoadingViewport,
} from '@/components/ui/page-loading-boundary'
import LanguageSwitcher from '@/components/LanguageSwitcher'
import { AuthAvatarImage } from '@/components/AuthAvatarImage'

export default function AppLayout({ children }: { children: React.ReactNode }) {
  return (
    <PageLoadingProvider>
      <AppLayoutContent>{children}</AppLayoutContent>
    </PageLoadingProvider>
  )
}

function AppLayoutContent({ children }: { children: React.ReactNode }) {
  const tNav = useTranslations('nav')
  const tCommon = useTranslations('common')
  const tBilling = useTranslations('billing')
  const tPremium = useTranslations('premiumOffer')
  const pathname = usePathname()
  const locale = useLocale()
  const collator = new Intl.Collator(locale)

  const navGroups = [
    {
      key: 'learning',
      label: tNav('learning'),
      items: [
        { href: '/plan', label: tNav('myPlan') },
        { href: '/progress', label: tNav('progress') },
        { href: '/assessment', label: tNav('assessment') },
      ],
    },
    {
      key: 'practice',
      label: tNav('practice'),
      items: [
        { href: '/chat', label: tNav('tutor') },
        { href: '/conversation', label: tNav('conversation') },
        { href: '/listening', label: tNav('listening') },
        { href: '/reading', label: tNav('reading') },
        { href: '/flashcards', label: tNav('flashcards') },
        { href: '/games', label: tNav('games') },
        { href: '/grammar-practice', label: tNav('practiceGrammar') },
      ].sort((a, b) => collator.compare(a.label, b.label)),
    },
    {
      key: 'resources',
      label: tNav('resources'),
      items: [
        { href: '/grammar', label: tNav('grammar') },
        { href: '/vocabulary', label: tNav('vocabulary') },
        { href: '/phrasebook', label: tNav('phrasebook') },
      ].sort((a, b) => collator.compare(a.label, b.label)),
    },
    {
      key: 'help',
      label: tNav('help'),
      items: [
        { href: '/faq', label: tNav('faq') },
        { href: '/feedback', label: tNav('feedback') },
        { href: null, label: tNav('contact') },
      ].sort((a, b) => collator.compare(a.label, b.label)),
    },
  ]

  const router = useRouter()
  const user = useAuthStore((s) => s.user)
  const accessToken = useAuthStore((s) => s.accessToken)
  const setTokens = useAuthStore((s) => s.setTokens)
  const setUser = useAuthStore((s) => s.setUser)
  const logout = useAuthStore((s) => s.logout)
  const handleLogout = useLogout()
  const [initializing, setInitializing] = useState(true)
  const loadConfig = useConfigStore((s) => s.load)
  const [logoutConfirm, setLogoutConfirm] = useState(false)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [collapsedGroups, setCollapsedGroups] = useState<
    Record<string, boolean>
  >({})
  const [contactOpen, setContactOpen] = useState(false)
  const [resendSent, setResendSent] = useState(false)
  const [feedbackUnreadCount, setFeedbackUnreadCount] = useState(0)

  const PREMIUM_HREFS = new Set([
    '/chat',
    '/listening',
    '/reading',
    '/conversation',
    '/grammar-practice',
  ])
  const stripeEnabled = useConfigStore((s) => s.stripeEnabled)
  const configLoaded = useConfigStore((s) => s.loaded)
  const showPremiumBadge = stripeEnabled && !isSubscribed(user, stripeEnabled)
  const showPremiumAction = configLoaded && !!user && showPremiumBadge
  const { trialDaysLeft } = useTrialStatus()
  useFreemiumStatusRefresh(!initializing)

  async function handleResendVerification() {
    const res = await apiFetch('/api/auth/resend-verification', {
      method: 'POST',
    })
    if (res.ok) setResendSent(true)
  }

  // On every page load, Zustand is empty. Use the httpOnly refresh cookie
  // to silently get a new access token, then fetch /me to populate the user.
  useEffect(() => {
    let canceled = false
    const controller = new AbortController()
    const { sessionVersion } = useAuthStore.getState()
    const obsolete = () =>
      canceled || useAuthStore.getState().sessionVersion !== sessionVersion
    async function init() {
      // Load Stripe config once (non-blocking)
      loadConfig()
      try {
        if (!accessToken) {
          const access_token = await requestAccessToken()
          if (obsolete()) return
          setTokens(access_token)
        }
        // Fetch user info if not already loaded
        const meRes = await apiFetch('/api/auth/me', {
          signal: controller.signal,
        })
        if (obsolete()) return
        if (!meRes.ok) {
          logout()
          router.push('/login')
          return
        }
        const me = await meRes.json()
        if (obsolete()) return
        setUser(mapUser(me))

        if (me.learning_goals === null) {
          router.replace('/onboarding')
          return
        }
      } catch {
        if (obsolete()) return
        logout()
        router.push('/login')
      } finally {
        if (!canceled) setInitializing(false)
      }
    }
    init()
    return () => {
      canceled = true
      controller.abort()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  useEffect(() => {
    if (initializing) return

    async function loadFeedbackUnreadCount() {
      try {
        const res = await apiFetch('/api/feedback/unread-summary')
        if (!res.ok) return
        const data = await res.json()
        setFeedbackUnreadCount(data.unread_count ?? 0)
      } catch {
        setFeedbackUnreadCount(0)
      }
    }

    loadFeedbackUnreadCount()
    window.addEventListener('freelingo:feedback-read', loadFeedbackUnreadCount)
    return () => {
      window.removeEventListener(
        'freelingo:feedback-read',
        loadFeedbackUnreadCount
      )
    }
  }, [initializing])

  useEffect(() => {
    const desktop = window.matchMedia('(min-width: 48rem)')
    function closeMenuOnDesktop(event: MediaQueryListEvent) {
      if (event.matches) setMobileMenuOpen(false)
    }
    desktop.addEventListener('change', closeMenuOnDesktop)
    return () => desktop.removeEventListener('change', closeMenuOnDesktop)
  }, [])

  if (initializing) {
    return (
      <PageLoadingViewport className="h-dvh">
        <PageLoading label={tCommon('initializing')} className="bg-fl-bg" />
      </PageLoadingViewport>
    )
  }

  const feedbackBadgeText =
    feedbackUnreadCount > 99
      ? '99+'
      : feedbackUnreadCount > 0
        ? String(feedbackUnreadCount)
        : ''

  function isActiveNavHref(href: string) {
    return pathname === href || pathname.startsWith(href + '/')
  }

  function renderNavLink(
    item: { href: string; label: string },
    mobile: boolean
  ) {
    const active = isActiveNavHref(item.href)
    return (
      <Link
        key={item.href}
        href={item.href}
        onClick={mobile ? () => setMobileMenuOpen(false) : undefined}
        aria-current={active ? 'page' : undefined}
        className={`flex min-h-11 items-center gap-3 border-l-2 px-5 py-2.5 font-sans text-sm wrap-anywhere transition-colors ${
          active
            ? 'text-fl-fg bg-fl-surface-2 border-fl-accent font-medium'
            : 'text-fl-muted-2 hover:text-fl-fg hover:bg-fl-surface border-transparent'
        }`}
      >
        <span>{item.label}</span>
        {showPremiumBadge && PREMIUM_HREFS.has(item.href) && (
          <span className="text-fl-accent ml-auto shrink-0 text-xs">★</span>
        )}
        {item.href === '/feedback' && feedbackBadgeText && (
          <span className="text-fl-label ml-auto flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-red-600 leading-none font-bold text-white">
            {feedbackBadgeText}
          </span>
        )}
      </Link>
    )
  }

  function renderNavigation(mobile: boolean) {
    const utilityItems = [{ href: '/settings', label: tNav('settings') }]
    if (user?.role === 'admin') {
      utilityItems.push({ href: '/admin', label: tNav('admin') })
    }
    utilityItems.sort((a, b) => collator.compare(a.label, b.label))

    return (
      <>
        {renderNavLink({ href: '/dashboard', label: tNav('home') }, mobile)}
        {navGroups.map((group) => {
          const expanded = !collapsedGroups[group.key]
          const collapsedActive =
            !expanded &&
            group.items.some(
              (item) => item.href !== null && isActiveNavHref(item.href)
            )
          const panelId = `${mobile ? 'mobile' : 'desktop'}-nav-${group.key}`
          return (
            <div key={group.key} className="mt-4">
              <h2>
                <button
                  type="button"
                  aria-expanded={expanded}
                  aria-controls={panelId}
                  onClick={() =>
                    setCollapsedGroups((previous) => ({
                      ...previous,
                      [group.key]: !previous[group.key],
                    }))
                  }
                  className={`text-fl-muted-1 hover:text-fl-fg hover:bg-fl-surface flex min-h-11 w-full items-center gap-3 border-l-2 px-5 py-2 text-left font-sans text-xs font-semibold tracking-wider uppercase transition-colors ${
                    collapsedActive ? 'border-fl-accent' : 'border-transparent'
                  }`}
                >
                  <span className="flex-1">{group.label}</span>
                  {group.key === 'help' && !expanded && feedbackBadgeText && (
                    <span className="text-fl-label flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-red-600 leading-none font-bold tracking-normal text-white">
                      {feedbackBadgeText}
                    </span>
                  )}
                  <ChevronDown
                    aria-hidden="true"
                    className={`size-3.5 shrink-0 ${expanded ? '' : '-rotate-90'}`}
                  />
                </button>
              </h2>
              <div id={panelId} hidden={!expanded}>
                {group.items.map((item) =>
                  item.href === null ? (
                    <button
                      key="contact"
                      type="button"
                      onClick={() => {
                        if (mobile) setMobileMenuOpen(false)
                        setContactOpen(true)
                      }}
                      className="text-fl-muted-2 hover:text-fl-fg hover:bg-fl-surface min-h-11 w-full border-l-2 border-transparent px-5 py-2.5 text-left font-sans text-sm wrap-anywhere transition-colors"
                    >
                      {item.label}
                    </button>
                  ) : (
                    renderNavLink(
                      { href: item.href, label: item.label },
                      mobile
                    )
                  )
                )}
              </div>
            </div>
          )
        })}
        <div className="border-fl-border mt-4 border-t pt-2">
          {utilityItems.map((item) => renderNavLink(item, mobile))}
        </div>
      </>
    )
  }

  return (
    <div className="bg-fl-bg flex h-dvh overflow-hidden">
      {/* Sidebar */}
      <aside className="border-fl-border bg-fl-bg hidden w-60 shrink-0 flex-col border-r px-0 py-0 md:flex">
        {/* Logo area */}
        <div className="border-fl-border flex shrink-0 items-center gap-2 border-b px-5 py-5">
          <span className="text-fl-label text-fl-muted-2">●</span>
          <span className="text-fl-fg font-code text-sm font-bold tracking-widest uppercase">
            FreeLingo
          </span>
        </div>

        {/* Language switcher */}
        <div className="border-fl-border shrink-0 border-b">
          <LanguageSwitcher />
        </div>

        {showPremiumAction && (
          <Link
            href="/settings#plan"
            className="bg-fl-accent text-fl-accent-fg hover:bg-fl-accent/90 focus-visible:outline-fl-accent mx-4 mt-4 shrink-0 px-3 py-2 text-center font-sans text-sm font-semibold focus-visible:outline-2 focus-visible:outline-offset-2"
          >
            {tPremium('viewPremium')}
          </Link>
        )}

        {/* Nav */}
        <nav className="min-h-0 flex-1 overflow-y-auto py-3">
          {renderNavigation(false)}
        </nav>

        {/* User + logout */}
        <div className="border-fl-border shrink-0 border-t px-5 py-3">
          <div className="mb-3 flex items-center gap-3">
            <div className="border-fl-border h-8 w-8 flex-shrink-0 overflow-hidden rounded-full border">
              {user?.avatar ? (
                <AuthAvatarImage
                  avatar={user.avatar}
                  alt=""
                  width={32}
                  height={32}
                  className="h-full w-full object-cover"
                  fallback={
                    <div className="bg-fl-surface-2 flex h-full w-full items-center justify-center">
                      <span className="text-fl-muted-1 font-mono text-xs select-none">
                        {(user?.displayName ||
                          user?.username ||
                          '?')[0].toUpperCase()}
                      </span>
                    </div>
                  }
                />
              ) : (
                <div className="bg-fl-surface-2 flex h-full w-full items-center justify-center">
                  <span className="text-fl-muted-1 font-mono text-xs select-none">
                    {(user?.displayName ||
                      user?.username ||
                      '?')[0].toUpperCase()}
                  </span>
                </div>
              )}
            </div>
            <div className="min-w-0">
              <p className="text-fl-caption text-fl-muted-2 truncate font-sans">
                {user?.displayName || user?.username}
              </p>
              <p className="text-fl-label text-fl-muted-4 truncate font-sans">
                @{user?.username?.toLowerCase()}
              </p>
              {trialDaysLeft > 0 && (
                <Link
                  href="/settings#plan"
                  className="text-fl-label text-fl-accent focus-visible:outline-fl-accent block truncate font-mono text-xs underline-offset-4 hover:underline focus-visible:outline-2"
                >
                  ★ {tBilling('trialDays', { days: trialDaysLeft })}
                </Link>
              )}
            </div>
          </div>
          <p className="text-fl-label text-fl-muted-4 font-code mb-2 tracking-wider">
            v1.14.5
          </p>
          <button
            onClick={() => setLogoutConfirm(true)}
            className="text-fl-muted-2 hover:text-fl-fg w-full text-left font-sans text-sm transition-colors"
          >
            {tCommon('logout')}
          </button>
        </div>
      </aside>

      {mobileMenuOpen && (
        <div
          aria-hidden="true"
          className="bg-fl-bg/40 fixed inset-0 z-40 touch-none backdrop-blur-[3px] md:hidden"
        />
      )}

      {/* Mobile top bar */}
      <div className="border-fl-border bg-fl-bg fixed top-0 right-0 left-0 z-50 border-b md:hidden">
        <div className="flex items-center justify-between gap-3 px-4 py-3">
          <span className="text-fl-fg font-code text-xs font-bold tracking-widest uppercase">
            FreeLingo
          </span>
          {showPremiumAction && (
            <Link
              href="/settings#plan"
              onClick={() => setMobileMenuOpen(false)}
              aria-label={tPremium('viewPremium')}
              className="bg-fl-accent text-fl-accent-fg hover:bg-fl-accent/90 focus-visible:outline-fl-accent ml-auto px-3 py-1 font-sans text-sm font-semibold focus-visible:outline-2 focus-visible:outline-offset-2"
            >
              {tPremium('navLabel')}
            </Link>
          )}
          <button
            onClick={() => setMobileMenuOpen((o) => !o)}
            className="text-fl-muted-2 hover:text-fl-fg p-1 font-mono transition-colors"
            aria-label={
              mobileMenuOpen ? tCommon('closeMenu') : tCommon('openMenu')
            }
            aria-expanded={mobileMenuOpen}
            aria-controls="mobile-navigation"
          >
            <span className="text-base leading-none">
              {mobileMenuOpen ? '✕' : '☰'}
            </span>
          </button>
        </div>

        {/* Dropdown */}
        {mobileMenuOpen && (
          <nav
            id="mobile-navigation"
            className="border-fl-border bg-fl-bg max-h-[calc(100svh-3.5rem)] overflow-y-auto overscroll-contain border-t pb-2"
          >
            <div className="border-fl-border border-b">
              <LanguageSwitcher />
            </div>
            <div className="py-3">{renderNavigation(true)}</div>
            <div className="border-fl-border mx-5 mt-2 border-t pt-3">
              <div className="mb-2 flex items-center gap-3">
                <div className="border-fl-border h-7 w-7 flex-shrink-0 overflow-hidden rounded-full border">
                  {user?.avatar ? (
                    <AuthAvatarImage
                      avatar={user.avatar}
                      alt=""
                      width={28}
                      height={28}
                      className="h-full w-full object-cover"
                      fallback={
                        <div className="bg-fl-surface-2 flex h-full w-full items-center justify-center">
                          <span className="text-fl-hint text-fl-muted-1 font-mono select-none">
                            {(user?.displayName ||
                              user?.username ||
                              '?')[0].toUpperCase()}
                          </span>
                        </div>
                      }
                    />
                  ) : (
                    <div className="bg-fl-surface-2 flex h-full w-full items-center justify-center">
                      <span className="text-fl-hint text-fl-muted-1 font-mono select-none">
                        {(user?.displayName ||
                          user?.username ||
                          '?')[0].toUpperCase()}
                      </span>
                    </div>
                  )}
                </div>
                <div className="min-w-0">
                  <p className="text-fl-caption text-fl-muted-2 truncate font-sans">
                    {user?.displayName || user?.username}
                  </p>
                  <p className="text-fl-label text-fl-muted-4 truncate font-sans">
                    @{user?.username?.toLowerCase()}
                  </p>
                </div>
              </div>
              {trialDaysLeft > 0 && (
                <Link
                  href="/settings#plan"
                  onClick={() => setMobileMenuOpen(false)}
                  className="text-fl-label text-fl-accent focus-visible:outline-fl-accent mb-2 block font-mono text-xs underline-offset-4 hover:underline focus-visible:outline-2"
                >
                  ★ {tBilling('trialDays', { days: trialDaysLeft })}
                </Link>
              )}
              <p className="text-fl-label text-fl-muted-4 font-code mb-2 tracking-wider">
                v1.14.5
              </p>
              <button
                onClick={() => {
                  setMobileMenuOpen(false)
                  setLogoutConfirm(true)
                }}
                className="text-fl-muted-2 hover:text-fl-fg font-sans text-sm transition-colors"
              >
                {tCommon('logout')}
              </button>
            </div>
          </nav>
        )}
      </div>

      {/* Main */}
      <main
        inert={mobileMenuOpen}
        className={`flex min-h-0 min-w-0 flex-1 flex-col overflow-hidden pt-14 md:pt-0 ${mobileMenuOpen ? 'isolate' : ''}`}
      >
        {/* Email verification banner */}
        {user && user.is_verified === false && (
          <div className="border-fl-border bg-fl-surface flex shrink-0 flex-wrap items-center gap-x-4 gap-y-1 border-b px-4 py-2">
            <span className="text-fl-muted-1 font-mono text-xs tracking-wide">
              ● {tCommon('verifyEmailBanner')}
            </span>
            {resendSent ? (
              <span className="text-fl-muted-2 font-mono text-xs">
                {tCommon('verifyEmailSent')}
              </span>
            ) : (
              <button
                onClick={handleResendVerification}
                className="text-fl-accent font-mono text-xs underline transition-all hover:no-underline"
              >
                {tCommon('resendVerification')}
              </button>
            )}
          </div>
        )}
        <PageLoadingViewport>{children}</PageLoadingViewport>
      </main>

      <LoadingBar />

      <ContactFormModal
        open={contactOpen}
        onClose={() => setContactOpen(false)}
      />

      <ConfirmDialog
        open={logoutConfirm}
        title={tCommon('logoutConfirmTitle')}
        message={tCommon('logoutConfirmMessage')}
        confirmLabel={tCommon('logout')}
        onConfirm={handleLogout}
        onCancel={() => setLogoutConfirm(false)}
      />
    </div>
  )
}
