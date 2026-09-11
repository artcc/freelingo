'use client'

import { useState, useMemo, useEffect, useCallback } from 'react'
import { useTranslations } from 'next-intl'
import {
  getPhrasebookCategories,
  getPhrasebookNativeHelp,
  type PhrasebookNativeHelp,
  type PhrasebookCategory,
  type Register,
} from '@/data/phrasebook'
import type { CEFRLevel } from '@/data/types'
import { useLanguageStore } from '@/store/language'
import { AudioPlayer } from '@/components/ui/AudioPlayer'
import { PageLoading } from '@/components/ui/page-loading'
import { TargetLanguageText } from '@/components/TargetLanguageText'
import { useAuthStore } from '@/store/auth'

const CEFR_LEVELS: CEFRLevel[] = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
const REGISTERS: Register[] = ['formal', 'neutral', 'informal']

const REGISTER_COLORS: Record<string, string> = {
  formal: 'text-blue-600 dark:text-blue-400',
  neutral: 'text-fl-muted-2',
  informal: 'text-amber-600 dark:text-amber-400',
}

function CategoryCard({
  cat,
  registerFilter,
  search,
  language,
}: {
  cat: PhrasebookCategory
  registerFilter: Register | 'All'
  search: string
  language: string
}) {
  const t = useTranslations('phrasebook')
  const tCommon = useTranslations('common')
  const tTargetLang = useTranslations('targetLanguages')
  const user = useAuthStore((s) => s.user)
  const nativeLanguageName = user?.native_language
    ? tTargetLang(user.native_language)
    : ''
  const [nativeHelpOpen, setNativeHelpOpen] = useState(
    cat.level === 'A1' || cat.level === 'A2'
  )
  const [nativeHelp, setNativeHelp] = useState<PhrasebookNativeHelp | null>(
    null
  )
  const [loadingNativeHelp, setLoadingNativeHelp] = useState(false)
  const [nativeHelpError, setNativeHelpError] = useState(false)
  const phrases = cat.phrases.filter((p) => {
    const matchesRegister =
      registerFilter === 'All' || p.register === registerFilter
    const matchesSearch =
      !search || p.text.toLowerCase().includes(search.toLowerCase())
    return matchesRegister && matchesSearch
  })

  if (!phrases.length) return null

  async function generateNativeHelp() {
    if (loadingNativeHelp) return
    setLoadingNativeHelp(true)
    setNativeHelpError(false)
    try {
      const help = await getPhrasebookNativeHelp(cat.id, language)
      if (help) {
        setNativeHelp(help)
      } else {
        setNativeHelpError(true)
      }
    } catch {
      setNativeHelpError(true)
    } finally {
      setLoadingNativeHelp(false)
    }
  }

  return (
    <div className="border-fl-border bg-fl-surface border">
      <div className="border-fl-border flex items-center gap-3 border-b px-5 py-4">
        <span className="text-xl">{cat.icon}</span>
        <div className="min-w-0 flex-1">
          <p className="text-fl-fg truncate font-mono text-xs font-bold tracking-wide">
            {cat.situation}
          </p>
        </div>
        <span className="border-fl-border text-fl-label text-fl-muted-3 shrink-0 border px-2 py-0.5 font-mono tracking-widest uppercase">
          {cat.level}
        </span>
      </div>

      {nativeLanguageName && (
        <div className="border-fl-border border-b px-5 py-3">
          <button
            type="button"
            onClick={() => setNativeHelpOpen((open) => !open)}
            className="text-fl-label text-fl-muted-3 hover:text-fl-fg flex w-full items-center justify-between font-mono tracking-widest uppercase transition-colors"
            aria-expanded={nativeHelpOpen}
          >
            <span>
              {tCommon('nativeHelpTitle', { language: nativeLanguageName })}
            </span>
            <span>{nativeHelpOpen ? '−' : '+'}</span>
          </button>
          {nativeHelpOpen && (
            <div className="mt-3 space-y-3">
              {loadingNativeHelp ? (
                <p className="text-fl-muted-3 font-mono text-xs">
                  {tCommon('nativeHelpLoading', {
                    language: nativeLanguageName,
                  })}
                </p>
              ) : nativeHelp ? (
                <>
                  <p className="text-fl-muted-1 max-w-[70ch] text-base leading-relaxed">
                    {nativeHelp.summary}
                  </p>

                  {nativeHelp.usage_tips.length > 0 && (
                    <div className="space-y-1">
                      <p className="text-fl-label text-fl-muted-3 font-mono tracking-widest uppercase">
                        {tCommon('nativeHelpUsageTips')}
                      </p>
                      <ul className="space-y-1">
                        {nativeHelp.usage_tips.map((tip, i) => (
                          <li
                            key={i}
                            className="text-fl-muted-1 max-w-[70ch] text-sm leading-relaxed"
                          >
                            <span className="text-fl-muted-3 mr-2">·</span>
                            {tip}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {nativeHelp.register_notes.length > 0 && (
                    <div className="border-fl-border space-y-1 border-t pt-3">
                      <p className="text-fl-label text-fl-muted-3 font-mono tracking-widest uppercase">
                        {tCommon('nativeHelpRegisterNotes')}
                      </p>
                      {nativeHelp.register_notes.map((note, i) => (
                        <p
                          key={i}
                          className="text-fl-muted-1 max-w-[70ch] text-sm leading-relaxed"
                        >
                          {note}
                        </p>
                      ))}
                    </div>
                  )}

                  {nativeHelp.phrase_notes.length > 0 && (
                    <div className="border-fl-border space-y-2 border-t pt-3">
                      <p className="text-fl-label text-fl-muted-3 font-mono tracking-widest uppercase">
                        {tCommon('nativeHelpPhraseNotes')}
                      </p>
                      {nativeHelp.phrase_notes.map((item, i) => (
                        <div key={i} className="space-y-0.5">
                          <TargetLanguageText
                            languageCode={language}
                            className="text-fl-muted-1 text-sm italic"
                          >
                            {item.phrase}
                          </TargetLanguageText>
                          <p className="text-fl-muted-1 text-sm leading-relaxed">
                            {item.note}
                          </p>
                        </div>
                      ))}
                    </div>
                  )}

                  {nativeHelp.common_traps.length > 0 && (
                    <div className="border-fl-border space-y-2 border-t pt-3">
                      <p className="text-fl-label text-fl-muted-3 font-mono tracking-widest uppercase">
                        {tCommon('nativeHelpCommonTraps')}
                      </p>
                      {nativeHelp.common_traps.map((trap, i) => (
                        <div key={i} className="space-y-0.5">
                          <p className="text-fl-muted-2 text-sm">
                            {trap.mistake}
                          </p>
                          <p className="text-fl-muted-1 text-sm leading-relaxed">
                            {trap.fix}
                          </p>
                        </div>
                      ))}
                    </div>
                  )}

                  {nativeHelp.mini_glossary.length > 0 && (
                    <div className="border-fl-border space-y-2 border-t pt-3">
                      <p className="text-fl-label text-fl-muted-3 font-mono tracking-widest uppercase">
                        {tCommon('nativeHelpMiniGlossary')}
                      </p>
                      {nativeHelp.mini_glossary.map((item, i) => (
                        <div key={i}>
                          <TargetLanguageText
                            languageCode={language}
                            className="text-fl-muted-1 text-sm font-bold"
                          >
                            {item.term}
                          </TargetLanguageText>
                          <p className="text-fl-muted-2 text-sm">
                            {item.meaning}
                          </p>
                          {item.note && (
                            <p className="text-fl-muted-1 text-sm leading-relaxed">
                              {item.note}
                            </p>
                          )}
                        </div>
                      ))}
                    </div>
                  )}
                </>
              ) : (
                <button
                  type="button"
                  onClick={generateNativeHelp}
                  className="text-fl-muted-3 hover:text-fl-fg font-mono text-sm transition-colors"
                >
                  {nativeHelpError
                    ? tCommon('retry')
                    : tCommon('nativeHelpShow', {
                        language: nativeLanguageName,
                      })}
                </button>
              )}
            </div>
          )}
        </div>
      )}

      <ul className="divide-fl-border divide-y">
        {phrases.map((phrase, i) => (
          <li key={i} className="group space-y-1 px-5 py-3">
            <div className="flex items-start justify-between gap-3">
              <TargetLanguageText
                as="p"
                languageCode={language}
                className="text-fl-fg flex-1"
              >
                {phrase.text}
              </TargetLanguageText>
              <div className="flex shrink-0 items-center gap-1">
                <span
                  className={`text-fl-label font-mono tracking-widest uppercase ${REGISTER_COLORS[phrase.register]}`}
                >
                  {t(phrase.register)}
                </span>
                <AudioPlayer
                  text={phrase.text}
                  size="sm"
                  audioUrl={`/api/phrasebook/audio/${encodeURIComponent(cat.id)}/${cat.phrases.indexOf(phrase)}?language=${encodeURIComponent(language)}`}
                />
                <CopyButton text={phrase.text} />
              </div>
            </div>
            {phrase.context && (
              <TargetLanguageText
                as="p"
                languageCode={language}
                className="text-fl-muted-1 italic"
              >
                {phrase.context}
              </TargetLanguageText>
            )}
          </li>
        ))}
      </ul>
    </div>
  )
}

function CopyButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false)

  async function handleCopy() {
    try {
      await navigator.clipboard.writeText(text)
      setCopied(true)
      setTimeout(() => setCopied(false), 1500)
    } catch {
      /* ignore */
    }
  }

  return (
    <button
      onClick={handleCopy}
      className="text-fl-label text-fl-muted-4 hover:text-fl-fg px-1 font-mono transition-colors"
      title="Copy"
      aria-label="Copy phrase"
    >
      {copied ? '\u2713' : '\u{1f4cb}'}
    </button>
  )
}

export default function PhrasebookPage() {
  const t = useTranslations('phrasebook')
  const tCommon = useTranslations('common')
  const activeLanguage = useLanguageStore((s) => s.activeLanguage)
  const [categories, setCategories] = useState<PhrasebookCategory[]>([])
  const [loading, setLoading] = useState(true)
  const [loadError, setLoadError] = useState(false)
  const [activeLevel, setActiveLevel] = useState<CEFRLevel | 'All'>('All')
  const [activeRegister, setActiveRegister] = useState<Register | 'All'>('All')
  const [search, setSearch] = useState('')

  const fetchCategories = useCallback(async (lang: string) => {
    setLoading(true)
    setLoadError(false)
    try {
      const data = await getPhrasebookCategories(lang)
      setCategories(data)
    } catch {
      setLoadError(true)
      setCategories([])
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchCategories(activeLanguage?.code ?? 'en-GB')
  }, [activeLanguage?.code, fetchCategories])

  const filteredCategories = useMemo(() => {
    return categories.filter((cat) => {
      const matchesLevel = activeLevel === 'All' || cat.level === activeLevel
      const matchesRegister =
        activeRegister === 'All' ||
        cat.phrases.some((p) => p.register === activeRegister)
      const matchesSearch =
        !search ||
        cat.phrases.some((p) =>
          p.text.toLowerCase().includes(search.toLowerCase())
        )
      return matchesLevel && matchesRegister && matchesSearch
    })
  }, [activeLevel, activeRegister, search, categories])

  const totalPhrases = categories.reduce((acc, c) => acc + c.phrases.length, 0)

  if (loading) {
    return <PageLoading />
  }

  if (loadError) {
    return (
      <div className="flex min-h-[60vh] flex-col items-center justify-center gap-4">
        <p className="text-fl-muted-2 font-mono text-sm">{tCommon('error')}</p>
        <button
          onClick={() => fetchCategories(activeLanguage?.code ?? 'en-GB')}
          className="text-fl-accent font-mono text-xs tracking-widest uppercase underline"
        >
          {tCommon('retry')}
        </button>
      </div>
    )
  }

  const hasActiveFilters =
    activeLevel !== 'All' || activeRegister !== 'All' || !!search

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
            {t('statsLine', {
              situationCount: categories.length,
              phraseCount: totalPhrases,
              range: `${CEFR_LEVELS[0]} \u2013 ${CEFR_LEVELS[CEFR_LEVELS.length - 1]}`,
            })}
          </p>

          <div className="space-y-2">
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder={t('searchPlaceholder')}
              className="border-fl-border bg-fl-surface-2 text-fl-fg placeholder:text-fl-muted-3 focus:border-fl-fg w-full border px-3 py-2 font-mono text-xs focus:outline-none"
            />
          </div>

          <div className="space-y-2">
            <p className="text-fl-label text-fl-muted-3 font-mono tracking-widest uppercase">
              {t('level')}
            </p>
            <div className="flex flex-wrap gap-2">
              {(['All', ...CEFR_LEVELS] as const).map((lvl) => (
                <button
                  key={lvl}
                  onClick={() => setActiveLevel(lvl)}
                  className={`text-fl-label border px-3 py-1.5 font-mono tracking-widest uppercase transition-colors ${
                    activeLevel === lvl
                      ? 'border-fl-fg text-fl-fg bg-fl-surface-2'
                      : 'border-fl-border text-fl-muted-3 hover:border-fl-border-2 hover:text-fl-fg'
                  }`}
                >
                  {lvl === 'All' ? tCommon('all') : lvl}
                </button>
              ))}
            </div>
          </div>

          <div className="space-y-2">
            <p className="text-fl-label text-fl-muted-3 font-mono tracking-widest uppercase">
              {t('register')}
            </p>
            <div className="flex flex-wrap gap-2">
              {(['All', ...REGISTERS] as const).map((reg) => (
                <button
                  key={reg}
                  onClick={() => setActiveRegister(reg)}
                  className={`text-fl-label border px-3 py-1.5 font-mono tracking-widest uppercase transition-colors ${
                    activeRegister === reg
                      ? 'border-fl-fg text-fl-fg bg-fl-surface-2'
                      : 'border-fl-border text-fl-muted-3 hover:border-fl-border-2 hover:text-fl-fg'
                  }`}
                >
                  {reg === 'All' ? tCommon('all') : t(reg)}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {hasActiveFilters && (
        <p className="text-fl-label text-fl-muted-3 font-mono">
          {t('situationsShown', { count: filteredCategories.length })}
        </p>
      )}

      {CEFR_LEVELS.map((level) => {
        const cats = filteredCategories.filter((c) => c.level === level)
        if (!cats.length) return null
        return (
          <section key={level} className="space-y-3">
            <div className="flex items-center gap-3">
              <span className="text-fl-fg font-mono text-base font-bold tracking-widest">
                {level}
              </span>
              <div className="bg-fl-border h-px flex-1" />
            </div>
            <div className="grid gap-4 md:grid-cols-2">
              {cats.map((cat) => (
                <CategoryCard
                  key={cat.id}
                  cat={cat}
                  registerFilter={activeRegister}
                  search={search}
                  language={activeLanguage?.code ?? 'en-GB'}
                />
              ))}
            </div>
          </section>
        )
      })}

      {filteredCategories.length === 0 && (
        <div className="border-fl-border bg-fl-surface space-y-4 border px-6 py-10 text-center">
          <p className="text-fl-muted-3 font-mono text-xs tracking-widest uppercase">
            {t('noResults')}
          </p>
          {hasActiveFilters && (
            <button
              onClick={() => {
                setActiveLevel('All')
                setActiveRegister('All')
                setSearch('')
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
