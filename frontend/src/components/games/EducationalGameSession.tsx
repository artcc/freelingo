'use client'

import { useEffect, useRef, useState } from 'react'
import { Check, Heart, Target } from 'lucide-react'
import { ArenaRequestError, answerGameSessionQuestion, completeGameSession, moveArena, readArena, startArena, startGameSession, type ArenaMove, type ArenaState, type GameId, type GameLanguage, type GameSessionNextResponse, type GameSessionQuestion, type GameSessionResult, type GameSessionStartResponse } from '@/lib/games/persist'
import { useAuthStore } from '@/store/auth'
import { useProgressStore } from '@/store/progress'
import type { AchievementId } from '@/lib/games/achievements'
import { markLearningProgressUpdated } from '@/lib/learning-progress'
import { submitArenaMove } from '@/lib/games/arena-move-recovery'

type Props = { gameId: GameId; language: GameLanguage; targetLanguage: string; difficulty: number; arabic: boolean; title: string; mechanic?: string; format?: string; onExit: () => void; onReplay: () => void }
const ARCADE = new Set(['quick_choice', 'spelling', 'word_scramble', 'memory', 'matching'])
const tx = (ar: boolean, a: string, e: string) => ar ? a : e
function saveResult(result: GameSessionResult) { const state = useProgressStore.getState(); state.setProgress({ streak: state.streak, xp: result.total_xp, skills: result.skills, achievements: result.achievements as AchievementId[], gameStats: { gamesPlayed: result.games_played, questionsAnswered: result.questions_answered, correctAnswers: result.correct_answers, bestRoundScore: result.best_round_score, dailyChallengesCompleted: result.daily_challenges_completed, lastDailyChallengeDate: result.last_daily_challenge_date, currentCorrectStreak: result.current_correct_streak, bestCorrectStreak: result.best_correct_streak } }); markLearningProgressUpdated() }
export function EducationalGameSession(props: Props) { const id = useAuthStore((s) => s.user?.id); const key = `${id}:${props.targetLanguage}:${props.difficulty}:${props.gameId}`; return ARCADE.has(props.gameId) ? <ArenaGame key={key} {...props} /> : <QuestionRound key={key} {...props} /> }

function QuestionRound({ gameId, language, difficulty, arabic, title, mechanic, format, onExit, onReplay }: Props) {
 const [session, setSession] = useState<GameSessionStartResponse | null>(null); const [question, setQuestion] = useState<GameSessionQuestion | null>(null); const [feedback, setFeedback] = useState<GameSessionNextResponse | null>(null); const [result, setResult] = useState<GameSessionResult | null>(null); const [loading, setLoading] = useState(true); const [busy, setBusy] = useState(false); const [error, setError] = useState(''); const [value, setValue] = useState(''); const [selected, setSelected] = useState(''); const epoch = useRef(0); const answers = useRef<Array<{ question_id: string; choice: string }>>([])
 useEffect(() => { const n = ++epoch.current; void startGameSession(gameId, language, difficulty, gameId === 'review_mix').then((data) => { if (n !== epoch.current) return; if (!data.questions.length && !data.interaction) throw new Error('empty'); setSession(data); setQuestion(data.questions[0] ?? null); setLoading(false) }).catch(() => { if (n === epoch.current) { setLoading(false); setError(tx(arabic, 'تعذر بدء اللعبة. تحقق من وجود خطة نشطة ثم أعد المحاولة.', 'Could not start the game. Check your active plan and retry.')) } }); return () => { epoch.current += 1 } }, [arabic, difficulty, gameId, language])
 async function submit(answer: string) { if (!session || !question || busy || feedback || !answer.trim()) return; setBusy(true); try { const next = await answerGameSessionQuestion(session.session_id, question.id, answer.trim()); if (next.correct) answers.current = [...answers.current.filter((a) => a.question_id !== question.id), { question_id: question.id, choice: answer.trim() }]; setSelected(answer); setFeedback(next) } catch { setError(tx(arabic, 'تعذر تصحيح الإجابة.', 'Validation failed.')) } finally { setBusy(false) } }
 async function finish() { if (!session || busy || result) return; setBusy(true); try { const saved = await completeGameSession(session.session_id, answers.current, session.daily_challenge, session.daily_challenge_date, []); setResult(saved); saveResult(saved) } catch { setError(tx(arabic, 'تعذر حفظ الجولة.', 'Could not save the round.')) } finally { setBusy(false) } }
 function next() { if (!feedback || busy) return; if (feedback.finished) { void finish(); return } setQuestion(feedback.question); setFeedback(null); setSelected(''); setValue('') }
 if (loading) return <section className="edu-stage" aria-busy="true"><p role="status">{tx(arabic, 'جارٍ تجهيز الجولة…', 'Preparing the round…')}</p><button onClick={onExit}>{tx(arabic, 'العودة', 'Back')}</button></section>
 return <section className={`edu-stage game-session-stage format-${format ?? 'recall'}`} aria-busy={busy}><header className="edu-session-head"><button onClick={onExit} disabled={busy}>{tx(arabic, 'الألعاب', 'Games')}</button><div><span className="game-session-format">{mechanic}</span><h2>{title}</h2></div></header>{error && <p className="edu-error" role="alert">{error}</p>}{result ? <div className="edu-result" role="status"><h3>{tx(arabic, 'تم حفظ الجولة', 'Round saved')}</h3><p>{result.round_correct}/{result.round_questions} · +{result.xp_earned} XP</p><button className="edu-primary" onClick={onReplay}>{tx(arabic, 'جولة جديدة', 'New round')}</button><button onClick={onExit}>{tx(arabic, 'اختيار لعبة أخرى', 'Choose another game')}</button></div> : question ? <><div className="game-session-coach"><span><Check size={16} />{mechanic}</span><span>{tx(arabic, 'التصحيح على الخادم', 'Server validated')}</span></div><progress value={feedback?.answered ?? 0} max={feedback?.total ?? session?.questions.length ?? 1} aria-label={tx(arabic, 'تقدم الجولة', 'Round progress')} /><h3 className="edu-prompt" dir="auto">{question.prompt}</h3>{question.input_mode === 'text' ? <form className="edu-answer-form" onSubmit={(e) => { e.preventDefault(); void submit(value) }}><label htmlFor="game-answer">{tx(arabic, 'إجابتك', 'Your answer')}</label><input id="game-answer" value={value} onChange={(e) => setValue(e.target.value)} disabled={busy || !!feedback} autoComplete="off" /><button className="edu-primary" disabled={busy || !!feedback || !value.trim()}>{tx(arabic, 'تحقق', 'Check')}</button></form> : <div className="edu-choices">{question.choices.map((choice, i) => <button key={`${i}:${choice}`} disabled={busy || !!feedback} aria-pressed={selected === choice} onClick={() => void submit(choice)}><span>{i + 1}</span><b dir="auto">{choice}</b></button>)}</div>}{feedback && <div className="edu-feedback" data-correct={feedback.correct} role="status"><strong>{feedback.correct ? tx(arabic, 'صحيح!', 'Correct!') : tx(arabic, 'ليست صحيحة', 'Not quite')}</strong><p>{question.hint}</p><button className="edu-primary" onClick={next} disabled={busy}>{feedback.finished ? tx(arabic, 'حفظ الجولة', 'Save round') : tx(arabic, 'التالي', 'Next')}</button></div>}</> : <button className="edu-primary" onClick={onReplay}>{tx(arabic, 'إعادة المحاولة', 'Retry')}</button>}</section>
}

export function ArenaGame({ gameId, targetLanguage, difficulty, arabic, title, mechanic, onExit, onReplay }: Props) {
 const userId = useAuthStore((s) => s.user?.id); const key = `juba:arcade:${userId}:${targetLanguage}:${gameId}:${difficulty}`; const [state, setState] = useState<ArenaState | null>(null); const [busy, setBusy] = useState(false); const [error, setError] = useState(''); const [order, setOrder] = useState<string[]>([]); const [left, setLeft] = useState<string | null>(null); const snapshot = useRef<ArenaState | null>(null); const pending = useRef<ArenaMove | null>(null); const text = (a: string, e: string) => tx(arabic, a, e)
 const activeRequest = useRef<AbortController | null>(null)
 const alive = useRef(false)
 const appliedResult = useRef<string | null>(null)
 const [relaxed, setRelaxed] = useState(false)
 const [still, setStill] = useState(false)
 const clearSaved = () => { try { sessionStorage.removeItem(key) } catch {} }
 const accept = (next: ArenaState) => {
   if (!alive.current) return
   snapshot.current = next
   setState(next); setOrder([]); setLeft(null); setError('')
   try { next.phase === 'finished' ? sessionStorage.removeItem(key) : sessionStorage.setItem(key, next.session_id) } catch {}
   if (next.result && appliedResult.current !== next.session_id) {
     appliedResult.current = next.session_id
     saveResult(next.result)
   }
 }
 useEffect(() => {
   alive.current = true
   const controller = new AbortController()
   activeRequest.current = controller
   let saved: string | null = null
   try { saved = sessionStorage.getItem(key) } catch {}
   if (saved) {
     setBusy(true)
     void readArena(saved, controller.signal).then(next => { if (!controller.signal.aborted) accept(next) }).catch((err: unknown) => {
       if (!alive.current || controller.signal.aborted) return
       if (err instanceof ArenaRequestError && err.terminal) {
         clearSaved(); snapshot.current = null; setState(null); pending.current = null
         setError(text('انتهت الجولة أو تغيرت خطة التعلم. ابدأ جولة جديدة.', 'Round expired or learning plan changed. Start a new round.'))
       } else setError(text('تعذر استعادة الجولة. أعد المحاولة.', 'Could not restore the round. Retry.'))
     }).finally(() => { if (alive.current && !controller.signal.aborted) setBusy(false) })
   }
   return () => { alive.current = false; activeRequest.current?.abort(); pending.current = null }
   // Session identity changes remount this component through its parent key.
   // eslint-disable-next-line react-hooks/exhaustive-deps
 }, [key])
 async function start() {
   if (activeRequest.current && !activeRequest.current.signal.aborted && busy) return
   const controller = new AbortController()
   activeRequest.current = controller
   setBusy(true); setError('')
   try {
     let saved: string | null = null
     try { saved = sessionStorage.getItem(key) } catch {}
     accept(saved ? await readArena(saved, controller.signal) : await startArena(gameId, targetLanguage, difficulty, relaxed, controller.signal))
   } catch (err) {
     if (!alive.current || controller.signal.aborted) return
     if (err instanceof ArenaRequestError && err.terminal) {
       clearSaved(); snapshot.current = null; setState(null); pending.current = null
       setError(text('انتهت الجولة أو تغيرت خطة التعلم. ابدأ جولة جديدة.', 'Round expired or learning plan changed. Start a new round.'))
     } else setError(text('تعذر بدء الجولة. أعد المحاولة.', 'Could not start the round. Retry.'))
   } finally { if (alive.current && !controller.signal.aborted) setBusy(false) }
 }
 async function send(kind: ArenaMove['kind'], value = '', orderValue: string[] = []) {
   const current = snapshot.current
   if (!current || busy) return
   const controller = new AbortController()
   activeRequest.current = controller
   setBusy(true)
   const move = pending.current ?? { action_id: crypto.randomUUID(), version: current.version, kind, value, order: orderValue }
   pending.current = move
   try {
     const nextState = await submitArenaMove(current.session_id, move,
       (id, payload) => moveArena(id, payload, controller.signal),
       id => readArena(id, controller.signal))
     if (!alive.current || controller.signal.aborted) return
     pending.current = null; accept(nextState)
   } catch (err) {
     if (!alive.current || controller.signal.aborted) return
     if (err instanceof ArenaRequestError && err.permanent) pending.current = null
     if (err instanceof ArenaRequestError && err.terminal) {
       clearSaved(); setState(null); snapshot.current = null; pending.current = null
       setError(text('انتهت الجولة أو تغيرت خطة التعلم. ابدأ جولة جديدة.', 'Round expired or learning plan changed. Start a new round.'))
     } else if (err instanceof ArenaRequestError && err.permanent) {
       setError(text('رُفضت الحركة. يمكنك متابعة اللعب.', 'Move rejected. You can continue playing.'))
     } else setError(text('تعذر تأكيد الحركة. أعد إرسالها دون تغييرها.', 'Could not confirm the move. Retry the same move.'))
   } finally { if (alive.current && !controller.signal.aborted) setBusy(false) }
 }
 if (!state) return <section className="edu-stage arcade-stage" aria-busy={busy}>
   <div className="arcade-rules"><span className="game-session-format">{mechanic}</span><h3>{title}</h3>
   <p>{text('كل حركة تؤثر في نتيجتك، والتصحيح يتم على الخادم.', 'Every move affects your result and is validated on the server.')}</p>
   {error && <p className="edu-error" role="alert">{error}</p>}
   <label><input type="checkbox" checked={relaxed} disabled={busy} onChange={event => setRelaxed(event.target.checked)} />{text('تدريب دون توقيت، نفس XP', 'Untimed practice, same XP')}</label>
   <button className="edu-primary" onClick={() => void start()} disabled={busy}>{busy ? text('جارٍ التحضير…', 'Preparing…') : text('ابدأ اللعب', 'Start playing')}</button>
   <button onClick={onExit}>{text('العودة للألعاب', 'Back to games')}</button></div></section>
 const frozen = busy || Boolean(pending.current) || state.phase !== 'playing'; const tiles = state.question?.tiles ?? []
 return <section className="edu-stage arcade-stage"><header className="edu-session-head"><button onClick={onExit} disabled={busy}>{text('العودة للألعاب', 'Back to games')}</button><button disabled={busy || Boolean(pending.current) || state.attempts === 0 || state.phase === 'finished'} onClick={() => void send('leave')}>{text('أنهِ واحفظ التعلم', 'End and save learning')}</button><div><span className="game-session-format">{mechanic}</span><h2>{title}</h2></div><Target size={24} /></header>{error && <p className="edu-error" role="alert">{error}</p>}{pending.current && <button disabled={busy} onClick={() => { const move = pending.current; if (move) void send(move.kind, move.value, move.order) }}>{text('أعد إرسال الحركة', 'Retry move')}</button>}<div className="arcade-hud"><span><Check size={18} />{state.correct}/{state.total}</span><span>{[0, 1, 2].map((i) => <Heart key={i} size={20} fill={i < state.lives ? 'currentColor' : 'none'} />)}</span></div>{state.result ? <div className="arcade-result" role="status"><strong className="arcade-emblem">{state.result.won ? '★' : '↻'}</strong><h3>{state.result.won ? text('اجتزت التحدي!', 'Challenge cleared!') : text('انتهت الجولة', 'Round over')}</h3><p>+{state.result.xp_earned} XP</p><button className="edu-primary" onClick={onReplay}>{text('جولة جديدة', 'New round')}</button><button onClick={onExit}>{text('اختر لعبة أخرى', 'Choose another game')}</button></div> : <>{gameId === 'quick_choice' && state.question && <><p className="edu-prompt" dir="auto">{state.question.prompt}</p><label><input type="checkbox" checked={still} onChange={event => setStill(event.target.checked)} />{text("أبقِ الأهداف ثابتة", "Keep targets still")}</label><div className="arcade-hunt" data-still={still}>{state.question.choices?.map((choice) => <button key={choice} disabled={frozen} style={still ? { animation: 'none', transform: 'none' } : undefined} onClick={() => void send('answer', choice)}>{choice}</button>)}</div></>}{(gameId === 'spelling' || gameId === 'word_scramble') && <><p className="edu-prompt">{state.question?.prompt}</p><div className="arcade-letter-pool">{tiles.map((tile) => <button key={tile.id} disabled={frozen || order.includes(tile.id)} onClick={() => setOrder((v) => [...v, tile.id])}>{tile.label}</button>)}</div><button className="edu-primary" disabled={frozen || order.length !== tiles.length} onClick={() => void send('answer', '', order)}>{text('تحقق من الكلمة', 'Check word')}</button></>}{gameId === 'memory' && <div className="arcade-memory">{state.cards?.map((card, i) => <button key={card.id} className="arcade-card" aria-label={card.opened || card.matched ? card.label ?? undefined : text(`بطاقة مخفية ${i + 1}`, `Hidden card ${i + 1}`)} disabled={frozen || card.matched || card.opened} onClick={() => void send('flip', card.id)}>{card.opened || card.matched ? card.label : `#${i + 1}`}</button>)}</div>}{gameId === 'matching' && <div className="edu-matching">{(['word', 'meaning'] as const).map((side) => <div key={side}>{state.cards?.filter((c) => c.side === side).map((card) => <button key={card.id} aria-pressed={side === 'word' ? left === card.id : undefined} disabled={frozen || card.matched || (side === 'meaning' && !left)} onClick={() => side === 'word' ? setLeft(card.id) : left ? void send('pair', '', [left, card.id]) : undefined}>{card.label}</button>)}</div>)}</div>}{state.feedback && <div className="edu-feedback" data-correct={state.feedback.correct} role="status"><strong>{state.feedback.correct ? text('أحسنت!', 'Nice!') : text('حاول مرة أخرى', 'Try again')}</strong><button className="edu-primary" disabled={busy || Boolean(pending.current)} onClick={() => void send(gameId === 'memory' ? 'hide' : 'continue')}>{text('التالي', 'Next')}</button></div>}</>}</section>
}
