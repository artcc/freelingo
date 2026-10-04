import type { ReactNode } from 'react'
import ReferenceFeatures from './ReferenceFeatures'
import CompetitionStandings from '@/components/games/CompetitionStandings'
import LeagueMovement from '@/components/games/LeagueMovement'
import LeagueRiskAlert from '@/components/games/LeagueRiskAlert'
import GameProgressSummary from '@/components/games/GameProgressSummary'

export default function DashboardLayout({children}:{children:ReactNode}){
  return <div className="reference-dashboard-route"><LeagueRiskAlert/>{children}<GameProgressSummary/><LeagueMovement/><CompetitionStandings/><ReferenceFeatures/></div>
}
