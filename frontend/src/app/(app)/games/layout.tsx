import type {ReactNode} from 'react'
import CompetitionStandings from '@/components/games/CompetitionStandings'
import LeagueMovement from '@/components/games/LeagueMovement'
import LeagueRiskAlert from '@/components/games/LeagueRiskAlert'
import GameProgressSummary from '@/components/games/GameProgressSummary'

export default function GamesLayout({children}:{children:ReactNode}){
  return <><LeagueRiskAlert/>{children}<GameProgressSummary/><LeagueMovement/><CompetitionStandings/></>
}
