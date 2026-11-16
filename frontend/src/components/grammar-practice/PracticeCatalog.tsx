'use client'

import { useEffect, useRef, useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useTranslations } from 'next-intl'
import { isSubscribed, useAuthStore } from '@/store/auth'
import { useLanguageStore } from '@/store/language'
import { useFreemiumStore } from '@/store/freemium'
import { useConfigStore } from '@/store/config'
import { useTrialStatus } from '@/hooks/useTrialStatus'
import { FreemiumQuotaBanner } from '@/components/billing/FreemiumQuotaBanner'
import { PaywallBanner } from '@/components/billing/PaywallBanner'
import { TargetLanguageText } from '@/components/TargetLanguageText'
import NoPlanBanner from '@/components/plan/NoPlanBanner'
import { Pagination } from '@/components/ui/pagination'
import { PageLoading } from '@/components/ui/page-loading'
import { useFreemiumAccessRecovery } from '@/lib/freemium-access'
import {
  practiceRequest,
  PracticeRequestError,
  uncertainPracticeRequest,
  pendingPracticeKey,
  readPendingPractice,
  type PendingPractice,
  type PracticeLibrary,
  type PracticeHistory,
  type PracticeSession,
  type PracticeTopic,
} from '@/lib/grammar-practice'
import {
  PracticeScope,
  practiceButton,
  practiceScope,
  canActInPractice,
  settlePractice,
} from './PracticeScope'

export function PracticeCatalog({ topicId }: { topicId?: string }) {
  return (
    <PracticeScope saved={!!topicId}>
      <Catalog key={topicId ?? 'library'} topicId={topicId} />
    </PracticeScope>
  )
}

function Catalog({ topicId }: { topicId?: string }) {
  const t = useTranslations('grammarPractice')
  const common = useTranslations('common')
  const target = useTranslations('targetLanguages')
  const router = useRouter()
  const scope = practiceScope()
  const language = useLanguageStore.getState().activeLanguage?.code
  const languageReady =
    !useLanguageStore.getState().needsRefresh &&
    !useLanguageStore.getState().isSwitching
  const user = useAuthStore((s) => s.user)
  const stripeEnabled = useConfigStore((s) => s.stripeEnabled)
  const { freemiumTrialActive } = useTrialStatus()
  const [data, setData] = useState<PracticeLibrary | PracticeHistory | null>(
    null
  )
  const [page, setPage] = useState(0)
  const [retry, setRetry] = useState(0)
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  const [pending, setPending] = useState<PendingPractice | null>(null)
  const [conflictingSession, setConflictingSession] = useState<string | null>(
    null
  )
  const [retryAt, setRetryAt] = useState(0)
  const [clock, setClock] = useState(Date.now)
  const [contextChanged, setContextChanged] = useState(false)
  const operation = useRef<AbortController | null>(null)
  const creating = useRef(false)
  const { accessDenied, reportAccessDenied } =
    useFreemiumAccessRecovery('grammar_practice')
  const wasDenied = useRef(false)
  useEffect(() => {
    if (wasDenied.current && !accessDenied) setRetry((n) => n + 1)
    wasDenied.current = accessDenied
  }, [accessDenied])

  useEffect(() => {
    const controller = new AbortController()
    const unsubscribe = useFreemiumStore.subscribe((state, previous) => {
      if (
        !data?.limited ||
        data.quota.remaining > 0 ||
        state.lastFetch <= 0 ||
        (previous.status?.grammar_practice_remaining ?? 0) > 0 ||
        (state.status?.grammar_practice_remaining ?? 0) <= 0
      )
        return
      // Only a confirmed unavailable -> available transition reconciles the catalog.
      // A conflicting catalog refresh cannot rearm itself via another positive status read.
      void settlePractice(scope, controller.signal).then((current) => {
        if (current) setRetry((n) => n + 1)
      })
    })
    return () => {
      controller.abort()
      unsubscribe()
    }
  }, [data, scope])

  useEffect(() => {
    if (retryAt <= Date.now()) return
    const timer = setTimeout(() => setClock(Date.now()), retryAt - Date.now())
    return () => clearTimeout(timer)
  }, [retryAt])

  useEffect(() => {
    const controller = new AbortController()
    operation.current = controller
    creating.current = false
    setBusy(false)
    setData(null)
    setError('')
    setContextChanged(false)
    if (topicId) {
      try {
        setPending(readPendingPractice(topicId))
      } catch {
        /* Recovery remains available through the session URL. */
      }
    }
    void practiceRequest<PracticeLibrary | PracticeHistory>(
      topicId
        ? `/topics/${encodeURIComponent(topicId)}?skip=${page * 10}&limit=10`
        : `/topics?target_language=${encodeURIComponent(language ?? '')}&skip=${page * 20}&limit=20`,
      { signal: controller.signal }
    )
      .then(async (result) => {
        if (!(await settlePractice(scope, controller.signal))) return
        if (!topicId && result.target_language !== language)
          throw new Error('context')
        setData(result)
        void useFreemiumStore.getState().fetchStatus(true)
      })
      .catch(async (e: unknown) => {
        if (!(await settlePractice(scope, controller.signal))) return
        setError(common('errorMessage'))
        if (e instanceof PracticeRequestError && e.retryAfter)
          setRetryAt(Date.now() + e.retryAfter * 1000)
      })
    return () => controller.abort()
  }, [topicId, language, scope, page, retry, common])

  async function start(recovery?: PendingPractice) {
    if (
      !topicId ||
      creating.current ||
      Date.now() < retryAt ||
      !canActInPractice(scope)
    )
      return
    if (
      !recovery &&
      (!data?.study_plan_id ||
        !languageReady ||
        data.target_language !== language ||
        pending ||
        contextChanged)
    )
      return
    const controller = operation.current
    if (!controller || controller.signal.aborted) return
    const request: PendingPractice = recovery ?? {
      topic_id: Number(topicId),
      payload: {
        request_id: crypto.randomUUID(),
        study_plan_id: data!.study_plan_id!,
        target_language: data!.target_language,
      },
    }
    const id = request.payload.request_id
    // Persist the complete immutable submission before sending, including for explicit retries.
    try {
      sessionStorage.setItem(
        pendingPracticeKey(topicId),
        JSON.stringify(request)
      )
    } catch {
      setError(common('errorMessage'))
      return
    }
    creating.current = true
    setPending(request)
    setBusy(true)
    setError('')
    let submitted = false
    try {
      if (recovery) {
        try {
          const saved = await practiceRequest<PracticeSession>(
            `/sessions/${id}`,
            { signal: controller.signal }
          )
          if (!(await settlePractice(scope, controller.signal))) return
          sessionStorage.removeItem(pendingPracticeKey(topicId))
          setPending(null)
          router.push(`/grammar-practice/sessions/${saved.id}`)
          return
        } catch (e) {
          if (!(await settlePractice(scope, controller.signal))) return
          if (!(e instanceof PracticeRequestError) || e.status !== 404) throw e
        }
      }
      if (!(await settlePractice(scope, controller.signal))) return
      submitted = true
      const result = await practiceRequest<PracticeSession>(
        `/topics/${request.topic_id}/sessions`,
        {
          method: 'POST',
          signal: controller.signal,
          body: JSON.stringify(request.payload),
        }
      )
      if (!(await settlePractice(scope, controller.signal))) return
      sessionStorage.removeItem(pendingPracticeKey(topicId))
      setPending(null)
      router.push(`/grammar-practice/sessions/${result.id}`)
    } catch (e) {
      if (!(await settlePractice(scope, controller.signal))) return
      if (!submitted) {
        setError(t('recoveryError'))
        if (e instanceof PracticeRequestError && e.retryAfter)
          setRetryAt(Date.now() + e.retryAfter * 1000)
      } else if (uncertainPracticeRequest(e)) {
        router.push(`/grammar-practice/sessions/${id}`)
      } else if (e instanceof PracticeRequestError) {
        try {
          sessionStorage.removeItem(pendingPracticeKey(topicId))
        } catch {
          // Keep the in-memory outcome usable if storage becomes unavailable.
        }
        setPending(null)
        if (e.code === 'practice_in_progress' && e.sessionId)
          setConflictingSession(e.sessionId)
        else if (e.code === 'freemium_exhausted') reportAccessDenied()
        else {
          const changed = e.status === 409 || e.status === 404
          setContextChanged(changed)
          setError(changed ? t('contextChanged') : common('errorMessage'))
          if (e.retryAfter) setRetryAt(Date.now() + e.retryAfter * 1000)
        }
      }
    } finally {
      if (await settlePractice(scope, controller.signal)) {
        creating.current = false
        setBusy(false)
      }
    }
  }

  const history = data && 'topic' in data ? data : null
  const library = data && 'topics' in data ? data : null
  const unlimited =
    !stripeEnabled || isSubscribed(user, stripeEnabled) || freemiumTrialActive
  const blocked =
    accessDenied ||
    (!unlimited && !!(data?.limited && data.quota.remaining <= 0))

  if (!data && !error && !pending) return <PageLoading />
  if (library && !library.study_plan_id && library.total === 0)
    return <NoPlanBanner />

  return (
    <div className="mx-auto max-w-4xl space-y-6 px-4 py-6 font-sans md:px-8">
      {topicId && (
        <Link
          href="/grammar-practice"
          className="text-fl-muted-2 hover:text-fl-fg inline-flex text-sm transition-colors"
        >
          ← {t('back')}
        </Link>
      )}
      <header className="space-y-2">
        <h1
          className={
            history
              ? 'text-fl-fg text-xl font-semibold'
              : 'text-fl-fg text-sm font-bold tracking-widest uppercase'
          }
        >
          {history ? (
            <TargetLanguageText languageCode={history.target_language}>
              {history.topic.title}
            </TargetLanguageText>
          ) : (
            t('title')
          )}
        </h1>
        <p className="text-fl-muted-2 text-sm">{t('description')}</p>
        {data && (
          <p className="text-fl-muted-3 text-xs">
            {target(data.target_language)}
          </p>
        )}
      </header>
      {error && (
        <div role="alert" className="space-y-3">
          <p className="text-fl-error-fg text-sm">{error}</p>
          <button
            disabled={clock < retryAt || busy}
            className={practiceButton}
            onClick={() => setRetry((n) => n + 1)}
          >
            {common('retry')}
          </button>
        </div>
      )}
      {!data && !error && <PageLoading fullScreen={false} />}
      {pending && (
        <section className="border-fl-border bg-fl-surface space-y-3 border p-4">
          <p className="text-fl-muted-2 text-sm">{t('recoveryError')}</p>
          <div className="flex flex-wrap gap-3">
            <Link
              className={practiceButton}
              href={`/grammar-practice/sessions/${pending.payload.request_id}`}
            >
              {t('recover')}
            </Link>
            <button
              className={practiceButton}
              disabled={busy || clock < retryAt}
              onClick={() => void start(pending)}
            >
              {t('retryCreation')}
            </button>
          </div>
        </section>
      )}
      {data && (
        <>
          <FreemiumQuotaBanner feature="grammar_practice" />
          {blocked && <PaywallBanner feature="grammar_practice" compact />}
          {!data.study_plan_id && (
            <div className="border-fl-border bg-fl-surface flex flex-wrap items-center justify-between gap-4 border p-4">
              <p className="text-fl-muted-2 text-sm">{t('noPlan')}</p>
              <Link href="/assessment" className={practiceButton}>
                {t('assessment')}
              </Link>
            </div>
          )}
          {library && (
            <>
              {library.total === 0 ? (
                <div className="border-fl-border bg-fl-surface space-y-4 border px-6 py-10 text-center">
                  <p className="text-fl-muted-2 text-sm">{t('empty')}</p>
                  <Link href="/grammar" className={practiceButton}>
                    {t('explore')}
                  </Link>
                </div>
              ) : (
                <Link href="/grammar" className={practiceButton}>
                  {t('explore')}
                </Link>
              )}
              <div className="grid gap-3 sm:grid-cols-2">
                {library.topics.map((topic) => (
                  <Link
                    key={topic.id}
                    href={`/grammar-practice/${topic.id}`}
                    className="border-fl-border bg-fl-surface hover:border-fl-border-2 hover:bg-fl-surface-2 block min-w-0 space-y-3 border p-5 transition-colors"
                  >
                    <h2 className="text-fl-fg font-semibold">
                      <TargetLanguageText languageCode={data.target_language}>
                        {topic.title}
                      </TargetLanguageText>
                    </h2>
                    <TopicStats topic={topic} />
                  </Link>
                ))}
              </div>
            </>
          )}
          {history && (
            <>
              <TopicStats topic={history.topic} />
              <div className="flex flex-wrap gap-3">
                {languageReady && history.target_language === language ? (
                  <Link
                    href={`/grammar/${history.topic.slug}`}
                    className={practiceButton}
                  >
                    {t('theory')}
                  </Link>
                ) : (
                  <button className={practiceButton} disabled>
                    {t('theory')}
                  </button>
                )}
                {(conflictingSession || history.topic.active_session_id) && (
                  <Link
                    className={practiceButton}
                    href={`/grammar-practice/sessions/${conflictingSession ?? history.topic.active_session_id}`}
                  >
                    {t('continue')}
                  </Link>
                )}
                <button
                  className={practiceButton}
                  disabled={
                    busy ||
                    !!pending ||
                    blocked ||
                    !history.study_plan_id ||
                    !languageReady ||
                    history.target_language !== language ||
                    contextChanged ||
                    clock < retryAt
                  }
                  onClick={() => void start()}
                >
                  {busy ? common('loading') : t('generate')}
                </button>
              </div>
              {(!languageReady || history.target_language !== language) && (
                <p className="text-fl-muted-2 text-sm">{t('contextChanged')}</p>
              )}
              <section className="space-y-3">
                <h2 className="text-fl-fg text-sm font-bold tracking-widest uppercase">
                  {t('history')}
                </h2>
                {history.sessions.length === 0 && (
                  <div className="border-fl-border bg-fl-surface border p-6 text-center">
                    <p className="text-fl-muted-2 text-sm">{t('noHistory')}</p>
                  </div>
                )}
                {history.sessions.map((session) => (
                  <Link
                    key={session.id}
                    href={`/grammar-practice/sessions/${session.id}`}
                    className="border-fl-border bg-fl-surface hover:border-fl-border-2 hover:bg-fl-surface-2 text-fl-fg flex flex-wrap items-center justify-between gap-3 border p-4 text-sm transition-colors"
                  >
                    <time dateTime={session.created_at}>
                      {session.created_at.slice(0, 10)}
                    </time>
                    <span>
                      {t(session.status)} ·{' '}
                      {t('score', {
                        correct: session.correct,
                        answered: session.answered,
                      })}
                    </span>
                  </Link>
                ))}
              </section>
            </>
          )}
          <Pagination
            page={page}
            totalPages={Math.ceil(data.total / (topicId ? 10 : 20))}
            loading={busy}
            onPageChange={setPage}
            prevLabel={common('back')}
            nextLabel={common('next')}
          />
          {blocked && (
            <button
              className={practiceButton}
              onClick={() => setRetry((n) => n + 1)}
            >
              {common('retry')}
            </button>
          )}
        </>
      )}
    </div>
  )
}

function TopicStats({ topic }: { topic: PracticeTopic }) {
  const t = useTranslations('grammarPractice')
  return (
    <div className="text-fl-muted-2 space-y-1 text-sm">
      <p>
        {topic.level} · {t('answered', { count: topic.answered })} ·{' '}
        {t('accuracy', {
          percent: topic.answered
            ? Math.round((topic.correct / topic.answered) * 100)
            : 0,
        })}
      </p>
      <p>
        {t('lastPracticed')}:{' '}
        {topic.last_practiced ? (
          <time dateTime={topic.last_practiced}>
            {topic.last_practiced.slice(0, 10)}
          </time>
        ) : (
          t('never')
        )}
      </p>
    </div>
  )
}
