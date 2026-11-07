import { act, cleanup, fireEvent, render, screen } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import DetectivePage from '@/app/(app)/games/error-detective/[id]/page'
import SentenceOrderPage from '@/app/(app)/games/sentence-order/[id]/page'
import VocabularyPairsPage from '@/app/(app)/games/vocabulary-pairs/[id]/page'
import { GameCatalog } from '@/components/games/GameCatalog'
import { gameRequest } from '@/lib/detective'
import { useLanguageStore } from '@/store/language'
import { getLanguageByCode } from '@/lib/target-languages'

vi.mock('next/navigation', () => ({
  useParams: () => ({ id: 'game-1' }),
  useRouter: () => ({ push: vi.fn() }),
}))
vi.mock('next-intl', () => {
  const translate = (key: string) => key
  return { useTranslations: () => translate }
})
vi.mock('@/lib/detective', async (original) => ({
  ...(await original<typeof import('@/lib/detective')>()),
  gameRequest: vi.fn(),
}))
vi.mock('@/components/ui/AudioPlayer', () => ({ AudioPlayer: () => null }))

beforeEach(() => {
  vi.resetAllMocks()
  useLanguageStore.setState({
    activeLanguage: getLanguageByCode('en-GB'),
    needsRefresh: false,
    isSwitching: false,
  })
})
afterEach(cleanup)

describe.each([
  { gameType: 'detective', path: 'error-detective', Page: DetectivePage },
  {
    gameType: 'sentence-order',
    path: 'sentence-order',
    Page: SentenceOrderPage,
  },
  {
    gameType: 'vocabulary-pairs',
    path: 'vocabulary-pairs',
    Page: VocabularyPairsPage,
  },
] as const)('$gameType loading', ({ gameType, path, Page }) => {
  it('keeps session navigation visible through initial loading and generation', async () => {
    let resolve!: (value: unknown) => void
    vi.mocked(gameRequest).mockReturnValueOnce(
      new Promise((done) => {
        resolve = done
      })
    )
    const { container } = render(<Page />)
    expect(screen.getByRole('heading', { name: 'title' })).toBeVisible()
    expect(screen.getByRole('link', { name: /back/ })).toHaveAttribute(
      'href',
      `/games/${path}`
    )
    expect(screen.getByRole('status', { name: 'loading' })).toBeVisible()
    expect(screen.getByRole('status')).not.toHaveAttribute('aria-busy')
    expect(container.querySelector('.h-dvh')).toBeNull()
    await act(async () => {
      resolve({
        id: 'game-1',
        game_type: gameType,
        study_plan_id: 1,
        target_language: 'en-GB',
        native_language: 'es',
        level: 'A1',
        mode: 'free',
        status: 'generating',
        error: null,
        xp_earned: 0,
        created_at: '2026-10-06T12:00:00Z',
        remaining_seconds: 60,
        challenges: [],
        attempts: [],
        meanings: [],
      })
    })
    expect(
      screen.getByRole('status', { name: 'generatingDescription' })
    ).toBeVisible()
    expect(screen.getByRole('status')).not.toHaveAttribute('aria-busy')
    expect(screen.getByRole('link', { name: /back/ })).toBeVisible()
    expect(container.querySelector('.h-dvh')).toBeNull()
  })

  it('keeps catalog navigation available and replaces local loading with retry on failure', async () => {
    vi.mocked(gameRequest).mockRejectedValueOnce(new Error('offline'))
    vi.mocked(gameRequest).mockReturnValueOnce(new Promise(() => {}))
    const { container } = render(<GameCatalog gameType={gameType} />)
    expect(screen.getByRole('status', { name: 'loading' })).toBeVisible()
    expect(screen.getByRole('status')).not.toHaveAttribute('aria-busy')
    expect(screen.getByRole('link', { name: /back/ })).toHaveAttribute(
      'href',
      '/games'
    )
    expect(await screen.findByRole('alert')).toHaveTextContent('errorMessage')
    expect(screen.queryByRole('status')).toBeNull()
    fireEvent.click(screen.getByRole('button', { name: 'retry' }))
    expect(screen.getByRole('status', { name: 'loading' })).toBeInTheDocument()
    expect(container.querySelector('.h-dvh')).toBeNull()
  })
})
