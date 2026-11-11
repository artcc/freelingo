import { NextRequest, NextResponse } from 'next/server'

const BACKEND_URL = process.env.BACKEND_URL || 'http://backend:8000'

/** Cached audio may require synthesis before the backend can send response headers. */
export async function proxyAudioGet(request: NextRequest, path: string) {
  const signal = AbortSignal.any([request.signal, AbortSignal.timeout(60_000)])
  try {
    signal.throwIfAborted()
    const headers = new Headers()
    for (const name of [
      'Authorization',
      'Cookie',
      'X-Real-IP',
      'X-Forwarded-For',
      'Range',
      'If-Range',
    ]) {
      const value = request.headers.get(name)
      if (value) headers.set(name, value)
    }
    const url = new URL(path, BACKEND_URL)
    url.search = request.nextUrl.search
    const response = await fetch(url, {
      method: 'GET',
      headers,
      signal,
      cache: 'no-store',
    })
    const body = await response.arrayBuffer()
    signal.throwIfAborted()
    const outgoing = new Headers({ 'Cache-Control': 'no-store' })
    for (const name of [
      'Content-Type',
      'Retry-After',
      'Accept-Ranges',
      'Content-Range',
      'ETag',
      'Last-Modified',
    ]) {
      const value = response.headers.get(name)
      if (value) outgoing.set(name, value)
    }
    return new NextResponse(body, {
      status: response.status,
      headers: outgoing,
    })
  } catch {
    return NextResponse.json(
      { detail: 'Speech synthesis is unavailable' },
      { status: signal.aborted ? 504 : 502 }
    )
  }
}
