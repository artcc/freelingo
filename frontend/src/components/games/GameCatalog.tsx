'use client'

import { useEffect, useRef, useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useTranslations } from 'next-intl'
import { useLanguageStore } from '@/store/language'
import { isFreemiumTrialActive, isSubscribed, useAuthStore } from '@/store/auth'
import { useFreemiumStore } from '@/store/freemium'
import { useConfigStore } from '@/store/config'
import { FreemiumQuotaBanner } from '@/components/billing/FreemiumQuotaBanner'
import { PaywallBanner } from '@/components/billing/PaywallBanner'
import { Pagination } from '@/components/ui/pagination'
import { PageLoading } from '@/components/ui/page-loading'
import {
  gameRequest,
  GameRequestError,
  type DetectiveCatalog,
  type DetectiveSession,
  type GameMode,
} from '@/lib/detective'

const button =
  'border-fl-border hover:border-fl-border-2 text-fl-fg border px-4 py-2 text-sm disabled:opacity-40'

export function GameCatalog({
  gameType,
}: {
  gameType: 'detective' | 'sentence-order' | 'vocabulary-pairs'
}) {
  const t = useTranslations('detective')
  const game = useTranslations(
    gameType === 'detective'
      ? 'detective'
      : gameType === 'sentence-order'
        ? 'sentenceOrder'
        : 'vocabularyPairs'
  )
  const gamePath = gameType === 'detective' ? 'error-detective' : gameType
  const common = useTranslations('common')
  const tTarget = useTranslations('targetLanguages')
  const router = useRouter()
  const language = useLanguageStore((s) => s.activeLanguage)
  const activePlan = useLanguageStore(
    (s) => s.userLanguages.find((item) => item.is_active)?.plan
  )
  const planId = activePlan?.id
  const level = activePlan?.cefr_level
  const sessionVersion = useAuthStore((s) => s.sessionVersion)
  const needsRefresh = useLanguageStore((s) => s.needsRefresh)
  const switching = useLanguageStore((s) => s.isSwitching)
  const [catalog, setCatalog] = useState<DetectiveCatalog | null>(null)
  const [error, setError] = useState('')
  const [noPlan, setNoPlan] = useState(false)
  const [paywall, setPaywall] = useState(false)
  const [busy, setBusy] = useState(false)
  const [page, setPage] = useState(0)
  const [retry, setRetry] = useState(0)
  const operation = useRef<AbortController | null>(null)
  const pending = useRef<string | null>(null)
  const blocked = useRef(false)
  const quotaWasAvailable = useRef(false)
  const quotaRecoveryAttempted = useRef(false)
  const accessRecoveryVersion = useRef(0)
  const languageCode = language?.code

  useEffect(() => {
    setPage(0)
  }, [languageCode])

  useEffect(() => {
    quotaRecoveryAttempted.current = false
    const initial = useFreemiumStore.getState().status
    quotaWasAvailable.current =
      !!initial && (initial.trial_active || initial.games_remaining > 0)
    const sameScope = () => {
      const context = useLanguageStore.getState()
      const plan = context.userLanguages.find((item) => item.is_active)?.plan
      return (
        useAuthStore.getState().sessionVersion === sessionVersion &&
        context.activeLanguage?.code === languageCode &&
        plan?.id === planId &&
        plan?.cefr_level === level &&
        !context.isSwitching &&
        !context.needsRefresh
      )
    }
    const recover = () => {
      if (!sameScope()) return
      ++accessRecoveryVersion.current
      if (blocked.current) {
        // A positive advisory transition permits one new authoritative catalog read.
        blocked.current = false
        quotaRecoveryAttempted.current = true
        setRetry((value) => value + 1)
      }
    }
    const unsubscribe = [
      useFreemiumStore.subscribe((state, previous) => {
        if (
          !sameScope() ||
          state.status === previous.status ||
          state.lastFetch === 0 ||
          !state.status
        )
          return
        const available =
          state.status.trial_active || state.status.games_remaining > 0
        const recovered = available && !quotaWasAvailable.current
        quotaWasAvailable.current = available
        if (!available) quotaRecoveryAttempted.current = false
        if (recovered) recover()
      }),
      useAuthStore.subscribe((state, previous) => {
        if (
          (state.user?.subscription_status !==
            previous.user?.subscription_status &&
            isSubscribed(state.user, true)) ||
          (state.user?.freemium_trial_ends_at !==
            previous.user?.freemium_trial_ends_at &&
            isFreemiumTrialActive(state.user, true))
        )
          recover()
      }),
      useConfigStore.subscribe((state, previous) => {
        if (
          (!state.stripeEnabled && previous.stripeEnabled) ||
          (state.freemiumTrialEnabled &&
            !previous.freemiumTrialEnabled &&
            isFreemiumTrialActive(
              useAuthStore.getState().user,
              state.stripeEnabled
            ))
        )
          recover()
      }),
    ]
    return () => unsubscribe.forEach((stop) => stop())
  }, [sessionVersion, languageCode, planId, level, gameType])

  useEffect(() => {
    const controller = new AbortController()
    const recoveryVersion = accessRecoveryVersion.current
    operation.current?.abort()
    operation.current = controller
    setCatalog(null)
    setBusy(false)
    pending.current = null
    blocked.current = false
    const cancel = () => {
      controller.abort()
      operation.current?.abort()
      operation.current = null
    }
    const current = () => {
      const context = useLanguageStore.getState()
      const plan = context.userLanguages.find((item) => item.is_active)?.plan
      return (
        !controller.signal.aborted &&
        useAuthStore.getState().sessionVersion === sessionVersion &&
        context.activeLanguage?.code === languageCode &&
        plan?.id === planId &&
        plan?.cefr_level === level &&
        !context.isSwitching &&
        context.needsRefresh === needsRefresh
      )
    }
    if (switching) return cancel
    async function load() {
      setError('')
      setNoPlan(false)
      setPaywall(false)
      try {
        if (!languageCode || needsRefresh) {
          const loaded = await useLanguageStore
            .getState()
            .fetchLanguages(controller.signal)
          if (!loaded || !useLanguageStore.getState().activeLanguage)
            throw new Error('context')
          if (!current()) return
        }
        const data = await gameRequest<DetectiveCatalog>(
          `/${gameType}?skip=${page * 10}`,
          { signal: controller.signal }
        )
        if (current()) {
          if (
            data.limited &&
            data.quota.remaining <= 0 &&
            recoveryVersion !== accessRecoveryVersion.current
          ) {
            setRetry((value) => value + 1)
            return
          }
          blocked.current = data.limited && data.quota.remaining <= 0
          if (!blocked.current) quotaRecoveryAttempted.current = false
          else if (!quotaRecoveryAttempted.current) {
            // The catalog can contradict an older positive global snapshot.
            // Arm one reconciliation, but do not rearm a conflicting retry:
            // catalog 0 -> status 3 -> catalog 0 -> status 3 must terminate.
            quotaWasAvailable.current = false
          }
          setCatalog(data)
          void useFreemiumStore.getState().fetchStatus(true)
        }
      } catch (e) {
        if (!current()) return
        if (e instanceof GameRequestError && e.status === 404) setNoPlan(true)
        else setError(common('errorMessage'))
      }
    }
    void load()
    return cancel
  }, [
    languageCode,
    planId,
    level,
    needsRefresh,
    switching,
    page,
    retry,
    common,
    gameType,
    sessionVersion,
  ])

  async function start(mode: GameMode) {
    if (!catalog || busy || switching || pending.current) return
    const controller = new AbortController()
    const recoveryVersion = accessRecoveryVersion.current
    operation.current?.abort()
    operation.current = controller
    const current = () => {
      const context = useLanguageStore.getState()
      const plan = context.userLanguages.find((item) => item.is_active)?.plan
      return (
        !controller.signal.aborted &&
        useAuthStore.getState().sessionVersion === sessionVersion &&
        context.activeLanguage?.code === languageCode &&
        plan?.id === planId &&
        plan?.cefr_level === level &&
        !context.isSwitching &&
        !context.needsRefresh
      )
    }
    if (!current()) return
    const id = crypto.randomUUID()
    pending.current = id
    setBusy(true)
    setError('')
    try {
      const session = await gameRequest<Pick<DetectiveSession, 'id'>>(
        `/${gameType}`,
        {
          method: 'POST',
          signal: controller.signal,
          body: JSON.stringify({
            request_id: id,
            study_plan_id: catalog.study_plan_id,
            mode,
          }),
        }
      )
      if (current()) router.push(`/games/${gamePath}/${session.id}`)
    } catch (e) {
      if (!current()) return
      if (e instanceof GameRequestError && e.status < 500 && e.status !== 408) {
        pending.current = null
        if (
          e.status === 402 &&
          (e.code === 'freemium_exhausted' ||
            e.code === 'subscription_required')
        ) {
          if (recoveryVersion !== accessRecoveryVersion.current) {
            setRetry((value) => value + 1)
            return
          }
          blocked.current = true
          quotaWasAvailable.current = false
          quotaRecoveryAttempted.current = false
          setPaywall(true)
          void useFreemiumStore.getState().fetchStatus(true)
        } else
          setError(
            e.status === 409 ? t('contextChanged') : common('errorMessage')
          )
      } else {
        // The POST may have committed. Recover by identity, never create another game automatically.
        router.push(`/games/${gamePath}/${id}`)
      }
    } finally {
      if (!controller.signal.aborted) setBusy(false)
    }
  }

  return (
    <div className="mx-auto max-w-4xl space-y-6 p-6 font-sans">
      <Link href="/games" className="text-fl-muted-2 text-sm">
        ← {common('back')}
      </Link>
      <header className="border-fl-border bg-fl-surface space-y-3 border p-6">
        <h1 className="text-fl-fg text-lg font-semibold">{game('title')}</h1>
        <p className="text-fl-muted-2 text-sm leading-relaxed">
          {game('rules')}
        </p>
        <p className="text-fl-muted-2 text-sm leading-relaxed">
          {gameType === 'vocabulary-pairs' ? game('xpRules') : t('xpRules')}
        </p>
        {catalog && (
          <p className="text-fl-muted-2 text-sm">
            {tTarget(catalog.target_language)} · {catalog.level}
          </p>
        )}
      </header>
      {error && (
        <div role="alert" className="text-fl-error-fg space-y-3">
          <p>{error}</p>
          <button className={button} onClick={() => setRetry((n) => n + 1)}>
            {common('retry')}
          </button>
        </div>
      )}
      {noPlan && (
        <div className="border-fl-border space-y-4 border p-6">
          <p>{common('noActivePlan')}</p>
          <Link href="/assessment" className={button}>
            {t('assessment')}
          </Link>
        </div>
      )}
      {!catalog && !noPlan && !error && (
        <PageLoading fullScreen={false} label={common('loading')} />
      )}
      {catalog && (
        <>
          <FreemiumQuotaBanner feature="games" />
          {(paywall || (catalog.limited && catalog.quota.remaining === 0)) && (
            <PaywallBanner feature="games" />
          )}
          <div className="grid gap-3 sm:grid-cols-3">
            {(['review', 'prepare', 'free'] as const).map((mode) => (
              <section
                key={mode}
                className="border-fl-border bg-fl-surface flex flex-col gap-3 border p-5"
              >
                <h2 className="font-semibold">{t(mode)}</h2>
                <p className="text-fl-muted-2 flex-1 text-sm">
                  {gameType === 'vocabulary-pairs' && mode === 'free'
                    ? game('freeDescription')
                    : t(`${mode}Description`)}
                </p>
                {!catalog.modes[mode].available && (
                  <p className="text-fl-muted-2 text-sm">
                    {t(
                      catalog.modes[mode].reason === 'noUpcoming'
                        ? 'noUpcoming'
                        : 'noSources'
                    )}
                  </p>
                )}
                <button
                  className={button}
                  disabled={
                    busy ||
                    paywall ||
                    switching ||
                    !catalog.modes[mode].available ||
                    (catalog.limited && catalog.quota.remaining === 0)
                  }
                  onClick={() => void start(mode)}
                >
                  {busy ? common('loading') : common('start')}
                </button>
              </section>
            ))}
          </div>
          <section className="space-y-3">
            <h2 className="font-semibold">{t('history')}</h2>
            {catalog.history.length === 0 && (
              <p className="text-fl-muted-2 text-sm">{t('noHistory')}</p>
            )}
            {catalog.history.map((session) => (
              <Link
                key={session.id}
                href={`/games/${gamePath}/${session.id}`}
                className="border-fl-border bg-fl-surface hover:border-fl-border-2 flex flex-wrap justify-between gap-3 border p-4 text-sm"
              >
                <span>
                  {t(session.mode)} · {session.level} ·{' '}
                  <time dateTime={session.created_at} className="font-code">
                    {session.created_at.slice(0, 10)}
                  </time>
                </span>
                <span>
                  {t(session.status)}
                  {session.status === 'completed'
                    ? ` · ${session.xp_earned} XP`
                    : ''}
                </span>
              </Link>
            ))}
            <Pagination
              page={page}
              totalPages={Math.ceil(catalog.total / 10)}
              onPageChange={setPage}
              prevLabel={common('back')}
              nextLabel={common('next')}
            />
          </section>
        </>
      )}
    </div>
  )
}
