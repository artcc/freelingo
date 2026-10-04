'use client'

import {useLocale,useTranslations} from 'next-intl'
import {Check,Lock,Play,Flag,BookOpen,TreePine,Mountain,Star} from 'lucide-react'
import './adventure-path.css'

interface UnitStatus{completed:boolean;active:boolean;locked:boolean;isLevelTest:boolean}
interface Props{title:string;index:number;lessonCount:number;grammarCount:number;competency:number;status:UnitStatus;onClick:()=>void;onStartLesson?:()=>void}

/** A curriculum unit, not a fabricated game level. Unlocks and callbacks are
 * supplied by the existing server-backed plan page without changing progression. */
export default function UnitCard({title,index,lessonCount,grammarCount,competency,status,onClick,onStartLesson}:Props){
 const t=useTranslations('plan'),common=useTranslations('common'),ar=useLocale().startsWith('ar')
 const progress=Math.round(Math.max(0,Math.min(1,Number.isFinite(competency)?competency:0))*100)
 const world=Math.floor(index/6)%3
 const state=status.locked?'locked':status.completed?'completed':status.active?'active':'available'
 const Icon=status.locked?Lock:status.isLevelTest?Flag:status.completed?Check:status.active?Play:BookOpen
 return <article className="juba-adventure-stop" data-position={index%4} data-world={world} data-state={state} data-finale={status.isLevelTest}>
  <svg className="juba-adventure-road" viewBox="0 0 600 210" preserveAspectRatio="none" aria-hidden="true"><path className="road-edge" d="M300 -20 C300 50 510 20 510 105 S300 155 300 230"/><path className="road-fill" d="M300 -20 C300 50 510 20 510 105 S300 155 300 230"/><path className="road-dashes" d="M300 -20 C300 50 510 20 510 105 S300 155 300 230"/></svg>
  {index%6===0&&<span className="juba-adventure-world" aria-hidden="true">{world===0?(ar?'غابة البدايات':'The learning forest'):world===1?(ar?'جسر المعرفة':'Across the river'):(ar?'قمم التعلّم':'Learning peaks')}</span>}
  <div className="juba-adventure-scenery" aria-hidden="true">{world===2?<Mountain/>:<TreePine/>}<span className="scenery-rock"/><span className="scenery-bush"/>{world===1&&<span className="scenery-stream"/>}</div>
  <div className="juba-adventure-station">
   {status.active&&<span className="juba-adventure-current">{common('start')}</span>}
   <button type="button" className="juba-adventure-node" disabled={status.locked} onClick={onClick} aria-label={t('unitAriaLabel',{index:index+1,title})} aria-current={status.active?'step':undefined}>
    <Icon aria-hidden="true" size={30} strokeWidth={3}/><span className="juba-adventure-number">{index+1}</span>
   </button>
   <div className="juba-adventure-label"><h3>{title}</h3><p>{t('nLessons',{count:lessonCount})}{grammarCount>0&&<> · {t('nGrammar',{count:grammarCount})}</>}</p>
    {!status.locked&&<div className="juba-adventure-mastery" role="progressbar" aria-label={title} aria-valuemin={0} aria-valuemax={100} aria-valuenow={progress}><span style={{width:`${progress}%`}}/></div>}
    <span className="juba-adventure-status">{status.locked?<><Lock size={12} aria-hidden="true"/>{ar?'تُفتح وفق تقدّمك':'Unlocks with your progress'}</>:status.completed?<><Star size={12} aria-hidden="true"/>{t('completed')} · {progress}%</>:status.isLevelTest?t('levelTestLabel'):`${progress}%`}</span>
    {status.active&&onStartLesson&&<button type="button" className="juba-adventure-start" onClick={onStartLesson}>{common('start')} <Play size={13} aria-hidden="true"/></button>}
   </div>
  </div>
 </article>
}
