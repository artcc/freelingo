'use client'

import { useState, useEffect, useRef, use, useCallback } from 'react'
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
  const tLang = useTranslations('languages')
  const tFlashcards = useTranslations('flashcards')
  const activeLanguage = useLanguageStore((s) => s.activeLanguage)
  const isSwitching = useLanguageStore((s) => s.isSwitching)
  const needsRefresh = useLanguageStore((s) => s.needsRefresh)
  const invalidationVersion = useLanguageStore((s) => s.invalidationVersion)
  const sessionVersion = useAuthStore((s) => s.sessionVersion)
  const user = useAuthStore((s) => s.user)
  const [loadedSet, setLoadedSet] = useState<{
    set: VocabularySet
    language: string
    studyPlanId: number | null
  } | null>(null)
  const vocabSet = loadedSet?.set ?? null
  const [loading, setLoading] = useState(true)
  const [loadError, setLoadError] = useState(false)
  const [reload, setReload] = useState(0)
  const viewVersion = useRef(0)
  const addRequest = useRef<symbol | null>(null)
  const [adding, setAdding] = useState(false)
  const [addedCount, setAddedCount] = useState<number | null>(null)
  const [error, setError] = useState('')
  const [nativeHelpOpen, setNativeHelpOpen] = useState(false)
  const [nativeHelp, setNativeHelp] = useState<VocabularyNativeHelp | null>(
    null
  )
  const [loadingNativeHelp, setLoadingNativeHelp] = useState(false)
  const nativeHelpRequest = useRef<AbortController | null>(null)
  const [nativeHelpError, setNativeHelpError] = useState(false)
  const nativeLanguageName = user?.native_language
    ? tLang(user.native_language)
    : ''

  const acceptsContext = useCallback(() => {
    const state = useLanguageStore.getState()
    return (
      useAuthStore.getState().sessionVersion === sessionVersion &&
      state.activeLanguage?.code === activeLanguage?.code &&
      state.invalidationVersion === invalidationVersion &&
      !state.isSwitching &&
      !state.needsRefresh
    )
  }, [activeLanguage?.code, invalidationVersion, sessionVersion])

  useEffect(() => {
    const controller = new AbortController()
    const version = ++viewVersion.current
    const cleanup = () => {
      controller.abort()
      if (viewVersion.current === version) ++viewVersion.current
    }
    setLoading(true)
    setLoadError(false)
    setAddedCount(null)
    setAdding(false)
    addRequest.current = null
    if (isSwitching) return cleanup
    if (!activeLanguage || needsRefresh) {
      void useLanguageStore
        .getState()
        .fetchLanguages(controller.signal)
        .then((ok) => {
          if (
            (!ok || !useLanguageStore.getState().activeLanguage) &&
            !controller.signal.aborted
          ) {
            setLoadError(true)
            setLoading(false)
          }
        })
      return cleanup
    }
    const language = activeLanguage.code
    const current = () =>
      !controller.signal.aborted &&
      version === viewVersion.current &&
      acceptsContext()
    void (async () => {
      try {
        const [setResponse, planResponse] = await Promise.all([
          apiFetch(
            `/api/vocabulary/${encodeURIComponent(setId)}?language=${encodeURIComponent(language)}`,
            { signal: controller.signal }
          ),
          apiFetch('/api/study-plan/current', { signal: controller.signal }),
        ])
        if (setResponse.status === 404) {
          if (current()) setLoadedSet(null)
          return
        }
        if (!setResponse.ok || !planResponse.ok)
          throw new Error('Could not load vocabulary context')
        const [data, plan] = await Promise.all([
          setResponse.json() as Promise<{ set: VocabularySet }>,
          planResponse.json() as Promise<{
            id: number
            target_language: string
          } | null>,
        ])
        if (!current()) return
        if (plan && plan.target_language !== language) {
          setError(tFlashcards('contextChanged'))
          throw new Error('Vocabulary context changed')
        }
        setLoadedSet({ set: data.set, language, studyPlanId: plan?.id ?? null })
      } catch {
        if (current()) setLoadError(true)
      } finally {
        if (current()) setLoading(false)
      }
    })()
    return cleanup
  }, [
    setId,
    activeLanguage,
    isSwitching,
    needsRefresh,
    invalidationVersion,
    sessionVersion,
    reload,
    acceptsContext,
    tFlashcards,
  ])

  async function refreshContext() {
    const previousContext = useLanguageStore.getState()
    setLoading(true)
    const ok = await useLanguageStore.getState().fetchLanguages()
    if (useAuthStore.getState().sessionVersion !== sessionVersion) return
    if (!ok) {
      setLoadError(true)
      setLoading(false)
      return
    }
    const context = useLanguageStore.getState()
    // Changed store dependencies already reload the view; only force unchanged context.
    if (
      context.activeLanguage === previousContext.activeLanguage &&
      context.isSwitching === previousContext.isSwitching &&
      context.needsRefresh === previousContext.needsRefresh &&
      context.invalidationVersion === previousContext.invalidationVersion
    )
      setReload((value) => value + 1)
  }

  useEffect(() => {
    setNativeHelpOpen(false)
    setNativeHelp(null)
    setNativeHelpError(false)
    setLoadingNativeHelp(false)
    return () => {
      nativeHelpRequest.current?.abort()
      nativeHelpRequest.current = null
    }
  }, [
    setId,
    activeLanguage,
    sessionVersion,
    invalidationVersion,
    isSwitching,
    needsRefresh,
    reload,
    tFlashcards,
    user?.native_language,
  ])

  const targetLanguageCode = activeLanguage?.code ?? 'en-GB'

  const generateNativeHelp = useCallback(async () => {
    if (
      nativeHelpRequest.current ||
      loading ||
      !acceptsContext() ||
      loadedSet?.language !== targetLanguageCode ||
      loadedSet.set.id !== setId
    )
      return
    const controller = new AbortController()
    nativeHelpRequest.current = controller
    const version = viewVersion.current
    const nativeLanguage = user?.native_language
    const current = () =>
      !controller.signal.aborted &&
      nativeHelpRequest.current === controller &&
      version === viewVersion.current &&
      acceptsContext() &&
      useAuthStore.getState().user?.native_language === nativeLanguage
    setLoadingNativeHelp(true)
    setNativeHelpError(false)
    try {
      const res = await apiFetch(
        `/api/vocabulary/${encodeURIComponent(setId)}/native-help?language=${targetLanguageCode}`,
        { method: 'POST', signal: controller.signal }
      )
      if (!res.ok) throw new Error('native help failed')
      const data = (await res.json()) as { native_help: VocabularyNativeHelp }
      if (current()) setNativeHelp(data.native_help)
    } catch {
      if (current()) setNativeHelpError(true)
    } finally {
      if (current()) setLoadingNativeHelp(false)
      if (nativeHelpRequest.current === controller)
        nativeHelpRequest.current = null
    }
  }, [
    loading,
    acceptsContext,
    loadedSet,
    setId,
    targetLanguageCode,
    user?.native_language,
  ])

  if (loading) {
    return <PageLoading />
  }

  if (loadError)
    return (
      <div className="mx-auto max-w-4xl space-y-4 p-6">
        <p role="alert" className="text-fl-error-fg">
          {error || tCommon('errorMessage')}
        </p>
        <button
          onClick={() => void refreshContext()}
          className="border-fl-border border px-4 py-2"
        >
          {tCommon('retry')}
        </button>
      </div>
    )

  if (!vocabSet) notFound()

  async function handleAddAll() {
    if (
      !vocabSet ||
      !loadedSet ||
      addRequest.current ||
      !acceptsContext() ||
      loadedSet.language !== activeLanguage?.code ||
      vocabSet.id !== setId
    )
      return
    if (loadedSet.studyPlanId === null) {
      setError(tCommon('noActivePlan'))
      return
    }
    const version = viewVersion.current
    const token = Symbol('add-vocabulary')
    addRequest.current = token
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
        body: JSON.stringify({
          flashcards: cards,
          study_plan_id: loadedSet.studyPlanId,
          target_language: loadedSet.language,
        }),
      })
      if (!acceptsContext() || version !== viewVersion.current) return
      if (!res.ok) {
        const d = await res.json().catch(() => ({}))
        if (!acceptsContext() || version !== viewVersion.current) return
        if (res.status === 409 && d.detail === 'flashcard_context_changed') {
          setError(tFlashcards('contextChanged'))
          await refreshContext()
          return
        }
        throw new Error(
          (d as { detail?: string }).detail === 'No active study plan found'
            ? 'No active study plan found'
            : t('addFailed')
        )
      }
      const data = (await res.json()) as { created: number }
      if (acceptsContext() && version === viewVersion.current)
        setAddedCount(data.created)
    } catch (err) {
      if (!acceptsContext() || version !== viewVersion.current) return
      const msg = err instanceof Error ? err.message : ''
      setError(
        msg === 'No active study plan found'
          ? tCommon('noActivePlan')
          : t('addFailed')
      )
    } finally {
      if (addRequest.current === token) {
        addRequest.current = null
        if (acceptsContext() && version === viewVersion.current)
          setAdding(false)
      }
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
                className="bg-fl-accent text-fl-accent-fg hover:bg-fl-accent/90 px-5 py-2.5 font-mono text-sm font-bold tracking-widest uppercase transition-colors disabled:opacity-40"
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
