'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useTranslations } from 'next-intl'
import { ArrowRight, Check, Circle } from 'lucide-react'
import { PageLoading } from '@/components/ui/page-loading'
import { TargetLanguageText } from '@/components/TargetLanguageText'
import { apiFetch } from '@/lib/api'
import { getCurriculumUnits, type CurriculumUnit } from '@/data/curriculum'
import { useLanguageStore } from '@/store/language'
import { useAuthStore } from '@/store/auth'
import type { TargetLanguage } from '@/lib/target-languages'
import UnitCard from '@/components/plan/UnitCard'
import UnitDrawer from '@/components/plan/UnitDrawer'
import LevelTestBanner from '@/components/plan/LevelTestBanner'
import NoPlanBanner from '@/components/plan/NoPlanBanner'
import type { CEFRLevel } from '@/data/grammar'

// ── Types ──────────────────────────────────────────────────────────────────────

interface PendingLesson {
  id: number
  title: string
  lesson_type: string
  week_number: number
  day_number: number
}

interface PlanLesson extends PendingLesson {
  unit_id: string | null
  is_completed: boolean
}

interface TodayLesson {
  id: number | null
  title: string
  lesson_type: string
  week: number
  day: number
  unit_id?: string
  is_completed?: boolean
}

interface TodayResponse {
  plan_id: number
  progress_day: number
  lessons: TodayLesson[]
  completion?: CompletionState
}

type LessonAction = 'start' | 'continue' | 'review'

interface Lesson {
  id: number | null
  title: string
  lesson_type: string
  week: number
  day: number
  unit_id?: string
  completed?: boolean
  action?: LessonAction
}

interface StudyPlan {
  id: number
  cefr_level: string
  duration_weeks: number
  days_per_week: number
  progress_day: number
  completion_test_taken: boolean
  completion_test_score: number | null
  completion_test_recommendation: string | null
  generated_plan: {
    weekly_plan: {
      week: number
      days: {
        day: number
        title: string
        lesson_type: string
        unit_id: string
      }[]
    }[]
  }
}

interface CompletionState {
  state: 'in_progress' | 'ready' | 'taken'
  score: number | null
  recommendation: string | null
  next_level: string | null
}

// ── Helpers ───────────────────────────────────────────────────────────────────

function flattenLessons(plan: StudyPlan): Lesson[] {
  const result: Lesson[] = []
  for (const week of plan.generated_plan.weekly_plan) {
    for (const day of week.days) {
      result.push({
        id: null,
        title: day.title,
        lesson_type: day.lesson_type,
        week: week.week,
        day: day.day,
        unit_id: day.unit_id,
        completed: false,
      })
    }
  }
  return result
}

function lessonsByUnit(lessons: Lesson[]): Record<string, Lesson[]> {
  const map: Record<string, Lesson[]> = {}
  for (const l of lessons) {
    const key = l.unit_id ?? '__unassigned'
    if (!map[key]) map[key] = []
    map[key].push(l)
  }
  return map
}

function lessonKey(week: number, day: number, title: string): string {
  return `${week}:${day}:${title}`
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function PlanPage() {
  const language = useLanguageStore((s) => s.activeLanguage)
  const needsRefresh = useLanguageStore((s) => s.needsRefresh)
  const isSwitching = useLanguageStore((s) => s.isSwitching)
  const planId = useLanguageStore(
    (s) => s.userLanguages.find((l) => l.is_active)?.plan?.id
  )

  if (isSwitching) return <PageLoading />
  if (!language || needsRefresh) return <PlanLanguageRecovery />
  return (
    <PlanContent key={`${language.code}:${planId ?? ''}`} language={language} />
  )
}

function PlanLoadError({ onRetry }: { onRetry: () => void }) {
  const t = useTranslations('common')
  return (
    <div className="mx-auto max-w-4xl space-y-4 p-6 text-center">
      <p role="alert" className="text-fl-muted-1">
        {t('errorMessage')}
      </p>
      <button
        className="border-fl-border text-fl-fg hover:bg-fl-surface-2 border px-4 py-2 text-sm"
        onClick={onRetry}
      >
        {t('retry')}
      </button>
    </div>
  )
}

function PlanLanguageRecovery() {
  const fetchLanguages = useLanguageStore((s) => s.fetchLanguages)
  const [loading, setLoading] = useState(true)
  const [attempt, setAttempt] = useState(0)
  useEffect(() => {
    const controller = new AbortController()
    void fetchLanguages(controller.signal).then(() => {
      if (!controller.signal.aborted) setLoading(false)
    })
    return () => controller.abort()
  }, [fetchLanguages, attempt])
  if (loading) return <PageLoading />
  return (
    <PlanLoadError
      onRetry={() => {
        setLoading(true)
        setAttempt((value) => value + 1)
      }}
    />
  )
}

function PlanContent({ language }: { language: TargetLanguage }) {
  const t = useTranslations('plan')
  const tCommon = useTranslations('common')
  const router = useRouter()
  const langName = language.name

  const [plan, setPlan] = useState<StudyPlan | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [activeDrawer, setActiveDrawer] = useState<CurriculumUnit | null>(null)
  const [todayProgressDay, setTodayProgressDay] = useState<number | null>(null)
  const [pendingLessons, setPendingLessons] = useState<PendingLesson[]>([])
  const [lessonStates, setLessonStates] = useState<
    Record<string, Pick<Lesson, 'id' | 'completed'>>
  >({})
  const [completion, setCompletion] = useState<CompletionState | null>(null)
  const [units, setUnits] = useState<CurriculumUnit[]>([])
  const [unitsLoading, setUnitsLoading] = useState(true)
  const [unitsError, setUnitsError] = useState(false)
  const [unitsAttempt, setUnitsAttempt] = useState(0)
  const [planAttempt, setPlanAttempt] = useState(0)

  useEffect(() => {
    const controller = new AbortController()
    const signal = AbortSignal.any([
      controller.signal,
      AbortSignal.timeout(20_000),
    ])
    const { sessionVersion } = useAuthStore.getState()
    const obsolete = () => {
      const context = useLanguageStore.getState()
      return (
        controller.signal.aborted ||
        context.isSwitching ||
        context.needsRefresh ||
        context.activeLanguage?.code !== language.code ||
        useAuthStore.getState().sessionVersion !== sessionVersion
      )
    }
    async function loadPlan() {
      setLoading(true)
      setError('')
      setCompletion(null)
      setTodayProgressDay(null)
      setLessonStates({})
      setPendingLessons([])
      setActiveDrawer(null)
      // /today can generate a lesson. Its transport lifetime belongs to this
      // context, but it must not consume the read-only plan's 20-second budget.
      const todayRequest = apiFetch('/api/study-plan/today', {
        signal: controller.signal,
      })
        .then(async (res) =>
          res.ok ? ((await res.json()) as TodayResponse) : null
        )
        .catch(() => null)
      try {
        const [planRes, pendingRes, lessonsRes] = await Promise.all([
          apiFetch('/api/study-plan/current', { signal }),
          apiFetch('/api/study-plan/pending-lessons', { signal }).catch(
            () => null
          ),
          apiFetch('/api/study-plan/lessons', { signal }).catch(() => null),
        ])

        if (obsolete()) return
        signal.throwIfAborted()
        if (!planRes.ok) {
          if (planRes.status === 404) {
            router.push('/assessment')
            return
          }
          throw new Error(`Failed to load plan (${planRes.status})`)
        }

        const planData = (await planRes.json()) as StudyPlan | null
        if (obsolete()) return
        signal.throwIfAborted()
        setPlan(planData)
        if (!planData) return

        if (!lessonsRes?.ok) {
          throw new Error('Failed to load lesson progress')
        }

        const states: Record<string, Pick<Lesson, 'id' | 'completed'>> = {}

        const generatedLessons = (await lessonsRes.json()) as PlanLesson[]
        if (obsolete()) return
        signal.throwIfAborted()
        for (const lesson of generatedLessons) {
          states[
            lessonKey(lesson.week_number, lesson.day_number, lesson.title)
          ] = {
            id: lesson.id,
            completed: lesson.is_completed,
          }
        }

        if (pendingRes?.ok) {
          const pendingData = (await pendingRes.json()) as PendingLesson[]
          if (obsolete()) return
          signal.throwIfAborted()
          setPendingLessons(
            pendingData.filter(
              (lesson) =>
                !states[
                  lessonKey(lesson.week_number, lesson.day_number, lesson.title)
                ]?.completed
            )
          )
          for (const lesson of pendingData) {
            const key = lessonKey(
              lesson.week_number,
              lesson.day_number,
              lesson.title
            )
            if (states[key]?.completed) continue
            states[
              lessonKey(lesson.week_number, lesson.day_number, lesson.title)
            ] = {
              id: lesson.id,
              completed: false,
            }
          }
        }

        setLessonStates(states)
        void todayRequest
          .then((todayData) => {
            if (
              obsolete() ||
              !todayData ||
              todayData.plan_id !== planData.id ||
              todayData.progress_day < planData.progress_day
            )
              return
            setTodayProgressDay(todayData.progress_day)
            setCompletion(todayData.completion ?? null)
            const todayStates: typeof states = {}
            for (const lesson of todayData.lessons) {
              if (lesson.id == null) continue
              todayStates[lessonKey(lesson.week, lesson.day, lesson.title)] = {
                id: lesson.id,
                completed: lesson.is_completed ?? false,
              }
            }
            setLessonStates((previous) => {
              const merged = { ...previous }
              for (const [key, state] of Object.entries(todayStates)) {
                // Completion is irreversible; parallel reads can be older than /lessons.
                if (!merged[key]?.completed) merged[key] = state
              }
              return merged
            })
            setPendingLessons((previous) =>
              previous.filter(
                (lesson) =>
                  !todayStates[
                    lessonKey(
                      lesson.week_number,
                      lesson.day_number,
                      lesson.title
                    )
                  ]?.completed
              )
            )
          })
          .catch(() => {
            // An unavailable supplementary response must not hide the loaded plan.
          })
      } catch (err) {
        if (!obsolete())
          setError(err instanceof Error ? err.message : 'Failed to load')
      } finally {
        if (!obsolete()) setLoading(false)
      }
    }
    void loadPlan()
    return () => controller.abort()
  }, [router, language.code, planAttempt])

  useEffect(() => {
    let cancelled = false
    setUnits([])
    setUnitsLoading(true)
    setUnitsError(false)
    if (plan?.cefr_level) {
      void getCurriculumUnits(plan.cefr_level, language.code)
        .then((data) => {
          if (!cancelled) setUnits(data)
        })
        .catch(() => {
          if (!cancelled) setUnitsError(true)
        })
        .finally(() => {
          if (!cancelled) setUnitsLoading(false)
        })
    }
    return () => {
      cancelled = true
    }
  }, [plan?.id, plan?.cefr_level, language.code, unitsAttempt])

  if (loading) {
    return <PageLoading />
  }

  if (error)
    return (
      <PlanLoadError onRetry={() => setPlanAttempt((value) => value + 1)} />
    )
  if (!plan) {
    return <NoPlanBanner />
  }

  const level = plan.cefr_level as CEFRLevel
  const progressDay = todayProgressDay ?? plan.progress_day
  const dayIndex = (lesson: Lesson) =>
    (lesson.week - 1) * plan.days_per_week + lesson.day - 1
  const allLessons = flattenLessons(plan).map((lesson): Lesson => {
    const state = lessonStates[lessonKey(lesson.week, lesson.day, lesson.title)]
    return {
      ...lesson,
      ...state,
      action:
        state?.id != null
          ? state.completed
            ? 'review'
            : dayIndex(lesson) === progressDay
              ? 'start'
              : 'continue'
          : undefined,
    }
  })
  const byUnit = lessonsByUnit(allLessons)
  // The persisted current_unit is only an initial value, not a progress cursor.
  const currentUnitId = allLessons.find(
    (lesson) => dayIndex(lesson) === progressDay
  )?.unit_id
  const completedUnits = new Set(
    Object.entries(byUnit)
      .filter(
        ([, lessons]) =>
          lessons.length > 0 && lessons.every((lesson) => lesson.completed)
      )
      .map(([unitId]) => unitId)
  )

  // The real level test unlocks when the learner reaches the plan's final
  // position, as reported by the backend completion contract.
  const levelTestReady = completion?.state === 'ready'
  const teachingLessons = allLessons.filter(
    (lesson) =>
      lesson.unit_id !== 'completion-test' && lesson.unit_id !== 'level-test'
  )
  const completedLessonCount = teachingLessons.filter(
    (lesson) => lesson.completed
  ).length
  const progressPercent = teachingLessons.length
    ? Math.round((completedLessonCount / teachingLessons.length) * 100)
    : 0
  const progressSummary = t('progressSummary', {
    completed: completedLessonCount,
    total: teachingLessons.length,
  })

  return (
    <div className="mx-auto max-w-4xl space-y-8 px-4 py-8 sm:px-6">
      {/* ── Header ── */}
      <header className="space-y-5">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div className="space-y-2">
            <p className="text-fl-accent text-xs font-medium tracking-widest uppercase">
              {t('learningRoadmap')}
            </p>
            <h1 className="text-fl-fg text-3xl font-semibold">{t('title')}</h1>
          </div>
          <div className="border-fl-border bg-fl-surface flex items-center gap-3 border px-4 py-3">
            <span className="text-fl-muted-1 text-sm">{langName}</span>
            <span className="text-fl-fg font-code text-lg font-semibold">
              <span className="sr-only">{t('level')} </span>
              {level}
            </span>
          </div>
        </div>
        <div className="border-fl-border bg-fl-surface space-y-4 border p-5 sm:p-6">
          <div className="flex flex-wrap items-baseline justify-between gap-2">
            <p className="text-fl-fg text-sm font-medium">{progressSummary}</p>
            <span
              className="text-fl-accent font-code text-sm"
              aria-hidden="true"
            >
              {progressPercent}%
            </span>
          </div>
          <div
            role="progressbar"
            aria-label={progressSummary}
            aria-valuemin={0}
            aria-valuemax={teachingLessons.length || 1}
            aria-valuenow={completedLessonCount}
            className="bg-fl-border h-1.5 overflow-hidden"
          >
            <div
              className="bg-fl-accent h-full transition-[width] duration-300 motion-reduce:transition-none"
              style={{ width: `${progressPercent}%` }}
            />
          </div>
          <div className="text-fl-muted-1 flex flex-wrap items-center justify-between gap-2 text-xs">
            <p>
              {t('durationDetail', {
                weeks: plan.duration_weeks,
                days: plan.days_per_week,
              })}
            </p>
            <p>
              <span>{t('unitsLabel')}</span>{' '}
              <span className="font-code">
                {unitsLoading || unitsError ? '—' : units.length}
              </span>
            </p>
          </div>
        </div>
      </header>

      {/* ── Pending lessons ── */}
      {pendingLessons.length > 0 && (
        <details className="border-fl-border bg-fl-surface border">
          <summary className="focus-visible:outline-fl-fg cursor-pointer px-5 py-4 text-sm focus-visible:outline-2 focus-visible:outline-offset-2">
            <span className="text-fl-fg font-medium">
              {pendingLessons.length} {t('pendingLessons')}
            </span>
            <span className="text-fl-muted-1 mt-1 block text-xs">
              {t('pendingReassurance')}
            </span>
          </summary>
          <div className="divide-fl-border border-fl-border divide-y border-t">
            {pendingLessons.map((lesson) => (
              <div
                key={lesson.id}
                className="flex flex-wrap items-center justify-between gap-3 px-5 py-4"
              >
                <div className="min-w-0 flex-1">
                  <TargetLanguageText
                    as="p"
                    languageCode={language.code}
                    className="text-fl-fg text-sm break-words"
                  >
                    {lesson.title}
                  </TargetLanguageText>
                  <p className="text-fl-muted-1 mt-1 text-xs">
                    {t('weekDay', {
                      week: lesson.week_number,
                      day: lesson.day_number,
                    })}
                  </p>
                </div>
                <button
                  onClick={() => router.push(`/lesson/${lesson.id}`)}
                  className="border-fl-border text-fl-fg hover:bg-fl-surface-2 focus-visible:outline-fl-fg shrink-0 border px-4 py-2 text-sm focus-visible:outline-2 focus-visible:outline-offset-2"
                >
                  {t('resume')}
                </button>
              </div>
            ))}
          </div>
        </details>
      )}

      {/* ── Unit list ── */}
      <div>
        {unitsLoading ? (
          <PageLoading fullScreen={false} />
        ) : unitsError ? (
          <div className="border-fl-border bg-fl-surface space-y-3 border px-6 py-10 text-center">
            <p role="alert" className="text-fl-muted-1 text-sm">
              {tCommon('errorMessage')}
            </p>
            <button
              className="border-fl-border text-fl-fg hover:bg-fl-surface-2 border px-4 py-2 text-sm"
              onClick={() => {
                setUnitsLoading(true)
                setUnitsAttempt((value) => value + 1)
              }}
            >
              {tCommon('retry')}
            </button>
          </div>
        ) : (
          units.length === 0 && (
            <div className="border-fl-border bg-fl-surface space-y-3 border px-6 py-10 text-center">
              <p className="text-fl-muted-3 font-mono text-xs tracking-widest uppercase">
                {t('noUnitsForLevel', { level })}
              </p>
              <p className="text-fl-label text-fl-muted-4 font-mono">
                {t('noUnitsDesc')}
              </p>
            </div>
          )
        )}
        <ol aria-label={t('learningRoadmap')}>
          {units.map((unit, i) => {
            const unitLessons = byUnit[unit.id] ?? []
            const completedLessons = unitLessons.filter(
              (l) => l.completed
            ).length
            const isCompleted = completedUnits.has(unit.id)
            const isActive = unit.id === currentUnitId && !isCompleted
            const activeLesson = unitLessons.find(
              (lesson) =>
                lesson.id != null &&
                !lesson.completed &&
                dayIndex(lesson) === progressDay
            )

            // Reached units and generated lessons stay accessible even after a skipped day.
            const isReached = unitLessons.some(
              (lesson) => dayIndex(lesson) <= progressDay
            )
            const hasGeneratedLessons = unitLessons.some(
              (lesson) => lesson.id != null
            )
            const prereqUnit = unit.prerequisite_unit
            const prereqCompleted = prereqUnit
              ? completedUnits.has(prereqUnit)
              : true
            const isLocked =
              !isReached &&
              !hasGeneratedLessons &&
              !isCompleted &&
              !prereqCompleted &&
              i > 0

            return (
              <li key={unit.id} className="relative pb-5 pl-12 sm:pl-14">
                <span
                  aria-hidden="true"
                  className="bg-fl-border absolute top-9 -bottom-9 left-[18px] w-px"
                />
                <UnitCard
                  title={unit.title}
                  languageCode={language.code}
                  index={i}
                  lessonCount={unitLessons.length || unit.lesson_types.length}
                  grammarCount={unit.grammar_points.length}
                  progress={
                    unitLessons.length > 0
                      ? completedLessons / unitLessons.length
                      : 0
                  }
                  status={{
                    completed: isCompleted,
                    active: isActive,
                    locked: isLocked,
                    isLevelTest: false,
                  }}
                  onClick={() => setActiveDrawer(unit)}
                  onStartLesson={
                    isActive && activeLesson?.id != null
                      ? () => router.push(`/lesson/${activeLesson.id}`)
                      : undefined
                  }
                >
                  {isActive && (
                    <ol
                      aria-label={t('lessonsHeader', {
                        count: unitLessons.length,
                      })}
                      className="border-fl-border space-y-1 border-t px-4 py-3 sm:px-5"
                    >
                      {unitLessons.map((lesson) => {
                        const isCurrent =
                          dayIndex(lesson) === progressDay && !lesson.completed
                        const Icon = lesson.completed
                          ? Check
                          : isCurrent
                            ? ArrowRight
                            : Circle
                        return (
                          <li
                            key={lessonKey(
                              lesson.week,
                              lesson.day,
                              lesson.title
                            )}
                            className={`flex items-start gap-3 py-2 ${isCurrent ? 'text-fl-fg' : 'text-fl-muted-1'}`}
                          >
                            <Icon
                              aria-hidden="true"
                              className={`mt-1 size-4 shrink-0 ${isCurrent ? 'text-fl-accent' : ''}`}
                            />
                            <div className="min-w-0">
                              <span className="sr-only">
                                {t(
                                  lesson.completed
                                    ? 'completed'
                                    : isCurrent
                                      ? 'currentLesson'
                                      : 'lessonPending'
                                )}
                                {': '}
                              </span>
                              <TargetLanguageText
                                languageCode={language.code}
                                className="block text-sm break-words"
                              >
                                {lesson.title}
                              </TargetLanguageText>
                              <span className="text-fl-muted-1 mt-1 block text-xs">
                                {t('weekDay', {
                                  week: lesson.week,
                                  day: lesson.day,
                                })}
                              </span>
                            </div>
                          </li>
                        )
                      })}
                    </ol>
                  )}
                </UnitCard>
              </li>
            )
          })}

          {/* Level test pseudo-unit */}
          {units.length > 0 && (
            <li className="relative pl-12 sm:pl-14">
              <UnitCard
                title={t('completionTestTitle', { level })}
                index={units.length}
                lessonCount={1}
                grammarCount={0}
                progress={
                  plan.completion_test_score != null
                    ? plan.completion_test_score
                    : 0
                }
                status={{
                  completed: plan.completion_test_taken,
                  active: levelTestReady && !plan.completion_test_taken,
                  locked: !levelTestReady && !plan.completion_test_taken,
                  isLevelTest: true,
                }}
                onClick={() => {
                  if (levelTestReady && !plan.completion_test_taken) {
                    router.push(`/assessment/level-test?plan=${plan.id}`)
                  }
                }}
              />
            </li>
          )}
        </ol>
      </div>

      {/* ── Level test banner ── */}
      {levelTestReady && !plan.completion_test_taken && (
        <LevelTestBanner planId={plan.id} level={level} />
      )}

      {/* ── Completion test result ── */}
      {plan.completion_test_taken && (
        <div className="border-fl-border bg-fl-surface space-y-2 border px-6 py-4">
          <p className="text-fl-hint text-fl-muted-3 font-mono tracking-widest uppercase">
            {t('levelTestResult')}
          </p>
          <p className="text-fl-body text-fl-fg font-mono">
            {t('testScore')}{' '}
            <span className="font-bold">
              {plan.completion_test_score != null
                ? `${Math.round(plan.completion_test_score * 100)}%`
                : 'n/a'}
            </span>
          </p>
          {plan.completion_test_recommendation && (
            <p className="text-fl-label text-fl-muted-1 font-mono">
              {plan.completion_test_recommendation}
            </p>
          )}
        </div>
      )}

      {/* ── Active drawer ── */}
      {activeDrawer && (
        <UnitDrawer
          unit={activeDrawer}
          languageCode={language.code}
          lessons={(byUnit[activeDrawer.id] ?? []).map((l) => ({
            ...l,
            completed: l.completed ?? false,
          }))}
          onClose={() => setActiveDrawer(null)}
          onStartLesson={(lessonId) => {
            setActiveDrawer(null)
            router.push(`/lesson/${lessonId}`)
          }}
        />
      )}
    </div>
  )
}
