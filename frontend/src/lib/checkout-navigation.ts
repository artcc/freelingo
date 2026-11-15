import type { BillingInterval } from '@/lib/billing-copy'

export function getSelectedPlan(plan: string | null): BillingInterval | null {
  return plan === 'monthly' || plan === 'yearly' ? plan : null
}

export function checkoutNavigationHref(
  path:
    | '/register'
    | '/login'
    | '/onboarding'
    | '/settings'
    | '/terms'
    | '/privacy',
  plan: string | null,
  invite?: string | null
): string {
  const query = new URLSearchParams()
  if (path === '/terms' || path === '/privacy') query.set('from', 'register')
  const selectedPlan = getSelectedPlan(plan)
  if (selectedPlan) query.set('plan', selectedPlan)
  if (invite && path !== '/onboarding' && path !== '/settings') {
    query.set('invite', invite)
  }
  const search = query.toString()
  return `${path}${search ? `?${search}` : ''}${path === '/settings' ? '#plan' : ''}`
}
