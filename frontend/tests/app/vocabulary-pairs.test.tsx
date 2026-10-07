import { act, fireEvent, render, screen, waitFor, within } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import SessionPage from '@/app/(app)/games/vocabulary-pairs/[id]/page'
import CatalogPage from '@/app/(app)/games/vocabulary-pairs/page'
import { gameRequest } from '@/lib/detective'
import type { VocabularyPairsSession } from '@/lib/vocabulary-pairs'
import { useLanguageStore } from '@/store/language'
import { useFreemiumStore } from '@/store/freemium'
import { getLanguageByCode } from '@/lib/target-languages'

const { push } = vi.hoisted(() => ({ push: vi.fn() }))
vi.mock('next/navigation', () => ({ useParams: () => ({ id: 'pairs-1' }), useRouter: () => ({ push }) }))
vi.mock('next-intl', () => {
  const translate = (key: string, values?: Record<string, unknown>) => values ? `${key}:${Object.values(values).join('|')}` : key
  return { useTranslations: () => translate }
})
vi.mock('@/lib/detective', async (original) => ({ ...await original<typeof import('@/lib/detective')>(), gameRequest: vi.fn() }))
vi.mock('@/components/ui/AudioPlayer', () => ({ AudioPlayer: ({ text }: { text: string }) => <button>audio:{text}</button> }))
vi.mock('@/components/billing/FreemiumQuotaBanner', () => ({ FreemiumQuotaBanner: () => null }))
vi.mock('@/components/billing/PaywallBanner', () => ({ PaywallBanner: () => <div>paywall</div> }))

const choices = [2, 4, 1, 0, 3]
const initial: VocabularyPairsSession = {
  id: 'pairs-1', game_type: 'vocabulary-pairs', study_plan_id: 1, target_language: 'en-GB', native_language: 'es', level: 'A1',
  mode: 'free', status: 'ready', error: null, xp_earned: 0, created_at: '2026-10-06T12:00:00Z', remaining_seconds: null,
  challenges: ['cat', 'dog', 'book', 'house', 'tree'].map((term, index) => ({ term, index, matched: false })),
  meanings: ['casa', 'libro', 'gato', 'árbol', 'perro'].map((text, index) => ({ text, index })), attempts: [],
}
const catalog = {
  study_plan_id: 9, target_language: 'en-GB', level: 'A1', limited: false,
  quota: { remaining: 3, limit: 3 }, total: 0, history: [],
  modes: { review: { available: false }, prepare: { available: false }, free: { available: true } },
}

beforeEach(() => {
  vi.resetAllMocks()
  useLanguageStore.setState({ activeLanguage: getLanguageByCode('en-GB'), needsRefresh: false, isSwitching: false })
  useFreemiumStore.setState({ fetchStatus: vi.fn().mockResolvedValue(undefined) })
})

async function selectPair(term: string, meaning: string) {
  fireEvent.click(within(await screen.findByRole('group', { name: 'terms' })).getByRole('button', { name: term }))
  fireEvent.click(within(screen.getByRole('group', { name: 'meanings' })).getByRole('button', { name: meaning }))
}

describe('Vocabulary Pairs', () => {
  it('plays all five pairs after a mistake, preserves attempted combinations and reveals examples at completion', async () => {
    let state = structuredClone(initial)
    vi.mocked(gameRequest).mockResolvedValueOnce(state)
    const wrong = { attempt: 0, challenge: 0, choice: 4, correct: false }
    state = { ...state, attempts: [wrong] }
    vi.mocked(gameRequest).mockResolvedValueOnce(state)
    for (let i = 0; i < 5; i++) {
      state = {
        ...state,
        status: i === 4 ? 'completed' : 'ready', xp_earned: i === 4 ? 11 : 0,
        challenges: state.challenges.map((c) => ({
          ...c, ...(c.index === i ? { matched: true, choice: choices[i], assisted: i < 2 } : {}),
          ...(i === 4 ? { sentence: `Example ${c.term}`, translation: `Traducción ${c.term}` } : {}),
        })),
        attempts: [...state.attempts, { attempt: i + 1, challenge: i, choice: choices[i], correct: true }],
      }
      vi.mocked(gameRequest).mockResolvedValueOnce(state)
    }
    render(<SessionPage />)
    expect(await screen.findByRole('button', { name: 'check' })).toBeDisabled()
    expect(screen.queryByRole('button', { name: /audio:/ })).not.toBeInTheDocument()
    expect(screen.getByText('cat')).toHaveAttribute('lang', 'en-GB')
    expect(screen.getByText('gato')).toHaveAttribute('lang', 'es')
    await selectPair('cat', 'perro')
    fireEvent.click(screen.getByRole('button', { name: 'check' }))
    expect(await screen.findByText(/matchIncorrect/)).toBeInTheDocument()
    await selectPair('cat', 'perro')
    expect(screen.getByText('alreadyTried')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'check' })).toBeDisabled()
    // Deselect; both items remain available for another combination.
    await selectPair('cat', 'perro')
    for (let i = 0; i < 5; i++) {
      await selectPair(initial.challenges[i].term, initial.meanings[choices[i]].text)
      fireEvent.click(screen.getByRole('button', { name: 'check' }))
      expect(await screen.findByRole('button', { name: `audio:${initial.challenges[i].term}` })).toBeInTheDocument()
      if (i < 4) {
        expect(screen.queryByText(/Example/)).not.toBeInTheDocument()
        expect(within(screen.getByRole('group', { name: 'terms' })).getByRole('button', { name: `${initial.challenges[i].term} matched` })).toBeDisabled()
      }
    }
    expect(screen.getByText('results:3|11')).toBeInTheDocument()
    expect(screen.getAllByText(/^Example/)).toHaveLength(5)
    expect(screen.getAllByText(/^Traducción/)).toHaveLength(5)
    expect(screen.queryByRole('button', { name: 'check' })).not.toBeInTheDocument()
    const posts = vi.mocked(gameRequest).mock.calls.filter(([, opts]) => opts?.method === 'POST')
    expect(posts).toHaveLength(6)
    expect(posts.map(([, opts]) => JSON.parse(String(opts?.body)).attempt)).toEqual([0, 1, 2, 3, 4, 5])
  })

  it('recovers an uncertain submission through GET and continues with the persisted attempt number', async () => {
    const recovered = { ...initial, attempts: [{ attempt: 0, challenge: 0, choice: 4, correct: false }] }
    vi.mocked(gameRequest).mockResolvedValueOnce(initial).mockRejectedValueOnce(new Error('network')).mockResolvedValueOnce(recovered).mockResolvedValueOnce(recovered)
    render(<SessionPage />)
    await selectPair('cat', 'perro')
    fireEvent.click(screen.getByRole('button', { name: 'check' }))
    fireEvent.click(await screen.findByRole('button', { name: 'retry' }))
    expect(await screen.findByText(/matchIncorrect/)).toBeInTheDocument()
    expect(vi.mocked(gameRequest).mock.calls[2][0]).toBe('/sessions/pairs-1')
    await selectPair('cat', 'gato')
    fireEvent.click(screen.getByRole('button', { name: 'check' }))
    await waitFor(() => expect(gameRequest).toHaveBeenCalledTimes(4))
    expect(JSON.parse(String(vi.mocked(gameRequest).mock.calls[3][1]?.body))).toEqual({ step: 'match', attempt: 1, challenge: 0, choice: 2 })
  })

  it('aborts a pending answer when leaving and ignores its late result', async () => {
    let resolve!: (data: VocabularyPairsSession) => void
    const pending = new Promise<VocabularyPairsSession>((done) => { resolve = done })
    vi.mocked(gameRequest).mockResolvedValueOnce(initial).mockReturnValueOnce(pending)
    const { unmount } = render(<SessionPage />)
    await selectPair('cat', 'gato')
    fireEvent.click(screen.getByRole('button', { name: 'check' }))
    const signal = vi.mocked(gameRequest).mock.calls[1][1]?.signal
    const invalidate = vi.spyOn(useLanguageStore.getState(), 'invalidateLanguages')
    unmount()
    expect(signal?.aborted).toBe(true)
    await act(async () => resolve(initial))
    expect(invalidate).not.toHaveBeenCalled()
    invalidate.mockRestore()
  })

  it('retains CJK script and persisted language after switching active language', async () => {
    vi.mocked(gameRequest).mockResolvedValue({ ...initial, target_language: 'ja-JP', challenges: [{ ...initial.challenges[0], term: '猫', matched: true, choice: 2, assisted: false }] })
    render(<SessionPage />)
    expect(await screen.findByRole('button', { name: 'audio:猫' })).toBeInTheDocument()
    for (const text of screen.getAllByText('猫')) expect(text).toHaveAttribute('lang', 'ja-JP')
    expect(screen.getByText(/ja-JP · A1/)).toBeInTheDocument()
  })

  it('rejects another game type', async () => {
    vi.mocked(gameRequest).mockResolvedValue({ ...initial, game_type: 'sentence-order' })
    render(<SessionPage />)
    expect(await screen.findByRole('alert')).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'check' })).not.toBeInTheDocument()
  })

  it('starts the third game with the displayed plan and its own route', async () => {
    vi.mocked(gameRequest).mockResolvedValueOnce(catalog).mockResolvedValueOnce(initial)
    render(<CatalogPage />)
    fireEvent.click((await screen.findAllByRole('button', { name: 'start' }))[2])
    await waitFor(() => expect(push).toHaveBeenCalledWith('/games/vocabulary-pairs/pairs-1'))
    expect(vi.mocked(gameRequest).mock.calls[0][0]).toBe('/vocabulary-pairs?skip=0')
    expect(vi.mocked(gameRequest).mock.calls[1][0]).toBe('/vocabulary-pairs')
    expect(JSON.parse(String(vi.mocked(gameRequest).mock.calls[1][1]?.body))).toMatchObject({ study_plan_id: 9, mode: 'free' })
    expect(screen.getByText('freeDescription')).toBeInTheDocument()
  })
})
