'use client'

import { useEffect, useRef, useState, useCallback } from 'react'
import Link from 'next/link'
import { useTranslations } from 'next-intl'
import {
  BookOpen,
  Check,
  ChevronDown,
  Clock,
  Layers,
  Mic,
  Plus,
  RotateCcw,
  Sparkles,
} from 'lucide-react'
import { apiFetch } from '@/lib/api'
import { AudioPlayer } from '@/components/ui/AudioPlayer'
import { PageLoading } from '@/components/ui/page-loading'
import { TargetLanguageText } from '@/components/TargetLanguageText'
import { CEFR_LEVELS } from '@/data/curriculum'
import { trackBrowserEvent } from '@/lib/analytics'
import { useAuthStore } from '@/store/auth'
import {
  FlashcardBoundary,
  FlashcardError,
  useFlashcardScope,
} from '@/components/flashcards/FlashcardBoundary'
import { FlashcardActions } from '@/components/flashcards/FlashcardActions'
import { PremiumResultOffer } from '@/components/billing/PremiumResultOffer'
import {
  BackPreference,
  useBackPreference,
} from '@/components/flashcards/BackPreference'
import { SpeakingCard } from '@/components/flashcards/SpeakingCard'
import type { Flashcard } from '@/components/flashcards/types'
import NoPlanBanner from '@/components/plan/NoPlanBanner'

interface ReviewResult {
  id: number
  word: string
  quality: number
  xp: number
}

const isNewCard = (card: Flashcard) =>
  card.interval === 0 && card.repetitions === 0

export default function FlashcardsPage() {
  return (
    <FlashcardBoundary>
      {(code) => <FlashcardsContent targetLanguageCode={code} />}
    </FlashcardBoundary>
  )
}

function FlashcardsContent({
  targetLanguageCode,
}: {
  targetLanguageCode: string
}) {
  const t = useTranslations('flashcards')
  const tCommon = useTranslations('common')
  const isCurrent = useFlashcardScope()
  const [cards, setCards] = useState<Flashcard[]>([])
  const [dueCards, setDueCards] = useState<Flashcard[]>([])
  const [stage, setStage] = useState<'setup' | 'review' | 'summary'>('setup')
  const [sessionSize, setSessionSize] = useState('10')
  const [sessionTotal, setSessionTotal] = useState(0)
  const [completed, setCompleted] = useState<ReviewResult[]>([])
  const [removed, setRemoved] = useState(0)
  const [current, setCurrent] = useState(0)
  const [flipped, setFlipped] = useState(false)
  const [loading, setLoading] = useState(true)
  const [total, setTotal] = useState(0)
  const [showGenerate, setShowGenerate] = useState(false)
  const [genTopic, setGenTopic] = useState('')
  const [genCount, setGenCount] = useState(10)
  const [genCefr, setGenCefr] = useState('')
  const genLevelEdited = useRef(false)
  const [generationResult, setGenerationResult] = useState<{
    created: number
    skipped_duplicates: number
    skipped_empty: number
  } | null>(null)
  const [generating, setGenerating] = useState(false)
  const [genError, setGenError] = useState('')
  const [speakingMode, setSpeakingMode] = useState(false)
  const [reviewing, setReviewing] = useState(false)
  const reviewingRef = useRef(false)
  const reviewAttempt = useRef<{
    cardId: number
    word: string
    quality: number
    reviewId: string
  } | null>(null)
  const [reviewCanRefresh, setReviewCanRefresh] = useState(false)
  const sessionRecorded = useRef(false)
  const loadRequest = useRef<AbortController | null>(null)
  const [loadError, setLoadError] = useState(false)
  const [noPlan, setNoPlan] = useState(false)
  const [reviewError, setReviewError] = useState(false)
  const [managing, setManaging] = useState(false)
  const [recording, setRecording] = useState(false)
  const preference = useBackPreference(stage === 'review')
  const backContent = preference.value
  const generatingRef = useRef(false)

  const loadDue = useCallback(async () => {
    if (!isCurrent()) return
    loadRequest.current?.abort()
    const controller = new AbortController()
    loadRequest.current = controller
    setLoading(true)
    setLoadError(false)
    setReviewError(false)
    try {
      const res = await apiFetch('/api/flashcards/due', {
        signal: controller.signal,
      })
      if (res.status === 404) {
        if (isCurrent() && !controller.signal.aborted) setNoPlan(true)
        return
      }
      if (!res.ok) throw new Error('Could not load flashcards')
      const data = await res.json()
      if (isCurrent() && !controller.signal.aborted) {
        setNoPlan(false)
        setDueCards(data.due)
        setCards([])
        setStage('setup')
        setCompleted([])
        setRemoved(0)
        if (!genLevelEdited.current) setGenCefr(data.cefr_level)
        setTotal(data.total)
        setCurrent(0)
        setFlipped(false)
        sessionRecorded.current = false
      }
    } catch {
      if (isCurrent() && !controller.signal.aborted) setLoadError(true)
    } finally {
      if (isCurrent() && !controller.signal.aborted) setLoading(false)
    }
  }, [isCurrent])

  useEffect(() => {
    void loadDue()
    return () => loadRequest.current?.abort()
  }, [loadDue])

  async function reviewCard(quality: number) {
    if (
      stage !== 'review' ||
      cards.length === 0 ||
      reviewingRef.current ||
      managing ||
      generatingRef.current ||
      !isCurrent()
    )
      return
    reviewingRef.current = true
    setReviewing(true)
    setReviewError(false)
    const card = cards[current]
    const attempt = reviewAttempt.current ?? {
      cardId: card.id,
      word: card.word,
      quality,
      reviewId: crypto.randomUUID(),
    }
    reviewAttempt.current = attempt
    setReviewCanRefresh(false)
    const sessionVersion = useAuthStore.getState().sessionVersion
    try {
      const response = await apiFetch(
        `/api/flashcards/${attempt.cardId}/review`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            quality: attempt.quality,
            review_id: attempt.reviewId,
          }),
        }
      )
      if (!response.ok) {
        if (isCurrent())
          setReviewCanRefresh(
            response.status >= 400 &&
              response.status < 500 &&
              ![408, 429].includes(response.status)
          )
        throw new Error('Could not review flashcard')
      }
      const result = await response.json()
      if (!isCurrent()) return
      reviewAttempt.current = null
      setCompleted((previous) => [
        ...previous,
        {
          id: card.id,
          word: attempt.word,
          quality: attempt.quality,
          xp: result.xp_earned,
        },
      ])
      setDueCards((items) => items.filter((item) => item.id !== card.id))
      if (!sessionRecorded.current)
        sessionRecorded.current = trackBrowserEvent(
          'flashcard_session_started',
          { sessionVersion }
        )
      if (current < cards.length - 1) {
        setCurrent(current + 1)
        setFlipped(false)
      } else {
        setStage('summary')
      }
    } catch {
      if (isCurrent()) setReviewError(true)
    } finally {
      reviewingRef.current = false
      if (isCurrent()) setReviewing(false)
    }
  }

  function startSession() {
    if (!isCurrent() || generatingRef.current || !dueCards.length) return
    const selected = dueCards.slice(
      0,
      sessionSize === 'all' ? dueCards.length : Number(sessionSize)
    )
    setCards(selected)
    setSessionTotal(selected.length)
    setCurrent(0)
    setCompleted([])
    setRemoved(0)
    setFlipped(false)
    setReviewError(false)
    sessionRecorded.current = false
    setStage('review')
    setShowGenerate(false)
  }

  async function generateCards(e: React.FormEvent) {
    e.preventDefault()
    if (
      !genTopic.trim() ||
      !genCefr ||
      stage === 'review' ||
      generatingRef.current ||
      reviewingRef.current ||
      managing ||
      recording ||
      !isCurrent()
    )
      return
    generatingRef.current = true
    setGenerating(true)
    setGenError('')
    setGenerationResult(null)
    try {
      const res = await apiFetch('/api/flashcards/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          topic: genTopic.trim(),
          count: genCount,
          cefr_level: genCefr,
        }),
      })
      if (!res.ok) {
        const data = await res.json().catch(() => ({}))
        throw new Error(data.detail || `Error ${res.status}`)
      }
      const result = await res.json()
      if (!isCurrent()) return
      setGenerationResult(result)
      setShowGenerate(false)
      setGenTopic('')
      await loadDue()
    } catch (err: unknown) {
      if (!isCurrent()) return
      const msg = err instanceof Error ? err.message : ''
      setGenError(
        msg === 'No active study plan found'
          ? tCommon('noActivePlan')
          : tCommon('errorMessage')
      )
    } finally {
      generatingRef.current = false
      if (isCurrent()) setGenerating(false)
    }
  }

  if (loading) {
    return <PageLoading />
  }

  if (loadError) return <FlashcardError onRetry={() => void loadDue()} />
  if (noPlan) return <NoPlanBanner />

  function removeCurrent(deleted: boolean) {
    setManaging(false)
    setReviewError(false)
    setFlipped(false)
    setRemoved((value) => value + 1)
    setDueCards((items) =>
      items.filter((item) => item.id !== cards[current].id)
    )
    if (deleted) setTotal((value) => value - 1)
    if (current >= cards.length - 1) {
      setStage('summary')
    } else {
      setCards((items) => items.filter((item) => item.id !== cards[current].id))
    }
  }

  const sessionProcessed = completed.length + removed

  return (
    <div className="mx-auto max-w-4xl space-y-6 px-4 py-6 font-sans sm:p-6">
      {/* Header */}
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1 className="text-fl-fg flex items-center gap-3 text-2xl font-semibold tracking-tight">
            <Layers
              className="text-fl-accent size-6 shrink-0"
              aria-hidden="true"
            />
            {t('title')}
          </h1>
          <p className="text-fl-muted-2 mt-2 text-sm tabular-nums">
            {total} {t('total')} · {dueCards.length} {t('due')}
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Link
            href="/flashcards/vocabulary"
            className="border-fl-border text-fl-fg hover:bg-fl-surface-2 focus-visible:outline-fl-accent inline-flex min-h-11 items-center gap-2 border px-4 py-2 text-sm font-medium transition-colors focus-visible:outline-2 focus-visible:outline-offset-2"
          >
            <BookOpen className="size-4 shrink-0" aria-hidden="true" />
            {t('myVocabularyBtn')}
          </Link>
          <button
            disabled={
              stage === 'review' ||
              reviewing ||
              managing ||
              recording ||
              generating
            }
            onClick={() => {
              setShowGenerate(!showGenerate)
            }}
            aria-expanded={showGenerate}
            aria-label={`+ ${t('generateBtn')}`}
            aria-controls="flashcard-generate-panel"
            className={`focus-visible:outline-fl-accent inline-flex min-h-11 items-center gap-2 border px-4 py-2 text-sm font-medium transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 disabled:cursor-not-allowed disabled:opacity-40 ${
              showGenerate
                ? 'border-fl-accent/40 bg-fl-accent/10 text-fl-fg'
                : 'border-fl-border text-fl-fg hover:bg-fl-surface-2'
            }`}
          >
            <Plus className="size-4 shrink-0" aria-hidden="true" />
            {t('generateBtn')}
          </button>
        </div>
      </div>

      {generationResult && (
        <div
          role="status"
          className="border-fl-accent/35 bg-fl-surface text-fl-muted-1 flex items-start gap-3 border p-4 text-sm"
        >
          <Check
            className="text-fl-accent mt-0.5 size-5 shrink-0"
            aria-hidden="true"
          />
          <div className="space-y-1">
            <p>
              {t('generationCounts', {
                created: generationResult.created,
                duplicates: generationResult.skipped_duplicates,
              })}
            </p>
            {generationResult.skipped_empty > 0 && (
              <p>
                {t('generationEmpty', {
                  count: generationResult.skipped_empty,
                })}
              </p>
            )}
          </div>
        </div>
      )}

      {/* Generate panel */}
      {showGenerate && (
        <div
          id="flashcard-generate-panel"
          className="border-fl-border bg-fl-surface border"
        >
          <div className="border-fl-border flex items-center gap-2 border-b px-5 py-4">
            <Sparkles className="text-fl-accent size-5" aria-hidden="true" />
            <h2 className="text-fl-fg font-semibold">{t('generate')}</h2>
          </div>
          {genError && (
            <div
              role="alert"
              className="border-fl-error/40 text-fl-error-fg mx-5 mt-4 border px-4 py-3 text-sm"
            >
              ✕ {genError}
            </div>
          )}
          <form onSubmit={generateCards} className="space-y-4 p-5 sm:p-6">
            <div>
              <label
                htmlFor="flashcard-topic"
                className="text-fl-muted-1 mb-2 block text-sm font-medium"
              >
                {t('topic')}
              </label>
              <input
                id="flashcard-topic"
                type="text"
                value={genTopic}
                onChange={(e) => setGenTopic(e.target.value)}
                required
                placeholder={t('topicPlaceholder')}
                className="bg-fl-bg border-fl-border text-fl-fg placeholder:text-fl-muted-2 focus-visible:outline-fl-accent w-full border px-4 py-3 text-base transition-colors focus-visible:outline-2 focus-visible:outline-offset-2"
              />
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label
                  htmlFor="flashcard-count"
                  className="text-fl-muted-1 mb-2 block text-sm font-medium"
                >
                  {t('count')}
                </label>
                <select
                  id="flashcard-count"
                  value={genCount}
                  onChange={(e) => setGenCount(Number(e.target.value))}
                  className="bg-fl-bg border-fl-border text-fl-fg focus-visible:outline-fl-accent min-h-11 w-full border px-3 py-2 text-base focus-visible:outline-2 focus-visible:outline-offset-2"
                >
                  {[5, 10, 15, 20].map((n) => (
                    <option key={n} value={n}>
                      {n} {t('cards')}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label
                  htmlFor="flashcard-level"
                  className="text-fl-muted-1 mb-2 block text-sm font-medium"
                >
                  {t('level')}
                </label>
                <select
                  id="flashcard-level"
                  value={genCefr}
                  onChange={(e) => {
                    genLevelEdited.current = true
                    setGenCefr(e.target.value)
                  }}
                  className="bg-fl-bg border-fl-border text-fl-fg focus-visible:outline-fl-accent min-h-11 w-full border px-3 py-2 text-base focus-visible:outline-2 focus-visible:outline-offset-2"
                >
                  {CEFR_LEVELS.map((l) => (
                    <option key={l} value={l}>
                      {l}
                    </option>
                  ))}
                </select>
              </div>
            </div>
            <button
              type="submit"
              disabled={
                generating ||
                reviewing ||
                managing ||
                recording ||
                !genTopic.trim() ||
                !genCefr
              }
              className="bg-fl-accent text-fl-accent-fg hover:bg-fl-accent/90 focus-visible:outline-fl-accent min-h-11 w-full px-5 py-3 text-sm font-semibold transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 disabled:cursor-not-allowed disabled:opacity-40 sm:w-auto"
            >
              {generating ? t('generating') : t('submit')}
            </button>
          </form>
        </div>
      )}

      {/* No cards */}
      {stage === 'setup' && dueCards.length === 0 && (
        <div className="border-fl-border bg-fl-surface border px-6 py-12 text-center">
          {total === 0 ? (
            <Layers
              className="text-fl-accent mx-auto mb-4 size-8"
              aria-hidden="true"
            />
          ) : (
            <Check
              className="text-fl-accent mx-auto mb-4 size-8"
              aria-hidden="true"
            />
          )}
          <h2 className="text-fl-fg text-lg font-semibold">{t('noDue')}</h2>
          {total === 0 && (
            <p className="text-fl-muted-2 mx-auto mt-2 max-w-md text-sm leading-relaxed">
              {t('noCardsHint')}
            </p>
          )}
          <button
            onClick={loadDue}
            disabled={generating}
            className="border-fl-border text-fl-fg hover:bg-fl-surface-2 focus-visible:outline-fl-accent mt-6 inline-flex min-h-11 items-center gap-2 border px-5 py-2 text-sm font-medium focus-visible:outline-2 focus-visible:outline-offset-2 disabled:opacity-40"
          >
            <RotateCcw className="size-4" aria-hidden="true" />
            {t('refresh')}
          </button>
        </div>
      )}

      {stage === 'setup' && dueCards.length > 0 && (
        <section
          className="border-fl-accent/35 border-l-fl-accent bg-fl-surface space-y-6 border border-l-4 p-5 sm:p-8"
          aria-labelledby="flashcard-session-title"
        >
          <div className="flex flex-wrap items-start justify-between gap-5">
            <div className="space-y-2">
              <h2
                id="flashcard-session-title"
                className="text-fl-fg text-xl font-semibold"
              >
                {t('sessionTitle')}
              </h2>
              <p className="text-fl-muted-1 text-sm leading-relaxed">
                {t('sessionComposition', {
                  new: dueCards.filter(isNewCard).length,
                  review: dueCards.filter((card) => !isNewCard(card)).length,
                })}
              </p>
            </div>
            <div className="bg-fl-accent/10 text-fl-accent min-w-24 px-4 py-3 text-center">
              <p className="text-3xl font-semibold tabular-nums">
                {dueCards.length}
              </p>
              <p className="mt-1 text-sm">{t('due')}</p>
            </div>
          </div>
          <fieldset disabled={generating}>
            <legend className="text-fl-muted-1 mb-3 text-sm font-medium">
              {t('sessionSize')}
            </legend>
            <div className="grid grid-cols-2 gap-2 sm:grid-cols-3">
              {['5', '10', 'all'].map((size) => (
                <label
                  key={size}
                  className={size === 'all' ? 'col-span-2 sm:col-span-1' : ''}
                >
                  <input
                    type="radio"
                    name="flashcard-session-size"
                    value={size}
                    checked={sessionSize === size}
                    onChange={(event) => setSessionSize(event.target.value)}
                    className="peer sr-only"
                  />
                  <span className="border-fl-border text-fl-muted-1 peer-checked:border-fl-accent peer-checked:bg-fl-accent/10 peer-checked:text-fl-fg peer-focus-visible:outline-fl-accent hover:bg-fl-surface-2 flex min-h-12 cursor-pointer items-center justify-center border px-3 py-3 text-center text-sm font-medium transition-colors peer-focus-visible:outline-2 peer-focus-visible:outline-offset-2 peer-disabled:cursor-not-allowed peer-disabled:opacity-40">
                    {size === 'all' ? t('sessionAll') : `${size} ${t('cards')}`}
                  </span>
                </label>
              ))}
            </div>
          </fieldset>
          <button
            disabled={generating}
            onClick={startSession}
            className="bg-fl-accent text-fl-accent-fg hover:bg-fl-accent/90 focus-visible:outline-fl-accent inline-flex min-h-11 w-full items-center justify-center gap-2 px-5 py-3 text-sm font-semibold transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 disabled:cursor-not-allowed disabled:opacity-40 sm:w-auto"
          >
            <BookOpen className="size-4" aria-hidden="true" />
            {t('sessionStart')}
          </button>
        </section>
      )}

      {stage === 'summary' && (
        <section
          className="border-fl-border bg-fl-surface space-y-6 border p-5 sm:p-8"
          aria-labelledby="flashcard-summary-title"
        >
          <h2
            id="flashcard-summary-title"
            className="text-fl-fg flex items-center gap-3 text-xl font-semibold"
          >
            <Check
              className="text-fl-accent size-6 shrink-0"
              aria-hidden="true"
            />
            {t('sessionSummary')}
          </h2>
          <dl className="grid gap-3 sm:grid-cols-3">
            {[
              {
                label: 'sessionReviewed',
                value: completed.length,
                icon: Layers,
              },
              {
                label: 'sessionXp',
                value: completed.reduce((sum, item) => sum + item.xp, 0),
                icon: Sparkles,
              },
              {
                label: 'sessionRemaining',
                value: dueCards.length,
                icon: Clock,
              },
            ].map(({ label, value, icon: Icon }) => (
              <div
                key={label}
                className={`border p-4 sm:p-5 ${label === 'sessionXp' ? 'border-fl-accent/35 bg-fl-accent/10' : 'border-fl-border bg-fl-bg'}`}
              >
                <dt className="text-fl-muted-1 flex items-center gap-2 text-sm">
                  <Icon
                    className="text-fl-accent size-4 shrink-0"
                    aria-hidden="true"
                  />
                  {t(label)}
                </dt>
                <dd className="text-fl-fg mt-3 text-3xl font-semibold tracking-tight tabular-nums">
                  {value}
                </dd>
              </div>
            ))}
          </dl>
          {removed > 0 && (
            <p className="text-fl-muted-2 text-sm">
              {t('sessionRemoved', { count: removed })}
            </p>
          )}
          {completed.some((item) => item.quality <= 3) && (
            <div className="space-y-2">
              <h3 className="text-fl-fg font-medium">
                {t('sessionDifficult')}
              </h3>
              <ul className="border-fl-border divide-fl-border divide-y border">
                {completed
                  .filter((item) => item.quality <= 3)
                  .map((item) => (
                    <li
                      key={item.id}
                      className="text-fl-muted-1 flex flex-wrap items-center justify-between gap-2 px-4 py-3"
                    >
                      <TargetLanguageText languageCode={targetLanguageCode}>
                        {item.word}
                      </TargetLanguageText>
                      <span className="border-fl-border bg-fl-bg border px-2 py-1 text-xs">
                        {t(item.quality < 3 ? 'again' : 'hard')}
                      </span>
                    </li>
                  ))}
              </ul>
            </div>
          )}
          <button
            disabled={generating}
            onClick={() => void loadDue()}
            className="bg-fl-accent text-fl-accent-fg hover:bg-fl-accent/90 focus-visible:outline-fl-accent inline-flex min-h-11 w-full items-center justify-center gap-2 px-5 py-3 text-sm font-semibold transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 disabled:opacity-40 sm:w-auto"
          >
            <RotateCcw className="size-4" aria-hidden="true" />
            {t('sessionReturn')}
          </button>
          {completed.length > 0 && <PremiumResultOffer feature="flashcards" />}
        </section>
      )}

      {/* Card review */}
      {stage === 'review' && cards.length > 0 && (
        <>
          <div className="space-y-3">
            <div className="text-fl-muted-1 flex flex-wrap items-center justify-between gap-3 text-sm">
              <span className="tabular-nums">
                {sessionProcessed + 1} / {sessionTotal} ·{' '}
                {t(
                  isNewCard(cards[current]) ? 'newCards' : 'sessionReviewCard'
                )}
              </span>
              <button
                disabled={
                  reviewing ||
                  reviewError ||
                  managing ||
                  recording ||
                  generating
                }
                onClick={() => setStage('summary')}
                className="text-fl-muted-1 hover:text-fl-fg focus-visible:outline-fl-accent min-h-11 px-2 text-sm underline underline-offset-4 focus-visible:outline-2 focus-visible:outline-offset-2 disabled:opacity-40"
              >
                {t('sessionFinish')}
              </button>
            </div>
            <div
              role="progressbar"
              aria-label={t('sessionProgress')}
              aria-valuenow={sessionProcessed}
              aria-valuemin={0}
              aria-valuemax={sessionTotal}
              className="bg-fl-border h-1.5 overflow-hidden"
            >
              <div
                className="bg-fl-accent h-full transition-[width] duration-300 motion-reduce:transition-none"
                style={{
                  width: `${sessionTotal ? Math.min(100, (sessionProcessed / sessionTotal) * 100) : 0}%`,
                }}
              />
            </div>
          </div>
          <div className="border-fl-border bg-fl-surface flex flex-wrap items-end justify-between gap-4 border p-4 sm:px-5">
            {/* Mode toggle */}
            <div
              role="group"
              aria-label={t('reviewMode')}
              className="border-fl-border flex max-w-full flex-wrap gap-1 border p-1"
            >
              <button
                aria-pressed={!speakingMode}
                disabled={
                  reviewing ||
                  reviewError ||
                  managing ||
                  recording ||
                  generating
                }
                onClick={() => {
                  setSpeakingMode(false)
                  setFlipped(false)
                }}
                className={`focus-visible:outline-fl-accent inline-flex min-h-11 items-center justify-center gap-2 px-3 py-2 text-sm font-medium transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 disabled:cursor-not-allowed disabled:opacity-40 ${!speakingMode ? 'bg-fl-fg text-fl-bg' : 'text-fl-muted-1 hover:bg-fl-surface-2 hover:text-fl-fg'}`}
              >
                <BookOpen className="size-4 shrink-0" aria-hidden="true" />
                {t('standardMode')}
              </button>
              <button
                aria-pressed={speakingMode}
                disabled={
                  reviewing ||
                  reviewError ||
                  managing ||
                  recording ||
                  generating
                }
                onClick={() => {
                  setSpeakingMode(true)
                  setFlipped(false)
                }}
                className={`focus-visible:outline-fl-accent inline-flex min-h-11 items-center justify-center gap-2 px-3 py-2 text-sm font-medium transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 disabled:cursor-not-allowed disabled:opacity-40 ${speakingMode ? 'bg-fl-fg text-fl-bg' : 'text-fl-muted-1 hover:bg-fl-surface-2 hover:text-fl-fg'}`}
              >
                <Mic className="size-4 shrink-0" aria-hidden="true" />
                {t('speakingMode')}
              </button>
            </div>
            {!speakingMode && <BackPreference preference={preference} />}
          </div>

          {/* ── Standard mode ── */}
          {!speakingMode && (
            <>
              <div className="border-fl-accent/35 bg-fl-surface border">
                <div className="border-fl-border flex items-center justify-between gap-3 border-b px-6 py-4">
                  <div className="flex items-center gap-2">
                    <span className="text-fl-muted-1 text-sm font-medium">
                      {flipped
                        ? t(
                            backContent === 'translation' &&
                              cards[current].translation.trim()
                              ? 'field_translation'
                              : 'back'
                          )
                        : t('front')}
                    </span>
                  </div>
                  <AudioPlayer
                    text={cards[current].word}
                    studyPlanId={cards[current].study_plan_id}
                    size="md"
                  />
                </div>

                <button
                  type="button"
                  aria-expanded={flipped}
                  aria-label={flipped ? t('tapToHide') : t('tapToReveal')}
                  disabled={reviewing || reviewError || managing || generating}
                  onClick={() => setFlipped(!flipped)}
                  className="hover:bg-fl-surface-2 focus-visible:outline-fl-accent flex min-h-[240px] w-full flex-col items-center justify-center gap-5 p-6 text-center transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 disabled:opacity-60 sm:min-h-[280px] sm:p-10"
                >
                  {!flipped ? (
                    <TargetLanguageText
                      as="span"
                      languageCode={targetLanguageCode}
                      className="text-fl-fg max-w-full text-3xl font-semibold [overflow-wrap:anywhere] break-words sm:text-4xl"
                    >
                      {cards[current].word}
                    </TargetLanguageText>
                  ) : (
                    <>
                      {backContent === 'translation' &&
                      cards[current].translation.trim() ? (
                        <span className="text-fl-fg-2 max-w-full font-sans text-xl leading-relaxed [overflow-wrap:anywhere] break-words">
                          {cards[current].translation}
                        </span>
                      ) : (
                        <TargetLanguageText
                          languageCode={targetLanguageCode}
                          className="text-fl-fg-2 max-w-full text-xl [overflow-wrap:anywhere] break-words"
                        >
                          {cards[current].definition}
                        </TargetLanguageText>
                      )}
                      {backContent === 'translation' &&
                        cards[current].translation.trim() && (
                          <TargetLanguageText
                            languageCode={targetLanguageCode}
                            className="text-fl-muted-1"
                          >
                            {cards[current].definition}
                          </TargetLanguageText>
                        )}
                      {cards[current].example_sentence && (
                        <TargetLanguageText
                          as="span"
                          languageCode={targetLanguageCode}
                          className="text-fl-muted-1 italic"
                        >
                          {cards[current].example_sentence}
                        </TargetLanguageText>
                      )}
                      {backContent === 'definition' &&
                        cards[current].translation && (
                          <span className="text-fl-muted-1 border-fl-border mt-1 border-t pt-3 font-sans text-sm leading-relaxed">
                            {cards[current].translation}
                          </span>
                        )}
                    </>
                  )}
                  <span className="text-fl-muted-2 mt-3 inline-flex items-center gap-2 text-sm">
                    <RotateCcw className="size-4 shrink-0" aria-hidden="true" />
                    {flipped ? t('tapToHide') : t('tapToReveal')}
                  </span>
                </button>
              </div>

              {flipped && (
                <div
                  role="group"
                  aria-labelledby="flashcard-rating-title"
                  aria-describedby="flashcard-rating-help flashcard-rating-again"
                  className="border-fl-border bg-fl-surface space-y-4 border p-4 sm:p-5"
                >
                  <div className="space-y-1">
                    <p
                      id="flashcard-rating-title"
                      className="text-fl-fg font-sans font-medium"
                    >
                      {t('ratingTitle')}
                    </p>
                    <p
                      id="flashcard-rating-help"
                      className="text-fl-muted-1 font-sans text-sm"
                    >
                      {t('ratingHelp')}
                    </p>
                  </div>
                  <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
                    {[
                      { key: 'again', q: 0, color: 'var(--fl-muted-1)' },
                      { key: 'hard', q: 3, color: 'var(--fl-muted-1)' },
                      { key: 'good', q: 4, color: 'var(--fl-muted-0)' },
                      { key: 'easy', q: 5, color: 'var(--fl-fg)' },
                    ].map(({ key, q, color }) => (
                      <div key={q} className="space-y-2 text-center">
                        <button
                          disabled={
                            reviewing || reviewError || managing || generating
                          }
                          onClick={() => reviewCard(q)}
                          aria-describedby={`flashcard-rating-${key}-hint`}
                          className="border-fl-border hover:border-fl-border-2 hover:bg-fl-surface-2 focus-visible:outline-fl-accent min-h-11 w-full border px-2 py-3 text-sm font-semibold transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 disabled:cursor-not-allowed disabled:opacity-40"
                          style={{ color }}
                        >
                          {t(key)}
                        </button>
                        <p
                          id={`flashcard-rating-${key}-hint`}
                          className="text-fl-muted-1 text-sm leading-relaxed"
                        >
                          {t(`${key}Hint`)}
                        </p>
                      </div>
                    ))}
                  </div>
                  <p
                    id="flashcard-rating-again"
                    className="border-fl-border text-fl-muted-2 border-t pt-3 text-sm leading-relaxed"
                  >
                    {t('againTomorrow')}
                  </p>
                </div>
              )}
            </>
          )}

          {/* ── Speaking mode ── */}
          {speakingMode && (
            <SpeakingCard
              key={JSON.stringify([
                cards[current].id,
                cards[current].word,
                cards[current].definition,
                cards[current].translation,
                cards[current].example_sentence,
              ])}
              card={cards[current]}
              languageCode={targetLanguageCode}
              disabled={reviewing || reviewError || managing || generating}
              onBusyChange={setRecording}
              onReview={reviewCard}
            />
          )}

          {reviewError && (
            <div className="flex flex-wrap items-center gap-3 text-sm">
              <p role="alert" className="text-fl-error-fg">
                {tCommon('errorMessage')} {t('reviewRetryHint')}
              </p>
              <button
                className="underline"
                disabled={reviewing || managing || recording || generating}
                onClick={() =>
                  void reviewCard(reviewAttempt.current?.quality ?? 4)
                }
              >
                {t('retryReview')}
              </button>
              {reviewCanRefresh && (
                <button
                  className="underline"
                  disabled={reviewing}
                  onClick={() => {
                    reviewAttempt.current = null
                    void loadDue()
                  }}
                >
                  {t('refresh')}
                </button>
              )}
            </div>
          )}
          <div className="border-fl-border bg-fl-surface space-y-3 border p-4 sm:p-5">
            <FlashcardActions
              key={cards[current].id}
              card={cards[current]}
              disabled={reviewing || reviewError || recording || generating}
              onInteractionChange={setManaging}
              onUpdate={(updated) => {
                if (updated.is_suspended) removeCurrent(false)
                else
                  setCards((items) =>
                    items.map((item) =>
                      item.id === updated.id ? updated : item
                    )
                  )
                setDueCards((items) =>
                  items.map((item) => (item.id === updated.id ? updated : item))
                )
              }}
              onDelete={() => removeCurrent(true)}
            />
            <p className="text-fl-muted-2 text-sm leading-relaxed">
              {t('suspendHint')}
            </p>
          </div>

          <details className="border-fl-border bg-fl-surface group border">
            <summary className="text-fl-muted-1 focus-visible:outline-fl-accent flex min-h-11 cursor-pointer list-none items-center justify-between gap-3 px-4 py-3 text-sm font-medium focus-visible:outline-2 focus-visible:outline-offset-2 [&::-webkit-details-marker]:hidden">
              {t('reviewDetails')}
              <ChevronDown
                className="size-4 shrink-0 group-open:rotate-180"
                aria-hidden="true"
              />
            </summary>
            <dl className="border-fl-border grid grid-cols-3 gap-3 border-t p-4 text-sm">
              <div>
                <dt className="text-fl-muted-2 font-code">EF</dt>
                <dd className="text-fl-fg font-code mt-1 tabular-nums">
                  {cards[current].ease_factor.toFixed(2)}
                </dd>
              </div>
              <div>
                <dt className="text-fl-muted-2">{t('interval')}</dt>
                <dd className="text-fl-fg font-code mt-1 tabular-nums">
                  {cards[current].interval}d
                </dd>
              </div>
              <div>
                <dt className="text-fl-muted-2">{t('repetitions')}</dt>
                <dd className="text-fl-fg font-code mt-1 tabular-nums">
                  {cards[current].repetitions}
                </dd>
              </div>
            </dl>
          </details>
        </>
      )}
    </div>
  )
}
