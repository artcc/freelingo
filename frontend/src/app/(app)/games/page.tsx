'use client'

import { useState } from 'react'
import { useLocale } from 'next-intl'
import { useLanguageStore } from '@/store/language'
import { gameLanguageForTargetLanguage, type GameId } from '@/lib/games/persist'
import { EducationalGameSession } from '@/components/games/EducationalGameSession'
import './educational-games.css'

const activities: Array<{id: GameId; icon: string; ar: string; en: string; arDesc: string; enDesc: string}> = [
  {id:'memory',icon:'◈',ar:'ذاكرة الكلمات',en:'Word memory',arDesc:'اقلب البطاقات وتذكّر مكان كل كلمة ومعناها.',enDesc:'Flip cards and remember each word and its meaning.'},
  {id:'matching',icon:'⇄',ar:'وصل المعنى',en:'Meaning match',arDesc:'صل الكلمات بتعريفاتها، وتعلّم من المحاولات الخاطئة.',enDesc:'Connect words with their definitions and learn from missed matches.'},
  {id:'sentence_builder',icon:'▤',ar:'مهندس الجمل',en:'Sentence architect',arDesc:'اختر الكلمات ورتّبها لبناء جملة ثم أرسلها للتصحيح.',enDesc:'Select and reorder word tiles to build a sentence, then submit it for scoring.'},
  {id:'quick_choice',icon:'◎',ar:'صيد المعاني',en:'Meaning hunt',arDesc:'اختر المعنى الصحيح، مع أسئلة تتكيّف مع إجاباتك.',enDesc:'Choose meanings in a round that adapts to your answers.'},
  {id:'spelling',icon:'✎',ar:'تحدي الإملاء',en:'Spelling studio',arDesc:'استرجع الكلمات واكتبها، دون كشف الإجابة مسبقًا.',enDesc:'Recall and type words without seeing the answer first.'},
  {id:'listening_detective',icon:'♪',ar:'محقق الاستماع',en:'Listening detective',arDesc:'شغّل الجملة وحدد الكلمة التي تسمعها.',enDesc:'Play the sentence and identify the word you hear.'},
  {id:'grammar_duel',icon:'≋',ar:'مبارزة القواعد',en:'Grammar duel',arDesc:'اكتشف الصيغة الصحيحة وراجع الخطأ قبل الانتقال.',enDesc:'Find the correct form and revisit mistakes before advancing.'},
  {id:'fill_blank',icon:'□',ar:'الكلمة المفقودة',en:'Missing word',arDesc:'أكمل سياق الجملة بالكلمة المناسبة.',enDesc:'Complete the sentence with the appropriate word.'},
  {id:'word_scramble',icon:'↺',ar:'فكّ الكلمة',en:'Word unscramble',arDesc:'حلّ ترتيب الحروف واسترجع الكلمة الصحيحة.',enDesc:'Solve scrambled letters and retrieve the correct word.'},
  {id:'review_mix',icon:'↻',ar:'إنقاذ الكلمات',en:'Retrieval rescue',arDesc:'راجع عناصر تحتاج الاسترجاع من سجل تعلّمك الفعلي.',enDesc:'Retrieve due items from your real learning history.'},
]

export default function GamesPage() {
  const arabic = useLocale().startsWith('ar')
  const language = useLanguageStore(state => state.activeLanguage)
  const code = language?.code ?? 'en-GB'
  const [game, setGame] = useState<GameId | null>(null)
  const [difficulty, setDifficulty] = useState(1)
  const [round, setRound] = useState(0)
  const activity = activities.find(item => item.id === game)
  return <main className="juba-page-shell educational-games" dir={arabic ? 'rtl' : 'ltr'}>
    <header className="edu-heading"><div><p>{arabic ? 'مختبر اللغة' : 'Language lab'} · <b dir="ltr">{code}</b></p><h1>{arabic ? 'تعلّم باللعب' : 'Learn through play'}</h1><p>{arabic ? 'محتوى من خطتك ومستواك. التصحيح والنقاط من الخادم، وليس من المتصفح.' : 'Content from your plan and level. The server validates answers and awards points.'}</p></div></header>
    {game && activity ? <EducationalGameSession key={`${game}:${code}:${difficulty}:${round}`} gameId={game} language={gameLanguageForTargetLanguage(code)} targetLanguage={code} difficulty={difficulty} arabic={arabic} title={arabic ? activity.ar : activity.en} onExit={() => setGame(null)} onReplay={() => setRound(value => value + 1)} /> : <>
      <section className="edu-level"><label htmlFor="game-difficulty">{arabic ? 'درجة التحدي' : 'Challenge difficulty'}</label><select id="game-difficulty" value={difficulty} onChange={event => setDifficulty(Number(event.target.value))}><option value={1}>{arabic ? 'تدرّب' : 'Practice'}</option><option value={2}>{arabic ? 'تحدّ نفسك' : 'Challenge'}</option><option value={3}>{arabic ? 'تحدٍ متقدم' : 'Advanced challenge'}</option></select><span>{arabic ? 'لا يغيّر مستوى CEFR لخطة التعلم.' : 'Does not change your plan’s CEFR level.'}</span></section>
      <section className="edu-catalog" aria-label={arabic ? 'الألعاب التعليمية' : 'Educational games'}>{activities.map((item, index) => <button key={item.id} className="edu-activity" onClick={() => setGame(item.id)}><span className="edu-number">{String(index + 1).padStart(2,'0')}</span><span className="edu-symbol" aria-hidden="true">{item.icon}</span><span><strong>{arabic ? item.ar : item.en}</strong><small>{arabic ? item.arDesc : item.enDesc}</small></span><span className="edu-play">{arabic ? 'العب' : 'Play'} {arabic ? '←' : '→'}</span></button>)}</section>
      <p className="edu-note">{arabic ? 'تحتاج إلى خطة تعلّم نشطة. لن ننشئ نتائج أو منافسين وهميين عند غياب البيانات.' : 'An active learning plan is required. Missing content is not replaced with fake results or opponents.'}</p>
    </>}
  </main>
}
