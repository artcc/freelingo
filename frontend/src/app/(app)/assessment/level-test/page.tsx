'use client'

import { useState, useEffect, useCallback, useRef } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { useLocale, useTranslations } from 'next-intl'
import { ClipboardCheck, Check, X, ChevronLeft, ChevronRight, Trophy } from 'lucide-react'
import { apiFetch } from '@/lib/api'
import { ConfirmDialog } from '@/components/ui/confirm-dialog'
import { PageLoading } from '@/components/ui/page-loading'
import '../..//resource-reference.css'

// The server keeps the answer key; it is revealed per question only after grading.
interface LevelTestQuestion{id:string;skill:string;difficulty:string;question:string;options:string[]}
interface LevelTestAnswerResponse{question_id:string;correct:boolean;correct_answer:string;explanation?:string|null}
interface AnswerRecord{question_id:string;skill:string;difficulty:string;correct:boolean}
interface LevelTestResult{score:number;recommendation:'advance'|'extend'|'repeat';next_level:string|null}
interface SkillBreakdown{correct:number;total:number}
type FlowStep='loading'|'quiz'|'submitting'|'result'|'error'
function computeSkillBreakdown(questions:LevelTestQuestion[],answers:AnswerRecord[]):Record<string,SkillBreakdown>{const map:Record<string,SkillBreakdown>={};answers.forEach(answer=>{const question=questions.find(item=>item.id===answer.question_id);if(!question)return;const skill=question.skill;if(!map[skill])map[skill]={correct:0,total:0};map[skill].total+=1;if(answer.correct)map[skill].correct+=1});return map}
export default function LevelTestPage(){
  const t=useTranslations('assessment')
  const tCommon=useTranslations('common')
  const rtl=useLocale()==='ar'
  const router=useRouter()
  const searchParams=useSearchParams()
  const planId=searchParams.get('plan')
  const [startConfirmed,setStartConfirmed]=useState(false)
  const [showStartWarning,setShowStartWarning]=useState(true)
  const [step,setStep]=useState<FlowStep>('loading')
  const [questions,setQuestions]=useState<LevelTestQuestion[]>([])
  const [currentIndex,setCurrentIndex]=useState(0)
  const [answers,setAnswers]=useState<AnswerRecord[]>([])
  const [cefrLevel,setCefrLevel]=useState('')
  const [result,setResult]=useState<LevelTestResult|null>(null)
  const [error,setError]=useState('')
  const [selectedOption,setSelectedOption]=useState<string|null>(null)
  const [answerConfirmed,setAnswerConfirmed]=useState(false)
  const answersRef=useRef<AnswerRecord[]>([])
  const [revealed,setRevealed]=useState<Record<string,string>>({})
  const [grading,setGrading]=useState(false)
  const skillLabels:Record<string,string>={grammar:t('skills.grammar'),vocabulary:t('skills.vocabulary'),reading:t('skills.reading')}
  const loadQuestions=useCallback(async()=>{
    if(!startConfirmed)return
    const planIdNum=Number(planId)
    if(!planId||!Number.isInteger(planIdNum)||planIdNum<=0){setError('Invalid plan ID. Please access the level test from your plan page.');setStep('error');return}
    setStep('loading');setError('')
    try{
      const res=await apiFetch(`/api/assessment/level-test/questions/${planIdNum}`)
      if(!res.ok){const data=await res.json().catch(()=>({}));throw new Error((data as {detail?:string}).detail??`Error ${res.status}`)}
      const data=await res.json() as {plan_id:number;cefr_level:string;questions:LevelTestQuestion[]}
      if(!data.questions?.length)throw new Error('No questions received from the server.')
      answersRef.current=[];setAnswers([]);setRevealed({});setCurrentIndex(0);setSelectedOption(null);setAnswerConfirmed(false)
      setQuestions(data.questions);setCefrLevel(data.cefr_level);setStep('quiz')
    }catch(err){setError(err instanceof Error?err.message:'Failed to load level test.');setStep('error')}
  },[planId,startConfirmed])
  useEffect(()=>{void loadQuestions()},[loadQuestions])
  function handleSelectOption(option:string){if(answerConfirmed)return;setSelectedOption(option)}
  async function handleConfirmAnswer(){
    if(!selectedOption||answerConfirmed||grading)return
    const question=questions[currentIndex]
    setGrading(true);setError('')
    try{
      const res=await apiFetch('/api/assessment/level-test/answer',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({plan_id:Number(planId),question_id:question.id,selected:selectedOption})})
      if(!res.ok){const data=await res.json().catch(()=>({}));throw new Error((data as {detail?:string}).detail??`Error ${res.status}`)}
      const graded=await res.json() as LevelTestAnswerResponse
      setRevealed(previous=>({...previous,[question.id]:graded.correct_answer}))
      setAnswerConfirmed(true)
      const record:AnswerRecord={question_id:question.id,skill:question.skill,difficulty:question.difficulty,correct:graded.correct===true}
      const newAnswers=[...answersRef.current,record];setAnswers(newAnswers);answersRef.current=newAnswers
    }catch(err){setError(err instanceof Error?err.message:tCommon('error'))}finally{setGrading(false)}
  }
  function handleNext(){if(currentIndex+1>=questions.length){void submitTest();return}setCurrentIndex(value=>value+1);setSelectedOption(null);setAnswerConfirmed(false)}
  async function submitTest(){
    setStep('submitting');setError('')
    try{
      const res=await apiFetch('/api/assessment/level-test/submit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({plan_id:Number(planId)})})
      if(!res.ok){const data=await res.json().catch(()=>({}));throw new Error((data as {detail?:string}).detail??`Error ${res.status}`)}
      const data=await res.json() as LevelTestResult;setResult(data);setStep('result')
    }catch(err){setError(err instanceof Error?err.message:'Submission failed.');setStep('error')}
  }
  const q=questions[currentIndex]
  const progress=questions.length?currentIndex/questions.length*100:0
  const breakdown=result?computeSkillBreakdown(questions,answers):{}
  const weakAreas=Object.entries(breakdown).filter(([,value])=>value.total>0&&value.correct/value.total<.6).map(([skill])=>skillLabels[skill]??skill)
  const recommendation=result?({
    advance:{label:rtl?`الانتقال إلى ${result.next_level??'المستوى التالي'}`:`Advance to ${result.next_level??'next level'}`,message:rtl?`أظهرت إتقانًا جيدًا للمستوى ${cefrLevel}. برنامج المستوى ${result.next_level??'التالي'} جاهز.`:`You demonstrated solid ${cefrLevel} mastery. Your ${result.next_level??'next-level'} programme is ready!`,nextAction:result.next_level?'/assessment':'/plan',nextLabel:result.next_level?(rtl?`ابدأ برنامج ${result.next_level}`:`Start ${result.next_level} programme`):(rtl?'انتقل إلى الخطة':'Go to plan')},
    extend:{label:rtl?'تمديد 4 أسابيع':'4-week extension',message:rtl?`المجالات التي تحتاج تقوية: ${weakAreas.join(', ')||'فهم المقروء'}. نوصي بأربعة أسابيع إضافية من الممارسة المركزة.`:`Weak areas detected: ${weakAreas.join(', ')||'Reading Comprehension'}. We recommend 4 extra weeks of focused practice.`,nextAction:'/plan',nextLabel:rtl?'قبول التمديد':'Accept extension'},
    repeat:{label:rtl?`إعادة ${cefrLevel}`:`Repeat ${cefrLevel}`,message:rtl?`النتيجة أقل من 55%. تحتاج عدة كفاءات أساسية في ${cefrLevel} إلى تقوية. تم إعداد خطة جديدة.`:`Score below 55%. Several core ${cefrLevel} competencies need reinforcement. A fresh plan has been prepared.`,nextAction:'/plan',nextLabel:rtl?`ابدأ خطة ${cefrLevel} جديدة`:`Start new ${cefrLevel} plan`},
  })[result.recommendation]:null
  const Forward=rtl?ChevronLeft:ChevronRight
  const Back=rtl?ChevronRight:ChevronLeft
  return <div className="juba-page-shell reference-resource-page reference-level-test" dir={rtl?'rtl':'ltr'}>
    <style>{`
      .juba-app-shell .reference-level-test-progress{height:8px;border-radius:3px;overflow:hidden;background:var(--juba-soft);}
      .juba-app-shell .reference-level-test-progress>span{display:block;height:100%;background:var(--juba-yellow);}
      .juba-app-shell .reference-level-test-question{padding:24px 16px;font-size:18px;line-height:1.7;color:var(--juba-ink);margin:0;overflow-wrap:anywhere;}
      .juba-app-shell .reference-level-test-options{display:flex;flex-direction:column;gap:12px;padding:0 16px 16px;}
      .juba-app-shell .reference-level-test-options button{display:flex;align-items:flex-start;gap:12px;min-height:48px;padding:14px 16px;border:1px solid var(--juba-border);border-radius:5px;background:var(--juba-card);color:var(--juba-ink);font-size:14px;line-height:1.7;text-align:start;}
      .juba-app-shell .reference-level-test-options button[data-selected="true"]{background:var(--juba-green-soft);border-color:var(--juba-green);}
      .juba-app-shell .reference-level-test-options button[data-result="correct"]{border-color:var(--juba-green);color:var(--juba-green-dark);}
      .juba-app-shell .reference-level-test-options button[data-result="incorrect"]{border-color:var(--duo-red);color:var(--duo-red);}
      .juba-app-shell .reference-level-test-options button:disabled{opacity:1;}
      .juba-app-shell .reference-level-test-key{width:24px;height:24px;flex:none;border-radius:4px;background:var(--juba-soft);color:var(--juba-muted);display:grid;place-items:center;font-size:11px;}
      .juba-app-shell .reference-level-test-actions{display:flex;align-items:center;gap:8px;flex-wrap:wrap;padding:16px;border-block-start:1px solid var(--juba-border);}
      .juba-app-shell .reference-level-test-actions button{padding-inline:16px;}
      .juba-app-shell .reference-level-test-feedback{display:flex;align-items:flex-start;gap:8px;margin:0 16px 16px;padding:12px;border:1px solid var(--juba-green);border-radius:5px;font-size:13px;color:var(--juba-green-dark);}
      .juba-app-shell .reference-level-test-feedback[data-correct="false"]{border-color:var(--duo-red);color:var(--duo-red);}
      .juba-app-shell .reference-level-test-feedback>svg{flex:none;}
      .juba-app-shell .reference-level-test-results{display:grid;grid-template-columns:minmax(0,1fr) 264px;gap:24px;align-items:start;}
      .juba-app-shell .reference-level-test-score{padding:16px;}
      .juba-app-shell .reference-level-test-score>strong{display:block;font-size:32px;font-weight:650;margin-block-end:12px;font-variant-numeric:tabular-nums;}
      .juba-app-shell .reference-level-test-score p{font-size:12px;color:var(--juba-muted);margin:8px 0 0;}
      .juba-app-shell .reference-level-test-breakdown{margin:0;padding:16px;display:flex;flex-direction:column;gap:20px;}
      .juba-app-shell .reference-level-test-breakdown>div{display:flex;flex-direction:column;gap:8px;}
      .juba-app-shell .reference-level-test-breakdown dt{font-size:13px;font-weight:600;color:var(--juba-ink);}
      .juba-app-shell .reference-level-test-breakdown dd{margin:0;font-size:12px;color:var(--juba-muted);}
      .juba-app-shell .reference-level-test-breakdown dd>span{display:block;margin-block-end:8px;font-variant-numeric:tabular-nums;}
      .juba-app-shell .reference-level-test-recommendation h3{font-size:18px;font-weight:650;margin:0 0 8px;}
      .juba-app-shell .reference-level-test-recommendation p{font-size:14px;line-height:1.7;color:var(--juba-muted);margin:0;}
      @media(max-width:1000px){.juba-app-shell .reference-level-test-results{grid-template-columns:1fr;}}
      @media(max-width:640px){.juba-app-shell .reference-level-test-results{gap:16px;}}
    `}</style>
    <header className="reference-resource-heading"><ClipboardCheck size={40} aria-hidden="true"/><div><h1>{cefrLevel} {rtl?'اختبار المستوى':'Level test'}</h1><p>{step==='result'?t('resultStep'):t('cefrLevel')}</p></div></header>
    {showStartWarning?<ConfirmDialog open title={t('startWarningTitle')} message={t('startWarningMessageLevelTest')} confirmLabel={t('startWarningConfirm')} onConfirm={()=>{setShowStartWarning(false);setStartConfirmed(true)}} onCancel={()=>router.push('/plan')}/>:step==='loading'||step==='submitting'?<PageLoading label={step==='loading'?t('levelTest.loadingTest'):t('levelTest.submittingTest')}/>:step==='error'?<section className="reference-resource-panel reference-resource-state" role="alert"><p>{error}</p><button className="juba-secondary-button" onClick={()=>router.push('/plan')}><Back size={16}/>{rtl?'العودة إلى الخطة':'Back to plan'}</button><button className="juba-secondary-button" onClick={()=>questions.length&&answersRef.current.length===questions.length?void submitTest():void loadQuestions()}>{tCommon('retry')}</button></section>:step==='result'&&result&&recommendation?<div className="reference-level-test-results"><section className="reference-resource-panel"><header className="reference-resource-panel-head"><h2>{rtl?'تحليل المهارات':'Skill breakdown'}</h2></header><dl className="reference-level-test-breakdown">{Object.entries(breakdown).map(([skill,value])=>{const pct=value.total>0?Math.round(value.correct/value.total*100):0;return <div key={skill}><dt>{skillLabels[skill]??skill}</dt><dd><span>{value.correct}/{value.total} ({pct}%)</span><div className="reference-level-test-progress" role="progressbar" aria-label={skillLabels[skill]??skill} aria-valuemin={0} aria-valuemax={100} aria-valuenow={pct}><span style={{width:pct+'%',background:pct<60?'var(--juba-yellow)':'var(--juba-green)'}}/></div></dd></div>})}</dl><div className="reference-resource-body reference-level-test-recommendation"><h3>{recommendation.label}</h3><p>{recommendation.message}</p></div><div className="reference-level-test-actions"><button className="juba-primary-button" onClick={()=>router.push(recommendation.nextAction)}>{recommendation.nextLabel}<Forward size={16}/></button><button className="juba-secondary-button" onClick={()=>router.push('/plan')}><Back size={16}/>{rtl?'العودة إلى الخطة':'Back to plan'}</button></div></section><aside className="reference-resource-panel"><header className="reference-resource-panel-head"><h2>{tCommon('score')}</h2><Trophy size={18}/></header><div className="reference-level-test-score"><strong>{Math.round(result.score*100)}%</strong><div className="reference-level-test-progress" role="progressbar" aria-label={tCommon('score')} aria-valuemin={0} aria-valuemax={100} aria-valuenow={Math.max(0,Math.min(100,Math.round(result.score*100)))}><span style={{width:Math.max(0,Math.min(100,Math.round(result.score*100)))+'%'}}/></div><p>{answers.filter(answer=>answer.correct).length}/{questions.length} {rtl?'صحيح':'correct'}</p></div></aside></div>:q?<section className="reference-resource-panel"><header className="reference-resource-panel-head"><h2>{skillLabels[q.skill]??q.skill}</h2><span>{q.difficulty} · {currentIndex+1}/{questions.length}</span></header><div className="reference-level-test-progress" role="progressbar" aria-label={t('title')} aria-valuemin={0} aria-valuemax={100} aria-valuenow={Math.round(progress)}><span style={{width:progress+'%'}}/></div><p className="reference-level-test-question" dir="auto">{q.question}</p><div className="reference-level-test-options">{q.options.map((option,index)=><button key={index} disabled={answerConfirmed} data-selected={selectedOption===option} data-result={answerConfirmed?(option===revealed[q.id]?'correct':option===selectedOption?'incorrect':undefined):undefined} onClick={()=>handleSelectOption(option)}><span className="reference-level-test-key" aria-hidden="true">{['A','B','C','D'][index]??String(index+1)}</span><span dir="auto">{option}</span></button>)}</div>{answerConfirmed&&<div className="reference-level-test-feedback" data-correct={answers.at(-1)?.correct} role="status">{answers.at(-1)?.correct?<><Check size={16}/><span>{rtl?'صحيح':'Correct'}</span></>:<><X size={16}/><span>{rtl?'إجابة غير صحيحة. الإجابة الصحيحة:':'Incorrect. Correct answer:'} <bdi>{revealed[q.id]}</bdi></span></>}</div>}{error&&<div className="reference-level-test-feedback" data-correct="false" role="alert"><X size={16}/><span>{error}</span></div>}<div className="reference-level-test-actions">{!answerConfirmed?<button className="juba-primary-button" onClick={()=>void handleConfirmAnswer()} disabled={!selectedOption||grading}>{rtl?'تأكيد الإجابة':'Confirm answer'}</button>:<button className="juba-primary-button" onClick={handleNext}>{currentIndex+1>=questions.length?(rtl?'إرسال الاختبار':'Submit test'):(rtl?'السؤال التالي':'Next question')}<Forward size={16}/></button>}</div></section>:null}
  </div>
}
