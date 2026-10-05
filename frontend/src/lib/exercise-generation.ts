import { apiFetch } from '@/lib/api'

type Feature = 'listening' | 'reading'
type Failure =
  | 'failed'
  | 'timeout'
  | 'unavailable'
  | 'noActivePlan'
  | 'contextChanged'

export interface ExerciseContext {
  study_plan_id: number
  target_language: string
  level: string
}

interface ExerciseResponse<T> {
  available: boolean
  exercise: (T & { target_language: string; level: string }) | null
  context: ExerciseContext
  generation_status: 'idle' | 'generating' | 'failed'
  generation_error: 'timeout' | 'generation_failed' | 'interrupted' | null
  generation_deadline: string | null
  generation_remaining_seconds: number | null
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
  method = 'GET',
  timeout = 20_000
): Promise<T> {
  const response = await apiFetch(url, {
    method,
    signal: AbortSignal.any([
      signal,
      AbortSignal.timeout(Math.max(1, Math.ceil(timeout))),
    ]),
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
      body.detail === 'study_context_changed'
        ? 'contextChanged'
        : body.detail === 'No active study plan found'
          ? 'noActivePlan'
          : 'failed'
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
  context: expectedContext,
  onGenerating,
}: {
  feature: Feature
  signal: AbortSignal
  generate?: boolean
  voice?: string
  context: Pick<ExerciseContext, 'target_language'> & Partial<ExerciseContext>
  onGenerating: () => void
}): Promise<T | null> {
  const base = `/api/${feature}`
  let mayStart = generate
  let waiting = false
  let uncertainPost = false
  let failures = 0
  let deadline: number | null = null
  let generationEnd: number | null = null
  let context = { ...expectedContext }

  const query = () => {
    const params = new URLSearchParams()
    for (const [key, value] of Object.entries(context)) {
      if (value !== undefined) params.set(`expected_${key}`, String(value))
    }
    return params
  }
  const remaining = () =>
    deadline === null ? Infinity : deadline - performance.now()

  while (true) {
    signal.throwIfAborted()
    if (remaining() <= 0) throw new ExerciseGenerationError('timeout')
    try {
      const data = await request<ExerciseResponse<T>>(
        `${base}/next?${query()}`,
        signal,
        'GET',
        Math.min(20_000, remaining())
      )
      signal.throwIfAborted()
      if (!data.context) throw new ExerciseGenerationError('unavailable')
      if (
        Object.entries(context).some(
          ([key, value]) =>
            value !== undefined &&
            value !== data.context[key as keyof ExerciseContext]
        )
      )
        throw new ExerciseGenerationError('contextChanged')
      context = data.context
      if (data.available && data.exercise) {
        if (
          data.exercise.target_language !== context.target_language ||
          data.exercise.level !== context.level
        ) {
          throw new ExerciseGenerationError('contextChanged')
        }
        return data.exercise
      }
      if (data.generation_status === 'generating') {
        mayStart = false
        waiting = true
        onGenerating()
        // Anchor server-calculated remaining time to a monotonic local clock, never wall time.
        // Keep the first budget so other users' jobs cannot extend this operation indefinitely.
        const seconds = data.generation_remaining_seconds
        generationEnd ??=
          performance.now() +
          (seconds !== null && Number.isFinite(seconds)
            ? Math.max(0, seconds) * 1000
            : 60_000)
        deadline ??= generationEnd + 10_000
        // The lookup at generationEnd is the final check, bounded by the remaining grace period.
        if (performance.now() >= generationEnd)
          throw new ExerciseGenerationError('timeout')
      } else if (mayStart) {
        mayStart = false
        waiting = true
        onGenerating()
        const params = query()
        if (feature === 'listening' && voice) params.set('voice', voice)
        try {
          await request(
            `${base}/generate?${params}`,
            signal,
            'POST',
            Math.min(20_000, remaining())
          )
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
        Math.min(
          10_000,
          Math.max(0, (generationEnd ?? Infinity) - performance.now())
        ),
        signal
      )
    } catch (error) {
      signal.throwIfAborted()
      if (error instanceof ExerciseGenerationError) throw error
      failures += 1
      if (remaining() <= 0) throw new ExerciseGenerationError('timeout')
      if (failures >= 4) {
        throw new ExerciseGenerationError('unavailable')
      }
      const backoff = Math.min(10_000 * 2 ** (failures - 1), 60_000)
      const retryAfter = error instanceof RetryableError ? error.retryAfter : 0
      // A very long Retry-After is surfaced rather than holding this screen indefinitely.
      if (retryAfter > 120_000) throw new ExerciseGenerationError('unavailable')
      await pause(Math.min(Math.max(backoff, retryAfter), remaining()), signal)
    }
  }
}
