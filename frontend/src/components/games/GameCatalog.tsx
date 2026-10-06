'use client'

import { useEffect, useRef, useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useTranslations } from 'next-intl'
import { useLanguageStore } from '@/store/language'
import { useFreemiumStore } from '@/store/freemium'
import { FreemiumQuotaBanner } from '@/components/billing/FreemiumQuotaBanner'
import { PaywallBanner } from '@/components/billing/PaywallBanner'
import { Pagination } from '@/components/ui/pagination'
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
  gameType: 'detective' | 'sentence-order'
}) {
  const t = useTranslations('detective')
  const game = useTranslations(
    gameType === 'detective' ? 'detective' : 'sentenceOrder'
  )
  const gamePath =
    gameType === 'detective' ? 'error-detective' : 'sentence-order'
  const common = useTranslations('common')
  const tTarget = useTranslations('targetLanguages')
  const router = useRouter()
  const language = useLanguageStore((s) => s.activeLanguage)
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
  const languageCode = language?.code

  useEffect(() => {
    setPage(0)
  }, [languageCode])

  useEffect(() => {
    const controller = new AbortController()
    operation.current?.abort()
    operation.current = controller
    setCatalog(null)
    setBusy(false)
    pending.current = null
    const cancel = () => {
      controller.abort()
      operation.current?.abort()
      operation.current = null
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
          if (controller.signal.aborted) return
        }
        const data = await gameRequest<DetectiveCatalog>(
          `/${gameType}?skip=${page * 10}`,
          { signal: controller.signal }
        )
        if (!controller.signal.aborted) {
          setCatalog(data)
          void useFreemiumStore.getState().fetchStatus(true)
        }
      } catch (e) {
        if (controller.signal.aborted) return
        if (e instanceof GameRequestError && e.status === 404) setNoPlan(true)
        else setError(common('errorMessage'))
      }
    }
    void load()
    return cancel
  }, [languageCode, needsRefresh, switching, page, retry, common, gameType])

  async function start(mode: GameMode) {
    if (!catalog || busy || switching || pending.current) return
    const controller = new AbortController()
    operation.current?.abort()
    operation.current = controller
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
      if (!controller.signal.aborted)
        router.push(`/games/${gamePath}/${session.id}`)
    } catch (e) {
      if (controller.signal.aborted) return
      if (e instanceof GameRequestError && e.status < 500 && e.status !== 408) {
        pending.current = null
        if (e.status === 402) setPaywall(true)
        else
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
          {t('xpRules')}
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
        <p role="status">{common('loading')}</p>
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
                  {t(`${mode}Description`)}
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
