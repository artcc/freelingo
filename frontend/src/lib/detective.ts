import { apiFetch } from '@/lib/api'
import { getFreemiumAccessFailure } from '@/lib/freemium-access'

export type GameMode = 'review' | 'prepare' | 'free'
export interface Challenge {
  index: number
  sentence: string
  fragments: string[]
  detection: number | null
  correction: number | null
  error_index?: number
  options?: string[]
  correct_index?: number
  corrected_sentence?: string
  explanation?: string
}
export interface DetectiveSession {
  id: string
  game_type?: 'detective' | 'sentence-order' | 'vocabulary-pairs'
  study_plan_id: number
  target_language: string
  native_language: string
  level: string
  mode: GameMode
  status: 'generating' | 'ready' | 'completed' | 'failed' | 'abandoned'
  challenges: Challenge[]
  xp_earned: number
  error: string | null
  created_at: string
  remaining_seconds: number | null
}
export interface DetectiveCatalog {
  study_plan_id: number
  target_language: string
  level: string
  modes: Record<GameMode, { available: boolean; reason: string | null }>
  quota: { remaining: number; limit: number }
  limited: boolean
  history: Omit<DetectiveSession, 'challenges'>[]
  total: number
}

export class GameRequestError extends Error {
  constructor(
    public status: number,
    public code: string,
    public retryAfter = 0
  ) {
    super(code)
  }
}

export async function gameRequest<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const timeout = AbortSignal.timeout(20_000)
  const res = await apiFetch(`/api/games${path}`, {
    cache: 'no-store',
    ...options,
    signal: options.signal
      ? AbortSignal.any([options.signal, timeout])
      : timeout,
    headers: { 'Content-Type': 'application/json', ...options.headers },
  })
  if (!res.ok) {
    const body: unknown = await res.json().catch(() => null)
    const access = getFreemiumAccessFailure(res.status, body, 'games')
    const detail =
      body && typeof body === 'object'
        ? (body as { detail?: unknown }).detail
        : undefined
    const retry = res.headers.get('Retry-After')
    const seconds = retry
      ? /^\d+$/.test(retry)
        ? Number(retry)
        : Math.max(0, (Date.parse(retry) - Date.now()) / 1000)
      : 0
    throw new GameRequestError(
      res.status,
      access === 'exhausted'
        ? 'freemium_exhausted'
        : access === 'unavailable'
          ? 'freemium_unavailable'
          : res.status !== 402 && typeof detail === 'string'
            ? detail
            : 'unavailable',
      Number.isFinite(seconds) ? seconds : 0
    )
  }
  return res.json()
}
