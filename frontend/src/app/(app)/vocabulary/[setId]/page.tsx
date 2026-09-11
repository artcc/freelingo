'use client'

import { useState, useEffect, use, useCallback } from 'react'
import { notFound, useRouter } from 'next/navigation'
import Link from 'next/link'
import { useTranslations } from 'next-intl'
import { PageLoading } from '@/components/ui/page-loading'
import type { VocabularyNativeHelp, VocabularySet } from '@/data/types'
import { useLanguageStore } from '@/store/language'
import { useAuthStore } from '@/store/auth'
import { apiFetch } from '@/lib/api'
import { TargetLanguageText } from '@/components/TargetLanguageText'

const POS_LABELS: Record<string, string> = {
  noun: 'n.',
  verb: 'v.',
  adjective: 'adj.',
  adverb: 'adv.',
  phrase: 'phr.',
  conjunction: 'conj.',
  preposition: 'prep.',
  numeral: 'num.',
  pronoun: 'pron.',
}

export default function VocabularySetPage({
  params,
}: {
  params: Promise<{ setId: string }>
}) {
  const { setId } = use(params)
  const router = useRouter()
  const t = useTranslations('vocabulary')
  const tCommon = useTranslations('common')
  const tTargetLang = useTranslations('targetLanguages')
  const activeLanguage = useLanguageStore((s) => s.activeLanguage)
  const user = useAuthStore((s) => s.user)
  const [vocabSet, setVocabSet] = useState<VocabularySet | null>(null)
  const [loading, setLoading] = useState(true)
  const [adding, setAdding] = useState(false)
  const [addedCount, setAddedCount] = useState<number | null>(null)
  const [error, setError] = useState('')
  const [nativeHelpOpen, setNativeHelpOpen] = useState(false)
  const [nativeHelp, setNativeHelp] = useState<VocabularyNativeHelp | null>(
    null
  )
  const [loadingNativeHelp, setLoadingNativeHelp] = useState(false)
  const [nativeHelpError, setNativeHelpError] = useState(false)
  const nativeLanguageName = user?.native_language
    ? tTargetLang(user.native_language)
    : ''

  useEffect(() => {
    const lang = activeLanguage?.code ?? 'en-GB'
    setLoading(true)
    apiFetch(`/api/vocabulary/${encodeURIComponent(setId)}?language=${lang}`)
      .then((r) => {
        if (!r.ok) throw new Error('not found')
        return r.json()
      })
      .then((d: { set: VocabularySet }) => setVocabSet(d.set))
      .catch(() => setVocabSet(null))
      .finally(() => setLoading(false))
  }, [setId, activeLanguage?.code])

  useEffect(() => {
    setNativeHelpOpen(false)
    setNativeHelp(null)
    setNativeHelpError(false)
  }, [setId, activeLanguage?.code])

  const targetLanguageCode = activeLanguage?.code ?? 'en-GB'

  const generateNativeHelp = useCallback(async () => {
    if (loadingNativeHelp) return
    setLoadingNativeHelp(true)
    setNativeHelpError(false)
    try {
      const res = await apiFetch(
        `/api/vocabulary/${encodeURIComponent(setId)}/native-help?language=${targetLanguageCode}`,
        { method: 'POST' }
      )
      if (!res.ok) throw new Error('native help failed')
      const data = (await res.json()) as { native_help: VocabularyNativeHelp }
      setNativeHelp(data.native_help)
    } catch {
      setNativeHelpError(true)
    } finally {
      setLoadingNativeHelp(false)
    }
  }, [loadingNativeHelp, setId, targetLanguageCode])

  if (loading) {
    return <PageLoading />
  }

  if (!vocabSet) notFound()

  async function handleAddAll() {
    if (!vocabSet) return
    setAdding(true)
    setError('')
    try {
      const cards = vocabSet.words.map((w) => ({
        word: w.word,
        definition: w.definition,
        example_sentence: w.example,
        translation: '', // user's native language translation will be added by LLM generation
      }))
      const res = await apiFetch('/api/flashcards/bulk', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ flashcards: cards }),
      })
      if (!res.ok) {
        const d = await res.json().catch(() => ({}))
        throw new Error(
          (d as { detail?: string }).detail ?? `Error ${res.status}`
        )
      }
      const data = (await res.json()) as { created: number }
      setAddedCount(data.created)
    } catch (err) {
      const msg = err instanceof Error ? err.message : ''
      setError(
        msg === 'No active study plan found'
          ? tCommon('noActivePlan')
          : msg || 'Failed to add flashcards.'
      )
    } finally {
      setAdding(false)
    }
  }

  return (
    <div className="mx-auto max-w-4xl space-y-4 p-6">
      {/* Breadcrumb */}
      <nav className="text-fl-label text-fl-muted-3 flex items-center gap-2 font-mono">
        <Link
          href="/vocabulary"
          className="hover:text-fl-fg tracking-widest uppercase transition-colors"
        >
          {t('title')}
        </Link>
        <span>›</span>
        <span className="text-fl-muted-2 tracking-widest uppercase">
          {vocabSet.level}
        </span>
        <span>›</span>
        <span className="text-fl-fg tracking-wide">{vocabSet.topic}</span>
      </nav>

      {/* Header */}
      <div className="border-fl-border bg-fl-surface border">
        <div className="border-fl-border flex items-center gap-2 border-b px-6 py-4">
          <span className="text-fl-label text-fl-muted-3">●</span>
          <span className="text-fl-label text-fl-muted-2 font-mono tracking-widest uppercase">
            {t('vocabularySet')}
          </span>
        </div>
        <div className="space-y-3 px-6 py-5">
          <div className="flex flex-wrap items-center gap-2">
            <span className="border-fl-border text-fl-label text-fl-muted-3 border px-2 py-0.5 font-mono tracking-widest uppercase">
              {vocabSet.level}
            </span>
            <span className="border-fl-border text-fl-label text-fl-muted-3 border px-2 py-0.5 font-mono tracking-widest uppercase">
              {vocabSet.unit_ref}
            </span>
          </div>
          <h1 className="text-fl-fg font-mono text-xl font-bold tracking-wide">
            {vocabSet.topic}
          </h1>
          <p className="text-fl-label text-fl-muted-3 font-mono">
            {vocabSet.words.length} {t('words')}
          </p>

          {/* Add to flashcards */}
          {addedCount !== null ? (
            <div className="border border-green-500 px-4 py-2">
              <p className="font-mono text-xs text-green-600 dark:text-green-400">
                ✓ {t('cardsAdded', { count: addedCount })}{' '}
                <button
                  onClick={() => router.push('/flashcards')}
                  className="underline hover:no-underline"
                >
                  {t('goToFlashcards')}
                </button>
              </p>
            </div>
          ) : (
            <div className="flex items-center gap-3">
              <button
                onClick={handleAddAll}
                disabled={adding}
                className="bg-fl-accent text-fl-accent-fg hover:bg-fl-accent/90 px-5 py-2.5 font-mono text-xs font-bold tracking-widest uppercase transition-colors disabled:opacity-40"
              >
                {adding ? '...' : t('addAll', { count: vocabSet.words.length })}
              </button>
            </div>
          )}
          {error && <p className="font-mono text-xs text-red-500">{error}</p>}
        </div>
      </div>

      {nativeLanguageName && (
        <div className="border-fl-border bg-fl-surface border">
          <button
            type="button"
            onClick={() => setNativeHelpOpen((open) => !open)}
            className="border-fl-border text-fl-label text-fl-muted-2 hover:text-fl-fg flex w-full items-center justify-between border-b px-6 py-4 font-mono tracking-widest uppercase transition-colors"
            aria-expanded={nativeHelpOpen}
          >
            <span>
              {tCommon('nativeHelpTitle', { language: nativeLanguageName })}
            </span>
            <span>{nativeHelpOpen ? '−' : '+'}</span>
          </button>
          {nativeHelpOpen && (
            <div className="space-y-4 px-6 py-5">
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

                  {nativeHelp.study_tips.length > 0 && (
                    <div className="space-y-2">
                      <p className="text-fl-label text-fl-muted-3 font-mono tracking-widest uppercase">
                        {tCommon('nativeHelpStudyTips')}
                      </p>
                      <ul className="space-y-1">
                        {nativeHelp.study_tips.map((tip, i) => (
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

                  {nativeHelp.word_notes.length > 0 && (
                    <div className="border-fl-border space-y-2 border-t pt-3">
                      <p className="text-fl-label text-fl-muted-3 font-mono tracking-widest uppercase">
                        {tCommon('nativeHelpWordNotes')}
                      </p>
                      {nativeHelp.word_notes.map((item, i) => (
                        <div key={i} className="space-y-0.5">
                          <TargetLanguageText
                            languageCode={targetLanguageCode}
                            className="text-fl-muted-1 text-sm font-bold"
                          >
                            {item.word}
                          </TargetLanguageText>
                          <p className="text-fl-muted-2 text-sm">
                            {item.meaning}
                          </p>
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
                            languageCode={targetLanguageCode}
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

                  {nativeHelp.practice_prompts.length > 0 && (
                    <div className="border-fl-border space-y-2 border-t pt-3">
                      <p className="text-fl-label text-fl-muted-3 font-mono tracking-widest uppercase">
                        {tCommon('nativeHelpPractice')}
                      </p>
                      <ul className="space-y-1">
                        {nativeHelp.practice_prompts.map((prompt, i) => (
                          <li
                            key={i}
                            className="text-fl-muted-1 max-w-[70ch] text-sm leading-relaxed"
                          >
                            <span className="text-fl-muted-3 mr-2">·</span>
                            {prompt}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </>
              ) : (
                <div className="text-center">
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
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* Word list */}
      <div className="border-fl-border bg-fl-surface divide-fl-border divide-y border">
        {vocabSet.words.map((word, i) => (
          <div key={i} className="space-y-1.5 px-5 py-4">
            <div className="flex items-baseline gap-3">
              <TargetLanguageText
                languageCode={targetLanguageCode}
                className="text-fl-fg font-bold"
              >
                {word.word}
              </TargetLanguageText>
              <span className="text-fl-label text-fl-muted-3 font-mono italic">
                {POS_LABELS[word.pos] ?? word.pos}
              </span>
              {word.ipa && (
                <span className="text-fl-muted-1 font-sans text-sm">
                  {word.ipa}
                </span>
              )}
              {word.frequency_rank && (
                <span className="text-fl-label text-fl-muted-4 ml-auto font-mono">
                  #{word.frequency_rank}
                </span>
              )}
            </div>
            <TargetLanguageText
              as="p"
              languageCode={targetLanguageCode}
              className="text-fl-muted-1"
            >
              {word.definition}
            </TargetLanguageText>
            <TargetLanguageText
              as="p"
              languageCode={targetLanguageCode}
              className="text-fl-muted-1 italic"
            >
              &ldquo;{word.example}&rdquo;
            </TargetLanguageText>
          </div>
        ))}
      </div>

      <Link
        href="/vocabulary"
        className="text-fl-label text-fl-muted-2 hover:text-fl-fg inline-block font-mono tracking-widest uppercase transition-colors"
      >
        ← {t('backToVocabulary')}
      </Link>
    </div>
  )
}
