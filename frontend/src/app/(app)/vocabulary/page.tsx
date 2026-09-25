'use client'

import { useState, useEffect, useMemo } from 'react'
import Link from 'next/link'
import { useTranslations } from 'next-intl'
import { apiFetch } from '@/lib/api'
import type { VocabularySet } from '@/data/types'
import { CEFR_LEVELS, type CEFRLevel } from '@/data/curriculum'
import { useLanguageStore } from '@/store/language'

// ── Constants ─────────────────────────────────────────────────────────────────

// ── Set card ──────────────────────────────────────────────────────────────────

function SetCard({ s, wordsLabel }: { s: VocabularySet; wordsLabel: string }) {
  return (
    <Link
      href={`/vocabulary/${s.id}`}
      className="border-fl-border bg-fl-surface hover:border-fl-border-2 hover:bg-fl-surface-2 group block border transition-colors"
    >
      <div className="space-y-2 px-4 py-4">
        <div className="flex items-start justify-between gap-2">
          <p className="text-fl-fg group-hover:text-fl-fg-bright font-mono text-xs leading-snug font-bold tracking-wide transition-colors">
            {s.topic}
          </p>
          <span className="border-fl-border text-fl-label text-fl-muted-3 shrink-0 border px-1.5 py-0.5 font-mono tracking-widest uppercase">
            {s.level}
          </span>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-fl-label text-fl-muted-3 font-mono tracking-widest uppercase">
            {s.words.length} {wordsLabel}
          </span>
          <span className="text-fl-label text-fl-muted-4 font-mono tracking-widest uppercase">
            {s.unit_ref}
          </span>
        </div>
      </div>
    </Link>
  )
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function VocabularyIndexPage() {
  const t = useTranslations('vocabulary')
  const tCommon = useTranslations('common')
  const activeLanguage = useLanguageStore((s) => s.activeLanguage)
  const [activeLevel, setActiveLevel] = useState<CEFRLevel | 'All'>('All')
  const [search, setSearch] = useState('')
  const [vocabSets, setVocabSets] = useState<VocabularySet[]>([])

  useEffect(() => {
    const lang = activeLanguage?.code ?? 'en-GB'
    apiFetch(`/api/vocabulary?language=${lang}`)
      .then((r) => r.json())
      .then((d: { sets: VocabularySet[] }) => setVocabSets(d.sets))
      .catch(() => setVocabSets([]))
  }, [activeLanguage?.code])

  const filtered = useMemo(() => {
    const q = search.toLowerCase()
    return vocabSets.filter((s) => {
      const matchesLevel = activeLevel === 'All' || s.level === activeLevel
      const matchesSearch =
        !q || s.topic.toLowerCase().includes(q) || s.id.includes(q)
      return matchesLevel && matchesSearch
    })
  }, [vocabSets, activeLevel, search])

  const totalWords = vocabSets.reduce((acc, s) => acc + s.words.length, 0)
  const usedLevels = [...new Set(vocabSets.map((s) => s.level))] as CEFRLevel[]

  return (
    <div className="mx-auto max-w-4xl space-y-8 p-6">
      {/* Header */}
      <div className="border-fl-border bg-fl-surface border">
        <div className="border-fl-border flex items-center gap-2 border-b px-6 py-4">
          <span className="text-fl-label text-fl-muted-3">●</span>
          <span className="text-fl-label text-fl-muted-2 font-mono tracking-widest uppercase">
            {t('title')}
          </span>
        </div>
        <div className="space-y-4 px-6 py-5">
          <p className="text-fl-muted-2 font-mono text-xs leading-relaxed">
            {t('sets', { count: vocabSets.length })} · {totalWords} {t('words')}
            {usedLevels.length > 0 && (
              <>
                {' · '}
                {usedLevels[0]} – {usedLevels[usedLevels.length - 1]}
              </>
            )}
          </p>
          {/* Search */}
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder={t('searchPlaceholder')}
            className="bg-fl-bg border-fl-border text-fl-fg placeholder:text-fl-muted-4 focus:border-fl-border-2 w-full max-w-sm border px-4 py-2.5 font-mono text-xs transition-colors focus:outline-none"
          />
          {/* Level filter */}
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => setActiveLevel('All')}
              className={`text-fl-label border px-3 py-1.5 font-mono tracking-widest uppercase transition-colors ${
                activeLevel === 'All'
                  ? 'border-fl-fg text-fl-fg bg-fl-surface-2'
                  : 'border-fl-border text-fl-muted-3 hover:border-fl-border-2 hover:text-fl-fg'
              }`}
            >
              {t('all')}
            </button>
            {usedLevels.map((level) => (
              <button
                key={level}
                onClick={() =>
                  setActiveLevel(activeLevel === level ? 'All' : level)
                }
                className={`text-fl-label border px-3 py-1.5 font-mono tracking-widest uppercase transition-colors ${
                  activeLevel === level
                    ? 'border-fl-fg text-fl-fg bg-fl-surface-2'
                    : 'border-fl-border text-fl-muted-3 hover:border-fl-border-2 hover:text-fl-fg'
                }`}
              >
                {level}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Level sections */}
      {CEFR_LEVELS.map((level) => {
        const sets = filtered.filter((s) => s.level === level)
        if (!sets.length) return null
        return (
          <section key={level} className="space-y-3">
            <div className="flex items-center gap-3">
              <span className="text-fl-fg font-mono text-base font-bold tracking-widest">
                {level}
              </span>
              <div className="bg-fl-border h-px flex-1" />
              <span className="text-fl-label text-fl-muted-3 font-mono">
                {t('sets', { count: sets.length })} ·{' '}
                {sets.reduce((a, s) => a + s.words.length, 0)} {t('words')}
              </span>
            </div>
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {sets.map((s) => (
                <SetCard key={s.id} s={s} wordsLabel={t('words')} />
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
          {(search || activeLevel !== 'All') && (
            <button
              onClick={() => {
                setSearch('')
                setActiveLevel('All')
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
