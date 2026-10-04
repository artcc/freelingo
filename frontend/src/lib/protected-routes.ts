// Every authenticated application route under src/app/(app) must be listed
// here so the middleware blocks anonymous access server-side. A unit test
// (protected-routes.test.ts) fails when a new (app) route is added without
// being protected. Public pages live outside (app) and are not listed.
export const PROTECTED_ROUTES = [
  '/admin',
  '/assessment',
  '/billing',
  '/chat',
  '/coach',
  '/conversation',
  '/courses',
  '/dashboard',
  '/faq',
  '/feedback',
  '/flashcards',
  '/friends',
  '/games',
  '/grammar',
  '/leagues',
  '/lesson',
  '/listening',
  '/onboarding',
  '/phrasebook',
  '/plan',
  '/progress',
  '/reading',
  '/review',
  '/settings',
  '/translator',
  '/vocabulary',
] as const

export function isProtectedPath(pathname: string): boolean {
  return PROTECTED_ROUTES.some((route) => pathname === route || pathname.startsWith(route + '/'))
}

// Build the login redirect target. A locale-prefixed request (/ar/dashboard)
// keeps its prefix (/ar/login) and the original destination is preserved in
// `next` so the login page can return the user to where they were going.
export function loginRedirectPath(
  normalizedPath: string,
  search: string,
  localePrefix: string | null,
): string {
  const loginPath = localePrefix ? `/${localePrefix}/login` : '/login'
  const destination = `${localePrefix ? `/${localePrefix}` : ''}${normalizedPath}${search}`
  return `${loginPath}?next=${encodeURIComponent(destination)}`
}
