import { apiFetch } from '@/lib/api'
import { getFreemiumAccessFailure } from '@/lib/freemium-access'
import { useAuthStore } from '@/store/auth'

export interface PendingPractice {
  topic_id: number
  payload: {
    request_id: string
    study_plan_id: number
    target_language: string
  }
}

export function pendingPracticeKey(topicId: number | string) {
  return `grammar-practice:${useAuthStore.getState().user?.id}:${topicId}`
}

export function readPendingPractice(
  topicId: number | string
): PendingPractice | null {
  const raw = sessionStorage.getItem(pendingPracticeKey(topicId))
  if (!raw) return null
  try {
    const value = JSON.parse(raw)
    if (
      value?.topic_id === Number(topicId) &&
      typeof value.payload?.request_id === 'string' &&
      Number.isInteger(value.payload.study_plan_id) &&
      typeof value.payload.target_language === 'string'
    )
      return value
  } catch {
    // Legacy UUID-only markers cannot replay the original context safely.
  }
  sessionStorage.removeItem(pendingPracticeKey(topicId))
  return null
}

export function findPendingPractice(sessionId: string): PendingPractice | null {
  const prefix = pendingPracticeKey('')
  const keys = Array.from({ length: sessionStorage.length }, (_, index) =>
    sessionStorage.key(index)
  )
  for (const key of keys) {
    if (!key?.startsWith(prefix)) continue
    const pending = readPendingPractice(key.slice(prefix.length))
    if (pending?.payload.request_id === sessionId) return pending
  }
  return null
}

export interface PracticeTopic {
  id: number
  slug: string
  title: string
  level: string
  answered: number
  correct: number
  completed_sessions: number
  last_practiced: string | null
  active_session_id: string | null
}

export interface PracticeChallenge {
  index: number
  type: 'multiple_choice' | 'fill_blank'
  question: string
  options?: string[]
  answer?: number | string
  correct?: boolean
  correct_answer?: string
  explanation?: string
}

export interface PracticeSession {
  id: string
  topic_id: number
  title: string
  study_plan_id: number
  target_language: string
  native_language: string
  topic_level: string
  learner_level: string
  status: 'generating' | 'ready' | 'completed' | 'failed' | 'abandoned'
  error: string | null
  created_at: string
  completed_at: string | null
  remaining_seconds: number | null
  answered: number
  correct: number
  challenges: PracticeChallenge[]
}

interface PracticeContext {
  study_plan_id: number | null
  target_language: string
  quota: { remaining: number; limit: number }
  limited: boolean
  total: number
}

export interface PracticeLibrary extends PracticeContext {
  topics: PracticeTopic[]
}

export interface PracticeHistory extends PracticeContext {
  topic: PracticeTopic
  sessions: PracticeSession[]
}

export class PracticeRequestError extends Error {
  constructor(
    public status: number,
    public code: string,
    public retryAfter = 0,
    public sessionId?: string
  ) {
    super(code)
  }
}

export function uncertainPracticeRequest(error: unknown) {
  return (
    !(error instanceof PracticeRequestError) ||
    error.status >= 500 ||
    error.status === 408
  )
}

export async function practiceRequest<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const timeout = AbortSignal.timeout(20_000)
  const response = await apiFetch(`/api/grammar-practice${path}`, {
    cache: 'no-store',
    ...options,
    signal: options.signal
      ? AbortSignal.any([options.signal, timeout])
      : timeout,
    headers: { 'Content-Type': 'application/json', ...options.headers },
  })
  if (!response.ok) {
    const body = await response.json().catch(() => null)
    const access = getFreemiumAccessFailure(
      response.status,
      body,
      'grammar_practice'
    )
    const detail = body?.detail
    const retry = response.headers.get('Retry-After')
    const seconds = retry
      ? /^\d+$/.test(retry)
        ? Number(retry)
        : Math.max(0, (Date.parse(retry) - Date.now()) / 1000)
      : 0
    throw new PracticeRequestError(
      response.status,
      access === 'exhausted'
        ? 'freemium_exhausted'
        : access === 'unavailable'
          ? 'freemium_unavailable'
          : typeof detail === 'string'
            ? detail
            : typeof detail?.code === 'string'
              ? detail.code
              : 'unavailable',
      Number.isFinite(seconds) ? seconds : 0,
      typeof detail?.session_id === 'string' ? detail.session_id : undefined
    )
  }
  return response.json()
}
