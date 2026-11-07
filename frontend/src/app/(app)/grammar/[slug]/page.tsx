'use client'

import { useState, useEffect, useCallback, useRef } from 'react'
import { notFound } from 'next/navigation'
import Link from 'next/link'
import { use } from 'react'
import { useTranslations } from 'next-intl'
import {
  getGrammarNativeHelp,
  getGrammarTopics,
  type GrammarNativeHelp,
  type GrammarTopic,
} from '@/data/grammar'
import { TargetLanguageText } from '@/components/TargetLanguageText'
import { useAuthStore } from '@/store/auth'
import { useAnalyticsView } from '@/hooks/useAnalyticsView'
import { useLanguageStore, waitForLanguageSwitch } from '@/store/language'
import { PageLoading } from '@/components/ui/page-loading'

function renderExplanation(text: string) {
  const lines = text.split('\n')
  return lines.map((line, i) => {
    if (line.startsWith('- ')) {
      return (
        <li
          key={i}
          className="text-fl-muted-1 font-sans text-base leading-relaxed"
        >
          <span className="text-fl-muted-3 mr-2">{'\u00b7'}</span>
          <RichText text={line.slice(2)} />
        </li>
      )
    }
    if (line.trim() === '') return null
    if (line.startsWith('|')) {
      return (
        <tr key={i}>
          {line
            .split('|')
            .filter(Boolean)
            .map((cell, ci) => (
              <td
                key={ci}
                className="text-fl-label text-fl-muted-1 border-fl-border border px-3 py-1.5 font-mono"
              >
                <RichText text={cell.trim()} />
              </td>
            ))}
        </tr>
      )
    }
    return (
      <p
        key={i}
        className="text-fl-muted-1 font-sans text-base leading-relaxed"
      >
        <RichText text={line} />
      </p>
    )
  })
}

function RichText({ text }: { text: string }) {
  const parts = text.split(/(\*\*[^*]+\*\*|`[^`]+`)/)
  return (
    <>
      {parts.map((part, i) => {
        if (part.startsWith('**') && part.endsWith('**')) {
          return (
            <strong key={i} className="text-fl-fg font-bold">
              {part.slice(2, -2)}
            </strong>
          )
        }
        if (part.startsWith('`') && part.endsWith('`')) {
          return (
            <code key={i} className="bg-fl-surface-2 text-fl-fg font-code px-1">
              {part.slice(1, -1)}
            </code>
          )
        }
        return <span key={i}>{part}</span>
      })}
    </>
  )
}

export default function GrammarDetailPage({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const tCommon = useTranslations('common')
  const activeLanguage = useLanguageStore((s) => s.activeLanguage)
  const needsRefresh = useLanguageStore((s) => s.needsRefresh)
  const isSwitching = useLanguageStore((s) => s.isSwitching)
  const invalidationVersion = useLanguageStore((s) => s.invalidationVersion)
  const sessionVersion = useAuthStore((s) => s.sessionVersion)
  const nativeLanguage = useAuthStore((s) => s.user?.native_language)
  const languageCode = activeLanguage?.code
  const scope = `${sessionVersion}:${invalidationVersion}:${languageCode}:${needsRefresh}`
  const { slug } = use(params)
  const analyticsRef = useAnalyticsView(
    'grammar_viewed',
    `${languageCode}:${slug}`
  )

  const [topics, setTopics] = useState<GrammarTopic[]>([])
  const [loading, setLoading] = useState(true)
  const [loadError, setLoadError] = useState(false)
  const [loadedScope, setLoadedScope] = useState<string | null>(null)
  const [attempt, setAttempt] = useState(0)

  useEffect(() => {
    const controller = new AbortController()
    const isCurrent = () => {
      const state = useLanguageStore.getState()
      return (
        !controller.signal.aborted &&
        useAuthStore.getState().sessionVersion === sessionVersion &&
        state.invalidationVersion === invalidationVersion &&
        state.activeLanguage?.code === languageCode &&
        state.needsRefresh === needsRefresh
      )
    }
    setLoading(true)
    setLoadError(false)
    setTopics([])
    async function load() {
      try {
        if (useLanguageStore.getState().isSwitching) {
          await waitForLanguageSwitch(controller.signal)
        }
        if (!isCurrent()) return
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
    void load()
    return () => controller.abort()
  }, [
    languageCode,
    needsRefresh,
    invalidationVersion,
    sessionVersion,
    scope,
    attempt,
  ])

  if (loading || loadedScope !== scope || (loadError && isSwitching)) {
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

  const topic = topics.find((item) => item.slug === slug)
  if (!topic) notFound()

  return (
    <>
      {isSwitching && <PageLoading />}
      <div hidden={isSwitching} inert={isSwitching}>
        <GrammarTopicContent
          key={`${scope}:${slug}:${nativeLanguage}`}
          topic={topic}
          topics={topics}
          targetLanguageCode={languageCode!}
          analyticsRef={analyticsRef}
        />
      </div>
    </>
  )
}

function GrammarTopicContent({
  topic,
  topics,
  targetLanguageCode,
  analyticsRef,
}: {
  topic: GrammarTopic
  topics: GrammarTopic[]
  targetLanguageCode: string
  analyticsRef: (node: HTMLElement | null) => void
}) {
  const t = useTranslations('grammar')
  const tCommon = useTranslations('common')
  const tNav = useTranslations('nav')
  const tLang = useTranslations('languages')
  const nativeLanguage = useAuthStore((s) => s.user?.native_language)
  const isSwitching = useLanguageStore((s) => s.isSwitching)
  const nativeLanguageName = nativeLanguage ? tLang(nativeLanguage) : ''
  const [nativeHelpOpen, setNativeHelpOpen] = useState(
    topic.level === 'A1' || topic.level === 'A2'
  )
  const [nativeHelp, setNativeHelp] = useState<GrammarNativeHelp | null>(null)
  const [loadingNativeHelp, setLoadingNativeHelp] = useState(false)
  const [nativeHelpError, setNativeHelpError] = useState(false)
  const helpRequest = useRef<AbortController | null>(null)

  useEffect(
    () => () => {
      helpRequest.current?.abort()
      helpRequest.current = null
    },
    []
  )

  const generateNativeHelp = useCallback(async () => {
    if (
      !nativeLanguage ||
      helpRequest.current ||
      useLanguageStore.getState().isSwitching
    ) {
      return
    }
    const controller = new AbortController()
    helpRequest.current = controller
    const sessionVersion = useAuthStore.getState().sessionVersion
    const invalidationVersion = useLanguageStore.getState().invalidationVersion
    const isCurrent = () => {
      const auth = useAuthStore.getState()
      const context = useLanguageStore.getState()
      return (
        !controller.signal.aborted &&
        helpRequest.current === controller &&
        auth.sessionVersion === sessionVersion &&
        auth.user?.native_language === nativeLanguage &&
        context.activeLanguage?.code === targetLanguageCode &&
        context.invalidationVersion === invalidationVersion &&
        !context.needsRefresh
      )
    }
    setLoadingNativeHelp(true)
    setNativeHelpError(false)
    try {
      const help = await getGrammarNativeHelp(
        topic.slug,
        targetLanguageCode,
        controller.signal
      )
      if (!isCurrent()) return
      if (help) setNativeHelp(help)
      else setNativeHelpError(true)
    } catch {
      if (isCurrent()) setNativeHelpError(true)
    } finally {
      if (isCurrent()) {
        helpRequest.current = null
        setLoadingNativeHelp(false)
      }
    }
  }, [nativeLanguage, targetLanguageCode, topic.slug])

  useEffect(() => {
    if (
      !isSwitching &&
      nativeHelpOpen &&
      !nativeHelp &&
      !loadingNativeHelp &&
      !nativeHelpError
    ) {
      // Let StrictMode finish its setup replay before starting the POST.
      let cancelled = false
      queueMicrotask(() => {
        if (!cancelled) void generateNativeHelp()
      })
      return () => {
        cancelled = true
      }
    }
  }, [
    generateNativeHelp,
    isSwitching,
    loadingNativeHelp,
    nativeHelp,
    nativeHelpOpen,
    nativeHelpError,
  ])

  const hasTable = topic.explanation.includes('|')
  const explanationLines = topic.explanation.split('\n')
  const hasList = explanationLines.some((l) => l.startsWith('- '))

  const relatedTopics = topic.related
    .map((s) => topics.find((t) => t.slug === s))
    .filter(Boolean)

  return (
    <div ref={analyticsRef} className="mx-auto max-w-4xl space-y-4 p-6">
      <nav className="text-fl-label text-fl-muted-3 flex items-center gap-2 font-mono">
        <Link
          href="/grammar"
          className="hover:text-fl-fg tracking-widest uppercase transition-colors"
        >
          {tNav('grammar')}
        </Link>
        <span>{'\u203a'}</span>
        <span className="text-fl-muted-2 tracking-widest uppercase">
          {topic.level}
        </span>
        <span>{'\u203a'}</span>
        <span className="text-fl-fg tracking-wide">{topic.title}</span>
      </nav>

      <div className="border-fl-border bg-fl-surface border">
        <div className="border-fl-border flex items-center gap-2 border-b px-6 py-4">
          <span className="text-fl-label text-fl-muted-3">{'\u25cf'}</span>
          <span className="text-fl-label text-fl-muted-2 font-mono tracking-widest uppercase">
            {t('backToGrammar')}
          </span>
        </div>
        <div className="space-y-3 px-6 py-5">
          <div className="flex flex-wrap items-center gap-2">
            <span className="border-fl-border text-fl-label text-fl-muted-3 border px-2 py-0.5 font-mono tracking-widest uppercase">
              {topic.level}
            </span>
            <span className="border-fl-border text-fl-label text-fl-muted-3 border px-2 py-0.5 font-mono tracking-widest uppercase">
              {topic.category}
            </span>
          </div>
          <h1 className="text-fl-fg font-mono text-xl font-bold tracking-wide">
            {topic.title}
          </h1>
          <p className="text-fl-muted-1 max-w-[70ch] font-sans text-sm leading-relaxed">
            {topic.summary}
          </p>
          {topic.structure && (
            <div className="border-fl-border bg-fl-bg border px-4 py-3">
              <p className="text-fl-label text-fl-muted-3 mb-1 font-mono tracking-widest uppercase">
                {t('structure')}
              </p>
              <p className="text-fl-fg font-sans text-sm leading-relaxed">
                {topic.structure}
              </p>
            </div>
          )}
        </div>
      </div>

      <div className="border-fl-border bg-fl-surface border">
        <div className="border-fl-border flex items-center gap-2 border-b px-6 py-4">
          <span className="text-fl-label text-fl-muted-2 font-mono tracking-widest uppercase">
            {t('explanation')}
          </span>
        </div>
        <div className="space-y-2 px-6 py-5">
          {hasTable ? (
            <div className="overflow-x-auto">
              <table className="w-full border-collapse">
                <tbody>{renderExplanation(topic.explanation)}</tbody>
              </table>
            </div>
          ) : hasList ? (
            <ul className="max-w-[70ch] space-y-1">
              {renderExplanation(topic.explanation)}
            </ul>
          ) : (
            <div className="max-w-[70ch] space-y-2">
              {renderExplanation(topic.explanation)}
            </div>
          )}
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
                  <div className="space-y-2">
                    <p className="text-fl-muted-1 max-w-[70ch] text-base leading-relaxed">
                      {nativeHelp.summary}
                    </p>
                    <p className="text-fl-muted-1 max-w-[70ch] text-base leading-relaxed">
                      {nativeHelp.explanation}
                    </p>
                  </div>

                  {nativeHelp.key_points.length > 0 && (
                    <div className="space-y-2">
                      <p className="text-fl-label text-fl-muted-3 font-mono tracking-widest uppercase">
                        {tCommon('nativeHelpKeyPoints')}
                      </p>
                      <ul className="space-y-1">
                        {nativeHelp.key_points.map((point, i) => (
                          <li
                            key={i}
                            className="text-fl-muted-1 max-w-[70ch] text-sm leading-relaxed"
                          >
                            <span className="text-fl-muted-3 mr-2">·</span>
                            {point}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {nativeHelp.examples.length > 0 && (
                    <div className="border-fl-border space-y-2 border-t pt-3">
                      <p className="text-fl-label text-fl-muted-3 font-mono tracking-widest uppercase">
                        {t('examples')}
                      </p>
                      {nativeHelp.examples.map((ex, i) => (
                        <div key={i} className="space-y-0.5">
                          <TargetLanguageText
                            languageCode={targetLanguageCode}
                            className="text-fl-muted-1 text-sm italic"
                          >
                            {ex.sentence}
                          </TargetLanguageText>
                          <p className="text-fl-muted-1 text-sm leading-relaxed">
                            {ex.note}
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

      {topic.rules.length > 0 && (
        <div className="border-fl-border bg-fl-surface border">
          <div className="border-fl-border flex items-center gap-2 border-b px-6 py-4">
            <span className="text-fl-label text-fl-muted-2 font-mono tracking-widest uppercase">
              {t('keyRules')}
            </span>
          </div>
          <ul className="space-y-2 px-6 py-5">
            {topic.rules.map((rule, i) => (
              <li key={i} className="flex items-start gap-2">
                <span className="text-fl-label text-fl-muted-3 mt-0.5 shrink-0 font-mono">
                  {i + 1}.
                </span>
                <p className="text-fl-muted-1 max-w-[70ch] font-sans text-sm leading-relaxed">
                  {rule}
                </p>
              </li>
            ))}
          </ul>
        </div>
      )}

      {topic.examples.length > 0 && (
        <div className="border-fl-border bg-fl-surface border">
          <div className="border-fl-border flex items-center gap-2 border-b px-6 py-4">
            <span className="text-fl-label text-fl-muted-2 font-mono tracking-widest uppercase">
              {t('examples')}
            </span>
          </div>
          <div className="space-y-3 px-6 py-5">
            {topic.examples.map((ex, i) => (
              <div
                key={i}
                className="border-fl-border space-y-0.5 border-l-2 pl-4"
              >
                <p className="text-fl-fg font-sans text-base leading-relaxed">
                  {ex.text}
                </p>
                {ex.note && (
                  <p className="text-fl-muted-1 font-sans text-sm leading-relaxed italic">
                    {ex.note}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {topic.common_mistakes.length > 0 && (
        <div className="border-fl-border bg-fl-surface border">
          <div className="border-fl-border flex items-center gap-2 border-b px-6 py-4">
            <span className="text-fl-label text-fl-muted-2 font-mono tracking-widest uppercase">
              {t('commonMistakes')}
            </span>
          </div>
          <div className="space-y-4 px-6 py-5">
            {topic.common_mistakes.map((m, i) => (
              <div key={i} className="space-y-1.5">
                {m.wrong && (
                  <div className="flex items-start gap-2">
                    <span className="text-fl-label shrink-0 font-mono text-red-500">
                      {'\u2717'}
                    </span>
                    <p className="text-fl-muted-1 font-sans text-sm leading-relaxed line-through">
                      {m.wrong}
                    </p>
                  </div>
                )}
                {m.correct && (
                  <div className="flex items-start gap-2">
                    <span className="text-fl-label shrink-0 font-mono text-green-500">
                      {'\u2713'}
                    </span>
                    <p className="text-fl-fg font-sans text-sm leading-relaxed">
                      {m.correct}
                    </p>
                  </div>
                )}
                {m.note && (
                  <p className="text-fl-muted-1 max-w-[70ch] pl-5 font-sans text-sm leading-relaxed">
                    {m.note}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {relatedTopics.length > 0 && (
        <div className="border-fl-border bg-fl-surface border">
          <div className="border-fl-border flex items-center gap-2 border-b px-6 py-4">
            <span className="text-fl-label text-fl-muted-2 font-mono tracking-widest uppercase">
              {t('relatedTopics')}
            </span>
          </div>
          <div className="flex flex-wrap gap-2 px-6 py-5">
            {relatedTopics.map(
              (rt) =>
                rt && (
                  <Link
                    key={rt.slug}
                    href={`/grammar/${rt.slug}`}
                    className="border-fl-border text-fl-label text-fl-muted-2 hover:border-fl-border-2 hover:text-fl-fg border px-3 py-2 font-mono tracking-widest uppercase transition-colors"
                  >
                    {'\u25cf'} {rt.title}
                    <span className="text-fl-muted-4 ml-2">{rt.level}</span>
                  </Link>
                )
            )}
          </div>
        </div>
      )}

      <Link
        href="/grammar"
        className="text-fl-label text-fl-muted-2 hover:text-fl-fg inline-block font-mono tracking-widest uppercase transition-colors"
      >
        {'\u2190'} {t('backLink')}
      </Link>
    </div>
  )
}
