export type { CEFRLevel, Register } from '@/data/types'

import { apiFetch } from '@/lib/api'

export interface Phrase {
  text: string
  context: string
  register: string
  unit_ref?: string
  romanization?: string
}

export interface PhrasebookCategory {
  id: string
  level: string
  situation: string
  icon: string
  phrases: Phrase[]
}

export interface PhrasebookNativeHelpPhraseNote {
  phrase: string
  note: string
}

export interface PhrasebookNativeHelpTrap {
  mistake: string
  fix: string
}

export interface PhrasebookNativeHelpGlossaryItem {
  term: string
  meaning: string
  note?: string
}

export interface PhrasebookNativeHelp {
  summary: string
  usage_tips: string[]
  register_notes: string[]
  phrase_notes: PhrasebookNativeHelpPhraseNote[]
  common_traps: PhrasebookNativeHelpTrap[]
  mini_glossary: PhrasebookNativeHelpGlossaryItem[]
}

export async function getPhrasebookCategories(
  targetLanguage: string = 'en-GB',
  signal?: AbortSignal
): Promise<PhrasebookCategory[]> {
  const requestSignal = signal
    ? AbortSignal.any([signal, AbortSignal.timeout(20_000)])
    : AbortSignal.timeout(20_000)
  const res = await apiFetch(
    `/api/phrasebook?language=${encodeURIComponent(targetLanguage)}`,
    { signal: requestSignal }
  )
  if (!res.ok) throw new Error('Could not load phrasebook categories')
  const data = await res.json()
  requestSignal.throwIfAborted()
  return data.categories ?? []
}

export async function getPhrasebookByLevel(
  level: string,
  targetLanguage: string = 'en-GB',
  signal?: AbortSignal
): Promise<PhrasebookCategory[]> {
  const requestSignal = signal
    ? AbortSignal.any([signal, AbortSignal.timeout(20_000)])
    : AbortSignal.timeout(20_000)
  const res = await apiFetch(
    `/api/phrasebook/level/${encodeURIComponent(level)}?language=${encodeURIComponent(targetLanguage)}`,
    { signal: requestSignal }
  )
  if (!res.ok) throw new Error('Could not load phrasebook categories')
  const data = await res.json()
  requestSignal.throwIfAborted()
  return data.categories ?? []
}

export async function getPhrasebookNativeHelp(
  categoryId: string,
  targetLanguage: string = 'en-GB',
  signal?: AbortSignal
): Promise<PhrasebookNativeHelp | null> {
  const res = await apiFetch(
    `/api/phrasebook/${encodeURIComponent(categoryId)}/native-help?language=${encodeURIComponent(targetLanguage)}`,
    { method: 'POST', signal }
  )
  if (!res.ok) return null
  const data = await res.json()
  signal?.throwIfAborted()
  return data.native_help ?? null
}
