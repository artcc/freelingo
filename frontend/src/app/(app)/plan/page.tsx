'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useTranslations } from 'next-intl'
import { PageLoading } from '@/components/ui/page-loading'
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
  current_unit: string
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

interface CompetencyMap {
  [unitId: string]: number // 0–1
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
  const [competencies, setCompetencies] = useState<CompetencyMap>({})
  const [activeDrawer, setActiveDrawer] = useState<CurriculumUnit | null>(null)
  const [activeLessonId, setActiveLessonId] = useState<number | null>(null)
  const [pendingLessons, setPendingLessons] = useState<PendingLesson[]>([])
  const [lessonStates, setLessonStates] = useState<
    Record<string, Pick<Lesson, 'id' | 'completed' | 'action'>>
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
      setActiveLessonId(null)
      // /today can generate a lesson. Its transport lifetime belongs to this
      // context, but it must not consume the read-only plan's 20-second budget.
      const todayRequest = apiFetch('/api/study-plan/today', {
        signal: controller.signal,
      })
        .then(async (res) =>
          res.ok
            ? ((await res.json()) as {
                lessons: TodayLesson[]
                completion?: CompletionState
              })
            : null
        )
        .catch(() => null)
      try {
        const [planRes, compRes, pendingRes, lessonsRes] = await Promise.all([
          apiFetch('/api/study-plan/current', { signal }),
          apiFetch('/api/progress/competencies', { signal }).catch(() => null),
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

        if (compRes?.ok) {
          const compData = await compRes.json()
          if (obsolete()) return
          signal.throwIfAborted()
          // Backend returns [{unit_id, score}, ...] or Record<string, number>
          if (Array.isArray(compData)) {
            const map: CompetencyMap = {}
            for (const item of compData as {
              unit_id: string
              score: number
            }[]) {
              map[item.unit_id] = item.score
            }
            setCompetencies(map)
          } else {
            setCompetencies(compData as CompetencyMap)
          }
        }

        const states: Record<
          string,
          Pick<Lesson, 'id' | 'completed' | 'action'>
        > = {}

        if (lessonsRes?.ok) {
          const generatedLessons = (await lessonsRes.json()) as PlanLesson[]
          if (obsolete()) return
          signal.throwIfAborted()
          for (const lesson of generatedLessons) {
            states[
              lessonKey(lesson.week_number, lesson.day_number, lesson.title)
            ] = {
              id: lesson.id,
              completed: lesson.is_completed,
              action: lesson.is_completed ? 'review' : undefined,
            }
          }
        }

        if (pendingRes?.ok) {
          const pendingData = (await pendingRes.json()) as PendingLesson[]
          if (obsolete()) return
          signal.throwIfAborted()
          setPendingLessons(pendingData)
          for (const lesson of pendingData) {
            states[
              lessonKey(lesson.week_number, lesson.day_number, lesson.title)
            ] = {
              id: lesson.id,
              completed: false,
              action: 'continue',
            }
          }
        }

        setLessonStates(states)
        void todayRequest
          .then((todayData) => {
            if (obsolete() || !todayData) return
            setCompletion(todayData.completion ?? null)
            const nextLesson = todayData.lessons.find(
              (l) => l.id != null && !l.is_completed
            )
            setActiveLessonId(nextLesson?.id ?? null)
            const todayStates: typeof states = {}
            for (const lesson of todayData.lessons) {
              if (lesson.id == null) continue
              todayStates[lessonKey(lesson.week, lesson.day, lesson.title)] = {
                id: lesson.id,
                completed: lesson.is_completed ?? false,
                action: lesson.is_completed ? 'review' : 'start',
              }
            }
            setLessonStates((previous) => ({ ...previous, ...todayStates }))
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
  const allLessons = flattenLessons(plan).map((lesson) => ({
    ...lesson,
    ...lessonStates[lessonKey(lesson.week, lesson.day, lesson.title)],
  }))
  const byUnit = lessonsByUnit(allLessons)
  const currentUnitId = plan.current_unit

  // The real level test unlocks when the learner reaches the plan's final
  // position, as reported by the backend completion contract.
  const levelTestReady = completion?.state === 'ready'

  return (
    <div className="mx-auto max-w-4xl space-y-6 px-4 py-8">
      {/* ── Header ── */}
      <div className="border-fl-border bg-fl-surface border">
        <div className="border-fl-border flex items-center gap-2 border-b px-6 py-4">
          <span className="text-fl-label text-fl-muted-3">●</span>
          <span className="text-fl-label text-fl-muted-2 font-mono tracking-widest uppercase">
            {t('learningRoadmap')}
          </span>
        </div>
        <div className="flex flex-wrap items-center gap-4 px-6 py-4">
          <div>
            <p className="text-fl-hint text-fl-muted-3 font-mono tracking-widest uppercase">
              {langName ? `${langName} — ${t('level')}` : t('level')}
            </p>
            <p className="text-fl-fg font-mono text-2xl font-bold tracking-widest">
              {level}
            </p>
          </div>
          <div className="bg-fl-border h-8 w-px" />
          <div>
            <p className="text-fl-hint text-fl-muted-3 font-mono tracking-widest uppercase">
              {t('duration')}
            </p>
            <p className="text-fl-body text-fl-muted-1 font-mono">
              {t('durationDetail', {
                weeks: plan.duration_weeks,
                days: plan.days_per_week,
              })}
            </p>
          </div>
          <div className="bg-fl-border h-8 w-px" />
          <div>
            <p className="text-fl-hint text-fl-muted-3 font-mono tracking-widest uppercase">
              {t('unitsLabel')}
            </p>
            <p className="text-fl-body text-fl-muted-1 font-mono">
              {unitsLoading || unitsError ? '—' : units.length}
            </p>
          </div>
        </div>
      </div>

      {/* ── Unit list ── */}
      <div className="space-y-2">
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
        {units.map((unit, i) => {
          const unitLessons = byUnit[unit.id] ?? []
          const completedLessons = unitLessons.filter((l) => l.completed).length
          const isActive = unit.id === currentUnitId
          const unitComp = competencies[unit.id] ?? 0
          const isCompleted =
            unitComp >= 0.8 ||
            (completedLessons > 0 && completedLessons === unitLessons.length)

          // A unit is locked if its prerequisite is not completed
          const prereqUnit = unit.prerequisite_unit
          const prereqCompleted = prereqUnit
            ? (competencies[prereqUnit] ?? 0) >= 0.8
            : true
          const isLocked =
            !isActive && !isCompleted && !prereqCompleted && i > 0

          return (
            <UnitCard
              key={unit.id}
              title={unit.title}
              index={i}
              lessonCount={unitLessons.length || unit.lesson_types.length}
              grammarCount={unit.grammar_points.length}
              competency={unitComp}
              status={{
                completed: isCompleted,
                active: isActive,
                locked: isLocked,
                isLevelTest: false,
              }}
              onClick={() => setActiveDrawer(unit)}
              onStartLesson={
                isActive && activeLessonId != null
                  ? () => router.push(`/lesson/${activeLessonId}`)
                  : undefined
              }
            />
          )
        })}

        {/* Level test pseudo-unit */}
        {units.length > 0 && (
          <UnitCard
            title={t('completionTestTitle', { level })}
            index={units.length}
            lessonCount={1}
            grammarCount={0}
            competency={
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
        )}
      </div>

      {/* ── Pending lessons ── */}
      {pendingLessons.length > 0 && (
        <div className="border-fl-border bg-fl-surface border">
          <div className="border-fl-border space-y-2 border-b px-6 py-4">
            <div className="flex items-center gap-2">
              <span className="text-fl-label text-fl-muted-3">●</span>
              <span className="text-fl-label text-fl-muted-2 font-mono tracking-widest uppercase">
                {pendingLessons.length} {t('pendingLessons')}
              </span>
            </div>
            <p className="text-fl-caption text-fl-muted-1 font-mono">
              {t('pendingReassurance')}
            </p>
          </div>
          <div className="divide-fl-border divide-y">
            {pendingLessons.map((lesson) => (
              <div
                key={lesson.id}
                className="flex flex-wrap items-center justify-between gap-3 px-6 py-3"
              >
                <div>
                  <p className="text-fl-fg font-mono text-xs">{lesson.title}</p>
                  <p className="text-fl-hint text-fl-muted-3 mt-0.5 font-mono tracking-widest uppercase">
                    W{lesson.week_number} D{lesson.day_number} ·{' '}
                    {lesson.lesson_type}
                  </p>
                </div>
                <button
                  onClick={() => router.push(`/lesson/${lesson.id}`)}
                  className="text-fl-bg bg-fl-fg hover:bg-fl-fg/90 focus-visible:outline-fl-fg px-3 py-1 font-mono text-sm tracking-widest uppercase transition-colors focus-visible:outline-2 focus-visible:outline-offset-2"
                >
                  {t('resume')}
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

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
