import type { GameId } from './persist'

export type GameEngine = 'arena' | 'legacy'
export type GameCategory = 'recall' | 'build' | 'listen' | 'review'

export type GameDefinition = {
  id: GameId
  engine: GameEngine
  category: GameCategory
  icon: string
  ar: string
  en: string
  arDesc: string
  enDesc: string
}

/**
 * The single source of truth for the games catalog.
 * Keep presentation metadata here, while scoring and answers remain server-owned.
 */
export const GAME_REGISTRY = [
  { id: 'memory', engine: 'arena', category: 'recall', icon: '◈', ar: 'ذاكرة الكلمات', en: 'Word memory', arDesc: 'اقلب البطاقات وتذكّر مكان كل كلمة ومعناها.', enDesc: 'Flip cards and remember each word and its meaning.' },
  { id: 'matching', engine: 'arena', category: 'recall', icon: '⇄', ar: 'وصل المعنى', en: 'Meaning match', arDesc: 'صل الكلمات بتعريفاتها، وتعلّم من المحاولات الخاطئة.', enDesc: 'Connect words with their definitions and learn from missed matches.' },
  { id: 'sentence_builder', engine: 'legacy', category: 'build', icon: '▤', ar: 'مهندس الجمل', en: 'Sentence architect', arDesc: 'اختر الكلمات ورتّبها لبناء جملة ثم أرسلها للتصحيح.', enDesc: 'Select and reorder word tiles to build a sentence, then submit it for scoring.' },
  { id: 'quick_choice', engine: 'arena', category: 'recall', icon: '◎', ar: 'صيد المعاني', en: 'Meaning hunt', arDesc: 'اختر المعنى الصحيح، مع أسئلة تتكيّف مع إجاباتك.', enDesc: 'Choose meanings in a round that adapts to your answers.' },
  { id: 'spelling', engine: 'arena', category: 'build', icon: '✎', ar: 'تحدي الإملاء', en: 'Spelling studio', arDesc: 'استرجع الكلمات واكتبها، دون كشف الإجابة مسبقًا.', enDesc: 'Recall and type words without seeing the answer first.' },
  { id: 'listening_detective', engine: 'legacy', category: 'listen', icon: '♪', ar: 'محقق الاستماع', en: 'Listening detective', arDesc: 'شغّل الجملة وحدد الكلمة التي تسمعها.', enDesc: 'Play the sentence and identify the word you hear.' },
  { id: 'grammar_duel', engine: 'legacy', category: 'build', icon: '≋', ar: 'مبارزة القواعد', en: 'Grammar duel', arDesc: 'اكتشف الصيغة الصحيحة وراجع الخطأ قبل الانتقال.', enDesc: 'Find the correct form and revisit mistakes before advancing.' },
  { id: 'fill_blank', engine: 'legacy', category: 'build', icon: '□', ar: 'الكلمة المفقودة', en: 'Missing word', arDesc: 'أكمل سياق الجملة بالكلمة المناسبة.', enDesc: 'Complete the sentence with the appropriate word.' },
  { id: 'word_scramble', engine: 'arena', category: 'build', icon: '↺', ar: 'فكّ الكلمة', en: 'Word unscramble', arDesc: 'حلّ ترتيب الحروف واسترجع الكلمة الصحيحة.', enDesc: 'Solve scrambled letters and retrieve the correct word.' },
  { id: 'review_mix', engine: 'legacy', category: 'review', icon: '↻', ar: 'إنقاذ الكلمات', en: 'Retrieval rescue', arDesc: 'راجع عناصر تحتاج الاسترجاع من سجل تعلّمك الفعلي.', enDesc: 'Retrieve due items from your real learning history.' },
] as const satisfies readonly GameDefinition[]

export function getGameDefinition(id: GameId) {
  return GAME_REGISTRY.find(game => game.id === id)
}

export function isArenaGame(id: GameId) {
  return getGameDefinition(id)?.engine === 'arena'
}
