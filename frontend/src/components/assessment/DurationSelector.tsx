'use client'

import { useTranslations } from 'next-intl'

export interface DurationOption {
  weeks: number
  daysPerWeek: number
  intensity: 'intensive' | 'standard' | 'relaxed' | 'very_relaxed'
}

export const DURATION_OPTIONS: DurationOption[] = [
  { weeks: 4, daysPerWeek: 5, intensity: 'intensive' },
  { weeks: 8, daysPerWeek: 5, intensity: 'standard' },
  { weeks: 12, daysPerWeek: 4, intensity: 'relaxed' },
  { weeks: 16, daysPerWeek: 3, intensity: 'very_relaxed' },
]

export const GOAL_OPTIONS = [
  { id: 'grammar' },
  { id: 'vocabulary' },
  { id: 'reading' },
  { id: 'writing' },
  { id: 'conversation' },
  { id: 'listening' },
]

interface Props {
  selectedWeeks: number
  selectedGoals: string[]
  onSelectDuration: (option: DurationOption) => void
  onToggleGoal: (goal: string) => void
  onConfirm: () => void
  onBack: () => void
  cefr_level: string
  loading: boolean
}

export default function DurationSelector({
  selectedWeeks,
  selectedGoals,
  onSelectDuration,
  onToggleGoal,
  onConfirm,
  onBack,
  cefr_level,
  loading,
}: Props) {
  const t = useTranslations('assessment')
  const tCommon = useTranslations('common')
  const selected =
    DURATION_OPTIONS.find((o) => o.weeks === selectedWeeks) ??
    DURATION_OPTIONS[2]

  const intensityMap: Record<string, string> = {
    intensive: t('intensity.intensive'),
    standard: t('intensity.standard'),
    relaxed: t('intensity.relaxed'),
    very_relaxed: t('intensity.veryRelaxed'),
  }

  return (
    <div className="flex min-h-[60vh] items-center justify-center p-6">
      <div className="border-fl-border bg-fl-surface w-full max-w-md border">
        <div className="border-fl-border flex items-center gap-2 border-b px-6 py-4">
          <span className="text-fl-label text-fl-muted-3">●</span>
          <span className="text-fl-label text-fl-muted-2 font-mono tracking-widest uppercase">
            {t('step3')}
          </span>
        </div>

        <div className="space-y-8 p-8">
          {/* Duration */}
          <div>
            <p className="text-fl-hint text-fl-muted-3 mb-3 font-mono tracking-widest uppercase">
              {t('howManyWeeks', { cefr_level })}
            </p>
            <div className="grid grid-cols-2 gap-2">
              {DURATION_OPTIONS.map((opt) => (
                <button
                  key={opt.weeks}
                  onClick={() => onSelectDuration(opt)}
                  className={`border px-4 py-3 text-left transition-colors ${
                    selectedWeeks === opt.weeks
                      ? 'bg-fl-fg text-fl-bg border-fl-fg'
                      : 'border-fl-border text-fl-muted-2 hover:border-fl-border-2 hover:text-fl-fg'
                  }`}
                >
                  <p className="font-mono text-xs font-bold tracking-widest uppercase">
                    {t('nWeeks', { count: opt.weeks })}
                  </p>
                  <p
                    className={`text-fl-hint mt-0.5 font-mono ${
                      selectedWeeks === opt.weeks
                        ? 'opacity-70'
                        : 'text-fl-muted-3'
                    }`}
                  >
                    {intensityMap[opt.intensity]} ·{' '}
                    {t('approxLessons', { count: opt.weeks * opt.daysPerWeek })}
                  </p>
                  <p
                    className={`text-fl-hint mt-0.5 font-mono ${
                      selectedWeeks === opt.weeks
                        ? 'opacity-60'
                        : 'text-fl-muted-3'
                    }`}
                  >
                    {t('daysPerWeek', { count: opt.daysPerWeek })}
                  </p>
                </button>
              ))}
            </div>
          </div>

          {/* Goals */}
          <div>
            <p className="text-fl-hint text-fl-muted-3 mb-3 font-mono tracking-widest uppercase">
              {t('mainGoals')}
            </p>
            <div className="flex flex-wrap gap-2">
              {GOAL_OPTIONS.map((g) => (
                <button
                  key={g.id}
                  onClick={() => onToggleGoal(g.id)}
                  className={`border px-3 py-1.5 font-mono text-xs tracking-widest uppercase transition-colors ${
                    selectedGoals.includes(g.id)
                      ? 'bg-fl-fg text-fl-bg border-fl-fg'
                      : 'border-fl-border text-fl-muted-2 hover:border-fl-border-2 hover:text-fl-fg'
                  }`}
                >
                  {selectedGoals.includes(g.id) ? '✓ ' : ''}
                  {t(
                    `goals.${g.id as 'grammar' | 'vocabulary' | 'reading' | 'writing' | 'conversation' | 'listening'}`
                  )}
                </button>
              ))}
            </div>
          </div>

          {/* Summary */}
          <div className="border-fl-border text-fl-label text-fl-muted-1 space-y-1 border px-4 py-3 font-mono tracking-wide">
            <p>
              {t('summaryLevel')}:{' '}
              <span className="text-fl-fg font-bold">{cefr_level}</span>
            </p>
            <p>
              {t('summaryDuration')}:{' '}
              <span className="text-fl-fg">
                {t('nWeeks', { count: selected.weeks })}
              </span>
              {' · '}
              <span className="text-fl-fg">
                {t('daysPerWeek', { count: selected.daysPerWeek })}
              </span>
            </p>
            <p>
              {t('summaryGoals')}:{' '}
              <span className="text-fl-fg">
                {selectedGoals.length > 0
                  ? selectedGoals
                      .map((g) =>
                        t(
                          `goals.${g as 'grammar' | 'vocabulary' | 'reading' | 'writing' | 'conversation' | 'listening'}`
                        )
                      )
                      .join(', ')
                  : t('noneSelected')}
              </span>
            </p>
          </div>

          <div className="flex gap-2">
            <button
              onClick={onBack}
              className="border-fl-border text-fl-muted-2 hover:border-fl-border-2 hover:text-fl-fg flex-1 border py-3 font-mono text-xs tracking-widest uppercase transition-colors"
            >
              ← {tCommon('back')}
            </button>
            <button
              onClick={onConfirm}
              disabled={loading || selectedGoals.length === 0}
              className="bg-fl-fg text-fl-bg hover:bg-fl-fg-bright flex-[2] py-3 font-mono text-sm font-bold tracking-widest uppercase transition-colors disabled:opacity-40"
            >
              {loading ? t('buildingPlan') : `${t('startMyPlan')} →`}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
