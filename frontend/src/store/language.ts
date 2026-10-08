import { create } from 'zustand'
import {
  SUPPORTED_TARGET_LANGUAGES,
  getLanguageByCode,
} from '@/lib/target-languages'
import type { TargetLanguage } from '@/lib/target-languages'
import { apiFetch } from '@/lib/api'
import { mapUserLanguageInfo } from '@/lib/mappers'
import { useAuthStore } from '@/store/auth'

export interface UserLanguagePlan {
  id: number
  cefr_level: string | null
  progress_day: number
  total_days: number
  completion_pct: number
}

export interface UserLanguageProgress {
  total_xp: number
  current_streak: number
  lessons_completed: number
}

export interface UserLanguageInfo {
  target_language: string
  is_active: boolean
  plan: UserLanguagePlan | null
  progress: UserLanguageProgress | null
}

interface LanguageStore {
  activeLanguage: TargetLanguage | null
  userLanguages: UserLanguageInfo[]
  supportedLanguages: TargetLanguage[]
  availableLanguageCodes: string[]
  isSwitching: boolean
  needsRefresh: boolean
  invalidateLanguages: () => void
  fetchLanguages: (signal?: AbortSignal) => Promise<boolean>
  switchLanguage: (code: string) => Promise<boolean>
  addLanguage: (code: string) => Promise<boolean>
  removeLanguage: (code: string) => Promise<boolean>
}

let languageRequestId = 0
let languageRequest: {
  id: number
  sessionVersion: number
  promise: Promise<boolean>
} | null = null

// A page owns its wait, not the shared recovery of the global language snapshot.
function waitForLanguages(
  promise: Promise<boolean>,
  signal?: AbortSignal
): Promise<boolean> {
  if (!signal) return promise
  if (signal.aborted) return Promise.resolve(false)
  return new Promise((resolve) => {
    const abort = () => resolve(false)
    signal.addEventListener('abort', abort, { once: true })
    void promise.then((ok) => {
      signal.removeEventListener('abort', abort)
      resolve(!signal.aborted && ok)
    })
  })
}

export const useLanguageStore = create<LanguageStore>((set, get) => ({
  activeLanguage: null,
  userLanguages: [],
  supportedLanguages: SUPPORTED_TARGET_LANGUAGES,
  availableLanguageCodes: [],
  isSwitching: false,
  needsRefresh: false,

  invalidateLanguages: () => {
    ++languageRequestId
    set({ needsRefresh: true })
  },

  fetchLanguages: async (signal) => {
    if (signal?.aborted) return false
    const { sessionVersion } = useAuthStore.getState()
    if (
      languageRequest?.id === languageRequestId &&
      languageRequest.sessionVersion === sessionVersion
    ) {
      return waitForLanguages(languageRequest.promise, signal)
    }
    const requestId = ++languageRequestId
    const promise = (async () => {
      try {
        const requestSignal = AbortSignal.timeout(20_000)
        const res = await apiFetch('/api/languages', { signal: requestSignal })
        if (!res.ok) return false
        const data = await res.json()
        requestSignal.throwIfAborted()
        if (
          requestId !== languageRequestId ||
          sessionVersion !== useAuthStore.getState().sessionVersion
        )
          return false

        const languages: UserLanguageInfo[] = (data.languages || []).map(
          mapUserLanguageInfo
        )

        const active = languages.find((l) => l.is_active)
        const activeLang = active
          ? (getLanguageByCode(active.target_language) ?? null)
          : null

        set({
          userLanguages: languages,
          activeLanguage: activeLang,
          availableLanguageCodes: data.all_supported_languages || [],
          needsRefresh: false,
        })
        return true
      } catch {
        // Preserve the last snapshot and its invalidation state so callers can retry.
        return false
      }
    })().finally(() => {
      if (languageRequest?.id === requestId) languageRequest = null
    })
    languageRequest = { id: requestId, sessionVersion, promise }
    return waitForLanguages(promise, signal)
  },

  switchLanguage: async (code: string): Promise<boolean> => {
    if (get().isSwitching) return false
    set({ isSwitching: true })
    try {
      const signal = AbortSignal.timeout(20_000)
      const res = await apiFetch('/api/languages/active', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ target_language: code }),
        signal,
      })
      signal.throwIfAborted()
      if (!res.ok) {
        // Server/proxy failures may hide a committed mutation; reconcile with GET.
        if (res.status >= 500 || res.status === 408) get().invalidateLanguages()
        return false
      }
      get().invalidateLanguages()
      return await get().fetchLanguages()
    } catch {
      // A lost response does not tell us whether the server applied the switch.
      get().invalidateLanguages()
      return false
    } finally {
      set({ isSwitching: false })
    }
  },

  addLanguage: async (code: string): Promise<boolean> => {
    try {
      const res = await apiFetch('/api/languages', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ target_language: code }),
      })
      if (!res.ok) return false
      get().invalidateLanguages()
      await get().fetchLanguages()
      return true
    } catch {
      return false
    }
  },

  removeLanguage: async (code: string): Promise<boolean> => {
    try {
      const res = await apiFetch(`/api/languages/${encodeURIComponent(code)}`, {
        method: 'DELETE',
      })
      if (!res.ok) return false
      get().invalidateLanguages()
      await get().fetchLanguages()
      return true
    } catch {
      return false
    }
  },
}))

// A provisional switch may be rejected. Keep an operation's response until the
// switch settles; its owner then decides whether the original context survived.
// Cancellation releases this wait too, without changing the shared switch.
export function waitForLanguageSwitch(signal: AbortSignal): Promise<void> {
  if (signal.aborted || !useLanguageStore.getState().isSwitching) {
    return Promise.resolve()
  }
  return new Promise((resolve) => {
    const finish = () => {
      unsubscribe()
      signal.removeEventListener('abort', finish)
      resolve()
    }
    const unsubscribe = useLanguageStore.subscribe((state) => {
      if (!state.isSwitching) finish()
    })
    signal.addEventListener('abort', finish, { once: true })
  })
}
