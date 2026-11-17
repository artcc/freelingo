import { beforeEach, describe, expect, it, vi } from 'vitest'
import { apiFetch } from '@/lib/api'
import {
  fetchSituationCatalog,
  parseSituationSource,
  SituationContextError,
} from '@/lib/situations'

vi.mock('@/lib/api', () => ({ apiFetch: vi.fn() }))

const catalog = {
  study_plan_id: 7,
  target_language: 'fr-FR',
  cefr_level: 'B1',
  situations: [{ id: 'hotel_problem', category: 'travel' }],
}

beforeEach(() => vi.mocked(apiFetch).mockReset())

describe('situation source and catalog validation', () => {
  it('accepts only an explicit known source with its captured plan', () => {
    expect(
      parseSituationSource(
        new URLSearchParams('situation=hotel_problem&plan=7')
      )
    ).toEqual({ id: 'hotel_problem', studyPlanId: 7 })
  })

  it.each([
    '',
    'plan=7',
    'situation=hotel_problem',
    'situation=&plan=7',
    'situation=unknown&plan=7',
    'situation=hotel_problem&plan=0',
    'situation=hotel_problem&plan=-1',
    'situation=hotel_problem&plan=7.5',
    'situation=hotel_problem&plan=1e3',
    'situation=hotel_problem&plan=2147483648',
    'situation=hotel_problem&plan=7&plan=8',
    'situation=hotel_problem&situation=hotel_problem&plan=7',
    'situation=hotel_problem&plan=7&lesson=1',
    'situation=hotel_problem&plan=7&grammarPractice=',
  ])('rejects malformed or conflicting entry %s', (query) => {
    expect(parseSituationSource(new URLSearchParams(query))).toBeNull()
  })

  it('validates returned owner context and presentation identifiers', async () => {
    vi.mocked(apiFetch).mockResolvedValue(
      new Response(JSON.stringify(catalog))
    )
    await expect(
      fetchSituationCatalog(7, new AbortController().signal)
    ).resolves.toEqual(catalog)
    expect(apiFetch).toHaveBeenCalledWith(
      '/api/situations?study_plan_id=7',
      expect.objectContaining({ signal: expect.any(AbortSignal) })
    )
  })

  it.each([
    { study_plan_id: 8 },
    { target_language: 'xx-XX' },
    { cefr_level: 'A9' },
    { situations: [{ id: 'hotel_problem', category: 'work' }] },
    { situations: [{ id: 'unknown', category: 'travel' }] },
    { situations: [null] },
    { situations: [...catalog.situations, ...catalog.situations] },
  ])('rejects invalid response metadata %j', async (override) => {
    vi.mocked(apiFetch).mockResolvedValue(
      new Response(JSON.stringify({ ...catalog, ...override }))
    )
    await expect(
      fetchSituationCatalog(7, new AbortController().signal)
    ).rejects.toThrow()
  })

  it.each([404, 409])('distinguishes stale plan response %s', async (status) => {
    vi.mocked(apiFetch).mockResolvedValue(new Response(null, { status }))
    await expect(
      fetchSituationCatalog(7, new AbortController().signal)
    ).rejects.toBeInstanceOf(SituationContextError)
  })

  it('discards a body decoded after cancellation', async () => {
    const controller = new AbortController()
    vi.mocked(apiFetch).mockResolvedValue({
      ok: true,
      json: async () => {
        controller.abort()
        return catalog
      },
    } as Response)
    await expect(
      fetchSituationCatalog(7, controller.signal)
    ).rejects.toThrow()
  })
})
