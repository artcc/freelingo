'use client'

import { useEffect, useRef, useState } from 'react'
import { useParams } from 'next/navigation'
import Link from 'next/link'
import { useTranslations } from 'next-intl'
import { TargetLanguageText } from '@/components/TargetLanguageText'
import { AudioPlayer } from '@/components/ui/AudioPlayer'
import { ConfirmDialog } from '@/components/ui/confirm-dialog'
import { gameRequest, GameRequestError } from '@/lib/detective'
import type {
  SentenceOrderSession,
  SentenceOrderChallenge,
} from '@/lib/sentence-order'
import { useLanguageStore } from '@/store/language'
import { useFreemiumStore } from '@/store/freemium'

const button =
  'border-fl-border hover:border-fl-border-2 text-fl-fg border px-4 py-2 text-sm disabled:opacity-40'

export default function SentenceOrderSessionPage() {
  const { id } = useParams<{ id: string }>()
  const t = useTranslations('sentenceOrder')
  const shared = useTranslations('detective')
  const common = useTranslations('common')
  const tTarget = useTranslations('targetLanguages')
  const [session, setSession] = useState<SentenceOrderSession | null>(null)
  const [index, setIndex] = useState(0)
  const [order, setOrder] = useState<number[]>([])
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
    setOrder([])
    async function load() {
      try {
        const data = await gameRequest<SentenceOrderSession>(
          `/sessions/${id}`,
          {
            signal: controller.signal,
          }
        )
        if (controller.signal.aborted) return
        if (data.game_type !== 'sentence-order') {
          setError(true)
          return
        }
        setSession(data)
        const next = data.challenges.findIndex((c) => c.order === null)
        setIndex(next < 0 ? 0 : next)
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

  async function submit(action: 'answer' | 'abandon') {
    if (!session || busyRef.current || error) return
    if (
      action === 'answer' &&
      order.length !== session.challenges[index].fragments.length
    )
      return
    busyRef.current = true
    setBusy(true)
    const controller = new AbortController()
    mutation.current = controller
    try {
      const data = await gameRequest<SentenceOrderSession>(
        `/sessions/${id}/${action}`,
        {
          method: 'POST',
          signal: controller.signal,
          body:
            action === 'abandon'
              ? undefined
              : JSON.stringify({ challenge: index, step: 'order', order }),
        }
      )
      if (controller.signal.aborted) return
      setSession(data)
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

  function feedback(challenge: SentenceOrderChallenge) {
    if (challenge.order === null) return null
    return (
      <div className="space-y-3">
        <p className="text-sm">
          {shared(challenge.correct ? 'correct' : 'incorrect')}
        </p>
        {!challenge.correct && (
          <div className="space-y-2">
            <p className="text-fl-muted-2 text-sm">{t('yourSentence')}</p>
            <TargetLanguageText
              as="p"
              languageCode={session?.target_language}
              className="text-lg whitespace-pre-wrap"
            >
              {challenge.order
                .map((i) => challenge.fragments[i])
                .join(challenge.separator)}
            </TargetLanguageText>
          </div>
        )}
        <div className="flex flex-wrap items-center gap-3">
          <TargetLanguageText
            languageCode={session?.target_language}
            className="text-fl-fg text-lg whitespace-pre-wrap"
          >
            {challenge.corrected_sentence}
          </TargetLanguageText>
          {challenge.corrected_sentence && (
            <AudioPlayer
              key={challenge.index}
              text={challenge.corrected_sentence}
              studyPlanId={session?.study_plan_id}
              size="sm"
            />
          )}
        </div>
        <p
          lang={session?.native_language}
          className="text-fl-muted-2 text-sm leading-relaxed"
        >
          {challenge.explanation}
        </p>
      </div>
    )
  }

  const challenge = session?.challenges[index]
  return (
    <div className="mx-auto max-w-4xl space-y-6 p-6 font-sans">
      <Link href="/games/sentence-order" className="text-fl-muted-2 text-sm">
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
        <p role="status" className="text-fl-muted-2">
          {shared('generatingDescription')}
        </p>
      )}
      {session?.status === 'failed' && (
        <div role="alert" className="space-y-4">
          <p>{shared('failedDescription')}</p>
          <Link href="/games/sentence-order" className={button}>
            {common('back')}
          </Link>
        </div>
      )}
      {session?.status === 'ready' && challenge && (
        <section
          className="border-fl-border bg-fl-surface space-y-6 border p-6"
          aria-busy={busy}
        >
          <h2 className="font-semibold">
            {shared('challenge', { current: index + 1, total: 5 })}
          </h2>
          <p
            lang={session.native_language}
            className="text-fl-muted-2 leading-relaxed"
          >
            {challenge.clue}
          </p>
          {challenge.order === null ? (
            <>
              <p className="text-sm">{t('instructions')}</p>
              <div
                role="group"
                aria-label={t('yourSentence')}
                className="border-fl-border min-h-20 space-y-3 border p-4"
              >
                {order.length === 0 && (
                  <p className="text-fl-muted-2 text-sm">
                    {t('emptySentence')}
                  </p>
                )}
                <div className="flex flex-wrap gap-2">
                  {order.map((fragmentIndex, position) => (
                    <button
                      key={fragmentIndex}
                      className={button}
                      disabled={busy || error}
                      aria-label={t('removeFragment', {
                        fragment: challenge.fragments[fragmentIndex],
                        position: position + 1,
                      })}
                      onClick={() =>
                        setOrder((current) =>
                          current.filter((i) => i !== fragmentIndex)
                        )
                      }
                    >
                      <TargetLanguageText
                        languageCode={session.target_language}
                        className="text-lg"
                      >
                        {challenge.fragments[fragmentIndex]}
                      </TargetLanguageText>
                    </button>
                  ))}
                </div>
                <TargetLanguageText
                  as="p"
                  languageCode={session.target_language}
                  className="text-lg whitespace-pre-wrap"
                  aria-live="polite"
                >
                  {order
                    .map((i) => challenge.fragments[i])
                    .join(challenge.separator)}
                </TargetLanguageText>
              </div>
              <div
                role="group"
                aria-label={t('availableFragments')}
                className="flex flex-wrap gap-2"
              >
                {challenge.fragments.map((fragment, i) => (
                  <button
                    key={i}
                    className={button}
                    disabled={busy || error || order.includes(i)}
                    onClick={() =>
                      setOrder((current) =>
                        current.includes(i) ? current : [...current, i]
                      )
                    }
                  >
                    <TargetLanguageText
                      languageCode={session.target_language}
                      className="text-lg"
                    >
                      {fragment}
                    </TargetLanguageText>
                  </button>
                ))}
              </div>
              <button
                className={button}
                disabled={
                  busy || error || order.length !== challenge.fragments.length
                }
                onClick={() => void submit('answer')}
              >
                {t('check')}
              </button>
            </>
          ) : (
            <div aria-live="polite" className="space-y-5">
              {feedback(challenge)}
              <button
                className={button}
                disabled={busy || error}
                onClick={() => {
                  setIndex(index + 1)
                  setOrder([])
                }}
              >
                {common('next')}
              </button>
            </div>
          )}
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
      {session && ['completed', 'abandoned'].includes(session.status) && (
        <section className="space-y-5">
          <h2 className="font-semibold">{shared(session.status)}</h2>
          {session.status === 'completed' && (
            <p>
              {t('results', {
                correct: session.challenges.filter((c) => c.correct).length,
                xp: session.xp_earned,
              })}
            </p>
          )}
          {session.challenges
            .filter((c) => c.order !== null)
            .map((c) => (
              <div
                className="border-fl-border bg-fl-surface space-y-3 border p-5"
                key={c.index}
              >
                <p
                  lang={session.native_language}
                  className="text-fl-muted-2 text-sm"
                >
                  {c.clue}
                </p>
                {feedback(c)}
              </div>
            ))}
          <p className="text-fl-muted-2 text-sm">{shared('xpRules')}</p>
          <div className="flex flex-wrap gap-3">
            <Link className={button} href="/games/sentence-order">
              {shared('playAgain')}
            </Link>
            <Link className={button} href="/plan">
              {shared('plan')}
            </Link>
          </div>
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
