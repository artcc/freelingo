'use client'

import { useEffect, useId, useRef, useState } from 'react'
import { useTranslations } from 'next-intl'
import { apiFetch } from '@/lib/api'
import { useAuthStore } from '@/store/auth'

interface QuestionTranslationProps {
  exerciseId: number
  question: string
  nativeLanguage: string
  nativeLanguageName: string
  translation?: string | null
  translationLanguage?: string | null
}

// The parent keys this component by exercise/source, language and authentication session.
export function QuestionTranslation({
  exerciseId,
  question,
  nativeLanguage,
  nativeLanguageName,
  translation,
  translationLanguage,
}: QuestionTranslationProps) {
  const t = useTranslations('lesson')
  const contentId = useId()
  const [open, setOpen] = useState(false)
  const [text, setText] = useState(
    translationLanguage === nativeLanguage ? translation?.trim() || null : null
  )
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(false)
  const requestRef = useRef<AbortController | null>(null)

  useEffect(() => () => requestRef.current?.abort(), [])

  async function translate() {
    if (requestRef.current) return
    const controller = new AbortController()
    requestRef.current = controller
    const sessionVersion = useAuthStore.getState().sessionVersion
    const isCurrent = () => {
      const auth = useAuthStore.getState()
      return (
        !controller.signal.aborted &&
        auth.sessionVersion === sessionVersion &&
        auth.user?.native_language === nativeLanguage
      )
    }
    setLoading(true)
    setError(false)
    try {
      const response = await apiFetch(
        `/api/lessons/exercises/${exerciseId}/question-translation`,
        {
          method: 'POST',
          signal: AbortSignal.any([
            controller.signal,
            AbortSignal.timeout(30_000),
          ]),
        }
      )
      if (!response.ok) throw new Error('Question translation unavailable')
      const data = await response.json()
      if (!isCurrent()) return
      if (
        data.question !== question ||
        data.question_translation_language !== nativeLanguage ||
        typeof data.question_translation !== 'string' ||
        !data.question_translation.trim()
      ) {
        throw new Error('Question translation does not match its context')
      }
      setText(data.question_translation.trim())
    } catch {
      if (isCurrent()) setError(true)
    } finally {
      if (isCurrent()) setLoading(false)
      if (requestRef.current === controller) requestRef.current = null
    }
  }

  function toggle() {
    setOpen(!open)
    if (!open && !text) void translate()
  }

  return (
    <div className="border-fl-border bg-fl-bg border px-4 py-3">
      <button
        type="button"
        onClick={toggle}
        aria-expanded={open}
        aria-controls={contentId}
        className="text-fl-muted-1 hover:text-fl-fg focus-visible:outline-fl-fg text-sm underline underline-offset-4 transition-colors focus-visible:outline-2 focus-visible:outline-offset-2"
      >
        {open
          ? t('hideQuestionTranslation')
          : t('showQuestionTranslation', { language: nativeLanguageName })}
      </button>
      <div id={contentId} hidden={!open} aria-live="polite" aria-busy={loading}>
        {loading && (
          <p role="status" className="text-fl-muted-2 mt-3 text-sm">
            {t('translatingQuestion')}
          </p>
        )}
        {error && (
          <div className="mt-3 space-y-2">
            <p role="alert" className="text-fl-error text-sm">
              {t('questionTranslationError')}
            </p>
            <button
              type="button"
              onClick={() => void translate()}
              className="text-fl-muted-1 hover:text-fl-fg focus-visible:outline-fl-fg text-sm underline underline-offset-4 focus-visible:outline-2 focus-visible:outline-offset-2"
            >
              {t('retryQuestionTranslation')}
            </button>
          </div>
        )}
        {text && (
          <p
            lang={nativeLanguage}
            dir="auto"
            className="text-fl-muted-1 mt-3 max-w-[70ch] text-base leading-relaxed whitespace-pre-wrap"
          >
            {text}
          </p>
        )}
      </div>
    </div>
  )
}
