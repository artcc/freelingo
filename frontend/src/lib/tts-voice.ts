import { useConfigStore } from '@/store/config'

export const OPENAI_VOICES = [
  'alloy',
  'ash',
  'coral',
  'echo',
  'fable',
  'nova',
  'onyx',
  'sage',
  'shimmer',
] as const

export const GEMINI_VOICES = ['female', 'male'] as const

export function ttsVoiceStorageKey(provider: string): string {
  return provider === 'gemini' ? 'gemini_tts_voice' : 'tts_voice'
}

// Omit an unset preference so the backend remains authoritative for defaults.
export function resolveTtsVoice(
  provider: string,
  explicitVoice?: string
): string | undefined {
  const voices: readonly string[] | undefined =
    provider === 'gemini'
      ? GEMINI_VOICES
      : provider === 'openai'
        ? OPENAI_VOICES
        : undefined
  const valid = (voice: string | null | undefined): voice is string =>
    !!voice && (!voices || voices.includes(voice))

  if (valid(explicitVoice)) return explicitVoice
  try {
    const stored =
      typeof window !== 'undefined'
        ? localStorage.getItem(ttsVoiceStorageKey(provider))
        : null
    return valid(stored) ? stored : undefined
  } catch {
    return undefined
  }
}

export async function resolveConfiguredTtsVoice(
  signal: AbortSignal,
  explicitVoice?: string
): Promise<string | undefined> {
  signal.throwIfAborted()
  if (!useConfigStore.getState().loaded) {
    // Cancellation stops this consumer's wait, not the shared public config load.
    await new Promise<void>((resolve, reject) => {
      const abort = () => {
        signal.removeEventListener('abort', abort)
        reject(signal.reason)
      }
      signal.addEventListener('abort', abort, { once: true })
      useConfigStore
        .getState()
        .load()
        .then(resolve, reject)
        .finally(() => {
          signal.removeEventListener('abort', abort)
        })
    })
  }
  signal.throwIfAborted()
  const config = useConfigStore.getState()
  if (!config.loaded) throw new Error('TTS configuration is unavailable')
  return resolveTtsVoice(config.ttsProvider, explicitVoice)
}
