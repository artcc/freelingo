'use client'

import { useCallback, useRef } from 'react'
import { trackBrowserEvent, type BrowserEvent } from '@/lib/analytics'
import { useConfigStore } from '@/store/config'

/** One actual viewport exposure per mounted panel; no text or DOM attributes are collected. */
export function useAnalyticsView(event: BrowserEvent) {
  const enabled = useConfigStore((state) => state.analyticsEnabled)
  const recorded = useRef(false)
  const observer = useRef<IntersectionObserver | null>(null)
  return useCallback(
    (node: HTMLElement | null) => {
      observer.current?.disconnect()
      observer.current = null
      if (!node || !enabled || recorded.current) return
      const record = () => {
        if (!recorded.current) recorded.current = trackBrowserEvent(event)
        if (recorded.current) observer.current?.disconnect()
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
    [enabled, event]
  )
}
