'use client'

import { useEffect, useState, type ReactNode } from 'react'
import { useTranslations } from 'next-intl'
import { useAuthStore } from '@/store/auth'
import { useLanguageStore, waitForLanguageSwitch } from '@/store/language'
import { PageLoading } from '@/components/ui/page-loading'

export const practiceButton =
  'border-fl-border bg-fl-surface text-fl-fg hover:border-fl-border-2 hover:bg-fl-surface-2 focus-visible:outline-fl-fg inline-flex items-center justify-center gap-2 border px-4 py-2 text-center text-sm transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 disabled:cursor-not-allowed disabled:opacity-40'

export function practiceScope() {
  const auth = useAuthStore.getState()
  const language = useLanguageStore.getState()
  const plan = language.userLanguages.find((item) => item.is_active)?.plan
  return `${auth.sessionVersion}:${language.activeLanguage?.code}:${language.invalidationVersion}:${language.needsRefresh}:${plan?.id}:${plan?.cefr_level}`
}

export function canActInPractice(scope: string) {
  return scope === practiceScope() && !useLanguageStore.getState().isSwitching
}

export async function settlePractice(scope: string, signal: AbortSignal) {
  do {
    await waitForLanguageSwitch(signal)
    if (signal.aborted || scope !== practiceScope()) return false
  } while (useLanguageStore.getState().isSwitching)
  return true
}

/** Remount on context replacement; individual callbacks also check this snapshot. */
export function PracticeScope({
  children,
  saved = false,
}: {
  children: ReactNode
  saved?: boolean
}) {
  const sessionVersion = useAuthStore((s) => s.sessionVersion)
  useLanguageStore((s) => s.activeLanguage)
  useLanguageStore((s) => s.invalidationVersion)
  useLanguageStore((s) => s.userLanguages)
  const switching = useLanguageStore((s) => s.isSwitching)
  const refresh = useLanguageStore((s) => s.needsRefresh)
  const language = useLanguageStore((s) => s.activeLanguage?.code)
  const common = useTranslations('common')
  const [error, setError] = useState(false)
  const [retry, setRetry] = useState(0)
  useEffect(() => {
    const controller = new AbortController()
    setError(false)
    if (!saved && !switching && (refresh || !language)) {
      void useLanguageStore
        .getState()
        .fetchLanguages(controller.signal)
        .then((ok) => {
          if (
            !controller.signal.aborted &&
            useAuthStore.getState().sessionVersion === sessionVersion &&
            (!ok || !useLanguageStore.getState().activeLanguage)
          ) {
            setError(true)
          }
        })
    }
    return () => controller.abort()
  }, [saved, switching, refresh, language, retry, sessionVersion])
  if (error)
    return (
      <div role="alert" className="space-y-3 p-6">
        <p>{common('errorMessage')}</p>
        <button
          className={practiceButton}
          onClick={() => setRetry((n) => n + 1)}
        >
          {common('retry')}
        </button>
      </div>
    )
  if (!saved && (refresh || !language)) return <PageLoading />
  return (
    <>
      {switching && <PageLoading />}
      <div key={practiceScope()} hidden={switching} inert={switching}>
        {children}
      </div>
    </>
  )
}
