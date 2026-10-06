import { act, fireEvent, render, screen, waitFor, within } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import SessionPage from '@/app/(app)/games/sentence-order/[id]/page'
import CatalogPage from '@/app/(app)/games/sentence-order/page'
import { gameRequest } from '@/lib/detective'
import type { SentenceOrderSession } from '@/lib/sentence-order'
import { useLanguageStore } from '@/store/language'
import { useFreemiumStore } from '@/store/freemium'
import { getLanguageByCode } from '@/lib/target-languages'

const { push } = vi.hoisted(() => ({ push: vi.fn() }))
vi.mock('next/navigation', () => ({ useParams: () => ({ id: 'order-1' }), useRouter: () => ({ push }) }))
vi.mock('next-intl', () => {
  const translate = (key: string, values?: Record<string, unknown>) => values ? `${key}:${Object.values(values).join('|')}` : key
  return { useTranslations: () => translate }
})
vi.mock('@/lib/detective', async (original) => ({ ...await original<typeof import('@/lib/detective')>(), gameRequest: vi.fn() }))
vi.mock('@/components/ui/AudioPlayer', () => ({ AudioPlayer: ({ text }: { text: string }) => <button>audio:{text}</button> }))
vi.mock('@/components/billing/FreemiumQuotaBanner', () => ({ FreemiumQuotaBanner: () => null }))
vi.mock('@/components/billing/PaywallBanner', () => ({ PaywallBanner: () => <div>paywall</div> }))

const initial: SentenceOrderSession = {
  id: 'order-1', game_type: 'sentence-order', study_plan_id: 1, target_language: 'en-GB', native_language: 'es', level: 'A1',
  mode: 'free', status: 'ready', error: null, xp_earned: 0, created_at: '2026-10-06T12:00:00Z', remaining_seconds: null,
  challenges: [{ index: 0, clue: 'Ella va a casa.', fragments: ['home.', 'She', 'goes'], separator: ' ', order: null }],
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

async function arrange() {
  const available = within(await screen.findByRole('group', { name: 'availableFragments' }))
  for (const name of ['She', 'goes', 'home.']) fireEvent.click(available.getByRole('button', { name }))
}

describe('Sentence Order interaction', () => {
  it('builds, removes and reorders fragments before submitting once; audio is revealed only afterwards', async () => {
    const answered = { ...initial, challenges: [{ ...initial.challenges[0], order: [1, 2, 0], correct: true, corrected_sentence: 'She goes home.', explanation: 'El sujeto precede al verbo.' }] }
    vi.mocked(gameRequest).mockResolvedValueOnce(initial).mockResolvedValueOnce(answered)
    render(<SessionPage />)
    expect(await screen.findByRole('button', { name: 'check' })).toBeDisabled()
    expect(screen.queryByRole('button', { name: /audio:/ })).not.toBeInTheDocument()
    expect(screen.getByText('Ella va a casa.')).toHaveAttribute('lang', 'es')
    const available = within(screen.getByRole('group', { name: 'availableFragments' }))
    fireEvent.click(available.getByRole('button', { name: 'goes' }))
    expect(available.getByRole('button', { name: 'goes' })).toBeDisabled()
    fireEvent.click(screen.getByRole('button', { name: 'removeFragment:goes|1' }))
    expect(available.getByRole('button', { name: 'goes' })).toBeEnabled()
    await arrange()
    expect(screen.getByText('She goes home.')).toHaveAttribute('lang', 'en-GB')
    fireEvent.click(screen.getByRole('button', { name: 'check' }))
    expect(await screen.findByRole('button', { name: 'audio:She goes home.' })).toBeInTheDocument()
    expect(screen.getByText('El sujeto precede al verbo.')).toHaveAttribute('lang', 'es')
    expect(vi.mocked(gameRequest).mock.calls[1][1]?.body).toBe(JSON.stringify({ challenge: 0, step: 'order', order: [1, 2, 0] }))
  })

  it('keeps identical fragments independently selectable', async () => {
    vi.mocked(gameRequest).mockResolvedValue({ ...initial, challenges: [{ ...initial.challenges[0], fragments: ['that', 'I know', 'that', 'is true.'] }] })
    render(<SessionPage />)
    const available = within(await screen.findByRole('group', { name: 'availableFragments' }))
    fireEvent.click(available.getByRole('button', { name: 'I know' }))
    const repeated = available.getAllByRole('button', { name: 'that' })
    fireEvent.click(repeated[1])
    expect(repeated[0]).toBeEnabled()
    fireEvent.click(repeated[0])
    fireEvent.click(available.getByRole('button', { name: 'is true.' }))
    expect(screen.getByText('I know that that is true.')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'check' })).toBeEnabled()
  })

  it('preserves persisted CJK language and does not insert spaces in the preview', async () => {
    vi.mocked(gameRequest).mockResolvedValue({ ...initial, target_language: 'ja-JP', challenges: [{ ...initial.challenges[0], fragments: ['学生', '彼女は', 'です。'], separator: '' }] })
    render(<SessionPage />)
    const available = within(await screen.findByRole('group', { name: 'availableFragments' }))
    for (const name of ['彼女は', '学生', 'です。']) fireEvent.click(available.getByRole('button', { name }))
    expect(screen.getByText('彼女は学生です。')).toHaveAttribute('lang', 'ja-JP')
    expect(screen.getByText(/ja-JP · A1/)).toBeInTheDocument()
  })

  it('reloads after an uncertain answer instead of submitting again and resumes at the next challenge', async () => {
    const recovered = { ...initial, challenges: [
      { ...initial.challenges[0], order: [1, 2, 0], correct: true, corrected_sentence: 'She goes home.' },
      { ...initial.challenges[0], index: 1, clue: 'Segunda pista', fragments: ['tea.', 'I', 'like'] },
    ] }
    vi.mocked(gameRequest).mockResolvedValueOnce(initial).mockRejectedValueOnce(new Error('network')).mockResolvedValueOnce(recovered)
    render(<SessionPage />)
    await arrange()
    fireEvent.click(screen.getByRole('button', { name: 'check' }))
    fireEvent.click(await screen.findByRole('button', { name: 'retry' }))
    expect(await screen.findByText('Segunda pista')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'check' })).toBeDisabled()
    expect(vi.mocked(gameRequest).mock.calls.filter(([, options]) => options?.method === 'POST')).toHaveLength(1)
    expect(vi.mocked(gameRequest).mock.lastCall?.[0]).toBe('/sessions/order-1')
  })

  it('shows submitted and corrected sentences in completed results, with audio only for the correction', async () => {
    vi.mocked(gameRequest).mockResolvedValue({ ...initial, status: 'completed', xp_earned: 5, challenges: [{ ...initial.challenges[0], order: [0, 1, 2], correct: false, corrected_sentence: 'She goes home.', explanation: 'El sujeto precede al verbo.' }] })
    render(<SessionPage />)
    expect(await screen.findByText('results:0|5')).toBeInTheDocument()
    expect(screen.getByText('home. She goes')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'audio:She goes home.' })).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'check' })).not.toBeInTheDocument()
  })

  it('rejects a session belonging to another game', async () => {
    vi.mocked(gameRequest).mockResolvedValue({ ...initial, game_type: 'detective' })
    render(<SessionPage />)
    expect(await screen.findByRole('alert')).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'check' })).not.toBeInTheDocument()
  })
})

describe('Sentence Order catalog', () => {
  it('starts the selected game type with the displayed plan and opens its own route', async () => {
    vi.mocked(gameRequest).mockResolvedValueOnce(catalog).mockResolvedValueOnce(initial)
    render(<CatalogPage />)
    fireEvent.click((await screen.findAllByRole('button', { name: 'start' }))[2])
    await waitFor(() => expect(push).toHaveBeenCalledWith('/games/sentence-order/order-1'))
    expect(vi.mocked(gameRequest).mock.calls[0][0]).toBe('/sentence-order?skip=0')
    expect(vi.mocked(gameRequest).mock.calls[1][0]).toBe('/sentence-order')
    expect(JSON.parse(String(vi.mocked(gameRequest).mock.calls[1][1]?.body))).toMatchObject({ study_plan_id: 9, mode: 'free' })
  })

  it('recovers an uncertain creation by its original UUID', async () => {
    vi.mocked(gameRequest).mockResolvedValueOnce(catalog).mockRejectedValueOnce(new Error('network'))
    render(<CatalogPage />)
    fireEvent.click((await screen.findAllByRole('button', { name: 'start' }))[2])
    await waitFor(() => expect(push).toHaveBeenCalled())
    const request = JSON.parse(String(vi.mocked(gameRequest).mock.calls[1][1]?.body))
    expect(push).toHaveBeenCalledWith(`/games/sentence-order/${request.request_id}`)
  })

  it('keeps saved games accessible at zero quota', async () => {
    vi.mocked(gameRequest).mockResolvedValue({ ...catalog, limited: true, quota: { remaining: 0, limit: 3 }, total: 1, history: [initial] })
    render(<CatalogPage />)
    expect(await screen.findByText('paywall')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: /ready/ })).toHaveAttribute('href', '/games/sentence-order/order-1')
    for (const button of screen.getAllByRole('button', { name: 'start' })) expect(button).toBeDisabled()
  })

  it('ignores a late creation response after leaving', async () => {
    let resolve!: (data: SentenceOrderSession) => void
    const pending = new Promise<SentenceOrderSession>((res) => { resolve = res })
    vi.mocked(gameRequest).mockResolvedValueOnce(catalog).mockReturnValueOnce(pending)
    const { unmount } = render(<CatalogPage />)
    fireEvent.click((await screen.findAllByRole('button', { name: 'start' }))[2])
    const signal = vi.mocked(gameRequest).mock.calls[1][1]?.signal
    unmount()
    expect(signal?.aborted).toBe(true)
    await act(async () => resolve(initial))
    expect(push).not.toHaveBeenCalled()
  })
})
