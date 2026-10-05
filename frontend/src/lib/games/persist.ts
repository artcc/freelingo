import { apiFetch } from '@/lib/api'
import { completeWithRecovery } from './complete-with-recovery'

export type GameId = 'math' | 'words' | 'quick_choice' | 'context_quest' | 'listen_choose' | 'listening_detective' | 'word_categories' | 'translation_sprint' | 'grammar_duel' | 'spelling' | 'word_scramble' | 'fill_blank' | 'sequence' | 'memory' | 'matching' | 'ordering' | 'sentence_builder' | 'review_mix'
export type GameLanguage = 'ar' | 'fr' | 'en' | 'es' | 'de' | 'it' | 'pt' | 'ja' | 'ko' | 'zh' | 'tr' | 'ru' | 'nl' | 'pl' | 'el' | 'sv' | 'da' | 'no' | 'fi' | 'cs'
export function gameLanguageForTargetLanguage(targetLanguage?:string|null):GameLanguage{
  const base=String(targetLanguage??'').trim().toLowerCase().replace('_','-').split('-')[0]
  const supported:GameLanguage[]=['ar','fr','en','es','de','it','pt','ja','ko','zh','tr','ru','nl','pl','el','sv','da','no','fi','cs']
  return supported.includes(base as GameLanguage)?base as GameLanguage:'en'
}
export type ServerGameStats={total_xp:number;games_played:number;questions_answered:number;correct_answers:number;best_round_score:number;daily_challenges_completed:number;last_daily_challenge_date:string;current_correct_streak:number;best_correct_streak:number;achievements:string[];skills:Record<string,number>}
export type GameSessionQuestion={id:string;prompt:string;choices:string[];hint:string;skill:string;difficulty:number;input_mode?:'choice'|'text';audio_text?:string|null;audio_language?:string|null}
export type GameSessionStartResponse={session_id:string;game_id:string;questions:GameSessionQuestion[];expires_at:string;daily_challenge:boolean;daily_challenge_date:string;interaction?:InteractiveGameChallenge;adaptive_mode?:'new'|'review'|'steady'|'challenge'|'skill_review'|'skill_challenge';effective_difficulty?:number}
// Public challenge items carry only id and label. Pairing and ordering
// solutions stay on the server and are validated from the submitted trace.
export type InteractiveGameChallenge=
 |{type:'memory';cards:Array<{id:string;label:string}>}
 |{type:'matching';left:Array<{id:string;label:string}>;right:Array<{id:string;label:string}>}
 |{type:'ordering';items:Array<{id:string;label:string}>}
export type InteractiveGameTrace={first:string;second:string}|{left:string;right:string}|{order:string[]}
export type ArenaSkill='memory'|'vocabulary'|'writing'
export type GameSessionResult=ServerGameStats&{skill?:ArenaSkill;round_score:number;round_correct:number;round_questions:number;xp_earned:number;skill_results:Record<string,{correct:number;questions:number;accuracy:number;mastery_before?:number;mastery_after?:number;mastery_delta?:number}>;new_achievements:string[]}
async function detail(response:Response):Promise<string>{
  try{const payload=await response.json();if(typeof payload.detail==='string')return payload.detail;if(Array.isArray(payload.detail))return payload.detail.map((i:{msg?:string})=>i.msg).filter(Boolean).join('; ')}catch{}
  return `Game request failed: ${response.status}`
}
export async function startGameSession(gameId:string,language:GameLanguage,difficulty:number,review=false):Promise<GameSessionStartResponse>{
  const response=await apiFetch('/api/progress/game-session',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({game_id:gameId,language,difficulty:Math.min(3,Math.max(1,Math.floor(difficulty))),review})})
  if(!response.ok)throw new Error(await detail(response))
  return response.json()
}
export type GameSessionNextResponse={session_id:string;correct:boolean;question:GameSessionQuestion|null;finished:boolean;answered:number;total:number;adaptive_mode:'new'|'review'|'steady'|'challenge'|'skill_review'|'skill_challenge'}
export async function answerGameSessionQuestion(sessionId:string,questionId:string,choice:string):Promise<GameSessionNextResponse>{
  const response=await apiFetch('/api/progress/game-session/next',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({session_id:sessionId,question_id:questionId,choice})})
  if(!response.ok)throw new Error(await detail(response))
  return response.json()
}
export async function completeGameSession(sessionId:string,answers:Array<{question_id:string;choice:string}>,dailyChallenge=false,dailyChallengeDate='',interactionTrace:InteractiveGameTrace[]=[]):Promise<GameSessionResult>{
  return completeWithRecovery(sessionId,{session_id:sessionId,answers,interaction_trace:interactionTrace,daily_challenge:dailyChallenge,daily_challenge_date:dailyChallengeDate})
}
export type ArenaMove={action_id:string;version:number;kind:'flip'|'hide'|'pair'|'answer'|'timeout'|'continue'|'leave';value:string;order:string[]}
export type ArenaState={
  session_id:string;game:string;skill:ArenaSkill;version:number;phase:'playing'|'feedback'|'finished';index:number;total:number;lives:number;correct:number;attempts:number;max_moves:number;deadline:number|null;server_time?:number;relaxed:boolean
  question?:{prompt:string;choices?:string[];tiles?:Array<{id:string;label:string}>}
  cards?:Array<{id:string;label:string|null;side:'word'|'meaning';opened:boolean;matched:boolean}>
  feedback:{correct:boolean;answer?:string;meaning?:string}|null
  result?:GameSessionResult&{won:boolean}
}
export class ArenaRequestError extends Error{
  constructor(public status:number,message:string){super(message);this.name='ArenaRequestError'}
  get terminal(){return this.status===404||this.status===410||this.message.includes('Learning plan changed')||this.message.includes('Active learning language changed')}
  get permanent(){return this.status>=400&&this.status<500&&this.status!==408&&this.status!==429}
}
async function arenaFetch(path:string,body?:unknown,signal?:AbortSignal):Promise<ArenaState>{
  const response=await apiFetch(path,body===undefined?{signal}:{method:'POST',signal,headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})
  if(!response.ok)throw new ArenaRequestError(response.status,await detail(response))
  return response.json()
}
export function startArena(gameId:string,targetLanguage:string,difficulty:number,relaxed=false,signal?:AbortSignal){return arenaFetch('/api/progress/game-session/arena',{game_id:gameId,target_language:targetLanguage,difficulty,relaxed},signal)}
export function readArena(id:string,signal?:AbortSignal){return arenaFetch('/api/progress/game-session/arena/'+encodeURIComponent(id),undefined,signal)}
export function moveArena(id:string,move:ArenaMove,signal?:AbortSignal){return arenaFetch('/api/progress/game-session/arena/'+encodeURIComponent(id)+'/move',move,signal)}
