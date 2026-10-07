import type { DetectiveSession } from '@/lib/detective'

export interface VocabularyPair {
  index: number
  term: string
  matched: boolean
  choice?: number
  assisted?: boolean
  sentence?: string
  translation?: string
}

export interface PairAttempt {
  attempt: number
  challenge: number
  choice: number
  correct: boolean
}

export interface VocabularyPairsSession extends Omit<
  DetectiveSession,
  'challenges' | 'game_type'
> {
  game_type: 'vocabulary-pairs'
  challenges: VocabularyPair[]
  meanings: { index: number; text: string }[]
  attempts: PairAttempt[]
}
