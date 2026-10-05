import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { apiFetch } from '@/lib/api'
import { resolveExercise } from '@/lib/exercise-generation'

vi.mock('@/lib/api', () => ({ apiFetch: vi.fn() }))

const api = vi.mocked(apiFetch)
const exercise = { id: 42, target_language: 'en-GB' }
const idle = {
  available: false,
  exercise: null,
  generation_status: 'idle',
  generation_error: null,
  generation_deadline: null,
}
const response = (body: object, status = 200, headers = {}) =>
  new Response(JSON.stringify(body), { status, headers })
const pending = () => ({
  ...idle,
  generation_status: 'generating',
  generation_deadline: new Date(Date.now() + 600_000).toISOString(),
})
const ready = () => response({ ...idle, available: true, exercise })

describe('exercise generation recovery', () => {
  let controller: AbortController
  const onGenerating = vi.fn()
  const start = (
    generate = false,
    feature: 'reading' | 'listening' = 'reading'
  ) =>
    resolveExercise({
      feature,
      generate,
      signal: controller.signal,
      onGenerating,
    })

  beforeEach(() => {
    vi.useFakeTimers()
    vi.resetAllMocks()
    controller = new AbortController()
  })

  afterEach(() => {
    controller.abort()
    vi.useRealTimers()
  })

  it.each(['reading', 'listening'] as const)(
    'retrieves slow %s work without duplicate generation',
    async (feature) => {
      api
        .mockResolvedValueOnce(response(idle))
        .mockResolvedValueOnce(response({ status: 'generating' }, 202))
      for (let i = 0; i < 13; i++)
        api.mockResolvedValueOnce(response(pending()))
      api.mockResolvedValueOnce(ready())
      const result = expect(start(true, feature)).resolves.toEqual(exercise)
      await vi.advanceTimersByTimeAsync(130_000)
      await result
      expect(
        api.mock.calls.filter(([, options]) => options?.method === 'POST')
      ).toHaveLength(1)
      expect(api.mock.calls.every(([url]) => !url.includes('wait=true'))).toBe(
        true
      )
    }
  )

  it('reuses an available exercise before posting', async () => {
    api.mockResolvedValueOnce(ready())
    await expect(start(true)).resolves.toEqual(exercise)
    expect(api).toHaveBeenCalledTimes(1)
  })

  it('resumes an existing job on page entry', async () => {
    api
      .mockResolvedValueOnce(response(pending()))
      .mockResolvedValueOnce(ready())
    const result = expect(start()).resolves.toEqual(exercise)
    await vi.advanceTimersByTimeAsync(10_000)
    await result
    expect(onGenerating).toHaveBeenCalled()
    expect(
      api.mock.calls.every(([, options]) => options?.method === 'GET')
    ).toBe(true)
  })

  it.each([new TypeError('network disconnected'), response({}, 502)])(
    'recovers after transient transport failure',
    async (failure) => {
      api.mockResolvedValueOnce(response(pending()))
      if (failure instanceof Error) api.mockRejectedValueOnce(failure)
      else api.mockResolvedValueOnce(failure)
      api.mockResolvedValueOnce(ready())
      const result = expect(start()).resolves.toEqual(exercise)
      await vi.advanceTimersByTimeAsync(20_000)
      await result
    }
  )

  it('honours Retry-After without repeatedly hitting the endpoint', async () => {
    api
      .mockResolvedValueOnce(response({}, 429, { 'Retry-After': '30' }))
      .mockResolvedValueOnce(ready())
    const result = expect(start()).resolves.toEqual(exercise)
    await vi.advanceTimersByTimeAsync(29_999)
    expect(api).toHaveBeenCalledTimes(1)
    await vi.advanceTimersByTimeAsync(1)
    await result
  })

  it('retrieves a job after losing the POST response without sending it again', async () => {
    api
      .mockResolvedValueOnce(response(idle))
      .mockRejectedValueOnce(new TypeError('POST response lost'))
      .mockResolvedValueOnce(response(pending()))
      .mockResolvedValueOnce(ready())
    const result = expect(start(true)).resolves.toEqual(exercise)
    await vi.advanceTimersByTimeAsync(20_000)
    await result
    expect(
      api.mock.calls.filter(([, options]) => options?.method === 'POST')
    ).toHaveLength(1)
  })

  it('reports real failure instead of silently going idle', async () => {
    api.mockResolvedValueOnce(
      response({
        ...idle,
        generation_status: 'failed',
        generation_error: 'timeout',
      })
    )
    await expect(start()).rejects.toMatchObject({ code: 'timeout' })
    expect(api).toHaveBeenCalledTimes(1)
  })

  it.each([401, 402, 403, 404])(
    'does not retry a definitive HTTP %s',
    async (status) => {
      api.mockResolvedValueOnce(response({}, status))
      await expect(start()).rejects.toMatchObject({ code: 'failed' })
      expect(api).toHaveBeenCalledTimes(1)
    }
  )

  it('makes a final lookup before declaring a deadline exceeded', async () => {
    api
      .mockResolvedValueOnce(
        response({
          ...pending(),
          generation_deadline: new Date(Date.now()).toISOString(),
        })
      )
      .mockResolvedValueOnce(ready())
    const result = expect(start()).resolves.toEqual(exercise)
    await vi.advanceTimersByTimeAsync(10_000)
    await result
  })

  it('bounds recovery when the backend cannot be reached', async () => {
    api.mockRejectedValue(new TypeError('offline'))
    const result = expect(start()).rejects.toMatchObject({
      code: 'unavailable',
    })
    await vi.advanceTimersByTimeAsync(70_000)
    await result
    expect(api).toHaveBeenCalledTimes(4)
  })

  it('cancels a scheduled lookup', async () => {
    api.mockResolvedValue(response(pending()))
    const result = expect(start()).rejects.toMatchObject({ name: 'AbortError' })
    await vi.advanceTimersByTimeAsync(0)
    controller.abort()
    await result
    await vi.advanceTimersByTimeAsync(60_000)
    expect(api).toHaveBeenCalledTimes(1)
  })
})
