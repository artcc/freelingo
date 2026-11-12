import { NextRequest } from 'next/server'
import { proxyAudioGet } from '@/lib/audio-proxy'

export async function GET(
  request: NextRequest,
  context: { params: Promise<{ categoryId: string; phraseIndex: string }> }
) {
  const { categoryId, phraseIndex } = await context.params
  return proxyAudioGet(
    request,
    `/api/phrasebook/audio/${encodeURIComponent(categoryId)}/${encodeURIComponent(phraseIndex)}`
  )
}
