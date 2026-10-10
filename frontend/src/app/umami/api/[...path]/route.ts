import { getUmamiConfig } from '@/lib/umami-config'
import { sanitizeUmamiPageview } from '@/lib/umami-payload'

export const dynamic = 'force-dynamic'

export async function POST(
  req: Request,
  { params }: { params: Promise<{ path: string[] }> }
) {
  const config = getUmamiConfig()
  if (!config) return new Response(null, { status: 404 })

  const { path } = await params
  const endpoint = path.join('/')
  if (!['send', 'batch'].includes(endpoint))
    return new Response(null, { status: 404 })
  const url = `${new URL(config.scriptUrl).origin}/api/${endpoint}`

  let body: unknown
  try {
    const raw = await req.text()
    if (raw.length > 65536) return new Response(null, { status: 413 })
    const input: unknown = JSON.parse(raw)
    const hostname = new URL(
      `http://${req.headers.get('host') ?? new URL(req.url).host}`
    ).hostname
    const sanitize = (item: unknown) =>
      sanitizeUmamiPageview(item, config.websiteId, hostname)
    if (endpoint === 'batch') {
      if (!Array.isArray(input) || input.length > 50)
        return new Response(null, { status: 400 })
      const events = input.map(sanitize).filter((item) => item !== null)
      if (!events.length) return Response.json({})
      body = events
    } else {
      body = sanitize(input)
      if (!body) return Response.json({})
    }
  } catch {
    return new Response(null, { status: 400 })
  }
  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': req.headers.get('User-Agent') ?? '',
      },
      body: JSON.stringify(body),
      redirect: 'error',
      signal: AbortSignal.timeout(3_000),
    })
    return new Response(res.body, {
      status: res.status,
      headers: { 'Content-Type': 'application/json' },
    })
  } catch {
    return new Response(null, { status: 502 })
  }
}
