import { act, fireEvent, render, screen, waitFor } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import GamesPage from '@/app/(app)/games/page'
import DetectivePage from '@/app/(app)/games/error-detective/page'
import SentenceOrderPage from '@/app/(app)/games/sentence-order/page'
import VocabularyPairsPage from '@/app/(app)/games/vocabulary-pairs/page'
import { apiFetch } from '@/lib/api'
import { gameRequest, GameRequestError } from '@/lib/detective'
import { getLanguageByCode } from '@/lib/target-languages'
import { useLanguageStore, type UserLanguageInfo } from '@/store/language'
import { useAuthStore } from '@/store/auth'

const { push } = vi.hoisted(() => ({ push: vi.fn() }))
vi.mock('next/navigation', () => ({ useRouter: () => ({ push }) }))
vi.mock('next-intl', () => {
  const translate = (key: string) => key
  return { useTranslations: () => translate }
})
vi.mock('@/lib/api', () => ({ apiFetch: vi.fn() }))
vi.mock('@/lib/detective', async (original) => ({
  ...(await original<typeof import('@/lib/detective')>()),
  gameRequest: vi.fn(),
}))

const track: UserLanguageInfo = {
  target_language: 'en-GB',
  is_active: true,
  plan: {
    id: 1,
    cefr_level: 'A1',
    progress_day: 0,
    total_days: 48,
    completion_pct: 0,
  },
  progress: null,
}
const languageResponse = (plan: UserLanguageInfo['plan']) =>
  new Response(JSON.stringify({ languages: [{ ...track, plan }] }), {
    status: 200,
  })

beforeEach(() => {
  vi.clearAllMocks()
  vi.mocked(apiFetch).mockReset()
  vi.mocked(apiFetch).mockResolvedValue(languageResponse(null))
  vi.mocked(gameRequest).mockReset()
  useAuthStore.setState({ sessionVersion: 1, user: null })
  useLanguageStore.setState({
    activeLanguage: getLanguageByCode('en-GB'),
    userLanguages: [{ ...track, plan: null }],
    needsRefresh: false,
    isSwitching: false,
    invalidationVersion: 0,
  })
})

describe('Games no-plan presentation', () => {
  it('uses the shared assessment view on the games index without a plan', async () => {
    render(<GamesPage />)
    expect(
      await screen.findByRole('heading', { name: 'noPlanTitle' })
    ).toBeVisible()
    expect(screen.queryByRole('link')).not.toBeInTheDocument()
    fireEvent.click(screen.getByRole('button', { name: 'startAssessment' }))
    expect(push).toHaveBeenCalledWith('/assessment')
    expect(apiFetch).toHaveBeenCalledWith('/api/languages', expect.anything())
  })

  it('waits for missing context before showing the game links', async () => {
    useLanguageStore.setState({ activeLanguage: null, userLanguages: [] })
    let resolve!: (response: Response) => void
    vi.mocked(apiFetch).mockReturnValue(
      new Promise((done) => {
        resolve = done
      })
    )
    render(<GamesPage />)
    expect(screen.queryByText('noPlanTitle')).not.toBeInTheDocument()
    expect(screen.queryByRole('link')).not.toBeInTheDocument()
    await act(async () => resolve(languageResponse(track.plan)))
    expect(await screen.findAllByRole('link')).toHaveLength(3)
    expect(screen.queryByText('noPlanTitle')).not.toBeInTheDocument()
  })

  it('keeps failed context loading retryable instead of reporting no plan', async () => {
    useLanguageStore.setState({ needsRefresh: true })
    vi.mocked(apiFetch)
      .mockResolvedValueOnce(new Response('{}', { status: 503 }))
      .mockResolvedValueOnce(languageResponse(null))
    render(<GamesPage />)
    expect(await screen.findByRole('alert')).toHaveTextContent('errorMessage')
    expect(screen.queryByText('noPlanTitle')).not.toBeInTheDocument()
    fireEvent.click(screen.getByRole('button', { name: 'retry' }))
    expect(
      await screen.findByRole('heading', { name: 'noPlanTitle' })
    ).toBeVisible()
    expect(apiFetch).toHaveBeenCalledTimes(2)
  })

  it('keeps a successful context response without an active language retryable', async () => {
    useLanguageStore.setState({ activeLanguage: null, userLanguages: [] })
    vi.mocked(apiFetch).mockResolvedValue(
      new Response(JSON.stringify({ languages: [] }))
    )
    render(<GamesPage />)
    expect(await screen.findByRole('alert')).toBeVisible()
    expect(screen.queryByText('noPlanTitle')).not.toBeInTheDocument()
  })

  it('updates the index after a plan is added and after switching to a planless language', async () => {
    render(<GamesPage />)
    expect(await screen.findByText('noPlanTitle')).toBeVisible()
    act(() => useLanguageStore.setState({ userLanguages: [track] }))
    expect(screen.getAllByRole('link')).toHaveLength(3)
    act(() => useLanguageStore.setState({ isSwitching: true }))
    expect(screen.queryByRole('link')).not.toBeInTheDocument()
    expect(screen.queryByText('noPlanTitle')).not.toBeInTheDocument()
    act(() =>
      useLanguageStore.setState({
        isSwitching: false,
        activeLanguage: getLanguageByCode('ja-JP'),
        userLanguages: [
          { ...track, is_active: false },
          { ...track, target_language: 'ja-JP', plan: null },
        ],
      })
    )
    expect(screen.getByText('noPlanTitle')).toBeVisible()
    expect(screen.queryByRole('link')).not.toBeInTheDocument()
  })

  it('does not reuse the previous account snapshot when the new session lookup fails', async () => {
    render(<GamesPage />)
    expect(await screen.findByText('noPlanTitle')).toBeVisible()
    vi.mocked(apiFetch)
      .mockResolvedValueOnce(new Response('{}', { status: 503 }))
      .mockResolvedValueOnce(languageResponse(track.plan))

    act(() => useAuthStore.getState().startSession('next-account'))
    expect(await screen.findByRole('alert')).toHaveTextContent('errorMessage')
    expect(screen.queryByText('noPlanTitle')).not.toBeInTheDocument()
    expect(screen.queryByRole('link')).not.toBeInTheDocument()
    fireEvent.click(screen.getByRole('button', { name: 'retry' }))
    expect(await screen.findAllByRole('link')).toHaveLength(3)
    expect(screen.queryByText('noPlanTitle')).not.toBeInTheDocument()
  })

  it.each([
    { Page: DetectivePage, path: '/detective?skip=0' },
    { Page: SentenceOrderPage, path: '/sentence-order?skip=0' },
    { Page: VocabularyPairsPage, path: '/vocabulary-pairs?skip=0' },
  ])(
    'uses the shared view for direct entry to $path',
    async ({ Page, path }) => {
      vi.mocked(gameRequest).mockRejectedValue(
        new GameRequestError(404, 'No active study plan found')
      )
      render(<Page />)
      expect(
        await screen.findByRole('heading', { name: 'noPlanTitle' })
      ).toBeVisible()
      expect(screen.queryByText('rules')).not.toBeInTheDocument()
      fireEvent.click(screen.getByRole('button', { name: 'startAssessment' }))
      expect(push).toHaveBeenCalledWith('/assessment')
      await waitFor(() =>
        expect(gameRequest).toHaveBeenCalledWith(path, expect.anything())
      )
    }
  )
})
