import { apiFetch } from '@/lib/api'

type Feature = 'listening' | 'reading'
type Failure = 'failed' | 'timeout' | 'unavailable' | 'noActivePlan'

interface ExerciseResponse<T> {
  available: boolean
  exercise: T | null
  generation_status: 'idle' | 'generating' | 'failed'
  generation_error: 'timeout' | 'generation_failed' | 'interrupted' | null
  generation_deadline: string | null
}

export class ExerciseGenerationError extends Error {
  constructor(public readonly code: Failure) {
    super(code)
  }
}

class RetryableError extends Error {
  constructor(public readonly retryAfter = 0) {
    super('Exercise status temporarily unavailable')
  }
}

function pause(ms: number, signal: AbortSignal): Promise<void> {
  signal.throwIfAborted()
  return new Promise((resolve, reject) => {
    const abort = () => {
      clearTimeout(timer)
      reject(signal.reason)
    }
    const timer = setTimeout(() => {
      signal.removeEventListener('abort', abort)
      resolve()
    }, ms)
    signal.addEventListener('abort', abort, { once: true })
  })
}

async function request<T>(
  url: string,
  signal: AbortSignal,
  method = 'GET'
): Promise<T> {
  const response = await apiFetch(url, {
    method,
    signal: AbortSignal.any([signal, AbortSignal.timeout(20_000)]),
  })
  if (response.status === 429 || response.status >= 500) {
    const value = response.headers.get('Retry-After')
    const retryAfter = value
      ? Number.isFinite(Number(value))
        ? Number(value) * 1000
        : Date.parse(value) - Date.now()
      : 0
    throw new RetryableError(
      Number.isFinite(retryAfter) ? Math.max(0, retryAfter) : 0
    )
  }
  if (!response.ok) {
    const body = (await response.json().catch(() => ({}))) as {
      detail?: string
    }
    throw new ExerciseGenerationError(
      body.detail === 'No active study plan found' ? 'noActivePlan' : 'failed'
    )
  }
  return (await response.json()) as T
}

/** Query a shared pool, optionally starting one job. Transport retries never repeat POST. */
export async function resolveExercise<T>({
  feature,
  signal,
  generate = false,
  voice = '',
  onGenerating,
}: {
  feature: Feature
  signal: AbortSignal
  generate?: boolean
  voice?: string
  onGenerating: () => void
}): Promise<T | null> {
  const base = `/api/${feature}`
  let mayStart = generate
  let waiting = false
  let uncertainPost = false
  let failures = 0
  let deadline: number | null = null

  while (true) {
    signal.throwIfAborted()
    try {
      const data = await request<ExerciseResponse<T>>(`${base}/next`, signal)
      signal.throwIfAborted()
      if (data.available && data.exercise) return data.exercise
      if (data.generation_status === 'generating') {
        mayStart = false
        waiting = true
        onGenerating()
        // Keep the first deadline, so a succession of other users' jobs cannot extend our wait.
        const serverDeadline = data.generation_deadline
          ? Date.parse(data.generation_deadline)
          : NaN
        deadline ??= Number.isFinite(serverDeadline)
          ? serverDeadline + 10_000
          : Date.now() + 60_000
        if (Date.now() >= deadline) throw new ExerciseGenerationError('timeout')
      } else if (mayStart) {
        mayStart = false
        waiting = true
        onGenerating()
        const query =
          feature === 'listening' && voice
            ? `?voice=${encodeURIComponent(voice)}`
            : ''
        try {
          await request(`${base}/generate${query}`, signal, 'POST')
        } catch (error) {
          if (error instanceof ExerciseGenerationError) throw error
          uncertainPost = true
          // The job may already have been accepted. Only GET is safe to retry here.
          throw error
        }
        continue
      } else if (data.generation_status === 'failed') {
        throw new ExerciseGenerationError(
          data.generation_error === 'timeout' ? 'timeout' : 'failed'
        )
      } else {
        if (uncertainPost) throw new ExerciseGenerationError('unavailable')
        if (waiting) throw new ExerciseGenerationError('failed')
        return null
      }
      failures = 0
      await pause(
        Math.min(10_000, Math.max(0, (deadline ?? Infinity) - Date.now())),
        signal
      )
    } catch (error) {
      signal.throwIfAborted()
      if (error instanceof ExerciseGenerationError) throw error
      failures += 1
      if (failures >= 4 || (deadline !== null && Date.now() >= deadline)) {
        throw new ExerciseGenerationError('unavailable')
      }
      const backoff = Math.min(10_000 * 2 ** (failures - 1), 60_000)
      const retryAfter = error instanceof RetryableError ? error.retryAfter : 0
      // A very long Retry-After is surfaced rather than holding this screen indefinitely.
      if (retryAfter > 120_000) throw new ExerciseGenerationError('unavailable')
      await pause(Math.max(backoff, retryAfter), signal)
    }
  }
}
