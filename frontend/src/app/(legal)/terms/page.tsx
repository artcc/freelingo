'use client'

import Link from 'next/link'
import Image from 'next/image'
import { useTranslations } from 'next-intl'
import { useSearchParams } from 'next/navigation'

export default function TermsPage() {
  const t = useTranslations('legal.terms')
  const tCommon = useTranslations('common')
  const searchParams = useSearchParams()
  const from = searchParams.get('from')
  const isFromSettings = from === 'settings'
  const isFromRegister = from === 'register'
  const isFromLanding = from === 'landing'
  const backHref = isFromSettings
    ? '/settings'
    : isFromRegister
      ? '/register'
      : isFromLanding
        ? '/'
        : '/'
  const backLabel = isFromSettings
    ? t('linkBackSettings')
    : isFromRegister
      ? t('linkBack')
      : tCommon('back')
  const privacyHref = isFromSettings
    ? '/privacy?from=settings'
    : isFromRegister
      ? '/privacy?from=register'
      : isFromLanding
        ? '/privacy?from=landing'
        : '/privacy'
  const s2Items = [t('s2i1'), t('s2i2'), t('s2i3'), t('s2i4')]

  return (
    <div>
      <div className="mb-10 flex flex-col items-center">
        <Link href="/">
          <Image
            src="/logo.png"
            alt="FreeLingo"
            width={48}
            height={48}
            className="mb-3"
          />
        </Link>
        <h1 className="text-fl-fg font-code text-xl font-bold tracking-widest uppercase">
          FreeLingo
        </h1>
        <p className="text-fl-caption text-fl-muted-2 mt-1 font-mono tracking-widest uppercase">
          {tCommon('tagline')}
        </p>
      </div>

      <div className="border-fl-border bg-fl-surface space-y-8 border p-8">
        <div className="border-fl-border flex items-center gap-2 border-b pb-4">
          <span className="text-fl-label text-fl-muted-2">●</span>
          <span className="text-fl-muted-2 font-mono text-xs tracking-widest uppercase">
            {t('pageTitle')}
          </span>
        </div>

        <p className="text-fl-hint text-fl-muted-2 font-mono tracking-wide">
          {t('updated')}
        </p>

        <section className="space-y-3">
          <h2 className="text-fl-fg font-mono text-sm font-bold tracking-widest uppercase">
            {t('s1Title')}
          </h2>
          <p className="text-fl-fg-2 font-mono text-sm leading-relaxed">
            {t('s1Body')}
          </p>
        </section>

        <section className="space-y-3">
          <h2 className="text-fl-fg font-mono text-sm font-bold tracking-widest uppercase">
            {t('s2Title')}
          </h2>
          <p className="text-fl-fg-2 font-mono text-sm leading-relaxed">
            {t('s2Intro')}
          </p>
          <ul className="space-y-1 pl-4">
            {s2Items.map((item) => (
              <li
                key={item}
                className="text-fl-fg-2 flex gap-2 font-mono text-sm leading-relaxed"
              >
                <span className="text-fl-muted-2 flex-shrink-0">—</span>
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </section>

        {[
          { title: t('s3Title'), body: t('s3Body') },
          { title: t('s4Title'), body: t('s4Body') },
          { title: t('s5Title'), body: t('s5Body') },
          { title: t('s6Title'), body: t('s6Body') },
          { title: t('s7Title'), body: t('s7Body') },
          { title: t('s8Title'), body: t('s8Body') },
          { title: t('s9Title'), body: t('s9Body') },
          { title: t('s10Title'), body: t('s10Body') },
          { title: t('s11Title'), body: t('s11Body') },
        ].map((section) => (
          <section key={section.title} className="space-y-3">
            <h2 className="text-fl-fg font-mono text-sm font-bold tracking-widest uppercase">
              {section.title}
            </h2>
            <p className="text-fl-fg-2 font-mono text-sm leading-relaxed">
              {section.body}
            </p>
          </section>
        ))}

        <p className="text-fl-muted-2 font-mono text-xs tracking-wide">
          {t('linkContact')}
        </p>

        <div className="border-fl-border flex gap-6 border-t pt-4">
          <Link
            href={privacyHref}
            className="text-fl-muted-2 hover:text-fl-fg font-mono text-xs tracking-widest uppercase transition-colors"
          >
            {t('linkPrivacy')}
          </Link>
          <Link
            href={backHref}
            className="text-fl-muted-2 hover:text-fl-fg font-mono text-xs tracking-widest uppercase transition-colors"
          >
            {backLabel}
          </Link>
        </div>
      </div>
    </div>
  )
}
