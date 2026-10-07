'use client'

import { useEffect, useRef, useState } from 'react'
import { useParams } from 'next/navigation'
import Link from 'next/link'
import { useTranslations } from 'next-intl'
import { TargetLanguageText } from '@/components/TargetLanguageText'
import { AudioPlayer } from '@/components/ui/AudioPlayer'
import { ConfirmDialog } from '@/components/ui/confirm-dialog'
import {
  gameRequest,
  GameRequestError,
  type DetectiveSession,
  type Challenge,
} from '@/lib/detective'
import { useLanguageStore } from '@/store/language'
import { useFreemiumStore } from '@/store/freemium'

const button =
  'border-fl-border hover:border-fl-border-2 text-fl-fg border px-4 py-2 text-sm disabled:opacity-40'

export default function DetectiveSessionPage() {
  const { id } = useParams<{ id: string }>()
  const t = useTranslations('detective')
  const common = useTranslations('common')
  const tTarget = useTranslations('targetLanguages')
  const [session, setSession] = useState<DetectiveSession | null>(null)
  const [index, setIndex] = useState(0)
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
    async function load() {
      try {
        const data = await gameRequest<DetectiveSession>(`/sessions/${id}`, {
          signal: controller.signal,
        })
        if (controller.signal.aborted) return
        if (data.game_type && data.game_type !== 'detective') {
          setError(true)
          return
        }
        setSession(data)
        const next = data.challenges.findIndex((c) => c.correction === null)
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

  async function submit(step: 'detect' | 'correct' | 'abandon', choice = 0) {
    if (!session || busyRef.current || error) return
    busyRef.current = true
    setBusy(true)
    const controller = new AbortController()
    mutation.current = controller
    try {
      const data = await gameRequest<DetectiveSession>(
        `/sessions/${id}/${step === 'abandon' ? 'abandon' : 'answer'}`,
        {
          method: 'POST',
          signal: controller.signal,
          body:
            step === 'abandon'
              ? undefined
              : JSON.stringify({ challenge: index, step, choice }),
        }
      )
      if (controller.signal.aborted) return
      setSession(data)
      setAbandon(false)
      if (step !== 'abandon') useLanguageStore.getState().invalidateLanguages()
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

  function feedback(challenge: Challenge) {
    if (challenge.correction === null) return null
    return (
      <div className="space-y-3" key={challenge.index}>
        <p className="text-fl-muted-2 text-sm">
          {t('detectionResult')}:{' '}
          {t(
            challenge.detection === challenge.error_index
              ? 'correct'
              : 'incorrect'
          )}{' '}
          · {t('correctionResult')}:{' '}
          {t(
            challenge.correction === challenge.correct_index
              ? 'correct'
              : 'incorrect'
          )}
        </p>
        <div className="flex flex-wrap items-center gap-3">
          <TargetLanguageText
            languageCode={session?.target_language}
            className="text-fl-fg text-lg"
          >
            {challenge.corrected_sentence}
          </TargetLanguageText>
          {challenge.corrected_sentence && (
            <AudioPlayer
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
      <Link href="/games/error-detective" className="text-fl-muted-2 text-sm">
        ← {common('back')}
      </Link>
      <header className="border-fl-border bg-fl-surface space-y-2 border p-6">
        <h1 className="text-fl-fg text-lg font-semibold">{t('title')}</h1>
        {session && (
          <p className="text-fl-muted-2 text-sm">
            {tTarget(session.target_language)} · {session.level} ·{' '}
            {t(session.mode)}
          </p>
        )}
      </header>
      {error && (
        <div role="alert" className="space-y-3">
          <p>{common('errorMessage')}</p>
          <button
            className={button}
            onClick={() => {
              setBusy(false)
              setRetry((n) => n + 1)
            }}
          >
            {common('retry')}
          </button>
        </div>
      )}
      {!session && !error && <p role="status">{common('loading')}</p>}
      {session?.status === 'generating' && !error && (
        <p role="status" className="text-fl-muted-2">
          {t('generatingDescription')}
        </p>
      )}
      {session?.status === 'failed' && (
        <div role="alert" className="space-y-4">
          <p>{t('failedDescription')}</p>
          <Link href="/games/error-detective" className={button}>
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
            {t('challenge', { current: index + 1, total: 5 })}
          </h2>
          <p>
            {t(
              challenge.detection === null
                ? 'detect'
                : challenge.correction === null
                  ? 'chooseCorrection'
                  : 'explanation'
            )}
          </p>
          {challenge.detection === null ? (
            <div className="flex flex-wrap gap-2">
              {challenge.fragments.map((fragment, i) => (
                <button
                  key={i}
                  className={button}
                  disabled={busy || error}
                  onClick={() => void submit('detect', i)}
                >
                  <TargetLanguageText
                    languageCode={session.target_language}
                    className="text-lg whitespace-pre-wrap"
                  >
                    {fragment}
                  </TargetLanguageText>
                </button>
              ))}
            </div>
          ) : (
            <>
              <TargetLanguageText
                as="p"
                languageCode={session.target_language}
                className="text-lg leading-relaxed"
              >
                {challenge.fragments.map((fragment, i) =>
                  i === challenge.error_index ? (
                    <mark
                      key={i}
                      className="bg-fl-surface-2 text-fl-fg rounded-sm underline decoration-2 underline-offset-4"
                    >
                      {fragment}
                    </mark>
                  ) : (
                    <span key={i}>{fragment}</span>
                  )
                )}
              </TargetLanguageText>
              <p role="status" className="text-sm">
                {t('detectionResult')}:{' '}
                {t(
                  challenge.detection === challenge.error_index
                    ? 'correct'
                    : 'incorrect'
                )}
              </p>
              {challenge.correction === null && (
                <div className="grid gap-3 sm:grid-cols-3">
                  {challenge.options?.map((option, i) => (
                    <button
                      key={i}
                      className={button}
                      disabled={busy || error}
                      onClick={() => void submit('correct', i)}
                    >
                      <TargetLanguageText
                        languageCode={session.target_language}
                      >
                        {option}
                      </TargetLanguageText>
                    </button>
                  ))}
                </div>
              )}
            </>
          )}
          {challenge.correction !== null && (
            <div aria-live="polite">
              {feedback(challenge)}
              <button
                className={`${button} mt-5`}
                onClick={() => setIndex(index + 1)}
              >
                {common('next')}
              </button>
            </div>
          )}
          <p className="text-fl-muted-2 text-xs">{t('saved')}</p>
          <button
            className={button}
            disabled={busy || error}
            onClick={() => setAbandon(true)}
          >
            {t('abandon')}
          </button>
        </section>
      )}
      {session && ['completed', 'abandoned'].includes(session.status) && (
        <section className="space-y-5">
          <h2 className="font-semibold">{t(session.status)}</h2>
          {session.status === 'completed' && (
            <p>
              {t('results', {
                detected: session.challenges.filter(
                  (c) => c.detection === c.error_index
                ).length,
                corrected: session.challenges.filter(
                  (c) => c.correction === c.correct_index
                ).length,
                xp: session.xp_earned,
              })}
            </p>
          )}
          {session.challenges
            .filter((c) => c.correction !== null)
            .map((c) => (
              <div
                className="border-fl-border bg-fl-surface space-y-3 border p-5"
                key={c.index}
              >
                <TargetLanguageText
                  as="p"
                  languageCode={session.target_language}
                  className="text-fl-muted-2"
                >
                  {c.sentence}
                </TargetLanguageText>
                {feedback(c)}
              </div>
            ))}
          <p className="text-fl-muted-2 text-sm">{t('xpRules')}</p>
          <div className="flex flex-wrap gap-3">
            <Link className={button} href="/games/error-detective">
              {t('playAgain')}
            </Link>
            <Link className={button} href="/plan">
              {t('plan')}
            </Link>
          </div>
        </section>
      )}
      <ConfirmDialog
        open={abandon}
        title={t('abandon')}
        message={t('abandonDescription')}
        confirmLabel={t('abandon')}
        cancelLabel={common('cancel')}
        confirming={busy}
        onConfirm={() => void submit('abandon')}
        onCancel={() => setAbandon(false)}
      />
    </div>
  )
}
