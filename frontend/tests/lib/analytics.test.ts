import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { trackBrowserEvent, trackDashboardLink } from '@/lib/analytics'
import { useAuthStore } from '@/store/auth'
import { useConfigStore } from '@/store/config'

beforeEach(() => {
  useConfigStore.setState({ analyticsEnabled: true })
  useAuthStore.getState().startSession('test-token')
  vi.stubGlobal(
    'fetch',
    vi.fn().mockResolvedValue(new Response(null, { status: 204 }))
  )
})
afterEach(() => {
  useConfigStore.setState({ analyticsEnabled: false })
  vi.unstubAllGlobals()
})

describe('first-party analytics signals', () => {
  it('sends only the closed name and operation nonce without cookies or page data', () => {
    const operationId = 'cfe9b972-b334-4dd7-ac80-04761d4c5668'
    expect(trackBrowserEvent('tour_started', { operationId })).toBe(true)
    const [url, options] = vi.mocked(fetch).mock.calls[0]
    expect(url).toBe('/api/analytics/ui')
    expect(options?.credentials).toBe('omit')
    expect(options?.keepalive).toBe(true)
    expect(new Headers(options?.headers).get('Authorization')).toBe(
      'Bearer test-token'
    )
    expect(JSON.parse(String(options?.body))).toEqual({
      event: 'tour_started',
      operation_id: operationId,
    })
  })

  it('does not send when disabled, unauthenticated, or from a replaced session', () => {
    useConfigStore.setState({ analyticsEnabled: false })
    expect(trackBrowserEvent('tour_started')).toBe(false)
    useConfigStore.setState({ analyticsEnabled: true })
    const oldSession = useAuthStore.getState().sessionVersion
    useAuthStore.getState().startSession('replacement')
    expect(
      trackBrowserEvent('tour_started', { sessionVersion: oldSession })
    ).toBe(false)
    useAuthStore.setState({ accessToken: null })
    expect(trackBrowserEvent('tour_started')).toBe(false)
    expect(fetch).not.toHaveBeenCalled()
  })

  it('sends public FAQ events without account credentials', () => {
    trackBrowserEvent('faq_viewed')
    const [url, options] = vi.mocked(fetch).mock.calls[0]
    expect(url).toBe('/api/analytics/public')
    expect(new Headers(options?.headers).has('Authorization')).toBe(false)
  })

  it('ignores delivery errors without refreshing authentication', async () => {
    vi.mocked(fetch).mockRejectedValue(new TypeError('offline'))
    trackBrowserEvent('tour_skipped')
    await Promise.resolve()
    expect(fetch).toHaveBeenCalledTimes(1)
    expect(useAuthStore.getState().accessToken).toBe('test-token')
  })

  it('classifies dashboard actions without sending IDs, query strings, or billing actions', () => {
    trackDashboardLink('/lesson/123?secret=private')
    trackDashboardLink('/billing/success')
    trackDashboardLink('/__proto__')
    trackDashboardLink('https://other.example/plan')
    expect(fetch).toHaveBeenCalledTimes(1)
    const body = JSON.parse(String(vi.mocked(fetch).mock.calls[0][1]?.body))
    expect(body.event).toBe('dashboard_lesson_clicked')
    expect(Object.keys(body).sort()).toEqual(['event', 'operation_id'])
  })
})
