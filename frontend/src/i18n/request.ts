import { readFile } from 'node:fs/promises'
import path from 'node:path'
import { getRequestConfig } from 'next-intl/server'
import { cookies, headers } from 'next/headers'
import { normalizeLocale } from '@/lib/locales'

export default getRequestConfig(async () => {
  const headerStore = await headers()
  const cookieStore = await cookies()

  // x-next-locale is injected by the middleware on every request (including the
  // very first one, before the NEXT_LOCALE cookie has been written to the client)
  const locale = normalizeLocale(
    headerStore.get('x-next-locale') ?? cookieStore.get('NEXT_LOCALE')?.value
  )

  const messagesDirCandidates = [
    path.join(process.cwd(), 'src', 'messages'),
    path.join(process.cwd(), 'messages'),
    path.join(process.cwd(), '..', 'messages'),
    path.join(process.cwd(), '..', '..', 'messages'),
    path.join(process.cwd(), '..', '..', '..', 'messages'),
  ]

  async function loadMessages(requestedLocale: string) {
    for (const messagesDir of messagesDirCandidates) {
      try {
        const file = await readFile(path.join(messagesDir, `${requestedLocale}.json`), 'utf8')
        return JSON.parse(file)
      } catch {
        // Try the next known runtime location.
      }
    }
    return null
  }

  const englishMessages = await loadMessages('en')
  let messages = locale === 'en' ? englishMessages : await loadMessages(locale)

  if (!englishMessages && !messages) {
    throw new Error('No locale messages were found in the application runtime.')
  }

  // Locale files can be translated incrementally without missing-key failures:
  // every locale inherits the complete English message tree.
  const mergeMessages = (base: unknown, override: unknown): unknown => {
    if (!base || typeof base !== 'object' || Array.isArray(base)) return override ?? base
    if (!override || typeof override !== 'object' || Array.isArray(override)) return base
    const merged: Record<string, unknown> = { ...(base as Record<string, unknown>) }
    for (const [key, value] of Object.entries(override as Record<string, unknown>)) {
      merged[key] = mergeMessages(merged[key], value)
    }
    return merged
  }

  if (englishMessages && messages && locale !== 'en') {
    messages = mergeMessages(englishMessages, messages)
  }

  messages ??= englishMessages
  if (!messages) {
    throw new Error('No locale messages were found in the application runtime.')
  }

  // ProgressPage uses this key, and older locale files may not have it yet.
  const progressMessages = (messages as Record<string, unknown>).progress
  if (progressMessages && typeof progressMessages === 'object' && !Array.isArray(progressMessages)) {
    ;(progressMessages as Record<string, unknown>).learningActivity = locale === 'ar' ? 'النشاط التعليمي' : 'Learning activity'
  }

  return {
    locale,
    messages,
  }
})
