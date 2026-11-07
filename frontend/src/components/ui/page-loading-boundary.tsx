'use client'

import {
  createContext,
  useContext,
  useLayoutEffect,
  useMemo,
  useState,
  useSyncExternalStore,
  type ReactNode,
} from 'react'

const APPEAR_DELAY_MS = 200
const MIN_VISIBLE_MS = 300

const idleSnapshot = { busy: false, presentation: null as ReactNode }

function createLoadingController() {
  const owners = new Map<symbol, ReactNode>()
  const listeners = new Set<() => void>()
  let snapshot = idleSnapshot
  let startedAt: number | null = null
  let shownAt: number | null = null
  let appearanceTimer: ReturnType<typeof setTimeout> | undefined
  let finishTimer: ReturnType<typeof setTimeout> | undefined
  let disposed = false

  const publish = (busy: boolean, presentation: ReactNode) => {
    snapshot = { busy, presentation }
    listeners.forEach((listener) => listener())
  }
  const finish = () => {
    finishTimer = undefined
    startedAt = null
    shownAt = null
    publish(false, null)
  }

  return {
    subscribe(listener: () => void) {
      listeners.add(listener)
      return () => {
        listeners.delete(listener)
      }
    },
    getSnapshot: () => snapshot,
    show(id: symbol, view: ReactNode) {
      disposed = false
      clearTimeout(finishTimer)
      finishTimer = undefined
      startedAt ??= performance.now()
      owners.set(id, view)
      if (shownAt !== null || snapshot.presentation !== null) {
        publish(true, view)
        return
      }
      publish(true, null)
      clearTimeout(appearanceTimer)
      appearanceTimer = setTimeout(
        () => {
          appearanceTimer = undefined
          if (disposed || owners.size === 0) return
          publish(true, [...owners.values()].at(-1) ?? null)
        },
        Math.max(0, APPEAR_DELAY_MS - (performance.now() - startedAt))
      )
    },
    hide(id: symbol) {
      if (!owners.delete(id) || disposed) return
      if (owners.size > 0) {
        publish(
          true,
          snapshot.presentation === null
            ? null
            : ([...owners.values()].at(-1) ?? null)
        )
        return
      }
      clearTimeout(appearanceTimer)
      appearanceTimer = undefined
      // A timer firing is not evidence that React committed the indicator.
      if (shownAt === null) publish(true, null)
      const remaining =
        shownAt === null ? 0 : MIN_VISIBLE_MS - (performance.now() - shownAt)
      // Defer even an expired deadline so a same-commit handoff shares the clock.
      finishTimer = setTimeout(finish, Math.max(0, remaining))
    },
    presented() {
      if (owners.size > 0 && snapshot.presentation !== null) {
        shownAt ??= performance.now()
      }
    },
    resume() {
      disposed = false
    },
    dispose() {
      disposed = true
      clearTimeout(appearanceTimer)
      clearTimeout(finishTimer)
      owners.clear()
      startedAt = null
      shownAt = null
      snapshot = idleSnapshot
    },
  }
}

const LoadingContext = createContext<ReturnType<
  typeof createLoadingController
> | null>(null)
const serverSnapshot = () => idleSnapshot
const subscribeWithoutProvider = () => () => {}

export function PageLoadingProvider({ children }: { children: ReactNode }) {
  const [controller] = useState(createLoadingController)

  useLayoutEffect(() => {
    controller.resume()
    return () => controller.dispose()
  }, [controller])

  return (
    <LoadingContext.Provider value={controller}>
      {children}
    </LoadingContext.Provider>
  )
}

/** Includes the blank delay and retained presentation, not only active owners. */
export function usePageLoadingActive() {
  const controller = useContext(LoadingContext)
  return useSyncExternalStore(
    controller?.subscribe ?? subscribeWithoutProvider,
    controller ? () => controller.getSnapshot().busy : () => false,
    () => false
  )
}

/** Register only full-page loading; network activity and inline indicators stay independent. */
export function usePageLoadingPresentation(view: ReactNode) {
  const controller = useContext(LoadingContext)
  const id = useMemo(() => Symbol('page-loading'), [])

  useLayoutEffect(() => {
    if (!controller || view === null) return
    controller.show(id, view)
    return () => controller.hide(id)
  }, [controller, id, view])

  return controller !== null && view !== null
}

export function PageLoadingViewport({
  children,
  className = '',
}: {
  children: ReactNode
  className?: string
}) {
  const controller = useContext(LoadingContext)
  if (!controller)
    throw new Error('PageLoadingViewport requires PageLoadingProvider')
  return (
    <LoadingViewport controller={controller} className={className}>
      {children}
    </LoadingViewport>
  )
}

function LoadingViewport({
  controller,
  children,
  className,
}: {
  controller: ReturnType<typeof createLoadingController>
  children: ReactNode
  className: string
}) {
  const { busy, presentation } = useSyncExternalStore(
    controller.subscribe,
    controller.getSnapshot,
    serverSnapshot
  )

  useLayoutEffect(() => {
    if (presentation !== null) controller.presented()
  }, [controller, presentation])

  return (
    <div className={`relative min-h-0 flex-1 overflow-hidden ${className}`}>
      <div
        className={`h-full overflow-y-auto ${busy ? 'invisible' : ''}`}
        inert={busy}
        aria-busy={busy}
        aria-hidden={busy || undefined}
      >
        {children}
      </div>
      {busy && (
        <div className="bg-fl-bg absolute inset-0 z-10">{presentation}</div>
      )}
    </div>
  )
}
