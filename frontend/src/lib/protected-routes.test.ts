import { readdirSync } from 'node:fs'
import { join } from 'node:path'
import { describe, expect, it } from 'vitest'
import { PROTECTED_ROUTES, isProtectedPath, loginRedirectPath } from './protected-routes'

function appRouteSegments(): string[] {
  const appDir = join(process.cwd(), 'src', 'app', '(app)')
  return readdirSync(appDir, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name)
    .filter((name) => !name.startsWith('(') && !name.startsWith('_') && !name.startsWith('['))
}

describe('protected routes', () => {
  it('protects every route segment inside src/app/(app)', () => {
    const missing = appRouteSegments().filter((segment) => !isProtectedPath(`/${segment}`))
    expect(missing).toEqual([])
  })

  it('protects nested paths but not look-alike prefixes', () => {
    expect(isProtectedPath('/courses')).toBe(true)
    expect(isProtectedPath('/vocabulary/review')).toBe(true)
    expect(isProtectedPath('/translator/history')).toBe(true)
    expect(isProtectedPath('/coaching-info')).toBe(false)
    expect(isProtectedPath('/')).toBe(false)
    expect(isProtectedPath('/login')).toBe(false)
  })

  it('has no duplicate entries', () => {
    expect(new Set(PROTECTED_ROUTES).size).toBe(PROTECTED_ROUTES.length)
  })
})

describe('login redirect', () => {
  it('keeps the locale prefix and the destination', () => {
    expect(loginRedirectPath('/dashboard', '', 'ar')).toBe('/ar/login?next=%2Far%2Fdashboard')
    expect(loginRedirectPath('/plan', '?tab=1', 'fr')).toBe('/fr/login?next=%2Ffr%2Fplan%3Ftab%3D1')
  })

  it('uses the unprefixed login page when no locale prefix was given', () => {
    expect(loginRedirectPath('/courses', '', null)).toBe('/login?next=%2Fcourses')
  })
})
