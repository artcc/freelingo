import { NextRequest } from 'next/server'

const BACKEND_URL = process.env.BACKEND_URL || 'http://backend:8000'
// Bypass the generic rewrite's 30-second timeout. Providers have 60 seconds;
// this proxy allows transport overhead and finishes before the client's 75s.
const WARMUP_PROXY_TIMEOUT_MS = 70_000

export async function POST(request: NextRequest): Promise<Response> {
  const deadline = new AbortController()
  const timeout = setTimeout(() => deadline.abort(), WARMUP_PROXY_TIMEOUT_MS)
  const signal = AbortSignal.any([request.signal, deadline.signal])
  try {
    const headers = new Headers()
    // Preserve the trusted ingress headers used by the backend's IP limiter.
    for (const name of [
      'Authorization',
      'Cookie',
      'Content-Type',
      'X-Real-IP',
      'X-Forwarded-For',
    ]) {
      const value = request.headers.get(name)
      if (value) headers.set(name, value)
    }
    const body = await request.text()
    const backendRes = await fetch(`${BACKEND_URL}/api/conversation/warmup`, {
      method: 'POST',
      headers,
      body: body || undefined,
      signal,
    })
    const responseHeaders = new Headers({ 'Cache-Control': 'no-store' })
    for (const name of ['Content-Type', 'Retry-After']) {
      const value = backendRes.headers.get(name)
      if (value) responseHeaders.set(name, value)
    }
    return new Response(await backendRes.text(), {
      status: backendRes.status,
      headers: responseHeaders,
    })
  } catch (error) {
    if (deadline.signal.aborted && !request.signal.aborted) {
      return Response.json({ detail: 'warmup_proxy_timeout' }, { status: 504 })
    }
    throw error
  } finally {
    clearTimeout(timeout)
  }
}
