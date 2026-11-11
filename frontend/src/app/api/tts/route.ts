/**
 * TTS proxy — forwards the request to the backend and returns binary audio.
 *
 * A dedicated Route Handler is needed because the generic next.config.ts rewrite
 * would return the response as text/event-stream, breaking binary audio data.
 */

import { NextRequest, NextResponse } from 'next/server'

const BACKEND_URL = process.env.BACKEND_URL || 'http://backend:8000'

export async function POST(request: NextRequest): Promise<NextResponse> {
  const t0 = performance.now()
  const body = await request.text()

  const headers = new Headers()
  headers.set('Content-Type', 'application/json')

  const incomingTraceId = request.headers.get('X-TTS-Trace-ID')
  if (incomingTraceId) headers.set('X-TTS-Trace-ID', incomingTraceId)

  const auth = request.headers.get('Authorization')
  if (auth) headers.set('Authorization', auth)

  const cookie = request.headers.get('Cookie')
  if (cookie) headers.set('Cookie', cookie)

  const fetchStart = performance.now()
  const backendRes = await fetch(`${BACKEND_URL}/api/tts`, {
    method: 'POST',
    headers,
    body,
  })
  const fetchMs = performance.now() - fetchStart

  if (!backendRes.ok) {
    const errorText = await backendRes.text()
    return new NextResponse(errorText, { status: backendRes.status })
  }

  const bufferStart = performance.now()
  const audioBuffer = await backendRes.arrayBuffer()
  const bufferMs = performance.now() - bufferStart
  const totalMs = performance.now() - t0

  const traceId =
    backendRes.headers.get('X-TTS-Trace-ID') ||
    incomingTraceId ||
    `tts-${crypto.randomUUID()}`
  const outHeaders = new Headers()
  outHeaders.set(
    'Content-Type',
    backendRes.headers.get('Content-Type') || 'audio/mpeg'
  )
  outHeaders.set('X-TTS-Trace-ID', traceId)
  outHeaders.set('X-TTS-Proxy-Fetch-Ms', fetchMs.toFixed(1))
  outHeaders.set('X-TTS-Proxy-Buffer-Ms', bufferMs.toFixed(1))
  outHeaders.set('X-TTS-Proxy-Total-Ms', totalMs.toFixed(1))

  const backendSynthMs = backendRes.headers.get('X-TTS-Backend-Synth-Ms')
  const backendTotalMs = backendRes.headers.get('X-TTS-Backend-Total-Ms')
  if (backendSynthMs) outHeaders.set('X-TTS-Backend-Synth-Ms', backendSynthMs)
  if (backendTotalMs) outHeaders.set('X-TTS-Backend-Total-Ms', backendTotalMs)

  return new NextResponse(audioBuffer, {
    status: 200,
    headers: outHeaders,
  })
}
