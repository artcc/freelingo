import { beforeEach, describe, expect, it, vi } from 'vitest'
import { getGrammarTopics, getGrammarNativeHelp } from '@/data/grammar'
import {
  getPhrasebookCategories,
  getPhrasebookByLevel,
} from '@/data/phrasebook'

const { api } = vi.hoisted(() => ({ api: vi.fn() }))
vi.mock('@/lib/api', () => ({ apiFetch: api }))

beforeEach(() => {
  api.mockReset()
})

describe.each([
  {
    name: 'grammar',
    load: (signal?: AbortSignal) => getGrammarTopics('fr-FR', signal),
    field: 'topics',
  },
  {
    name: 'phrasebook',
    load: (signal?: AbortSignal) => getPhrasebookCategories('fr-FR', signal),
    field: 'categories',
  },
  {
    name: 'phrasebook level',
    load: (signal?: AbortSignal) => getPhrasebookByLevel('A1', 'fr-FR', signal),
    field: 'categories',
  },
])('$name catalog contract', ({ load, field }) => {
  it.each([401, 429, 503])(
    'rejects HTTP %s rather than fabricating an empty catalog',
    async (status) => {
      api.mockResolvedValue(new Response(null, { status }))
      await expect(load()).rejects.toThrow('Could not load')
    }
  )

  it('accepts a successful empty catalog', async () => {
    api.mockResolvedValue(Response.json({ [field]: [] }))
    await expect(load()).resolves.toEqual([])
  })

  it('cancels delayed decoding when its caller is aborted', async () => {
    const controller = new AbortController()
    let resolve!: (value: unknown) => void
    api.mockResolvedValue({
      ok: true,
      json: () =>
        new Promise((done) => {
          resolve = done
        }),
    })
    const result = load(controller.signal)
    await Promise.resolve()
    const requestSignal = api.mock.calls[0][1].signal as AbortSignal
    controller.abort()
    expect(requestSignal.aborted).toBe(true)
    resolve({ [field]: [] })
    await expect(result).rejects.toMatchObject({ name: 'AbortError' })
  })

  it('bounds read-only requests to twenty seconds', async () => {
    const deadline = new AbortController()
    const timeout = vi
      .spyOn(AbortSignal, 'timeout')
      .mockReturnValue(deadline.signal)
    api.mockImplementation(
      (_url: string, options: RequestInit) =>
        new Promise((_resolve, reject) => {
          options.signal!.addEventListener('abort', () =>
            reject(options.signal!.reason)
          )
        })
    )
    const result = load()
    deadline.abort(new DOMException('Timed out', 'TimeoutError'))
    await expect(result).rejects.toMatchObject({ name: 'TimeoutError' })
    expect(timeout).toHaveBeenCalledWith(20_000)
  })
})

it('passes cancellation to native help without imposing the catalog deadline', async () => {
  const timeout = vi.spyOn(AbortSignal, 'timeout')
  const controller = new AbortController()
  api.mockResolvedValue(Response.json({ native_help: null }))
  await getGrammarNativeHelp('greetings', 'fr-FR', controller.signal)
  expect(api).toHaveBeenCalledWith(expect.any(String), {
    method: 'POST',
    signal: controller.signal,
  })
  expect(timeout).not.toHaveBeenCalled()
})
