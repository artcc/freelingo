export const REVIEW_PROMPT_DISMISS_COOLDOWN_MS = 14 * 24 * 60 * 60 * 1000
export const REVIEW_PROMPT_MAX_DISMISSALS = 3
export const VOICE_REVIEW_PROMPT_MIN_SESSION_MS = 5 * 60 * 1000

interface PlanCompletionSnapshot {
  completion?: { state?: string | null } | null
  progress_day?: number
  total_days?: number
}

export function isPlanPositionComplete(
  payload: PlanCompletionSnapshot
): boolean {
  const state = payload.completion?.state
  if (state === 'ready' || state === 'taken') return true
  if (state) return false
  return (
    typeof payload.progress_day === 'number' &&
    typeof payload.total_days === 'number' &&
    payload.progress_day >= payload.total_days
  )
}

function canAskAfterDismissals(
  dismissal: { count: number; lastDismissedAt: number },
  now: number
): boolean {
  if (dismissal.count >= REVIEW_PROMPT_MAX_DISMISSALS) return false
  if (
    dismissal.lastDismissedAt > 0 &&
    now - dismissal.lastDismissedAt < REVIEW_PROMPT_DISMISS_COOLDOWN_MS
  ) {
    return false
  }
  return true
}

export function shouldShowVoiceReviewPrompt(
  dismissal: { count: number; lastDismissedAt: number },
  sessionDurationMs: number,
  now = Date.now()
): boolean {
  if (sessionDurationMs < VOICE_REVIEW_PROMPT_MIN_SESSION_MS) return false
  return canAskAfterDismissals(dismissal, now)
}

export function shouldShowUnitReviewPrompt(
  dismissal: { count: number; lastDismissedAt: number },
  unitCompleted: boolean,
  now = Date.now()
): boolean {
  if (!unitCompleted) return false
  return canAskAfterDismissals(dismissal, now)
}

export function shouldShowExerciseReviewPrompt(
  dismissal: { count: number; lastDismissedAt: number },
  exerciseCompleted: boolean,
  now = Date.now()
): boolean {
  if (!exerciseCompleted) return false
  return canAskAfterDismissals(dismissal, now)
}
