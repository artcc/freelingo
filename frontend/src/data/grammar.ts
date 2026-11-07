export type { CEFRLevel, GrammarCategory } from '@/data/types'

import { apiFetch } from '@/lib/api'

export interface GrammarExample {
  text: string
  translation?: string
  note?: string
}

export interface GrammarMistake {
  wrong: string
  correct: string
  note: string
}

export interface GrammarTopic {
  slug: string
  title: string
  level: string
  category: string
  summary: string
  explanation: string
  structure?: string
  rules: string[]
  examples: GrammarExample[]
  common_mistakes: GrammarMistake[]
  related: string[]
}

export interface GrammarNativeHelpExample {
  sentence: string
  note: string
}

export interface GrammarNativeHelpTrap {
  mistake: string
  fix: string
}

export interface GrammarNativeHelpGlossaryItem {
  term: string
  meaning: string
  note?: string
}

export interface GrammarNativeHelp {
  summary: string
  explanation: string
  key_points: string[]
  examples: GrammarNativeHelpExample[]
  common_traps: GrammarNativeHelpTrap[]
  mini_glossary: GrammarNativeHelpGlossaryItem[]
}

export async function getGrammarTopics(
  targetLanguage: string = 'en-GB',
  signal?: AbortSignal
): Promise<GrammarTopic[]> {
  const requestSignal = signal
    ? AbortSignal.any([signal, AbortSignal.timeout(20_000)])
    : AbortSignal.timeout(20_000)
  const res = await apiFetch(
    `/api/grammar?language=${encodeURIComponent(targetLanguage)}`,
    { signal: requestSignal }
  )
  if (!res.ok) throw new Error('Could not load grammar topics')
  const data = await res.json()
  requestSignal.throwIfAborted()
  return data.topics ?? []
}

export async function getGrammarNativeHelp(
  slug: string,
  targetLanguage: string = 'en-GB',
  signal?: AbortSignal
): Promise<GrammarNativeHelp | null> {
  const res = await apiFetch(
    `/api/grammar/${encodeURIComponent(slug)}/native-help?language=${encodeURIComponent(targetLanguage)}`,
    { method: 'POST', signal }
  )
  if (!res.ok) return null
  const data = await res.json()
  signal?.throwIfAborted()
  return data.native_help ?? null
}
