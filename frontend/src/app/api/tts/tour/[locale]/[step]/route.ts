import { NextRequest, NextResponse } from 'next/server'

const BACKEND_URL = process.env.BACKEND_URL || 'http://backend:8000'

export async function POST(
  request: NextRequest,
  context: { params: Promise<{ locale: string; step: string }> }
) {
  const { locale, step } = await context.params
  const url = new URL(
    `/api/tts/tour/${encodeURIComponent(locale)}/${encodeURIComponent(step)}`,
    BACKEND_URL
  )
  const headers = new Headers({ 'Content-Type': 'application/json' })
  for (const name of [
    'authorization',
    'cookie',
    'x-real-ip',
    'x-forwarded-for',
  ]) {
    const value = request.headers.get(name)
    if (value) headers.set(name, value)
  }
  const signal = AbortSignal.any([request.signal, AbortSignal.timeout(70_000)])
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers,
      body: await request.text(),
      signal,
      cache: 'no-store',
    })
    const body = await response.arrayBuffer()
    const outgoing = new Headers({ 'Cache-Control': 'no-store' })
    for (const name of ['content-type', 'retry-after']) {
      const value = response.headers.get(name)
      if (value) outgoing.set(name, value)
    }
    return new NextResponse(body, {
      status: response.status,
      headers: outgoing,
    })
  } catch {
    return NextResponse.json(
      { detail: 'Tour narration is unavailable' },
      { status: signal.aborted ? 504 : 502 }
    )
  }
}
