'use client'

import { useCallback, useRef } from 'react'
import { trackBrowserEvent, type BrowserEvent } from '@/lib/analytics'
import { useConfigStore } from '@/store/config'

/** The optional view key is local only; it distinguishes resource navigation, never users. */
export function useAnalyticsView(event: BrowserEvent, viewKey = '') {
  const enabled = useConfigStore((state) => state.analyticsEnabled)
  const recorded = useRef<string | null>(null)
  const identity = `${event}:${viewKey}`
  const observer = useRef<IntersectionObserver | null>(null)
  return useCallback(
    (node: HTMLElement | null) => {
      observer.current?.disconnect()
      observer.current = null
      if (!node || !enabled || recorded.current === identity) return
      const record = () => {
        if (recorded.current !== identity && trackBrowserEvent(event))
          recorded.current = identity
        if (recorded.current === identity) observer.current?.disconnect()
      }
      if (typeof IntersectionObserver === 'undefined') {
        record()
        return
      }
      try {
        const current = new IntersectionObserver(
          (entries) => {
            if (
              observer.current === current &&
              entries.some((entry) => entry.isIntersecting)
            )
              record()
          },
          { threshold: 0.1 }
        )
        observer.current = current
        current.observe(node)
      } catch {
        // Unsupported observation must not interfere with rendering.
      }
    },
    [enabled, event, identity]
  )
}
