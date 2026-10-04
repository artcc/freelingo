export type CEFRLevel = 'A1' | 'A2' | 'B1' | 'B2' | 'C1' | 'C2'

export type LessonType =
  | 'grammar'
  | 'vocabulary'
  | 'reading'
  | 'writing'
  | 'review'

export type GrammarCategory =
  | 'Tenses'
  | 'Questions'
  | 'Nouns'
  | 'Pronouns'
  | 'Adjectives & Adverbs'
  | 'Modals'
  | 'Conditionals'
  | 'Passive Voice'
  | 'Reported Speech'
  | 'Clauses'
  | 'Articles'
  | 'Prepositions'
  | 'Phrasal Verbs'
  | 'Advanced'

export type Register = 'formal' | 'neutral' | 'informal'

export type Skill = 'grammar' | 'vocabulary' | 'reading'

export type PartOfSpeech =
  | 'noun'
  | 'verb'
  | 'adjective'
  | 'adverb'
  | 'phrase'
  | 'conjunction'
  | 'preposition'
  | 'numeral'
  | 'pronoun'

export interface AssessmentQuestion {
  id: string
  skill: Skill
  difficulty: CEFRLevel
  question: string
  options: string[]
  /** Never sent by the API: answers are graded server-side via /api/assessment/bank/answer. */
  correct?: string
  grammar_slug?: string
}

export interface VocabularyEntry {
  word: string
  pos: PartOfSpeech
  definition: string
  example: string
  ipa?: string
  frequency_rank?: number
}

export interface VocabularySet {
  id: string
  level: CEFRLevel
  topic: string
  unit_ref: string
  words: VocabularyEntry[]
}

export interface VocabularyNativeHelpWordNote {
  word: string
  meaning: string
  note: string
}

export interface VocabularyNativeHelpTrap {
  mistake: string
  fix: string
}

export interface VocabularyNativeHelpGlossaryItem {
  term: string
  meaning: string
  note?: string | null
}

export interface VocabularyNativeHelp {
  summary: string
  study_tips: string[]
  word_notes: VocabularyNativeHelpWordNote[]
  common_traps: VocabularyNativeHelpTrap[]
  mini_glossary: VocabularyNativeHelpGlossaryItem[]
  practice_prompts: string[]
}
