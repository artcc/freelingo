import { NextRequest } from 'next/server'
import { proxyAudioGet } from '@/lib/audio-proxy'

export async function GET(
  request: NextRequest,
  context: { params: Promise<{ voice: string }> }
) {
  const { voice } = await context.params
  return proxyAudioGet(request, `/api/tts/preview/${encodeURIComponent(voice)}`)
}
