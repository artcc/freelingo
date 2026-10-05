import { create } from 'zustand'
import {
  SUPPORTED_TARGET_LANGUAGES,
  getLanguageByCode,
} from '@/lib/target-languages'
import type { TargetLanguage } from '@/lib/target-languages'
import { apiFetch } from '@/lib/api'
import { mapUserLanguageInfo } from '@/lib/mappers'

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
    const requestId = ++languageRequestId
    try {
      const requestSignal = AbortSignal.any([
        AbortSignal.timeout(20_000),
        ...(signal ? [signal] : []),
      ])
      const res = await apiFetch('/api/languages', { signal: requestSignal })
      if (!res.ok) return false
      const data = await res.json()
      requestSignal.throwIfAborted()
      if (requestId !== languageRequestId) return false

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
  },

  switchLanguage: async (code: string): Promise<boolean> => {
    set({ isSwitching: true })
    try {
      const res = await apiFetch('/api/languages/active', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ target_language: code }),
      })
      if (!res.ok) return false
      get().invalidateLanguages()
      return await get().fetchLanguages()
    } catch {
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
      await get().fetchLanguages()
      return true
    } catch {
      return false
    }
  },
}))
