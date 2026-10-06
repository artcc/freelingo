import type { DetectiveSession } from '@/lib/detective'

export interface SentenceOrderChallenge {
  index: number
  clue: string
  fragments: string[]
  separator: '' | ' '
  order: number[] | null
  correct?: boolean
  corrected_sentence?: string
  explanation?: string
}

export interface SentenceOrderSession extends Omit<
  DetectiveSession,
  'challenges' | 'game_type'
> {
  game_type: 'sentence-order'
  challenges: SentenceOrderChallenge[]
}
