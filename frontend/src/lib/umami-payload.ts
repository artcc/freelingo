const PUBLIC_PATHS = [
  '/',
  '/login',
  '/register',
  '/onboarding',
  '/forgot-password',
  '/reset-password',
  '/verify-email',
  '/privacy',
  '/terms',
  '/dashboard',
  '/assessment',
  '/assessment/level-test',
  '/plan',
  '/pending-lessons',
  '/lesson',
  '/chat',
  '/conversation',
  '/listening',
  '/reading',
  '/flashcards',
  '/flashcards/vocabulary',
  '/grammar',
  '/vocabulary',
  '/phrasebook',
  '/games',
  '/games/error-detective',
  '/games/sentence-order',
  '/games/vocabulary-pairs',
  '/progress',
  '/settings',
  '/settings/languages',
  '/settings/memories',
  '/faq',
  '/feedback',
  '/admin',
].sort((a, b) => b.length - a.length)

function object(value: unknown): value is Record<string, unknown> {
  return value !== null && typeof value === 'object' && !Array.isArray(value)
}

export function sanitizeUmamiPageview(
  value: unknown,
  websiteId: string,
  hostname: string
) {
  if (!object(value) || value.type !== 'event' || !object(value.payload))
    return null
  const input = value.payload
  // Browser collection is pageviews only. Product events use the authenticated backend.
  if (
    input.website !== websiteId ||
    input.name ||
    typeof input.url !== 'string' ||
    input.url.length > 4096
  )
    return null
  try {
    const url = new URL(input.url, 'https://freelingo.invalid')
    if (!['http:', 'https:'].includes(url.protocol)) return null
    const path = PUBLIC_PATHS.find(
      (path) =>
        url.pathname === path ||
        (path !== '/' && url.pathname.startsWith(`${path}/`))
    )
    if (!path) return null
    const payload: Record<string, string> = {
      website: websiteId,
      hostname,
      url: path,
      title: path,
      referrer: '',
    }
    if (
      typeof input.language === 'string' &&
      /^[a-z]{2,3}(?:-[a-z0-9]{2,8}){0,3}$/i.test(input.language)
    )
      payload.language = input.language
    if (
      typeof input.screen === 'string' &&
      /^\d{1,5}x\d{1,5}$/.test(input.screen)
    )
      payload.screen = input.screen
    return { type: 'event', payload }
  } catch {
    return null
  }
}
