import { beforeEach, describe, expect, it, vi } from 'vitest'
import { resolveTtsVoice } from '@/lib/tts-voice'

beforeEach(() => localStorage.clear())

describe('provider-aware TTS voice preferences', () => {
  it('keeps both preferences when switching providers', () => {
    localStorage.setItem('tts_voice', 'coral')
    localStorage.setItem('gemini_tts_voice', 'male')

    expect(resolveTtsVoice('openai')).toBe('coral')
    expect(resolveTtsVoice('gemini')).toBe('male')
    expect(resolveTtsVoice('openai')).toBe('coral')
    expect(localStorage.getItem('gemini_tts_voice')).toBe('male')
    expect(localStorage.getItem('tts_voice')).toBe('coral')
  })

  it.each([
    ['openai', 'tts_voice', 'female'],
    ['gemini', 'gemini_tts_voice', 'nova'],
    ['gemini', 'gemini_tts_voice', 'Kore'],
  ])(
    'ignores an incompatible stored or explicit voice for %s',
    (provider, key, voice) => {
      localStorage.setItem(key, voice)
      expect(resolveTtsVoice(provider, voice)).toBeUndefined()
      expect(localStorage.getItem(key)).toBe(voice)
    }
  )

  it.each([
    ['openai', 'tts_voice', 'alloy', 'nova'],
    ['gemini', 'gemini_tts_voice', 'male', 'female'],
  ])(
    'prefers a compatible explicit voice for %s',
    (provider, key, stored, explicit) => {
      localStorage.setItem(key, stored)
      expect(resolveTtsVoice(provider, explicit)).toBe(explicit)
      expect(resolveTtsVoice(provider, 'invalid')).toBe(stored)
    }
  )

  it('leaves default selection to the backend without a user preference', () => {
    expect(resolveTtsVoice('gemini')).toBeUndefined()
    expect(resolveTtsVoice('openai')).toBeUndefined()
    localStorage.setItem('tts_voice', 'nova')
    expect(resolveTtsVoice('gemini')).toBeUndefined()
  })

  it('retains the existing local-provider request behavior', () => {
    localStorage.setItem('tts_voice', 'nova')
    expect(resolveTtsVoice('local')).toBe('nova')
    expect(resolveTtsVoice('local', 'af_heart')).toBe('af_heart')
    localStorage.removeItem('tts_voice')
    localStorage.setItem('gemini_tts_voice', 'male')
    expect(resolveTtsVoice('local')).toBeUndefined()
  })

  it('tolerates unavailable browser storage', () => {
    vi.spyOn(localStorage, 'getItem').mockImplementation(() => {
      throw new DOMException('Storage blocked', 'SecurityError')
    })
    expect(resolveTtsVoice('gemini')).toBeUndefined()
    expect(resolveTtsVoice('openai')).toBeUndefined()
    expect(resolveTtsVoice('gemini', 'female')).toBe('female')
  })
})
