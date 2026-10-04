'use client'

import {useState} from 'react'
import {useLocale} from 'next-intl'
import {useLanguageStore} from '@/store/language'
import {gameLanguageForTargetLanguage,type GameId} from '@/lib/games/persist'
import {EducationalGameSession} from '@/components/games/EducationalGameSession'
import './educational-games.css'

const activities:Array<{id:GameId;icon:string;ar:string;en:string;arDesc:string;enDesc:string;color:string}>=[
 {id:'memory',icon:'◈',ar:'ذاكرة الكلمات',en:'Word memory',arDesc:'اقلب البطاقات وتذكّر مكان كل كلمة ومعناها.',enDesc:'Flip cards and remember each word and its meaning.',color:'mint'},
 {id:'matching',icon:'⇄',ar:'وصل المعنى',en:'Meaning match',arDesc:'صل الكلمات بتعريفاتها، وتعلّم من المحاولات الخاطئة.',enDesc:'Connect words with their definitions and learn from missed matches.',color:'sky'},
 {id:'sentence_builder',icon:'▤',ar:'مهندس الجمل',en:'Sentence architect',arDesc:'رتّب الكلمات لبناء جملة ثم أرسلها للتصحيح.',enDesc:'Arrange tiles to build a sentence, then submit it for scoring.',color:'sun'},
 {id:'quick_choice',icon:'◎',ar:'صيد المعاني',en:'Meaning hunt',arDesc:'اختر المعنى الصحيح، مع أسئلة تتكيّف مع إجاباتك.',enDesc:'Choose meanings in a round that adapts to your answers.',color:'violet'},
 {id:'spelling',icon:'✎',ar:'تحدي الإملاء',en:'Spelling studio',arDesc:'استرجع الكلمات واكتبها، دون كشف الإجابة مسبقًا.',en:'Recall and type words without seeing the answer first.',enDesc:'Recall and type words without seeing the answer first.',color:'coral'},
 {id:'listening_detective',icon:'♪',ar:'محقق الاستماع',en:'Listening detective',arDesc:'شغّل الجملة وحدد الكلمة التي تسمعها.',enDesc:'Play the sentence and identify the word you hear.',color:'blue'},
 {id:'grammar_duel',icon:'≋',ar:'مبارزة القواعد',en:'Grammar duel',arDesc:'اكتشف الصيغة الصحيحة وراجع الخطأ قبل الانتقال.',enDesc:'Find the correct form and revisit mistakes before advancing.',color:'lime'},
 {id:'fill_blank',icon:'□',ar:'الكلمة المفقودة',en:'Missing word',arDesc:'أكمل سياق الجملة بالكلمة المناسبة.',enDesc:'Complete the sentence with the appropriate word.',color:'peach'},
 {id:'word_scramble',icon:'↺',ar:'فكّ الكلمة',en:'Word unscramble',arDesc:'حلّ ترتيب الحروف واسترجع الكلمة الصحيحة.',enDesc:'Solve scrambled letters and retrieve the correct word.',color:'lavender'},
 {id:'review_mix',icon:'↻',ar:'إنقاذ الكلمات',en:'Retrieval rescue',arDesc:'راجع عناصر تحتاج الاسترجاع من سجل تعلّمك الفعلي.',enDesc:'Retrieve due items from your real learning history.',color:'green'},
]

export default function GamesPage(){
 const arabic=useLocale().startsWith('ar'),language=useLanguageStore(state=>state.activeLanguage),code=language?.code??'en-GB'
 const [game,setGame]=useState<GameId|null>(null),[difficulty,setDifficulty]=useState(1),[round,setRound]=useState(0)
 const activity=activities.find(item=>item.id===game)
 return <main className="juba-page-shell educational-games" dir={arabic?'rtl':'ltr'}>
  <header className="edu-heading"><div><span className="edu-kicker">{arabic?'مختبر JUBA للّغة':'JUBA LANGUAGE LAB'} · <b dir="ltr">{code}</b></span><h1>{arabic?'تعلّم باللعب، وتذكّر أكثر':'Play your way to fluency'}</h1><p>{arabic?'كل جولة تدريب قصيرة مرتبطة بخطتك ومستواك.':'Short practice rounds connected to your plan and level.'}</p></div><span className="edu-orbit" aria-hidden="true">✦</span></header>
  {game&&activity?<EducationalGameSession key={`${game}:${code}:${difficulty}:${round}`} gameId={game} language={gameLanguageForTargetLanguage(code)} targetLanguage={code} difficulty={difficulty} arabic={arabic} title={arabic?activity.ar:activity.en} onExit={()=>setGame(null)} onReplay={()=>setRound(value=>value+1)}/>:<>
   <section className="edu-level"><div><strong>{arabic?'درجة التحدي':'Challenge difficulty'}</strong><span>{arabic?'اختر الإيقاع المناسب لك.':'Pick the pace that fits you.'}</span></div><select id="game-difficulty" value={difficulty} onChange={event=>setDifficulty(Number(event.target.value))}><option value={1}>{arabic?'تدرّب':'Practice'}</option><option value={2}>{arabic?'تحدّ نفسك':'Challenge'}</option><option value={3}>{arabic?'تحدٍ متقدم':'Advanced challenge'}</option></select></section>
   <section className="edu-catalog" aria-label={arabic?'الألعاب التعليمية':'Educational games'}>{activities.map((item,index)=><button key={item.id} className={`edu-activity edu-${item.color}`} onClick={()=>setGame(item.id)}><span className="edu-number">{String(index+1).padStart(2,'0')}</span><span className="edu-symbol" aria-hidden="true">{item.icon}</span><span><strong>{arabic?item.ar:item.en}</strong><small>{arabic?item.arDesc:item.enDesc}</small></span><span className="edu-play">{arabic?'العب':'Play'} <b aria-hidden="true">{arabic?'←':'→'}</b></span></button>)}</section>
   <p className="edu-note">{arabic?'النقاط والتصحيح يتحقق منهما الخادم. لا نعرض نتائج أو منافسين وهميين.':'Scores and answers are validated by the server. No fake results or opponents.'}</p>
  </>}
 </main>
}
