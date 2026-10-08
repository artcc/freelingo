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

const MIN_VISIBLE_MS = 500

function createLoadingController() {
  const owners = new Map<symbol, ReactNode>()
  const listeners = new Set<() => void>()
  let presentation: ReactNode = null
  let startedAt: number | null = null
  let timer: ReturnType<typeof setTimeout> | undefined
  let disposed = false

  const publish = (next: ReactNode) => {
    presentation = next
    listeners.forEach((listener) => listener())
  }
  const finish = () => {
    timer = undefined
    startedAt = null
    publish(null)
  }

  return {
    subscribe(listener: () => void) {
      listeners.add(listener)
      return () => {
        listeners.delete(listener)
      }
    },
    getSnapshot: () => presentation,
    show(id: symbol, view: ReactNode) {
      disposed = false
      clearTimeout(timer)
      timer = undefined
      startedAt ??= performance.now()
      owners.set(id, view)
      publish(view)
    },
    hide(id: symbol) {
      if (!owners.delete(id) || disposed) return
      if (owners.size > 0) {
        publish([...owners.values()].at(-1) ?? null)
        return
      }
      const remaining = MIN_VISIBLE_MS - (performance.now() - (startedAt ?? 0))
      // Defer even an expired deadline so a same-commit handoff shares the clock.
      timer = setTimeout(finish, Math.max(0, remaining))
    },
    resume() {
      disposed = false
    },
    dispose() {
      disposed = true
      clearTimeout(timer)
    },
  }
}

const LoadingContext = createContext<ReturnType<
  typeof createLoadingController
> | null>(null)
const serverSnapshot = () => null
const subscribeHydration = () => () => {}
const clientHydrated = () => true
const serverHydrated = () => false

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

/** Register only full-page loading; network activity and inline indicators stay independent. */
export function usePageLoadingPresentation(view: ReactNode) {
  const controller = useContext(LoadingContext)
  const id = useMemo(() => Symbol('page-loading'), [])
  const hydrated = useSyncExternalStore(
    subscribeHydration,
    clientHydrated,
    serverHydrated
  )

  useLayoutEffect(() => {
    if (!controller || view === null) return
    controller.show(id, view)
    return () => controller.hide(id)
  }, [controller, id, view])

  return controller !== null && view !== null && hydrated
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
  const presentation = useSyncExternalStore(
    controller.subscribe,
    controller.getSnapshot,
    serverSnapshot
  )
  const busy = presentation !== null

  return (
    <div className={`relative min-h-0 flex-1 overflow-hidden ${className}`}>
      <div
        className={`h-full overflow-y-auto ${busy ? 'invisible' : ''}`}
        inert={busy}
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
