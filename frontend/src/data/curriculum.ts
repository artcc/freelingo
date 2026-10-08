import { apiFetch } from '@/lib/api'

export type CEFRLevel = 'A1' | 'A2' | 'B1' | 'B2' | 'C1' | 'C2'

export type LessonType =
  | 'grammar'
  | 'vocabulary'
  | 'reading'
  | 'writing'
  | 'review'

export interface CurriculumUnit {
  id: string
  level: string
  unit_number: number
  title: string
  default_weeks: number
  grammar_points: string[]
  vocabulary_set_ids: string[]
  lesson_types: LessonType[]
  prerequisite_unit?: string
  competency_checklist: string[]
}

export const CEFR_LEVELS = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'] as const

export async function getCurriculumUnits(
  level: string,
  targetLanguage: string = 'en-GB'
): Promise<CurriculumUnit[]> {
  const url = `/api/curriculum/${encodeURIComponent(level)}?language=${encodeURIComponent(targetLanguage)}`
  const res = await apiFetch(url)
  if (!res.ok) throw new Error(`Could not load curriculum (${res.status})`)
  return res.json()
}
