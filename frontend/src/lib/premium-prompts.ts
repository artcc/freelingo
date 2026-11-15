const COOLDOWN_MS = 3 * 24 * 60 * 60 * 1000

interface PromptPreferences {
  lastOfferedAt: number
  expiredTrialSeen: number
}

const fallback = new Map<number, PromptPreferences>()
const empty: PromptPreferences = { lastOfferedAt: 0, expiredTrialSeen: 0 }

function storageKey(userId: number) {
  return `fl_premium_prompts_${userId}`
}

function readPreferences(userId: number): PromptPreferences {
  try {
    const raw = localStorage.getItem(storageKey(userId))
    if (!raw) return fallback.get(userId) ?? empty
    const value = JSON.parse(raw)
    const pending = fallback.get(userId) ?? empty
    return {
      lastOfferedAt: Math.max(
        pending.lastOfferedAt,
        Number.isFinite(value?.lastOfferedAt) && value.lastOfferedAt > 0
          ? value.lastOfferedAt
          : 0
      ),
      expiredTrialSeen: Math.max(
        pending.expiredTrialSeen,
        Number.isFinite(value?.expiredTrialSeen) && value.expiredTrialSeen > 0
          ? value.expiredTrialSeen
          : 0
      ),
    }
  } catch {
    return fallback.get(userId) ?? empty
  }
}

function writePreferences(userId: number, value: PromptPreferences) {
  fallback.set(userId, value)
  try {
    localStorage.setItem(storageKey(userId), JSON.stringify(value))
    fallback.delete(userId)
  } catch {
    // Keep the frequency limit for this page session when storage is unavailable.
  }
}

export function claimPremiumResultOffer(userId: number, now = Date.now()) {
  const previous = readPreferences(userId)
  if (previous.lastOfferedAt && now - previous.lastOfferedAt < COOLDOWN_MS) {
    return false
  }
  writePreferences(userId, { ...previous, lastOfferedAt: now })
  return true
}

export function hasSeenTrialExpiry(userId: number, trialEnd: number) {
  return readPreferences(userId).expiredTrialSeen === trialEnd
}

export function acknowledgeTrialExpiry(userId: number, trialEnd: number) {
  writePreferences(userId, {
    lastOfferedAt: Date.now(),
    expiredTrialSeen: trialEnd,
  })
}
