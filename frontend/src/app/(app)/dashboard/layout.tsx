import type { ReactNode } from 'react'

export default function DashboardLayout({ children }: { children: ReactNode }) {
  return <div className="reference-dashboard-route">{children}</div>
}
