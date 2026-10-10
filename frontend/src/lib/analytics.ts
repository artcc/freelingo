import { apiUrl } from '@/lib/api'
import { useAuthStore } from '@/store/auth'
import { useConfigStore } from '@/store/config'

export type BrowserEvent =
  | 'grammar_viewed'
  | 'tour_started'
  | 'tour_completed'
  | 'tour_skipped'
  | 'dashboard_lesson_clicked'
  | 'dashboard_plan_clicked'
  | 'dashboard_assessment_clicked'
  | 'dashboard_flashcards_clicked'
  | 'dashboard_chat_clicked'
  | 'dashboard_voice_clicked'
  | 'flashcard_session_started'
  | 'vocabulary_audio_played'
  | 'phrasebook_audio_played'
  | 'progress_calendar_viewed'
  | 'progress_skills_viewed'
  | 'progress_rewards_viewed'
  | 'language_selector_opened'
  | 'appearance_changed'
  | 'voice_changed'
  | 'voice_preview_played'
  | 'faq_viewed'

/** Only closed event names and a transient deduplication nonce go to our backend. */
export function trackBrowserEvent(
  event: BrowserEvent,
  options: { operationId?: string; sessionVersion?: number } = {}
): boolean {
  if (!useConfigStore.getState().analyticsEnabled) return false
  const auth = useAuthStore.getState()
  if (
    options.sessionVersion !== undefined &&
    options.sessionVersion !== auth.sessionVersion
  )
    return false
  const publicEvent = event === 'faq_viewed'
  if (!publicEvent && !auth.accessToken) return false
  try {
    void fetch(apiUrl(`/api/analytics/${publicEvent ? 'public' : 'ui'}`), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(!publicEvent && auth.accessToken
          ? { Authorization: `Bearer ${auth.accessToken}` }
          : {}),
      },
      credentials: 'omit',
      body: JSON.stringify({
        event,
        operation_id: options.operationId ?? crypto.randomUUID(),
      }),
      signal: AbortSignal.timeout(5_000),
      keepalive: true,
    }).catch(() => {})
    return true
  } catch {
    return false
  }
}

export function trackDashboardLink(href: string) {
  try {
    const url = new URL(href, window.location.origin)
    if (url.origin !== window.location.origin) return
    const event: BrowserEvent | undefined = url.pathname.startsWith('/lesson/')
      ? 'dashboard_lesson_clicked'
      : url.pathname === '/assessment' ||
          url.pathname.startsWith('/assessment/')
        ? 'dashboard_assessment_clicked'
        : new Map<string, BrowserEvent>([
            ['/plan', 'dashboard_plan_clicked'],
            ['/flashcards', 'dashboard_flashcards_clicked'],
            ['/chat', 'dashboard_chat_clicked'],
            ['/conversation', 'dashboard_voice_clicked'],
          ]).get(url.pathname)
    if (event) trackBrowserEvent(event)
  } catch {
    // Link navigation does not depend on analytics.
  }
}
