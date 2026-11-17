import { apiFetch } from '@/lib/api'
import { getLanguageByCode } from '@/lib/target-languages'

// Presentation identifiers only; the backend owns availability and tutor context.
export const situationCategories = {
  daily_life: [
    'medical_appointment',
    'neighbour_problem',
    'flat_viewing',
    'school_meeting',
    'household_repair',
  ],
  travel: [
    'change_reservation',
    'hotel_problem',
    'ask_directions',
    'missed_connection',
    'lost_luggage',
  ],
  shopping_services: [
    'return_purchase',
    'restaurant_order',
    'phone_contract',
    'bank_appointment',
    'delivery_problem',
  ],
  social: [
    'meet_someone',
    'make_plans',
    'decline_invitation',
    'resolve_misunderstanding',
    'host_visitors',
  ],
  work: [
    'introduce_yourself',
    'explain_task',
    'clarify_instructions',
    'negotiate_deadline',
    'share_proposal',
  ],
} as const

export type SituationCategory = keyof typeof situationCategories
export type SituationId =
  (typeof situationCategories)[SituationCategory][number]
export interface Situation {
  id: SituationId
  category: SituationCategory
}
export interface SituationCatalog {
  study_plan_id: number
  target_language: string
  cefr_level: string
  situations: Situation[]
}

export class SituationContextError extends Error {}

export function parseSituationSource(params: {
  get: (name: string) => string | null
  getAll: (name: string) => string[]
}): { id: SituationId; studyPlanId: number } | null {
  const id = params.get('situation')
  const plan = params.get('plan')
  if (
    !id ||
    !plan ||
    params.getAll('situation').length !== 1 ||
    params.getAll('plan').length !== 1 ||
    params.get('lesson') !== null ||
    params.get('grammarPractice') !== null ||
    !Object.values(situationCategories).some((items) =>
      (items as readonly string[]).includes(id)
    ) ||
    !/^[1-9]\d*$/.test(plan) ||
    !Number.isSafeInteger(Number(plan)) ||
    Number(plan) > 2_147_483_647
  )
    return null
  return { id: id as SituationId, studyPlanId: Number(plan) }
}

export async function fetchSituationCatalog(
  studyPlanId: number,
  signal: AbortSignal
): Promise<SituationCatalog> {
  const boundedSignal = AbortSignal.any([signal, AbortSignal.timeout(20_000)])
  const response = await apiFetch(
    `/api/situations?study_plan_id=${studyPlanId}`,
    { signal: boundedSignal }
  )
  if (response.status === 404 || response.status === 409)
    throw new SituationContextError('Situation context unavailable')
  if (!response.ok) throw new Error('Situation catalog unavailable')
  const data: unknown = await response.json()
  boundedSignal.throwIfAborted()
  if (!data || typeof data !== 'object')
    throw new Error('Invalid situation catalog')
  const catalog = data as Partial<SituationCatalog>
  if (
    catalog.study_plan_id !== studyPlanId ||
    typeof catalog.target_language !== 'string' ||
    !getLanguageByCode(catalog.target_language) ||
    typeof catalog.cefr_level !== 'string' ||
    !/^[ABC][12]$/.test(catalog.cefr_level) ||
    !Array.isArray(catalog.situations)
  )
    throw new SituationContextError('Invalid situation context')
  const seen = new Set<string>()
  for (const item of catalog.situations) {
    if (
      !item ||
      typeof item !== 'object' ||
      !Object.hasOwn(situationCategories, item.category) ||
      !(situationCategories[item.category] as readonly string[]).includes(
        item.id
      ) ||
      seen.has(item.id)
    )
      throw new Error('Invalid situation catalog entry')
    seen.add(item.id)
  }
  return catalog as SituationCatalog
}
