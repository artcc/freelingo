import { StrictMode, type ReactNode } from 'react'
import { act, cleanup, fireEvent, render, screen } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { LoadingBar } from '@/components/ui/loading-bar'
import { PageLoading } from '@/components/ui/page-loading'
import {
  PageLoadingProvider,
  PageLoadingViewport,
} from '@/components/ui/page-loading-boundary'
import { useLoadingStore } from '@/store/loading'

vi.mock('next-intl', () => ({
  useTranslations: () => (key: string) => key,
}))

const advance = (ms: number) => act(() => vi.advanceTimersByTime(ms))
const start = () => act(() => useLoadingStore.getState().inc())
const finish = () => act(() => useLoadingStore.getState().dec())

function Shell({ children }: { children: ReactNode }) {
  return (
    <StrictMode>
      <PageLoadingProvider>
        <LoadingBar />
        <PageLoadingViewport>{children}</PageLoadingViewport>
      </PageLoadingProvider>
    </StrictMode>
  )
}

beforeEach(() => {
  vi.useFakeTimers({ toFake: ['setTimeout', 'clearTimeout', 'performance'] })
  useLoadingStore.setState({ count: 0, complete: false })
})

afterEach(() => {
  cleanup()
  vi.useRealTimers()
})

describe('LoadingBar', () => {
  it('never flashes a fast standalone request or its completion', () => {
    render(
      <StrictMode>
        <LoadingBar />
      </StrictMode>
    )
    start()
    advance(199)
    expect(screen.queryByRole('progressbar')).not.toBeInTheDocument()
    finish()
    advance(1000)
    expect(screen.queryByRole('progressbar')).not.toBeInTheDocument()
    expect(useLoadingStore.getState().complete).toBe(false)
    expect(vi.getTimerCount()).toBe(0)
  })

  it('discards a reveal when activity finishes before its first commit', () => {
    render(<LoadingBar />)
    start()
    act(() => {
      vi.advanceTimersByTime(200)
      useLoadingStore.getState().dec()
    })
    expect(screen.queryByRole('progressbar')).not.toBeInTheDocument()
    expect(useLoadingStore.getState().complete).toBe(false)
    expect(vi.getTimerCount()).toBe(0)
    advance(1000)
    expect(screen.queryByRole('progressbar')).not.toBeInTheDocument()
  })

  it('delays 200 ms, retains 300 ms from appearance and exits without animation events', () => {
    render(
      <StrictMode>
        <LoadingBar />
      </StrictMode>
    )
    start()
    advance(199)
    expect(screen.queryByRole('progressbar')).not.toBeInTheDocument()
    advance(1)
    const bar = screen.getByRole('progressbar', { name: 'loading' })
    expect(bar).toHaveClass('fixed', 'top-0', 'h-px')
    expect(bar.firstElementChild).toHaveClass('bg-fl-fg', 'animate-loading-bar')
    advance(20)
    finish()
    advance(279)
    expect(bar.firstElementChild).toHaveClass('animate-loading-bar')
    advance(1)
    expect(bar.firstElementChild).toHaveClass('animate-loading-bar-complete')
    advance(149)
    expect(screen.getByRole('progressbar')).toBeInTheDocument()
    advance(1)
    expect(screen.queryByRole('progressbar')).not.toBeInTheDocument()
    expect(useLoadingStore.getState().complete).toBe(false)
  })

  it('measures its minimum from the committed appearance when rendering is delayed', () => {
    render(<LoadingBar />)
    start()
    advance(600)
    finish()
    advance(299)
    expect(screen.getByRole('progressbar').firstElementChild).toHaveClass(
      'animate-loading-bar'
    )
    advance(1)
    expect(screen.getByRole('progressbar').firstElementChild).toHaveClass(
      'animate-loading-bar-complete'
    )
    advance(150)
    expect(screen.queryByRole('progressbar')).not.toBeInTheDocument()
  })

  it('does not restart the appearance delay or visible minimum as the counter changes', () => {
    render(<LoadingBar />)
    start()
    advance(100)
    start()
    advance(100)
    expect(screen.getByRole('progressbar')).toBeInTheDocument()
    advance(250)
    finish()
    start()
    finish()
    finish()
    advance(50)
    expect(screen.getByRole('progressbar').firstElementChild).toHaveClass(
      'animate-loading-bar-complete'
    )
    advance(150)
    expect(screen.queryByRole('progressbar')).not.toBeInTheDocument()
  })

  it('cancels pending completion and ignores stale animation events during renewed activity', () => {
    render(<LoadingBar />)
    start()
    advance(200)
    finish()
    advance(100)
    start()
    advance(1000)
    expect(screen.getByRole('progressbar').firstElementChild).toHaveClass(
      'animate-loading-bar'
    )
    finish()
    advance(0)
    advance(75)
    start()
    const indicator = screen.getByRole('progressbar').firstElementChild!
    fireEvent.animationEnd(indicator, { animationName: 'loading-bar-complete' })
    advance(1000)
    expect(screen.getByRole('progressbar').firstElementChild).toHaveClass(
      'animate-loading-bar'
    )
    expect(useLoadingStore.getState().count).toBe(1)
    finish()
    advance(0)
    advance(150)
    expect(screen.queryByRole('progressbar')).not.toBeInTheDocument()
  })

  it('starts a fresh delay after a fully completed cycle', () => {
    render(<LoadingBar />)
    start()
    advance(200)
    advance(300)
    finish()
    advance(0)
    advance(150)
    start()
    advance(199)
    expect(screen.queryByRole('progressbar')).not.toBeInTheDocument()
    advance(1)
    expect(screen.getByRole('progressbar')).toBeInTheDocument()
    finish()
    advance(299)
    expect(screen.getByRole('progressbar').firstElementChild).toHaveClass(
      'animate-loading-bar'
    )
    advance(1)
    advance(150)
    expect(screen.queryByRole('progressbar')).not.toBeInTheDocument()
  })

  it('suppresses the bar through page delay and retention without stale completion afterward', () => {
    const { rerender } = render(
      <Shell>
        <PageLoading />
      </Shell>
    )
    start()
    advance(200)
    expect(screen.getByRole('status')).toBeInTheDocument()
    expect(screen.queryByRole('progressbar')).not.toBeInTheDocument()
    rerender(
      <Shell>
        <button>Ready</button>
      </Shell>
    )
    finish()
    expect(useLoadingStore.getState().count).toBe(0)
    advance(299)
    expect(screen.queryByRole('progressbar')).not.toBeInTheDocument()
    advance(1)
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
    advance(1000)
    expect(screen.queryByRole('progressbar')).not.toBeInTheDocument()
    expect(useLoadingStore.getState().complete).toBe(false)
  })

  it('immediately hides an existing bar when full-page loading starts', () => {
    const { rerender } = render(
      <Shell>
        <button>Ready</button>
      </Shell>
    )
    start()
    advance(200)
    expect(screen.getByRole('progressbar')).toBeInTheDocument()
    rerender(
      <Shell>
        <PageLoading />
      </Shell>
    )
    expect(screen.queryByRole('progressbar')).not.toBeInTheDocument()
    advance(100)
    finish()
    rerender(
      <Shell>
        <button>Ready</button>
      </Shell>
    )
    advance(0)
    advance(1000)
    expect(screen.queryByRole('progressbar')).not.toBeInTheDocument()
  })

  it('reflects genuinely pending network activity once the page presentation ends', () => {
    const { rerender } = render(
      <Shell>
        <PageLoading />
      </Shell>
    )
    start()
    advance(200)
    advance(50)
    rerender(
      <Shell>
        <button>Ready</button>
      </Shell>
    )
    advance(250)
    expect(screen.getByRole('button')).toBeInTheDocument()
    expect(useLoadingStore.getState().count).toBe(1)
    advance(199)
    expect(screen.queryByRole('progressbar')).not.toBeInTheDocument()
    advance(1)
    expect(screen.getByRole('progressbar')).toBeInTheDocument()
    finish()
    advance(300)
    advance(150)
    expect(screen.queryByRole('progressbar')).not.toBeInTheDocument()
  })

  it('does not show legacy completion state without an observed pending cycle', () => {
    useLoadingStore.setState({ complete: true })
    render(<LoadingBar />)
    advance(1000)
    expect(screen.queryByRole('progressbar')).not.toBeInTheDocument()
    expect(useLoadingStore.getState().complete).toBe(false)
  })

  it('supports reduced motion and completes using its timer', () => {
    render(<LoadingBar />)
    start()
    advance(200)
    expect(
      screen.getByRole('progressbar').querySelector('style')
    ).toHaveTextContent('@media (prefers-reduced-motion: reduce)')
    finish()
    advance(300)
    advance(150)
    expect(screen.queryByRole('progressbar')).not.toBeInTheDocument()
  })

  it.each(['delay', 'minimum', 'exit'] as const)(
    'cancels timers when unmounted during %s',
    (phase) => {
      const { unmount } = render(
        <StrictMode>
          <LoadingBar />
        </StrictMode>
      )
      start()
      if (phase !== 'delay') {
        advance(200)
        finish()
      }
      if (phase === 'exit') advance(300)
      unmount()
      expect(vi.getTimerCount()).toBe(0)
      expect(useLoadingStore.getState().count).toBe(phase === 'delay' ? 1 : 0)
    }
  )
})
