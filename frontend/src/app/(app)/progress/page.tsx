'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'

import { useLocale, useTranslations } from 'next-intl'
import { PageLoading } from '@/components/ui/page-loading'
import { apiFetch } from '@/lib/api'
import { useLanguageStore } from '@/store/language'
import NoPlanBanner from '@/components/plan/NoPlanBanner'
import {
  getCurriculumUnits,
  type CurriculumUnit,
  type CEFRLevel,
} from '@/data/curriculum'
import type { VocabularySet } from '@/data/types'
import { Check, Circle, CircleDashed } from 'lucide-react'
import {
  ProgressOverview,
  type ActivityDay,
} from '@/components/dashboard/ProgressOverview'
import {
  ActivityHistory,
  type ProgressHistoryEntry,
} from '@/components/progress/ActivityHistory'
import { RewardGuide } from '@/components/progress/RewardGuide'
import { TargetLanguageText } from '@/components/TargetLanguageText'

// ── Types ──────────────────────────────────────────────────────────────────────

interface CompetencyRecord {
  unit_id: string
  score: number // 0–1 average
  mastered_count: number
  total_count: number
}

interface ProgressSummary {
  total_xp: number
  current_streak: number
  total_lessons: number
  total_exercises: number
  exercises_correct: number
  accuracy: number
  skills: Record<string, number>
  today_xp: number
  activity_week: ActivityDay[]
}

interface FlashcardProgress {
  id: number
  word: string
  repetitions: number
}

interface StudyPlan {
  id: number
  cefr_level: string
}

type CompetencyStatus = 'mastered' | 'in-progress' | 'not-started'

// ── Helpers ────────────────────────────────────────────────────────────────────

function getCompetencyStatus(
  itemIndex: number,
  masteredCount: number,
  totalCount: number,
  score: number
): CompetencyStatus {
  if (itemIndex < masteredCount) return 'mastered'
  if (score > 0 && itemIndex < totalCount) return 'in-progress'
  return 'not-started'
}

const STATUS_ICON = {
  mastered: Check,
  'in-progress': CircleDashed,
  'not-started': Circle,
}

const STATUS_LABEL = {
  mastered: 'mastered',
  'in-progress': 'inProgress',
  'not-started': 'notStarted',
}

const STATUS_COLOR: Record<CompetencyStatus, string> = {
  mastered: 'text-fl-fg',
  'in-progress': 'text-amber-600 dark:text-amber-400',
  'not-started': 'text-fl-muted-4',
}

// ── Sub-components ────────────────────────────────────────────────────────────

function UnitCompetencyBlock({
  unit,
  record,
  languageCode,
}: {
  unit: CurriculumUnit
  record: CompetencyRecord | undefined
  languageCode: string
}) {
  const t = useTranslations('progress')
  const tPlan = useTranslations('plan')
  const number = new Intl.NumberFormat(useLocale())
  const masteredCount = record?.mastered_count ?? 0
  const totalCount = unit.competency_checklist.length
  const score = record?.score ?? 0
  const pct =
    totalCount > 0 ? Math.round((masteredCount / totalCount) * 100) : 0

  return (
    <div className="border-fl-border bg-fl-surface border">
      {/* Unit header */}
      <div className="border-fl-border flex flex-wrap items-center justify-between gap-3 border-b px-5 py-4">
        <div className="min-w-0 space-y-1">
          <span className="text-fl-muted-2 text-xs">
            {tPlan('unitLabel')} {number.format(unit.unit_number)}
          </span>
          <TargetLanguageText
            as="h3"
            languageCode={languageCode}
            className="text-fl-fg font-semibold"
          >
            {unit.title}
          </TargetLanguageText>
        </div>
        <div className="flex items-center gap-3">
          <span className="text-fl-muted-2 text-xs tabular-nums">
            {number.format(masteredCount)}/{number.format(totalCount)}{' '}
            {t('mastered')}
          </span>
          {record && (
            <span className="text-fl-muted-2 text-xs tabular-nums">
              {number.format(Math.round(score * 100))}%
            </span>
          )}
        </div>
      </div>

      {/* Progress bar */}
      <div
        className="bg-fl-border h-1"
        role="progressbar"
        aria-label={`${unit.title}: ${t('mastered')}`}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-valuenow={pct}
      >
        <div
          className="bg-fl-accent h-full transition-[width] motion-reduce:transition-none"
          style={{ width: `${pct}%` }}
        />
      </div>

      {/* Competency list */}
      <ul className="space-y-2 px-5 py-3">
        {unit.competency_checklist.map((text, idx) => {
          const status = getCompetencyStatus(
            idx,
            masteredCount,
            record?.total_count ?? 0,
            score
          )
          const Icon = STATUS_ICON[status]
          return (
            <li key={idx} className="flex items-start gap-3">
              <span className={`mt-0.5 shrink-0 ${STATUS_COLOR[status]}`}>
                <Icon className="size-4" aria-hidden="true" />
                <span className="sr-only">{t(STATUS_LABEL[status])}: </span>
              </span>
              <TargetLanguageText
                languageCode={languageCode}
                className={STATUS_COLOR[status]}
              >
                {text}
              </TargetLanguageText>
              {status === 'in-progress' && record && (
                <span className="text-fl-muted-2 ml-auto shrink-0 text-xs tabular-nums">
                  {number.format(Math.round(score * 100))}%
                </span>
              )}
            </li>
          )
        })}
      </ul>
    </div>
  )
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function ProgressPage() {
  const activeLanguage = useLanguageStore((s) => s.activeLanguage)
  const targetLanguageCode = activeLanguage?.code ?? 'en-GB'
  return (
    <ProgressContent
      key={targetLanguageCode}
      targetLanguageCode={targetLanguageCode}
      languageName={activeLanguage?.name}
    />
  )
}

interface ProgressData {
  summary: ProgressSummary
  competencies: CompetencyRecord[]
  plan: StudyPlan
  flashcards: FlashcardProgress[]
  levelUnits: CurriculumUnit[]
  vocabSets: VocabularySet[]
  history: ProgressHistoryEntry[]
}

function ProgressContent({
  targetLanguageCode,
  languageName,
}: {
  targetLanguageCode: string
  languageName?: string
}) {
  const locale = useLocale()
  const t = useTranslations('progress')
  const tVocab = useTranslations('vocabulary')
  const common = useTranslations('common')
  const tDashboard = useTranslations('dashboard')
  const tPlan = useTranslations('plan')
  const [data, setData] = useState<ProgressData | null>(null)
  const [loading, setLoading] = useState(true)
  const [loadError, setLoadError] = useState(false)
  const [retry, setRetry] = useState(0)
  const [showAllLevels, setShowAllLevels] = useState(false)

  useEffect(() => {
    let cancelled = false
    async function load() {
      try {
        const [sumRes, compRes, planRes, flashRes, historyRes, vocabRes] =
          await Promise.all([
            apiFetch('/api/progress/summary'),
            apiFetch('/api/progress/competencies'),
            apiFetch('/api/study-plan/current'),
            apiFetch('/api/flashcards/all'),
            apiFetch('/api/progress/history'),
            apiFetch(
              `/api/vocabulary?language=${encodeURIComponent(targetLanguageCode)}`
            ),
          ])
        if (cancelled) return
        if (!planRes.ok) throw new Error('Could not load study plan')
        const plan = (await planRes.json()) as StudyPlan | null
        if (cancelled || !plan) return
        if (
          [sumRes, compRes, flashRes, historyRes, vocabRes].some(
            (res) => !res.ok
          )
        ) {
          throw new Error('Could not load progress')
        }
        const [summary, competencies, flashcards, history, vocabulary] =
          await Promise.all([
            sumRes.json() as Promise<ProgressSummary>,
            compRes.json() as Promise<CompetencyRecord[]>,
            flashRes.json() as Promise<FlashcardProgress[]>,
            historyRes.json() as Promise<{ entries: ProgressHistoryEntry[] }>,
            vocabRes.json() as Promise<{ sets: VocabularySet[] }>,
          ])
        if (cancelled) return
        const levelUnits = await getCurriculumUnits(
          plan.cefr_level,
          targetLanguageCode
        )
        if (cancelled) return
        setData({
          summary,
          competencies,
          plan,
          flashcards,
          levelUnits,
          vocabSets: vocabulary.sets,
          history: history.entries,
        })
      } catch {
        if (!cancelled) setLoadError(true)
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    void load()
    return () => {
      cancelled = true
    }
  }, [targetLanguageCode, retry])

  if (loading) {
    return <PageLoading label={t('loading')} />
  }

  if (loadError) {
    return (
      <div className="mx-auto max-w-4xl space-y-4 p-6 text-center">
        <p role="alert" className="text-fl-muted-1">
          {common('errorMessage')}
        </p>
        <button
          className="border-fl-border text-fl-fg hover:bg-fl-surface-2 border px-4 py-2 text-sm"
          onClick={() => {
            setLoadError(false)
            setLoading(true)
            setRetry((value) => value + 1)
          }}
        >
          {common('retry')}
        </button>
      </div>
    )
  }

  if (!data) {
    return <NoPlanBanner />
  }

  const {
    summary,
    competencies,
    plan,
    flashcards,
    levelUnits,
    vocabSets,
    history,
  } = data
  const compMap = Object.fromEntries(competencies.map((c) => [c.unit_id, c]))
  const cefrLevel = plan.cefr_level as CEFRLevel
  const displayVocabSets = showAllLevels
    ? vocabSets
    : vocabSets.filter((s) => s.level === cefrLevel)
  const totalDisplayWords = displayVocabSets.reduce(
    (a, s) => a + s.words.length,
    0
  )

  const masteredWordSet = new Set(
    flashcards
      .filter((f) => f.repetitions > 0)
      .map((f) => f.word.trim().toLowerCase())
  )
  const totalMastered = displayVocabSets.reduce(
    (a, s) =>
      a +
      s.words.filter((w) => masteredWordSet.has(w.word.trim().toLowerCase()))
        .length,
    0
  )
  const today = summary.activity_week.at(-1)?.date

  return (
    <div className="mx-auto max-w-4xl space-y-8 p-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h1 className="text-fl-fg text-2xl font-semibold">{t('title')}</h1>
        {languageName && (
          <span className="border-fl-border text-fl-muted-1 border px-3 py-1 text-sm">
            {languageName} · {cefrLevel}
          </span>
        )}
      </div>

      <ProgressOverview
        xp={summary.total_xp}
        todayXp={summary.today_xp}
        streak={summary.current_streak}
        activity={summary.activity_week}
        lessons={summary.total_lessons}
        correct={summary.exercises_correct}
        total={summary.total_exercises}
        showDetails={false}
      />
      {today && <ActivityHistory entries={history} endDate={today} />}
      <RewardGuide />

      {/* Grammar Competencies */}
      {levelUnits.length > 0 && (
        <section className="space-y-4">
          <div className="flex items-center gap-3">
            <h2 className="text-fl-fg text-lg font-semibold">
              {cefrLevel
                ? t('competenciesSection', { level: cefrLevel })
                : t('competencies')}
            </h2>
            <div className="bg-fl-border h-px flex-1" />
          </div>

          {levelUnits.map((unit) => (
            <UnitCompetencyBlock
              key={unit.id}
              unit={unit}
              record={compMap[unit.id]}
              languageCode={targetLanguageCode}
            />
          ))}

          {competencies.length === 0 && (
            <div className="border-fl-border bg-fl-surface border px-6 py-8 text-center">
              <p className="text-fl-muted-2 text-sm leading-relaxed">
                {t('noCompetencies')}
              </p>
              <Link
                href="/plan"
                className="text-fl-accent mt-4 inline-block text-sm font-medium hover:underline"
              >
                {t('goToMyPlan')}
              </Link>
            </div>
          )}
        </section>
      )}

      {/* Vocabulary Progress */}
      {displayVocabSets.length > 0 && (
        <section className="space-y-4">
          <div className="flex flex-wrap items-center gap-3">
            <h2 className="text-fl-fg text-lg font-semibold">
              {showAllLevels
                ? t('vocabularySection')
                : cefrLevel
                  ? t('vocabularyHeader', { level: cefrLevel })
                  : t('vocabularySection')}
            </h2>
            <div className="bg-fl-border h-px flex-1" />
            <span className="text-fl-muted-2 text-sm tabular-nums">
              {totalMastered.toLocaleString(locale)}/
              {totalDisplayWords.toLocaleString(locale)} {tVocab('words')}
            </span>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setShowAllLevels(false)}
              aria-pressed={!showAllLevels}
              className={`border px-3 py-1.5 text-sm transition-colors ${
                !showAllLevels
                  ? 'border-fl-fg text-fl-fg bg-fl-surface-2'
                  : 'border-fl-border text-fl-muted-3 hover:border-fl-border-2 hover:text-fl-fg'
              }`}
            >
              {t('currentLevelOnly')}
            </button>
            <button
              onClick={() => setShowAllLevels(true)}
              aria-pressed={showAllLevels}
              className={`border px-3 py-1.5 text-sm transition-colors ${
                showAllLevels
                  ? 'border-fl-fg text-fl-fg bg-fl-surface-2'
                  : 'border-fl-border text-fl-muted-3 hover:border-fl-border-2 hover:text-fl-fg'
              }`}
            >
              {t('allLevels')}
            </button>
          </div>

          <div className="border-fl-border bg-fl-surface divide-fl-border divide-y border">
            {displayVocabSets.map((s) => {
              const mastered = s.words.filter((w) =>
                masteredWordSet.has(w.word.trim().toLowerCase())
              ).length
              const pct =
                s.words.length > 0
                  ? Math.round((mastered / s.words.length) * 100)
                  : 0
              return (
                <div key={s.id} className="flex items-center gap-4 px-5 py-3">
                  <Link
                    href={`/vocabulary/${s.id}`}
                    className="text-fl-muted-1 hover:text-fl-fg min-w-0 flex-1 truncate text-sm transition-colors"
                  >
                    <TargetLanguageText languageCode={targetLanguageCode}>
                      {s.topic}
                    </TargetLanguageText>
                  </Link>
                  <div className="flex items-center gap-3">
                    <div
                      className="bg-fl-border h-1 w-16 sm:w-24"
                      role="progressbar"
                      aria-label={s.topic}
                      aria-valuemin={0}
                      aria-valuemax={100}
                      aria-valuenow={pct}
                    >
                      <div
                        className="bg-fl-accent h-full transition-[width] motion-reduce:transition-none"
                        style={{ width: `${pct}%` }}
                      />
                    </div>
                    <span className="text-fl-muted-2 min-w-12 text-right text-xs tabular-nums">
                      {mastered.toLocaleString(locale)}/
                      {s.words.length.toLocaleString(locale)}
                    </span>
                  </div>
                </div>
              )
            })}
          </div>
        </section>
      )}

      {/* Skills breakdown */}
      {summary && Object.keys(summary.skills).length > 0 && (
        <section className="space-y-4">
          <div className="flex items-center gap-3">
            <h2 className="text-fl-fg text-lg font-semibold">
              {tDashboard('recentPerformance')}
            </h2>
            <div className="bg-fl-border h-px flex-1" />
          </div>
          <p className="text-fl-muted-2 text-sm">
            {tDashboard('recentPerformanceDescription')}
          </p>
          <div className="border-fl-border bg-fl-surface divide-fl-border divide-y border">
            {Object.entries(summary.skills).map(([skill, value]) => (
              <div key={skill} className="flex items-center gap-4 px-5 py-3">
                <span className="text-fl-muted-1 w-28 text-sm">
                  {tPlan.has(`lessonTypes.${skill}`)
                    ? tPlan(`lessonTypes.${skill}`)
                    : skill}
                </span>
                <div
                  className="bg-fl-border h-1 flex-1"
                  role="progressbar"
                  aria-label={
                    tPlan.has(`lessonTypes.${skill}`)
                      ? tPlan(`lessonTypes.${skill}`)
                      : skill
                  }
                  aria-valuemin={0}
                  aria-valuemax={100}
                  aria-valuenow={Math.round(value * 100)}
                >
                  <div
                    className="bg-fl-accent h-full"
                    style={{ width: `${Math.round(value * 100)}%` }}
                  />
                </div>
                <span className="text-fl-muted-2 w-10 text-right text-xs tabular-nums">
                  {Math.round(value * 100).toLocaleString(locale)}%
                </span>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  )
}
