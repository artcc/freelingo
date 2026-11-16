'use client'

import { useParams } from 'next/navigation'
import { PracticeSession } from '@/components/grammar-practice/PracticeSession'

export default function GrammarPracticeSessionPage() {
  const { sessionId } = useParams<{ sessionId: string }>()
  return <PracticeSession sessionId={sessionId} />
}
