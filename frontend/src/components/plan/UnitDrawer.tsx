'use client'

import {useEffect,useId,useRef,useState} from 'react'
import {useLocale,useTranslations} from 'next-intl'
import {Check,Lock,X,Play,BookOpen,Headphones,PenLine,MessageCircle,RefreshCw} from 'lucide-react'
import {apiFetch} from '@/lib/api'
import type {CurriculumUnit} from '@/data/curriculum'
import './unit-adventure.css'
interface Lesson{id:number|null;title:string;lesson_type:string;week:number;day:number;completed:boolean;action?:'start'|'continue'|'review'}
interface Props{unit:CurriculumUnit;lessons:Lesson[];onClose:()=>void;onStartLesson:(lessonId:number)=>void;onStartUnit?:()=>void}
interface JourneyLesson{id:number;is_completed:boolean;available:boolean;state:string}
interface Journey{plan_id:number;sections:{units:{id:string;lessons:JourneyLesson[]}[]}[]}
export default function UnitDrawer({unit,lessons,onClose,onStartLesson,onStartUnit}:Props){
 const t=useTranslations('plan'),common=useTranslations('common'),rtl=useLocale().startsWith('ar')
 const word=(ar:string,en:string)=>rtl?ar:en
 const ref=useRef<HTMLDivElement>(null),closeRef=useRef(onClose),alive=useRef(false),lock=useRef(false),controller=useRef<AbortController|null>(null)
 closeRef.current=onClose
 const titleId=useId(),[preparing,setPreparing]=useState(false),[error,setError]=useState('')
 const completed=lessons.filter(l=>l.completed).length,progress=lessons.length?Math.round(completed/lessons.length*100):0
 const nextLesson=lessons.find(l=>l.id!==null&&!l.completed&&(l.action==='start'||l.action==='continue'))
 const unfinished=lessons.some(l=>!l.completed)
 const needsPreparation=!nextLesson&&(unfinished||!lessons.length)
 useEffect(()=>{
  alive.current=true
  const previous=document.activeElement as HTMLElement|null,panel=ref.current,overflow=document.body.style.overflow
  document.body.style.overflow='hidden';panel?.focus()
  function keydown(event:KeyboardEvent){
   if(event.key==='Escape'){event.preventDefault();closeRef.current();return}
   if(event.key!=='Tab')return
   const focusable=Array.from(panel?.querySelectorAll<HTMLElement>('button:not([disabled]),a[href],input:not([disabled]),select:not([disabled]),textarea:not([disabled]),[tabindex="0"]')??[]).filter(e=>!e.closest('[hidden]'))
   if(!focusable.length){event.preventDefault();panel?.focus();return}
   const first=focusable[0],last=focusable[focusable.length-1]
   if(event.shiftKey&&(document.activeElement===first||document.activeElement===panel||!panel?.contains(document.activeElement))){event.preventDefault();last.focus()}
   else if(!event.shiftKey&&(document.activeElement===last||document.activeElement===panel||!panel?.contains(document.activeElement))){event.preventDefault();first.focus()}
  }
  document.addEventListener('keydown',keydown)
  return()=>{alive.current=false;controller.current?.abort();document.body.style.overflow=overflow;document.removeEventListener('keydown',keydown);previous?.focus()}
 },[])
 const typeLabel:Record<string,string>={grammar:t('lessonTypes.grammar'),vocabulary:t('lessonTypes.vocabulary'),reading:t('lessonTypes.reading'),writing:t('lessonTypes.writing'),listening:t('lessonTypes.listening'),conversation:t('lessonTypes.conversation'),review:t('lessonTypes.review'),level_test:t('lessonTypes.level_test')}
 async function start(){
  if(lock.current)return
  if(onStartUnit){onStartUnit();return}
  if(nextLesson?.id!=null){onStartLesson(nextLesson.id);return}
  if(!needsPreparation)return
  lock.current=true;setPreparing(true);setError('')
  const abort=new AbortController();controller.current=abort
  try{
   // /today is the existing quota-controlled generation boundary. Never create
   // arbitrary future lessons or route to a fabricated id from the schedule.
   const response=await apiFetch('/api/study-plan/today',{signal:abort.signal})
   if(!response.ok){
    const data=await response.json().catch(()=>null)
    const detail=typeof data?.detail==='string'?data.detail:''
    throw new Error(response.status===402?word('وصلت إلى حصة توليد الدروس. راجع الباقة أو موعد التجديد.','Lesson generation allowance reached. Check your plan or reset time.'):detail||word('تعذّر تجهيز الدرس. حاول مجددًا.','Could not prepare the lesson. Try again.'))
   }
   const today=await response.json() as {plan_id:number}
   const journeyResponse=await apiFetch('/api/study-plan/learning-path',{signal:abort.signal})
   if(!journeyResponse.ok)throw new Error(word('تعذّر التحقق من الدرس المتاح. حاول مجددًا.','Could not verify lesson availability. Try again.'))
   const journey=await journeyResponse.json() as Journey
   if(journey.plan_id!==today.plan_id)throw new Error(word('تغيّرت الخطة. أغلق الوحدة وحدّث المسار.','The plan changed. Close this unit and refresh the path.'))
   const selected=journey.sections.flatMap(s=>s.units).find(u=>u.id===unit.id)
   const ready=selected?.lessons.find(l=>!l.is_completed&&l.available&&Number.isInteger(l.id)&&l.id>0)
   if(!ready)throw new Error(word('لم يُجهّز درس متاح لهذه الوحدة. قد يكون التوليد فشل أو يلزم إكمال وحدة سابقة؛ أعد المحاولة أو راجع المسار.','No available lesson was prepared for this unit. Generation may have failed or an earlier unit may need completion. Retry or review your path.'))
   if(alive.current&&!abort.signal.aborted)onStartLesson(ready.id)
  }catch(err){if(alive.current&&!abort.signal.aborted)setError(err instanceof Error?err.message:common('error'))}
  finally{lock.current=false;if(alive.current){setPreparing(false);controller.current=null}}
 }
 return <div className="learning-unit-overlay" onMouseDown={e=>{if(e.target===e.currentTarget)onClose()}}>
  <div className="learning-unit-drawer unit-adventure" ref={ref} tabIndex={-1} role="dialog" aria-modal="true" aria-labelledby={titleId} dir={rtl?'rtl':'ltr'}>
   <header className="learning-unit-header"><span className="unit-adventure-emblem" aria-hidden="true"><BookOpen size={25}/></span><div><small>{unit.level} · {t('unitLabel')}</small><h2 id={titleId} dir="auto">{unit.title}</h2></div><button type="button" className="learning-unit-close" onClick={onClose} aria-label={common('close')}><X size={20}/></button></header>
   <section className="unit-adventure-summary"><div><strong>{completed}/{lessons.length}</strong><span>{t('lessonsHeader',{count:lessons.length})}</span></div><div className="learning-unit-track" role="progressbar" aria-label={t('lessonsHeader',{count:lessons.length})} aria-valuemin={0} aria-valuemax={100} aria-valuenow={progress}><span style={{width:`${progress}%`}}/></div></section>
   <div className="learning-unit-scroll">
    {unit.grammar_points.length>0&&<details className="learning-unit-grammar"><summary>{t('grammarCovered')}</summary><div>{unit.grammar_points.map(point=><span key={point} dir="auto">{point}</span>)}</div></details>}
    {!lessons.length?<p className="learning-unit-empty">{t('noLessons')}</p>:<ol className="unit-adventure-trail">{lessons.map((lesson,index)=>{
     const actionable=lesson.id!==null&&Boolean(lesson.action),current=lesson===nextLesson,state=lesson.completed?'done':current?'current':actionable?'available':'planned'
     const Icon=lesson.completed?Check:current?Play:lesson.lesson_type==='listening'?Headphones:lesson.lesson_type==='writing'?PenLine:lesson.lesson_type==='conversation'?MessageCircle:BookOpen
     return <li key={`${lesson.week}:${lesson.day}:${index}`} data-state={state}>
      <div className="unit-adventure-step"><button type="button" className="unit-adventure-node" disabled={!actionable||preparing} aria-current={current?'step':undefined} aria-label={`${index+1}. ${lesson.title}`} onClick={()=>{if(lesson.id!==null)onStartLesson(lesson.id)}}>{actionable?<Icon size={24} aria-hidden="true"/>:<Lock size={19} aria-hidden="true"/>}<span>{index+1}</span></button>
      <div className="unit-adventure-lesson"><small>{typeLabel[lesson.lesson_type]??lesson.lesson_type}</small><strong dir="auto">{lesson.title}</strong><p>{t('weekDay',{week:lesson.week,day:lesson.day})}</p>
       {actionable&&<button type="button" className="unit-adventure-lesson-action" disabled={preparing} onClick={()=>{if(lesson.id!==null)onStartLesson(lesson.id)}}>{lesson.action==='review'?t('reviewLesson'):lesson.action==='continue'?t('resume'):common('start')}</button>}
       {!actionable&&<span className="unit-adventure-planned">{word('مخطّط، ليس جاهزًا للبدء بعد','Scheduled, not ready to start yet')}</span>}
      </div></div>
     </li>
    })}</ol>}
   </div>
   <footer className="learning-unit-footer">
    {error&&<p className="unit-adventure-error" role="alert">{error}</p>}
    {preparing&&<p className="unit-adventure-preparing" role="status">{word('جارٍ توليد الدرس والتحقق من إمكانية بدءه…','Generating the lesson and checking availability…')}</p>}
    {(onStartUnit||nextLesson||needsPreparation)&&<button type="button" className="unit-adventure-primary" disabled={preparing} onClick={()=>void start()}>{preparing?<RefreshCw size={17} aria-hidden="true"/>:<Play size={17} aria-hidden="true"/>}{preparing?common('loading'):needsPreparation&&!onStartUnit?word('جهّز الدرس وابدأ التعلّم','Prepare lesson & start learning'):t.has('startLearning')?t('startLearning'):common('start')}</button>}
    <button type="button" className="juba-secondary-button" onClick={onClose}>{common('close')}</button>
   </footer>
  </div>
 </div>
}
