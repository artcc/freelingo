import { create } from 'zustand'
import { apiFetch } from '@/lib/api'
import { useAuthStore } from '@/store/auth'

interface FreemiumStatus {
  trial_active: boolean
  trial_ends_at: string | null
  chat_remaining: number
  chat_limit: number
  lessons_remaining: number
  lessons_limit: number
  listening_remaining: number
  listening_limit: number
  reading_remaining: number
  reading_limit: number
  games_remaining: number
  games_limit: number
  voice_remaining_seconds: number
  voice_limit_seconds: number
}

interface FreemiumStore {
  status: FreemiumStatus | null
  loaded: boolean
  lastFetch: number
  fetchStatus: (force?: boolean) => Promise<void>
  /** Optimistically decrement a numeric quota counter on the client. */
  decrement: (feature: NumericFreemiumKey) => void
}

type NumericFreemiumKey =
  | 'chat_remaining'
  | 'lessons_remaining'
  | 'listening_remaining'
  | 'reading_remaining'

let statusRequestId = 0
let consumptionVersion = 0
let pendingStatus: Promise<void> | null = null
const DAY_MS = 86_400_000

export const useFreemiumStore = create<FreemiumStore>((set, get) => ({
  status: null,
  loaded: false,
  lastFetch: 0,
  fetchStatus: async (force = false) => {
    const now = Date.now()
    if (!useAuthStore.getState().accessToken) return
    const { status, loaded, lastFetch } = get()
    const trialEnd = Date.parse(status?.trial_ends_at ?? '')
    const crossedTrialEnd = status?.trial_active && trialEnd <= now
    // UTC midnight also covers Monday's weekly replenishment.
    const sameDay = Math.floor(now / DAY_MS) === Math.floor(lastFetch / DAY_MS)
    if (
      !force &&
      loaded &&
      sameDay &&
      !crossedTrialEnd &&
      now - lastFetch < 60_000
    )
      return
    if (!force && pendingStatus) return pendingStatus
    const requestId = ++statusRequestId
    const version = consumptionVersion
    const { sessionVersion } = useAuthStore.getState()
    if (force) set({ lastFetch: 0 })
    const request = (async () => {
      try {
        const res = await apiFetch('/api/freemium/status')
        if (!res.ok) return
        const data: FreemiumStatus = await res.json()
        if (
          requestId !== statusRequestId ||
          useAuthStore.getState().sessionVersion !== sessionVersion
        )
          return
        // A read started before a confirmed consumption may contain the old quota.
        if (version !== consumptionVersion) {
          await get().fetchStatus(true)
          return
        }
        set({ status: data, loaded: true, lastFetch: now })
      } catch {
        // Non-fatal
      }
    })()
    pendingStatus = request
    try {
      await request
    } finally {
      if (requestId === statusRequestId) pendingStatus = null
    }
  },
  decrement: (feature: NumericFreemiumKey) => {
    ++consumptionVersion
    const current = get().status
    if (!current) return
    set({
      status: {
        ...current,
        [feature]: Math.max(0, current[feature] - 1),
      },
    })
  },
}))

// Clear the snapshot itself, not just its TTL: banners and paywalls read it
// directly, including while the next session's request is pending or fails.
useAuthStore.subscribe((state, previous) => {
  if (state.sessionVersion === previous.sessionVersion) return
  ++statusRequestId
  pendingStatus = null
  useFreemiumStore.setState({ status: null, loaded: false, lastFetch: 0 })
})
