import { act, cleanup, render } from '@testing-library/react'
import { afterEach, beforeEach, expect, it, vi } from 'vitest'
import { useAnalyticsView } from '@/hooks/useAnalyticsView'
import { useAuthStore } from '@/store/auth'
import { useConfigStore } from '@/store/config'

class Observer {
  static instances: Observer[] = []
  observe = vi.fn()
  disconnect = vi.fn()
  constructor(public callback: IntersectionObserverCallback) {
    Observer.instances.push(this)
  }
  trigger(visible: boolean) {
    this.callback(
      [{ isIntersecting: visible } as IntersectionObserverEntry],
      this as unknown as IntersectionObserver
    )
  }
}

function Panel() {
  return <section ref={useAnalyticsView('progress_calendar_viewed')} />
}

beforeEach(() => {
  useConfigStore.setState({ analyticsEnabled: true })
  useAuthStore.getState().startSession('token')
  Observer.instances = []
  vi.stubGlobal('IntersectionObserver', Observer)
  vi.stubGlobal(
    'fetch',
    vi.fn().mockResolvedValue(new Response(null, { status: 204 }))
  )
})
afterEach(() => {
  cleanup()
  useConfigStore.setState({ analyticsEnabled: false })
  vi.unstubAllGlobals()
})

it('counts the first viewport exposure only, never hidden rendering', () => {
  render(<Panel />)
  const observer = Observer.instances.at(-1)!
  expect(fetch).not.toHaveBeenCalled()
  act(() => observer.trigger(false))
  expect(fetch).not.toHaveBeenCalled()
  act(() => observer.trigger(true))
  act(() => observer.trigger(true))
  expect(fetch).toHaveBeenCalledTimes(1)
  expect(observer.disconnect).toHaveBeenCalled()
})

it('does not publish a queued observation after unmount', () => {
  const { unmount } = render(<Panel />)
  const observer = Observer.instances.at(-1)!
  unmount()
  act(() => observer.trigger(true))
  expect(fetch).not.toHaveBeenCalled()
})
