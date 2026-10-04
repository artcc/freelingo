import { readFile } from 'node:fs/promises'
import path from 'node:path'
import { getRequestConfig } from 'next-intl/server'
import { cookies, headers } from 'next/headers'
import { normalizeLocale } from '@/lib/locales'

export default getRequestConfig(async () => {
  const headerStore = await headers()
  const cookieStore = await cookies()

  // x-next-locale is injected by the middleware on every request (including the
  // very first one, before the NEXT_LOCALE cookie has been written to the client)
  const locale = normalizeLocale(
    headerStore.get('x-next-locale') ?? cookieStore.get('NEXT_LOCALE')?.value
  )

  const messagesDirCandidates = [
    path.join(process.cwd(), 'src', 'messages'),
    path.join(process.cwd(), 'messages'),
    path.join(process.cwd(), '..', 'messages'),
    path.join(process.cwd(), '..', '..', 'messages'),
    path.join(process.cwd(), '..', '..', '..', 'messages'),
  ]

  async function loadMessages(requestedLocale: string) {
    for (const messagesDir of messagesDirCandidates) {
      try {
        const file = await readFile(path.join(messagesDir, `${requestedLocale}.json`), 'utf8')
        return JSON.parse(file)
      } catch {
        // Try the next known runtime location.
      }
    }
    return null
  }

  const englishMessages = await loadMessages('en')
  let messages = locale === 'en' ? englishMessages : await loadMessages(locale)

  if (!englishMessages && !messages) {
    throw new Error('No locale messages were found in the application runtime.')
  }

  // Locale files can be translated incrementally without missing-key failures:
  // every locale inherits the complete English message tree.
  const mergeMessages = (base: unknown, override: unknown): unknown => {
    if (!base || typeof base !== 'object' || Array.isArray(base)) return override ?? base
    if (!override || typeof override !== 'object' || Array.isArray(override)) return base
    const merged: Record<string, unknown> = { ...(base as Record<string, unknown>) }
    for (const [key, value] of Object.entries(override as Record<string, unknown>)) {
      merged[key] = mergeMessages(merged[key], value)
    }
    return merged
  }

  if (englishMessages && messages && locale !== 'en') {
    messages = mergeMessages(englishMessages, messages)
  }

  messages ??= englishMessages
  if (!messages) {
    throw new Error('No locale messages were found in the application runtime.')
  }

  // Keep the runtime resilient while locale JSON files are translated incrementally.
  // These keys are used by the current Progress and vocabulary-review pages but were
  // absent from the checked-in English tree, which caused the whole route to throw.
  const root = messages as Record<string, unknown>
  const progress = (root.progress && typeof root.progress === 'object' && !Array.isArray(root.progress))
    ? root.progress as Record<string, unknown>
    : {}
  Object.assign(progress, {
    learningActivity: locale === 'ar' ? 'النشاط التعليمي' : 'Learning activity',
    exercises: locale === 'ar' ? 'التمارين' : 'Exercises',
    last7Days: locale === 'ar' ? 'آخر 7 أيام' : 'Last 7 days',
    sevenDayXp: locale === 'ar' ? 'نقاط الخبرة خلال 7 أيام' : '7-day XP',
    reviewLink: locale === 'ar' ? 'مراجعة المفردات' : 'Review vocabulary',
  })
  root.progress = progress

  const targetLanguages = (root.targetLanguages && typeof root.targetLanguages === 'object' && !Array.isArray(root.targetLanguages))
    ? root.targetLanguages as Record<string, unknown>
    : {}
  targetLanguages.ar ??= 'Arabic'
  root.targetLanguages = targetLanguages

  const vocabularyReview = (root.vocabularyReview && typeof root.vocabularyReview === 'object' && !Array.isArray(root.vocabularyReview))
    ? vocabularyReviewFrom(root.vocabularyReview as Record<string, unknown>, locale)
    : vocabularyReviewFrom({}, locale)
  root.vocabularyReview = vocabularyReview

  return {
    locale,
    messages: root,
  }
})

function vocabularyReviewFrom(existing: Record<string, unknown>, locale: string): Record<string, unknown> {
  const ar = locale === 'ar'
  const fallback: Record<string, string> = ar ? {
    title: 'مراجعة المفردات', cardsDue: 'بطاقات مستحقة', dueNow: 'مستحق الآن', saved: 'محفوظة', vocabulary: 'المفردات',
    loading: 'جارٍ تحميل المراجعة...', unavailable: 'تعذر تحميل المراجعة', tryAgain: 'إعادة المحاولة', noDue: 'لا توجد كلمات مستحقة للمراجعة',
    caughtUp: 'أحسنت، لا توجد مراجعات مستحقة الآن.', guestHint: 'احفظ كلمات من المترجم لبدء المراجعة.', openVocabulary: 'فتح المفردات', openTranslator: 'فتح المترجم',
    progressLabel: 'التقدم', tapToHear: 'اضغط للاستماع', shortcutHint: 'اختصار لوحة المفاتيح', rateKeys: '1 إلى 4 للتقييم', spaceShortcut: 'المسافة لإظهار الترجمة',
    reveal: 'إظهار الإجابة', again: 'مرة أخرى', hard: 'صعب', good: 'جيد', easy: 'سهل', complete: 'اكتملت المراجعة', reviewed: 'تمت مراجعة {count} كلمات',
    reviewAgain: 'المراجعة مرة أخرى', account: 'الحساب', source: 'المصدر', target: 'الهدف', loadError: 'تعذر تحميل البطاقات', saveError: 'تعذر حفظ المراجعة'
  } : {
    title: 'Vocabulary review', cardsDue: 'cards due', dueNow: 'due now', saved: 'saved', vocabulary: 'Vocabulary',
    loading: 'Loading review...', unavailable: 'Review unavailable', tryAgain: 'Try again', noDue: 'No words due for review',
    caughtUp: 'You are all caught up for now.', guestHint: 'Save words from the translator to start reviewing.', openVocabulary: 'Open vocabulary', openTranslator: 'Open translator',
    progressLabel: 'Progress', tapToHear: 'Tap to hear', shortcutHint: 'Keyboard shortcut', rateKeys: 'Press 1 to 4 to rate', spaceShortcut: 'Press Space to reveal',
    reveal: 'Reveal answer', again: 'Again', hard: 'Hard', good: 'Good', easy: 'Easy', complete: 'Review complete', reviewed: 'Reviewed {count} words',
    reviewAgain: 'Review again', account: 'Account', source: 'source', target: 'target', loadError: 'Could not load cards', saveError: 'Could not save review'
  }
  return { ...fallback, ...existing }
}
