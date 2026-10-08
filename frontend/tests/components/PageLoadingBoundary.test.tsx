import { StrictMode, useEffect, type ReactNode } from 'react'
import { act, cleanup, fireEvent, render, screen } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import {
  PageLoadingProvider,
  PageLoadingViewport,
} from '@/components/ui/page-loading-boundary'
import { PageLoading } from '@/components/ui/page-loading'
import { ExerciseGenerationLoading } from '@/components/ui/exercise-generation-loading'
import AppLoading from '@/app/(app)/loading'
import { useLoadingStore } from '@/store/loading'

vi.mock('next-intl', () => ({
  useTranslations: () => (key: string) => key,
}))
const avatarLifecycle = vi.hoisted(() => ({ mounted: vi.fn() }))
vi.mock('@/components/lingu/LinguAvatar', () => ({
  default: function MockAvatar() {
    useEffect(() => {
      avatarLifecycle.mounted()
    }, [])
    return <span data-testid="lingu" aria-hidden="true" />
  },
}))

function Boundary({ children }: { children: ReactNode }) {
  return (
    <StrictMode>
      <PageLoadingProvider>
        <PageLoadingViewport>{children}</PageLoadingViewport>
      </PageLoadingProvider>
    </StrictMode>
  )
}

const advance = (ms: number) => act(() => vi.advanceTimersByTime(ms))

beforeEach(() => {
  avatarLifecycle.mounted.mockClear()
  vi.useFakeTimers({ toFake: ['setTimeout', 'clearTimeout', 'performance'] })
  useLoadingStore.setState({ count: 0, complete: false })
})

afterEach(() => {
  cleanup()
  vi.useRealTimers()
})

describe('page loading minimum duration', () => {
  it('holds fast loading for exactly 500 ms and keeps ready content inert', () => {
    const started = vi.fn()
    function Ready() {
      useEffect(() => {
        started()
      }, [])
      return <button>Continue</button>
    }
    const { rerender, container } = render(
      <Boundary>
        <AppLoading />
      </Boundary>
    )
    advance(100)
    rerender(
      <Boundary>
        <Ready />
      </Boundary>
    )

    expect(started).toHaveBeenCalled()
    expect(container.querySelector('[inert]')).not.toBeNull()
    expect(screen.queryByRole('button')).not.toBeInTheDocument()
    expect(screen.getByRole('status')).toHaveTextContent('loading')
    expect(useLoadingStore.getState().count).toBe(0)

    advance(399)
    expect(screen.getByRole('status')).toBeInTheDocument()
    advance(1)
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Continue' })).toBeInTheDocument()
    expect(container.querySelector('[inert]')).toBeNull()
  })

  it('does not add another wait when slow loading ends', () => {
    const { rerender } = render(
      <Boundary>
        <PageLoading />
      </Boundary>
    )
    advance(1500)
    expect(screen.getByRole('status')).toBeInTheDocument()
    rerender(
      <Boundary>
        <button>Ready</button>
      </Boundary>
    )
    advance(0)
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
    expect(screen.getByRole('button')).toBeInTheDocument()
  })

  it('shares the deadline between route, page and generation loading', () => {
    const { rerender } = render(
      <Boundary>
        <AppLoading />
      </Boundary>
    )
    advance(100)
    rerender(
      <Boundary>
        <PageLoading label="Preparing" />
      </Boundary>
    )
    advance(100)
    rerender(
      <Boundary>
        <ExerciseGenerationLoading label="Generating" description="Exercise" />
      </Boundary>
    )
    advance(100)
    rerender(
      <Boundary>
        <button>Exercise ready</button>
      </Boundary>
    )
    expect(screen.getByRole('status')).toHaveTextContent('Generating')
    advance(199)
    expect(screen.getByRole('status')).toBeInTheDocument()
    advance(1)
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
  })

  it('keeps an expired deadline across an immediate loading handoff', () => {
    const { rerender } = render(
      <Boundary>
        <AppLoading />
      </Boundary>
    )
    advance(1500)
    rerender(
      <Boundary>
        <PageLoading label="Preparing" />
      </Boundary>
    )
    advance(50)
    rerender(
      <Boundary>
        <button>Ready</button>
      </Boundary>
    )
    advance(0)
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
  })

  it('cancels pending completion when loading resumes and releases only its own counter slots', () => {
    useLoadingStore.setState({ count: 2 })
    const { rerender } = render(
      <Boundary>
        <PageLoading />
      </Boundary>
    )
    advance(100)
    rerender(
      <Boundary>
        <button>Ready</button>
      </Boundary>
    )
    advance(200)
    rerender(
      <Boundary>
        <PageLoading label="Retrying" />
      </Boundary>
    )
    advance(1000)
    expect(screen.getByRole('status')).toHaveTextContent('Retrying')
    expect(useLoadingStore.getState().count).toBe(3)
    rerender(
      <Boundary>
        <button>Ready</button>
      </Boundary>
    )
    advance(0)
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
    expect(useLoadingStore.getState().count).toBe(2)
  })

  it('does not restart the minimum when loading text changes', () => {
    const { rerender } = render(
      <Boundary>
        <PageLoading label="Loading" />
      </Boundary>
    )
    advance(200)
    rerender(
      <Boundary>
        <PageLoading label="Almost ready" />
      </Boundary>
    )
    advance(100)
    rerender(
      <Boundary>
        <button>Ready</button>
      </Boundary>
    )
    advance(200)
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
  })

  it('starts a new minimum after a completed loading cycle', () => {
    const { rerender } = render(
      <Boundary>
        <PageLoading />
      </Boundary>
    )
    advance(100)
    rerender(
      <Boundary>
        <button>Ready</button>
      </Boundary>
    )
    advance(400)
    rerender(
      <Boundary>
        <PageLoading />
      </Boundary>
    )
    advance(100)
    rerender(
      <Boundary>
        <button>Ready again</button>
      </Boundary>
    )
    advance(399)
    expect(screen.getByRole('status')).toBeInTheDocument()
    advance(1)
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
  })

  it('does not retain inline loading or hide other page content', () => {
    const { rerender } = render(
      <Boundary>
        <PageLoading fullScreen={false} />
        <button>Action</button>
      </Boundary>
    )
    expect(screen.getByRole('button')).toBeInTheDocument()
    rerender(
      <Boundary>
        <button>Action</button>
      </Boundary>
    )
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
    expect(vi.getTimerCount()).toBe(0)
  })

  it('cleans up a pending minimum when the provider unmounts', () => {
    const { rerender, unmount } = render(
      <Boundary>
        <PageLoading />
      </Boundary>
    )
    advance(100)
    rerender(
      <Boundary>
        <button>Ready</button>
      </Boundary>
    )
    expect(vi.getTimerCount()).toBe(1)
    unmount()
    expect(vi.getTimerCount()).toBe(0)
    expect(useLoadingStore.getState().count).toBe(0)
  })

  it('keeps the overlay outside the scrolling content and preserves its scroll and form state', () => {
    function Page({ loading }: { loading: boolean }) {
      return (
        <section data-testid="page">
          {loading && <PageLoading />}
          <input aria-label="Draft" defaultValue="" />
          <button>Continue</button>
        </section>
      )
    }
    const { rerender } = render(
      <Boundary>
        <Page loading={false} />
      </Boundary>
    )
    const page = screen.getByTestId('page')
    const scroller = page.parentElement!
    const input = screen.getByRole('textbox')
    scroller.scrollTop = 360
    fireEvent.change(input, { target: { value: 'Keep my draft' } })

    rerender(
      <Boundary>
        <Page loading />
      </Boundary>
    )
    const status = screen.getByRole('status')
    expect(scroller.contains(status)).toBe(false)
    expect(scroller).toHaveAttribute('inert')
    expect(screen.queryByRole('textbox')).not.toBeInTheDocument()

    advance(100)
    rerender(
      <Boundary>
        <Page loading={false} />
      </Boundary>
    )
    advance(400)

    expect(screen.queryByRole('status')).not.toBeInTheDocument()
    expect(screen.getByTestId('page')).toBe(page)
    expect(page.parentElement).toBe(scroller)
    expect(scroller.scrollTop).toBe(360)
    expect(screen.getByRole('textbox')).toBe(input)
    expect(input).toHaveValue('Keep my draft')
    expect(scroller).not.toHaveAttribute('inert')
  })

  it('keeps the same avatar mounted across general loading, generation and delay warnings', () => {
    const { rerender } = render(
      <Boundary>
        <PageLoading label="Loading" />
      </Boundary>
    )
    const avatar = screen.getByTestId('lingu')
    const mounts = avatarLifecycle.mounted.mock.calls.length

    advance(200)
    rerender(
      <Boundary>
        <ExerciseGenerationLoading
          label="Generating"
          description="Preparing your exercise"
        />
      </Boundary>
    )
    expect(
      screen.getByRole('heading', { name: 'Generating' })
    ).toBeInTheDocument()
    expect(screen.getByTestId('lingu')).toBe(avatar)

    advance(200)
    rerender(
      <Boundary>
        <ExerciseGenerationLoading
          label="Generating"
          description="Preparing your exercise"
          warning="Taking longer than expected"
        />
      </Boundary>
    )
    expect(screen.getByText('Taking longer than expected')).toBeInTheDocument()
    expect(screen.getByTestId('lingu')).toBe(avatar)
    expect(avatarLifecycle.mounted).toHaveBeenCalledTimes(mounts)
    expect(screen.getAllByRole('status')).toHaveLength(1)

    rerender(
      <Boundary>
        <button>Ready</button>
      </Boundary>
    )
    advance(100)
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
  })
})
