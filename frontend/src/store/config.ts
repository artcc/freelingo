import { create } from 'zustand'

export interface DashboardBannerTranslation {
  title: string
  subtitle: string
  description: string
}

export interface DashboardBanner {
  revision: number
  translations: Record<string, DashboardBannerTranslation>
}

interface ConfigStore {
  analyticsEnabled: boolean
  allowRegistration: boolean
  stripeEnabled: boolean
  stripeTrialDays: number
  freemiumTrialEnabled: boolean
  ttsProvider: string
  openaiTtsVoice: string
  geminiTtsVoice: string
  maintenanceMode: boolean
  priceMonthly: number
  priceYearly: number
  totalPriceMonthly: number
  totalPriceYearly: number
  dashboardBanner: DashboardBanner | null
  loaded: boolean
  load: () => Promise<void>
}

let loading: Promise<void> | null = null

export const useConfigStore = create<ConfigStore>((set, get) => ({
  analyticsEnabled: false,
  allowRegistration: false,
  stripeEnabled: false,
  stripeTrialDays: 7,
  freemiumTrialEnabled: true,
  ttsProvider: 'local',
  openaiTtsVoice: 'nova',
  geminiTtsVoice: 'female',
  maintenanceMode: false,
  priceMonthly: 0.0,
  priceYearly: 0.0,
  totalPriceMonthly: 0.0,
  totalPriceYearly: 0.0,
  dashboardBanner: null,
  loaded: false,
  load: () => {
    if (get().loaded) return Promise.resolve()
    if (loading) return loading
    const controller = new AbortController()
    let timeout: ReturnType<typeof setTimeout>
    const deadline = new Promise<never>((_, reject) => {
      timeout = setTimeout(() => {
        const error = new DOMException(
          'Configuration load timed out',
          'TimeoutError'
        )
        controller.abort(error)
        reject(error)
      }, 20_000)
    })
    loading = (async () => {
      try {
        // Bound both headers and body, even if the transport ignores cancellation.
        const data = await Promise.race([
          fetch('/api/config', { signal: controller.signal }).then((res) =>
            res.ok ? res.json() : null
          ),
          deadline,
        ])
        if (!data) return
        controller.signal.throwIfAborted()
        set({
          analyticsEnabled: data.analytics_enabled === true,
          allowRegistration: data.allow_registration === true,
          stripeEnabled: data.stripe_enabled ?? false,
          stripeTrialDays: data.stripe_trial_days ?? 7,
          freemiumTrialEnabled: data.freemium_trial_enabled ?? true,
          ttsProvider: data.tts_provider ?? 'local',
          openaiTtsVoice: data.openai_tts_voice ?? 'nova',
          geminiTtsVoice: data.gemini_tts_voice ?? 'female',
          maintenanceMode: data.maintenance_mode ?? false,
          priceMonthly: data.price_monthly ?? 0.0,
          priceYearly: data.price_yearly ?? 0.0,
          totalPriceMonthly: data.total_price_monthly ?? 0.0,
          totalPriceYearly: data.total_price_yearly ?? 0.0,
          dashboardBanner: data.dashboard_banner ?? null,
          loaded: true,
        })
      } catch {
        // Non-fatal: keep conservative defaults and allow the next load to retry.
      }
    })().finally(() => {
      clearTimeout(timeout)
      loading = null
    })
    return loading
  },
}))
