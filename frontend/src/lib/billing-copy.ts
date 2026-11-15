export type BillingInterval = 'monthly' | 'yearly'

export function hasTwoMonthsFree(monthly: number, yearly: number): boolean {
  if (
    !Number.isFinite(monthly) ||
    !Number.isFinite(yearly) ||
    monthly <= 0 ||
    yearly <= 0
  ) {
    return false
  }
  const monthlyCents = Math.round(monthly * 100)
  const yearlyCents = Math.round(yearly * 100)
  return (
    Number.isSafeInteger(monthlyCents) &&
    Number.isSafeInteger(yearlyCents) &&
    monthlyCents > 0 &&
    Math.abs(monthly * 100 - monthlyCents) < 0.000001 &&
    Math.abs(yearly * 100 - yearlyCents) < 0.000001 &&
    yearlyCents === monthlyCents * 10
  )
}

export function splitYearlyCta(label: string, showSavings = true) {
  const parts = label.split(' · ')
  if (parts.length < 2) return { main: label, savings: null }

  return {
    main: `${parts.slice(0, -1).join(' · ')} →`,
    savings: showSavings
      ? (parts.at(-1)?.replace('→', '').trim() ?? null)
      : null,
  }
}
