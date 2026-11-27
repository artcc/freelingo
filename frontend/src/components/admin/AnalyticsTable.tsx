import type { ReactNode } from 'react'
import { useTranslations } from 'next-intl'

export function AnalyticsTable({
  title,
  headers,
  rows,
}: {
  title: string
  headers: string[]
  rows: { key: string; cells: ReactNode[] }[]
}) {
  const t = useTranslations('adminAnalytics')
  if (!rows.length) return <p className="text-fl-muted-2">{t('empty')}</p>

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-start text-sm tabular-nums">
        <caption className="sr-only">{title}</caption>
        <thead>
          <tr>
            {headers.map((header) => (
              <th
                key={header}
                scope="col"
                className="border-fl-border text-fl-muted-2 border-b px-2 py-2 text-start font-medium"
              >
                {header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-fl-border divide-y">
          {rows.map(({ key, cells: [label, ...values] }) => (
            <tr key={key}>
              <th scope="row" className="px-2 py-2 text-start font-medium">
                {label}
              </th>
              {values.map((value, index) => (
                <td key={headers[index + 1]} className="px-2 py-2">
                  {value}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
