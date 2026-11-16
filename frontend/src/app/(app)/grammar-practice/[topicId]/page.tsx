'use client'

import { useParams } from 'next/navigation'
import { PracticeCatalog } from '@/components/grammar-practice/PracticeCatalog'

export default function GrammarPracticeTopicPage() {
  const { topicId } = useParams<{ topicId: string }>()
  return <PracticeCatalog topicId={topicId} />
}
