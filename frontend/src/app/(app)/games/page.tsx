'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { useTranslations } from 'next-intl'
import { availableGames } from '@/lib/games'
import { useLanguageStore } from '@/store/language'
import { useAuthStore } from '@/store/auth'
import NoPlanBanner from '@/components/plan/NoPlanBanner'
import { PageLoading } from '@/components/ui/page-loading'

export default function GamesPage() {
  const language = useLanguageStore((s) => s.activeLanguage)
  const activeTrack = useLanguageStore((s) =>
    s.userLanguages.find(
      (item) => item.is_active && item.target_language === language?.code
    )
  )
  const needsRefresh = useLanguageStore((s) => s.needsRefresh)
  const switching = useLanguageStore((s) => s.isSwitching)
  const version = useLanguageStore((s) => s.invalidationVersion)
  const sessionVersion = useAuthStore((s) => s.sessionVersion)
  const [verifiedSession, setVerifiedSession] = useState<number | null>(null)

  if (switching) return <PageLoading />
  if (verifiedSession !== sessionVersion || needsRefresh || !activeTrack)
    return (
      <GamesContextRecovery
        key={`${sessionVersion}:${version}`}
        sessionVersion={sessionVersion}
        onReady={setVerifiedSession}
      />
    )
  if (!activeTrack.plan) return <NoPlanBanner />

  return <GamesContent />
}

function GamesContextRecovery({
  sessionVersion,
  onReady,
}: {
  sessionVersion: number
  onReady: (sessionVersion: number) => void
}) {
  const common = useTranslations('common')
  const fetchLanguages = useLanguageStore((s) => s.fetchLanguages)
  const [failed, setFailed] = useState(false)
  const [attempt, setAttempt] = useState(0)

  useEffect(() => {
    const controller = new AbortController()
    void fetchLanguages(controller.signal).then((ok) => {
      if (
        controller.signal.aborted ||
        useAuthStore.getState().sessionVersion !== sessionVersion
      )
        return
      const context = useLanguageStore.getState()
      const activeTrack = context.userLanguages.find(
        (item) =>
          item.is_active &&
          item.target_language === context.activeLanguage?.code
      )
      if (ok && !context.needsRefresh && activeTrack) onReady(sessionVersion)
      else setFailed(true)
    })
    return () => controller.abort()
  }, [fetchLanguages, attempt, sessionVersion, onReady])

  if (!failed) return <PageLoading />
  return (
    <div className="space-y-3 p-6 text-center">
      <p role="alert" className="text-fl-error-fg">
        {common('errorMessage')}
      </p>
      <button
        className="border-fl-border text-fl-fg border px-4 py-2 text-sm"
        onClick={() => {
          setFailed(false)
          setAttempt((value) => value + 1)
        }}
      >
        {common('retry')}
      </button>
    </div>
  )
}

function GamesContent() {
  const t = useTranslations('games')

  return (
    <div className="mx-auto max-w-4xl space-y-8 p-6">
      <div className="border-fl-border bg-fl-surface border">
        <div className="border-fl-border flex items-center gap-2 border-b px-6 py-4">
          <span aria-hidden="true" className="text-fl-label text-fl-muted-3">
            ●
          </span>
          <h1 className="text-fl-label text-fl-muted-2 font-sans tracking-widest uppercase">
            {t('title')}
          </h1>
        </div>
        <div className="px-6 py-5">
          <p className="text-fl-muted-2 font-sans text-sm leading-relaxed">
            {t('description')}
          </p>
        </div>
      </div>

      {availableGames.length === 0 ? (
        <section
          aria-labelledby="games-empty-title"
          className="border-fl-border bg-fl-surface space-y-4 border px-6 py-10 text-center"
        >
          <h2
            id="games-empty-title"
            className="text-fl-fg font-sans text-base font-semibold"
          >
            {t('emptyTitle')}
          </h2>
          <p className="text-fl-muted-2 mx-auto max-w-lg font-sans text-sm leading-relaxed">
            {t('emptyDescription')}
          </p>
          <Link
            href="/plan"
            className="text-fl-label border-fl-border text-fl-muted-3 hover:border-fl-border-2 hover:text-fl-fg inline-block border px-4 py-2 font-sans tracking-widest uppercase transition-colors"
          >
            {t('goToPlan')}
          </Link>
        </section>
      ) : (
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {availableGames.map((game) => (
            <Link
              key={game.id}
              href={game.href}
              className="border-fl-border bg-fl-surface hover:border-fl-border-2 hover:bg-fl-surface-2 group block overflow-hidden border transition-colors"
            >
              <div className="relative aspect-video w-full overflow-hidden">
                <Image
                  src={`/game/${game.id}.jpeg`}
                  alt=""
                  fill
                  sizes="(min-width: 1024px) 33vw, (min-width: 640px) 50vw, 100vw"
                  className="object-cover transition-transform duration-300 group-hover:scale-105"
                />
              </div>
              <div className="space-y-2 p-4">
                <h2 className="text-fl-fg group-hover:text-fl-fg-bright font-sans text-sm font-semibold transition-colors">
                  {t(game.titleKey)}
                </h2>
                <p className="text-fl-muted-2 font-sans text-sm leading-relaxed">
                  {t(game.descriptionKey)}
                </p>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}
