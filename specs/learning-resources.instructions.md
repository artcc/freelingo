---
description: "Current-state specification for Grammar, Vocabulary, Phrasebook, progress and competencies, placement-bank resources, and level-completion tests."
applyTo: "backend/app/data/**, backend/app/models/{resource_native_help,progress,competency}.py, backend/app/routers/{grammar,vocabulary,phrasebook,progress,assessment,curriculum}.py, backend/app/services/{resource_native_help,progress_service,assessment}.py, frontend/src/app/(app)/{grammar,vocabulary,phrasebook,progress,assessment,plan}/**, frontend/src/data/curriculum.ts"
---

# Learning Resources

## Purpose and source of truth

Grammar, Vocabulary, Phrasebook, curriculum, and assessment-bank content is defined in backend Python
dataclasses grouped by target language and CEFR level. The frontend retrieves these resources through
authenticated APIs; it does not contain the canonical datasets.

All ten supported target languages provide A1-C2 curriculum, grammar, vocabulary, phrasebook, and
placement-bank data. Dispatchers select exact English variants and ISO-prefix packages for other
languages. Unknown dispatcher input currently falls back to `en-GB` rather than returning an error.

Static resource APIs accept an explicit language query and do not require it to match the user's
active language or owned plans. Frontend resource pages normally send the active language, with
`en-GB` fallback.

## Shared native-language help

Grammar, Vocabulary, and Phrasebook can generate additional help in the authenticated user's native
language. The client chooses target resource/language but cannot override native language.
Help labels resolve the profile's native-language code through the UI locale's `languages` catalog;
`targetLanguages` names only learning languages and cannot label every native language.

Generated help is cached globally in `resource_native_helps` by resource type/key, target language,
native language, and source-content hash. Changing hashed source data invalidates the cache.

Redis uses a 90-second generation lock. A request that finds another generator waits through short
database checks and returns cached content if it appears; otherwise it returns `503` asking the caller
to retry. LLM failures also return `503`.

The lock-acquisition path does not treat every false-like Redis result identically, so strict
single-generation behavior is not guaranteed under all Redis return/failure conditions.

## Grammar reference

Each `GrammarTopic` contains slug, title, CEFR level, free-form category, summary, explanation,
optional structure, rules, examples, common mistakes, and related slugs. Examples use target `text`
with optional translation and note.

Categories are language-specific strings, not a universal 14-value backend enum. Slugs and related
references are checked by data-integrity tests. Lesson grammar references are restricted to slugs
declared by the selected language curriculum, not one fixed global list.

- `GET /api/grammar`: authenticated, `60/minute`; returns all complete topics for the language.
- `GET /api/grammar/{slug}`: authenticated, `60/minute`; returns one topic or `404`.
- `POST /api/grammar/{slug}/native-help`: authenticated, `10/minute`; returns cached/generated help,
  `404` for unknown slug, or `503` when unavailable.

The index groups by CEFR level and searches title, summary, and category. Categories are derived from
returned data. Detail currently loads the full collection and locates the slug locally rather than
calling the single-topic endpoint.

Detail renders explanation, structure, rules, examples, mistakes, and related links. Example
translations returned by the API are not displayed. A1/A2 native help opens and generates on load;
B1-C2 generates when opened. Grammar pages do not provide TTS, flashcard creation, or automatic
current-slug chat context. Lesson `grammar_refs` provide the implemented cross-link.

## Vocabulary hub

A `VocabularySet` contains ID, CEFR level, topic, curriculum `unit_ref`, and entries. Each entry
contains target-language word, part of speech, target-language definition and example, plus optional
IPA and frequency rank. Set IDs need only be unique within one target language; size varies by
language.

- `GET /api/vocabulary`: authenticated, `60/minute`; returns complete sets and entries.
- `GET /api/vocabulary/level/{level}`: authenticated, `60/minute`; level is case-insensitive and an
  invalid level returns `400`.
- `GET /api/vocabulary/{set_id}`: authenticated, `60/minute`; returns one set or `404`.
- `POST /api/vocabulary/{set_id}/native-help`: authenticated, `10/minute`; uses the shared cache and
  returns `404`/`503` under the shared rules.

The index groups and filters by level and searches set topic or ID; it does not search inside words
or show deck coverage. Detail shows word, part of speech, IPA, frequency, definition, and example.

The available deck action adds the entire set through flashcard bulk creation. There is no per-entry
add control. Bulk creation requires the active plan and deduplicates normalized words within it. The
page currently sends an empty translation and the bulk endpoint does not generate one.

Vocabulary native help begins collapsed and is generated on request. Progress treats an item as
covered only when its plan-owned flashcard has `repetitions > 0`.

## Phrasebook

Each category contains ID, CEFR level, situation, icon, and phrases. Phrases contain target-language
text, context, register (`formal`, `neutral`, or `informal`), optional unit reference, and optional
romanization. CJK resources provide romanization data, though the current page does not display it.

- `GET /api/phrasebook`: authenticated, `60/minute`; returns all categories.
- `GET /api/phrasebook/level/{level}`: authenticated, `60/minute`; invalid level returns `400`.
- `GET /api/phrasebook/{category_id}`: authenticated, `60/minute`; unknown category returns `404`.
- `POST /api/phrasebook/{category_id}/native-help`: authenticated, `10/minute`; uses shared cache.
- `GET /api/phrasebook/audio/{category_id}/{phrase_index}`: authenticated, `30/minute`; returns
  cached MP3, `404` for invalid category/index, or `503` without TTS.

Phrase audio is stored below `{AUDIO_STORAGE_PATH}/phrasebook/{iso}/`. Instruction-capable OpenAI
models use a synthesis hash covering text, language, model, voice, speed, format, and instructions;
other providers/models retain a hash of language, category, index, and text. Generation writes a
temporary file and replaces atomically. Responses use `Cache-Control: no-store`, and browser playback
bypasses its HTTP cache while retaining the backend disk cache. The endpoint passes the full target
language to TTS for pronunciation guidance when supported by the configured model.

The page filters A1-C2, register, and target text. It searches phrase text but not context. Categories
display phrases directly rather than through expansion controls. Each phrase has explicit audio and
copy buttons; clicking text itself does not copy.

A1/A2 help panels begin open but generation still requires button action. B1-C2 begins closed. Help
state can survive an active-language change when category IDs are reused. Phrasebook does not create
flashcards.

## Progress and competencies

Progress has daily rows per user, plan, and date with XP, lessons, exercises, streak, and skill JSON.
`UserCompetency` stores one row per user, plan, unit, and competency text.

The Progress screen shows current-plan XP, today's XP, the current streak, seven-day activity,
lesson count and lesson-exercise accuracy through the shared dashboard overview. Accuracy remains
unset before any lesson exercises. Daily history supplies a rolling 28-day XP chart and activity
calendar, including zero-XP practice and inactive gaps, using UTC dates. A reward guide explains
the existing sources, thresholds and daily limits with links to practice. It is guidance rather
than a per-source XP breakdown or a record of earned milestones. Competencies, vocabulary coverage
and recent skill performance remain separate from participation rewards.

### Activity and rewards

Activity days use UTC. Submitted Reading/Listening attempts count even with zero correct answers
or zero replay XP; conversations count after a distinct learner contribution receives a persisted
nonempty tutor response. Greetings, unanswered contributions, and planless conversations do not count.
The current streak is the latest stored streak only if its date is today or yesterday; otherwise it is
zero. New daily rows carry forward the previous row's skill snapshot before applying scored updates.
Daily rows also retain ordered scores per skill in `skill_updates`. Under the same plan lock and
transaction, a late write reconciles every later row's streak from consecutive activity dates and
replays each later day's own scores against its corrected predecessor, rounding each EMA update to
three decimals. Gaps reset streaks but do not discard skills; XP and daily counters stay on their
original dates. Same-day scores retain their persistence order. Legacy rows with null `skill_updates`
remain opaque skill checkpoints: their original score sequences are not inferred or backfilled.
Reconciliation preserves those checkpoints and uses them as the baseline for following tracked days.

Conversation activity uses the persisted assistant response's UTC completion date. Each eligible
response has a unique `reply_to_id` pointing to its learner message; both messages carry the actual
turn `modality` (`chat` or `voice`). Conversation origin is only descriptive. Counting follows these
associations rather than message order, including replies completed after a prompt's UTC day ends.
Unpaired legacy messages are not reconstructed or classified for rewards. Text continuation of voice
history counts only toward chat thresholds/caps and does not consume the voice reward.

Comprehension captures `completed_at` once on entry to submission. Its date is used for replay
eligibility, source key, ledger, and daily progress. Conversation rewards likewise pass the persisted
response date through all daily checks and writes. Database waits never recalculate the activity day.
Voice captures the response completion timestamp in the successful processing path before scheduling
the background transcript task, so task scheduling delays cannot move activity to another UTC day.

Base rewards are 20 XP for lesson completion, 5/1 for correct/incorrect lesson exercises, 2 per
flashcard review, and 10 per correct first-attempt Reading/Listening answer. Additional rewards:

- Voice: 20 XP after three distinct answered learner contributions in a conversation on a UTC day,
  once per conversation/day, at most 60 XP per plan/day. Lesson practice shares this reward.
- Text chat: 10 XP per block of five distinct answered contributions in a conversation/day, at most
  30 XP per plan/day across conversations. Whitespace and case differences do not make a new contribution.
- Reading/Listening replay: 5 XP per exercise/plan/UTC day when an attempt for that exercise in that
  plan exists on an earlier UTC day. Other replays give zero XP. All submitted attempts count as activity.
- Unit: 30 XP once per plan/unit, after all its persisted schedule slots have completed lesson rows.
  Future scheduled lessons must also be complete, not just already generated lessons.
- Level: 100 XP once per plan, after all scheduled teaching lessons and the level test are complete,
  independently of the test score. Current/legacy completion-test slots are excluded.
- Games: 5 XP for completion plus 2 per fully correct challenge: both steps in Error Detective,
  an accepted arrangement in Sentence Order, or a Vocabulary Pair with neither item involved in an
  incorrect attempt. The three games share a limit of 45 game XP per plan/UTC day. Remaining daily
  allowance can partially credit completion. Accepted answers count as activity even when there is
  no XP. Games do not update lesson/exercise completion counters, skills or competencies. Completion
  and rewards are transactional and retry-safe.

`progress_rewards.py` records additional awards in `progress_rewards`. A unique plan/kind/source key
and a PostgreSQL `FOR NO KEY UPDATE` plan-row lock protect repeat requests and daily limits without
conflicting with FK `KEY SHARE` locks held by concurrent inserts. Award and daily credit share
the caller's transaction. Comprehension attempt persistence shares that transaction. Existing totals
are preserved; no historical reward backfill is performed. A qualifying milestone submitted again
may receive its first award if its ledger key does not yet exist. Lesson completion checks both unit
and level milestones, including when the level test was recorded before the last teaching lesson.
Resubmitting an already-completed lesson checks the same milestones without repeating base lesson XP,
completion counters, competencies, or quota consumption, and preserves its original `completed_at`.
Any newly granted milestone uses the resubmission's UTC activity day; an already-awarded milestone
does not create new activity. All eligible milestone awards share the completion transaction and its
single captured activity date. Rewards describe participation and
completion, not linguistic mastery. Ownership comes from the persisted conversation/lesson/plan or
the validated comprehension attempt context, never from mutable client selection.

Exercise skill uses lesson type as its key. Updates apply `0.7 * previous + 0.3 * latest`; a new skill
starts at the latest score. Lesson completion applies the lesson's mean answered-exercise score, or
0.5 when none is available, to every competency in the unit. Mastery is `score >= 0.80`.

- `GET /api/progress/summary`: authenticated, `60/minute`; summarizes the active plan, returns zeros
  without one, and exposes skill JSON from the latest daily row. Includes `today_xp` and seven
  chronological `activity_week` entries (`date`, `active`, `xp`), ending on the current UTC day.
- `GET /api/progress/history`: authenticated, `60/minute`; returns up to 90 recent daily rows.
- `GET /api/progress/competencies`: authenticated, `60/minute`; returns unit ID, average score,
  mastered count, and total count, or an empty list without a plan.

The Progress page combines summary, daily history, unit aggregates, plan, curriculum, vocabulary,
and flashcards. It waits for local language switching to finish and reconciles missing or invalidated
language context before loading these resources. Failed reconciliation and curriculum HTTP errors
show a retry action; an unsuccessful curriculum request is not treated as an empty collection.
These frontend guards do not make active-plan endpoints atomic across concurrent changes in other
tabs; their responses do not expose a shared context identity for verification.
Because the API does not return individual competency status, the page
presents the first `mastered_count` curriculum competencies as mastered and cannot identify the
actual mastered items. Unit bars use mastered count rather than average score.

Vocabulary coverage is calculated from reviewed plan-owned cards. Skill display uses the latest
daily skill JSON and may contain any lesson-type key, not only four fixed skills.

## Placement assessment bank

The placement bank contains target-language questions across A1-C2 and grammar, vocabulary, and
reading. Questions include ID, skill, difficulty, prompt, options, correct option, and optional
grammar slug.

- `GET /api/assessment/bank`: authenticated, `60/minute`; returns the bank including correct answers.
- `POST /api/assessment/evaluate`: authenticated, `60/minute`; evaluates submitted answer records.
- `POST /api/assessment/complete`: authenticated, `10/minute`; creates the selected-language plan.

After successful completion, the frontend invalidates and refreshes the shared language/plan summary
before navigating to Plan or showing the voice-trial offer. If this bounded refresh fails, completion
still proceeds, and the summary remains marked for refresh. Listening and Reading recover that
context before using it; a summary failure must not cause the plan-creation request to be repeated.

The client calculates each `correct` boolean. Evaluation trusts submitted question metadata and does
not retrieve the bank to verify selected options. The deterministic algorithm is described in
`platform.instructions.md`.

Legacy `/assessment/start`, `/submit`, and `/free-write` LLM endpoints remain available but are not
used by the current assessment page.

## Level-completion test

The level test unlocks when the learner reaches the plan's final position
(`progress_day >= duration_weeks × days_per_week − 1`) and no lesson from a passed day is still pending.
Skipped lessons keep the assessment locked until completed and remain reachable through
`/pending-lessons`. Unit competency is informational and does not gate the assessment; the test's own
recommendation handles reinforcement. A persisted result keeps the flow eligible so existing
submissions are never refused. Eligibility is enforced by the backend, not only by a frontend button.

- `GET /api/assessment/level-test/questions/{plan_id}`: authenticated, `5/minute`; gathers grammar
  and vocabulary identifiers from the plan language/level curriculum and asks the LLM for a test.
  Returns 403 before the final position or while a passed-day lesson is pending, unless a result is
  already persisted.
- `POST /api/assessment/level-test/submit`: authenticated, `10/minute`; evaluates submitted answer
  records and persists score/recommendation on the plan. Applies the same eligibility rule and returns
  403 before the final position or while a passed-day lesson is pending, unless a result is already
  persisted.
- `GET /api/assessment/level-test/result/{plan_id}`: authenticated, `60/minute`; returns a recorded
  result. It requires a persisted result and is not affected by eligibility.

The prompt requests 20 questions across grammar, vocabulary, and reading, but generated JSON is not
validated by a Pydantic question schema and correct options are returned to the browser. Submit does
not bind answers to a stored session, verify them against generated questions, require 20 answers, or
prevent resubmission; its only eligibility gate is the final-position and pending-lessons rule above.

Recommendation thresholds are `advance` at 0.75 or above, `extend` from 0.55 to below 0.75, and
`repeat` below 0.55. Score is the mean of three skill profiles, including zero for an absent skill.

Recommendations are persisted, but current frontend actions only navigate to Assessment or Plan.
They do not automatically create a next-level plan, extend duration, focus weak units, or archive and
repeat a plan.

## Navigation

Grammar, Vocabulary, and Phrasebook appear in the Resources group on desktop and mobile. Progress
and Assessment remain learning pages. Middleware checks refresh-cookie presence and every resource
endpoint independently requires backend authentication.

## Related specifications

- `platform.instructions.md` — onboarding and placement journey.
- `study-plan.instructions.md` — curriculum distribution and lesson lifecycle.
- `target-language.instructions.md` and `add-target-language.instructions.md` — language data rules.
- `speech-services.instructions.md` — phrase audio.
- `database-models.instructions.md` and `api-endpoints.instructions.md` — complete contracts.
