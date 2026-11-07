import { StrictMode, useEffect, type ReactNode } from 'react'
import { renderToString } from 'react-dom/server'
import { act, cleanup, fireEvent, render, screen } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import {
  PageLoadingProvider,
  PageLoadingViewport,
  usePageLoadingActive,
} from '@/components/ui/page-loading-boundary'
import { PageLoading } from '@/components/ui/page-loading'
import { ExerciseGenerationLoading } from '@/components/ui/exercise-generation-loading'
import AppLoading from '@/app/(app)/loading'
import { useLoadingStore } from '@/store/loading'

vi.mock('next-intl', () => ({
  useTranslations: () => (key: string) => key,
}))
vi.mock('@/components/lingu/LinguAvatar', () => ({
  default: () => {
    throw new Error('Loading must not mount a 3D avatar')
  },
}))

function Activity() {
  return <span data-testid="activity">{String(usePageLoadingActive())}</span>
}

function Boundary({ children }: { children: ReactNode }) {
  return (
    <StrictMode>
      <PageLoadingProvider>
        <Activity />
        <PageLoadingViewport>{children}</PageLoadingViewport>
      </PageLoadingProvider>
    </StrictMode>
  )
}

const advance = (ms: number) => act(() => vi.advanceTimersByTime(ms))

beforeEach(() => {
  vi.useFakeTimers({ toFake: ['setTimeout', 'clearTimeout', 'performance'] })
  useLoadingStore.setState({ count: 0, complete: false })
})

afterEach(() => {
  cleanup()
  vi.useRealTimers()
})

describe('page loading presentation', () => {
  it('does not bypass the managed delay with a server-rendered standalone indicator', () => {
    const html = renderToString(
      <Boundary>
        <PageLoading />
      </Boundary>
    )
    expect(html).not.toContain('role="status"')
    expect(useLoadingStore.getState().count).toBe(0)
  })

  it('blocks content immediately but never shows or retains a fast load', () => {
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
        <button>Underlying action</button>
      </Boundary>
    )
    expect(container.querySelector('[inert]')).not.toBeNull()
    expect(screen.queryByRole('button')).not.toBeInTheDocument()
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
    expect(screen.getByTestId('activity')).toHaveTextContent('true')

    advance(199)
    rerender(
      <Boundary>
        <Ready />
      </Boundary>
    )
    expect(started).toHaveBeenCalled()
    expect(useLoadingStore.getState().count).toBe(0)
    advance(0)
    expect(screen.getByRole('button', { name: 'Continue' })).toBeInTheDocument()
    expect(container.querySelector('[inert]')).toBeNull()
    expect(screen.getByTestId('activity')).toHaveTextContent('false')
    advance(1000)
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
  })

  it('shows at 200 ms and retains for 300 ms from appearance without counter slots', () => {
    const { rerender, container } = render(
      <Boundary>
        <PageLoading />
      </Boundary>
    )
    advance(199)
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
    advance(1)
    expect(screen.getByRole('status', { name: 'loading' })).toBeInTheDocument()
    expect(screen.getByRole('status').closest('[aria-busy="true"]')).toBeNull()
    advance(20)
    rerender(
      <Boundary>
        <button>Ready</button>
      </Boundary>
    )
    expect(useLoadingStore.getState().count).toBe(0)
    expect(container.querySelector('[inert]')).not.toBeNull()
    expect(screen.getByTestId('activity')).toHaveTextContent('true')
    advance(279)
    expect(screen.getByRole('status')).toBeInTheDocument()
    advance(1)
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
    expect(screen.getByRole('button')).toBeInTheDocument()
    expect(screen.getByTestId('activity')).toHaveTextContent('false')
  })

  it('starts the minimum at the committed appearance rather than the timer deadline', () => {
    const { rerender } = render(
      <Boundary>
        <PageLoading />
      </Boundary>
    )
    // React commits after this batched timer advance, not at the 200 ms callback.
    advance(600)
    expect(screen.getByRole('status')).toBeInTheDocument()
    rerender(
      <Boundary>
        <button>Ready</button>
      </Boundary>
    )
    advance(299)
    expect(screen.getByRole('status')).toBeInTheDocument()
    advance(1)
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
  })

  it('does not retain an indicator whose timer fired but never committed', () => {
    const { rerender } = render(
      <Boundary>
        <PageLoading />
      </Boundary>
    )
    act(() => {
      vi.advanceTimersByTime(200)
      rerender(
        <Boundary>
          <button>Ready</button>
        </Boundary>
      )
    })
    advance(0)
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
    expect(screen.getByRole('button')).toBeInTheDocument()
    expect(vi.getTimerCount()).toBe(0)
  })

  it('does not add a wait when slow loading ends', () => {
    const { rerender } = render(
      <Boundary>
        <PageLoading />
      </Boundary>
    )
    advance(200)
    advance(1300)
    rerender(
      <Boundary>
        <button>Ready</button>
      </Boundary>
    )
    advance(0)
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
    expect(screen.getByRole('button')).toBeInTheDocument()
  })

  it('shares the delay and visible deadline across same-commit route/page/generation handoffs', () => {
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
    advance(99)
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
    advance(1)
    expect(screen.getByRole('status')).toHaveTextContent('Preparing')
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

  it('keeps an expired deadline across a same-commit handoff', () => {
    const { rerender } = render(
      <Boundary>
        <AppLoading />
      </Boundary>
    )
    advance(200)
    advance(1300)
    rerender(
      <Boundary>
        <PageLoading label="Preparing" />
      </Boundary>
    )
    expect(screen.getByRole('status')).toHaveTextContent('Preparing')
    advance(50)
    rerender(
      <Boundary>
        <button>Ready</button>
      </Boundary>
    )
    advance(0)
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
  })

  it('cancels retention when loading resumes and releases only owned counter slots', () => {
    useLoadingStore.setState({ count: 2 })
    const { rerender } = render(
      <Boundary>
        <PageLoading />
      </Boundary>
    )
    advance(200)
    advance(50)
    rerender(
      <Boundary>
        <button>Ready</button>
      </Boundary>
    )
    expect(useLoadingStore.getState().count).toBe(2)
    advance(100)
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

  it('does not restart delay or retention when the label changes', () => {
    const { rerender } = render(
      <Boundary>
        <PageLoading label="Loading" />
      </Boundary>
    )
    advance(100)
    rerender(
      <Boundary>
        <PageLoading label="Almost ready" />
      </Boundary>
    )
    advance(100)
    expect(screen.getByRole('status')).toHaveTextContent('Almost ready')
    rerender(
      <Boundary>
        <PageLoading label="Finishing" />
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

  it('starts a fresh delay and minimum after a completed cycle', () => {
    const { rerender } = render(
      <Boundary>
        <PageLoading />
      </Boundary>
    )
    advance(200)
    advance(400)
    rerender(
      <Boundary>
        <button>Ready</button>
      </Boundary>
    )
    advance(0)
    rerender(
      <Boundary>
        <PageLoading />
      </Boundary>
    )
    advance(199)
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
    advance(1)
    rerender(
      <Boundary>
        <button>Ready again</button>
      </Boundary>
    )
    advance(299)
    expect(screen.getByRole('status')).toBeInTheDocument()
    advance(1)
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
  })

  it('keeps overlapping owners active and falls back to the remaining presentation', () => {
    const { rerender } = render(
      <Boundary>
        <PageLoading key="first" label="First" />
        <PageLoading key="second" label="Second" />
      </Boundary>
    )
    advance(200)
    expect(screen.getByRole('status')).toHaveTextContent('Second')
    expect(useLoadingStore.getState().count).toBe(2)
    rerender(
      <Boundary>
        <PageLoading key="first" label="First" />
      </Boundary>
    )
    advance(1000)
    expect(screen.getByRole('status')).toHaveTextContent('First')
    expect(useLoadingStore.getState().count).toBe(1)
  })

  it('preserves a pending appearance when one overlapping owner ends before commit', () => {
    const { rerender } = render(
      <Boundary>
        <PageLoading key="first" label="First" />
        <PageLoading key="second" label="Second" />
      </Boundary>
    )
    act(() => {
      vi.advanceTimersByTime(200)
      rerender(
        <Boundary>
          <PageLoading key="first" label="First" />
        </Boundary>
      )
    })
    expect(screen.getByRole('status')).toHaveTextContent('First')
    expect(useLoadingStore.getState().count).toBe(1)
  })

  it('leaves inline loading compact, immediate, local and motion-safe', () => {
    const { rerender } = render(
      <Boundary>
        <PageLoading fullScreen={false} />
        <button>Action</button>
      </Boundary>
    )
    expect(screen.getByRole('button')).toBeInTheDocument()
    const status = screen.getByRole('status')
    expect(status.tagName).toBe('SPAN')
    expect(status.querySelector('svg')).toHaveClass('motion-safe:animate-spin')
    expect(screen.getByTestId('activity')).toHaveTextContent('false')
    rerender(
      <Boundary>
        <PageLoading fullScreen={false} showDot={false} />
      </Boundary>
    )
    expect(screen.getByRole('status').querySelector('svg')).toBeNull()
    rerender(
      <Boundary>
        <button>Action</button>
      </Boundary>
    )
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
    expect(vi.getTimerCount()).toBe(0)
  })

  it.each(['delay', 'visible', 'retained'] as const)(
    'cleans timers and slots on provider unmount during %s',
    (phase) => {
      const { rerender, unmount } = render(
        <Boundary>
          <PageLoading />
        </Boundary>
      )
      if (phase !== 'delay') advance(250)
      if (phase === 'retained') {
        rerender(
          <Boundary>
            <button>Ready</button>
          </Boundary>
        )
      }
      unmount()
      expect(vi.getTimerCount()).toBe(0)
      expect(useLoadingStore.getState().count).toBe(0)
    }
  )

  it('keeps the overlay outside content scrolling and preserves form and scroll state', () => {
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
    expect(scroller).toHaveAttribute('inert')
    expect(scroller).toHaveAttribute('aria-hidden', 'true')
    expect(screen.queryByRole('textbox')).not.toBeInTheDocument()
    advance(200)
    const status = screen.getByRole('status')
    expect(scroller.contains(status)).toBe(false)
    expect(status).toHaveClass('overflow-y-auto')
    expect(status).toHaveAttribute('tabindex', '0')
    rerender(
      <Boundary>
        <Page loading={false} />
      </Boundary>
    )
    advance(300)
    expect(screen.getByTestId('page')).toBe(page)
    expect(page.parentElement).toBe(scroller)
    expect(scroller.scrollTop).toBe(360)
    expect(screen.getByRole('textbox')).toBe(input)
    expect(input).toHaveValue('Keep my draft')
    expect(scroller).not.toHaveAttribute('inert')
  })

  it('sizes the indicator slot to its content independently of wrapping text and warnings', () => {
    const { rerender } = render(
      <Boundary>
        <PageLoading label="Loading" />
      </Boundary>
    )
    advance(200)
    const spinner = screen.getByRole('status').querySelector('svg')!
    const slot = spinner.parentElement!
    const geometry = slot.parentElement!
    expect(spinner).toHaveClass('motion-safe:animate-spin')
    expect(slot).toHaveAttribute('aria-hidden', 'true')
    expect(slot).toHaveClass('size-6')
    expect(geometry).toHaveClass(
      'grid-rows-[minmax(1.5rem,1fr)_24px_minmax(1.5rem,1fr)]'
    )
    rerender(
      <Boundary>
        <ExerciseGenerationLoading
          label="Generating a long wrapping title"
          description="Preparing your exercise"
        />
      </Boundary>
    )
    const image = screen.getByRole('status').querySelector('img')!
    expect(image).toHaveAttribute('src', '/logo.png')
    expect(image.parentElement).toBe(slot)
    expect(slot).toHaveClass('size-[75px]', 'md:size-[150px]')
    expect(slot.parentElement).toBe(geometry)
    expect(slot).not.toHaveTextContent('Generating')
    expect(screen.getByRole('heading')).toHaveTextContent(
      'Generating a long wrapping title'
    )
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
    expect(screen.getByRole('status').querySelector('img')?.parentElement).toBe(
      slot
    )
    expect(screen.getAllByRole('status')).toHaveLength(1)
    expect(screen.queryByRole('img')).not.toBeInTheDocument()
  })

  it('keeps standalone public loading immediately usable without a provider', () => {
    const { unmount } = render(
      <StrictMode>
        <PageLoading label="Public loading" />
      </StrictMode>
    )
    expect(
      screen.getByRole('status', { name: 'Public loading' })
    ).toBeInTheDocument()
    expect(useLoadingStore.getState().count).toBe(1)
    unmount()
    expect(useLoadingStore.getState().count).toBe(0)
    expect(vi.getTimerCount()).toBe(0)
  })
})
