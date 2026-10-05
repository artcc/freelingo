'use client'

import { useCallback, useEffect, useRef, useState } from 'react'
import Link from 'next/link'
import { useLocale } from 'next-intl'
import { apiFetch } from '@/lib/api'
import { subscribeToLearningProgressUpdated } from '@/lib/learning-progress'
import { useLanguageStore } from '@/store/language'
import { useAuthStore } from '@/store/auth'
import './game-progress-summary.css'

type SkillScore = Record<string, number>
type ProgressState =
  | { kind: 'loading' }
  | { kind: 'error' }
  | { kind: 'ready'; totalXp: number; streak: number; skills: SkillScore }

type SummaryProps = { arabic: boolean; state: ProgressState; onRetry: () => void }

const skillLabels: Record<string, { ar: string; en: string }> = {
  memory: { ar: 'ذاكرة', en: 'Memory' },
  vocabulary: { ar: 'مفردات', en: 'Vocabulary' },
  writing: { ar: 'كتابة', en: 'Writing' },
  listening: { ar: 'استماع', en: 'Listening' },
  grammar: { ar: 'قواعد', en: 'Grammar' },
}

export function GameProgressSummaryView({ arabic, state, onRetry }: SummaryProps) {
  const copy = (ar: string, en: string) => arabic ? ar : en
  const skills = state.kind === 'ready' ? Object.entries(state.skills).filter(([, value]) => Number.isFinite(value)).sort((a, b) => b[1] - a[1]).slice(0, 3) : []
  return <section className="juba-page-shell game-progress-summary" dir={arabic ? 'rtl' : 'ltr'} aria-label={copy('اللعب ونقاط التعلّم', 'Play and learning XP')}>
    <div className="game-progress-summary-copy">
      <span className="game-progress-summary-kicker">JUBA LISAN</span>
      <h2>{copy('العب، تعلّم، وتابع تقدّمك', 'Play, learn, track your progress')}</h2>
      <p>{copy('تُضاف نقاط الجولات المحفوظة إلى تقدّمك في لوحة التحكم. الخادم يحدد المكافأة، وليست كل إعادة لعب مكافأة إضافية.', 'Saved-round XP contributes to your dashboard progress. The server decides rewards; replay is not a guaranteed extra reward.')}</p>
    </div>
    <div className="game-progress-summary-account" aria-live="polite">
      {state.kind === 'loading' ? <p role="status">{copy('جارٍ تحميل تقدّم اللغة النشطة…', 'Loading active-language progress…')}</p>
        : state.kind === 'error' ? <div role="alert"><p>{copy('تعذر تحميل النقاط. لم نغيّر بياناتك.', 'Could not load XP. Your data has not been changed.')}</p><button type="button" onClick={onRetry}>{copy('إعادة المحاولة', 'Retry')}</button></div>
        : <><dl><div><dt>{copy('إجمالي XP في مسار اللغة النشط', 'Total XP in your active language track')}</dt><dd><bdi>{state.totalXp}</bdi> <span>XP</span></dd></div><div><dt>{copy('أيام الاستمرارية', 'Streak days')}</dt><dd><bdi>{state.streak}</bdi></dd></div></dl>{skills.length > 0 && <div className="game-progress-summary-skills"><strong>{copy('أبرز المهارات', 'Top skills')}</strong>{skills.map(([skill, value]) => <div className="game-progress-summary-skill" key={skill}><span>{skillLabels[skill]?.[arabic ? 'ar' : 'en'] ?? skill}</span><progress max={1} value={Math.max(0, Math.min(1, value))} aria-label={`${skill} ${Math.round(value * 100)}%`} /><bdi>{Math.round(value * 100)}%</bdi></div>)}</div>}</>}
      <nav aria-label={copy('متابعة التقدم', 'Track progress')}><Link href="/games">{copy('العب الآن', 'Play now')}</Link><Link href="/dashboard">{copy('لوحة التحكم', 'Dashboard')}</Link><Link href="/progress">{copy('تفاصيل التقدم', 'Progress details')}</Link></nav>
    </div>
  </section>
}

export default function GameProgressSummary() {
  const arabic = useLocale().startsWith('ar')
  const accountId = useAuthStore(state => state.user?.id)
  const language = useLanguageStore(state => state.activeLanguage?.code)
  const switching = useLanguageStore(state => state.isSwitching)
  const [state, setState] = useState<ProgressState>({ kind: 'loading' })
  const generation = useRef(0)
  const request = useRef<AbortController | null>(null)
  const load = useCallback(async () => {
    request.current?.abort()
    const current = ++generation.current
    if (!accountId || !language || switching) { setState({ kind: 'loading' }); return }
    const controller = new AbortController()
    request.current = controller
    setState({ kind: 'loading' })
    try {
      const response = await apiFetch('/api/progress/summary', { signal: controller.signal })
      if (!response.ok) throw new Error('Progress unavailable')
      const value: unknown = await response.json()
      if (!value || typeof value !== 'object') throw new Error('Invalid progress')
      const data = value as { total_xp?: unknown; current_streak?: unknown; skills?: unknown }
      if (typeof data.total_xp !== 'number' || !Number.isFinite(data.total_xp) || data.total_xp < 0 || typeof data.current_streak !== 'number' || !Number.isFinite(data.current_streak) || data.current_streak < 0) throw new Error('Invalid progress')
      const skills: SkillScore = data.skills && typeof data.skills === 'object' && !Array.isArray(data.skills)
        ? Object.fromEntries(Object.entries(data.skills).filter(([, score]) => typeof score === 'number' && Number.isFinite(score)))
        : {}
      if (current === generation.current && !controller.signal.aborted && useAuthStore.getState().user?.id === accountId && useLanguageStore.getState().activeLanguage?.code === language && !useLanguageStore.getState().isSwitching) setState({ kind: 'ready', totalXp: data.total_xp, streak: data.current_streak, skills })
    } catch {
      if (current === generation.current && !controller.signal.aborted) setState({ kind: 'error' })
    }
  }, [accountId, language, switching])
  useEffect(() => {
    void load()
    const refresh = () => { void load() }
    const onVisible = () => { if (document.visibilityState === 'visible') refresh() }
    const unsubscribe = subscribeToLearningProgressUpdated(refresh)
    window.addEventListener('focus', refresh)
    document.addEventListener('visibilitychange', onVisible)
    return () => {
      generation.current += 1; request.current?.abort(); unsubscribe()
      window.removeEventListener('focus', refresh)
      document.removeEventListener('visibilitychange', onVisible)
    }
  }, [load])
  return <GameProgressSummaryView arabic={arabic} state={state} onRetry={() => { void load() }} />
}
