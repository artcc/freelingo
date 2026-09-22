import { describe, expect, it } from 'vitest'
import {
  REVIEW_PROMPT_DISMISS_COOLDOWN_MS,
  REVIEW_PROMPT_MAX_DISMISSALS,
  VOICE_REVIEW_PROMPT_MIN_SESSION_MS,
  isPlanPositionComplete,
  shouldShowUnitReviewPrompt,
  shouldShowVoiceReviewPrompt,
} from '@/lib/review-prompt-triggers'

describe('review prompt triggers', () => {
  it('does not show voice prompt before the minimum session duration', () => {
    expect(
      shouldShowVoiceReviewPrompt(
        { count: 0, lastDismissedAt: 0 },
        VOICE_REVIEW_PROMPT_MIN_SESSION_MS - 1
      )
    ).toBe(false)
  })

  it('shows voice prompt after a long enough session when there is no cooldown', () => {
    expect(
      shouldShowVoiceReviewPrompt(
        { count: 0, lastDismissedAt: 0 },
        VOICE_REVIEW_PROMPT_MIN_SESSION_MS
      )
    ).toBe(true)
  })

  it('shows unit prompt when a unit was completed', () => {
    expect(
      shouldShowUnitReviewPrompt({ count: 0, lastDismissedAt: 0 }, true)
    ).toBe(true)
  })

  it('does not show unit prompt when no unit was completed', () => {
    expect(
      shouldShowUnitReviewPrompt({ count: 0, lastDismissedAt: 0 }, false)
    ).toBe(false)
  })

  it('does not show during dismissal cooldown', () => {
    const now = 1_000_000_000
    expect(
      shouldShowVoiceReviewPrompt(
        { count: 1, lastDismissedAt: now - 1_000 },
        VOICE_REVIEW_PROMPT_MIN_SESSION_MS,
        now
      )
    ).toBe(false)
    expect(
      shouldShowUnitReviewPrompt(
        { count: 1, lastDismissedAt: now - 1_000 },
        true,
        now
      )
    ).toBe(false)
  })

  it('shows after dismissal cooldown expires', () => {
    const now = 1_000_000_000
    expect(
      shouldShowVoiceReviewPrompt(
        {
          count: 1,
          lastDismissedAt: now - REVIEW_PROMPT_DISMISS_COOLDOWN_MS,
        },
        VOICE_REVIEW_PROMPT_MIN_SESSION_MS,
        now
      )
    ).toBe(true)
  })

  it('does not show after the maximum dismissal count', () => {
    expect(
      shouldShowVoiceReviewPrompt(
        { count: REVIEW_PROMPT_MAX_DISMISSALS, lastDismissedAt: 0 },
        VOICE_REVIEW_PROMPT_MIN_SESSION_MS
      )
    ).toBe(false)
    expect(
      shouldShowUnitReviewPrompt(
        { count: REVIEW_PROMPT_MAX_DISMISSALS, lastDismissedAt: 0 },
        true
      )
    ).toBe(false)
  })
})

describe('plan position completion', () => {
  it('treats the ready completion state as plan completion', () => {
    expect(
      isPlanPositionComplete({
        completion: { state: 'ready' },
        progress_day: 15,
        total_days: 16,
      })
    ).toBe(true)
  })

  it('treats the taken completion state as plan completion', () => {
    expect(
      isPlanPositionComplete({
        completion: { state: 'taken' },
        progress_day: 16,
        total_days: 16,
      })
    ).toBe(true)
  })

  it('trusts an in_progress state even at the final coordinate', () => {
    expect(
      isPlanPositionComplete({
        completion: { state: 'in_progress' },
        progress_day: 16,
        total_days: 16,
      })
    ).toBe(false)
  })

  it('falls back to the legacy exhausted plan', () => {
    expect(isPlanPositionComplete({ progress_day: 16, total_days: 16 })).toBe(
      true
    )
    expect(isPlanPositionComplete({ progress_day: 15, total_days: 16 })).toBe(
      false
    )
  })
})
