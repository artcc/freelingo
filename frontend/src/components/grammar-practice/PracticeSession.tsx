'use client'

import { useEffect, useRef, useState } from 'react'
import Link from 'next/link'
import { useTranslations } from 'next-intl'
import { TargetLanguageText } from '@/components/TargetLanguageText'
import { ConfirmDialog } from '@/components/ui/confirm-dialog'
import { PageLoading } from '@/components/ui/page-loading'
import { useFreemiumStore } from '@/store/freemium'
import {
  practiceRequest,
  PracticeRequestError,
  pendingPracticeKey,
  readPendingPractice,
  findPendingPractice,
  type PendingPractice,
  type PracticeSession as Session,
  type PracticeChallenge,
} from '@/lib/grammar-practice'
import {
  PracticeScope,
  practiceButton,
  practiceScope,
  canActInPractice,
  settlePractice,
} from './PracticeScope'
import { PracticeVoiceButton } from './PracticeVoiceButton'

function pause(milliseconds: number, signal: AbortSignal) {
  return new Promise<void>((resolve, reject) => {
    const abort = () => {
      clearTimeout(timer)
      reject(new DOMException('Aborted', 'AbortError'))
    }
    const timer = setTimeout(() => {
      signal.removeEventListener('abort', abort)
      resolve()
    }, milliseconds)
    signal.addEventListener('abort', abort, { once: true })
    if (signal.aborted) abort()
  })
}

export function PracticeSession({ sessionId }: { sessionId: string }) {
  return (
    <PracticeScope saved>
      <SessionContent key={sessionId} sessionId={sessionId} />
    </PracticeScope>
  )
}

function SessionContent({ sessionId }: { sessionId: string }) {
  const t = useTranslations('grammarPractice')
  const common = useTranslations('common')
  const target = useTranslations('targetLanguages')
  const [session, setSession] = useState<Session | null>(null)
  const [busy, setBusy] = useState(false)
  const [known, setKnown] = useState(false)
  const [error, setError] = useState('')
  const [retry, setRetry] = useState(0)
  const [retryAt, setRetryAt] = useState(0)
  const [clock, setClock] = useState(Date.now)
  const [abandon, setAbandon] = useState(false)
  const [missingCreation, setMissingCreation] =
    useState<PendingPractice | null>(null)
  const operation = useRef<AbortController | null>(null)
  const posting = useRef(false)
  const scope = practiceScope()

  useEffect(() => {
    if (retryAt <= Date.now()) return
    const timer = setTimeout(() => setClock(Date.now()), retryAt - Date.now())
    return () => clearTimeout(timer)
  }, [retryAt])

  useEffect(() => {
    const controller = new AbortController()
    operation.current = controller
    const current = () =>
      !controller.signal.aborted && scope === practiceScope()
    setKnown(false)
    setError('')
    setMissingCreation(null)
    setBusy(false)
    posting.current = false
    void (async () => {
      const hardDeadline = performance.now() + 300_000
      let deadline = hardDeadline
      let anchored = false
      let failures = 0
      try {
        while (current()) {
          if (!(await settlePractice(scope, controller.signal))) return
          let result: Session
          try {
            result = await practiceRequest<Session>(
              `/sessions/${encodeURIComponent(sessionId)}`,
              {
                signal: AbortSignal.any([
                  controller.signal,
                  AbortSignal.timeout(
                    Math.max(
                      1,
                      Math.ceil(Math.min(20_000, deadline - performance.now()))
                    )
                  ),
                ]),
              }
            )
            failures = 0
          } catch (e) {
            if (!(await settlePractice(scope, controller.signal))) return
            const delay =
              e instanceof PracticeRequestError && e.retryAfter
                ? e.retryAfter * 1000
                : Math.min(10_000, 1000 * 2 ** failures)
            const recoverable =
              !(e instanceof PracticeRequestError) ||
              e.status >= 500 ||
              e.status === 429 ||
              e.status === 408
            if (
              !recoverable ||
              ++failures >= 4 ||
              performance.now() + delay >= deadline ||
              delay > 120_000
            )
              throw e
            await pause(delay, controller.signal)
            continue
          }
          if (!(await settlePractice(scope, controller.signal))) return
          setSession(result)
          if (result.status !== 'generating') {
            setKnown(true)
            try {
              if (
                readPendingPractice(result.topic_id)?.payload.request_id ===
                sessionId
              ) {
                sessionStorage.removeItem(pendingPracticeKey(result.topic_id))
              }
            } catch {
              /* The URL remains the durable recovery identity. */
            }
            void useFreemiumStore.getState().fetchStatus(true)
            return
          }
          if (!anchored) {
            deadline = Math.min(
              hardDeadline,
              performance.now() +
                Math.max(0, result.remaining_seconds ?? 60) * 1000 +
                10_000
            )
            anchored = true
          }
          const remaining = deadline - performance.now()
          if (remaining <= 0) throw new Error('timeout')
          await pause(Math.min(3000, remaining), controller.signal)
          if (performance.now() >= deadline) throw new Error('timeout')
        }
      } catch (e) {
        if (!(await settlePractice(scope, controller.signal))) return
        setError(t('recoveryError'))
        if (e instanceof PracticeRequestError && e.status === 404) {
          try {
            setMissingCreation(findPendingPractice(sessionId))
          } catch {
            /* Read recovery remains available without browser storage. */
          }
        }
        if (e instanceof PracticeRequestError && e.retryAfter)
          setRetryAt(Date.now() + e.retryAfter * 1000)
      }
    })()
    return () => controller.abort()
  }, [sessionId, scope, retry, t])

  async function submit(
    path: 'answers' | 'abandon',
    answer?: { index: number; value: number | string }
  ) {
    const controller = operation.current
    if (
      !session ||
      !known ||
      busy ||
      posting.current ||
      session.status !== 'ready' ||
      !controller ||
      controller.signal.aborted ||
      !canActInPractice(scope)
    )
      return
    posting.current = true
    setBusy(true)
    setError('')
    try {
      const result = await practiceRequest<Session>(
        `/sessions/${session.id}/${path}`,
        {
          method: 'POST',
          signal: controller.signal,
          ...(answer ? { body: JSON.stringify(answer) } : {}),
        }
      )
      if (!(await settlePractice(scope, controller.signal))) return
      setSession(result)
      setAbandon(false)
    } catch (e) {
      if (!(await settlePractice(scope, controller.signal))) return
      // Never replay a mutation: an authoritative GET must establish the saved answer first.
      setKnown(false)
      setAbandon(false)
      setError(t('recoveryError'))
      if (e instanceof PracticeRequestError && e.retryAfter) {
        setRetryAt(Date.now() + e.retryAfter * 1000)
      } else setRetry((n) => n + 1)
    } finally {
      if (await settlePractice(scope, controller.signal)) {
        posting.current = false
        setBusy(false)
      }
    }
  }

  const answered =
    session?.challenges.filter(
      (challenge) => challenge.index < session.answered
    ) ?? []
  const challenge = session?.challenges.find(
    (item) => item.index === session.answered
  )
  return (
    <div className="mx-auto max-w-4xl space-y-6 px-4 py-6 font-sans md:px-8">
      <Link
        href={
          session
            ? `/grammar-practice/${session.topic_id}`
            : '/grammar-practice'
        }
        className="text-fl-muted-2 hover:text-fl-fg inline-flex text-sm transition-colors"
      >
        ← {t('back')}
      </Link>
      {error && (
        <div role="alert" className="space-y-3">
          <p className="text-fl-error-fg text-sm">{error}</p>
          <button
            className={practiceButton}
            disabled={busy || clock < retryAt}
            onClick={() => setRetry((n) => n + 1)}
          >
            {common('retry')}
          </button>
        </div>
      )}
      {missingCreation && (
        <Link
          className={practiceButton}
          href={`/grammar-practice/${missingCreation.topic_id}`}
        >
          {t('retryCreation')}
        </Link>
      )}
      {!session && !error && <PageLoading fullScreen={false} />}
      {session && (
        <>
          <header className="space-y-2">
            <h1 className="text-fl-fg text-xl font-semibold">
              <TargetLanguageText languageCode={session.target_language}>
                {session.title}
              </TargetLanguageText>
            </h1>
            <p className="text-fl-muted-2 text-sm">
              {target(session.target_language)} · {session.topic_level}
            </p>
            <p role="status" className="text-fl-muted-2 text-sm">
              {t(session.status)} ·{' '}
              {t('score', {
                correct: session.correct,
                answered: session.answered,
              })}
            </p>
          </header>
          {session.status === 'generating' && !error && (
            <PageLoading fullScreen={false} label={t('generating')} />
          )}
          {(session.status === 'failed' || session.status === 'abandoned') && (
            <Link
              className={practiceButton}
              href={`/grammar-practice/${session.topic_id}`}
            >
              {t('another')}
            </Link>
          )}
          {answered.map((item) => (
            <section
              key={item.index}
              className={`space-y-3 border p-5 ${
                item.correct
                  ? 'border-fl-success/50 bg-fl-success/5'
                  : 'border-fl-error-fg/50 bg-fl-error-fg/5'
              }`}
            >
              <TargetLanguageText
                as="h2"
                languageCode={session.target_language}
                className="text-fl-fg text-lg"
              >
                {item.index + 1}. {item.question}
              </TargetLanguageText>
              <p
                className={`text-sm font-semibold ${
                  item.correct ? 'text-fl-success' : 'text-fl-error-fg'
                }`}
              >
                {t(item.correct ? 'correct' : 'incorrect')}
              </p>
              <p>
                {t('yourAnswer')}:{' '}
                <TargetLanguageText languageCode={session.target_language}>
                  {typeof item.answer === 'number'
                    ? item.options?.[item.answer]
                    : item.answer}
                </TargetLanguageText>
              </p>
              {item.correct_answer && (
                <p>
                  {t('solution')}:{' '}
                  <TargetLanguageText languageCode={session.target_language}>
                    {item.correct_answer}
                  </TargetLanguageText>
                </p>
              )}
              {item.explanation && (
                <p
                  lang={session.native_language}
                  className="text-fl-muted-2 text-sm leading-relaxed"
                >
                  {item.explanation}
                </p>
              )}
            </section>
          ))}
          {session.status === 'ready' && challenge && (
            <ChallengeForm
              key={challenge.index}
              challenge={challenge}
              language={session.target_language}
              disabled={busy || !known}
              onAnswer={(value) =>
                void submit('answers', { index: challenge.index, value })
              }
            />
          )}
          {session.status === 'ready' && (
            <button
              className={practiceButton}
              disabled={busy || !known}
              onClick={() => setAbandon(true)}
            >
              {t('abandon')}
            </button>
          )}
          {session.status === 'completed' && (
            <section className="border-fl-border bg-fl-surface space-y-4 border p-6">
              <h2 className="text-fl-fg text-sm font-bold tracking-widest uppercase">
                {t('completed')}
              </h2>
              <p className="text-fl-fg text-2xl font-bold">
                {t('accuracy', {
                  percent: session.answered
                    ? Math.round((session.correct / session.answered) * 100)
                    : 0,
                })}
              </p>
              <div className="flex flex-wrap gap-3">
                <Link
                  className={practiceButton}
                  href={`/grammar-practice/${session.topic_id}`}
                >
                  {t('another')}
                </Link>
                <PracticeVoiceButton
                  sessionId={session.id}
                  title={session.title}
                  targetLanguage={session.target_language}
                />
              </div>
            </section>
          )}
        </>
      )}
      <ConfirmDialog
        open={abandon}
        title={t('abandon')}
        message={t('abandonDescription')}
        confirmLabel={t('abandon')}
        cancelLabel={common('cancel')}
        confirming={busy}
        onCancel={() => setAbandon(false)}
        onConfirm={() => void submit('abandon')}
      />
    </div>
  )
}

function ChallengeForm({
  challenge,
  language,
  disabled,
  onAnswer,
}: {
  challenge: PracticeChallenge
  language: string
  disabled: boolean
  onAnswer: (value: number | string) => void
}) {
  const t = useTranslations('grammarPractice')
  const [value, setValue] = useState<number | string>('')
  return (
    <form
      className="border-fl-border bg-fl-surface space-y-4 border p-4 sm:p-6"
      onSubmit={(event) => {
        event.preventDefault()
        if (
          !disabled &&
          value !== '' &&
          (typeof value === 'number' || value.trim())
        )
          onAnswer(value)
      }}
    >
      <TargetLanguageText
        as="h2"
        languageCode={language}
        className="text-fl-fg text-lg"
      >
        {challenge.index + 1}. {challenge.question}
      </TargetLanguageText>
      {challenge.type === 'multiple_choice' ? (
        <fieldset disabled={disabled} className="grid gap-3">
          <legend className="sr-only">{t('choose')}</legend>
          {challenge.options?.map((option, index) => (
            <label
              key={index}
              className={`flex items-center gap-3 border p-3 transition-colors ${
                value === index
                  ? 'border-fl-accent text-fl-fg bg-fl-surface-2'
                  : 'border-fl-border text-fl-muted-1 hover:border-fl-muted-2 hover:text-fl-fg'
              } ${disabled ? 'cursor-not-allowed opacity-40' : 'cursor-pointer'}`}
            >
              <input
                type="radio"
                name={`challenge-${challenge.index}`}
                value={index}
                checked={value === index}
                className="accent-fl-fg shrink-0"
                onChange={() => setValue(index)}
              />
              <TargetLanguageText languageCode={language}>
                {option}
              </TargetLanguageText>
            </label>
          ))}
        </fieldset>
      ) : (
        <label className="block space-y-2">
          <span className="text-fl-muted-2 text-sm">{t('fillBlank')}</span>
          <TargetLanguageText
            as="span"
            languageCode={language}
            className="block"
          >
            <input
              lang={language}
              className="border-fl-border bg-fl-bg text-fl-fg focus:border-fl-border-2 w-full border p-3 font-[inherit] transition-colors focus:outline-none disabled:opacity-40"
              value={value}
              maxLength={500}
              disabled={disabled}
              autoComplete="off"
              onChange={(event) => setValue(event.target.value)}
            />
          </TargetLanguageText>
        </label>
      )}
      <button
        className="border-fl-border bg-fl-fg text-fl-bg hover:bg-fl-fg/90 focus-visible:outline-fl-fg w-full border py-3 text-sm font-bold tracking-widest uppercase transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 disabled:cursor-not-allowed disabled:opacity-40"
        disabled={
          disabled ||
          value === '' ||
          (typeof value === 'string' && !value.trim())
        }
        type="submit"
      >
        {t('check')}
      </button>
    </form>
  )
}
