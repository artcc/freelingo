'use client'

import { useId, useLayoutEffect, useRef, useState } from 'react'
import { useLocale, useTranslations } from 'next-intl'
import { TargetLanguageText } from '@/components/TargetLanguageText'
import { apiFetch } from '@/lib/api'
import type { ExerciseContext } from '@/lib/exercise-generation'
import { formatLanguageName } from '@/lib/target-languages'
import { useAuthStore } from '@/store/auth'
import { useLanguageStore } from '@/store/language'

interface QuestionExplanationProps {
  feature: 'reading' | 'listening'
  attemptId: number
  questionIndex: number
  sourceText: string
  context: ExerciseContext
  sessionVersion: number
}

interface Explanation {
  explanation: string
  evidence: string
  native_language: string
  target_language: string
}

function matchesContext(context: ExerciseContext) {
  const language = useLanguageStore.getState()
  const plan = language.userLanguages.find((item) => item.is_active)?.plan
  return (
    !language.isSwitching &&
    !language.needsRefresh &&
    language.activeLanguage?.code === context.target_language &&
    plan?.id === context.study_plan_id &&
    plan?.cefr_level === context.level
  )
}

export function QuestionExplanation(props: QuestionExplanationProps) {
  const user = useAuthStore((state) => state.user)
  const sessionVersion = useAuthStore((state) => state.sessionVersion)
  const activeLanguage = useLanguageStore((state) => state.activeLanguage)
  const userLanguages = useLanguageStore((state) => state.userLanguages)
  const isSwitching = useLanguageStore((state) => state.isSwitching)
  const needsRefresh = useLanguageStore((state) => state.needsRefresh)
  const plan = userLanguages.find((item) => item.is_active)?.plan

  if (
    !user?.native_language ||
    sessionVersion !== props.sessionVersion ||
    isSwitching ||
    needsRefresh ||
    activeLanguage?.code !== props.context.target_language ||
    plan?.id !== props.context.study_plan_id ||
    plan?.cefr_level !== props.context.level ||
    !Number.isInteger(props.attemptId) ||
    props.attemptId <= 0
  )
    return null

  // Remount before painting a different attempt, profile language or study context.
  const key = JSON.stringify([
    props.feature,
    props.attemptId,
    props.questionIndex,
    props.sourceText,
    props.context.study_plan_id,
    props.context.target_language,
    props.context.level,
    sessionVersion,
    user.id,
    user.native_language,
  ])
  return (
    <ExplanationContent
      key={key}
      {...props}
      userId={user.id}
      nativeLanguage={user.native_language}
    />
  )
}

function ExplanationContent({
  feature,
  attemptId,
  questionIndex,
  sourceText,
  context,
  sessionVersion,
  userId,
  nativeLanguage,
}: QuestionExplanationProps & { userId: number; nativeLanguage: string }) {
  const t = useTranslations('questionExplanation')
  const tCommon = useTranslations('common')
  const tLanguage = useTranslations('languages')
  const locale = useLocale()
  const contentId = useId()
  const [open, setOpen] = useState(false)
  const [data, setData] = useState<Explanation | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(false)
  const request = useRef<AbortController | null>(null)

  const {
    study_plan_id: studyPlanId,
    target_language: targetLanguage,
    level,
  } = context
  useLayoutEffect(() => {
    // Store notifications also catch changes that React batches before a render.
    const invalidate = () => {
      const auth = useAuthStore.getState()
      if (
        auth.sessionVersion === sessionVersion &&
        auth.user?.id === userId &&
        auth.user.native_language === nativeLanguage &&
        matchesContext({
          study_plan_id: studyPlanId,
          target_language: targetLanguage,
          level,
        })
      )
        return
      request.current?.abort()
      request.current = null
      setOpen(false)
      setData(null)
      setLoading(false)
      setError(false)
    }
    const unsubscribeAuth = useAuthStore.subscribe(invalidate)
    const unsubscribeLanguage = useLanguageStore.subscribe(invalidate)
    return () => {
      unsubscribeAuth()
      unsubscribeLanguage()
      request.current?.abort()
    }
  }, [
    studyPlanId,
    targetLanguage,
    level,
    nativeLanguage,
    sessionVersion,
    userId,
  ])

  async function explain() {
    if (request.current) return
    const controller = new AbortController()
    const current = () => {
      const auth = useAuthStore.getState()
      return (
        !controller.signal.aborted &&
        auth.sessionVersion === sessionVersion &&
        auth.user?.id === userId &&
        auth.user.native_language === nativeLanguage &&
        matchesContext(context)
      )
    }
    if (!current()) return
    request.current = controller
    setLoading(true)
    setError(false)
    try {
      const response = await apiFetch(
        `/api/${feature}/attempts/${attemptId}/questions/${questionIndex}/explanation`,
        {
          method: 'POST',
          signal: AbortSignal.any([
            controller.signal,
            AbortSignal.timeout(30_000),
          ]),
        }
      )
      if (!response.ok) throw new Error('Question explanation unavailable')
      const explanation = (await response.json()) as Explanation
      if (!current()) return
      if (
        explanation.native_language !== nativeLanguage ||
        explanation.target_language !== context.target_language ||
        typeof explanation.explanation !== 'string' ||
        !explanation.explanation.trim() ||
        typeof explanation.evidence !== 'string' ||
        !explanation.evidence.trim() ||
        !sourceText.includes(explanation.evidence)
      ) {
        throw new Error('Question explanation does not match its context')
      }
      setData(explanation)
    } catch {
      if (current()) setError(true)
    } finally {
      if (current()) setLoading(false)
      if (request.current === controller) request.current = null
    }
  }

  return (
    <div className="border-fl-border mt-3 border-t pt-3">
      <button
        type="button"
        aria-expanded={open}
        aria-controls={contentId}
        onClick={() => {
          setOpen(!open)
          if (!open && !data) void explain()
        }}
        className="text-fl-muted-1 hover:text-fl-fg focus-visible:outline-fl-fg text-sm underline underline-offset-4 transition-colors focus-visible:outline-2 focus-visible:outline-offset-2"
      >
        {open ? t('hide') : t('show')}
      </button>
      <div id={contentId} hidden={!open} aria-live="polite" aria-busy={loading}>
        {loading && (
          <p role="status" className="text-fl-muted-2 mt-3 text-sm">
            {t('loading')}
          </p>
        )}
        {error && (
          <div className="mt-3 space-y-2">
            <p role="alert" className="text-fl-error-fg text-sm">
              {t('error')}
            </p>
            <button
              type="button"
              onClick={() => void explain()}
              className="text-fl-muted-1 hover:text-fl-fg focus-visible:outline-fl-fg text-sm underline underline-offset-4 focus-visible:outline-2 focus-visible:outline-offset-2"
            >
              {tCommon('retry')}
            </button>
          </div>
        )}
        {data && (
          <div className="mt-3 space-y-3">
            <div>
              <p className="text-fl-label text-fl-muted-3 mb-1 font-mono tracking-widest uppercase">
                {t('evidence')}
              </p>
              <TargetLanguageText
                as="blockquote"
                languageCode={data.target_language}
                className="border-fl-border text-fl-fg max-w-[70ch] border-l-2 pl-3 whitespace-pre-wrap"
              >
                {data.evidence}
              </TargetLanguageText>
            </div>
            <div>
              <p className="text-fl-label text-fl-muted-3 mb-1 font-mono tracking-widest uppercase">
                {t('language', {
                  language: formatLanguageName(
                    tLanguage(nativeLanguage),
                    locale
                  ),
                })}
              </p>
              <p
                lang={nativeLanguage}
                dir="auto"
                className="text-fl-muted-1 max-w-[70ch] font-sans text-base leading-relaxed whitespace-pre-wrap"
              >
                {data.explanation}
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
