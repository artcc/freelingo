'use client'

import { useEffect, useRef, useState } from 'react'
import { useParams } from 'next/navigation'
import Link from 'next/link'
import { useTranslations } from 'next-intl'
import { TargetLanguageText } from '@/components/TargetLanguageText'
import { AudioPlayer } from '@/components/ui/AudioPlayer'
import { ConfirmDialog } from '@/components/ui/confirm-dialog'
import { gameRequest, GameRequestError } from '@/lib/detective'
import type { VocabularyPairsSession } from '@/lib/vocabulary-pairs'
import { useLanguageStore } from '@/store/language'
import { useFreemiumStore } from '@/store/freemium'

const button =
  'border-fl-border hover:border-fl-border-2 text-fl-fg border px-4 py-2 text-sm disabled:opacity-40'

export default function VocabularyPairsSessionPage() {
  const { id } = useParams<{ id: string }>()
  const t = useTranslations('vocabularyPairs')
  const shared = useTranslations('detective')
  const common = useTranslations('common')
  const tTarget = useTranslations('targetLanguages')
  const [session, setSession] = useState<VocabularyPairsSession | null>(null)
  const [term, setTerm] = useState<number | null>(null)
  const [meaning, setMeaning] = useState<number | null>(null)
  const [error, setError] = useState(false)
  const [busy, setBusy] = useState(false)
  const [retry, setRetry] = useState(0)
  const [abandon, setAbandon] = useState(false)
  const mutation = useRef<AbortController | null>(null)
  const busyRef = useRef(false)

  useEffect(() => {
    const controller = new AbortController()
    let timer: ReturnType<typeof setTimeout>
    let failures = 0
    let end = Infinity
    setSession(null)
    setError(false)
    setBusy(false)
    setAbandon(false)
    setTerm(null)
    setMeaning(null)
    async function load() {
      try {
        const data = await gameRequest<VocabularyPairsSession>(
          `/sessions/${id}`,
          { signal: controller.signal }
        )
        if (controller.signal.aborted) return
        if (data.game_type !== 'vocabulary-pairs') {
          setError(true)
          return
        }
        setSession(data)
        failures = 0
        if (data.status === 'generating') {
          if (end === Infinity)
            end =
              performance.now() + (data.remaining_seconds ?? 600) * 1000 + 10000
          if (performance.now() >= end) {
            setError(true)
            return
          }
          timer = setTimeout(() => void load(), 5000)
        } else void useFreemiumStore.getState().fetchStatus(true)
      } catch (e) {
        if (controller.signal.aborted) return
        failures += 1
        const delay = Math.max(
          5000 * failures,
          e instanceof GameRequestError ? e.retryAfter * 1000 : 0
        )
        if (failures < 4 && delay <= 120000 && performance.now() + delay < end)
          timer = setTimeout(() => void load(), delay)
        else setError(true)
      }
    }
    void load()
    return () => {
      controller.abort()
      clearTimeout(timer)
      mutation.current?.abort()
      busyRef.current = false
    }
  }, [id, retry])

  const tried =
    session?.attempts.some(
      (a) => a.challenge === term && a.choice === meaning
    ) ?? false

  async function submit(action: 'answer' | 'abandon') {
    if (!session || busyRef.current || error) return
    if (action === 'answer' && (term === null || meaning === null || tried))
      return
    busyRef.current = true
    setBusy(true)
    const controller = new AbortController()
    mutation.current = controller
    try {
      const data = await gameRequest<VocabularyPairsSession>(
        `/sessions/${id}/${action}`,
        {
          method: 'POST',
          signal: controller.signal,
          body:
            action === 'abandon'
              ? undefined
              : JSON.stringify({
                  step: 'match',
                  attempt: session.attempts.length,
                  challenge: term,
                  choice: meaning,
                }),
        }
      )
      if (controller.signal.aborted) return
      setSession(data)
      setTerm(null)
      setMeaning(null)
      setAbandon(false)
      if (action === 'answer') useLanguageStore.getState().invalidateLanguages()
    } catch {
      if (!controller.signal.aborted) {
        setError(true)
        setAbandon(false)
      }
    } finally {
      if (!controller.signal.aborted) {
        busyRef.current = false
        setBusy(false)
      }
    }
  }

  const matched = session?.challenges.filter((c) => c.matched) ?? []
  const last = session?.attempts.at(-1)
  return (
    <div className="mx-auto max-w-4xl space-y-6 p-6 font-sans">
      <Link href="/games/vocabulary-pairs" className="text-fl-muted-2 text-sm">
        ← {common('back')}
      </Link>
      <header className="border-fl-border bg-fl-surface space-y-2 border p-6">
        <h1 className="text-fl-fg text-lg font-semibold">{t('title')}</h1>
        {session && (
          <p className="text-fl-muted-2 text-sm">
            {tTarget(session.target_language)} · {session.level} ·{' '}
            {shared(session.mode)}
          </p>
        )}
      </header>
      {error && (
        <div role="alert" className="space-y-3">
          <p>{common('errorMessage')}</p>
          <button className={button} onClick={() => setRetry((n) => n + 1)}>
            {common('retry')}
          </button>
        </div>
      )}
      {!session && !error && <p role="status">{common('loading')}</p>}
      {session?.status === 'generating' && !error && (
        <p role="status">{shared('generatingDescription')}</p>
      )}
      {session?.status === 'failed' && (
        <p role="alert">{shared('failedDescription')}</p>
      )}
      {session?.status === 'ready' && (
        <section
          className="border-fl-border bg-fl-surface space-y-5 border p-6"
          aria-busy={busy}
        >
          <h2 className="font-semibold">
            {t('progress', { count: matched.length })}
          </h2>
          <p className="text-fl-muted-2 text-sm">{t('instructions')}</p>
          <div className="grid grid-cols-2 gap-3">
            <div
              role="group"
              aria-label={t('terms')}
              className="min-w-0 space-y-3"
            >
              <h3 className="text-sm font-semibold">{t('terms')}</h3>
              {session.challenges.map((c) => (
                <button
                  key={c.index}
                  className={`${button} w-full break-words ${term === c.index ? 'bg-fl-surface-2 border-fl-border-2' : ''}`}
                  aria-pressed={term === c.index}
                  disabled={busy || error || c.matched}
                  onClick={() => setTerm(term === c.index ? null : c.index)}
                >
                  <TargetLanguageText
                    languageCode={session.target_language}
                    className="text-lg"
                  >
                    {c.term}
                  </TargetLanguageText>{' '}
                  {c.matched && (
                    <span className="block text-xs">{t('matched')}</span>
                  )}
                </button>
              ))}
            </div>
            <div
              role="group"
              aria-label={t('meanings')}
              className="min-w-0 space-y-3"
            >
              <h3 className="text-sm font-semibold">{t('meanings')}</h3>
              {session.meanings.map((m) => {
                const solved = matched.some((c) => c.choice === m.index)
                return (
                  <button
                    key={m.index}
                    className={`${button} w-full break-words ${meaning === m.index ? 'bg-fl-surface-2 border-fl-border-2' : ''}`}
                    aria-pressed={meaning === m.index}
                    disabled={busy || error || solved}
                    onClick={() =>
                      setMeaning(meaning === m.index ? null : m.index)
                    }
                  >
                    <span lang={session.native_language}>{m.text}</span>{' '}
                    {solved && (
                      <span className="block text-xs">{t('matched')}</span>
                    )}
                  </button>
                )
              })}
            </div>
          </div>
          <button
            className={button}
            disabled={
              busy || error || term === null || meaning === null || tried
            }
            onClick={() => void submit('answer')}
          >
            {t('check')}
          </button>
          <div role="status" className="text-sm">
            {tried
              ? t('alreadyTried')
              : last && (
                  <>
                    {t(last.correct ? 'matchCorrect' : 'matchIncorrect')}{' '}
                    <TargetLanguageText languageCode={session.target_language}>
                      {session.challenges[last.challenge].term}
                    </TargetLanguageText>
                    {' — '}
                    <span lang={session.native_language}>
                      {
                        session.meanings.find((m) => m.index === last.choice)
                          ?.text
                      }
                    </span>
                  </>
                )}
          </div>
          <p className="text-fl-muted-2 text-xs">{shared('saved')}</p>
          <button
            className={button}
            disabled={busy || error}
            onClick={() => setAbandon(true)}
          >
            {shared('abandon')}
          </button>
        </section>
      )}
      {session &&
        ['ready', 'completed', 'abandoned'].includes(session.status) && (
          <section className="space-y-4">
            <h2 className="font-semibold">
              {session.status === 'ready'
                ? t('matched')
                : shared(session.status)}
            </h2>
            {session.status === 'completed' && (
              <p>
                {t('results', {
                  correct: matched.filter((c) => !c.assisted).length,
                  xp: session.xp_earned,
                })}
              </p>
            )}
            {matched.map((c) => (
              <div
                key={c.index}
                className="border-fl-border bg-fl-surface space-y-3 border p-5"
              >
                <div className="flex flex-wrap items-center gap-3">
                  <TargetLanguageText
                    languageCode={session.target_language}
                    className="text-lg"
                  >
                    {c.term}
                  </TargetLanguageText>
                  <AudioPlayer text={c.term} size="sm" />
                  <span lang={session.native_language}>
                    {session.meanings.find((m) => m.index === c.choice)?.text}
                  </span>
                </div>
                <p className="text-fl-muted-2 text-xs">
                  {t(c.assisted ? 'withHelp' : 'firstTry')}
                </p>
                {c.sentence && (
                  <div className="space-y-2">
                    <TargetLanguageText
                      as="p"
                      languageCode={session.target_language}
                      className="text-lg"
                    >
                      {c.sentence}
                    </TargetLanguageText>
                    <p
                      lang={session.native_language}
                      className="text-fl-muted-2 text-sm"
                    >
                      {c.translation}
                    </p>
                  </div>
                )}
              </div>
            ))}
            <p className="text-fl-muted-2 text-sm">{t('xpRules')}</p>
            {session.status !== 'ready' && (
              <div className="flex flex-wrap gap-3">
                <Link className={button} href="/games/vocabulary-pairs">
                  {shared('playAgain')}
                </Link>
                <Link className={button} href="/plan">
                  {shared('plan')}
                </Link>
              </div>
            )}
          </section>
        )}
      <ConfirmDialog
        open={abandon}
        title={shared('abandon')}
        message={shared('abandonDescription')}
        confirmLabel={shared('abandon')}
        cancelLabel={common('cancel')}
        confirming={busy}
        onConfirm={() => void submit('abandon')}
        onCancel={() => setAbandon(false)}
      />
    </div>
  )
}
