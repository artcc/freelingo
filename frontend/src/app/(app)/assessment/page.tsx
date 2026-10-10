'use client'

import { useState, useEffect, useRef } from 'react'
import { useRouter } from 'next/navigation'
import { useLocale, useTranslations } from 'next-intl'
import { apiFetch, apiUrl } from '@/lib/api'
import { useLanguageStore, waitForLanguageSwitch } from '@/store/language'
import { isSubscribed, useAuthStore } from '@/store/auth'
import { useConfigStore } from '@/store/config'
import BeginnerGate from '@/components/assessment/BeginnerGate'
import AdaptiveQuizCard from '@/components/assessment/AdaptiveQuizCard'
import DurationSelector, {
  DURATION_OPTIONS,
  type DurationOption,
} from '@/components/assessment/DurationSelector'
import { type AssessmentQuestion, type CEFRLevel } from '@/data/types'
import { buildAnswerRecord, type AnswerRecord } from '@/lib/assessment-answers'
import { CEFR_LEVELS } from '@/data/curriculum'
import { ConfirmDialog } from '@/components/ui/confirm-dialog'
import { PageLoading } from '@/components/ui/page-loading'

// ── Types ──────────────────────────────────────────────────────────────────────

interface AssessmentResult {
  cefr_level: string
  score: number
  skill_profile: Record<string, number>
  strengths: string[]
  weaknesses: string[]
}

interface ExistingPlan {
  cefr_level: string
  created_at: string
}

interface VoiceTrialOffer {
  available: boolean
  token?: string
  duration_seconds?: number
}

interface AssessmentCompleteResponse {
  plan_id: number
  cefr_level: string
  voice_trial?: VoiceTrialOffer
}

interface AssessmentFlow {
  language: string
  sessionVersion: number
  controller: AbortController
  analyticsAttemptId?: string
  analyticsController?: AbortController
  evaluation?: {
    body: string
    pending: boolean
  }
  completionInvalidationVersion?: number
}

function isCurrentFlow(flow: AssessmentFlow | null): flow is AssessmentFlow {
  const context = useLanguageStore.getState()
  return (
    flow !== null &&
    !flow.controller.signal.aborted &&
    useAuthStore.getState().sessionVersion === flow.sessionVersion &&
    !context.isSwitching &&
    !context.needsRefresh &&
    context.activeLanguage?.code === flow.language
  )
}

type FlowStep =
  | 'checking'
  | 'existing'
  | 'beginner-gate'
  | 'quiz'
  | 'evaluation-error'
  | 'result'
  | 'duration'
  | 'voice-trial-offer'

// ── Constants ──────────────────────────────────────────────────────────────────

const MAX_QUESTIONS = 15
const CORRECT_STREAK_TO_UP = 2
const WRONG_STREAK_TO_DOWN = 2
const START_LEVEL: CEFRLevel = 'A2'

function pickNextQuestion(
  bank: AssessmentQuestion[],
  usedIds: Set<string>,
  currentLevel: CEFRLevel
): AssessmentQuestion | null {
  const available = bank.filter(
    (q) => !usedIds.has(q.id) && q.difficulty === currentLevel
  )
  if (available.length === 0) return null
  return available[Math.floor(Math.random() * available.length)]
}

function adjustLevel(current: CEFRLevel, direction: 'up' | 'down'): CEFRLevel {
  const idx = CEFR_LEVELS.indexOf(current)
  if (direction === 'up' && idx < CEFR_LEVELS.length - 1)
    return CEFR_LEVELS[idx + 1]
  if (direction === 'down' && idx > 0) return CEFR_LEVELS[idx - 1]
  return current
}

// ── Component ─────────────────────────────────────────────────────────────────

export default function AssessmentPage() {
  const t = useTranslations('assessment')
  const tCommon = useTranslations('common')
  const locale = useLocale()
  const router = useRouter()
  const activeLanguage = useLanguageStore((s) => s.activeLanguage)
  const needsRefresh = useLanguageStore((s) => s.needsRefresh)
  const invalidationVersion = useLanguageStore((s) => s.invalidationVersion)
  const isSwitching = useLanguageStore((s) => s.isSwitching)
  const fetchLanguages = useLanguageStore((s) => s.fetchLanguages)
  const user = useAuthStore((s) => s.user)
  const sessionVersion = useAuthStore((s) => s.sessionVersion)
  const stripeEnabled = useConfigStore((s) => s.stripeEnabled)
  const configLoaded = useConfigStore((s) => s.loaded)
  const loadConfig = useConfigStore((s) => s.load)

  const [step, setStep] = useState<FlowStep>('checking')
  const [existingPlan, setExistingPlan] = useState<ExistingPlan | null>(null)
  const [error, setError] = useState('')
  const [bank, setBank] = useState<AssessmentQuestion[]>([])
  const [contextError, setContextError] = useState(false)
  const [contextAttempt, setContextAttempt] = useState(0)
  const flowRef = useRef<AssessmentFlow | null>(null)
  const completedFlow = useRef<AssessmentFlow | null>(null)
  const mounted = useRef(false)

  useEffect(() => {
    mounted.current = true
    return () => {
      mounted.current = false
      flowRef.current?.controller.abort()
    }
  }, [])

  useEffect(
    () =>
      useConfigStore.subscribe((state) => {
        if (state.analyticsEnabled) return
        const flow = flowRef.current
        if (!flow) return
        // Observe disabling immediately, independently of the educational flow.
        flow.analyticsController?.abort()
        delete flow.analyticsController
        delete flow.analyticsAttemptId
      }),
    []
  )

  const [currentQuestion, setCurrentQuestion] =
    useState<AssessmentQuestion | null>(null)
  const [questionNumber, setQuestionNumber] = useState(0)
  const [answers, setAnswers] = useState<AnswerRecord[]>([])
  const [usedIds] = useState<Set<string>>(() => new Set())
  const [currentLevel, setCurrentLevel] = useState<CEFRLevel>(START_LEVEL)
  const [correctStreak, setCorrectStreak] = useState(0)
  const [wrongStreak, setWrongStreak] = useState(0)

  const [result, setResult] = useState<AssessmentResult | null>(null)
  const [selectedLevel, setSelectedLevel] = useState<CEFRLevel>('A1')
  const [evaluating, setEvaluating] = useState(false)

  const [durationOption, setDurationOption] = useState<DurationOption>(
    DURATION_OPTIONS[2]
  )
  const [selectedGoals, setSelectedGoals] = useState<string[]>([
    'grammar',
    'vocabulary',
  ])
  const [submitting, setSubmitting] = useState(false)
  const [trialLoading, setTrialLoading] = useState(false)
  const [createdPlanId, setCreatedPlanId] = useState<number | null>(null)
  const [voiceTrial, setVoiceTrial] = useState<VoiceTrialOffer | null>(null)

  // Warning dialog shown before the adaptive quiz starts
  const [showStartWarning, setShowStartWarning] = useState(false)

  useEffect(() => {
    void loadConfig()
  }, [loadConfig])

  useEffect(() => {
    // A committed assessment only needs summary recovery, never another assessment.
    if (
      completedFlow.current &&
      completedFlow.current === flowRef.current &&
      completedFlow.current.language === activeLanguage?.code &&
      completedFlow.current.sessionVersion === sessionVersion &&
      completedFlow.current.completionInvalidationVersion ===
        invalidationVersion
    )
      return
    flowRef.current?.controller.abort()
    completedFlow.current = null
    const controller = new AbortController()
    const flow: AssessmentFlow = {
      language: activeLanguage?.code ?? '',
      sessionVersion,
      controller,
    }
    flowRef.current = flow
    setStep('checking')
    setContextError(false)
    setError('')
    setBank([])
    setExistingPlan(null)
    setResult(null)
    setAnswers([])
    setCurrentQuestion(null)
    setShowStartWarning(false)
    setEvaluating(false)
    setSubmitting(false)
    setTrialLoading(false)
    setCreatedPlanId(null)
    setVoiceTrial(null)
    async function check() {
      try {
        if (useLanguageStore.getState().isSwitching) {
          await waitForLanguageSwitch(controller.signal)
        }
        if (controller.signal.aborted) return
        if (!flow.language || needsRefresh) {
          const ok = await fetchLanguages(controller.signal)
          if (controller.signal.aborted) return
          if (!ok || !useLanguageStore.getState().activeLanguage)
            setContextError(true)
          return
        }
        const signal = AbortSignal.any([
          controller.signal,
          AbortSignal.timeout(20_000),
        ])
        const [planRes, bankRes] = await Promise.all([
          apiFetch('/api/study-plan/current', { signal }),
          apiFetch(`/api/assessment/bank?language=${flow.language}`, {
            signal,
          }),
        ])
        if (!bankRes.ok || (!planRes.ok && planRes.status !== 404))
          throw new Error('Assessment context unavailable')
        const bankData = (await bankRes.json()) as {
          questions: AssessmentQuestion[]
        }
        const plan = planRes.ok
          ? ((await planRes.json()) as ExistingPlan | null)
          : null
        signal.throwIfAborted()
        await waitForLanguageSwitch(controller.signal)
        if (!isCurrentFlow(flow)) return
        setBank(bankData.questions)
        if (plan?.cefr_level) {
          setExistingPlan(plan)
          setStep('existing')
        } else {
          setStep('beginner-gate')
        }
      } catch {
        await waitForLanguageSwitch(controller.signal)
        if (
          !controller.signal.aborted &&
          useAuthStore.getState().sessionVersion === flow.sessionVersion
        )
          setContextError(true)
      }
    }
    void check()
    return () => {
      // Our own successful completion invalidates the summary, not this flow.
      // A later flow or unmount still cancels its outstanding continuation.
      if (completedFlow.current !== flow) controller.abort()
    }
  }, [
    activeLanguage?.code,
    needsRefresh,
    invalidationVersion,
    sessionVersion,
    fetchLanguages,
    contextAttempt,
  ])

  const canOfferVoiceTrial =
    configLoaded &&
    stripeEnabled &&
    user !== null &&
    !isSubscribed(user, stripeEnabled) &&
    !user.assessment_voice_trial_used

  function loadNextQuestion(
    level: CEFRLevel,
    usedSet: Set<string>,
    answersToSend: AnswerRecord[]
  ) {
    if (!isCurrentFlow(flowRef.current)) return
    const q = pickNextQuestion(bank, usedSet, level)
    if (q) {
      usedSet.add(q.id)
      setCurrentQuestion(q)
    } else {
      void evaluateQuiz(answersToSend)
    }
  }

  function startQuiz() {
    const flow = flowRef.current
    if (!isCurrentFlow(flow)) return
    if (bank.length === 0) {
      setError(tCommon('errorMessage'))
      return
    }
    usedIds.clear()
    setAnswers([])
    setCurrentLevel(START_LEVEL)
    setCorrectStreak(0)
    setWrongStreak(0)
    const q = pickNextQuestion(bank, usedIds, START_LEVEL)
    if (q) {
      usedIds.add(q.id)
      setCurrentQuestion(q)
      setQuestionNumber(1)
      setStep('quiz')
      if (
        useConfigStore.getState().analyticsEnabled &&
        !flow.analyticsAttemptId
      ) {
        try {
          const token = useAuthStore.getState().accessToken
          if (!token) return
          flow.analyticsAttemptId = crypto.randomUUID()
          flow.analyticsController = new AbortController()
          // Best-effort signal: analytics must not trigger auth refresh or page loading.
          void fetch(apiUrl('/api/assessment/started'), {
            method: 'POST',
            headers: {
              Authorization: `Bearer ${token}`,
              'X-Assessment-Attempt': flow.analyticsAttemptId,
            },
            signal: AbortSignal.any([
              flow.controller.signal,
              flow.analyticsController.signal,
              AbortSignal.timeout(5_000),
            ]),
          }).catch(() => {})
        } catch {
          // Unsupported browser APIs must not prevent starting the quiz.
        }
      }
    }
  }

  function handleAnswer(chosen: string) {
    const flow = flowRef.current
    if (!currentQuestion || !isCurrentFlow(flow)) return

    const record = buildAnswerRecord(currentQuestion, chosen)
    // A declared gap steers the quiz like a wrong answer — it removes the guess,
    // it does not add a penalty on top of it.
    const isCorrect = record.correct
    const newAnswers = [...answers, record]
    setAnswers(newAnswers)

    let newCorrect = correctStreak
    let newWrong = wrongStreak
    let newLevel = currentLevel

    if (isCorrect) {
      newCorrect += 1
      newWrong = 0
      if (newCorrect >= CORRECT_STREAK_TO_UP) {
        newLevel = adjustLevel(currentLevel, 'up')
        newCorrect = 0
      }
    } else {
      newWrong += 1
      newCorrect = 0
      if (newWrong >= WRONG_STREAK_TO_DOWN) {
        newLevel = adjustLevel(currentLevel, 'down')
        newWrong = 0
      }
    }

    setCorrectStreak(newCorrect)
    setWrongStreak(newWrong)

    if (newAnswers.length >= MAX_QUESTIONS) {
      void evaluateQuiz(newAnswers)
      return
    }

    setCurrentLevel(newLevel)
    setQuestionNumber((n) => n + 1)
    setTimeout(() => {
      void waitForLanguageSwitch(flow.controller.signal).then(() => {
        if (isCurrentFlow(flow)) loadNextQuestion(newLevel, usedIds, newAnswers)
      })
    }, 150)
  }

  async function evaluateQuiz(answersToSend?: AnswerRecord[]) {
    const flow = flowRef.current
    if (!isCurrentFlow(flow) || flow.evaluation?.pending) return
    // Keep the exact payload and synchronous request lock with their owning flow.
    const evaluation =
      flow.evaluation ??
      (answersToSend
        ? { body: JSON.stringify({ answers: answersToSend }), pending: false }
        : null)
    if (!evaluation) return
    flow.evaluation = evaluation
    evaluation.pending = true
    setError('')
    setEvaluating(true)
    setStep('quiz')
    setCurrentQuestion(null)
    try {
      const res = await apiFetch('/api/assessment/evaluate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(useConfigStore.getState().analyticsEnabled &&
          flow.analyticsAttemptId
            ? { 'X-Assessment-Attempt': flow.analyticsAttemptId }
            : {}),
        },
        body: evaluation.body,
        signal: flow.controller.signal,
      })
      if (!res.ok) throw new Error(tCommon('errorMessage'))
      const data = (await res.json()) as AssessmentResult
      await waitForLanguageSwitch(flow.controller.signal)
      if (!isCurrentFlow(flow)) return
      setResult(data)
      setSelectedLevel(data.cefr_level as CEFRLevel)
      setStep('result')
    } catch {
      await waitForLanguageSwitch(flow.controller.signal)
      if (isCurrentFlow(flow)) {
        setError(tCommon('errorMessage'))
        setStep('evaluation-error')
      }
    } finally {
      evaluation.pending = false
      if (isCurrentFlow(flow)) setEvaluating(false)
    }
  }

  async function handleComplete() {
    const flow = flowRef.current
    if (!result || submitting || !isCurrentFlow(flow)) return
    setSubmitting(true)
    setError('')
    const ownsCompletion = () =>
      mounted.current &&
      !flow.controller.signal.aborted &&
      flowRef.current === flow &&
      completedFlow.current === flow &&
      flow.completionInvalidationVersion ===
        useLanguageStore.getState().invalidationVersion &&
      useAuthStore.getState().sessionVersion === flow.sessionVersion &&
      !useLanguageStore.getState().isSwitching &&
      useLanguageStore.getState().activeLanguage?.code === flow.language
    try {
      const res = await apiFetch('/api/assessment/complete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          cefr_level: selectedLevel,
          skill_profile: result.skill_profile,
          strengths: result.strengths,
          weaknesses: result.weaknesses,
          duration_weeks: durationOption.weeks,
          days_per_week: durationOption.daysPerWeek,
          goals: selectedGoals,
          // Explicit target_language prevents /complete from relying on the
          // potentially-stale users.target_language column when the user is
          // completing assessment for a newly added language.
          target_language: flow.language,
        }),
        // Observe the mutation even after its visual flow is abandoned: the
        // server may already have replaced the user's active plan.
      })
      if (!res.ok) throw new Error(tCommon('errorMessage'))
      if (useAuthStore.getState().sessionVersion !== flow.sessionVersion) return
      const context = useLanguageStore.getState()
      // Only the surviving flow may claim this as its own invalidation. A
      // provisional switch can still be rejected, so keep that flow suspended.
      if (
        mounted.current &&
        !flow.controller.signal.aborted &&
        flowRef.current === flow &&
        !context.needsRefresh &&
        context.activeLanguage?.code === flow.language
      ) {
        completedFlow.current = flow
        flow.completionInvalidationVersion = context.invalidationVersion + 1
      }
      // HTTP success confirms persistence. Reconcile globally before decoding
      // the body, independent of unmount, language changes or body failure.
      context.invalidateLanguages()
      const reconciliation = context.fetchLanguages()
      const data = (await res.json()) as AssessmentCompleteResponse
      await reconciliation
      await waitForLanguageSwitch(flow.controller.signal)
      if (!ownsCompletion()) return
      setCreatedPlanId(data.plan_id)
      if (data.voice_trial?.available && data.voice_trial.token) {
        setVoiceTrial(data.voice_trial)
        setStep('voice-trial-offer')
        setContextError(useLanguageStore.getState().needsRefresh)
        setSubmitting(false)
        return
      }
      router.push('/plan')
    } catch {
      await waitForLanguageSwitch(flow.controller.signal)
      if (ownsCompletion()) {
        // The plan was committed but its response body was unreadable. Recover
        // the existing plan through GET rather than enabling another completion.
        completedFlow.current = null
        setContextAttempt((value) => value + 1)
        return
      }
      if (isCurrentFlow(flow)) {
        setError(tCommon('errorMessage'))
        setSubmitting(false)
      }
    }
  }

  function startVoiceTrial() {
    if (!voiceTrial?.token) return
    const flow = flowRef.current
    if (!isCurrentFlow(flow)) return
    sessionStorage.setItem(
      'assessment_voice_trial',
      JSON.stringify({
        token: voiceTrial.token,
        durationSeconds: voiceTrial.duration_seconds ?? 300,
        cefrLevel: selectedLevel,
        planId: createdPlanId,
        targetLanguage: flow.language,
      })
    )
    router.push('/conversation')
  }

  async function requestVoiceTrial() {
    const flow = flowRef.current
    if (!existingPlan || !isCurrentFlow(flow)) return
    setTrialLoading(true)
    setError('')
    try {
      const res = await apiFetch('/api/assessment/voice-trial', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ target_language: flow.language }),
        signal: flow.controller.signal,
      })
      if (!res.ok) throw new Error(tCommon('errorMessage'))
      const data = (await res.json()) as AssessmentCompleteResponse
      await waitForLanguageSwitch(flow.controller.signal)
      if (!isCurrentFlow(flow)) return
      if (data.voice_trial?.available && data.voice_trial.token) {
        setCreatedPlanId(data.plan_id)
        setSelectedLevel(data.cefr_level as CEFRLevel)
        setVoiceTrial(data.voice_trial)
        setStep('voice-trial-offer')
        return
      }
      setError(tCommon('errorMessage'))
    } catch {
      await waitForLanguageSwitch(flow.controller.signal)
      if (isCurrentFlow(flow)) setError(tCommon('errorMessage'))
    } finally {
      if (isCurrentFlow(flow)) setTrialLoading(false)
    }
  }

  // ── Loading ────────────────────────────────────────────────────────────────
  if (isSwitching) return <PageLoading label={tCommon('loading')} />
  if (contextError)
    return (
      <div className="mx-auto max-w-md space-y-4 p-6 text-center">
        <p role="alert" className="text-fl-muted-1">
          {tCommon('errorMessage')}
        </p>
        <button
          className="border-fl-border text-fl-fg hover:bg-fl-surface-2 border px-4 py-2 text-sm"
          disabled={submitting}
          onClick={async () => {
            const flow = completedFlow.current
            if (!flow) {
              setContextError(false)
              setContextAttempt((value) => value + 1)
              return
            }
            // Recover a committed completion's own summary without another POST.
            setSubmitting(true)
            const ok = await fetchLanguages(flow.controller.signal)
            if (
              flow.controller.signal.aborted ||
              completedFlow.current !== flow ||
              useAuthStore.getState().sessionVersion !== flow.sessionVersion ||
              flow.completionInvalidationVersion !==
                useLanguageStore.getState().invalidationVersion
            )
              return
            setContextError(!ok)
            setSubmitting(false)
          }}
        >
          {tCommon('retry')}
        </button>
      </div>
    )
  if (
    step === 'checking' ||
    (step === 'quiz' && (evaluating || !currentQuestion))
  ) {
    return (
      <PageLoading label={evaluating ? t('evaluating') : tCommon('loading')} />
    )
  }

  if (step === 'evaluation-error') {
    return (
      <div className="mx-auto max-w-md space-y-4 p-6 text-center">
        <p role="alert" className="text-fl-muted-1">
          {error}
        </p>
        <button
          className="border-fl-border text-fl-fg hover:bg-fl-surface-2 border px-4 py-2 text-sm"
          onClick={() => void evaluateQuiz()}
        >
          {tCommon('retry')}
        </button>
      </div>
    )
  }

  // ── Existing plan ─────────────────────────────────────────────────────────
  if (step === 'existing' && existingPlan) {
    const assessedDate = new Date(existingPlan.created_at).toLocaleDateString(
      locale,
      {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      }
    )
    return (
      <div className="flex min-h-[60vh] items-center justify-center p-6">
        <div className="border-fl-border bg-fl-surface w-full max-w-md border">
          <div className="border-fl-border flex items-center gap-2 border-b px-6 py-4">
            <span className="text-fl-label text-fl-muted-3">●</span>
            <span className="text-fl-label text-fl-muted-2 font-mono tracking-widest uppercase">
              {t('title')}
            </span>
          </div>
          <div className="space-y-6 p-8 text-center">
            <div>
              <p className="text-fl-label text-fl-muted-3 mb-2 font-mono tracking-widest uppercase">
                {t('currentLevel')}
              </p>
              <p className="text-fl-fg font-mono text-6xl font-bold tracking-widest">
                {existingPlan.cefr_level}
              </p>
            </div>
            <div className="border-fl-border border py-3">
              <p className="text-fl-label text-fl-muted-3 font-mono tracking-widest uppercase">
                {t('assessedOn')}
              </p>
              <p className="text-fl-muted-1 mt-1 font-mono text-xs">
                {assessedDate}
              </p>
            </div>
            <p className="text-fl-label text-fl-muted-3 font-mono leading-relaxed">
              {t('alreadyHasPlan')}
            </p>
            {canOfferVoiceTrial && (
              <div className="border-fl-border bg-fl-surface-2 space-y-3 border px-4 py-5">
                <p className="text-fl-fg font-mono text-sm font-bold">
                  {t('voiceTrialTitle')}
                </p>
                <p className="text-fl-muted-1 font-mono text-xs leading-relaxed">
                  {t('voiceTrialDesc', { minutes: 5 })}
                </p>
                <button
                  onClick={requestVoiceTrial}
                  disabled={trialLoading}
                  className="bg-fl-accent text-fl-accent-fg hover:bg-fl-accent/90 w-full py-3 font-mono text-sm font-bold tracking-widest uppercase transition-colors disabled:opacity-50"
                >
                  {trialLoading ? '...' : `${t('voiceTrialStart')} →`}
                </button>
              </div>
            )}
            {error && (
              <div className="border-fl-error/40 text-fl-error-fg border px-4 py-3 font-mono text-xs">
                ✕ {error}
              </div>
            )}
            <div className="flex gap-2">
              <button
                onClick={() => router.push('/dashboard')}
                className="border-fl-border text-fl-muted-2 hover:border-fl-border-2 hover:text-fl-fg flex-1 border px-3 py-3 font-mono text-xs tracking-widest uppercase transition-colors"
              >
                ← {tCommon('backToDashboard')}
              </button>
              <button
                onClick={() => setStep('beginner-gate')}
                className="bg-fl-accent text-fl-accent-fg hover:bg-fl-accent/90 flex-[1.75] px-3 py-3 font-mono text-sm font-bold tracking-widest uppercase transition-colors"
              >
                {t('retake')}
              </button>
            </div>
          </div>
        </div>
      </div>
    )
  }

  // ── BeginnerGate ──────────────────────────────────────────────────────────
  if (step === 'beginner-gate') {
    return (
      <>
        <BeginnerGate
          languageCode={activeLanguage?.iso639 ?? ''}
          onBeginner={() => {
            if (!isCurrentFlow(flowRef.current)) return
            setResult({
              cefr_level: 'A1',
              score: 0,
              skill_profile: {},
              strengths: [],
              weaknesses: [],
            })
            setSelectedLevel('A1')
            setAnswers([])
            setStep('duration')
          }}
          onHasExperience={() => setShowStartWarning(true)}
        />
        <ConfirmDialog
          open={showStartWarning}
          title={t('startWarningTitle')}
          message={t('startWarningMessage')}
          confirmLabel={t('startWarningConfirm')}
          onConfirm={() => {
            setShowStartWarning(false)
            startQuiz()
          }}
          onCancel={() => setShowStartWarning(false)}
        />
      </>
    )
  }

  // ── Quiz ──────────────────────────────────────────────────────────────────
  if (step === 'quiz' && currentQuestion) {
    return (
      <AdaptiveQuizCard
        question={currentQuestion}
        questionNumber={questionNumber}
        totalQuestions={MAX_QUESTIONS}
        onAnswer={handleAnswer}
        languageCode={activeLanguage?.code}
      />
    )
  }

  // ── Result ────────────────────────────────────────────────────────────────
  if (step === 'result' && result) {
    const score = Math.round(result.score * 100)
    const aiLevel = result.cefr_level
    const levelChanged = selectedLevel !== aiLevel
    return (
      <div className="flex min-h-[60vh] items-center justify-center p-6">
        <div className="border-fl-border bg-fl-surface w-full max-w-md border">
          <div className="border-fl-border flex items-center gap-2 border-b px-6 py-4">
            <span className="text-fl-label text-fl-muted-3">●</span>
            <span className="text-fl-label text-fl-muted-2 font-mono tracking-widest uppercase">
              {t('resultStep')}
            </span>
          </div>
          <div className="space-y-6 p-8 text-center">
            <div>
              <p className="text-fl-label text-fl-muted-3 mb-2 font-mono tracking-widest uppercase">
                {t('cefrLevel')}
              </p>
              <p className="text-fl-fg font-mono text-6xl font-bold tracking-widest">
                {aiLevel}
              </p>
            </div>
            <div className="border-fl-border border py-3">
              <p className="text-fl-label text-fl-muted-3 font-mono tracking-widest uppercase">
                {tCommon('score')}
              </p>
              <p className="text-fl-fg-2 mt-1 font-mono text-2xl">{score}%</p>
            </div>
            <div>
              <p className="text-fl-hint text-fl-muted-3 mb-2 font-mono tracking-widest uppercase">
                {t('overrideLevel')}
              </p>
              <div className="flex flex-wrap justify-center gap-1">
                {CEFR_LEVELS.map((lvl) => (
                  <button
                    key={lvl}
                    onClick={() => setSelectedLevel(lvl)}
                    className={`border px-3 py-1.5 font-mono text-xs font-bold tracking-widest transition-colors ${
                      selectedLevel === lvl
                        ? 'bg-fl-accent text-fl-accent-fg border-fl-accent'
                        : 'border-fl-border text-fl-muted-2 hover:border-fl-border-2 hover:text-fl-fg'
                    }`}
                  >
                    {lvl}
                  </button>
                ))}
              </div>
              {levelChanged && (
                <p className="text-fl-hint text-fl-muted-1 mt-2 font-mono">
                  {t('suggestedLevel', { aiLevel, selectedLevel })}
                </p>
              )}
            </div>
            {result.strengths.length > 0 && (
              <div>
                <p className="text-fl-hint text-fl-muted-3 mb-2 font-mono tracking-widest uppercase">
                  {t('strengths')}
                </p>
                <div className="flex flex-wrap justify-center gap-1">
                  {result.strengths.map((s) => (
                    <span
                      key={s}
                      className="border-fl-border text-fl-label text-fl-muted-1 border px-3 py-1 font-mono tracking-widest uppercase"
                    >
                      {s}
                    </span>
                  ))}
                </div>
              </div>
            )}
            {result.weaknesses.length > 0 && (
              <div>
                <p className="text-fl-hint text-fl-muted-3 mb-2 font-mono tracking-widest uppercase">
                  {t('needsWork')}
                </p>
                <div className="flex flex-wrap justify-center gap-1">
                  {result.weaknesses.map((w) => (
                    <span
                      key={w}
                      className="border-fl-error/30 text-fl-label text-fl-error-dim border px-3 py-1 font-mono tracking-widest uppercase"
                    >
                      {w}
                    </span>
                  ))}
                </div>
              </div>
            )}
            {error && (
              <div className="border-fl-error/40 text-fl-error-fg border px-4 py-3 font-mono text-xs">
                ✕ {error}
              </div>
            )}
            <button
              onClick={() => setStep('duration')}
              className="bg-fl-accent text-fl-accent-fg hover:bg-fl-accent/90 w-full py-3 font-mono text-sm font-bold tracking-widest uppercase transition-colors"
            >
              {t('createPlan')} →
            </button>
          </div>
        </div>
      </div>
    )
  }

  // ── Duration + goals ──────────────────────────────────────────────────────
  if (step === 'duration') {
    return (
      <DurationSelector
        selectedWeeks={durationOption.weeks}
        selectedGoals={selectedGoals}
        onSelectDuration={setDurationOption}
        onToggleGoal={(goal) =>
          setSelectedGoals((prev) =>
            prev.includes(goal)
              ? prev.filter((g) => g !== goal)
              : [...prev, goal]
          )
        }
        onConfirm={handleComplete}
        onBack={() => {
          const isBeginner =
            result?.score === 0 &&
            result?.cefr_level === 'A1' &&
            answers.length === 0
          setStep(isBeginner ? 'beginner-gate' : 'result')
        }}
        cefr_level={selectedLevel}
        loading={submitting}
      />
    )
  }

  // ── Voice trial offer ─────────────────────────────────────────────────────
  if (step === 'voice-trial-offer') {
    const minutes = Math.round((voiceTrial?.duration_seconds ?? 300) / 60)
    return (
      <div className="flex min-h-[60vh] items-center justify-center p-6">
        <div className="border-fl-border bg-fl-surface w-full max-w-md border">
          <div className="border-fl-border flex items-center gap-2 border-b px-6 py-4">
            <span className="text-fl-label text-fl-muted-3">●</span>
            <span className="text-fl-label text-fl-muted-2 font-mono tracking-widest uppercase">
              {t('voiceTrialLabel')}
            </span>
          </div>
          <div className="space-y-6 p-8 text-center">
            <div>
              <p className="text-fl-label text-fl-muted-3 mb-2 font-mono tracking-widest uppercase">
                {t('cefrLevel')}
              </p>
              <p className="text-fl-fg font-mono text-6xl font-bold tracking-widest">
                {selectedLevel}
              </p>
            </div>
            <div className="border-fl-border bg-fl-surface-2 border px-4 py-5">
              <p className="text-fl-fg mb-2 font-mono text-base font-bold">
                {t('voiceTrialTitle')}
              </p>
              <p className="text-fl-muted-1 font-mono text-xs leading-relaxed">
                {t('voiceTrialDesc', { minutes })}
              </p>
            </div>
            <button
              onClick={startVoiceTrial}
              className="bg-fl-accent text-fl-accent-fg hover:bg-fl-accent/90 w-full py-3 font-mono text-sm font-bold tracking-widest uppercase transition-colors"
            >
              {t('voiceTrialStart')} →
            </button>
            <button
              onClick={() => router.push('/plan')}
              className="text-fl-hint text-fl-muted-4 hover:text-fl-muted-2 w-full font-mono tracking-widest uppercase transition-colors"
            >
              {t('voiceTrialSkip')}
            </button>
          </div>
        </div>
      </div>
    )
  }

  return null
}
