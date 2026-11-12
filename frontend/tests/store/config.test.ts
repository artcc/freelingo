import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { useConfigStore } from '@/store/config'
import { resolveConfiguredTtsVoice } from '@/lib/tts-voice'

describe('useConfigStore', () => {
  const originalFetch = global.fetch

  beforeEach(() => {
    useConfigStore.setState({
      analyticsEnabled: false,
      allowRegistration: false,
      stripeEnabled: false,
      stripeTrialDays: 7,
      freemiumTrialEnabled: true,
      ttsProvider: 'local',
      openaiTtsVoice: 'nova',
      geminiTtsVoice: 'female',
      maintenanceMode: false,
      dashboardBanner: null,
      loaded: false,
    })
    vi.stubGlobal('fetch', vi.fn())
  })

  afterEach(() => {
    vi.useRealTimers()
    global.fetch = originalFetch
    vi.unstubAllGlobals()
  })

  it('loads config from /api/config', async () => {
    vi.mocked(fetch).mockResolvedValueOnce(
      new Response(
        JSON.stringify({
          analytics_enabled: true,
          allow_registration: true,
          stripe_enabled: true,
          stripe_trial_days: 14,
          tts_provider: 'openai',
          openai_tts_voice: 'alloy',
          maintenance_mode: true,
          freemium_trial_enabled: false,
          dashboard_banner: {
            revision: 3,
            translations: {
              en: { title: 'News', subtitle: 'Today', description: 'Details' },
            },
          },
        }),
        { status: 200, headers: { 'Content-Type': 'application/json' } }
      )
    )

    await useConfigStore.getState().load()

    expect(useConfigStore.getState().allowRegistration).toBe(true)
    expect(useConfigStore.getState().analyticsEnabled).toBe(true)
    expect(useConfigStore.getState().stripeEnabled).toBe(true)
    expect(useConfigStore.getState().stripeTrialDays).toBe(14)
    expect(useConfigStore.getState().ttsProvider).toBe('openai')
    expect(useConfigStore.getState().openaiTtsVoice).toBe('alloy')
    expect(useConfigStore.getState().maintenanceMode).toBe(true)
    expect(useConfigStore.getState().freemiumTrialEnabled).toBe(false)
    expect(useConfigStore.getState().dashboardBanner?.revision).toBe(3)
    expect(useConfigStore.getState().loaded).toBe(true)
  })

  it('keeps signup closed until configuration arrives', async () => {
    let resolveConfig!: (response: Response) => void
    vi.mocked(fetch).mockReturnValueOnce(
      new Promise((resolve) => {
        resolveConfig = resolve
      })
    )
    const loading = useConfigStore.getState().load()
    expect(useConfigStore.getState().allowRegistration).toBe(false)
    resolveConfig(new Response(JSON.stringify({ allow_registration: true })))
    await loading
    expect(useConfigStore.getState().allowRegistration).toBe(true)
  })

  it('loads the Gemini provider and its independent default voice', async () => {
    vi.mocked(fetch).mockResolvedValueOnce(
      new Response(
        JSON.stringify({
          tts_provider: 'gemini',
          gemini_tts_voice: 'male',
          openai_tts_voice: 'coral',
        })
      )
    )

    await useConfigStore.getState().load()

    expect(useConfigStore.getState().ttsProvider).toBe('gemini')
    expect(useConfigStore.getState().geminiTtsVoice).toBe('male')
    expect(useConfigStore.getState().openaiTtsVoice).toBe('coral')
  })

  it('loads closed registration even if the previous state allowed it', async () => {
    useConfigStore.setState({ allowRegistration: true })
    vi.mocked(fetch).mockResolvedValueOnce(
      new Response(JSON.stringify({ allow_registration: false }))
    )
    await useConfigStore.getState().load()
    expect(useConfigStore.getState().allowRegistration).toBe(false)
  })

  it('does not fetch twice (idempotency)', async () => {
    vi.mocked(fetch).mockResolvedValue(
      new Response(JSON.stringify({ stripe_enabled: true }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      })
    )

    await useConfigStore.getState().load()
    await useConfigStore.getState().load()

    expect(fetch).toHaveBeenCalledTimes(1)
  })

  it.each(['response', 'body'])(
    'releases a stalled %s after 20 seconds and ignores it after a successful retry',
    async (stage) => {
      vi.useFakeTimers()
      const staleConfig = { allow_registration: false, tts_provider: 'openai' }
      const response = new Response(JSON.stringify(staleConfig))
      let release!: () => void
      if (stage === 'response') {
        vi.mocked(fetch).mockReturnValueOnce(
          new Promise((resolve) => {
            release = () => resolve(response)
          })
        )
      } else {
        vi.spyOn(response, 'json').mockReturnValueOnce(
          new Promise((resolve) => {
            release = () => resolve(staleConfig)
          })
        )
        vi.mocked(fetch).mockReturnValueOnce(
          new Promise((resolve) => {
            setTimeout(() => resolve(response), 5_000)
          })
        )
      }
      vi.mocked(fetch).mockResolvedValueOnce(
        new Response(
          JSON.stringify({ allow_registration: true, tts_provider: 'gemini' })
        )
      )

      const loading = useConfigStore.getState().load()
      let settled = false
      void loading.then(() => {
        settled = true
      })

      try {
        expect(useConfigStore.getState().load()).toBe(loading)
        await vi.advanceTimersByTimeAsync(19_999)
        expect(settled).toBe(false)
        expect(fetch).toHaveBeenCalledTimes(1)

        await vi.advanceTimersByTimeAsync(1)
        expect(settled).toBe(true)
        expect(vi.mocked(fetch).mock.calls[0][1]?.signal?.aborted).toBe(true)
        expect(useConfigStore.getState().loaded).toBe(false)
        expect(useConfigStore.getState().allowRegistration).toBe(false)

        await useConfigStore.getState().load()

        expect(fetch).toHaveBeenCalledTimes(2)
        expect(useConfigStore.getState().loaded).toBe(true)
        expect(useConfigStore.getState().allowRegistration).toBe(true)
        expect(useConfigStore.getState().ttsProvider).toBe('gemini')
        expect(vi.getTimerCount()).toBe(0)

        release()
        await vi.advanceTimersByTimeAsync(0)

        expect(useConfigStore.getState().allowRegistration).toBe(true)
        expect(useConfigStore.getState().ttsProvider).toBe('gemini')
      } finally {
        release()
        await loading
      }
    }
  )

  it('keeps the shared load alive when one consumer cancels its wait', async () => {
    let resolveConfig!: (response: Response) => void
    vi.mocked(fetch).mockReturnValueOnce(
      new Promise((resolve) => {
        resolveConfig = resolve
      })
    )
    const controller = new AbortController()
    const cancelled = resolveConfiguredTtsVoice(controller.signal)
    const waiting = resolveConfiguredTtsVoice(
      new AbortController().signal,
      'male'
    )
    const cancelledResult = expect(cancelled).rejects.toMatchObject({
      name: 'AbortError',
    })

    controller.abort()
    await cancelledResult

    expect(fetch).toHaveBeenCalledTimes(1)
    expect(vi.mocked(fetch).mock.calls[0][1]?.signal?.aborted).not.toBe(true)
    expect(useConfigStore.getState().loaded).toBe(false)

    resolveConfig(new Response(JSON.stringify({ tts_provider: 'gemini' })))

    await expect(waiting).resolves.toBe('male')
    expect(useConfigStore.getState().loaded).toBe(true)
    expect(fetch).toHaveBeenCalledTimes(1)
  })

  it('keeps defaults and allows retry when fetch fails', async () => {
    vi.mocked(fetch).mockRejectedValueOnce(new Error('network error'))

    await useConfigStore.getState().load()

    expect(useConfigStore.getState().allowRegistration).toBe(false)
    expect(useConfigStore.getState().stripeEnabled).toBe(false)
    expect(useConfigStore.getState().ttsProvider).toBe('local')
    expect(useConfigStore.getState().loaded).toBe(false)
  })

  it.each(['network error', 'invalid JSON'])(
    'recovers registration and billing configuration after %s',
    async (failure) => {
      if (failure === 'network error') {
        vi.mocked(fetch).mockRejectedValueOnce(new Error('offline'))
      } else {
        vi.mocked(fetch).mockResolvedValueOnce(new Response('invalid JSON'))
      }
      vi.mocked(fetch).mockResolvedValueOnce(
        new Response(
          JSON.stringify({ allow_registration: true, stripe_enabled: true })
        )
      )

      await useConfigStore.getState().load()

      expect(useConfigStore.getState().allowRegistration).toBe(false)
      expect(useConfigStore.getState().stripeEnabled).toBe(false)
      expect(useConfigStore.getState().loaded).toBe(false)

      await useConfigStore.getState().load()

      expect(fetch).toHaveBeenCalledTimes(2)
      expect(useConfigStore.getState().allowRegistration).toBe(true)
      expect(useConfigStore.getState().stripeEnabled).toBe(true)
      expect(useConfigStore.getState().loaded).toBe(true)
    }
  )

  it('does not mark loaded when response is not ok (allows retry)', async () => {
    vi.mocked(fetch).mockResolvedValueOnce(
      new Response('error', { status: 500 })
    )

    await useConfigStore.getState().load()

    expect(useConfigStore.getState().allowRegistration).toBe(false)
    expect(useConfigStore.getState().stripeEnabled).toBe(false)
    expect(useConfigStore.getState().loaded).toBe(false)
  })

  it('uses defaults for missing fields in response', async () => {
    vi.mocked(fetch).mockResolvedValueOnce(
      new Response(JSON.stringify({}), {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      })
    )

    await useConfigStore.getState().load()

    expect(useConfigStore.getState().allowRegistration).toBe(false)
    expect(useConfigStore.getState().stripeEnabled).toBe(false)
    expect(useConfigStore.getState().stripeTrialDays).toBe(7)
    expect(useConfigStore.getState().ttsProvider).toBe('local')
    expect(useConfigStore.getState().openaiTtsVoice).toBe('nova')
    expect(useConfigStore.getState().geminiTtsVoice).toBe('female')
    expect(useConfigStore.getState().maintenanceMode).toBe(false)
    expect(useConfigStore.getState().freemiumTrialEnabled).toBe(true)
    expect(useConfigStore.getState().dashboardBanner).toBeNull()
  })
})
