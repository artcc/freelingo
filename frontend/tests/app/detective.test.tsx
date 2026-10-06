import { act, fireEvent, render, screen, waitFor } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import SessionPage from '@/app/(app)/games/error-detective/[id]/page'
import CatalogPage from '@/app/(app)/games/error-detective/page'
import { gameRequest, type DetectiveSession } from '@/lib/detective'
import { useLanguageStore } from '@/store/language'
import { useFreemiumStore } from '@/store/freemium'
import { getLanguageByCode } from '@/lib/target-languages'

const { push } = vi.hoisted(() => ({ push: vi.fn() }))
vi.mock('next/navigation', () => ({ useParams: () => ({ id: 'game-1' }), useRouter: () => ({ push }) }))
vi.mock('next-intl', () => {
  const translate = (key: string) => key
  return { useTranslations: () => translate }
})
vi.mock('@/lib/detective', async (original) => ({ ...await original<typeof import('@/lib/detective')>(), gameRequest: vi.fn() }))
vi.mock('@/components/ui/AudioPlayer', () => ({ AudioPlayer: ({ text }: { text: string }) => <button>audio:{text}</button> }))
vi.mock('@/components/billing/FreemiumQuotaBanner', () => ({ FreemiumQuotaBanner: () => null }))
vi.mock('@/components/billing/PaywallBanner', () => ({ PaywallBanner: () => <div>paywall</div> }))

const initial: DetectiveSession = {
  id: 'game-1', study_plan_id: 1, target_language: 'en-GB', native_language: 'es', level: 'A1',
  mode: 'free', status: 'ready', error: null, xp_earned: 0, created_at: '2026-10-06T12:00:00Z', remaining_seconds: null,
  challenges: [{ index: 0, sentence: 'She go home.', fragments: ['She ', 'go ', 'home.'], detection: null, correction: null }],
}

beforeEach(() => {
  vi.clearAllMocks()
  useLanguageStore.setState({ activeLanguage: getLanguageByCode('en-GB'), needsRefresh: false, isSwitching: false })
  useFreemiumStore.setState({ fetchStatus: vi.fn().mockResolvedValue(undefined) })
})

describe('Detective session', () => {
  it('reveals correction choices only after detection and uses the shared audio for the corrected sentence', async () => {
    const detected = { ...initial, challenges: [{ ...initial.challenges[0], detection: 1, error_index: 1, options: ['goes ', 'gone ', 'going '] }] }
    const corrected = { ...detected, challenges: [{ ...detected.challenges[0], correction: 0, correct_index: 0, corrected_sentence: 'She goes home.', explanation: 'Con she se añade -s.' }] }
    vi.mocked(gameRequest).mockResolvedValueOnce(initial).mockResolvedValueOnce(detected).mockResolvedValueOnce(corrected)
    render(<SessionPage />)
    fireEvent.click(await screen.findByRole('button', { name: 'go' }))
    fireEvent.click(await screen.findByRole('button', { name: 'goes' }))
    expect(await screen.findByRole('button', { name: 'audio:She goes home.' })).toBeInTheDocument()
    expect(screen.getByText('Con she se añade -s.')).toHaveAttribute('lang', 'es')
    expect(vi.mocked(gameRequest).mock.calls[1][1]?.body).toBe(JSON.stringify({ challenge: 0, step: 'detect', choice: 1 }))
    expect(vi.mocked(gameRequest).mock.calls[2][1]?.body).toBe(JSON.stringify({ challenge: 0, step: 'correct', choice: 0 }))
  })

  it('resumes at correction and does not load the newly selected language into an existing game', async () => {
    useLanguageStore.setState({ activeLanguage: getLanguageByCode('ja-JP') })
    vi.mocked(gameRequest).mockResolvedValue({ ...initial, challenges: [{ ...initial.challenges[0], detection: 0, error_index: 1, options: ['goes', 'gone', 'going'] }] })
    render(<SessionPage />)
    expect(await screen.findByRole('button', { name: 'goes' })).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'She' })).not.toBeInTheDocument()
    expect(screen.getByText('goes')).toHaveAttribute('lang', 'en-GB')
    expect(screen.queryByRole('button', { name: /audio:/ })).not.toBeInTheDocument()
  })

  it('recovers an uncertain answer with GET rather than repeating the submission', async () => {
    vi.mocked(gameRequest).mockResolvedValueOnce(initial).mockRejectedValueOnce(new Error('network')).mockResolvedValueOnce({ ...initial, challenges: [{ ...initial.challenges[0], detection: 1, error_index: 1, options: ['goes', 'gone', 'going'] }] })
    render(<SessionPage />)
    fireEvent.click(await screen.findByRole('button', { name: 'go' }))
    fireEvent.click(await screen.findByRole('button', { name: 'retry' }))
    expect(await screen.findByRole('button', { name: 'goes' })).toBeInTheDocument()
    expect(vi.mocked(gameRequest).mock.calls.filter(([, options]) => options?.method === 'POST')).toHaveLength(1)
  })
})

describe('Detective catalog', () => {
  it.each(['success', 'failure'] as const)(
    'cancels creation on unmount and ignores a late %s',
    async (outcome) => {
      let resolve!: (session: DetectiveSession) => void
      let reject!: (error: Error) => void
      const creation = new Promise<DetectiveSession>((res, rej) => {
        resolve = res
        reject = rej
      })
      vi.mocked(gameRequest).mockResolvedValueOnce({
        study_plan_id: 1, target_language: 'en-GB', level: 'A1', limited: false,
        quota: { remaining: 3, limit: 3 }, total: 0, history: [],
        modes: { review: { available: false }, prepare: { available: false }, free: { available: true } },
      }).mockReturnValueOnce(creation)
      const { unmount } = render(<CatalogPage />)
      fireEvent.click((await screen.findAllByRole('button', { name: 'start' }))[2])
      const signal = vi.mocked(gameRequest).mock.calls[1][1]?.signal
      expect(signal?.aborted).toBe(false)
      unmount()
      expect(signal?.aborted).toBe(true)
      // A transport can settle after cancellation: neither branch may navigate.
      await act(async () => {
        if (outcome === 'success') resolve(initial)
        else reject(new Error('network'))
      })
      expect(push).not.toHaveBeenCalled()
    }
  )

  it('keeps existing games reachable when the free quota is exhausted', async () => {
    vi.mocked(gameRequest).mockResolvedValue({ study_plan_id: 1, target_language: 'en-GB', level: 'A1', limited: true, quota: { remaining: 0, limit: 3 }, total: 1, history: [initial], modes: { review: { available: false }, prepare: { available: false }, free: { available: true } } })
    render(<CatalogPage />)
    expect(await screen.findByText('paywall')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: /ready/ })).toHaveAttribute('href', '/games/error-detective/game-1')
    for (const button of screen.getAllByRole('button', { name: 'start' })) expect(button).toBeDisabled()
  })

  it('passes the displayed plan to generation and opens the returned session', async () => {
    vi.mocked(gameRequest).mockResolvedValueOnce({ study_plan_id: 9, target_language: 'en-GB', level: 'A1', limited: false, quota: { remaining: 3, limit: 3 }, total: 0, history: [], modes: { review: { available: false }, prepare: { available: false }, free: { available: true } } }).mockResolvedValueOnce(initial)
    render(<CatalogPage />)
    const buttons = await screen.findAllByRole('button', { name: 'start' })
    fireEvent.click(buttons[2])
    await waitFor(() => expect(push).toHaveBeenCalledWith('/games/error-detective/game-1'))
    expect(JSON.parse(String(vi.mocked(gameRequest).mock.calls[1][1]?.body))).toMatchObject({ study_plan_id: 9, mode: 'free' })
  })
})
