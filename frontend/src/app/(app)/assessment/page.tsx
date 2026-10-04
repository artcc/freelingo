'use client'

import { useEffect, useRef, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useLocale, useTranslations } from 'next-intl'
import { ClipboardCheck, Mic, ChevronLeft, ChevronRight } from 'lucide-react'
import { apiFetch } from '@/lib/api'
import { useLanguageStore } from '@/store/language'
import { isSubscribed, useAuthStore } from '@/store/auth'
import { useConfigStore } from '@/store/config'
import BeginnerGate from '@/components/assessment/BeginnerGate'
import AdaptiveQuizCard from '@/components/assessment/AdaptiveQuizCard'
import DurationSelector, { DURATION_OPTIONS, type DurationOption } from '@/components/assessment/DurationSelector'
import { type AssessmentQuestion, type CEFRLevel } from '@/data/types'
import { CEFR_LEVELS } from '@/data/curriculum'
import { ConfirmDialog } from '@/components/ui/confirm-dialog'
import { PageLoading } from '@/components/ui/page-loading'
import { resolveAssessmentTransition } from '@/components/assessment/assessment-transition'
import '../resource-reference.css'

interface AnswerRecord{question_id:string;skill:string;difficulty:string;correct:boolean}
interface AssessmentResult{cefr_level:string;score:number;skill_profile:Record<string,number>;strengths:string[];weaknesses:string[]}
interface ExistingPlan{cefr_level:string;created_at:string}
interface VoiceTrialOffer{available:boolean;token?:string;duration_seconds?:number}
interface AssessmentCompleteResponse{plan_id:number;cefr_level:string;voice_trial?:VoiceTrialOffer}
type FlowStep='checking'|'existing'|'beginner-gate'|'quiz'|'result'|'duration'|'voice-trial-offer'
const MAX_QUESTIONS=15
const START_LEVEL:CEFRLevel='A2'
function adjustLevel(current:CEFRLevel,direction:'up'|'down'):CEFRLevel{const index=CEFR_LEVELS.indexOf(current);if(direction==='up'&&index<CEFR_LEVELS.length-1)return CEFR_LEVELS[index+1];if(direction==='down'&&index>0)return CEFR_LEVELS[index-1];return current}
export default function AssessmentPage(){
  const t=useTranslations('assessment')
  const tCommon=useTranslations('common')
  const locale=useLocale()
  const rtl=locale==='ar'
  const router=useRouter()
  const activeLanguage=useLanguageStore(s=>s.activeLanguage)
  const user=useAuthStore(s=>s.user)
  const stripeEnabled=useConfigStore(s=>s.stripeEnabled)
  const configLoaded=useConfigStore(s=>s.loaded)
  const loadConfig=useConfigStore(s=>s.load)
  const [step,setStep]=useState<FlowStep>('checking')
  const [existingPlan,setExistingPlan]=useState<ExistingPlan|null>(null)
  const [error,setError]=useState('')
  const [bank,setBank]=useState<AssessmentQuestion[]>([])
  const [currentQuestion,setCurrentQuestion]=useState<AssessmentQuestion|null>(null)
  const [questionNumber,setQuestionNumber]=useState(0)
  const [answers,setAnswers]=useState<AnswerRecord[]>([])
  const answersRef=useRef<AnswerRecord[]>([])
  const usedIds=useRef(new Set<string>())
  const answeredIds=useRef(new Set<string>())
  const evaluationLock=useRef(false)
  // Server-side grading session: the bank no longer carries answers, so every
  // choice is graded by POST /api/assessment/bank/answer.
  const gradingSessionId=useRef<string|null>(null)
  const answerPending=useRef(false)
  const sessionVersion=useRef(0)
  const [currentLevel,setCurrentLevel]=useState<CEFRLevel>(START_LEVEL)
  const [correctStreak,setCorrectStreak]=useState(0)
  const [wrongStreak,setWrongStreak]=useState(0)
  const [result,setResult]=useState<AssessmentResult|null>(null)
  const [selectedLevel,setSelectedLevel]=useState<CEFRLevel>('A1')
  const [evaluating,setEvaluating]=useState(false)
  const [durationOption,setDurationOption]=useState<DurationOption>(DURATION_OPTIONS[2])
  const [selectedGoals,setSelectedGoals]=useState<string[]>(['grammar','vocabulary'])
  const [submitting,setSubmitting]=useState(false)
  const [trialLoading,setTrialLoading]=useState(false)
  const [createdPlanId,setCreatedPlanId]=useState<number|null>(null)
  const [voiceTrial,setVoiceTrial]=useState<VoiceTrialOffer|null>(null)
  const [showStartWarning,setShowStartWarning]=useState(false)
  useEffect(()=>{void loadConfig()},[loadConfig])
  useEffect(()=>{
    let cancelled=false
    sessionVersion.current+=1
    answersRef.current=[];usedIds.current.clear();answeredIds.current.clear()
    setAnswers([]);setCurrentQuestion(null);setBank([]);setExistingPlan(null);setResult(null);setVoiceTrial(null);setError('');setShowStartWarning(false);setStep('checking')
    async function check(){
      try{
        const lang=activeLanguage?.code??'en-GB'
        const [planRes,bankRes]=await Promise.all([apiFetch('/api/study-plan/current'),apiFetch(`/api/assessment/bank?language=${lang}`)])
        const bankData=bankRes.ok?await bankRes.json() as {questions:AssessmentQuestion[];session_id:string}:null
        const plan=planRes.ok?await planRes.json():null
        if(cancelled)return
        if(bankData){setBank(bankData.questions);gradingSessionId.current=bankData.session_id}
        if(plan?.cefr_level){setExistingPlan(plan as ExistingPlan);setStep('existing');return}
      }catch{/* Beginner setup remains available without an existing plan. */}
      if(!cancelled)setStep('beginner-gate')
    }
    void check();return ()=>{cancelled=true;sessionVersion.current+=1}
  },[activeLanguage?.code])
  const canOfferVoiceTrial=configLoaded&&stripeEnabled&&user!==null&&!isSubscribed(user,stripeEnabled)&&!user.assessment_voice_trial_used
  async function startQuiz(){
    if(evaluationLock.current){setError(tCommon('error'));return}
    // Every attempt gets a fresh grading session so retakes start from zero.
    let questions=bank
    try{
      const res=await apiFetch(`/api/assessment/bank?language=${activeLanguage?.code??'en-GB'}`)
      if(!res.ok)throw new Error(`Error ${res.status}`)
      const data=await res.json() as {questions:AssessmentQuestion[];session_id:string}
      questions=data.questions;gradingSessionId.current=data.session_id;setBank(questions)
    }catch{setError(tCommon('error'));return}
    if(!questions.length){setError(tCommon('error'));return}
    const available=questions.filter(question=>question.difficulty===START_LEVEL)
    if(!available.length){setError(tCommon('error'));return}
    const question=available[Math.floor(Math.random()*available.length)]
    sessionVersion.current+=1;answersRef.current=[];usedIds.current.clear();answeredIds.current.clear()
    setError('');setAnswers([]);setCurrentLevel(START_LEVEL);setCorrectStreak(0);setWrongStreak(0)
    usedIds.current.add(question.id);setCurrentQuestion(question);setQuestionNumber(1);setStep('quiz')
  }
  async function handleAnswer(chosen:string){
    if(!currentQuestion||evaluationLock.current||answerPending.current||answeredIds.current.has(currentQuestion.id))return
    if(!currentQuestion.options.includes(chosen)||!gradingSessionId.current)return
    const question=currentQuestion
    const version=sessionVersion.current
    answeredIds.current.add(question.id);answerPending.current=true
    let correct=false
    try{
      const res=await apiFetch('/api/assessment/bank/answer',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({session_id:gradingSessionId.current,question_id:question.id,selected:chosen})})
      if(!res.ok)throw new Error(`Error ${res.status}`)
      correct=(await res.json() as {correct:boolean}).correct===true
    }catch{answeredIds.current.delete(question.id);if(version===sessionVersion.current)setError(tCommon('error'));return}
    finally{answerPending.current=false}
    if(version!==sessionVersion.current)return
    setError('')
    const record:AnswerRecord={question_id:question.id,skill:question.skill,difficulty:question.difficulty,correct}
    const nextAnswers=[...answersRef.current,record]
    answersRef.current=nextAnswers;setAnswers(nextAnswers)
    let nextCorrect=correctStreak;let nextWrong=wrongStreak;let nextLevel=currentLevel
    if(correct){nextCorrect+=1;nextWrong=0;if(nextCorrect>=2){nextLevel=adjustLevel(currentLevel,'up');nextCorrect=0}}
    else{nextWrong+=1;nextCorrect=0;if(nextWrong>=2){nextLevel=adjustLevel(currentLevel,'down');nextWrong=0}}
    setCorrectStreak(nextCorrect);setWrongStreak(nextWrong);setCurrentLevel(nextLevel)
    const transition=resolveAssessmentTransition(bank,usedIds.current,nextLevel,nextAnswers,MAX_QUESTIONS)
    if(transition.kind==='evaluate'){void evaluateQuiz();return}
    usedIds.current.add(transition.question.id);setCurrentQuestion(transition.question);setQuestionNumber(nextAnswers.length+1)
  }
  async function evaluateQuiz(){
    if(evaluationLock.current||!gradingSessionId.current)return
    evaluationLock.current=true
    const version=sessionVersion.current
    setEvaluating(true);setCurrentQuestion(null);setError('')
    try{
      const res=await apiFetch('/api/assessment/evaluate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({session_id:gradingSessionId.current})})
      if(!res.ok){const data=await res.json().catch(()=>({}));throw new Error((data as {detail?:string}).detail??`Error ${res.status}`)}
      const data=await res.json() as AssessmentResult
      if(version!==sessionVersion.current)return
      setResult(data);setSelectedLevel(data.cefr_level as CEFRLevel);setStep('result')
    }catch(err){if(version===sessionVersion.current){const msg=err instanceof Error?err.message:'';setError(msg==='ai_service_error'||msg==='ai_service_unavailable'?tCommon('error'):msg||tCommon('error'))}}finally{evaluationLock.current=false;if(version===sessionVersion.current)setEvaluating(false)}
  }
  async function handleComplete(){
    if(!result||submitting)return
    setSubmitting(true);setError('')
    try{
      const res=await apiFetch('/api/assessment/complete',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({cefr_level:selectedLevel,skill_profile:result.skill_profile,strengths:result.strengths,weaknesses:result.weaknesses,duration_weeks:durationOption.weeks,days_per_week:durationOption.daysPerWeek,goals:selectedGoals,target_language:activeLanguage?.code??undefined})})
      if(!res.ok){const data=await res.json().catch(()=>({}));throw new Error((data as {detail?:string}).detail??`Error ${res.status}`)}
      const data=await res.json() as AssessmentCompleteResponse;setCreatedPlanId(data.plan_id)
      if(data.voice_trial?.available&&data.voice_trial.token){setVoiceTrial(data.voice_trial);setStep('voice-trial-offer');setSubmitting(false);return}
      router.push('/plan')
    }catch(err){const msg=err instanceof Error?err.message:'';setError(msg==='ai_service_error'||msg==='ai_service_unavailable'?tCommon('error'):msg||tCommon('error'));setSubmitting(false)}
  }
  function startVoiceTrial(){if(!voiceTrial?.token)return;sessionStorage.setItem('assessment_voice_trial',JSON.stringify({token:voiceTrial.token,durationSeconds:voiceTrial.duration_seconds??300,cefrLevel:selectedLevel,planId:createdPlanId,targetLanguage:activeLanguage?.code}));router.push('/conversation')}
  async function requestVoiceTrial(){
    if(!existingPlan||trialLoading)return
    setTrialLoading(true);setError('')
    try{
      const res=await apiFetch('/api/assessment/voice-trial',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({target_language:activeLanguage?.code})})
      if(!res.ok){const data=await res.json().catch(()=>({}));throw new Error((data as {detail?:string}).detail??`Error ${res.status}`)}
      const data=await res.json() as AssessmentCompleteResponse
      if(data.voice_trial?.available&&data.voice_trial.token){setCreatedPlanId(data.plan_id);setSelectedLevel(data.cefr_level as CEFRLevel);setVoiceTrial(data.voice_trial);setStep('voice-trial-offer');return}
      setError(tCommon('error'))
    }catch(err){setError(err instanceof Error?err.message:tCommon('error'))}finally{setTrialLoading(false)}
  }
  const Forward=rtl?ChevronLeft:ChevronRight
  const Back=rtl?ChevronRight:ChevronLeft
  const panel='reference-resource-panel'
  const body='reference-resource-body'
  const actions='learning-assessment-actions'
  return <div className="juba-page-shell reference-resource-page learning-assessment" dir={rtl?'rtl':'ltr'}>
    <style>{`
      .juba-app-shell .learning-assessment-grid{display:grid;grid-template-columns:minmax(0,1fr) 264px;gap:24px;align-items:start;}
      .juba-app-shell .learning-assessment-grid>div{display:flex;flex-direction:column;gap:24px;min-width:0;}
      .juba-app-shell .learning-assessment-level{display:flex;align-items:center;gap:16px;flex-wrap:wrap;padding:16px;}
      .juba-app-shell .learning-assessment-level>strong{display:grid;place-items:center;width:64px;height:72px;border-radius:6px;background:var(--juba-green-soft);color:var(--juba-green-dark);font-size:28px;font-weight:650;}
      .juba-app-shell .learning-assessment-level p{margin:4px 0;font-size:13px;line-height:1.7;color:var(--juba-muted);}
      .juba-app-shell .learning-assessment-actions{display:flex;align-items:center;gap:8px;flex-wrap:wrap;padding:16px;border-block-start:1px solid var(--juba-border);}
      .juba-app-shell .learning-assessment-actions button{padding-inline:16px;}
      .juba-app-shell .learning-assessment-score{font-size:28px;font-weight:650;font-variant-numeric:tabular-nums;color:var(--juba-ink);margin:0;}
      .juba-app-shell .learning-assessment-picker{display:flex;flex-wrap:wrap;gap:8px;}
      .juba-app-shell .learning-assessment-picker button{min-height:44px;padding:8px 12px;border:1px solid var(--juba-border);border-radius:5px;background:var(--juba-card);color:var(--juba-muted);font-size:13px;}
      .juba-app-shell .learning-assessment-picker button[aria-pressed="true"]{background:var(--juba-green-soft);color:var(--juba-green-dark);border-color:var(--juba-green);}
      .juba-app-shell .learning-assessment-tags{display:flex;flex-wrap:wrap;gap:8px;list-style:none;padding:16px;margin:0;}
      .juba-app-shell .learning-assessment-tags li{padding:6px 10px;border-radius:4px;font-size:12px;background:var(--juba-green-soft);color:var(--juba-green-dark);}
      .juba-app-shell .learning-assessment-error{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;padding:12px 16px;border:1px solid var(--duo-red);border-radius:6px;color:var(--duo-red);font-size:13px;}
      .juba-app-shell .learning-assessment-error button{padding-inline:12px;}
      @media(max-width:1000px){.juba-app-shell .learning-assessment-grid{grid-template-columns:1fr;}}
      @media(max-width:640px){.juba-app-shell .learning-assessment-grid,.juba-app-shell .learning-assessment-grid>div{gap:16px;}}
    `}</style>
    <header className="reference-resource-heading"><ClipboardCheck size={40} aria-hidden="true"/><div><h1>{t('title')}</h1><p>{step==='result'?t('resultStep'):step==='voice-trial-offer'?t('voiceTrialLabel'):t('cefrLevel')}</p></div></header>
    {error&&<div className="learning-assessment-error" role="alert"><span>{error}</span>{step==='quiz'&&!currentQuestion&&!evaluating&&<button className="juba-secondary-button" onClick={()=>void evaluateQuiz()}>{tCommon('retry')}</button>}</div>}
    {(step==='checking'||(step==='quiz'&&(evaluating||!currentQuestion)&&!error))&&<PageLoading label={evaluating?t('evaluating'):tCommon('loading')}/>}
    {step==='existing'&&existingPlan&&<div className="learning-assessment-grid"><div><section className={panel}><header className="reference-resource-panel-head"><h2>{t('currentLevel')}</h2></header><div className="learning-assessment-level"><strong>{existingPlan.cefr_level}</strong><div><p>{t('assessedOn')}</p><p>{new Date(existingPlan.created_at).toLocaleDateString(locale,{year:'numeric',month:'long',day:'numeric'})}</p></div></div><div className={body}><p>{t('alreadyHasPlan')}</p></div><div className={actions}><button className="juba-secondary-button" onClick={()=>router.push('/dashboard')}><Back size={16}/>{tCommon('backToDashboard')}</button><button className="juba-primary-button" onClick={()=>setStep('beginner-gate')}>{t('retake')}</button></div></section></div>{canOfferVoiceTrial&&<aside className={panel}><header className="reference-resource-panel-head"><h2>{t('voiceTrialTitle')}</h2><Mic size={18}/></header><div className={body}><p>{t('voiceTrialDesc',{minutes:5})}</p></div><div className={actions}><button className="juba-primary-button" onClick={()=>void requestVoiceTrial()} disabled={trialLoading}>{trialLoading?'…':t('voiceTrialStart')}<Forward size={16}/></button></div></aside>}</div>}
    {step==='beginner-gate'&&<><BeginnerGate languageCode={activeLanguage?.iso639??''} onBeginner={()=>{setResult({cefr_level:'A1',score:0,skill_profile:{},strengths:[],weaknesses:[]});setSelectedLevel('A1');setAnswers([]);answersRef.current=[];setStep('duration')}} onHasExperience={()=>setShowStartWarning(true)}/><ConfirmDialog open={showStartWarning} title={t('startWarningTitle')} message={t('startWarningMessage')} confirmLabel={t('startWarningConfirm')} onConfirm={()=>{setShowStartWarning(false);void startQuiz()}} onCancel={()=>setShowStartWarning(false)}/></>}
    {step==='quiz'&&currentQuestion&&<AdaptiveQuizCard question={currentQuestion} questionNumber={questionNumber} totalQuestions={MAX_QUESTIONS} onAnswer={choice=>void handleAnswer(choice)} languageCode={activeLanguage?.code}/>}
    {step==='result'&&result&&<div className="learning-assessment-grid"><div><section className={panel}><header className="reference-resource-panel-head"><h2>{t('cefrLevel')}</h2></header><div className="learning-assessment-level"><strong>{result.cefr_level}</strong><div><p>{t('overrideLevel')}</p><div className="learning-assessment-picker" role="group" aria-label={t('overrideLevel')}>{CEFR_LEVELS.map(level=><button key={level} aria-pressed={selectedLevel===level} onClick={()=>setSelectedLevel(level)}>{level}</button>)}</div></div></div>{selectedLevel!==result.cefr_level&&<div className={body}><p>{t('suggestedLevel',{aiLevel:result.cefr_level,selectedLevel})}</p></div>}<div className={actions}><button className="juba-primary-button" onClick={()=>setStep('duration')}>{t('createPlan')}<Forward size={16}/></button></div></section>{result.strengths.length>0&&<section className={panel}><header className="reference-resource-panel-head"><h2>{t('strengths')}</h2></header><ul className="learning-assessment-tags">{result.strengths.map(item=><li key={item} dir="auto">{item}</li>)}</ul></section>}{result.weaknesses.length>0&&<section className={panel}><header className="reference-resource-panel-head"><h2>{t('needsWork')}</h2></header><ul className="learning-assessment-tags">{result.weaknesses.map(item=><li key={item} dir="auto">{item}</li>)}</ul></section>}</div><aside className={panel}><header className="reference-resource-panel-head"><h2>{tCommon('score')}</h2></header><div className={body}><p className="learning-assessment-score">{Math.round(result.score*100)}%</p></div></aside></div>}
    {step==='duration'&&<DurationSelector selectedWeeks={durationOption.weeks} selectedGoals={selectedGoals} onSelectDuration={setDurationOption} onToggleGoal={goal=>setSelectedGoals(previous=>previous.includes(goal)?previous.filter(item=>item!==goal):[...previous,goal])} onConfirm={handleComplete} onBack={()=>{const beginner=result?.score===0&&result?.cefr_level==='A1'&&answers.length===0;setStep(beginner?'beginner-gate':'result')}} cefr_level={selectedLevel} loading={submitting}/>}
    {step==='voice-trial-offer'&&<section className={panel}><header className="reference-resource-panel-head"><h2>{t('voiceTrialLabel')}</h2><Mic size={20}/></header><div className="learning-assessment-level"><strong>{selectedLevel}</strong><div><p>{t('cefrLevel')}</p><p>{t('voiceTrialTitle')}</p></div></div><div className={body}><p>{t('voiceTrialDesc',{minutes:Math.round((voiceTrial?.duration_seconds??300)/60)})}</p></div><div className={actions}><button className="juba-primary-button" onClick={startVoiceTrial}>{t('voiceTrialStart')}<Forward size={16}/></button><button className="juba-secondary-button" onClick={()=>router.push('/plan')}>{t('voiceTrialSkip')}</button></div></section>}
  </div>
}
