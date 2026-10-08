import { PageLoading } from '@/components/ui/page-loading'

// Keep route Suspense and client-side page loading visually consistent.
export default function AppLoading() {
  return <PageLoading className="bg-fl-bg" />
}
