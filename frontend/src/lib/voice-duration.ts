/** Format an exact voice balance without rounding a partial minute up. */
export function formatVoiceDuration(seconds: number, locale: string): string {
  const minutes = Math.floor(seconds / 60)
  const remainder = seconds % 60
  const parts: string[] = []
  if (minutes > 0) {
    parts.push(
      new Intl.NumberFormat(locale, { style: 'unit', unit: 'minute' }).format(
        minutes
      )
    )
  }
  if (remainder > 0 || minutes === 0) {
    parts.push(
      new Intl.NumberFormat(locale, { style: 'unit', unit: 'second' }).format(
        remainder
      )
    )
  }
  return parts.join(' ')
}
