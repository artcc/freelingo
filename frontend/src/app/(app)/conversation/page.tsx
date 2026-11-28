/**
 * /conversation — Voice conversation page.
 *
 * ConversationMode uses @ricky0123/vad-react (ONNX/WASM) and the Web Audio
 * API, neither of which are compatible with SSR. It is loaded client-side only
 * via `dynamic({ ssr: false })`.
 */
'use client'

import { useCallback, useEffect, useState } from 'react'
import { useSearchParams } from 'next/navigation'
import { useTranslations } from 'next-intl'
import Link from 'next/link'
import dynamic from 'next/dynamic'
import type { ChatContextItem } from '@/lib/conversation-ws'
import { PageLoading } from '@/components/ui/page-loading'
import { FreemiumQuotaBanner } from '@/components/billing/FreemiumQuotaBanner'
import FreeVoiceBalance from '@/components/conversation/FreeVoiceBalance'
import { PaywallBanner } from '@/components/billing/PaywallBanner'
import { MaintenanceGate } from '@/components/billing/MaintenanceBanner'
import { apiFetch } from '@/lib/api'
import { useLanguageStore } from '@/store/language'
import { useConfigStore } from '@/store/config'
import { useAuthStore, isSubscribed } from '@/store/auth'
import { useFreemiumStore } from '@/store/freemium'
import { useTrialStatus } from '@/hooks/useTrialStatus'
import {
  fetchSituationCatalog,
  parseSituationSource,
  type SituationId,
} from '@/lib/situations'

function ConversationLoading() {
  return <PageLoading />
}

const ConversationMode = dynamic(
  () => import('@/components/conversation/ConversationMode'),
  {
    ssr: false,
    loading: ConversationLoading,
  }
)

interface LessonPractice {
  id?: number
  grammarPracticeSessionId?: string
  situationId?: SituationId
  situationStudyPlanId?: number
  title?: string
  cefrLevel: string
  targetLanguage: string
}

export default function ConversationPage() {
  const searchParams = useSearchParams()
  const sessionVersion = useAuthStore((s) => s.sessionVersion)
  const userId = useAuthStore((s) => s.user?.id)
  const lessonId = searchParams.get('lesson')
  const grammarPracticeId = searchParams.get('grammarPractice')
  const ownerKey = `${sessionVersion}:${userId}`
  if (searchParams.has('situation') || searchParams.has('plan')) {
    const source = parseSituationSource(searchParams)
    return (
      <SituationConversationPage
        key={`${ownerKey}:situation:${searchParams.toString()}`}
        source={source}
      />
    )
  }
  if (grammarPracticeId !== null) {
    return (
      <GrammarConversationPage
        key={`${ownerKey}:grammar:${grammarPracticeId}:${lessonId}`}
        sessionId={grammarPracticeId}
        conflictingSource={lessonId !== null}
      />
    )
  }
  return lessonId !== null ? (
    <LessonConversationPage
      key={`${ownerKey}:${lessonId}`}
      lessonId={lessonId}
    />
  ) : (
    <ConversationPageContent key={ownerKey} />
  )
}

function SituationConversationPage({
  source,
}: {
  source: ReturnType<typeof parseSituationSource>
}) {
  const t = useTranslations('situations')
  const [practice, setPractice] = useState<LessonPractice | null>(null)
  const [failed, setFailed] = useState(false)
  const [attempt, setAttempt] = useState(0)
  const id = source?.id
  const studyPlanId = source?.studyPlanId

  useEffect(() => {
    const controller = new AbortController()
    const owner = useAuthStore.getState()
    const current = () => {
      const auth = useAuthStore.getState()
      return (
        !controller.signal.aborted &&
        auth.sessionVersion === owner.sessionVersion &&
        auth.user?.id === owner.user?.id
      )
    }
    async function load() {
      try {
        if (!id || !studyPlanId) throw new Error('Invalid situation source')
        const catalog = await fetchSituationCatalog(
          studyPlanId,
          controller.signal
        )
        if (!current()) return
        if (!catalog.situations.some((item) => item.id === id))
          throw new Error('Situation unavailable')
        setPractice({
          situationId: id,
          situationStudyPlanId: studyPlanId,
          cefrLevel: catalog.cefr_level,
          targetLanguage: catalog.target_language,
        })
      } catch {
        if (current()) setFailed(true)
      }
    }
    void load()
    return () => controller.abort()
  }, [id, studyPlanId, attempt])

  if (failed)
    return (
      <div className="flex min-h-[60vh] flex-col items-center justify-center gap-4 p-6">
        <p role="alert" className="text-fl-muted-1 font-sans text-sm">
          {t('unavailable')}
        </p>
        <button
          type="button"
          className="text-fl-accent font-sans text-sm underline"
          onClick={() => {
            setFailed(false)
            setAttempt((value) => value + 1)
          }}
        >
          {t('retry')}
        </button>
        <Link
          href="/situations"
          className="text-fl-muted-1 font-sans text-sm underline"
        >
          {t('back')}
        </Link>
      </div>
    )
  if (!practice) return <ConversationLoading />
  return <ConversationPageContent practice={practice} />
}

function GrammarConversationPage({
  sessionId,
  conflictingSource,
}: {
  sessionId: string
  conflictingSource: boolean
}) {
  const t = useTranslations('grammarPractice')
  const tCommon = useTranslations('common')
  const [practice, setPractice] = useState<LessonPractice | null>(null)
  const [failed, setFailed] = useState(false)
  const [attempt, setAttempt] = useState(0)

  useEffect(() => {
    const controller = new AbortController()
    const timeout = setTimeout(() => controller.abort(), 20_000)
    let cancelled = false
    async function load() {
      try {
        if (
          conflictingSource ||
          !/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(
            sessionId
          )
        )
          throw new Error('Invalid grammar practice')
        const res = await apiFetch(
          `/api/grammar-practice/sessions/${sessionId}`,
          { signal: controller.signal }
        )
        if (!res.ok) throw new Error('Grammar practice unavailable')
        const data = await res.json()
        if (
          controller.signal.aborted ||
          data.id !== sessionId.toLowerCase() ||
          data.status !== 'completed' ||
          typeof data.title !== 'string' ||
          typeof data.learner_level !== 'string' ||
          typeof data.target_language !== 'string' ||
          !data.target_language
        )
          throw new Error('Invalid grammar practice context')
        if (!cancelled)
          setPractice({
            grammarPracticeSessionId: data.id,
            title: data.title,
            cefrLevel: data.learner_level,
            targetLanguage: data.target_language,
          })
      } catch {
        if (!cancelled) setFailed(true)
      } finally {
        clearTimeout(timeout)
      }
    }
    void load()
    return () => {
      cancelled = true
      clearTimeout(timeout)
      controller.abort()
    }
  }, [sessionId, conflictingSource, attempt])

  if (failed)
    return (
      <div className="flex min-h-[60vh] flex-col items-center justify-center gap-4 p-6">
        <p role="alert" className="text-fl-muted-1 font-sans text-sm">
          {t('voiceUnavailable')}
        </p>
        <button
          type="button"
          className="text-fl-accent font-sans text-sm underline"
          onClick={() => {
            setFailed(false)
            setAttempt((value) => value + 1)
          }}
        >
          {tCommon('retry')}
        </button>
        <Link
          href="/grammar-practice"
          className="text-fl-muted-1 font-sans text-sm underline"
        >
          {t('back')}
        </Link>
      </div>
    )
  if (!practice) return <ConversationLoading />
  return <ConversationPageContent practice={practice} />
}

function LessonConversationPage({ lessonId }: { lessonId: string }) {
  const t = useTranslations('lessonPractice')
  const tCommon = useTranslations('common')
  const [practice, setPractice] = useState<LessonPractice | null>(null)
  const [failed, setFailed] = useState(false)
  const [attempt, setAttempt] = useState(0)

  useEffect(() => {
    const controller = new AbortController()
    let cancelled = false
    const timeout = setTimeout(() => controller.abort(), 20_000)
    async function load() {
      try {
        const id = Number(lessonId)
        if (
          !/^\d+$/.test(lessonId) ||
          !Number.isSafeInteger(id) ||
          id <= 0 ||
          id > 2_147_483_647
        ) {
          throw new Error('Invalid lesson')
        }
        const res = await apiFetch(`/api/lessons/${id}`, {
          signal: controller.signal,
        })
        if (!res.ok) throw new Error('Lesson unavailable')
        const data = await res.json()
        if (
          data.lesson?.id !== id ||
          data.lesson?.is_completed !== true ||
          typeof data.lesson?.title !== 'string' ||
          typeof data.lesson?.cefr_level !== 'string' ||
          typeof data.target_language !== 'string' ||
          !data.target_language
        ) {
          throw new Error('Invalid lesson context')
        }
        if (!cancelled) {
          setPractice({
            id,
            title: data.lesson.title,
            cefrLevel: data.lesson.cefr_level,
            targetLanguage: data.target_language,
          })
        }
      } catch {
        if (!cancelled) setFailed(true)
      } finally {
        clearTimeout(timeout)
      }
    }
    void load()
    return () => {
      cancelled = true
      clearTimeout(timeout)
      controller.abort()
    }
  }, [lessonId, attempt])

  if (failed) {
    return (
      <div className="flex min-h-[60vh] flex-col items-center justify-center gap-4 p-6">
        <p role="alert" className="text-fl-muted-1 font-sans text-sm">
          {t('unavailable')}
        </p>
        <button
          type="button"
          className="text-fl-accent font-sans text-sm underline"
          onClick={() => {
            setFailed(false)
            setAttempt((value) => value + 1)
          }}
        >
          {tCommon('retry')}
        </button>
        <Link
          href="/plan"
          className="text-fl-muted-1 font-sans text-sm underline"
        >
          {t('back')}
        </Link>
      </div>
    )
  }
  if (!practice) return <ConversationLoading />
  return <ConversationPageContent practice={practice} />
}

function ConversationPageContent({ practice }: { practice?: LessonPractice }) {
  const tSituations = useTranslations('situations')
  const activeLanguage = useLanguageStore((s) => s.activeLanguage)
  const activePlanId = useLanguageStore(
    (s) =>
      s.userLanguages.find(
        (language) => language.target_language === s.activeLanguage?.code
      )?.plan?.id
  )
  const planKey = `${activeLanguage?.code}:${activePlanId}`
  const stripeEnabled = useConfigStore((s) => s.stripeEnabled)
  const user = useAuthStore((s) => s.user)
  const { freemiumTrialActive } = useTrialStatus()
  const fetchFreemium = useFreemiumStore((s) => s.fetchStatus)
  const freemiumStatus = useFreemiumStore((s) => s.status)
  const [sessionActive, setSessionActive] = useState(false)
  const [sessionStarted, setSessionStarted] = useState(false)
  const handleSessionActiveChange = useCallback((active: boolean) => {
    setSessionActive(active)
    if (active) setSessionStarted(true)
  }, [])
  const freemiumExhausted =
    stripeEnabled &&
    !isSubscribed(user, stripeEnabled) &&
    !freemiumTrialActive &&
    freemiumStatus &&
    freemiumStatus.voice_remaining_seconds <= 0
  const situationsExhausted =
    !!practice?.situationId &&
    stripeEnabled &&
    !isSubscribed(user, stripeEnabled) &&
    !freemiumTrialActive &&
    freemiumStatus?.situations_remaining !== undefined &&
    freemiumStatus.situations_remaining <= 0
  const exhaustedFeature = situationsExhausted ? 'situations' : 'voice'

  const [initialContext, setInitialContext] = useState<
    ChatContextItem[] | undefined
  >(undefined)
  const [autoStart, setAutoStart] = useState(!!practice)
  const [cefrLevel, setCefrLevel] = useState<string | null>(
    practice?.cefrLevel ?? null
  )
  const [planReady, setPlanReady] = useState(!!practice)
  const [readyPlanKey, setReadyPlanKey] = useState<string>()
  const [voiceTrial, setVoiceTrial] = useState<{
    token: string
    durationSeconds?: number
    cefrLevel?: string
    targetLanguage?: string
  } | null>(null)

  useEffect(() => {
    if (
      practice?.situationId &&
      !sessionStarted &&
      (situationsExhausted || freemiumExhausted)
    ) {
      setAutoStart(false)
    }
  }, [
    practice?.situationId,
    sessionStarted,
    situationsExhausted,
    freemiumExhausted,
  ])

  useEffect(() => {
    if (stripeEnabled && !isSubscribed(user, stripeEnabled)) {
      void fetchFreemium(true)
    }
  }, [stripeEnabled, user, fetchFreemium])

  useEffect(() => {
    if (practice) return
    setSessionActive(false)
    setSessionStarted(false)
    const controller = new AbortController()
    const raw = sessionStorage.getItem('voice_context')
    if (raw) {
      sessionStorage.removeItem('voice_context')
      try {
        const parsed = JSON.parse(raw) as unknown
        if (
          typeof parsed === 'object' &&
          parsed !== null &&
          'messages' in (parsed as Record<string, unknown>)
        ) {
          const pkg = parsed as { messages: unknown }
          if (Array.isArray(pkg.messages)) {
            setInitialContext(pkg.messages as ChatContextItem[])
          }
          setAutoStart(true)
        } else if (Array.isArray(parsed)) {
          setInitialContext(parsed as ChatContextItem[])
          setAutoStart(true)
        }
      } catch {
        // malformed — ignore
      }
    }
    const trialRaw = sessionStorage.getItem('assessment_voice_trial')
    if (trialRaw) {
      sessionStorage.removeItem('assessment_voice_trial')
      try {
        const parsed = JSON.parse(trialRaw) as {
          token?: unknown
          durationSeconds?: unknown
          cefrLevel?: unknown
          targetLanguage?: unknown
        }
        if (typeof parsed.token === 'string' && parsed.token.length > 0) {
          setVoiceTrial({
            token: parsed.token,
            durationSeconds:
              typeof parsed.durationSeconds === 'number' &&
              Number.isSafeInteger(parsed.durationSeconds) &&
              parsed.durationSeconds > 0
                ? parsed.durationSeconds
                : undefined,
            cefrLevel:
              typeof parsed.cefrLevel === 'string'
                ? parsed.cefrLevel
                : undefined,
            targetLanguage:
              typeof parsed.targetLanguage === 'string'
                ? parsed.targetLanguage
                : undefined,
          })
          setInitialContext([
            {
              role: 'user',
              content:
                'I just completed the placement assessment. Please start a short, friendly voice conversation adapted to my level.',
            },
          ])
          setAutoStart(true)
        }
      } catch {
        // malformed — ignore
      }
    }
    setPlanReady(false)
    setCefrLevel(null)
    apiFetch('/api/study-plan/today', { signal: controller.signal })
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => {
        if (!controller.signal.aborted && data?.cefr_level) {
          setCefrLevel(data.cefr_level)
        }
      })
      .catch(() => {
        /* sin plan — usa default 1500ms */
      })
      .finally(() => {
        if (!controller.signal.aborted) {
          setReadyPlanKey(planKey)
          setPlanReady(true)
        }
      })
    return () => controller.abort()
  }, [planKey, practice])

  if (!practice && (!planReady || readyPlanKey !== planKey)) {
    return <ConversationLoading />
  }

  return (
    <MaintenanceGate>
      {voiceTrial ? (
        <ConversationMode
          initialContext={initialContext}
          autoStart={autoStart}
          cefrLevel={voiceTrial.cefrLevel ?? cefrLevel}
          targetLanguage={voiceTrial.targetLanguage ?? activeLanguage?.code}
          voiceTrialToken={voiceTrial.token}
          voiceTrialDurationSeconds={voiceTrial.durationSeconds}
          trialMode
        />
      ) : (freemiumExhausted || situationsExhausted) &&
        !sessionActive &&
        !sessionStarted ? (
        <>
          {exhaustedFeature === 'voice' &&
          freemiumStatus &&
          freemiumStatus.voice_limit_seconds > 0 ? (
            <div className="mb-4">
              <FreeVoiceBalance
                seconds={freemiumStatus.voice_remaining_seconds}
              />
            </div>
          ) : (
            <FreemiumQuotaBanner feature={exhaustedFeature} className="mb-4" />
          )}
          <PaywallBanner feature={exhaustedFeature} compact />
        </>
      ) : (
        <ConversationMode
          initialContext={initialContext}
          autoStart={autoStart}
          cefrLevel={cefrLevel}
          targetLanguage={practice?.targetLanguage ?? activeLanguage?.code}
          lessonId={practice?.id}
          grammarPracticeSessionId={practice?.grammarPracticeSessionId}
          situationId={practice?.situationId}
          situationStudyPlanId={practice?.situationStudyPlanId}
          lessonTitle={
            practice?.situationId
              ? tSituations(`items.${practice.situationId}.title`)
              : practice?.title
          }
          onSessionActiveChange={handleSessionActiveChange}
        />
      )}
    </MaintenanceGate>
  )
}
