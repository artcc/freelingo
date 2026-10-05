/**
 * /conversation — Voice conversation page.
 *
 * ConversationMode uses @ricky0123/vad-react (ONNX/WASM) and the Web Audio
 * API, neither of which are compatible with SSR. It is loaded client-side only
 * via `dynamic({ ssr: false })`.
 */
'use client'

import { useEffect, useState } from 'react'
import { useSearchParams } from 'next/navigation'
import { useTranslations } from 'next-intl'
import Link from 'next/link'
import dynamic from 'next/dynamic'
import type { ChatContextItem } from '@/lib/conversation-ws'
import { PageLoading } from '@/components/ui/page-loading'
import { FreemiumQuotaBanner } from '@/components/billing/FreemiumQuotaBanner'
import { PaywallBanner } from '@/components/billing/PaywallBanner'
import { MaintenanceGate } from '@/components/billing/MaintenanceBanner'
import { apiFetch } from '@/lib/api'
import { useLanguageStore } from '@/store/language'
import { useConfigStore } from '@/store/config'
import { useAuthStore, isSubscribed, isFreemiumTrialActive } from '@/store/auth'
import { useFreemiumStore } from '@/store/freemium'

function ConversationLoading() {
  return <PageLoading minHeight="min-h-[calc(100vh-56px)] md:min-h-screen" />
}

const ConversationMode = dynamic(
  () => import('@/components/conversation/ConversationMode'),
  {
    ssr: false,
    loading: ConversationLoading,
  }
)

interface LessonPractice {
  id: number
  title: string
  cefrLevel: string
  targetLanguage: string
}

export default function ConversationPage() {
  const searchParams = useSearchParams()
  const lessonId = searchParams.get('lesson')
  return lessonId !== null ? (
    <LessonConversationPage key={lessonId} lessonId={lessonId} />
  ) : (
    <ConversationPageContent />
  )
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
        if (!/^\d+$/.test(lessonId) || !Number.isSafeInteger(id) || id <= 0) {
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
  const activeLanguage = useLanguageStore((s) => s.activeLanguage)
  const stripeEnabled = useConfigStore((s) => s.stripeEnabled)
  const user = useAuthStore((s) => s.user)
  const fetchFreemium = useFreemiumStore((s) => s.fetchStatus)
  const freemiumStatus = useFreemiumStore((s) => s.status)
  const freemiumExhausted =
    stripeEnabled &&
    !isSubscribed(user, stripeEnabled) &&
    !isFreemiumTrialActive(user, stripeEnabled) &&
    freemiumStatus &&
    freemiumStatus.voice_remaining_seconds <= 0

  const freemiumVoiceRemaining = freemiumStatus
    ? Math.ceil(freemiumStatus.voice_remaining_seconds / 60)
    : undefined
  const freemiumVoiceLimit = freemiumStatus
    ? Math.ceil(freemiumStatus.voice_limit_seconds / 60)
    : undefined
  const showFreemiumVoicePill =
    stripeEnabled &&
    !isSubscribed(user, stripeEnabled) &&
    !isFreemiumTrialActive(user, stripeEnabled) &&
    freemiumStatus &&
    freemiumStatus.voice_limit_seconds > 0

  const [initialContext, setInitialContext] = useState<
    ChatContextItem[] | undefined
  >(undefined)
  const [autoStart, setAutoStart] = useState(!!practice)
  const [cefrLevel, setCefrLevel] = useState<string | null>(
    practice?.cefrLevel ?? null
  )
  const [planReady, setPlanReady] = useState(!!practice)
  const [voiceTrial, setVoiceTrial] = useState<{
    token: string
    durationSeconds: number
    cefrLevel?: string
    targetLanguage?: string
  } | null>(null)

  useEffect(() => {
    if (stripeEnabled && !isSubscribed(user, stripeEnabled)) {
      fetchFreemium()
    }
  }, [stripeEnabled, user, fetchFreemium])

  useEffect(() => {
    if (practice) return
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
              typeof parsed.durationSeconds === 'number'
                ? parsed.durationSeconds
                : 300,
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
    apiFetch('/api/study-plan/today')
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => {
        if (data?.cefr_level) setCefrLevel(data.cefr_level)
      })
      .catch(() => {
        /* sin plan — usa default 1500ms */
      })
      .finally(() => setPlanReady(true))
  }, [activeLanguage?.code, practice])

  if (!planReady) return null

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
      ) : freemiumExhausted ? (
        <>
          <FreemiumQuotaBanner feature="voice" className="mb-4" />
          <PaywallBanner feature="voice" compact />
        </>
      ) : (
        <ConversationMode
          initialContext={initialContext}
          autoStart={autoStart}
          cefrLevel={cefrLevel}
          targetLanguage={practice?.targetLanguage ?? activeLanguage?.code}
          lessonId={practice?.id}
          lessonTitle={practice?.title}
          freemiumVoiceRemaining={
            showFreemiumVoicePill ? freemiumVoiceRemaining : undefined
          }
          freemiumVoiceLimit={
            showFreemiumVoicePill ? freemiumVoiceLimit : undefined
          }
        />
      )}
    </MaintenanceGate>
  )
}
