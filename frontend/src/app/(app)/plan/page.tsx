'use client'

import {useState,useEffect,useCallback,useRef} from 'react'
import {useRouter} from 'next/navigation'
import {useLocale,useTranslations} from 'next-intl'
import {PageLoading} from '@/components/ui/page-loading'
import {apiFetch} from '@/lib/api'
import {nextLessonFromSources} from '@/lib/plan-next-lesson'
import {getCurriculumUnits,type CurriculumUnit} from '@/data/curriculum'
import {useLanguageStore} from '@/store/language'
import UnitCard from '@/components/plan/UnitCard'
import UnitDrawer from '@/components/plan/UnitDrawer'
import LevelTestBanner from '@/components/plan/LevelTestBanner'
import NoPlanBanner from '@/components/plan/NoPlanBanner'
import type {CEFRLevel} from '@/data/grammar'

type Action='start'|'continue'|'review'
interface PendingLesson{id:number;title:string;lesson_type:string;week_number:number;day_number:number}
interface PlanLesson extends PendingLesson{unit_id:string|null;is_completed:boolean}
interface Lesson{id:number|null;title:string;lesson_type:string;week:number;day:number;unit_id?:string;completed?:boolean;action?:Action}
interface TodayLesson{id:number|null;title:string;lesson_type:string;week:number;day:number;is_completed?:boolean}
interface StudyPlan{id:number;cefr_level:string;duration_weeks:number;days_per_week:number;current_unit:string;completion_test_taken:boolean;completion_test_score:number|null;completion_test_recommendation:string|null;generated_plan:{weekly_plan:{week:number;days:{day:number;title:string;lesson_type:string;unit_id:string}[]}[]}}
interface Journey{plan_id:number;next_lesson_id:number|null;sections:{units:{id:string;progress:number;state:string}[]}[]}
interface Snapshot{plan:StudyPlan;next:number|null;competencies:Record<string,number>;states:Record<string,Pick<Lesson,'id'|'completed'|'action'>>;pending:PendingLesson[];unitStates:Record<string,string>;partial:boolean}
const key=(week:number,day:number,title:string)=>`${week}:${day}:${title}`
async function optional<T>(path:string):Promise<T|null>{try{const r=await apiFetch(path);return r.ok?await r.json() as T:null}catch{return null}}

export default function PlanPage(){
 const t=useTranslations('plan'),common=useTranslations('common'),router=useRouter(),locale=useLocale()
 const activeLanguage=useLanguageStore(s=>s.activeLanguage),switching=useLanguageStore(s=>s.isSwitching)
 const [snapshot,setSnapshot]=useState<Snapshot|null>(null),[loading,setLoading]=useState(true),[noPlan,setNoPlan]=useState(false),[loadError,setLoadError]=useState(false),[launchError,setLaunchError]=useState('')
 const [units,setUnits]=useState<CurriculumUnit[]>([]),[activeDrawer,setActiveDrawer]=useState<CurriculumUnit|null>(null),[launching,setLaunching]=useState(false)
 const requestVersion=useRef(0),context=useRef(0),launchLock=useRef(false),mounted=useRef(false)
 const loadPlan=useCallback(async()=>{
  if(!mounted.current||switching||!activeLanguage?.code)return
  const request=++requestVersion.current,epoch=context.current
  setLoading(true);setLoadError(false);setNoPlan(false);setSnapshot(null);setUnits([]);setActiveDrawer(null);setLaunchError('')
  try{
   // /today creates today's lesson on the first visit. The journey and lesson lists must be
   // read after it; fetched in parallel, a brand-new plan reports next_lesson_id=null and the
   // page showed no start button at all.
   const [response,today]=await Promise.all([
    apiFetch('/api/study-plan/current'),optional<{plan_id:number;lessons:TodayLesson[]}>('/api/study-plan/today'),
   ])
   if(!mounted.current||request!==requestVersion.current||epoch!==context.current)return
   if(response.status===404){setNoPlan(true);return}
   if(!response.ok)throw new Error()
   const [rawJourney,comp,pending,generated]=await Promise.all([
    optional<Journey>('/api/study-plan/learning-path'),optional<Record<string,number>|Array<{unit_id:string;score:number}>>('/api/progress/competencies'),optional<PendingLesson[]>('/api/study-plan/pending-lessons'),optional<PlanLesson[]>('/api/study-plan/lessons'),
   ])
   if(!mounted.current||request!==requestVersion.current||epoch!==context.current)return
   const plan=await response.json() as StudyPlan
   if(!mounted.current||request!==requestVersion.current||epoch!==context.current)return
   const journey=rawJourney?.plan_id===plan.id?rawJourney:null
   const safeToday=today?.plan_id===plan.id&&Array.isArray(today.lessons)?today.lessons:[]
   const competencies:Record<string,number>={},unitStates:Record<string,string>={}
   if(journey){for(const section of journey.sections)for(const unit of section.units){competencies[unit.id]=unit.progress;unitStates[unit.id]=unit.state}}
   else if(Array.isArray(comp)){for(const item of comp)competencies[item.unit_id]=item.score}
   else if(comp)Object.assign(competencies,comp)
   const states:Snapshot['states']={}
   if(Array.isArray(generated))for(const lesson of generated)states[key(lesson.week_number,lesson.day_number,lesson.title)]={id:lesson.id,completed:lesson.is_completed,action:lesson.is_completed?'review':undefined}
   const pendingLessons=Array.isArray(pending)?pending:[]
   for(const lesson of pendingLessons)states[key(lesson.week_number,lesson.day_number,lesson.title)]={id:lesson.id,completed:false,action:'continue'}
   for(const lesson of safeToday){if(lesson.id===null)continue;const lessonKey=key(lesson.week,lesson.day,lesson.title);states[lessonKey]={id:lesson.id,completed:lesson.is_completed??false,action:lesson.is_completed?'review':states[lessonKey]?.action==='continue'?'continue':'start'}}
   setSnapshot({plan,next:nextLessonFromSources(journey,safeToday),competencies,states,pending:pendingLessons,unitStates,partial:!journey||pending===null||generated===null})
  }catch{if(mounted.current&&request===requestVersion.current&&epoch===context.current)setLoadError(true)}finally{if(mounted.current&&request===requestVersion.current&&epoch===context.current)setLoading(false)}
 },[activeLanguage?.code,switching])
 useEffect(()=>{
  mounted.current=true;context.current++;requestVersion.current++;setSnapshot(null);setUnits([]);setActiveDrawer(null);setNoPlan(false);setLoadError(false);setLaunchError('');setLoading(true)
  void loadPlan()
  return()=>{mounted.current=false;context.current++;requestVersion.current++}
 },[loadPlan])
 useEffect(()=>{
  let cancelled=false;setUnits([])
  if(snapshot?.plan.cefr_level&&activeLanguage?.code&&!switching)void getCurriculumUnits(snapshot.plan.cefr_level,activeLanguage.code).then(value=>{if(!cancelled)setUnits(value)}).catch(()=>{if(!cancelled)setUnits([])})
  return()=>{cancelled=true}
 },[snapshot?.plan.id,snapshot?.plan.cefr_level,activeLanguage?.code,switching])
 async function launchLesson(id:number){
  if(launchLock.current||!snapshot||switching)return
  launchLock.current=true;setLaunching(true);setLaunchError('')
  const epoch=context.current
  try{
   const response=await apiFetch('/api/study-plan/launch-lesson',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({lesson_id:id})})
   if(!mounted.current||epoch!==context.current)return
   if(!response.ok){setLaunchError(response.status===409&&t.has('lessonLocked')?t('lessonLocked'):common('error'));return}
   router.push(`/lesson/${id}`)
  }catch{if(mounted.current&&epoch===context.current)setLaunchError(common('error'))}finally{launchLock.current=false;if(mounted.current)setLaunching(false)}
 }
 if(loading||switching||!activeLanguage)return <PageLoading/>
 if(loadError)return <div className="juba-page-shell" role="alert"><p>{common('error')}</p><button className="juba-secondary-button" onClick={()=>void loadPlan()}>{common('retry')}</button></div>
 if(noPlan)return <NoPlanBanner/>
 if(!snapshot)return <PageLoading/>
 const {plan,competencies,pending,states,next,unitStates}=snapshot
 const byUnit:Record<string,Lesson[]>={}
 for(const week of plan.generated_plan.weekly_plan??[])for(const day of week.days??[]){const lesson:Lesson={id:null,title:day.title,lesson_type:day.lesson_type,week:week.week,day:day.day,unit_id:day.unit_id,completed:false,...states[key(week.week,day.day,day.title)]};const unit=lesson.unit_id??'__unassigned';(byUnit[unit]??=[]).push(lesson)}
 const level=plan.cefr_level as CEFRLevel
 const allCompleted=units.length>0&&units.every(unit=>(competencies[unit.id]??0)>=.8)
 const started=Object.values(states).some(state=>state.completed)
 const ar=locale==='ar'
 const startLabel=started?t('resume'):t.has('startLearning')?t('startLearning'):ar?'ابدأ التعلم':'Start learning'
 return <div className="juba-page-shell juba-mobile-plan w-full space-y-5 px-3 py-5 sm:px-6 sm:py-6 lg:px-8">
  <section className="juba-reference-hero px-5 py-5 sm:px-6"><p className="juba-eyebrow">{t('learningRoadmap')}</p><h1 className="text-[28px] font-semibold">{activeLanguage.name} · {level}</h1><p className="mt-3 text-sm text-[var(--juba-muted)]">{t('durationDetail',{weeks:plan.duration_weeks,days:plan.days_per_week})}</p><div className="mt-5 flex flex-wrap gap-4 text-sm"><span>{units.length} {t('unitsLabel')}</span><span>{pending.length} {t('pendingLessons')}</span><span>{Math.round((competencies[plan.current_unit]??0)*100)}%</span></div></section>
  {launchError&&<div role="alert" className="juba-reference-section p-4"><p>{launchError}</p><button className="juba-secondary-button" onClick={()=>setLaunchError('')}>{common('close')}</button></div>}
  {snapshot.partial&&<div className="juba-reference-section p-4" role="status"><p>{common('error')}</p><button className="juba-secondary-button" disabled={launching} onClick={()=>void loadPlan()}>{common('retry')}</button></div>}
  {next!==null&&<section className="juba-reference-section px-5 py-5"><div className="flex flex-wrap items-center justify-between gap-4"><div><p className="juba-eyebrow">{t('learningRoadmap')}</p><h2 className="mt-1 text-xl font-semibold">{startLabel}</h2></div><button disabled={launching} className="juba-primary-button" onClick={()=>void launchLesson(next)}>{launching?common('loading'):startLabel}</button></div></section>}
  {next===null&&pending.length===0&&!allCompleted&&!plan.completion_test_taken&&<section className="juba-reference-section px-5 py-5" role="status"><div className="flex flex-wrap items-center justify-between gap-4"><div><p className="juba-eyebrow">{t('learningRoadmap')}</p><h2 className="mt-1 text-xl font-semibold">{ar?'درس اليوم غير جاهز بعد':"Today's lesson is not ready yet"}</h2><p className="mt-1 text-sm text-[var(--juba-muted)]">{ar?'جرّب تجهيزه الآن.':'Try preparing it now.'}</p></div><button disabled={launching} className="juba-primary-button" onClick={()=>void loadPlan()}>{ar?'جهّز الدرس':'Prepare lesson'}</button></div></section>}
  {pending.length>0&&<section><h2 className="mb-4 text-xl font-semibold">{t('pendingLessons')}</h2><div className="grid gap-3 md:grid-cols-2">{pending.map(lesson=><button key={lesson.id} disabled={launching} onClick={()=>void launchLesson(lesson.id)} className="flex items-center gap-4 rounded-md border border-[var(--juba-border)] bg-[var(--juba-card)] p-4 text-start"><span className="min-w-0 flex-1"><strong className="block text-sm">{lesson.title}</strong><span className="mt-1 block text-xs text-[var(--juba-muted)]">{t('weekDay',{week:lesson.week_number,day:lesson.day_number})}</span></span><span>{t('resume')}</span></button>)}</div></section>}
  <section><h2 className="mb-5 text-xl font-semibold">{t('learningRoadmap')} · {level}</h2><div className="space-y-4">{units.length===0&&<div className="juba-reference-section px-6 py-10 text-center"><p>{t('noUnitsForLevel',{level})}</p><p className="mt-2 text-sm text-[var(--juba-muted)]">{t('noUnitsDesc')}</p></div>}{units.map((unit,index)=>{
   const lessons=byUnit[unit.id]??[],completed=lessons.filter(lesson=>lesson.completed).length,score=competencies[unit.id]??0
   const authoritative=unitStates[unit.id]
   const active=authoritative?authoritative==='active':unit.id===plan.current_unit
   const done=authoritative?authoritative==='completed'||authoritative==='mastered':score>=.8||(completed>0&&completed===lessons.length)
   const prereq=unit.prerequisite_unit?(competencies[unit.prerequisite_unit]??0)>=.8:true
   const locked=authoritative?authoritative==='locked':!active&&!done&&!prereq&&index>0
   return <UnitCard key={unit.id} title={unit.title} index={index} lessonCount={lessons.length||unit.lesson_types.length} grammarCount={unit.grammar_points.length} competency={score} status={{completed:done,active,locked,isLevelTest:false}} onClick={()=>{if(!launching)setActiveDrawer(unit)}} onStartLesson={active&&next!==null&&!launching?()=>void launchLesson(next):undefined}/>
  })}{units.length>0&&<UnitCard title={t('completionTestTitle',{level})} index={units.length} lessonCount={1} grammarCount={0} competency={plan.completion_test_score??0} status={{completed:plan.completion_test_taken,active:allCompleted&&!plan.completion_test_taken,locked:!allCompleted,isLevelTest:true}} onClick={()=>{if(allCompleted&&!plan.completion_test_taken)router.push(`/assessment/level-test?plan=${plan.id}`)}}/>}</div></section>
  {allCompleted&&!plan.completion_test_taken&&<LevelTestBanner planId={plan.id} level={level}/>}
  {plan.completion_test_taken&&<section className="juba-reference-section p-5"><h2>{t('levelTestResult')}</h2><p className="mt-2 text-sm">{t('testScore')} {plan.completion_test_score!==null?`${Math.round(plan.completion_test_score*100)}%`:'n/a'}</p>{plan.completion_test_recommendation&&<p className="mt-2 text-sm">{plan.completion_test_recommendation}</p>}</section>}
  {activeDrawer&&<UnitDrawer unit={activeDrawer} lessons={(byUnit[activeDrawer.id]??[]).map(lesson=>({...lesson,completed:lesson.completed??false}))} onClose={()=>setActiveDrawer(null)} onStartLesson={id=>{setActiveDrawer(null);void launchLesson(id)}}/>}
 </div>
}
