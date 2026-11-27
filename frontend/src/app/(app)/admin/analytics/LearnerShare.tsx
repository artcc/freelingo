import { useFormatter, useTranslations } from 'next-intl'

export function LearnerShare({
  count,
  total,
}: {
  count: number | null
  total: number
}) {
  const t = useTranslations('adminAnalytics')
  const format = useFormatter()
  if (total === 0) return t('noLearners')
  if (count === null) return t('pending')

  const share = format.number(count / total, {
    style: 'percent',
    maximumFractionDigits: 1,
  })
  return `${format.number(count)} (${share})`
}
