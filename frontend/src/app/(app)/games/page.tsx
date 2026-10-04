'use client'

import {useState} from 'react'
import {useLocale} from 'next-intl'
import {useLanguageStore} from '@/store/language'
import {gameLanguageForTargetLanguage,type GameId} from '@/lib/games/persist'
import {EducationalGameSession} from '@/components/games/EducationalGameSession'
import './educational-games.css'
import './games-vivid.css'

type GameFormat='recall'|'build'|'listen'|'review'
type Activity={id:GameId;icon:string;ar:string;en:string;arDesc:string;enDesc:string;color:string;format:GameFormat;arMechanic:string;enMechanic:string}
const activities:Activity[]=[
 {id:'memory',icon:'◈',ar:'ذاكرة الكلمات',en:'Word memory',arDesc:'اربط الكلمة بمعناها قبل نفاد الحركات.',enDesc:'Pair each word with its meaning before moves run out.',color:'mint',format:'recall',arMechanic:'استرجاع بصري',enMechanic:'Visual recall'},
 {id:'matching',icon:'⇄',ar:'وصل المعنى',en:'Meaning match',arDesc:'اختر كلمة وتعريفها، وتعلّم من الخطأ فورًا.',enDesc:'Pair a word with its definition and learn from each miss.',color:'sky',format:'recall',arMechanic:'مطابقة دلالية',enMechanic:'Semantic matching'},
 {id:'sentence_builder',icon:'▤',ar:'مهندس الجمل',en:'Sentence architect',arDesc:'رتّب الكلمات لبناء جملة صحيحة ثم احفظ نتيجتك.',enDesc:'Arrange tiles into a correct sentence and save your result.',color:'sun',format:'build',arMechanic:'بناء جملة',enMechanic:'Sentence construction'},
 {id:'quick_choice',icon:'◎',ar:'صيد المعاني',en:'Meaning hunt',arDesc:'اختر المعنى الصحيح قبل انتهاء الوقت.',enDesc:'Choose the correct meaning before time runs out.',color:'violet',format:'recall',arMechanic:'استدعاء سريع',enMechanic:'Rapid retrieval'},
 {id:'spelling',icon:'✎',ar:'تحدي الإملاء',en:'Spelling studio',arDesc:'كوّن الكلمة من حروفها دون كشف الحل.',enDesc:'Build the word from its letters without seeing the answer.',color:'coral',format:'build',arMechanic:'إنتاج كتابي',enMechanic:'Written production'},
 {id:'listening_detective',icon:'♪',ar:'محقق الاستماع',en:'Listening detective',arDesc:'استمع إلى مثال حقيقي وحدد الكلمة التي سمعتها.',enDesc:'Listen to an authored example and identify the word.',color:'blue',format:'listen',arMechanic:'تمييز سمعي',enMechanic:'Auditory recognition'},
 {id:'grammar_duel',icon:'≋',ar:'مبارزة القواعد',en:'Grammar duel',arDesc:'اختر الصيغة الصحيحة من أخطاء القواعد الفعلية.',enDesc:'Choose the correct form from authored grammar mistakes.',color:'lime',format:'recall',arMechanic:'تصحيح نحوي',enMechanic:'Grammar correction'},
 {id:'fill_blank',icon:'□',ar:'الكلمة المفقودة',en:'Missing word',arDesc:'أكمل السياق بالكلمة المناسبة من منهجك.',enDesc:'Complete the context with the right curriculum word.',color:'peach',format:'build',arMechanic:'إنتاج من السياق',enMechanic:'Context production'},
 {id:'word_scramble',icon:'↺',ar:'فكّ الكلمة',en:'Word unscramble',arDesc:'أعد ترتيب الحروف للوصول إلى الكلمة الصحيحة.',enDesc:'Reorder the letters to retrieve the target word.',color:'lavender',format:'build',arMechanic:'استرجاع هجائي',enMechanic:'Spelling retrieval'},
 {id:'review_mix',icon:'↻',ar:'إنقاذ الكلمات',en:'Retrieval rescue',arDesc:'راجع عناصر ضعيفة من سجل تعلّمك الحقيقي.',enDesc:'Review weak items from your real learning history.',color:'green',format:'review',arMechanic:'مراجعة متكيفة',enMechanic:'Adaptive review'},
]
const groups:[GameFormat,string,string][]=[['recall','استرجاع وتذكّر','Recall & remember'],['build','ابنِ وأنتج','Build & produce'],['listen','استمع وصحّح','Listen & correct'],['review','راجع بذكاء','Review intelligently']]
export default function GamesPage(){
 const arabic=useLocale().startsWith('ar'),language=useLanguageStore(state=>state.activeLanguage),code=language?.code??'en-GB'
 const [game,setGame]=useState<GameId|null>(null),[difficulty,setDifficulty]=useState(1),[round,setRound]=useState(0)
 const activity=activities.find(item=>item.id===game)
 return <main className="juba-page-shell educational-games" dir={arabic?'rtl':'ltr'}>
  <header className="edu-heading"><div><span className="edu-kicker">{arabic?'مختبر JUBA للّغة':'JUBA LANGUAGE LAB'} · <b dir="ltr">{code}</b></span><h1>{arabic?'تعلّم باللعب، وتذكّر أكثر':'Play your way to fluency'}</h1><p>{arabic?'كل لعبة لها ميكانيكية تعليمية واضحة، ومحتواها من منهجك ومستواك.':'Every game has a real learning mechanic, grounded in your curriculum and level.'}</p></div><span className="edu-orbit" aria-hidden="true">✦</span></header>
  {game&&activity?<EducationalGameSession key={`${game}:${code}:${difficulty}:${round}`} gameId={game} language={gameLanguageForTargetLanguage(code)} targetLanguage={code} difficulty={difficulty} arabic={arabic} title={arabic?activity.ar:activity.en} mechanic={arabic?activity.arMechanic:activity.enMechanic} format={activity.format} onExit={()=>setGame(null)} onReplay={()=>setRound(value=>value+1)}/>:<>
   <section className="edu-level"><div><strong>{arabic?'درجة التحدي':'Challenge difficulty'}</strong><span>{arabic?'تغيّر عمق الجولة، لا مستوى CEFR.':'Changes round depth, not your CEFR level.'}</span></div><select id="game-difficulty" value={difficulty} onChange={event=>setDifficulty(Number(event.target.value))}><option value={1}>{arabic?'تدرّب':'Practice'}</option><option value={2}>{arabic?'تحدّ نفسك':'Challenge'}</option><option value={3}>{arabic?'تحدٍ متقدم':'Advanced challenge'}</option></select></section>
   {groups.map(([format,arTitle,enTitle])=><section className="edu-game-group" key={format} aria-labelledby={`games-${format}`}><header><h2 id={`games-${format}`}>{arabic?arTitle:enTitle}</h2><span>{activities.filter(item=>item.format===format).length}</span></header><div className="edu-catalog">{activities.filter(item=>item.format===format).map((item,index)=><button key={item.id} className={`edu-activity edu-${item.color}`} onClick={()=>setGame(item.id)}><span className="edu-number">{String(index+1).padStart(2,'0')}</span><span className="edu-symbol" aria-hidden="true">{item.icon}</span><span><strong>{arabic?item.ar:item.en}</strong><small>{arabic?item.arDesc:item.enDesc}</small><em>{arabic?item.arMechanic:item.enMechanic}</em></span><span className="edu-play">{arabic?'العب':'Play'} <b aria-hidden="true">{arabic?'←':'→'}</b></span></button>)}</div></section>)}
   <p className="edu-note">{arabic?'التصحيح والنقاط وحفظ المراجعة يتحقق منها الخادم. لا توجد ألعاب شكلية أو نتائج وهمية.':'Answers, scoring and review history are validated by the server. No placeholder games or fake results.'}</p>
  </>}
 </main>
}
