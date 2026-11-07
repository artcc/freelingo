'use client'

import { useState, useMemo, useEffect } from 'react'
import Link from 'next/link'
import { useTranslations } from 'next-intl'
import { getGrammarTopics, type GrammarTopic } from '@/data/grammar'
import type { GrammarCategory } from '@/data/types'
import { CEFR_LEVELS } from '@/data/curriculum'
import { useLanguageStore } from '@/store/language'
import { PageLoading } from '@/components/ui/page-loading'
import { useAuthStore } from '@/store/auth'

function TopicCard({ topic }: { topic: GrammarTopic }) {
  return (
    <Link
      href={`/grammar/${topic.slug}`}
      className="border-fl-border bg-fl-surface hover:border-fl-border-2 hover:bg-fl-surface-2 group block border transition-colors"
    >
      <div className="space-y-2 px-4 py-4">
        <div className="flex items-start justify-between gap-2">
          <p className="text-fl-fg group-hover:text-fl-fg-bright font-mono text-xs leading-snug font-bold tracking-wide transition-colors">
            {topic.title}
          </p>
          <span className="border-fl-border text-fl-label text-fl-muted-3 shrink-0 border px-1.5 py-0.5 font-mono tracking-widest uppercase">
            {topic.level}
          </span>
        </div>
        <p className="text-fl-label text-fl-muted-2 font-mono leading-relaxed">
          {topic.summary}
        </p>
        <span className="border-fl-border text-fl-label text-fl-muted-3 inline-block border px-2 py-0.5 font-mono tracking-widest uppercase">
          {topic.category}
        </span>
      </div>
    </Link>
  )
}

export default function GrammarIndexPage() {
  const t = useTranslations('grammar')
  const tCommon = useTranslations('common')
  const activeLanguage = useLanguageStore((s) => s.activeLanguage)
  const needsRefresh = useLanguageStore((s) => s.needsRefresh)
  const isSwitching = useLanguageStore((s) => s.isSwitching)
  const invalidationVersion = useLanguageStore((s) => s.invalidationVersion)
  const sessionVersion = useAuthStore((s) => s.sessionVersion)
  const languageCode = activeLanguage?.code
  const scope = `${sessionVersion}:${invalidationVersion}:${languageCode}:${needsRefresh}`
  const [topics, setTopics] = useState<GrammarTopic[]>([])
  const [loading, setLoading] = useState(true)
  const [loadError, setLoadError] = useState(false)
  const [loadedScope, setLoadedScope] = useState<string | null>(null)
  const [attempt, setAttempt] = useState(0)
  const [search, setSearch] = useState('')
  const [activeCategory, setActiveCategory] = useState<GrammarCategory | 'All'>(
    'All'
  )

  useEffect(() => {
    const controller = new AbortController()
    const isCurrent = () => {
      const state = useLanguageStore.getState()
      return (
        !controller.signal.aborted &&
        useAuthStore.getState().sessionVersion === sessionVersion &&
        state.invalidationVersion === invalidationVersion &&
        state.activeLanguage?.code === languageCode &&
        state.needsRefresh === needsRefresh &&
        !state.isSwitching
      )
    }
    setLoading(true)
    setLoadError(false)
    setTopics([])
    async function load() {
      try {
        if (needsRefresh || !languageCode) {
          const ok = await useLanguageStore
            .getState()
            .fetchLanguages(controller.signal)
          if (!isCurrent()) return
          const state = useLanguageStore.getState()
          if (!ok || state.needsRefresh || !state.activeLanguage) {
            throw new Error('Could not resolve active language')
          }
          return
        }
        const data = await getGrammarTopics(languageCode, controller.signal)
        if (isCurrent()) setTopics(data)
      } catch {
        if (isCurrent()) setLoadError(true)
      } finally {
        if (isCurrent()) {
          setLoadedScope(scope)
          setLoading(false)
        }
      }
    }
    if (!isSwitching) void load()
    return () => controller.abort()
  }, [
    languageCode,
    needsRefresh,
    isSwitching,
    invalidationVersion,
    sessionVersion,
    scope,
    attempt,
  ])

  const allCategories: GrammarCategory[] = useMemo(
    () =>
      Array.from(
        new Set(topics.map((t) => t.category))
      ).sort() as GrammarCategory[],
    [topics]
  )

  const filtered = useMemo(() => {
    const q = search.toLowerCase()
    return topics.filter((t) => {
      const matchesSearch =
        !q ||
        t.title.toLowerCase().includes(q) ||
        t.summary.toLowerCase().includes(q) ||
        t.category.toLowerCase().includes(q)
      const matchesCategory =
        activeCategory === 'All' || t.category === activeCategory
      return matchesSearch && matchesCategory
    })
  }, [search, activeCategory, topics])

  const usedCategories = useMemo(() => {
    const cats = new Set(topics.map((t) => t.category))
    return allCategories.filter((c) => cats.has(c))
  }, [topics, allCategories])

  if (loading || loadedScope !== scope || isSwitching) {
    return <PageLoading />
  }

  if (loadError) {
    return (
      <div className="flex min-h-[60vh] flex-col items-center justify-center gap-4">
        <p role="alert" className="text-fl-muted-2 font-mono text-sm">
          {tCommon('error')}
        </p>
        <button
          onClick={() => {
            setLoading(true)
            setAttempt((value) => value + 1)
          }}
          className="text-fl-accent font-mono text-xs tracking-widest uppercase underline"
        >
          {tCommon('retry')}
        </button>
      </div>
    )
  }

  return (
    <div className="mx-auto max-w-4xl space-y-8 p-6">
      <div className="border-fl-border bg-fl-surface border">
        <div className="border-fl-border flex items-center gap-2 border-b px-6 py-4">
          <span className="text-fl-label text-fl-muted-3">{'\u25cf'}</span>
          <span className="text-fl-label text-fl-muted-2 font-mono tracking-widest uppercase">
            {t('title')}
          </span>
        </div>
        <div className="space-y-4 px-6 py-5">
          <p className="text-fl-muted-2 font-mono text-xs leading-relaxed">
            {t('topicsFound', { count: topics.length })} · A1 – C2
          </p>
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder={t('searchPlaceholder')}
            className="bg-fl-bg border-fl-border text-fl-fg placeholder:text-fl-muted-4 focus:border-fl-border-2 w-full max-w-sm border px-4 py-2.5 font-mono text-xs transition-colors focus:outline-none"
          />
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => setActiveCategory('All')}
              className={`text-fl-label border px-3 py-1.5 font-mono tracking-widest uppercase transition-colors ${
                activeCategory === 'All'
                  ? 'border-fl-fg text-fl-fg bg-fl-surface-2'
                  : 'border-fl-border text-fl-muted-3 hover:border-fl-border-2 hover:text-fl-fg'
              }`}
            >
              {t('allCategories')}
            </button>
            {usedCategories.map((cat) => (
              <button
                key={cat}
                onClick={() =>
                  setActiveCategory(activeCategory === cat ? 'All' : cat)
                }
                className={`text-fl-label border px-3 py-1.5 font-mono tracking-widest uppercase transition-colors ${
                  activeCategory === cat
                    ? 'border-fl-fg text-fl-fg bg-fl-surface-2'
                    : 'border-fl-border text-fl-muted-3 hover:border-fl-border-2 hover:text-fl-fg'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>
      </div>

      {(search || activeCategory !== 'All') && (
        <p className="text-fl-label text-fl-muted-3 font-mono">
          {t('topicsFound', { count: filtered.length })}
        </p>
      )}

      {CEFR_LEVELS.map((level) => {
        const levelTopics = filtered.filter((t) => t.level === level)
        if (!levelTopics.length) return null
        return (
          <section key={level} className="space-y-3">
            <div className="flex items-center gap-3">
              <span className="text-fl-fg font-mono text-base font-bold tracking-widest">
                {level}
              </span>
              <div className="bg-fl-border h-px flex-1" />
              <span className="text-fl-label text-fl-muted-3 font-mono">
                {t('topicsFound', { count: levelTopics.length })}
              </span>
            </div>
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {levelTopics.map((t) => (
                <TopicCard key={t.slug} topic={t} />
              ))}
            </div>
          </section>
        )
      })}

      {filtered.length === 0 && (
        <div className="border-fl-border bg-fl-surface space-y-4 border px-6 py-10 text-center">
          <p className="text-fl-muted-3 font-mono text-xs tracking-widest uppercase">
            {t('noResults')}
          </p>
          {(search || activeCategory !== 'All') && (
            <button
              onClick={() => {
                setSearch('')
                setActiveCategory('All')
              }}
              className="text-fl-label border-fl-border text-fl-muted-3 hover:border-fl-border-2 hover:text-fl-fg border px-4 py-2 font-mono tracking-widest uppercase transition-colors"
            >
              {tCommon('clearFilters')}
            </button>
          )}
        </div>
      )}
    </div>
  )
}
