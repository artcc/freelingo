/**
 * Streaming proxy for POST /api/chat
 *
 * next.config.ts rewrites buffer SSE responses before forwarding them,
 * which breaks token-by-token streaming. This Route Handler passes the
 * ReadableStream directly to the browser, preserving true SSE streaming.
 *
 * All other /api/chat/* sub-routes continue to use the rewrite.
 */

import { NextRequest } from 'next/server'

const BACKEND_URL = process.env.BACKEND_URL || 'http://backend:8000'

export async function POST(request: NextRequest) {
  const body = await request.text()

  const headers = new Headers()
  headers.set('Content-Type', 'application/json')
  const userAgent = request.headers.get('User-Agent')
  if (userAgent) headers.set('User-Agent', userAgent)

  const auth = request.headers.get('Authorization')
  if (auth) headers.set('Authorization', auth)

  // Forward cookies so the backend can read the httpOnly refresh token if needed
  const cookie = request.headers.get('Cookie')
  if (cookie) headers.set('Cookie', cookie)

  const backendRes = await fetch(`${BACKEND_URL}/api/chat`, {
    method: 'POST',
    headers,
    body,
  })

  if (!backendRes.ok || !backendRes.body) {
    const errorText = await backendRes.text()
    return new Response(errorText, { status: backendRes.status })
  }

  return new Response(backendRes.body, {
    status: backendRes.status,
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache, no-transform',
      'X-Accel-Buffering': 'no',
    },
  })
}
