'use client'

import Link from 'next/link'
import { useTranslations } from 'next-intl'
import { availableGames } from '@/lib/games'

export default function GamesPage() {
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
              className="border-fl-border bg-fl-surface hover:border-fl-border-2 hover:bg-fl-surface-2 group block space-y-2 border px-4 py-4 transition-colors"
            >
              <h2 className="text-fl-fg group-hover:text-fl-fg-bright font-sans text-sm font-semibold transition-colors">
                {t(game.titleKey)}
              </h2>
              <p className="text-fl-muted-2 font-sans text-sm leading-relaxed">
                {t(game.descriptionKey)}
              </p>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}
