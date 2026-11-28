import { describe, expect, it } from 'vitest'
import { formatVoiceDuration } from '@/lib/voice-duration'

describe('formatVoiceDuration', () => {
  it.each([
    [0, '0 sec'],
    [1, '1 sec'],
    [59, '59 sec'],
    [60, '1 min'],
    [89, '1 min 29 sec'],
    [3600, '60 min'],
  ] as const)('displays the exact balance of %i seconds', (seconds, label) => {
    expect(formatVoiceDuration(seconds, 'en-US')).toBe(label)
  })
})
