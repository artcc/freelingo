import Link from 'next/link'
import { cookies } from 'next/headers'
import { getLocale, getTranslations } from 'next-intl/server'
import type { Metadata } from 'next'
import {
  ArrowDown,
  ArrowRight,
  BookOpen,
  Cloud,
  Gamepad2,
  Mic,
  Server,
} from 'lucide-react'
import PricingSection from '@/components/billing/PricingSection'
import { LandingFAQ } from '@/components/ui/landing-faq'
import { LandingNav } from '@/components/ui/landing-nav'
import { ScrollReveal } from '@/components/ui/scroll-reveal'
import { ContactButton } from '@/components/ui/contact-button'
import { LanguageBubbles } from '@/components/LanguageBubbles'
import { TargetLanguageText } from '@/components/TargetLanguageText'
import { LandingReviewsCarousel } from '@/components/reviews/LandingReviewsCarousel'
import type { ReviewPublic, ReviewPublicSummary } from '@/types/api'
import { createPublicMetadata, SITE_URL } from '@/lib/seo'

export async function generateMetadata(): Promise<Metadata> {
  const t = await getTranslations('landing')
  return createPublicMetadata({
    path: '/',
    title: t('seoTitle'),
    description: t('seoDescription'),
    locale: await getLocale(),
  })
}

const jsonLd = {
  '@type': 'WebApplication',
  '@id': `${SITE_URL}/#application`,
  name: 'FreeLingo',
  applicationCategory: 'EducationalApplication',
  operatingSystem: 'Any',
  browserRequirements: 'Requires a modern web browser with JavaScript enabled.',
  url: `${SITE_URL}/`,
  author: {
    '@type': 'Person',
    name: 'Arturo Carretero Calvo',
    url: 'https://www.arturocarreterocalvo.com',
  },
}

export default async function Home() {
  const cookieStore = await cookies()
  const hasSession = cookieStore.has('refresh_token')
  const t = await getTranslations('landing')
  const tCommon = await getTranslations('common')
  const tGames = await getTranslations('games')
  const locale = await getLocale()

  let allowRegistration = false
  let stripeEnabled = false
  let freemiumTrialEnabled = false
  let trialDays = 0
  let priceMonthly = 0.0
  let priceYearly = 0.0
  let totalPriceMonthly = 0.0
  let totalPriceYearly = 0.0
  let reviews: ReviewPublic[] = []
  let reviewSummary: ReviewPublicSummary | null = null
  try {
    const backendUrl = process.env.BACKEND_URL || 'http://backend:8000'
    const [configRes, publicReviews, publicReviewSummary] = await Promise.all([
      // Landing CTAs can lag registration changes by the existing one-hour cache.
      // The backend still enforces ALLOW_REGISTRATION on every signup request.
      fetch(`${backendUrl}/api/config`, {
        next: { revalidate: 3600 },
      }).catch(() => null),
      fetch(`${backendUrl}/api/reviews/public?limit=50`, {
        next: { revalidate: 300 },
      })
        .then((res) => (res.ok ? res.json() : []))
        .catch(() => []),
      fetch(`${backendUrl}/api/reviews/public/summary`, {
        next: { revalidate: 300 },
      })
        .then((res) => (res.ok ? res.json() : null))
        .catch(() => null),
    ])
    reviews = publicReviews
    reviewSummary = publicReviewSummary
    if (configRes?.ok) {
      const cfg = await configRes.json()
      allowRegistration = cfg.allow_registration === true
      stripeEnabled = cfg.stripe_enabled ?? false
      freemiumTrialEnabled = cfg.freemium_trial_enabled === true
      trialDays = cfg.stripe_trial_days ?? 0
      priceMonthly = cfg.price_monthly ?? 0.0
      priceYearly = cfg.price_yearly ?? 0.0
      totalPriceMonthly = cfg.total_price_monthly ?? 0.0
      totalPriceYearly = cfg.total_price_yearly ?? 0.0
    }
  } catch {
    /* non-fatal */
  }

  const startHref = hasSession
    ? '/dashboard'
    : allowRegistration
      ? '/register'
      : '/login'
  const startLabel = hasSession
    ? t('dashboard')
    : allowRegistration
      ? t('startFree')
      : t('signIn')
  const showFreeNote = !hasSession && allowRegistration && stripeEnabled
  const startClassName =
    'bg-fl-accent text-fl-accent-fg hover:bg-fl-accent/90 focus-visible:outline-fl-accent inline-flex items-center justify-center gap-3 px-6 py-3 text-center font-sans text-sm font-bold transition-colors focus-visible:outline-2 focus-visible:outline-offset-4 motion-reduce:transition-none'

  return (
    <div className="bg-fl-bg text-fl-fg flex min-h-screen flex-col">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            '@context': 'https://schema.org',
            '@graph': [
              {
                '@type': 'WebSite',
                '@id': `${SITE_URL}/#website`,
                name: 'FreeLingo',
                url: `${SITE_URL}/`,
                inLanguage: locale,
                about: { '@id': jsonLd['@id'] },
              },
              {
                ...jsonLd,
                description: t('seoDescription'),
                inLanguage: locale,
                // Describe only the free signup actually offered on this response.
                ...(allowRegistration && !hasSession
                  ? {
                      offers: {
                        '@type': 'Offer',
                        name: t('startFree'),
                        price: 0,
                        url: `${SITE_URL}/register`,
                      },
                    }
                  : {}),
              },
            ],
          }).replace(/</g, '\\u003c'),
        }}
      />

      {/* Nav */}
      <LandingNav
        hasSession={hasSession}
        stripeEnabled={stripeEnabled}
        navFeatures={t('navFeatures')}
        navReviews={t('navReviews')}
        navPricing={t('navPricing')}
        navFAQ={t('navFAQ')}
        showReviews={reviews.length > 0 || (reviewSummary?.total ?? 0) > 0}
        signIn={t('signIn')}
        dashboard={t('dashboard')}
      />

      <main className="contents">
        {/* Hero */}
        <section className="flex flex-1 flex-col items-center justify-center px-6 pt-[10px] pb-12 text-center">
          <div className="mb-1 flex w-full flex-col items-center">
            <div className="mb-0 w-full max-w-[560px]">
              <LanguageBubbles />
            </div>
            <span className="text-fl-label text-fl-muted-2 mb-4 font-mono tracking-widest uppercase">
              {tCommon('tagline')}
            </span>
            <h1 className="text-fl-fg mb-4 max-w-2xl font-sans text-3xl leading-tight font-bold tracking-tight text-balance md:text-5xl">
              {t('hero')}
            </h1>
            <p className="text-fl-muted-1 mb-8 max-w-xl font-sans text-base leading-relaxed md:text-lg">
              {t('heroSub')}
            </p>
          </div>
          <div className="flex flex-col items-center gap-3 sm:flex-row">
            <Link href={startHref} className={startClassName}>
              {startLabel}
              <ArrowRight className="size-4 shrink-0" aria-hidden="true" />
            </Link>
            <a
              href="#features"
              className="border-fl-border text-fl-muted-1 hover:text-fl-fg hover:border-fl-border-2 focus-visible:outline-fl-accent inline-flex items-center justify-center gap-2 border px-6 py-3 font-sans text-sm transition-colors focus-visible:outline-2 focus-visible:outline-offset-4 motion-reduce:transition-none"
            >
              {t('howItWorks')}
              <ArrowDown className="size-4 shrink-0" aria-hidden="true" />
            </a>
          </div>
          {showFreeNote && (
            <p className="text-fl-muted-1 mt-4 max-w-lg font-sans text-sm leading-relaxed">
              {t(freemiumTrialEnabled ? 'freeTrialNote' : 'freeNote')}
            </p>
          )}
          <p className="text-fl-muted-1 mt-4 max-w-xl font-sans text-sm leading-relaxed">
            {t('modes.intro')}{' '}
            <a
              href="#modalities"
              className="text-fl-accent focus-visible:outline-fl-accent underline underline-offset-4 focus-visible:outline-2 focus-visible:outline-offset-4"
            >
              {t('modes.compare')}
            </a>
          </p>
        </section>

        {/* Learning journey */}
        <section
          id="features"
          aria-labelledby="how-it-works-title"
          className="mx-auto w-full max-w-5xl scroll-mt-20 px-6 pb-20"
        >
          <h2
            id="how-it-works-title"
            className="text-fl-fg mb-10 font-sans text-2xl font-bold tracking-tight md:text-3xl"
          >
            {t('journey.title')}
          </h2>
          <ol className="grid list-none md:grid-cols-3">
            {[
              { key: 'learn', Icon: BookOpen },
              { key: 'practice', Icon: Gamepad2 },
              { key: 'speak', Icon: Mic },
            ].map(({ key, Icon }, index) => (
              <li
                key={key}
                className="relative pb-8 pl-16 last:pb-0 md:pr-8 md:pb-0 md:pl-0 md:last:pr-0"
              >
                {index < 2 && (
                  <span
                    aria-hidden="true"
                    className="bg-fl-border absolute top-6 bottom-0 left-6 w-px md:right-0 md:bottom-auto md:h-px md:w-auto"
                  />
                )}
                <span
                  aria-hidden="true"
                  className="border-fl-accent/40 bg-fl-bg text-fl-accent font-code absolute top-0 left-0 flex size-12 items-center justify-center border text-sm md:relative md:mb-5"
                >
                  {String(index + 1).padStart(2, '0')}
                </span>
                <Icon
                  className="text-fl-accent mb-3 size-5"
                  aria-hidden="true"
                />
                <h3 className="text-fl-fg mb-3 font-sans text-lg font-semibold tracking-tight">
                  {t(`journey.${key}Title`)}
                </h3>
                <p className="text-fl-muted-1 font-sans text-base leading-relaxed">
                  {t(`journey.${key}Desc`)}
                </p>
                {key === 'practice' && (
                  <ul className="border-fl-border text-fl-muted-1 mt-4 space-y-1 border-l-2 pl-3 font-sans text-sm leading-relaxed">
                    {[
                      'detectiveTitle',
                      'sentenceOrderTitle',
                      'vocabularyPairsTitle',
                    ].map((game) => (
                      <li key={game}>{tGames(game)}</li>
                    ))}
                  </ul>
                )}
              </li>
            ))}
          </ol>

          <div className="border-fl-border mt-10 grid items-center gap-8 border-t pt-8 md:grid-cols-2 md:gap-12">
            <div>
              <h3 className="text-fl-fg mb-4 max-w-sm font-sans text-2xl leading-snug font-semibold tracking-tight text-balance">
                {t('journey.contextTitle')}
              </h3>
              <p className="text-fl-muted-1 font-sans text-base leading-relaxed">
                {t('journey.contextDesc')}
              </p>
              <p className="text-fl-muted-1 mt-4 font-sans text-sm leading-relaxed">
                {t('journey.support')}
              </p>
            </div>
            <section
              aria-labelledby="lingu-demo-title"
              className="border-fl-border bg-fl-surface min-w-0 border"
            >
              <div className="border-fl-border border-b px-5 py-4 sm:px-6">
                <h3
                  id="lingu-demo-title"
                  className="text-fl-fg font-sans text-base font-bold"
                >
                  {t('microDemo.title')}
                </h3>
                <p className="text-fl-muted-1 mt-1 font-sans text-sm">
                  {t('microDemo.exampleLabel')}
                </p>
              </div>
              <div className="space-y-5 p-5 sm:p-6">
                <div>
                  <p className="text-fl-muted-1 mb-2 font-sans text-sm">
                    {t('microDemo.questionLabel')}
                  </p>
                  <TargetLanguageText
                    as="p"
                    languageCode="en-GB"
                    className="text-fl-fg text-base leading-relaxed"
                  >
                    What did you do yesterday?
                  </TargetLanguageText>
                </div>
                <div className="border-fl-border border-l-2 pl-4">
                  <p className="text-fl-muted-1 mb-2 font-sans text-sm">
                    {t('microDemo.answerLabel')}
                  </p>
                  <TargetLanguageText
                    as="p"
                    languageCode="en-GB"
                    className="text-fl-fg-2 text-base leading-relaxed"
                  >
                    Yesterday I go to the park.
                  </TargetLanguageText>
                </div>
                <div className="border-fl-accent/40 border-l-2 pl-4">
                  <p className="text-fl-muted-1 mb-2 font-sans text-sm">
                    {t('microDemo.correctionLabel')}
                  </p>
                  <TargetLanguageText
                    as="p"
                    languageCode="en-GB"
                    className="text-fl-fg text-base leading-relaxed"
                  >
                    Yesterday I{' '}
                    <strong className="font-bold underline underline-offset-4">
                      went
                    </strong>{' '}
                    to the park.
                  </TargetLanguageText>
                  <p className="text-fl-muted-1 mt-2 font-sans text-sm leading-relaxed">
                    {t('microDemo.explanation')}
                  </p>
                </div>
              </div>
            </section>
          </div>
          <div className="mt-8 flex flex-col items-center gap-3 text-center">
            <Link href={startHref} className={startClassName}>
              {startLabel}
              <ArrowRight className="size-4 shrink-0" aria-hidden="true" />
            </Link>
            {showFreeNote && (
              <p className="text-fl-muted-1 max-w-lg font-sans text-sm leading-relaxed">
                {t(freemiumTrialEnabled ? 'freeTrialNote' : 'freeNote')}
              </p>
            )}
          </div>
        </section>

        {/* Reviews */}
        <ScrollReveal>
          <LandingReviewsCarousel reviews={reviews} summary={reviewSummary} />
        </ScrollReveal>

        {/* Cloud and self-hosting */}
        <section
          id="modalities"
          aria-labelledby="modalities-title"
          className="mx-auto w-full max-w-5xl scroll-mt-20 px-6 pb-16"
        >
          <h2
            id="modalities-title"
            className="text-fl-fg mb-8 font-sans text-2xl font-bold tracking-tight md:text-3xl"
          >
            {t('modes.title')}
          </h2>
          <div className="grid gap-4 md:grid-cols-2">
            {[
              { key: 'cloud', Icon: Cloud, href: `${SITE_URL}/login` },
              {
                key: 'selfHosted',
                Icon: Server,
                href: 'https://github.com/artcc/freelingo#quick-start',
              },
            ].map(({ key, Icon, href }) => (
              <article
                key={key}
                className="border-fl-border bg-fl-surface flex flex-col border p-6"
              >
                <Icon
                  className="text-fl-accent mb-4 size-5"
                  aria-hidden="true"
                />
                <h3 className="text-fl-fg mb-3 font-sans text-lg font-semibold">
                  {t(`modes.${key}.title`)}
                </h3>
                <p className="text-fl-muted-1 font-sans text-base leading-relaxed">
                  {t(`modes.${key}.description`)}
                </p>
                <ul className="text-fl-muted-1 mt-4 mb-6 list-disc space-y-2 pl-5 font-sans text-sm leading-relaxed">
                  {['setup', 'access', 'cost'].map((detail) => (
                    <li key={detail}>{t(`modes.${key}.${detail}`)}</li>
                  ))}
                </ul>
                <a
                  href={href}
                  className="text-fl-accent focus-visible:outline-fl-accent mt-auto inline-flex items-center gap-2 self-start font-sans text-sm font-semibold underline underline-offset-4 focus-visible:outline-2 focus-visible:outline-offset-4"
                >
                  {t(`modes.${key}.cta`)}
                  <ArrowRight className="size-4 shrink-0" aria-hidden="true" />
                </a>
              </article>
            ))}
          </div>
          <p className="text-fl-muted-1 mt-4 max-w-3xl font-sans text-sm leading-relaxed">
            {t('modes.accounts')}
          </p>
        </section>

        {/* Pricing */}
        <ScrollReveal>
          <div id="pricing" className="scroll-mt-16">
            <PricingSection
              allowRegistration={allowRegistration}
              stripeEnabled={stripeEnabled}
              freemiumTrialEnabled={freemiumTrialEnabled}
              trialDays={trialDays}
              hasSession={hasSession}
              priceMonthly={priceMonthly}
              priceYearly={priceYearly}
              totalPriceMonthly={totalPriceMonthly}
              totalPriceYearly={totalPriceYearly}
            />
          </div>
        </ScrollReveal>

        {/* FAQ */}
        <ScrollReveal>
          <section
            id="faq"
            className="mx-auto w-full max-w-5xl scroll-mt-16 px-6 pb-16"
          >
            <h2 className="text-fl-label text-fl-muted-2 mb-8 text-center font-mono tracking-widest uppercase">
              {t('faqTitle')}
            </h2>
            <LandingFAQ />
          </section>
        </ScrollReveal>
      </main>

      {/* Footer */}
      <footer className="border-fl-border border-t px-6 py-10">
        <div className="mx-auto grid max-w-4xl grid-cols-2 gap-8 md:grid-cols-4">
          <div>
            <span className="text-fl-hint text-fl-muted-3 font-code block tracking-widest uppercase">
              FreeLingo
            </span>
            <span className="text-fl-hint text-fl-muted-4 mt-2 block font-mono leading-relaxed">
              © {new Date().getFullYear()}
            </span>
          </div>
          <div>
            <h2 className="text-fl-label text-fl-muted-2 mb-3 font-sans text-sm font-semibold tracking-tight">
              {t('footerProduct')}
            </h2>
            <div className="flex flex-col gap-2">
              <a
                href="https://github.com/artcc/freelingo"
                target="_blank"
                rel="noopener noreferrer"
                className="text-fl-hint text-fl-muted-3 hover:text-fl-muted-1 font-mono tracking-widest uppercase transition-colors"
              >
                {t('github')}
              </a>
            </div>
          </div>
          <div>
            <h2 className="text-fl-label text-fl-muted-2 mb-3 font-sans text-sm font-semibold tracking-tight">
              {t('footerLegal')}
            </h2>
            <div className="flex flex-col gap-2">
              <Link
                href="/privacy?from=landing"
                className="text-fl-hint text-fl-muted-3 hover:text-fl-muted-1 font-mono tracking-widest uppercase transition-colors"
              >
                {t('privacy')}
              </Link>
              <Link
                href="/terms?from=landing"
                className="text-fl-hint text-fl-muted-3 hover:text-fl-muted-1 font-mono tracking-widest uppercase transition-colors"
              >
                {t('terms')}
              </Link>
            </div>
          </div>
          <div>
            <h2 className="text-fl-label text-fl-muted-2 mb-3 font-sans text-sm font-semibold tracking-tight">
              {t('contact')}
            </h2>
            <div className="flex flex-col gap-2">
              <a
                href="https://www.arturocarreterocalvo.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-fl-hint text-fl-muted-3 hover:text-fl-muted-1 font-mono tracking-widest uppercase transition-colors"
              >
                {t('aboutMe')}
              </a>
              <ContactButton />
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
