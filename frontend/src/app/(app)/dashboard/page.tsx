'use client'

import { useCallback, useEffect, useRef, useState } from 'react'
import Link from 'next/link'
import { useLocale, useTranslations } from 'next-intl'
import { BookOpen, Check, Flame, Library, Play, Trophy, UserRound, Sparkles, Users, Settings, CircleHelp, MessageCircle, RefreshCw, Shield, Crown } from 'lucide-react'
import { apiFetch } from '@/lib/api'
import { isSubscribed, needsPaymentRecovery, isFreemiumTrialActive, useAuthStore } from '@/store/auth'
import { useProgressStore } from '@/store/progress'
import { useLanguageStore } from '@/store/language'
import { useConfigStore } from '@/store/config'
import { subscriptionTimestamp } from '@/lib/subscription-time'
import OnboardingTour from '@/components/tour/OnboardingTour'
import WhatsNew from '@/components/whats-new/WhatsNew'
import { PageLoading } from '@/components/ui/page-loading'
import { SubscriptionPlanButtons } from '@/components/billing/SubscriptionPlanButtons'
import { subscribeToLearningProgressUpdated } from '@/lib/learning-progress'
import { AuthAvatarImage } from '@/components/AuthAvatarImage'
import './dashboard-reference.css'
import './dashboard-layout-fix.css'

interface TodayLessonItem { id:number|null;title:string;lesson_type:string;week:number;day:number;objectives:string[];estimated_minutes:number;is_completed:boolean }
interface CompletionState { state:'in_progress'|'ready'|'taken';score:number|null;recommendation:string|null;next_level:string|null }
interface FriendItem { id:number;username:string;display_name:string;avatar?:string|null;target_language?:string }
interface HistoryEntry { date:string;xp_earned:number;lessons_completed:number;exercises_correct:number;exercises_total:number;streak_day:number;skills:Record<string,number> }
interface Goal { daily_xp:number;daily_xp_target:number;daily_progress:number;weekly_xp:number;weekly_xp_target:number;weekly_progress:number }
interface LeagueEntry { user_id:number;username:string;display_name:string;rank:number;xp:number;is_current_user:boolean }
interface League { joined:boolean;tier:string;ends_at:string;entries:LeagueEntry[];current_user:LeagueEntry|null;total:number }
type HistoryRange='week'|'month'|'all'
const TIERS=['bronze','silver','gold','sapphire','ruby','diamond']
const AR_TIERS=['البرونزي','الفضي','الذهبي','الياقوت الأزرق','الياقوت الأحمر','الماسي']

function ProgressTrack({value,label}:{value:number;label:string}) {
  const safe=Math.max(0,Math.min(100,Number.isFinite(value)?value:0))
  return <div className="reference-dashboard-track" role="progressbar" aria-label={label} aria-valuemin={0} aria-valuemax={100} aria-valuenow={safe}><span style={{width:safe+'%'}}/></div>
}

export default function DashboardPage() {
  const locale=useLocale()
  const rtl=locale==='ar'
  const t=useTranslations('dashboard')
  const tProgress=useTranslations('progress')
  const tBilling=useTranslations('billing')
  const tNav=useTranslations('nav')
  const tTarget=useTranslations('targetLanguages')
  const tError=useTranslations('error')
  const text=(ar:string,en:string)=>rtl?ar:en
  const user=useAuthStore(s=>s.user)
  const accessToken=useAuthStore(s=>s.accessToken)
  const stripeEnabled=useConfigStore(s=>s.stripeEnabled)
  const {streak,xp,todayLessons,completedToday,setProgress,setTodayLessons}=useProgressStore()
  const activeLanguage=useLanguageStore(s=>s.activeLanguage)
  const switching=useLanguageStore(s=>s.isSwitching)
  const [loading,setLoading]=useState(true)
  const [loadError,setLoadError]=useState(false)
  const [hasPlan,setHasPlan]=useState(false)
  const [completion,setCompletion]=useState<CompletionState|null>(null)
  const [cefrLevel,setCefrLevel]=useState<string|null>(null)
  const [progressDay,setProgressDay]=useState(0)
  const [totalDays,setTotalDays]=useState(0)
  const [accuracy,setAccuracy]=useState(0)
  const [totalLessons,setTotalLessons]=useState(0)
  const [vocabularyLevel,setVocabularyLevel]=useState<string|null>(null)
  const [vocabularyMastered,setVocabularyMastered]=useState(0)
  const [vocabularyTotal,setVocabularyTotal]=useState(0)
  const [vocabularyProgress,setVocabularyProgress]=useState(0)
  const [goal,setGoal]=useState<Goal|null>(null)
  const [league,setLeague]=useState<League|null>(null)
  const [leagueError,setLeagueError]=useState(false)
  const [friendsError,setFriendsError]=useState(false)
  const [historyError,setHistoryError]=useState(false)
  const [portalLoading,setPortalLoading]=useState(false)
  const [portalError,setPortalError]=useState<string|null>(null)
  const [historyRange,setHistoryRange]=useState<HistoryRange>('week')
  const [historyEntries,setHistoryEntries]=useState<HistoryEntry[]>([])
  const [refreshing,setRefreshing]=useState(false)
  const [friends,setFriends]=useState<FriendItem[]>([])
  const generation=useRef(0)
  const inFlight=useRef(false)
  const accountId=user?.id
  const languageCode=activeLanguage?.code

  const loadData=useCallback(async()=>{
    if(!accountId||!accessToken||switching)return
    const epoch=++generation.current
    inFlight.current=true
    const read=async(path:string,optional404=false)=>{
      const res=await apiFetch(path)
      if(optional404&&res.status===404)return null
      if(!res.ok)throw new Error('Dashboard read failed')
      return res.json()
    }
    const results=await Promise.allSettled([
      read('/api/progress/summary'),read('/api/study-plan/today',true),
      read('/api/progress/history?range='+historyRange),read('/api/social/friends'),
      read('/api/progress/goals',true),
      languageCode?read('/api/leagues/current?target_language='+encodeURIComponent(languageCode)+'&limit=10'):Promise.resolve(null),
    ])
    if(epoch!==generation.current)return
    const [summary,plan,history,social,goals,division]=results
    // The dashboard shell is still useful when an optional panel fails. Keep
    // the banner for the core progress payload only, and show panel-specific
    // states below instead of claiming the whole dashboard is broken.
    setLoadError(summary.status==='rejected')
    if(summary.status==='fulfilled'){
      const p=summary.value
      setProgress({streak:p.current_streak??0,xp:p.total_xp??0,skills:p.skills??{}})
      setAccuracy(Math.round(Math.max(0,Math.min(1,p.accuracy??0))*100))
      setTotalLessons(p.total_lessons??0)
      setVocabularyLevel(p.vocabulary_level??null);setVocabularyMastered(p.vocabulary_mastered??0)
      setVocabularyTotal(p.vocabulary_total??0);setVocabularyProgress(p.vocabulary_progress??0)
    }
    if(plan.status==='fulfilled'){
      const p=plan.value
      setHasPlan(Boolean(p));setCefrLevel(p?.cefr_level??null);setCompletion(p?.completion??null)
      setProgressDay(p?.progress_day??0);setTotalDays(p?.total_days??0)
      setTodayLessons((p?.lessons??[]).map((l:TodayLessonItem)=>({id:l.id,title:l.title,lessonType:l.lesson_type,week:l.week,day:l.day,objectives:l.objectives||[],estimatedMinutes:l.estimated_minutes||25,isCompleted:l.is_completed})))
    }
    setHistoryError(history.status==='rejected');setFriendsError(social.status==='rejected');setLeagueError(division.status==='rejected')
    setHistoryEntries(history.status==='fulfilled'&&Array.isArray(history.value?.entries)?history.value.entries:[])
    setFriends(social.status==='fulfilled'&&Array.isArray(social.value)?social.value.slice(0,6):[])
    setGoal(goals.status==='fulfilled'?goals.value:null)
    setLeague(division.status==='fulfilled'?division.value:null)
    inFlight.current=false;setLoading(false);setRefreshing(false)
  },[accountId,accessToken,switching,languageCode,historyRange,setProgress,setTodayLessons])
  useEffect(()=>{
    generation.current+=1;inFlight.current=false;setLoading(true)
    setHistoryEntries([]);setFriends([]);setLeague(null);setGoal(null)
    setHasPlan(false);setCompletion(null);setCefrLevel(null);setProgressDay(0);setTotalDays(0)
    setAccuracy(0);setTotalLessons(0);setVocabularyLevel(null);setVocabularyMastered(0);setVocabularyTotal(0);setVocabularyProgress(0)
    setProgress({streak:0,xp:0,skills:{}});setTodayLessons([])
    return ()=>{generation.current+=1}
  },[accountId,languageCode,switching,setProgress,setTodayLessons])
  useEffect(()=>{void loadData();return()=>{generation.current+=1;inFlight.current=false}},[loadData])
  const refresh=useCallback(()=>{if(inFlight.current||switching)return;setRefreshing(true);void loadData()},[loadData,switching])
  useEffect(()=>{
    const onVisible=()=>{if(document.visibilityState==='visible')refresh()}
    window.addEventListener('focus',refresh)
    document.addEventListener('visibilitychange',onVisible)
    const unsubscribe=subscribeToLearningProgressUpdated(refresh)
    return()=>{
      window.removeEventListener('focus',refresh)
      document.removeEventListener('visibilitychange',onVisible)
      unsubscribe()
    }
  },[refresh])
  async function handleManageSubscription(){setPortalLoading(true);setPortalError(null);try{const res=await apiFetch('/api/billing/portal',{method:'POST'});if(!res.ok)throw new Error(tBilling('portalError'));const {url}=await res.json();window.location.assign(url)}catch(err){setPortalError(err instanceof Error?err.message:tBilling('portalError'));setPortalLoading(false)}}
  if(loading||switching)return <PageLoading label={t('loadingProgress')} minHeight="min-h-screen"/>
  const completedLessonCount=todayLessons.filter(l=>(l.id&&completedToday.includes(l.id))||l.isCompleted).length
  const nextLesson=todayLessons.find(l=>l.id&&!completedToday.includes(l.id)&&!l.isCompleted)
  const positionComplete=completion?.state==='ready'||completion?.state==='taken'
  const planCompletion=hasPlan&&totalDays>0?positionComplete?100:Math.min(100,Math.round(progressDay/totalDays*100)):0
  const currentDay=positionComplete?totalDays:Math.min(progressDay+1,totalDays)
  const dailyProgress=goal?Math.round(goal.daily_progress*100):0
  const lessonProgress=todayLessons.length?Math.round(completedLessonCount/todayLessons.length*100):0
  const vocabularyPct=Math.max(0,Math.min(100,Math.round(vocabularyProgress*100)))
  const chartEntries=historyEntries.slice(historyRange==='week'?-7:historyRange==='month'?-31:-60)
  const chartMax=Math.max(1,...chartEntries.map(e=>e.xp_earned))
  const name=user?.displayName||user?.username||''
  const tierIndex=league?TIERS.indexOf(league.tier):-1
  const trialEnd=subscriptionTimestamp(user?.freemium_trial_ends_at)
  const trialDays=trialEnd===null?0:Math.max(0,Math.ceil((trialEnd-Date.now())/86400000))
  const ownOutside=league?.current_user&&!league.entries.some(e=>e.user_id===league.current_user?.user_id)?league.current_user:null
  return <><OnboardingTour/><WhatsNew/><div className="juba-page-shell reference-dashboard" dir={rtl?'rtl':'ltr'} data-dashboard-version="reference-v4">{loadError&&<div className="reference-dashboard-alert" role="alert"><span>{tError('body')}</span><button disabled={refreshing} onClick={refresh}>{tError('retry')}</button></div>}<div className="reference-dashboard-layout"><div className="reference-dashboard-main"><header className="reference-dashboard-welcome"><span className="reference-dashboard-welcome-mark" aria-hidden="true"><BookOpen size={40}/></span><div><h1>{t('welcomeBack')} <strong><bdi>{name}</bdi>!</strong></h1><p>{text('أكملت ','You have completed ')}<strong>{dailyProgress}% {text('من هدفك اليومي!','of your daily goal!')}</strong></p></div><button className="reference-dashboard-refresh" aria-label={t('refresh')} disabled={refreshing} onClick={refresh}><RefreshCw size={18}/></button></header><div className="reference-dashboard-overview"><section className="reference-dashboard-card"><div className="reference-dashboard-card-head"><h2>{t('planProgress')}</h2><Link href="/plan">{t('goToMyPlan')}</Link></div><div className="reference-dashboard-progress-row"><span className="reference-dashboard-tile"><BookOpen size={23}/></span><div><span>{t('currentDay')} · {cefrLevel||'A1'}</span><ProgressTrack value={planCompletion} label={t('planProgress')}/></div><small>{currentDay}/{totalDays}</small></div><div className="reference-dashboard-progress-row"><span className="reference-dashboard-tile green"><Library size={23}/></span><div><span>{t('vocabularyProgress',{level:vocabularyLevel||'A1'})}</span><ProgressTrack value={vocabularyPct} label={tNav('vocabulary')}/></div><small>{vocabularyMastered}/{vocabularyTotal}</small></div><div className="reference-dashboard-progress-row"><span className="reference-dashboard-tile purple"><Check size={23}/></span><div><span>{t('lessonsCompletedToday')}</span><ProgressTrack value={lessonProgress} label={t('lessonsCompletedToday')}/></div><small>{completedLessonCount}/{todayLessons.length}</small></div></section><section className="reference-dashboard-card"><div className="reference-dashboard-card-head"><h2>{tProgress('dailyGoal')}</h2><Link href="/progress">{tProgress('goals')}</Link></div><div className="reference-dashboard-progress-row"><span className="reference-dashboard-tile"><Trophy size={23}/></span><div><span>{text('تقدم XP','XP progress')}</span><ProgressTrack value={dailyProgress} label={tProgress('dailyGoal')}/></div><small>{goal?`${goal.daily_xp}/${goal.daily_xp_target}`:'0/0'}</small></div><div className="reference-dashboard-mini-chart" aria-label={text('نقاط الأسبوع','Weekly XP')}>{historyEntries.slice(-7).map(e=><div key={e.date} title={`${e.date}: ${e.xp_earned} XP`}><span style={{height:Math.max(0,e.xp_earned/chartMax*100)+'%'}}/><small>{new Date(e.date+'T00:00:00').toLocaleDateString(locale,{weekday:'narrow'})}</small></div>)}</div>{!goal&&<p className="reference-dashboard-caption">{t('startWithAssessment')}</p>}</section></div><section className="reference-dashboard-card reference-dashboard-league" aria-label={text('الدوري الأسبوعي','Weekly league')}><div className="reference-dashboard-card-head"><h2>{league?.joined?(rtl?(AR_TIERS[tierIndex]||league.tier):league.tier.charAt(0).toUpperCase()+league.tier.slice(1))+text(' · الدوري',' League'):text('الدوري الأسبوعي','Weekly league')} </h2><Link href="/leagues">{text('عرض الكل','View all')}</Link></div>{league?.joined&&<p className="reference-dashboard-caption">{text('ينتهي ','Ends ')}{new Date(league.ends_at).toLocaleDateString(locale,{month:'short',day:'numeric'})}</p>}<div className="reference-dashboard-medals" aria-hidden="true">{TIERS.map((tier,i)=><span key={tier} data-tier={tier} data-active={league?.joined&&i===tierIndex}><Shield size={27}/></span>)}</div>{leagueError?<div className="reference-dashboard-empty" role="alert"><p>{text('تعذر تحميل الدوري.','Could not load your league.')}</p><button onClick={refresh}>{tError('retry')}</button></div>:league?.joined?<><ol className="reference-dashboard-standings">{[...league.entries,...(ownOutside?[ownOutside]:[])].map(e=><li key={e.user_id} data-current={e.is_current_user}><span>{e.rank}</span><span className="reference-dashboard-standing-avatar" aria-hidden="true">{(e.display_name||e.username).slice(0,1).toUpperCase()}</span><strong><bdi>{e.display_name||e.username}</bdi></strong><small>{e.xp} XP</small></li>)}</ol>{!league.entries.length&&<p className="reference-dashboard-caption">{text('لا توجد نتائج مسجلة بعد.','No results recorded yet.')}</p>}</>:<div className="reference-dashboard-empty"><Trophy size={30}/><p>{text('انضم إلى الدوري لتنافس بنقاط تعلّمك الحقيقية.','Join your league and compete with your real learning XP.')}</p><Link className="juba-primary-button" href="/leagues">{text('استكشف الدوري','Explore league')}</Link></div>}</section><section className="reference-dashboard-card reference-dashboard-history"><div className="reference-dashboard-card-head"><h2>{text('النقاط المكتسبة','XP earned')}</h2><div className="reference-dashboard-ranges" role="group" aria-label={t('recentPerformance')}>{(['week','month','all'] as const).map(range=><button key={range} aria-pressed={historyRange===range} onClick={()=>setHistoryRange(range)}>{t('historyRanges.'+range)}</button>)}</div></div><div className="reference-dashboard-chart" aria-label={t('xp')}><div className="reference-dashboard-chart-axis" aria-hidden="true">{[1,.75,.5,.25,0].map(n=><span key={n}>{Math.round(chartMax*n)}</span>)}</div><div className="reference-dashboard-chart-bars">{chartEntries.map(e=><div key={e.date} className="reference-dashboard-bar" title={`${e.date}: ${e.xp_earned} XP`}><div><span style={{height:(e.xp_earned/chartMax*100)+'%'}}/></div><small>{new Date(e.date+'T00:00:00').toLocaleDateString(locale,{month:'short',day:'numeric'})}</small></div>)}</div>{!chartEntries.length&&<div className="reference-dashboard-chart-empty" role={historyError?'alert':'status'}><p>{historyError?text('تعذر تحميل النشاط.','Could not load activity.'):text('لا يوجد نشاط مسجل لهذه الفترة.','No recorded activity for this period.')}</p>{historyError?<button onClick={refresh}>{tError('retry')}</button>:<Link href="/plan">{t('goToMyPlan')}</Link>}</div>}</div>{chartEntries.length>0&&<details className="reference-dashboard-chart-data"><summary>{text('عرض بيانات الرسم','View chart data')}</summary><div className="reference-dashboard-table"><table><thead><tr><th>{t('today')}</th><th>XP</th><th>{t('lessonsCompleted')}</th></tr></thead><tbody>{chartEntries.map(e=><tr key={e.date}><td>{e.date}</td><td>{e.xp_earned}</td><td>{e.lessons_completed}</td></tr>)}</tbody></table></div></details>}</section><section className="reference-dashboard-card reference-dashboard-next"><div className="reference-dashboard-card-head"><h2>{t('nextStep')}</h2><Link href="/plan">{t('goToMyPlan')}</Link></div><div className="reference-dashboard-lessons">{todayLessons.length?todayLessons.map((l,i)=>{const done=Boolean((l.id&&completedToday.includes(l.id))||l.isCompleted);const current=!done&&Boolean(nextLesson)&&l.id===nextLesson?.id;return <div className="reference-dashboard-lesson" key={l.id??`${i}-${l.title}`} data-current={current} aria-current={current?'step':undefined}><span className="reference-dashboard-node" data-done={done}>{done?<Check size={16}/>:current?<Play size={14}/>:i+1}</span><div><small>{l.lessonType} · {l.estimatedMinutes} {t('minutes')}</small><strong>{l.title}</strong><p>{l.objectives?.[0]||''}</p></div>{current&&l.id?<Link className="juba-primary-button" href={'/lesson/'+l.id}>{t('startLesson')}</Link>:done?<Check size={16}/>:null}</div>}):<div className="reference-dashboard-empty"><BookOpen size={24}/><p>{hasPlan?t('noLessons'):t('startWithAssessment')}</p><Link className="juba-primary-button" href={hasPlan?'/plan':'/assessment'}>{hasPlan?t('goToMyPlan'):t('takeAssessment')}</Link></div>}</div></section></div><aside className="reference-dashboard-rail" aria-label={text('ملخص التعلّم','Learning summary')}><section className="reference-dashboard-profile"><span className="reference-dashboard-avatar">{user?.avatar?<AuthAvatarImage avatar={user.avatar} alt="" width={96} height={96} className="h-full w-full object-cover"/>:<UserRound size={40}/>}</span><strong><bdi>{name}</bdi></strong><p>{cefrLevel||'A1'} · {activeLanguage?(tTarget.has(activeLanguage.code)?tTarget(activeLanguage.code):activeLanguage.code):''}</p><dl className="reference-dashboard-profile-stats"><div><dt>XP</dt><dd>{xp}</dd></div><div><dt><Crown size={18}/><span className="sr-only">{t('lessonsCompleted')}</span></dt><dd>{totalLessons}</dd></div><div><dt><Flame size={18}/><span className="sr-only">{t('streak')}</span></dt><dd>{streak}</dd></div><div><dt><Check size={18}/><span className="sr-only">{t('accuracy')}</span></dt><dd>{accuracy}%</dd></div></dl></section><nav className="reference-dashboard-utilities" aria-label={text('أدوات الحساب','Account utilities')}><Link href="/friends" aria-label={tNav('friends')}><Users size={17}/></Link><Link href="/chat" aria-label={tNav('tutor')}><MessageCircle size={17}/></Link><Link href="/faq" aria-label={tNav('faq')}><CircleHelp size={17}/></Link><Link href="/settings" aria-label={tNav('settings')}><Settings size={17}/></Link></nav><section className="reference-dashboard-card"><div className="reference-dashboard-card-head"><h2>{tProgress('weeklyGoal')}</h2><Link href="/progress">{tProgress('goals')}</Link></div><div className="reference-dashboard-achievement"><span className="reference-dashboard-achievement-icon"><Trophy size={28}/><small>XP</small></span><div><strong>{text('حافظ على الاستمرارية','Keep your momentum')}</strong><p>{goal?`${goal.weekly_xp}/${goal.weekly_xp_target} XP`:t('startWithAssessment')}</p><ProgressTrack value={goal?goal.weekly_progress*100:0} label={tProgress('weeklyGoal')}/></div></div></section><section className="reference-dashboard-card reference-dashboard-friends-card"><div className="reference-dashboard-card-head"><h2>{tNav('friends')}</h2><Link href="/friends">{text('عرض الكل','View all')}</Link></div>{friends.length?<div className="reference-dashboard-friends">{friends.map(f=><Link href={'/friends/chat/'+f.id} key={f.id}><span className="reference-dashboard-friend-avatar">{f.avatar?<AuthAvatarImage avatar={f.avatar} alt="" width={32} height={32} className="h-full w-full object-cover"/>:(f.display_name||f.username).slice(0,1).toUpperCase()}</span><span><strong><bdi>{f.display_name||f.username}</bdi></strong><small>{f.target_language||''}</small></span><MessageCircle size={14}/></Link>)}</div>:<div className="reference-dashboard-empty compact" role={friendsError?'alert':'status'}><Users size={24}/><p>{friendsError?text('تعذر تحميل الأصدقاء.','Could not load friends.'):text('تعلّم مع أصدقائك.','Learn with your friends.')}</p><Link href="/friends">{tNav('friends')}</Link></div>}</section>{stripeEnabled&&!isSubscribed(user,stripeEnabled)&&<section className="reference-dashboard-card reference-dashboard-premium"><Sparkles size={22}/><h2>{text('Go أو Plus','Go or Plus')}</h2>{isFreemiumTrialActive(user,stripeEnabled)&&<p>{tBilling('trialDays',{days:trialDays})}</p>}{needsPaymentRecovery(user)?<button className="juba-primary-button" onClick={handleManageSubscription} disabled={portalLoading}>{portalLoading?'…':tBilling('manage')}</button>:<SubscriptionPlanButtons/>}{portalError&&<p role="alert">{portalError}</p>}</section>}</aside></div></div></>}
