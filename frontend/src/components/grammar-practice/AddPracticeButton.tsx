'use client'

import { useEffect, useRef, useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useTranslations } from 'next-intl'
import { apiFetch } from '@/lib/api'
import { useLanguageStore } from '@/store/language'
import {
  practiceRequest,
  PracticeRequestError,
  type PracticeTopic,
} from '@/lib/grammar-practice'
import {
  PracticeScope,
  practiceButton,
  practiceScope,
  canActInPractice,
  settlePractice,
} from './PracticeScope'

export function AddPracticeButton(props: {
  slug: string
  targetLanguage: string
}) {
  return (
    <PracticeScope>
      <AddButton {...props} />
    </PracticeScope>
  )
}

function AddButton({
  slug,
  targetLanguage,
}: {
  slug: string
  targetLanguage: string
}) {
  const t = useTranslations('grammarPractice')
  const common = useTranslations('common')
  const router = useRouter()
  const [planId, setPlanId] = useState<number | null>(null)
  const [loaded, setLoaded] = useState(false)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const [contextChanged, setContextChanged] = useState(false)
  const [retry, setRetry] = useState(0)
  const [retryAt, setRetryAt] = useState(0)
  const [clock, setClock] = useState(Date.now)
  const controller = useRef<AbortController | null>(null)
  const adding = useRef(false)
  const scope = practiceScope()

  useEffect(() => {
    if (retryAt <= Date.now()) return
    const timer = setTimeout(() => setClock(Date.now()), retryAt - Date.now())
    return () => clearTimeout(timer)
  }, [retryAt])

  useEffect(() => {
    const request = new AbortController()
    controller.current = request
    setLoaded(false)
    setPlanId(null)
    setError('')
    setContextChanged(false)
    void (async () => {
      try {
        const response = await apiFetch('/api/study-plan/current', {
          signal: AbortSignal.any([
            request.signal,
            AbortSignal.timeout(20_000),
          ]),
          cache: 'no-store',
        })
        if (!response.ok) throw new Error('context')
        const plan: { id: number; target_language: string } | null =
          await response.json()
        if (!(await settlePractice(scope, request.signal))) return
        if (plan && plan.target_language !== targetLanguage) {
          setContextChanged(true)
          setError(t('contextChanged'))
          return
        }
        setPlanId(plan?.id ?? null)
        setLoaded(true)
      } catch {
        if (await settlePractice(scope, request.signal))
          setError(common('errorMessage'))
      }
    })()
    return () => request.abort()
  }, [scope, targetLanguage, retry, common, t])

  async function add() {
    const request = controller.current
    if (
      !request ||
      request.signal.aborted ||
      adding.current ||
      !loaded ||
      !planId ||
      Date.now() < retryAt ||
      !canActInPractice(scope)
    )
      return
    adding.current = true
    setBusy(true)
    setError('')
    try {
      const topic = await practiceRequest<PracticeTopic>('/topics', {
        method: 'POST',
        signal: request.signal,
        body: JSON.stringify({
          slug,
          study_plan_id: planId,
          target_language: targetLanguage,
        }),
      })
      if (await settlePractice(scope, request.signal))
        router.push(`/grammar-practice/${topic.id}`)
    } catch (e) {
      if (!(await settlePractice(scope, request.signal))) return
      if (
        e instanceof PracticeRequestError &&
        (e.status === 409 || e.status === 404)
      ) {
        setLoaded(false)
        setPlanId(null)
        setError(t('contextChanged'))
        setContextChanged(true)
      } else {
        setError(common('errorMessage'))
        if (e instanceof PracticeRequestError && e.retryAfter)
          setRetryAt(Date.now() + e.retryAfter * 1000)
      }
    } finally {
      if (await settlePractice(scope, request.signal)) {
        adding.current = false
        setBusy(false)
      }
    }
  }

  return (
    <div className="space-y-3 font-sans">
      <button
        className={practiceButton}
        disabled={!loaded || !planId || busy || clock < retryAt}
        onClick={() => void add()}
      >
        {busy ? common('loading') : t('add')}
      </button>
      {loaded && !planId && (
        <p className="text-fl-muted-2 text-sm">
          {t('noPlan')}{' '}
          <Link href="/assessment" className="underline">
            {t('assessment')}
          </Link>
        </p>
      )}
      {error && (
        <div role="alert">
          <p>{error}</p>
          <button
            className={practiceButton}
            disabled={busy || clock < retryAt}
            onClick={() => {
              if (!canActInPractice(scope)) return
              if (contextChanged)
                useLanguageStore.getState().invalidateLanguages()
              else setRetry((n) => n + 1)
            }}
          >
            {common('retry')}
          </button>
        </div>
      )}
    </div>
  )
}
