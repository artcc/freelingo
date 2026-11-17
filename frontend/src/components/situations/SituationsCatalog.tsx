'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useLocale, useTranslations } from 'next-intl'
import { MessageSquare, Search } from 'lucide-react'
import { useAuthStore, isSubscribed } from '@/store/auth'
import { useLanguageStore } from '@/store/language'
import { useConfigStore } from '@/store/config'
import { useFreemiumStore } from '@/store/freemium'
import { useTrialStatus } from '@/hooks/useTrialStatus'
import { FreemiumQuotaBanner } from '@/components/billing/FreemiumQuotaBanner'
import { PaywallBanner } from '@/components/billing/PaywallBanner'
import NoPlanBanner from '@/components/plan/NoPlanBanner'
import { PageLoading } from '@/components/ui/page-loading'
import {
  fetchSituationCatalog,
  SituationContextError,
  type SituationCatalog,
  type SituationCategory,
} from '@/lib/situations'

const buttonClass =
  'border-fl-border bg-fl-surface text-fl-fg hover:border-fl-border-2 hover:bg-fl-surface-2 focus-visible:outline-fl-accent inline-flex items-center justify-center border px-4 py-2 text-sm transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 disabled:cursor-not-allowed disabled:opacity-40'

function currentScope() {
  const auth = useAuthStore.getState()
  const state = useLanguageStore.getState()
  const plan = state.userLanguages.find(
    (language) => language.target_language === state.activeLanguage?.code
  )?.plan
  return `${auth.sessionVersion}:${auth.user?.id}:${state.activeLanguage?.code}:${plan?.id}:${plan?.cefr_level}:${state.invalidationVersion}`
}

export function SituationsCatalog() {
  const t = useTranslations('situations')
  const sessionVersion = useAuthStore((s) => s.sessionVersion)
  const userId = useAuthStore((s) => s.user?.id)
  const language = useLanguageStore((s) => s.activeLanguage?.code)
  const languages = useLanguageStore((s) => s.userLanguages)
  const switching = useLanguageStore((s) => s.isSwitching)
  const needsRefresh = useLanguageStore((s) => s.needsRefresh)
  useLanguageStore((s) => s.invalidationVersion)
  const [error, setError] = useState(false)
  const [retry, setRetry] = useState(0)
  const plan = languages.find((item) => item.target_language === language)?.plan

  useEffect(() => {
    const controller = new AbortController()
    setError(false)
    if (!switching && (needsRefresh || !language)) {
      void useLanguageStore
        .getState()
        .fetchLanguages(controller.signal)
        .then((ok) => {
          if (
            !controller.signal.aborted &&
            useAuthStore.getState().sessionVersion === sessionVersion &&
            useAuthStore.getState().user?.id === userId &&
            (!ok || !useLanguageStore.getState().activeLanguage)
          )
            setError(true)
        })
    }
    return () => controller.abort()
  }, [language, needsRefresh, switching, sessionVersion, userId, retry])

  if (error)
    return (
      <div role="alert" className="space-y-3 p-6">
        <p>{t('loadError')}</p>
        <button className={buttonClass} onClick={() => setRetry((n) => n + 1)}>
          {t('retry')}
        </button>
      </div>
    )
  if (switching || needsRefresh || !language) return <PageLoading />
  if (!plan) return <NoPlanBanner />
  return (
    <Catalog
      key={currentScope()}
      scope={currentScope()}
      planId={plan.id}
      language={language}
      level={plan.cefr_level}
    />
  )
}

function Catalog({
  scope,
  planId,
  language,
  level,
}: {
  scope: string
  planId: number
  language: string
  level: string | null
}) {
  const t = useTranslations('situations')
  const locale = useLocale()
  const router = useRouter()
  const [catalog, setCatalog] = useState<SituationCatalog | null>(null)
  const [error, setError] = useState<'loadError' | 'contextChanged' | null>(
    null
  )
  const [retry, setRetry] = useState(0)
  const [search, setSearch] = useState('')
  const [category, setCategory] = useState<SituationCategory | ''>('')
  const user = useAuthStore((s) => s.user)
  const stripeEnabled = useConfigStore((s) => s.stripeEnabled)
  const status = useFreemiumStore((s) => s.status)
  const { freemiumTrialActive } = useTrialStatus()
  const limited =
    stripeEnabled && !isSubscribed(user, stripeEnabled) && !freemiumTrialActive
  const blockedFeature =
    limited &&
    status?.situations_remaining !== undefined &&
    status.situations_remaining <= 0
      ? 'situations'
      : limited && status && status.voice_remaining_seconds <= 0
        ? 'voice'
        : null

  useEffect(() => {
    const controller = new AbortController()
    const current = () =>
      !controller.signal.aborted &&
      scope === currentScope() &&
      !useLanguageStore.getState().isSwitching &&
      !useLanguageStore.getState().needsRefresh
    setError(null)
    void fetchSituationCatalog(planId, controller.signal)
      .then((data) => {
        if (!current()) return
        if (
          data.target_language !== language ||
          (level && data.cefr_level !== level)
        )
          throw new SituationContextError('Situation context changed')
        setCatalog(data)
      })
      .catch((cause: unknown) => {
        if (current())
          setError(
            cause instanceof SituationContextError
              ? 'contextChanged'
              : 'loadError'
          )
      })
    if (stripeEnabled) void useFreemiumStore.getState().fetchStatus()
    return () => controller.abort()
  }, [scope, planId, language, level, retry, stripeEnabled])

  if (!catalog && !error) return <PageLoading />
  const collator = new Intl.Collator(locale)
  const categories = [
    ...new Set(catalog?.situations.map((item) => item.category)),
  ].sort((a, b) => collator.compare(t(`categories.${a}`), t(`categories.${b}`)))
  const query = search.trim().toLocaleLowerCase(locale)
  const items = (catalog?.situations ?? [])
    .filter(
      (item) =>
        (!category || item.category === category) &&
        [
          t(`items.${item.id}.title`),
          t(`items.${item.id}.description`),
          t(`categories.${item.category}`),
        ].some((text) => text.toLocaleLowerCase(locale).includes(query))
    )
    .sort((a, b) =>
      collator.compare(t(`items.${a.id}.title`), t(`items.${b.id}.title`))
    )

  return (
    <div className="mx-auto max-w-4xl space-y-6 px-4 py-6 font-sans md:px-8">
      <header className="space-y-2">
        <h1 className="text-fl-fg text-sm font-bold tracking-widest uppercase">
          {t('title')}
        </h1>
        <p className="text-fl-muted-2 text-sm">{t('description')}</p>
      </header>
      {error ? (
        <div role="alert" className="space-y-3">
          <p className="text-fl-error text-sm">{t(error)}</p>
          <button
            className={buttonClass}
            onClick={() => {
              if (error === 'contextChanged')
                useLanguageStore.getState().invalidateLanguages()
              else setRetry((n) => n + 1)
            }}
          >
            {t('retry')}
          </button>
        </div>
      ) : (
        <>
          <FreemiumQuotaBanner feature="situations" />
          {blockedFeature && <PaywallBanner feature={blockedFeature} compact />}
          <div className="flex flex-col gap-3 sm:flex-row">
            <label className="border-fl-border bg-fl-surface flex flex-1 items-center gap-2 border px-3">
              <Search
                className="text-fl-muted-2 size-4 shrink-0"
                aria-hidden="true"
              />
              <input
                type="search"
                aria-label={t('search')}
                placeholder={t('search')}
                value={search}
                onChange={(event) => setSearch(event.target.value)}
                className="text-fl-fg placeholder:text-fl-muted-3 focus-visible:outline-fl-accent w-full bg-transparent py-3 text-sm focus-visible:outline-2"
              />
            </label>
            <select
              aria-label={t('allCategories')}
              value={category}
              onChange={(event) =>
                setCategory(event.target.value as SituationCategory | '')
              }
              className="border-fl-border bg-fl-surface text-fl-fg focus-visible:outline-fl-accent border px-3 py-3 text-sm focus-visible:outline-2"
            >
              <option value="">{t('allCategories')}</option>
              {categories.map((item) => (
                <option key={item} value={item}>
                  {t(`categories.${item}`)}
                </option>
              ))}
            </select>
          </div>
          {items.length === 0 && (
            <p className="text-fl-muted-2 py-8 text-center text-sm">
              {t('noResults')}
            </p>
          )}
          {categories.map((group) => {
            const entries = items.filter((item) => item.category === group)
            if (!entries.length) return null
            return (
              <section
                key={group}
                aria-labelledby={`situation-${group}`}
                className="space-y-3"
              >
                <h2
                  id={`situation-${group}`}
                  className="text-fl-fg text-sm font-semibold"
                >
                  {t(`categories.${group}`)}
                </h2>
                <div className="grid gap-3 sm:grid-cols-2">
                  {entries.map((item) => (
                    <article
                      key={item.id}
                      className="border-fl-border bg-fl-surface flex min-w-0 flex-col gap-3 border p-5"
                    >
                      <MessageSquare
                        className="text-fl-accent size-5"
                        aria-hidden="true"
                      />
                      <h3 className="text-fl-fg font-semibold">
                        {t(`items.${item.id}.title`)}
                      </h3>
                      <p className="text-fl-muted-2 flex-1 text-sm leading-relaxed">
                        {t(`items.${item.id}.description`)}
                      </p>
                      <button
                        className={buttonClass}
                        disabled={!!blockedFeature}
                        aria-label={`${t('start')}: ${t(`items.${item.id}.title`)}`}
                        onClick={() => {
                          const state = useLanguageStore.getState()
                          if (
                            scope !== currentScope() ||
                            state.isSwitching ||
                            state.needsRefresh
                          )
                            return
                          router.push(
                            `/conversation?situation=${item.id}&plan=${planId}`
                          )
                        }}
                      >
                        {t('start')}
                      </button>
                    </article>
                  ))}
                </div>
              </section>
            )
          })}
        </>
      )}
    </div>
  )
}
